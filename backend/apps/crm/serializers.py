"""
Serializers pour l'app CRM
API REST admin-only pour gérer les leads, pipelines, interactions et notes
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Lead, Pipeline, Interaction, Note


# ==================== User Serializers ====================

class UserSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour les utilisateurs (username + nom complet)"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


# ==================== Note Serializers ====================

class NoteSerializer(serializers.ModelSerializer):
    """Serializer standard pour les notes"""

    created_by = UserSimpleSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='created_by',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Note
        fields = [
            'id', 'lead', 'content', 'is_private', 'is_important',
            'created_by', 'created_by_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NoteCreateSerializer(serializers.ModelSerializer):
    """Serializer pour création de notes"""

    class Meta:
        model = Note
        fields = ['lead', 'content', 'is_private', 'is_important']

    def create(self, validated_data):
        # Auto-assigner le created_by depuis le request.user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# ==================== Interaction Serializers ====================

class InteractionSerializer(serializers.ModelSerializer):
    """Serializer standard pour les interactions"""

    created_by = UserSimpleSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='created_by',
        write_only=True,
        required=False,
        allow_null=True
    )
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Interaction
        fields = [
            'id', 'lead', 'type', 'type_display', 'subject', 'content',
            'duration_minutes', 'created_by', 'created_by_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InteractionCreateSerializer(serializers.ModelSerializer):
    """Serializer pour création d'interactions"""

    class Meta:
        model = Interaction
        fields = ['lead', 'type', 'subject', 'content', 'duration_minutes']

    def create(self, validated_data):
        # Auto-assigner le created_by depuis le request.user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class InteractionDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les interactions avec lead info"""

    created_by = UserSimpleSerializer(read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    lead_company = serializers.CharField(source='lead.company', read_only=True)

    class Meta:
        model = Interaction
        fields = [
            'id', 'lead', 'lead_name', 'lead_company', 'type', 'type_display',
            'subject', 'content', 'duration_minutes', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ==================== Pipeline Serializers ====================

class PipelineSerializer(serializers.ModelSerializer):
    """Serializer standard pour les pipelines"""

    leads_count = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        fields = [
            'id', 'name', 'description', 'order', 'color',
            'is_active', 'created_at', 'leads_count'
        ]
        read_only_fields = ['id', 'created_at']

    def get_leads_count(self, obj):
        return obj.leads.count()


class PipelineDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les pipelines avec statistiques"""

    leads_count = serializers.SerializerMethodField()
    hot_leads_count = serializers.SerializerMethodField()
    warm_leads_count = serializers.SerializerMethodField()
    cold_leads_count = serializers.SerializerMethodField()
    total_expected_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        fields = [
            'id', 'name', 'description', 'order', 'color', 'is_active',
            'created_at', 'leads_count', 'hot_leads_count', 'warm_leads_count',
            'cold_leads_count', 'total_expected_revenue'
        ]
        read_only_fields = ['id', 'created_at']

    def get_leads_count(self, obj):
        return obj.leads.count()

    def get_hot_leads_count(self, obj):
        return obj.leads.filter(qualification='hot').count()

    def get_warm_leads_count(self, obj):
        return obj.leads.filter(qualification='warm').count()

    def get_cold_leads_count(self, obj):
        return obj.leads.filter(qualification='cold').count()

    def get_total_expected_revenue(self, obj):
        from django.db.models import Sum
        total = obj.leads.aggregate(Sum('expected_revenue'))['expected_revenue__sum']
        return float(total) if total else 0.0


# ==================== Lead Serializers ====================

class LeadSerializer(serializers.ModelSerializer):
    """Serializer standard pour les leads"""

    qualification_display = serializers.CharField(
        source='get_qualification_display', read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    company_size_display = serializers.CharField(
        source='get_company_size_display', read_only=True
    )
    assigned_to = UserSimpleSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )
    pipeline = PipelineSerializer(read_only=True)
    pipeline_id = serializers.PrimaryKeyRelatedField(
        queryset=Pipeline.objects.all(),
        source='pipeline',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'company_size',
            'company_size_display', 'position', 'need_type', 'message',
            'budget_mentioned', 'estimated_budget', 'qualification',
            'qualification_display', 'status', 'status_display', 'score',
            'source', 'source_display', 'assigned_to', 'assigned_to_id',
            'pipeline', 'pipeline_id', 'converted_to_client', 'conversion_date',
            'expected_revenue', 'last_contact_date', 'next_follow_up_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'score', 'created_at', 'updated_at']


class LeadDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour les leads avec interactions et notes"""

    qualification_display = serializers.CharField(
        source='get_qualification_display', read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    company_size_display = serializers.CharField(
        source='get_company_size_display', read_only=True
    )
    assigned_to = UserSimpleSerializer(read_only=True)
    pipeline = PipelineSerializer(read_only=True)
    interactions = InteractionSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    interactions_count = serializers.SerializerMethodField()
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'company_size',
            'company_size_display', 'position', 'need_type', 'message',
            'budget_mentioned', 'estimated_budget', 'qualification',
            'qualification_display', 'status', 'status_display', 'score',
            'source', 'source_display', 'ip_address', 'user_agent',
            'assigned_to', 'pipeline', 'converted_to_client', 'conversion_date',
            'expected_revenue', 'last_contact_date', 'next_follow_up_date',
            'internal_notes', 'interactions', 'notes', 'interactions_count',
            'notes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'score', 'created_at', 'updated_at']

    def get_interactions_count(self, obj):
        return obj.interactions.count()

    def get_notes_count(self, obj):
        return obj.notes.count()


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer pour création de leads avec validation"""

    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone', 'company', 'company_size', 'position',
            'need_type', 'message', 'budget_mentioned', 'estimated_budget',
            'source', 'ip_address', 'user_agent', 'expected_revenue',
            'next_follow_up_date', 'internal_notes', 'pipeline', 'assigned_to'
        ]

    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà"""
        if Lead.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Un lead avec cet email existe déjà."
            )
        return value.lower()

    def validate_estimated_budget(self, value):
        """Vérifier que le budget est positif"""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Le budget estimé ne peut pas être négatif."
            )
        return value

    def validate_expected_revenue(self, value):
        """Vérifier que le revenu attendu est positif"""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Le revenu attendu ne peut pas être négatif."
            )
        return value

    def validate(self, data):
        """Validation croisée"""
        # Si budget mentionné, vérifier qu'un montant est fourni
        if data.get('budget_mentioned') and not data.get('estimated_budget'):
            raise serializers.ValidationError({
                'estimated_budget': (
                    "Veuillez fournir un budget estimé si le budget est mentionné."
                )
            })
        return data

    def create(self, validated_data):
        """Créer le lead et déclencher l'auto-qualification"""
        lead = Lead(**validated_data)
        # L'auto_qualify() sera appelé automatiquement dans le save() du modèle
        lead.save()
        return lead


class LeadUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mise à jour de leads"""

    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone', 'company', 'company_size', 'position',
            'need_type', 'message', 'budget_mentioned', 'estimated_budget',
            'qualification', 'status', 'source', 'assigned_to', 'pipeline',
            'converted_to_client', 'conversion_date', 'expected_revenue',
            'last_contact_date', 'next_follow_up_date', 'internal_notes'
        ]

    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà (sauf pour le lead actuel)"""
        lead_id = self.instance.id if self.instance else None
        if Lead.objects.filter(email__iexact=value).exclude(id=lead_id).exists():
            raise serializers.ValidationError(
                "Un autre lead avec cet email existe déjà."
            )
        return value.lower()

    def validate_estimated_budget(self, value):
        """Vérifier que le budget est positif"""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Le budget estimé ne peut pas être négatif."
            )
        return value

    def validate_expected_revenue(self, value):
        """Vérifier que le revenu attendu est positif"""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Le revenu attendu ne peut pas être négatif."
            )
        return value


class LeadListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes de leads (performances)"""

    qualification_display = serializers.CharField(
        source='get_qualification_display', read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    pipeline_name = serializers.CharField(source='pipeline.name', read_only=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'company', 'company_size', 'qualification',
            'qualification_display', 'status', 'status_display', 'score',
            'source', 'assigned_to_name', 'pipeline_name', 'expected_revenue',
            'next_follow_up_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'score', 'created_at', 'updated_at']

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name() or obj.assigned_to.username
        return None
