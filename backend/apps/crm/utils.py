"""
Utilitaires pour l'app CRM
Fonctions d'envoi d'emails de notification
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_new_lead_notification(lead):
    """
    Envoie une notification email quand un nouveau Lead est créé

    Args:
        lead: Instance du modèle Lead

    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """

    try:
        # Préparer le contexte pour les templates
        context = {
            'lead': lead,
        }

        # Générer le contenu HTML et texte
        html_content = render_to_string('emails/crm/new_lead_notification.html', context)
        text_content = render_to_string('emails/crm/new_lead_notification.txt', context)

        # Définir le sujet selon la qualification
        subject_prefix = {
            'hot': '[HOT LEAD]',
            'warm': '[WARM LEAD]',
            'cold': '[COLD LEAD]',
            'unqualified': '[NOUVEAU LEAD]',
        }.get(lead.qualification, '[NOUVEAU LEAD]')

        subject = f"{subject_prefix} {lead.name} - {lead.company or 'Sans entreprise'}"

        # Créer l'email
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
            f"Email de notification envoyé pour le Lead #{lead.id} ({lead.name}) "
            f"à {', '.join(settings.CRM_NOTIFICATION_EMAILS)}"
        )

        return True

    except Exception as e:
        logger.error(
            f"Erreur lors de l'envoi de l'email de notification pour le Lead #{lead.id}: {str(e)}"
        )
        return False


def send_lead_status_change_notification(lead, old_status, new_status):
    """
    Envoie une notification quand le statut d'un Lead change

    Args:
        lead: Instance du modèle Lead
        old_status: Ancien statut
        new_status: Nouveau statut

    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """

    try:
        subject = f"[STATUT MODIFIÉ] {lead.name} - {old_status} → {new_status}"

        message = f"""
Le statut du Lead #{lead.id} a été modifié:

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
            f"Email de changement de statut envoyé pour le Lead #{lead.id}"
        )

        return True

    except Exception as e:
        logger.error(
            f"Erreur lors de l'envoi de l'email de changement de statut "
            f"pour le Lead #{lead.id}: {str(e)}"
        )
        return False
