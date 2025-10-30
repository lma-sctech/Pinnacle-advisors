"""
Script pour créer la configuration SEO initiale
Usage: python create_seo_settings.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import SEOSettings

# Créer la configuration SEO par défaut
seo_settings = SEOSettings.objects.create(
    meta_title='Pinnacle Advisors - Cabinet de Conseil Expert',
    meta_description='Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement. Expertise 360° pour faire de votre supply chain un avantage compétitif.',
    meta_keywords='supply chain, logistique, conseil, optimisation, transformation digitale, WMS, TMS, S&OP',
    author_name='Pinnacle Advisors',
    og_title='Pinnacle Advisors - Cabinet de Conseil Expert',
    og_description='Transformez votre supply chain en avantage compétitif',
    og_locale='fr_FR',
    is_active=True
)

print("[OK] Configuration SEO creee avec succes")
print(f"   ID: {seo_settings.id}")
print(f"   Titre: {seo_settings.meta_title}")
print(f"   Statut: {'Actif' if seo_settings.is_active else 'Inactif'}")
