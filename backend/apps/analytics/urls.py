"""
URLs pour l'API Analytics - God View Tracking
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AnalyticsTrackingViewSet,
    UserSessionViewSet,
    PageViewViewSet,
    EventViewSet,
    HeatmapDataViewSet,
    DailyAnalyticsViewSet
)
from .dashboard_views import analytics_dashboard, heatmap_view, heatmap_data_api

# Créer le router DRF
router = DefaultRouter()

# Enregistrer les ViewSets read-only (admin uniquement)
router.register(r'sessions', UserSessionViewSet, basename='session')
router.register(r'pageviews', PageViewViewSet, basename='pageview')
router.register(r'events', EventViewSet, basename='event')
router.register(r'heatmap-data', HeatmapDataViewSet, basename='heatmap-data')
router.register(r'daily', DailyAnalyticsViewSet, basename='daily')

# URLs de l'app
urlpatterns = [
    # Dashboard God View (admin uniquement)
    path('dashboard/', analytics_dashboard, name='analytics-dashboard'),
    path('heatmap/', heatmap_view, name='analytics-heatmap'),
    path('heatmap/data/', heatmap_data_api, name='analytics-heatmap-data'),

    # Endpoints de tracking (AllowAny - write-only)
    path('track/', AnalyticsTrackingViewSet.as_view({
        'post': 'create_session'
    }), name='track-session'),
    path('track/session/', AnalyticsTrackingViewSet.as_view({
        'post': 'create_session'
    }), name='track-session-alt'),
    path('track/pageview/', AnalyticsTrackingViewSet.as_view({
        'post': 'create_pageview'
    }), name='track-pageview'),
    path('track/event/', AnalyticsTrackingViewSet.as_view({
        'post': 'create_event'
    }), name='track-event'),
    path('track/heatmap/', AnalyticsTrackingViewSet.as_view({
        'post': 'create_heatmap'
    }), name='track-heatmap'),
    path('track/batch/', AnalyticsTrackingViewSet.as_view({
        'post': 'batch_create'
    }), name='track-batch'),
    path('track/session/<str:session_id>/end/', AnalyticsTrackingViewSet.as_view({
        'patch': 'end_session'
    }), name='track-session-end'),

    # Endpoints read-only (admin uniquement)
    path('', include(router.urls)),
]
