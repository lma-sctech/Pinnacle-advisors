#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test du fallback Celery: si Redis n'est pas disponible, l'envoi doit etre synchrone
"""

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import ContactSubmission
from apps.crm.models import Lead

print("=== Test Celery Fallback (sans Redis) ===\n")
print("[INFO] Redis n'est pas demarre -> le systeme devrait utiliser l'envoi synchrone\n")

# Compter les leads avant
leads_before = Lead.objects.count()
print(f"[INFO] Leads existants: {leads_before}")

# Créer une soumission avec un profil WARM
print("\n[TEST] Creation d'une ContactSubmission avec profil WARM...")

test_submission = ContactSubmission.objects.create(
    name="Test Celery Fallback",
    email="test.celery.fallback@pinnacle-test.com",
    phone="+33612345678",
    company="Test Fallback Company",
    need_type="optimization",
    message="Message de test pour verifier le fallback Celery. "
            "Ce message contient les mots cles urgents et strategique pour optimiser "
            "la supply chain. Nous cherchons une transformation digitale rapide et efficace. "
            "Budget disponible pour ce projet important et strategique.",
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0 Test Browser"
)

print(f"[OK] ContactSubmission cree: {test_submission}")
print("\n[INFO] Le signal devrait creer le Lead et tenter Celery...")
print("[INFO] Comme Redis n'est pas disponible, il devrait faire un fallback synchrone")
print("[INFO] Verifiez les logs ci-dessus pour voir 'Celery non disponible'\n")

# Petit delai
import time
time.sleep(0.5)

# Vérifier qu'un Lead a été créé
new_lead = Lead.objects.filter(email="test.celery.fallback@pinnacle-test.com").first()

if new_lead:
    print("\n" + "="*60)
    print("[SUCCESS] Lead cree avec succes!")
    print("="*60)
    print(f"\n[DETAILS] Informations du Lead:")
    print(f"   ID:              #{new_lead.id}")
    print(f"   Nom:             {new_lead.name}")
    print(f"   Email:           {new_lead.email}")
    print(f"   Qualification:   {new_lead.get_qualification_display()}")
    print(f"   Score:           {new_lead.score}/100")

    # Vérifier que la soumission est marquée comme traitée
    test_submission.refresh_from_db()
    print(f"\n[OK] Soumission marquee comme traitee: {test_submission.is_processed}")

    # Nettoyer
    print("\n[CLEANUP] Nettoyage des donnees test...")
    new_lead.delete()
    test_submission.delete()
    print("[OK] Donnees test supprimees")

else:
    print("\n[ERROR] Aucun Lead cree!")

print("\n=== Test termine ===")
print("\n[NOTE] Pour utiliser Celery avec Redis:")
print("  1. Installer Redis pour Windows (voir docs)")
print("  2. Demarrer Redis: redis-server")
print("  3. Demarrer Celery worker: celery -A config worker -l info")
print("  4. Les emails seront alors envoyes de maniere asynchrone")
