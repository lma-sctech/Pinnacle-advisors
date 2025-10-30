#!/usr/bin/env python
"""
Test final d'enregistrement des modeles dans Django Admin
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin

print("="*70)
print(" VERIFICATION FINALE - MODELES ENREGISTRES DANS DJANGO ADMIN")
print("="*70)

registered = admin.site._registry

print(f"\nTotal modeles enregistres: {len(registered)}\n")

if len(registered) > 0:
    # Regrouper par app
    apps_dict = {}
    for model in registered.keys():
        app_label = model._meta.app_label
        if app_label not in apps_dict:
            apps_dict[app_label] = []
        apps_dict[app_label].append(model.__name__)

    # Afficher par app
    for app_label in sorted(apps_dict.keys()):
        print(f"[{app_label.upper()}]")
        for model_name in sorted(apps_dict[app_label]):
            admin_class = registered[[m for m in registered if m.__name__ == model_name and m._meta.app_label == app_label][0]]
            print(f"  ✓ {model_name} -> {admin_class.__class__.__name__}")
        print()

    print("="*70)
    print(f"[SUCCESS] {len(registered)} modeles sont enregistres!")
    print("="*70)
    print("\nVous pouvez maintenant:")
    print("1. Demarrer le serveur: python manage.py runserver")
    print("2. Acceder a l'admin: http://localhost:8000/admin/")
    print("3. Se connecter avec:")
    print("   Username: lma")
    print("   Password: admin123")
    print()
else:
    print("[ERREUR] Aucun modele enregistre!")
    print("Verifiez que les fichiers admin.py sont corrects.")
