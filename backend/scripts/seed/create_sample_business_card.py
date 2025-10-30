"""
Script pour créer une carte de visite de démonstration
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import BusinessCard

def create_sample_card():
    """Crée une carte de visite de démonstration"""

    # Supprimer les cartes existantes pour cet exemple
    BusinessCard.objects.all().delete()

    # Créer la carte
    card = BusinessCard.objects.create(
        full_name="Jean Dupont",
        job_title="Directeur Supply Chain",
        tagline="Expert en optimisation de la chaîne logistique et transformation digitale",
        bio="Plus de 15 ans d'expérience dans l'optimisation des processus supply chain pour des entreprises internationales. Spécialisé dans la transformation digitale, l'amélioration continue et la réduction des coûts opérationnels.",
        email="jean.dupont@pinnacle-supply.com",
        phone="+33612345678",
        company_name="Pinnacle Advisors",
        website_url="http://localhost:3000",
        linkedin_url="https://www.linkedin.com/in/example",
        accent_color="#3B82F6",
        background_gradient_start="#3B82F6",
        background_gradient_end="#10B981",
        is_active=True
    )

    print("[OK] Carte de visite creee avec succes!")
    print(f"   ID: {card.id}")
    print(f"   Nom: {card.full_name}")
    print(f"   Poste: {card.job_title}")
    print(f"   Email: {card.email}")
    print(f"   Telephone: {card.phone}")
    print()
    print("[!] IMPORTANT: Vous devez ajouter une photo de profil via l'admin Django:")
    print(f"   >> http://localhost:8000/admin/website/businesscard/{card.id}/change/")
    print()
    print("[i] Accedez a la carte de visite:")
    print("   >> http://localhost:3000/card")
    print()
    print("[i] Pour tester le tracking QR code, ajoutez ?source=qr a l'URL:")
    print("   >> http://localhost:3000/card?source=qr")

if __name__ == '__main__':
    create_sample_card()
