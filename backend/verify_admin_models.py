#!/usr/bin/env python
"""
Verification finale de l'enregistrement des modeles dans Django Admin
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Forcer le chargement des apps
from django.apps import apps
apps.get_models()

# Maintenant verifier les modeles enregistres
from django.contrib import admin

print("=== VERIFICATION ADMIN - TOUS LES MODELES ===\n")

registered = admin.site._registry
print(f"Total modeles enregistres: {len(registered)}\n")

if len(registered) > 0:
    apps_dict = {}
    for model in registered.keys():
        app_label = model._meta.app_label
        if app_label not in apps_dict:
            apps_dict[app_label] = []
        apps_dict[app_label].append(model.__name__)

    for app_label in sorted(apps_dict.keys()):
        print(f"[{app_label.upper()}]")
        for model_name in sorted(apps_dict[app_label]):
            print(f"  ✓ {model_name}")
        print()

    print(f"[SUCCESS] {len(registered)} modeles sont enregistres dans l'admin!")
    print("\nVous pouvez maintenant:")
    print("1. Demarrer le serveur: python manage.py runserver")
    print("2. Acceder a l'admin: http://localhost:8000/admin/")
    print("3. Se connecter avec: lma / [votre password]")
else:
    print("[ERREUR] Aucun modele enregistre!")
