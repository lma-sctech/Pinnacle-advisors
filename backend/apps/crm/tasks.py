"""
Taches Celery asynchrones pour l'app CRM
"""

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_lead_notification_email(self, lead_id):
    """
    Tache asynchrone pour envoyer l'email de notification d'un nouveau Lead

    Args:
        self: Instance de la task (bind=True)
        lead_id: ID du Lead

    Returns:
        dict: Resultat de l'envoi avec status et message
    """

    try:
        # Importer ici pour eviter les imports circulaires
        from apps.crm.models import Lead

        # Recuperer le Lead
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            logger.error(f"Lead #{lead_id} introuvable pour envoi email")
            return {
                'status': 'error',
                'message': f'Lead #{lead_id} not found'
            }

        # Preparer le contexte pour les templates
        context = {'lead': lead}

        # Generer le contenu HTML et texte
        html_content = render_to_string('emails/crm/new_lead_notification.html', context)
        text_content = render_to_string('emails/crm/new_lead_notification.txt', context)

        # Definir le sujet selon la qualification
        subject_prefix = {
            'hot': '[HOT LEAD]',
            'warm': '[WARM LEAD]',
            'cold': '[COLD LEAD]',
            'unqualified': '[NOUVEAU LEAD]',
        }.get(lead.qualification, '[NOUVEAU LEAD]')

        subject = f"{subject_prefix} {lead.name} - {lead.company or 'Sans entreprise'}"

        # Creer l'email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.CRM_NOTIFICATION_EMAILS,
        )

        # Attacher la version HTML
        email.attach_alternative(html_content, "text/html")

        # Envoyer l'email
        email.send(fail_silently=False)

        logger.info(
            f"[CELERY] Email de notification envoye pour le Lead #{lead.id} ({lead.name}) "
            f"a {', '.join(settings.CRM_NOTIFICATION_EMAILS)}"
        )

        return {
            'status': 'success',
            'message': f'Email sent for Lead #{lead_id}',
            'lead_name': lead.name,
            'lead_qualification': lead.qualification
        }

    except Exception as exc:
        logger.error(
            f"[CELERY] Erreur lors de l'envoi de l'email pour le Lead #{lead_id}: {str(exc)}"
        )

        # Retry la task en cas d'erreur (max 3 fois avec 60s d'intervalle)
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error(
                f"[CELERY] Max retries atteint pour l'envoi email Lead #{lead_id}"
            )
            return {
                'status': 'failed',
                'message': f'Max retries exceeded for Lead #{lead_id}'
            }


@shared_task
def send_lead_status_change_email(lead_id, old_status, new_status):
    """
    Tache asynchrone pour envoyer un email quand le statut d'un Lead change

    Args:
        lead_id: ID du Lead
        old_status: Ancien statut
        new_status: Nouveau statut

    Returns:
        dict: Resultat de l'envoi
    """

    try:
        from apps.crm.models import Lead

        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            logger.error(f"Lead #{lead_id} introuvable pour email changement statut")
            return {'status': 'error', 'message': 'Lead not found'}

        subject = f"[STATUT MODIFIE] {lead.name} - {old_status} -> {new_status}"

        message = f"""
Le statut du Lead #{lead.id} a ete modifie:

Lead: {lead.name} ({lead.email})
Entreprise: {lead.company or 'N/A'}
Ancien statut: {old_status}
Nouveau statut: {new_status}
Qualification: {lead.get_qualification_display()}

Voir le Lead dans le CRM:
http://localhost:8000/admin/crm/lead/{lead.id}/change/

---
Pinnacle Advisors CRM
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.CRM_NOTIFICATION_EMAILS,
        )

        email.send(fail_silently=False)

        logger.info(
            f"[CELERY] Email de changement de statut envoye pour Lead #{lead_id}"
        )

        return {'status': 'success', 'message': f'Status change email sent for Lead #{lead_id}'}

    except Exception as exc:
        logger.error(
            f"[CELERY] Erreur envoi email changement statut Lead #{lead_id}: {str(exc)}"
        )
        return {'status': 'error', 'message': str(exc)}


@shared_task
def cleanup_old_leads():
    """
    Tache periodique pour nettoyer les vieux leads non qualifies (optionnel)
    A configurer avec Celery Beat pour execution automatique

    Returns:
        dict: Nombre de leads nettoyes
    """

    from apps.crm.models import Lead
    from django.utils import timezone
    from datetime import timedelta

    # Supprimer les leads Cold non contactes depuis 6 mois
    cutoff_date = timezone.now() - timedelta(days=180)

    old_leads = Lead.objects.filter(
        qualification='cold',
        status='new',
        created_at__lt=cutoff_date
    )

    count = old_leads.count()

    if count > 0:
        old_leads.delete()
        logger.info(f"[CELERY] {count} vieux leads Cold supprimes")

    return {'status': 'success', 'deleted_count': count}
