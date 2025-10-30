"""
Script pour créer les paramètres globaux du site
Usage: python create_site_settings.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import SiteSettings

# Créer les paramètres du site par défaut
site_settings = SiteSettings.objects.create(
    company_name='Pinnacle Advisors',
    company_tagline='Cabinet de conseil expert en optimisation et transformation des chaînes d\'approvisionnement.',
    navbar_cta_text='Demander un devis',
    mobile_menu_cta_text='Demander un devis',
    footer_nav_title='Navigation',
    footer_services_title='Nos Services',
    footer_follow_title='Suivez-nous',
    footer_hours_label='Horaires d\'ouverture',
    footer_copyright_text='© {year} Pinnacle Advisors. Tous droits réservés.',
    footer_legal_text='Mentions légales',
    footer_privacy_text='Politique de confidentialité',
    footer_terms_text='CGV',
    is_active=True
)

print("[OK] Parametres du site crees avec succes")
print(f"   ID: {site_settings.id}")
print(f"   Entreprise: {site_settings.company_name}")
print(f"   CTA Navbar: {site_settings.navbar_cta_text}")
print(f"   Statut: {'Actif' if site_settings.is_active else 'Inactif'}")
