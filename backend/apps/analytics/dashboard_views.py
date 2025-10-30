"""
Views pour le dashboard analytics God View dans Django Admin
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Q, F, Sum
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta, datetime
from .models import UserSession, PageView, Event, HeatmapData, DailyAnalytics


@staff_member_required
def analytics_dashboard(request):
    """
    Dashboard principal analytics avec KPIs et visualisations
    """
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    # ====== KPIs AUJOURD'HUI ======

    # Sessions aujourd'hui
    sessions_today = UserSession.objects.filter(
        start_time__date=today
    ).count()

    # Visiteurs uniques aujourd'hui (par IP)
    unique_visitors_today = UserSession.objects.filter(
        start_time__date=today
    ).values('ip_address').distinct().count()

    # Pages vues aujourd'hui
    pageviews_today = PageView.objects.filter(
        viewed_at__date=today
    ).count()

    # Events aujourd'hui
    events_today = Event.objects.filter(
        timestamp__date=today
    ).count()

    # Durée moyenne session aujourd'hui (en minutes)
    avg_duration_today = UserSession.objects.filter(
        start_time__date=today,
        duration_seconds__gt=0
    ).aggregate(
        avg=Avg('duration_seconds')
    )['avg']
    avg_duration_minutes = round(avg_duration_today / 60, 1) if avg_duration_today else 0

    # Bounce rate aujourd'hui (sessions avec 1 seule page)
    sessions_today_count = sessions_today if sessions_today > 0 else 1
    bounce_sessions_today = UserSession.objects.filter(
        start_time__date=today,
        pages_visited=1
    ).count()
    bounce_rate_today = round((bounce_sessions_today / sessions_today_count) * 100, 1)

    # Taux de conversion aujourd'hui
    converted_today = UserSession.objects.filter(
        start_time__date=today,
        converted=True
    ).count()
    conversion_rate_today = round((converted_today / sessions_today_count) * 100, 1)

    # ====== KPIs 30 DERNIERS JOURS ======

    # Sessions 30 jours
    sessions_30d = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).count()

    # Visiteurs uniques 30 jours
    unique_visitors_30d = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).values('ip_address').distinct().count()

    # Pages vues 30 jours
    pageviews_30d = PageView.objects.filter(
        viewed_at__date__gte=last_30_days
    ).count()

    # ====== ÉVOLUTION 7 DERNIERS JOURS (pour Chart.js) ======

    sessions_7d_data = []
    labels_7d = []

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = UserSession.objects.filter(start_time__date=date).count()
        sessions_7d_data.append(count)
        labels_7d.append(date.strftime('%d/%m'))

    # ====== TOP 10 PAGES (30 jours) ======

    top_pages = PageView.objects.filter(
        viewed_at__date__gte=last_30_days
    ).values('page_url').annotate(
        views=Count('id')
    ).order_by('-views')[:10]

    top_pages_labels = [page['page_url'][:50] for page in top_pages]
    top_pages_data = [page['views'] for page in top_pages]

    # ====== DEVICE BREAKDOWN (30 jours) ======

    device_stats = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')

    device_labels = [stat['device_type'] or 'Unknown' for stat in device_stats]
    device_data = [stat['count'] for stat in device_stats]

    # ====== BROWSER BREAKDOWN (30 jours) ======

    browser_stats = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).values('browser').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    browser_labels = [stat['browser'][:30] or 'Unknown' for stat in browser_stats]
    browser_data = [stat['count'] for stat in browser_stats]

    # ====== TRAFFIC SOURCES (30 jours) ======

    # Direct traffic (pas de referrer)
    direct_traffic = UserSession.objects.filter(
        start_time__date__gte=last_30_days,
        referrer=''
    ).count()

    # Organic (referrer non vide, pas de UTM)
    organic_traffic = UserSession.objects.filter(
        start_time__date__gte=last_30_days,
        utm_source='',
        referrer__isnull=False
    ).exclude(referrer='').count()

    # UTM campaigns
    utm_traffic = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).exclude(utm_source='').count()

    traffic_sources_labels = ['Direct', 'Organic', 'UTM Campaigns']
    traffic_sources_data = [direct_traffic, organic_traffic, utm_traffic]

    # ====== TOP UTM SOURCES (30 jours) ======

    utm_sources = UserSession.objects.filter(
        start_time__date__gte=last_30_days
    ).exclude(utm_source='').values('utm_source').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    # ====== DERNIÈRES SESSIONS (10 dernières) ======

    recent_sessions = UserSession.objects.select_related().order_by('-start_time')[:10]

    # ====== FUNNEL DE CONVERSION ======

    funnel_data = calculate_conversion_funnel(last_30_days, today)

    # ====== CONTEXTE TEMPLATE ======

    context = {
        'title': 'God View Dashboard',
        # KPIs aujourd'hui
        'sessions_today': sessions_today,
        'unique_visitors_today': unique_visitors_today,
        'pageviews_today': pageviews_today,
        'events_today': events_today,
        'avg_duration_minutes': avg_duration_minutes,
        'bounce_rate_today': bounce_rate_today,
        'conversion_rate_today': conversion_rate_today,

        # KPIs 30 jours
        'sessions_30d': sessions_30d,
        'unique_visitors_30d': unique_visitors_30d,
        'pageviews_30d': pageviews_30d,

        # Chart.js data (évolution 7 jours)
        'sessions_7d_labels': labels_7d,
        'sessions_7d_data': sessions_7d_data,

        # Top pages
        'top_pages_labels': top_pages_labels,
        'top_pages_data': top_pages_data,

        # Device breakdown
        'device_labels': device_labels,
        'device_data': device_data,

        # Browser breakdown
        'browser_labels': browser_labels,
        'browser_data': browser_data,

        # Traffic sources
        'traffic_sources_labels': traffic_sources_labels,
        'traffic_sources_data': traffic_sources_data,

        # UTM sources
        'utm_sources': utm_sources,

        # Sessions récentes
        'recent_sessions': recent_sessions,

        # Funnel
        'funnel_data': funnel_data,
    }

    return render(request, 'admin/analytics/dashboard.html', context)


def calculate_conversion_funnel(start_date, end_date):
    """
    Calcule le funnel de conversion en 6 étapes
    """
    # Total sessions dans la période
    total_sessions = UserSession.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date
    ).count()

    if total_sessions == 0:
        return {
            'steps': [],
            'total_sessions': 0
        }

    # Étape 1: Landing (Hero view) - Toutes les sessions
    step1_count = total_sessions
    step1_rate = 100.0

    # Étape 2: Services scroll - Sessions avec au moins 2 pages vues
    step2_count = UserSession.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        pages_visited__gte=2
    ).count()
    step2_rate = round((step2_count / total_sessions) * 100, 1) if total_sessions > 0 else 0

    # Étape 3: About scroll - Sessions avec au moins 3 pages vues
    step3_count = UserSession.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        pages_visited__gte=3
    ).count()
    step3_rate = round((step3_count / total_sessions) * 100, 1) if total_sessions > 0 else 0

    # Étape 4: Contact form view - Events de type "form"
    step4_sessions = Event.objects.filter(
        timestamp__date__gte=start_date,
        timestamp__date__lte=end_date,
        event_action__icontains='contact'
    ).values('session_id').distinct()
    step4_count = step4_sessions.count()
    step4_rate = round((step4_count / total_sessions) * 100, 1) if total_sessions > 0 else 0

    # Étape 5: Form submit - Events form_submit
    step5_sessions = Event.objects.filter(
        timestamp__date__gte=start_date,
        timestamp__date__lte=end_date,
        event_type='form_submit'
    ).values('session_id').distinct()
    step5_count = step5_sessions.count()
    step5_rate = round((step5_count / total_sessions) * 100, 1) if total_sessions > 0 else 0

    # Étape 6: Success - Sessions converties
    step6_count = UserSession.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        converted=True
    ).count()
    step6_rate = round((step6_count / total_sessions) * 100, 1) if total_sessions > 0 else 0

    steps = [
        {
            'name': 'Landing (Hero)',
            'count': step1_count,
            'rate': step1_rate,
            'drop_off': 0
        },
        {
            'name': 'Services Scroll',
            'count': step2_count,
            'rate': step2_rate,
            'drop_off': round(step1_rate - step2_rate, 1)
        },
        {
            'name': 'About Scroll',
            'count': step3_count,
            'rate': step3_rate,
            'drop_off': round(step2_rate - step3_rate, 1)
        },
        {
            'name': 'Contact View',
            'count': step4_count,
            'rate': step4_rate,
            'drop_off': round(step3_rate - step4_rate, 1)
        },
        {
            'name': 'Form Submit',
            'count': step5_count,
            'rate': step5_rate,
            'drop_off': round(step4_rate - step5_rate, 1)
        },
        {
            'name': 'Success',
            'count': step6_count,
            'rate': step6_rate,
            'drop_off': round(step5_rate - step6_rate, 1)
        },
    ]

    return {
        'steps': steps,
        'total_sessions': total_sessions,
        'final_conversion_rate': step6_rate
    }


@staff_member_required
def heatmap_view(request):
    """
    Vue pour afficher les heatmaps par page avec filtres
    """
    # Récupérer les paramètres de filtres
    page_url = request.GET.get('page_url', '')
    days = int(request.GET.get('days', 30))
    device_type = request.GET.get('device_type', '')

    # Date de début selon le filtre
    today = timezone.now().date()
    start_date = today - timedelta(days=days)

    # Récupérer toutes les URLs uniques pour le sélecteur
    all_pages = HeatmapData.objects.values('page_url').annotate(
        total_clicks=Sum('click_count')
    ).order_by('-total_clicks')

    # Si aucune page sélectionnée, prendre la première
    if not page_url and all_pages.exists():
        page_url = all_pages.first()['page_url']

    # Récupérer les données heatmap pour la page sélectionnée
    heatmap_query = HeatmapData.objects.filter(
        page_url=page_url,
        date__gte=start_date
    )

    # Filtre optionnel par device (via events liés)
    if device_type:
        # Cette partie pourrait être améliorée avec une relation directe
        # Pour l'instant on agrège toutes les données
        pass

    # Agréger les données par coordonnées
    heatmap_points = heatmap_query.values('x_position', 'y_position').annotate(
        clicks=Sum('click_count')
    ).order_by('-clicks')

    # Statistiques pour la page
    total_clicks = heatmap_query.aggregate(total=Sum('click_count'))['total'] or 0
    unique_points = heatmap_query.count()

    # Trouver les points les plus cliqués (top 10)
    top_hotspots = list(heatmap_points[:10])

    # Préparer les données pour heatmap.js (format requis)
    heatmap_data = []
    max_value = 0

    for point in heatmap_points:
        value = point['clicks']
        if value > max_value:
            max_value = value

        heatmap_data.append({
            'x': point['x_position'],
            'y': point['y_position'],
            'value': value
        })

    context = {
        'title': 'Heatmap Viewer',
        'all_pages': all_pages,
        'selected_page': page_url,
        'days_filter': days,
        'device_filter': device_type,
        'total_clicks': total_clicks,
        'unique_points': unique_points,
        'top_hotspots': top_hotspots,
        'heatmap_data': heatmap_data,
        'max_value': max_value,
    }

    return render(request, 'admin/analytics/heatmap.html', context)


@staff_member_required
def heatmap_data_api(request):
    """
    API endpoint pour récupérer les données heatmap en JSON
    Utilisé par le frontend pour charger les données dynamiquement
    """
    page_url = request.GET.get('page_url', '')
    days = int(request.GET.get('days', 30))

    if not page_url:
        return JsonResponse({'error': 'page_url required'}, status=400)

    today = timezone.now().date()
    start_date = today - timedelta(days=days)

    # Récupérer et agréger les données
    heatmap_points = HeatmapData.objects.filter(
        page_url=page_url,
        date__gte=start_date
    ).values('x_position', 'y_position').annotate(
        clicks=Sum('click_count')
    )

    # Formater pour heatmap.js
    data = []
    max_value = 0

    for point in heatmap_points:
        value = point['clicks']
        if value > max_value:
            max_value = value

        data.append({
            'x': point['x_position'],
            'y': point['y_position'],
            'value': value
        })

    return JsonResponse({
        'data': data,
        'max': max_value,
        'count': len(data)
    })
