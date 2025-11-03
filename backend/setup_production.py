#!/usr/bin/env python
"""
Script de setup automatique pour la production
Crée un superuser et peuple la database si vide
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.website.models import HeroSection, Service, AboutSection

User = get_user_model()

def create_superuser_if_needed():
    """Crée un superuser admin si aucun superuser n'existe"""
    if not User.objects.filter(is_superuser=True).exists():
        print("[OK] Création du superuser admin...")
        User.objects.create_superuser(
            username='admin',
            email='admin@pinnacle-advisors.tech',
            password='PinnacleAdmin2025!'  # À changer après première connexion!
        )
        print("[OK] Superuser créé: admin / PinnacleAdmin2025!")
        print("[ATTENTION] Changez le mot de passe après première connexion!")
    else:
        print("[OK] Superuser déjà existant")

def populate_if_empty():
    """Peuple la database si elle est vide"""
    if not Service.objects.exists():
        print("[OK] Database vide, peuplement en cours...")

        # Exécuter les scripts de population
        import subprocess
        import sys

        scripts = [
            'scripts/populate_content.py',
            'scripts/seed/create_seo_settings.py',
            'scripts/seed/create_site_settings.py',
        ]

        for script in scripts:
            print(f"[OK] Exécution de {script}...")
            try:
                subprocess.run([sys.executable, script], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERREUR] Échec de {script}: {e}")
            except FileNotFoundError:
                print(f"[AVERTISSEMENT] Script non trouvé: {script}")

        print("[OK] Database peuplée avec succès!")
    else:
        print("[OK] Database déjà peuplée")

if __name__ == '__main__':
    print("=" * 50)
    print("SETUP PRODUCTION - Pinnacle Advisors")
    print("=" * 50)

    create_superuser_if_needed()
    populate_if_empty()

    print("=" * 50)
    print("[OK] Setup terminé!")
    print("=" * 50)
