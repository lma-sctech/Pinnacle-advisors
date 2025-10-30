"""
ViewSets pour l'API Analytics - God View Tracking
"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db import transaction

from .models import UserSession, PageView, Event, HeatmapData, DailyAnalytics
from .serializers import (
    UserSessionSerializer,
    UserSessionCreateSerializer,
    PageViewSerializer,
    PageViewCreateSerializer,
    EventSerializer,
    EventCreateSerializer,
    HeatmapDataSerializer,
    HeatmapDataCreateSerializer,
    AnalyticsBatchSerializer,
    DailyAnalyticsSerializer
)


class AnalyticsTrackingViewSet(viewsets.GenericViewSet):
    """
    ViewSet principal pour le tracking analytics
    Endpoints write-only pour capturer les données utilisateur
    POST /api/analytics/session/        - Créer une session
    POST /api/analytics/pageview/       - Tracker une page vue
    POST /api/analytics/event/          - Tracker un événement
    POST /api/analytics/heatmap/        - Tracker un clic pour heatmap
    POST /api/analytics/batch/          - Envoyer plusieurs données en batch
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='session')
    def create_session(self, request):
        """
        Créer une nouvelle session utilisateur
        POST /api/analytics/session/

        Body:
        {
            "session_id": "unique-session-id",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0...",
            "device_type": "desktop",
            "browser": "Chrome",
            "screen_resolution": "1920x1080",
            "referrer": "https://google.com",
            "landing_page": "/",
            "utm_source": "google",
            "utm_campaign": "summer-2025"
        }
        """
        # Capturer l'IP automatiquement si non fournie
        if 'ip_address' not in request.data or not request.data['ip_address']:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')

            # Créer une copie mutable des données
            data = request.data.copy()
            data['ip_address'] = ip_address
        else:
            data = request.data

        serializer = UserSessionCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()

        response_serializer = UserSessionSerializer(session)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], url_path='pageview')
    def create_pageview(self, request):
        """
        Tracker une vue de page
        POST /api/analytics/pageview/

        Body:
        {
            "session_id": "unique-session-id",
            "page_url": "/services",
            "page_title": "Nos Services",
            "time_on_page": 45,
            "scroll_depth": 75
        }
        """
        serializer = PageViewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pageview = serializer.save()

        # Incrémenter le compteur de pages visitées de la session
        pageview.session.pages_visited += 1
        pageview.session.save(update_fields=['pages_visited'])

        response_serializer = PageViewSerializer(pageview)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], url_path='event')
    def create_event(self, request):
        """
        Tracker un événement
        POST /api/analytics/event/

        Body:
        {
            "session_id": "unique-session-id",
            "event_type": "click",
            "event_action": "cta-contact",
            "element_text": "Contactez-nous",
            "x_position": 450,
            "y_position": 250
        }
        """
        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        response_serializer = EventSerializer(event)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], url_path='heatmap')
    def create_heatmap(self, request):
        """
        Tracker un clic pour la heatmap
        POST /api/analytics/heatmap/

        Body:
        {
            "page_url": "/",
            "x_position": 450,
            "y_position": 250
        }
        """
        serializer = HeatmapDataCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        heatmap = serializer.save()

        response_serializer = HeatmapDataSerializer(heatmap)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], url_path='batch')
    def batch_create(self, request):
        """
        Envoyer plusieurs données analytics en batch
        Optimise les requêtes réseau en groupant les appels
        POST /api/analytics/batch/

        Body:
        {
            "session_id": "unique-session-id",
            "pageviews": [
                {"session_id": "...", "page_url": "/", ...},
                {"session_id": "...", "page_url": "/services", ...}
            ],
            "events": [
                {"session_id": "...", "event_type": "click", ...}
            ],
            "heatmap": [
                {"page_url": "/", "x_position": 450, "y_position": 250}
            ]
        }
        """
        serializer = AnalyticsBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        results = {
            'pageviews_created': 0,
            'events_created': 0,
            'heatmap_created': 0,
            'errors': []
        }

        with transaction.atomic():
            # Créer les pageviews
            pageviews_data = serializer.validated_data.get('pageviews', [])
            for pv_data in pageviews_data:
                try:
                    pv_serializer = PageViewCreateSerializer(data=pv_data)
                    pv_serializer.is_valid(raise_exception=True)
                    pageview = pv_serializer.save()

                    # Incrémenter le compteur de pages
                    pageview.session.pages_visited += 1
                    pageview.session.save(update_fields=['pages_visited'])

                    results['pageviews_created'] += 1
                except Exception as e:
                    results['errors'].append(f"PageView error: {str(e)}")

            # Créer les événements
            events_data = serializer.validated_data.get('events', [])
            for event_data in events_data:
                try:
                    event_serializer = EventCreateSerializer(data=event_data)
                    event_serializer.is_valid(raise_exception=True)
                    event_serializer.save()
                    results['events_created'] += 1
                except Exception as e:
                    results['errors'].append(f"Event error: {str(e)}")

            # Créer les données heatmap
            heatmap_data = serializer.validated_data.get('heatmap', [])
            for hm_data in heatmap_data:
                try:
                    hm_serializer = HeatmapDataCreateSerializer(data=hm_data)
                    hm_serializer.is_valid(raise_exception=True)
                    hm_serializer.save()
                    results['heatmap_created'] += 1
                except Exception as e:
                    results['errors'].append(f"Heatmap error: {str(e)}")

        return Response(results, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], url_path='session/(?P<session_id>[^/.]+)/end')
    def end_session(self, request, session_id=None):
        """
        Terminer une session utilisateur
        PATCH /api/analytics/session/{session_id}/end/

        Body:
        {
            "duration_seconds": 300,
            "converted": false
        }
        """
        try:
            session = UserSession.objects.get(session_id=session_id)
        except UserSession.DoesNotExist:
            return Response(
                {'detail': 'Session non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mettre à jour la session
        from django.utils import timezone
        session.end_time = timezone.now()

        if 'duration_seconds' in request.data:
            session.duration_seconds = request.data['duration_seconds']

        if 'converted' in request.data:
            session.converted = request.data['converted']

        session.save()

        serializer = UserSessionSerializer(session)
        return Response(serializer.data)


class UserSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet read-only pour les sessions (admin uniquement)
    GET /api/analytics/sessions/
    GET /api/analytics/sessions/{id}/
    """
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAdminUser]


class PageViewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet read-only pour les pageviews (admin uniquement)
    GET /api/analytics/pageviews/
    GET /api/analytics/pageviews/{id}/
    """
    queryset = PageView.objects.select_related('session')
    serializer_class = PageViewSerializer
    permission_classes = [IsAdminUser]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet read-only pour les events (admin uniquement)
    GET /api/analytics/events/
    GET /api/analytics/events/{id}/
    """
    queryset = Event.objects.select_related('session')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]


class HeatmapDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet read-only pour les heatmap data (admin uniquement)
    GET /api/analytics/heatmap-data/
    GET /api/analytics/heatmap-data/{id}/
    """
    queryset = HeatmapData.objects.all()
    serializer_class = HeatmapDataSerializer
    permission_classes = [IsAdminUser]


class DailyAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet read-only pour les statistiques quotidiennes (admin uniquement)
    GET /api/analytics/daily/
    GET /api/analytics/daily/{id}/
    """
    queryset = DailyAnalytics.objects.all()
    serializer_class = DailyAnalyticsSerializer
    permission_classes = [IsAdminUser]
