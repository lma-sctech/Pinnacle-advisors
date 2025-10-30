#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de l'enregistrement des modeles dans Django Admin
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin

print("=== TEST ENREGISTREMENT ADMIN ===\n")

# Forcer autodiscover
admin.autodiscover()

# Lister tous les modeles enregistres
registered = admin.site._registry

print(f"Total modeles enregistres: {len(registered)}\n")

if len(registered) == 0:
    print("[ERREUR] Aucun modele enregistre dans l'admin!")
    print("\nImportation manuelle des fichiers admin.py...")

    try:
        import apps.website.admin
        print("[OK] apps.website.admin importe")
    except Exception as e:
        print(f"[ERREUR] apps.website.admin: {e}")

    try:
        import apps.crm.admin
        print("[OK] apps.crm.admin importe")
    except Exception as e:
        print(f"[ERREUR] apps.crm.admin: {e}")

    try:
        import apps.analytics.admin
        print("[OK] apps.analytics.admin importe")
    except Exception as e:
        print(f"[ERREUR] apps.analytics.admin: {e}")

    # Re-verifier
    registered = admin.site._registry
    print(f"\nApres import manuel: {len(registered)} modeles")

if len(registered) > 0:
    print("\n=== MODELES ENREGISTRES ===")
    for model in sorted(registered.keys(), key=lambda x: (x._meta.app_label, x.__name__)):
        app_label = model._meta.app_label
        model_name = model.__name__
        admin_class = registered[model].__class__.__name__
        print(f"  - {app_label}.{model_name} -> {admin_class}")
else:
    print("\n[PROBLEME] Les modeles ne s'enregistrent pas!")
    print("Verifiez que les decorateurs @admin.register() fonctionnent.")
