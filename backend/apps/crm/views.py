"""
ViewSets pour l'app CRM
API REST admin-only pour gérer les leads, pipelines, interactions et notes
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Lead, Pipeline, Interaction, Note
from .serializers import (
    LeadSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
    LeadListSerializer,
    PipelineSerializer,
    PipelineDetailSerializer,
    InteractionSerializer,
    InteractionCreateSerializer,
    InteractionDetailSerializer,
    NoteSerializer,
    NoteCreateSerializer,
)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les leads CRM
    Admin-only - Endpoints CRUD complets + actions customs
    """

    queryset = Lead.objects.select_related(
        'assigned_to', 'pipeline'
    ).prefetch_related('interactions', 'notes')
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'qualification', 'status', 'source', 'company_size',
        'converted_to_client', 'assigned_to', 'pipeline'
    ]
    search_fields = ['name', 'email', 'company', 'message', 'need_type']
    ordering_fields = [
        'created_at', 'updated_at', 'score', 'expected_revenue',
        'next_follow_up_date', 'last_contact_date'
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retourner le serializer approprié selon l'action"""
        if self.action == 'list':
            return LeadListSerializer
        elif self.action == 'retrieve':
            return LeadDetailSerializer
        elif self.action == 'create':
            return LeadCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LeadUpdateSerializer
        return LeadSerializer

    @extend_schema(
        summary="Requalifier un lead",
        description="Relance l'algorithme de qualification automatique pour recalculer le score et le niveau de qualification du lead.",
        tags=['crm'],
    )
    @action(detail=True, methods=['post'])
    def requalify(self, request, pk=None):
        """
        Relancer la qualification automatique du lead
        POST /api/crm/leads/{id}/requalify/
        """
        lead = self.get_object()
        old_qualification = lead.qualification
        old_score = lead.score

        # Relancer l'auto-qualification
        lead.auto_qualify()
        lead.save()

        return Response({
            'message': 'Lead requalifié avec succès',
            'lead_id': lead.id,
            'old_qualification': old_qualification,
            'new_qualification': lead.qualification,
            'old_score': old_score,
            'new_score': lead.score,
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Assigner un lead",
        description="Assigne le lead à un utilisateur spécifique.",
        tags=['crm'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'ID de l\'utilisateur'}
                },
                'required': ['user_id']
            }
        }
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assigner le lead à un utilisateur
        POST /api/crm/leads/{id}/assign/
        Body: {"user_id": 1}
        """
        lead = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
            lead.assigned_to = user
            lead.save()

            return Response({
                'message': f'Lead assigné à {user.get_full_name() or user.username}',
                'lead_id': lead.id,
                'assigned_to': user.username,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Convertir un lead en client",
        description="Marque le lead comme converti en client avec un statut 'won'.",
        tags=['crm'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'expected_revenue': {'type': 'number', 'description': 'Revenu attendu en euros'}
                }
            }
        }
    )
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        """
        Convertir le lead en client
        POST /api/crm/leads/{id}/convert/
        Body: {"expected_revenue": 50000}
        """
        lead = self.get_object()

        if lead.converted_to_client:
            return Response(
                {'error': 'Lead déjà converti en client'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Marquer comme converti
        lead.converted_to_client = True
        lead.conversion_date = timezone.now()
        lead.status = 'won'

        # Mettre à jour le revenu attendu si fourni
        expected_revenue = request.data.get('expected_revenue')
        if expected_revenue:
            try:
                lead.expected_revenue = float(expected_revenue)
            except (ValueError, TypeError):
                return Response(
                    {'error': 'expected_revenue doit être un nombre'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        lead.save()

        return Response({
            'message': 'Lead converti en client avec succès',
            'lead_id': lead.id,
            'conversion_date': lead.conversion_date,
            'expected_revenue': lead.expected_revenue,
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Liste des leads hot",
        description="Retourne tous les leads avec une qualification 'hot' (score >= 70).",
        tags=['crm'],
    )
    @action(detail=False, methods=['get'])
    def hot_leads(self, request):
        """
        Obtenir tous les leads hot
        GET /api/crm/leads/hot_leads/
        """
        hot_leads = self.get_queryset().filter(qualification='hot')
        serializer = self.get_serializer(hot_leads, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Leads avec suivis en retard",
        description="Retourne les leads dont la date de prochain suivi est dépassée.",
        tags=['crm'],
    )
    @action(detail=False, methods=['get'])
    def overdue_followups(self, request):
        """
        Obtenir les leads avec suivis en retard
        GET /api/crm/leads/overdue_followups/
        """
        now = timezone.now()
        overdue = self.get_queryset().filter(
            next_follow_up_date__lt=now,
            status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation']
        )
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Statistiques des leads",
        description="Retourne des statistiques globales sur les leads (totaux par qualification, statut, source, etc.).",
        tags=['crm'],
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Statistiques globales des leads
        GET /api/crm/leads/stats/
        """
        queryset = self.get_queryset()

        stats = {
            'total_leads': queryset.count(),
            'hot_leads': queryset.filter(qualification='hot').count(),
            'warm_leads': queryset.filter(qualification='warm').count(),
            'cold_leads': queryset.filter(qualification='cold').count(),
            'unqualified_leads': queryset.filter(qualification='unqualified').count(),
            'converted_leads': queryset.filter(converted_to_client=True).count(),
            'by_status': {
                'new': queryset.filter(status='new').count(),
                'contacted': queryset.filter(status='contacted').count(),
                'qualified': queryset.filter(status='qualified').count(),
                'proposal': queryset.filter(status='proposal').count(),
                'negotiation': queryset.filter(status='negotiation').count(),
                'won': queryset.filter(status='won').count(),
                'lost': queryset.filter(status='lost').count(),
                'on_hold': queryset.filter(status='on_hold').count(),
            },
            'by_source': {
                'website': queryset.filter(source='website').count(),
                'referral': queryset.filter(source='referral').count(),
                'linkedin': queryset.filter(source='linkedin').count(),
                'email': queryset.filter(source='email').count(),
                'phone': queryset.filter(source='phone').count(),
                'event': queryset.filter(source='event').count(),
                'other': queryset.filter(source='other').count(),
            },
        }

        # Calculer le revenu total attendu
        from django.db.models import Sum
        total_revenue = queryset.aggregate(Sum('expected_revenue'))
        stats['total_expected_revenue'] = (
            float(total_revenue['expected_revenue__sum'])
            if total_revenue['expected_revenue__sum'] else 0.0
        )

        return Response(stats)


class PipelineViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les pipelines de vente
    Admin-only - Endpoints CRUD complets
    """

    queryset = Pipeline.objects.prefetch_related('leads')
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name', 'created_at']
    ordering = ['order', 'name']

    def get_serializer_class(self):
        """Retourner le serializer approprié selon l'action"""
        if self.action == 'retrieve':
            return PipelineDetailSerializer
        return PipelineSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Obtenir les pipelines actifs uniquement
        GET /api/crm/pipelines/active/
        """
        active_pipelines = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_pipelines, many=True)
        return Response(serializer.data)


class InteractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les interactions avec les leads
    Admin-only - Endpoints CRUD complets
    """

    queryset = Interaction.objects.select_related('lead', 'created_by')
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lead', 'type', 'created_by']
    search_fields = ['subject', 'content', 'lead__name', 'lead__company']
    ordering_fields = ['created_at', 'duration_minutes']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retourner le serializer approprié selon l'action"""
        if self.action == 'create':
            return InteractionCreateSerializer
        elif self.action == 'retrieve':
            return InteractionDetailSerializer
        return InteractionSerializer

    def perform_create(self, serializer):
        """Assigner automatiquement le created_by"""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Obtenir les interactions récentes (7 derniers jours)
        GET /api/crm/interactions/recent/
        """
        from datetime import timedelta
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_interactions = self.get_queryset().filter(created_at__gte=seven_days_ago)
        serializer = self.get_serializer(recent_interactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_lead(self, request):
        """
        Obtenir les interactions d'un lead spécifique
        GET /api/crm/interactions/by_lead/?lead_id=1
        """
        lead_id = request.query_params.get('lead_id')
        if not lead_id:
            return Response(
                {'error': 'lead_id query parameter requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        interactions = self.get_queryset().filter(lead_id=lead_id)
        serializer = self.get_serializer(interactions, many=True)
        return Response(serializer.data)


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les notes sur les leads
    Admin-only - Endpoints CRUD complets
    """

    queryset = Note.objects.select_related('lead', 'created_by')
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lead', 'is_private', 'is_important', 'created_by']
    search_fields = ['content', 'lead__name', 'lead__company']
    ordering_fields = ['created_at', 'is_important']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retourner le serializer approprié selon l'action"""
        if self.action == 'create':
            return NoteCreateSerializer
        return NoteSerializer

    def perform_create(self, serializer):
        """Assigner automatiquement le created_by"""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def important(self, request):
        """
        Obtenir les notes marquées comme importantes
        GET /api/crm/notes/important/
        """
        important_notes = self.get_queryset().filter(is_important=True)
        serializer = self.get_serializer(important_notes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_lead(self, request):
        """
        Obtenir les notes d'un lead spécifique
        GET /api/crm/notes/by_lead/?lead_id=1
        """
        lead_id = request.query_params.get('lead_id')
        if not lead_id:
            return Response(
                {'error': 'lead_id query parameter requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        notes = self.get_queryset().filter(lead_id=lead_id)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
