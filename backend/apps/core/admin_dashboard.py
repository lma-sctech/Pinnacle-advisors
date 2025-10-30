"""
Custom Django Admin Dashboard with KPIs
Displays key metrics for Pinnacle Advisors
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import timedelta


def admin_dashboard_view(request):
    """
    Vue dashboard personnalisee avec KPIs
    """
    # Import models here to avoid circular imports
    from apps.crm.models import Lead, Interaction
    from apps.analytics.models import UserSession, PageView, Event, DailyAnalytics
    from apps.website.models import ContactSubmission, FAQ

    # Dates
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    this_month_start = today.replace(day=1)

    # ===================
    # CRM KPIs
    # ===================

    # Leads par qualification
    leads_hot = Lead.objects.filter(qualification='hot').count()
    leads_warm = Lead.objects.filter(qualification='warm').count()
    leads_cold = Lead.objects.filter(qualification='cold').count()
    total_leads = Lead.objects.count()

    # Leads ce mois
    leads_this_month = Lead.objects.filter(created_at__gte=this_month_start).count()

    # Leads par statut
    leads_new = Lead.objects.filter(status='new').count()
    leads_contacted = Lead.objects.filter(status='contacted').count()
    leads_qualified = Lead.objects.filter(status='qualified').count()
    leads_proposal = Lead.objects.filter(status='proposal').count()
    leads_negotiation = Lead.objects.filter(status='negotiation').count()
    leads_won = Lead.objects.filter(status='won').count()
    leads_lost = Lead.objects.filter(status='lost').count()

    # Taux de conversion (won / total non-lost)
    leads_active = total_leads - leads_lost
    conversion_rate = (leads_won / leads_active * 100) if leads_active > 0 else 0

    # Score moyen des leads
    avg_score = Lead.objects.aggregate(avg=Avg('score'))['avg'] or 0

    # Interactions récentes
    recent_interactions = Interaction.objects.select_related('lead').order_by('-created_at')[:10]

    # ===================
    # Analytics KPIs
    # ===================

    # Sessions aujourd'hui
    sessions_today = UserSession.objects.filter(
        created_at__date=today
    ).count()

    # Visiteurs uniques aujourd'hui (par session_id unique)
    unique_visitors_today = UserSession.objects.filter(
        created_at__date=today
    ).values('session_id').distinct().count()

    # Total sessions 30 derniers jours
    sessions_30d = UserSession.objects.filter(
        created_at__gte=last_30_days
    ).count()

    # Pages vues aujourd'hui
    pageviews_today = PageView.objects.filter(
        created_at__date=today
    ).count()

    # Durée moyenne session (en minutes)
    avg_session_duration = UserSession.objects.aggregate(
        avg=Avg('duration')
    )['avg'] or 0
    avg_session_minutes = avg_session_duration / 60 if avg_session_duration > 0 else 0

    # Events aujourd'hui
    events_today = Event.objects.filter(
        created_at__date=today
    ).count()

    # Top 5 pages visitées (30 derniers jours)
    top_pages = PageView.objects.filter(
        created_at__gte=last_30_days
    ).values('page_url').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    # Bounce rate approximatif (sessions avec 1 seule page)
    single_page_sessions = UserSession.objects.filter(
        created_at__gte=last_30_days,
        pages_visited=1
    ).count()
    bounce_rate = (single_page_sessions / sessions_30d * 100) if sessions_30d > 0 else 0

    # ===================
    # Website KPIs
    # ===================

    # Soumissions contact ce mois
    contact_submissions_month = ContactSubmission.objects.filter(
        created_at__gte=this_month_start
    ).count()

    # FAQ les plus vues
    top_faqs = FAQ.objects.filter(
        is_published=True
    ).order_by('-views_count')[:5]

    # ===================
    # Context pour template
    # ===================

    context = {
        'title': 'Dashboard Pinnacle Advisors',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,

        # CRM
        'leads_hot': leads_hot,
        'leads_warm': leads_warm,
        'leads_cold': leads_cold,
        'total_leads': total_leads,
        'leads_this_month': leads_this_month,
        'leads_new': leads_new,
        'leads_contacted': leads_contacted,
        'leads_qualified': leads_qualified,
        'leads_proposal': leads_proposal,
        'leads_negotiation': leads_negotiation,
        'leads_won': leads_won,
        'leads_lost': leads_lost,
        'conversion_rate': round(conversion_rate, 1),
        'avg_score': round(avg_score, 1),
        'recent_interactions': recent_interactions,

        # Analytics
        'sessions_today': sessions_today,
        'unique_visitors_today': unique_visitors_today,
        'sessions_30d': sessions_30d,
        'pageviews_today': pageviews_today,
        'avg_session_minutes': round(avg_session_minutes, 1),
        'events_today': events_today,
        'top_pages': top_pages,
        'bounce_rate': round(bounce_rate, 1),

        # Website
        'contact_submissions_month': contact_submissions_month,
        'top_faqs': top_faqs,

        # Dates
        'today': today,
        'this_month_start': this_month_start,
    }

    return render(request, 'admin/dashboard.html', context)


def get_admin_dashboard_urls():
    """
    Retourne les URLs pour le dashboard
    A inclure dans admin.site.get_urls()
    """
    return [
        path('dashboard/', admin_dashboard_view, name='admin_dashboard'),
    ]
