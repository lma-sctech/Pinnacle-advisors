"""
Script pour créer un en-tête Team par défaut
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import TeamHeader

# Supprimer les en-têtes existants
TeamHeader.objects.all().delete()

# Créer un nouvel en-tête
header = TeamHeader.objects.create(
    title_part1="Notre Équipe",
    title_part2="d'Experts",
    description="Des professionnels passionnés avec plus de 15 ans d'expérience terrain en supply chain",
    is_active=True
)

print(f"En-tête Team créé avec succès!")
print(f"- ID: {header.id}")
print(f"- Titre: {header.title_part1} {header.title_part2}")
print(f"- Description: {header.description}")
print(f"- Statut: {'Actif' if header.is_active else 'Inactif'}")
