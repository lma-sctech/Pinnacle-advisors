#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour verifier le flux complet:
ContactSubmission -> Lead creation -> Email notification
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

print("=== Test du flux complet Contact -> Lead -> Email ===\n")

# Compter les leads avant
leads_before = Lead.objects.count()
print(f"[INFO] Leads existants: {leads_before}")

# Créer une soumission avec un profil HOT
print("\n[TEST] Creation d'une ContactSubmission avec profil HOT...")
print("[INFO] Criteres pour HOT (score >= 70):")
print("  - Grande entreprise (30pts)")
print("  - Budget mentionne (20pts)")
print("  - Message urgent (15pts)")
print("  - Besoin strategique (15pts)")
print("  - Message long (10pts)")
print("  - Infos completes (10pts)")
print("  = Total: 100 points\n")

test_submission = ContactSubmission.objects.create(
    name="Sophie Directrice",
    email="sophie.directrice@hotlead-test.com",
    phone="+33612345678",
    company="Test GE Company SA",
    need_type="optimization",
    message="Nous avons un besoin urgent d'optimiser notre supply chain internationale. "
            "Notre entreprise (5000+ employes) cherche une transformation digitale complete "
            "de nos processus logistiques. Budget disponible de 250000 euros. "
            "Nous souhaitons demarrer rapidement ce projet strategique car nous perdons "
            "actuellement beaucoup d'argent sur nos inefficacites operationnelles. "
            "Nous avons besoin d'une solution immediate pour ameliorer nos performances.",
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0 Test Browser"
)

print(f"[OK] ContactSubmission cree: {test_submission}")
print("\n[INFO] Attente du signal pour creer le Lead et envoyer l'email...")
print("[INFO] L'email sera affiche dans la console (EMAIL_BACKEND=console)\n")

# Le signal devrait avoir créé le Lead automatiquement
import time
time.sleep(0.5)  # Petit delai pour laisser le signal se terminer

# Vérifier qu'un Lead a été créé
new_lead = Lead.objects.filter(email="sophie.directrice@hotlead-test.com").first()

if new_lead:
    print("\n" + "="*60)
    print("[SUCCESS] Lead cree avec succes!")
    print("="*60)
    print(f"\n[DETAILS] Informations du Lead:")
    print(f"   ID:              #{new_lead.id}")
    print(f"   Nom:             {new_lead.name}")
    print(f"   Email:           {new_lead.email}")
    print(f"   Entreprise:      {new_lead.company}")
    print(f"   Qualification:   {new_lead.get_qualification_display()}")
    print(f"   Score:           {new_lead.score}/100")
    print(f"   Statut:          {new_lead.get_status_display()}")
    print(f"   Pipeline:        {new_lead.pipeline}")
    print(f"   Source:          {new_lead.get_source_display()}")

    # Vérifier que la soumission est marquée comme traitée
    test_submission.refresh_from_db()
    print(f"\n[OK] Soumission marquee comme traitee: {test_submission.is_processed}")

    if new_lead.qualification == 'hot':
        print("\n[SUCCESS] Lead qualifie comme HOT!")
        print("[INFO] Un email de notification devrait avoir ete envoye")
        print("[INFO] Verifiez la sortie console ci-dessus pour voir l'email\n")
    else:
        print(f"\n[WARNING] Lead qualifie comme {new_lead.qualification.upper()} (attendu: HOT)")
        print(f"[INFO] Score obtenu: {new_lead.score}/100 (minimum pour HOT: 70)")

    # Demander confirmation avant de nettoyer
    print("\n" + "="*60)
    response = input("Voulez-vous supprimer les donnees test? (o/n): ")

    if response.lower() in ['o', 'oui', 'y', 'yes']:
        print("\n[CLEANUP] Nettoyage des donnees test...")
        new_lead.delete()
        test_submission.delete()
        print("[OK] Donnees test supprimees")
    else:
        print("\n[INFO] Donnees test conservees")
        print(f"[INFO] Voir le Lead: http://localhost:8000/admin/crm/lead/{new_lead.id}/change/")

else:
    print("\n[ERROR] Aucun Lead cree! Le signal ne fonctionne pas.")

print("\n=== Test termine ===")
