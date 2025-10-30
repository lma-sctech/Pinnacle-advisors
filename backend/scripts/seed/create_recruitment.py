"""
Script pour créer une section de recrutement par défaut
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import Recruitment

# Supprimer les sections existantes
Recruitment.objects.all().delete()

# Créer une nouvelle section
recruitment = Recruitment.objects.create(
    title="Rejoignez notre équipe",
    description="Vous êtes un expert supply chain passionné ? Nous recherchons des talents pour renforcer notre équipe.",
    cta_text="Voir les opportunités",
    email="recrutement@pinnacle-advisors.tech",
    is_active=True,
    order=0
)

print(f"Section recrutement créée avec succès!")
print(f"- ID: {recruitment.id}")
print(f"- Titre: {recruitment.title}")
print(f"- Email: {recruitment.email}")
print(f"- Statut: {'Actif' if recruitment.is_active else 'Inactif'}")
