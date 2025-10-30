#!/usr/bin/env python
"""
Debug des decorateurs admin.register
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin
from apps.website.models import HeroSection

print("=== DEBUG DECORATEUR @admin.register() ===\n")

# Test 1: Enregistrement manuel direct
print("[TEST 1] Enregistrement manuel avec admin.site.register()")
try:
    admin.site.register(HeroSection)
    print(f"[OK] HeroSection enregistre manuellement")
    print(f"Modeles: {len(admin.site._registry)}")
    admin.site.unregister(HeroSection)  # On le retire pour le test suivant
except Exception as e:
    print(f"[ERREUR] {e}")

# Test 2: Enregistrement avec decorateur
print("\n[TEST 2] Enregistrement avec decorateur @admin.register()")

@admin.register(HeroSection)
class TestHeroAdmin(admin.ModelAdmin):
    list_display = ('title',)

print(f"Apres decorateur: {len(admin.site._registry)} modeles")
if HeroSection in admin.site._registry:
    print("[OK] HeroSection enregistre via decorateur")
else:
    print("[ERREUR] Decorateur n'a pas fonctionne")

# Test 3: Verifier l'instance admin
print("\n[TEST 3] Verification instance admin")
print(f"admin.site: {admin.site}")
print(f"admin.site.__class__: {admin.site.__class__}")
print(f"Type: {type(admin.site)}")

# Test 4: Lire le fichier admin.py et voir s'il s'execute
print("\n[TEST 4] Import fichier admin.py")
import importlib
import apps.website.admin

# Forcer reload
importlib.reload(apps.website.admin)
print(f"Apres reload admin.py: {len(admin.site._registry)} modeles")

if len(admin.site._registry) > 0:
    print("\n=== MODELES ENREGISTRES ===")
    for model in admin.site._registry.keys():
        print(f"  - {model._meta.app_label}.{model.__name__}")
