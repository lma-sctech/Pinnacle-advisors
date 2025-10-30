#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour verifier que le signal ContactSubmission -> Lead fonctionne
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

print("=== Test du signal ContactSubmission -> Lead CRM ===\n")

# Compter les leads avant
leads_before = Lead.objects.count()
print(f"[INFO] Leads existants: {leads_before}")

# Créer une soumission de contact test
print("\n[TEST] Creation d'une ContactSubmission test...")

test_submission = ContactSubmission.objects.create(
    name="Jean Testeur",
    email="jean.testeur@test-pinnacle.com",
    phone="+33612345678",
    company="Test Company SARL",
    need_type="optimization",
    message="Nous cherchons urgentement a optimiser notre supply chain. "
            "Budget disponible de 150000 euros pour une transformation digitale complete. "
            "Nous sommes une PME avec 150 employes et avons besoin d'aide rapidement.",
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0 Test Browser"
)

print(f"[OK] ContactSubmission cree: {test_submission}")

# Vérifier qu'un Lead a été créé
leads_after = Lead.objects.count()
print(f"\n[INFO] Leads apres creation: {leads_after}")

if leads_after > leads_before:
    print("[SUCCESS] Signal fonctionne! Un Lead a ete cree.")

    # Récupérer le Lead créé
    new_lead = Lead.objects.filter(email="jean.testeur@test-pinnacle.com").first()

    if new_lead:
        print(f"\n[DETAILS] Lead cree:")
        print(f"   - Nom: {new_lead.name}")
        print(f"   - Email: {new_lead.email}")
        print(f"   - Entreprise: {new_lead.company}")
        print(f"   - Source: {new_lead.source}")
        print(f"   - Qualification: {new_lead.get_qualification_display()}")
        print(f"   - Score: {new_lead.score}/100")
        print(f"   - Statut: {new_lead.get_status_display()}")
        print(f"   - Pipeline: {new_lead.pipeline}")

        # Vérifier que la soumission est marquée comme traitée
        test_submission.refresh_from_db()
        print(f"\n[OK] Soumission marquee comme traitee: {test_submission.is_processed}")

        # Nettoyer
        print("\n[CLEANUP] Nettoyage des donnees test...")
        new_lead.delete()
        test_submission.delete()
        print("[OK] Donnees test supprimees")

    else:
        print("[ERROR] Lead introuvable avec l'email test")
else:
    print("[ERROR] Aucun Lead cree! Le signal ne fonctionne pas.")

print("\n=== Test termine ===")
