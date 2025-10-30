"""
Tâches Celery pour l'app Analytics - Agrégation quotidienne
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from datetime import timedelta, datetime
import logging

from .models import UserSession, PageView, Event, HeatmapData, DailyAnalytics

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='analytics.aggregate_daily_analytics')
def aggregate_daily_analytics(self, target_date=None):
    """
    Tâche périodique pour agréger les analytics quotidiennes
    Exécutée chaque jour à minuit + 5 minutes (cron: 0 5 * * *)

    Args:
        target_date: Date cible (str format YYYY-MM-DD). Si None, utilise hier.

    Returns:
        dict: Statistiques agrégées
    """
    try:
        # Déterminer la date cible
        if target_date:
            target = datetime.strptime(target_date, '%Y-%m-%d').date()
        else:
            # Par défaut: jour précédent
            target = (timezone.now() - timedelta(days=1)).date()

        logger.info(f"[CELERY] Début agrégation analytics pour {target}")

        # Vérifier si l'agrégation existe déjà
        existing = DailyAnalytics.objects.filter(date=target).first()
        if existing:
            logger.warning(f"[CELERY] Agrégation déjà existante pour {target}, écrasement...")
            existing.delete()

        # 1. SESSIONS
        sessions_query = UserSession.objects.filter(start_time__date=target)
        total_sessions = sessions_query.count()

        if total_sessions == 0:
            logger.info(f"[CELERY] Aucune session pour {target}, création entrée vide")
            DailyAnalytics.objects.create(
                date=target,
                total_sessions=0,
                unique_visitors=0,
                total_pageviews=0,
                avg_session_duration=0,
                bounce_rate=0,
                conversion_rate=0,
                top_pages=[]
            )
            return {
                'status': 'success',
                'date': str(target),
                'total_sessions': 0,
                'message': 'No data for this day'
            }

        # 2. VISITEURS UNIQUES (par IP)
        unique_visitors = sessions_query.values('ip_address').distinct().count()

        # 3. PAGES VUES
        total_pageviews = PageView.objects.filter(
            viewed_at__date=target
        ).count()

        # 4. DURÉE MOYENNE SESSION (en minutes)
        avg_duration_seconds = sessions_query.filter(
            duration_seconds__gt=0
        ).aggregate(avg=Avg('duration_seconds'))['avg'] or 0
        avg_session_duration = round(avg_duration_seconds / 60, 2)

        # 5. BOUNCE RATE (sessions avec 1 seule page)
        bounce_sessions = sessions_query.filter(pages_visited=1).count()
        bounce_rate = round((bounce_sessions / total_sessions) * 100, 2)

        # 6. CONVERSION RATE
        converted_sessions = sessions_query.filter(converted=True).count()
        conversion_rate = round((converted_sessions / total_sessions) * 100, 2)

        # 7. TOP PAGES (Top 20)
        top_pages_query = PageView.objects.filter(
            viewed_at__date=target
        ).values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')[:20]

        top_pages = [
            {
                'url': page['page_url'],
                'views': page['views']
            }
            for page in top_pages_query
        ]

        # CRÉER L'ENTRÉE DailyAnalytics
        daily_analytics = DailyAnalytics.objects.create(
            date=target,
            total_sessions=total_sessions,
            unique_visitors=unique_visitors,
            total_pageviews=total_pageviews,
            avg_session_duration=avg_session_duration,
            bounce_rate=bounce_rate,
            conversion_rate=conversion_rate,
            top_pages=top_pages
        )

        logger.info(
            f"[CELERY] ✓ Agrégation terminée pour {target}: "
            f"{total_sessions} sessions, {unique_visitors} visiteurs uniques, "
            f"{conversion_rate}% conversion"
        )

        return {
            'status': 'success',
            'date': str(target),
            'total_sessions': total_sessions,
            'unique_visitors': unique_visitors,
            'total_pageviews': total_pageviews,
            'avg_session_duration': avg_session_duration,
            'bounce_rate': bounce_rate,
            'conversion_rate': conversion_rate,
            'top_pages_count': len(top_pages)
        }

    except Exception as e:
        logger.error(f"[CELERY] ✗ Erreur agrégation analytics pour {target}: {str(e)}")
        # Retry automatique en cas d'erreur
        raise self.retry(exc=e, countdown=300, max_retries=3)


@shared_task(name='analytics.cleanup_old_heatmap_data')
def cleanup_old_heatmap_data(days=180):
    """
    Nettoie les anciennes données heatmap (> X jours)
    Pour éviter une croissance excessive de la DB

    Args:
        days: Nombre de jours à conserver (défaut: 180 jours = 6 mois)

    Returns:
        dict: Nombre d'entrées supprimées
    """
    try:
        cutoff_date = (timezone.now() - timedelta(days=days)).date()

        logger.info(f"[CELERY] Nettoyage heatmap data avant {cutoff_date}")

        # Supprimer les vieilles données
        deleted_count = HeatmapData.objects.filter(date__lt=cutoff_date).delete()[0]

        logger.info(f"[CELERY] ✓ {deleted_count} entrées heatmap supprimées")

        return {
            'status': 'success',
            'deleted_count': deleted_count,
            'cutoff_date': str(cutoff_date)
        }

    except Exception as e:
        logger.error(f"[CELERY] ✗ Erreur nettoyage heatmap: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task(name='analytics.aggregate_all_missing_days')
def aggregate_all_missing_days():
    """
    Tâche pour agréger tous les jours manquants depuis le début des données
    Utile pour remplir les trous si la tâche quotidienne n'a pas tourné
    """
    try:
        logger.info("[CELERY] Début agrégation de tous les jours manquants")

        # Trouver la date de la première session
        first_session = UserSession.objects.order_by('start_time').first()
        if not first_session:
            logger.info("[CELERY] Aucune session trouvée")
            return {'status': 'success', 'message': 'No sessions found'}

        start_date = first_session.start_time.date()
        today = timezone.now().date()

        # Obtenir toutes les dates déjà agrégées
        existing_dates = set(
            DailyAnalytics.objects.values_list('date', flat=True)
        )

        # Trouver les dates manquantes
        current_date = start_date
        missing_dates = []

        while current_date < today:
            if current_date not in existing_dates:
                missing_dates.append(current_date)
            current_date += timedelta(days=1)

        logger.info(f"[CELERY] {len(missing_dates)} jours manquants trouvés")

        # Agréger chaque jour manquant
        aggregated = 0
        for date in missing_dates:
            try:
                aggregate_daily_analytics(target_date=date.strftime('%Y-%m-%d'))
                aggregated += 1
            except Exception as e:
                logger.error(f"[CELERY] Erreur agrégation {date}: {str(e)}")

        logger.info(f"[CELERY] ✓ {aggregated}/{len(missing_dates)} jours agrégés")

        return {
            'status': 'success',
            'missing_dates': len(missing_dates),
            'aggregated': aggregated
        }

    except Exception as e:
        logger.error(f"[CELERY] ✗ Erreur agrégation jours manquants: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task(name='analytics.generate_analytics_report')
def generate_analytics_report(start_date=None, end_date=None):
    """
    Génère un rapport analytics pour une période donnée
    Utilise les DailyAnalytics pour des calculs rapides

    Args:
        start_date: Date de début (str YYYY-MM-DD) ou None (30 jours)
        end_date: Date de fin (str YYYY-MM-DD) ou None (aujourd'hui)

    Returns:
        dict: Rapport complet
    """
    try:
        # Dates par défaut
        if not end_date:
            end = timezone.now().date()
        else:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()

        if not start_date:
            start = end - timedelta(days=30)
        else:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()

        logger.info(f"[CELERY] Génération rapport analytics {start} → {end}")

        # Récupérer les données agrégées
        daily_data = DailyAnalytics.objects.filter(
            date__gte=start,
            date__lte=end
        ).order_by('date')

        if not daily_data.exists():
            return {
                'status': 'success',
                'message': 'No data available',
                'period': {'start': str(start), 'end': str(end)}
            }

        # Calculer les métriques de période
        total_sessions = sum(d.total_sessions for d in daily_data)
        total_visitors = sum(d.unique_visitors for d in daily_data)
        total_pageviews = sum(d.total_pageviews for d in daily_data)

        avg_bounce_rate = round(
            sum(d.bounce_rate for d in daily_data) / daily_data.count(), 2
        )
        avg_conversion_rate = round(
            sum(d.conversion_rate for d in daily_data) / daily_data.count(), 2
        )
        avg_duration = round(
            sum(d.avg_session_duration for d in daily_data) / daily_data.count(), 2
        )

        # Top pages de la période
        all_pages = {}
        for day in daily_data:
            if day.top_pages:
                for page in day.top_pages:
                    url = page.get('url', '')
                    views = page.get('views', 0)
                    all_pages[url] = all_pages.get(url, 0) + views

        top_pages_period = sorted(
            [{'url': url, 'views': views} for url, views in all_pages.items()],
            key=lambda x: x['views'],
            reverse=True
        )[:10]

        report = {
            'status': 'success',
            'period': {
                'start': str(start),
                'end': str(end),
                'days': (end - start).days + 1
            },
            'metrics': {
                'total_sessions': total_sessions,
                'total_visitors': total_visitors,
                'total_pageviews': total_pageviews,
                'avg_bounce_rate': avg_bounce_rate,
                'avg_conversion_rate': avg_conversion_rate,
                'avg_session_duration': avg_duration
            },
            'top_pages': top_pages_period
        }

        logger.info(f"[CELERY] ✓ Rapport généré: {total_sessions} sessions")

        return report

    except Exception as e:
        logger.error(f"[CELERY] ✗ Erreur génération rapport: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
