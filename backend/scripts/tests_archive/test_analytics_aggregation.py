#!/usr/bin/env python
"""
Script de test pour l'agrégation quotidienne des analytics
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from apps.analytics.tasks import aggregate_daily_analytics, aggregate_all_missing_days
from apps.analytics.models import DailyAnalytics, UserSession

print("=== TEST AGREGATION ANALYTICS ===\n")

# Test 1: Vérifier s'il y a des sessions
print("[TEST 1] Vérification des sessions...")
total_sessions = UserSession.objects.count()
print(f"Total sessions dans la DB: {total_sessions}")

if total_sessions == 0:
    print("⚠️  Aucune session trouvée. Impossible de tester l'agrégation.")
    print("   Créez d'abord des données via l'API de tracking ou le populate script.\n")
else:
    # Test 2: Agréger hier
    print("\n[TEST 2] Agrégation du jour précédent...")
    yesterday = (timezone.now() - timedelta(days=1)).date()
    print(f"Date cible: {yesterday}")

    try:
        result = aggregate_daily_analytics(target_date=yesterday.strftime('%Y-%m-%d'))
        print(f"✓ Résultat: {result}")

        # Vérifier que l'entrée existe
        daily = DailyAnalytics.objects.filter(date=yesterday).first()
        if daily:
            print(f"\n✓ DailyAnalytics créé:")
            print(f"  - Sessions: {daily.total_sessions}")
            print(f"  - Visiteurs uniques: {daily.unique_visitors}")
            print(f"  - Pages vues: {daily.total_pageviews}")
            print(f"  - Durée moyenne: {daily.avg_session_duration} min")
            print(f"  - Bounce rate: {daily.bounce_rate}%")
            print(f"  - Conversion rate: {daily.conversion_rate}%")
            print(f"  - Top pages: {len(daily.top_pages) if daily.top_pages else 0}")
        else:
            print("✗ Erreur: DailyAnalytics non créé")

    except Exception as e:
        print(f"✗ Erreur lors de l'agrégation: {str(e)}")

    # Test 3: Compter les jours agrégés
    print("\n[TEST 3] Jours agrégés existants...")
    aggregated_count = DailyAnalytics.objects.count()
    print(f"Total jours agrégés: {aggregated_count}")

    if aggregated_count > 0:
        first = DailyAnalytics.objects.order_by('date').first()
        last = DailyAnalytics.objects.order_by('-date').first()
        print(f"Première date: {first.date}")
        print(f"Dernière date: {last.date}")

    # Test 4: Agréger tous les jours manquants (optionnel)
    print("\n[TEST 4] Voulez-vous agréger tous les jours manquants? (y/n)")
    response = input().strip().lower()
    if response == 'y':
        print("Lancement de l'agrégation de tous les jours manquants...")
        try:
            result = aggregate_all_missing_days()
            print(f"✓ Résultat: {result}")
        except Exception as e:
            print(f"✗ Erreur: {str(e)}")
    else:
        print("Agrégation complète ignorée.")

print("\n=== FIN DES TESTS ===")
print("\nCommandes utiles:")
print("- Démarrer Celery Worker: celery -A config worker -l info --pool=solo")
print("- Démarrer Celery Beat: celery -A config beat -l info")
print("- Tester tâche manuellement: python manage.py shell")
print("  >>> from apps.analytics.tasks import aggregate_daily_analytics")
print("  >>> aggregate_daily_analytics.delay()")
