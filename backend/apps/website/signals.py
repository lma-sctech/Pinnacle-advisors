"""
Django signals pour l'app website
Gestion automatique de la création de Leads CRM depuis ContactSubmission
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError
import logging

from .models import ContactSubmission
from apps.crm.models import Lead, Pipeline

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ContactSubmission)
def create_lead_from_contact(sender, instance, created, **kwargs):
    """
    Signal qui crée automatiquement un Lead CRM quand un ContactSubmission est créé

    Logique:
    - Vérifie si un Lead avec cet email existe déjà
    - Si non, crée un nouveau Lead avec les données du contact
    - Applique l'auto-qualification (hot/warm/cold)
    - Assigne au pipeline par défaut si disponible
    - Log les actions pour traçabilité
    """

    if not created:
        # Ne traiter que les nouvelles soumissions
        return

    # Vérifier si un Lead avec cet email existe déjà
    existing_lead = Lead.objects.filter(email=instance.email).first()

    if existing_lead:
        logger.info(
            f"Lead existant trouvé pour {instance.email}. "
            f"Lead ID: {existing_lead.id}. Nouveau contact ignoré."
        )
        # Marquer la soumission comme traitée
        ContactSubmission.objects.filter(id=instance.id).update(is_processed=True)
        return

    # Mapper les types de besoin ContactSubmission vers format Lead
    need_type_mapping = {
        'optimization': 'Optimisation supply chain',
        'audit': 'Audit et diagnostic',
        'strategy': 'Stratégie logistique',
        'digital': 'Transformation digitale',
        'training': 'Formation',
        'other': 'Autre',
    }

    # Essayer d'obtenir le pipeline par défaut
    default_pipeline = Pipeline.objects.filter(is_active=True).order_by('order').first()

    try:
        # Créer le Lead
        lead = Lead.objects.create(
            name=instance.name,
            email=instance.email,
            phone=instance.phone or '',
            company=instance.company or '',
            company_size='unknown',  # À affiner manuellement dans l'admin
            position='',  # Non disponible depuis le formulaire
            need_type=need_type_mapping.get(instance.need_type, instance.need_type),
            message=instance.message,
            budget_mentioned=False,  # Sera détecté par auto_qualify si keywords présents
            estimated_budget=None,
            qualification='unqualified',  # Sera calculé par auto_qualify()
            status='new',
            pipeline=default_pipeline,
            source='website',
            ip_address=instance.ip_address,
            user_agent=instance.user_agent,
            internal_notes=f"Lead créé automatiquement depuis le formulaire de contact (ID: {instance.id})"
        )

        # Le Lead.save() appelle automatiquement auto_qualify()
        # qui calcule le score et définit la qualification (hot/warm/cold)

        logger.info(
            f"✅ Lead créé avec succès: {lead.name} ({lead.email}) - "
            f"Qualification: {lead.get_qualification_display()} (Score: {lead.score}/100)"
        )

        # Marquer la soumission comme traitée
        ContactSubmission.objects.filter(id=instance.id).update(is_processed=True)

        # Envoyer notification email pour les leads Hot et Warm
        if lead.qualification in ['hot', 'warm']:
            # Essayer d'utiliser Celery (asynchrone) si disponible
            # Sinon fallback vers envoi synchrone
            try:
                from apps.crm.tasks import send_lead_notification_email
                # Envoyer via Celery (asynchrone)
                send_lead_notification_email.delay(lead.id)
                logger.info(f"📧 [CELERY] Task envoi email mise en queue pour Lead #{lead.id}")
            except Exception as celery_error:
                # Si Celery/Redis n'est pas disponible, utiliser envoi synchrone
                logger.warning(
                    f"⚠️ Celery non disponible ({str(celery_error)}). "
                    f"Envoi synchrone pour Lead #{lead.id}"
                )
                try:
                    from apps.crm.utils import send_new_lead_notification
                    send_new_lead_notification(lead)
                    logger.info(f"📧 Email de notification envoyé (sync) pour Lead #{lead.id}")
                except Exception as email_error:
                    logger.error(f"❌ Erreur envoi email pour Lead #{lead.id}: {str(email_error)}")

    except IntegrityError as e:
        logger.error(
            f"❌ Erreur création Lead pour {instance.email}: {str(e)}. "
            f"Probablement un doublon d'email."
        )
    except Exception as e:
        logger.error(
            f"❌ Erreur inattendue lors de la création du Lead pour {instance.email}: {str(e)}"
        )
