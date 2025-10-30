"""
Serializers pour l'API Analytics
"""
from rest_framework import serializers
from .models import UserSession, PageView, Event, HeatmapData, DailyAnalytics


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer pour créer des sessions utilisateur"""

    class Meta:
        model = UserSession
        fields = [
            'id', 'session_id', 'ip_address', 'user_agent', 'device_type',
            'browser', 'screen_resolution', 'referrer', 'landing_page',
            'utm_source', 'utm_campaign', 'start_time', 'end_time',
            'duration_seconds', 'pages_visited', 'converted'
        ]
        read_only_fields = ['id', 'start_time', 'end_time']

    def validate_session_id(self, value):
        """Validation de l'ID de session"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "L'ID de session doit contenir au moins 10 caractères."
            )
        return value.strip()


class UserSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une nouvelle session (API publique)"""
    session_id = serializers.CharField(required=False, allow_blank=True)
    user_agent = serializers.CharField(required=False, allow_blank=True)
    landing_page = serializers.CharField(required=False, allow_blank=True)
    ip_address = serializers.IPAddressField(required=False, allow_blank=True)

    class Meta:
        model = UserSession
        fields = [
            'session_id', 'ip_address', 'user_agent', 'device_type',
            'browser', 'screen_resolution', 'referrer', 'landing_page',
            'utm_source', 'utm_campaign'
        ]

    def validate_session_id(self, value):
        """Validation de l'ID de session"""
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError(
                "L'ID de session doit contenir au moins 10 caractères."
            )
        return value.strip() if value else None

    def create(self, validated_data):
        """Créer une session, générer un session_id si non fourni"""
        if not validated_data.get('session_id'):
            import uuid
            validated_data['session_id'] = str(uuid.uuid4())

        # Valeurs par défaut si non fournies
        if not validated_data.get('user_agent'):
            validated_data['user_agent'] = 'Unknown'

        if not validated_data.get('landing_page'):
            validated_data['landing_page'] = '/'

        if not validated_data.get('ip_address'):
            validated_data['ip_address'] = '0.0.0.0'

        return super().create(validated_data)


class PageViewSerializer(serializers.ModelSerializer):
    """Serializer pour les vues de pages"""

    class Meta:
        model = PageView
        fields = [
            'id', 'session', 'page_url', 'page_title',
            'viewed_at', 'time_on_page', 'scroll_depth'
        ]
        read_only_fields = ['id', 'viewed_at']


class PageViewCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une vue de page (API publique)"""
    session_id = serializers.CharField(write_only=True)

    class Meta:
        model = PageView
        fields = [
            'session_id', 'page_url', 'page_title',
            'time_on_page', 'scroll_depth'
        ]

    def validate_page_url(self, value):
        """Validation de l'URL"""
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError("L'URL de la page est requise.")
        return value.strip()

    def validate_scroll_depth(self, value):
        """Validation du scroll depth"""
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Le scroll depth doit être entre 0 et 100%."
            )
        return value

    def create(self, validated_data):
        """Créer la PageView en trouvant la session par session_id"""
        session_id = validated_data.pop('session_id')
        try:
            session = UserSession.objects.get(session_id=session_id)
            validated_data['session'] = session
            return super().create(validated_data)
        except UserSession.DoesNotExist:
            raise serializers.ValidationError({
                'session_id': 'Session non trouvée. Créez d\'abord une session.'
            })


class EventSerializer(serializers.ModelSerializer):
    """Serializer pour les événements"""

    class Meta:
        model = Event
        fields = [
            'id', 'session', 'event_type', 'event_action',
            'element_text', 'x_position', 'y_position', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un événement (API publique)"""
    session_id = serializers.CharField(write_only=True)

    class Meta:
        model = Event
        fields = [
            'session_id', 'event_type', 'event_action',
            'element_text', 'x_position', 'y_position'
        ]

    def validate_event_action(self, value):
        """Validation de l'action"""
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError("L'action de l'événement est requise.")
        return value.strip()

    def create(self, validated_data):
        """Créer l'Event en trouvant la session par session_id"""
        session_id = validated_data.pop('session_id')
        try:
            session = UserSession.objects.get(session_id=session_id)
            validated_data['session'] = session
            return super().create(validated_data)
        except UserSession.DoesNotExist:
            raise serializers.ValidationError({
                'session_id': 'Session non trouvée. Créez d\'abord une session.'
            })


class HeatmapDataSerializer(serializers.ModelSerializer):
    """Serializer pour les données heatmap"""

    class Meta:
        model = HeatmapData
        fields = [
            'id', 'page_url', 'x_position', 'y_position',
            'click_count', 'date'
        ]
        read_only_fields = ['id', 'date']


class HeatmapDataCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer des données heatmap (API publique)"""

    class Meta:
        model = HeatmapData
        fields = ['page_url', 'x_position', 'y_position']

    def validate_page_url(self, value):
        """Validation de l'URL"""
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError("L'URL de la page est requise.")
        return value.strip()

    def create(self, validated_data):
        """
        Créer ou mettre à jour les données heatmap
        Si le point (x, y) existe déjà pour cette page aujourd'hui,
        on incrémente le compteur de clics
        """
        from django.utils import timezone
        today = timezone.now().date()

        # Chercher si ce point existe déjà aujourd'hui
        existing = HeatmapData.objects.filter(
            page_url=validated_data['page_url'],
            x_position=validated_data['x_position'],
            y_position=validated_data['y_position'],
            date=today
        ).first()

        if existing:
            # Incrémenter le compteur
            existing.click_count += 1
            existing.save()
            return existing
        else:
            # Créer une nouvelle entrée
            return super().create(validated_data)


class AnalyticsBatchSerializer(serializers.Serializer):
    """
    Serializer pour envoyer plusieurs données analytics en batch
    Permet d'optimiser les requêtes réseau
    """
    session_id = serializers.CharField(required=False)
    pageviews = PageViewCreateSerializer(many=True, required=False)
    events = EventCreateSerializer(many=True, required=False)
    heatmap = HeatmapDataCreateSerializer(many=True, required=False)

    def validate(self, data):
        """Validation du batch"""
        if not any([
            data.get('pageviews'),
            data.get('events'),
            data.get('heatmap')
        ]):
            raise serializers.ValidationError(
                "Au moins un type de données doit être fourni (pageviews, events, ou heatmap)."
            )
        return data


class DailyAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques quotidiennes (read-only pour admin)"""

    class Meta:
        model = DailyAnalytics
        fields = [
            'id', 'date', 'total_sessions', 'unique_visitors',
            'total_pageviews', 'avg_session_duration', 'bounce_rate',
            'conversion_rate', 'top_pages'
        ]
        read_only_fields = ['id']
