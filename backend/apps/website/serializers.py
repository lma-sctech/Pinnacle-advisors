from rest_framework import serializers
from .models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo, ContactSubmission, BusinessCard,
    Recruitment, TeamHeader, SEOSettings, SiteSettings
)


class HeroSectionSerializer(serializers.ModelSerializer):
    """Serializer pour la section Hero"""

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'subtitle', 'cta_text', 'cta_link',
            'background_image', 'video_url', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class HeroSectionDetailSerializer(HeroSectionSerializer):
    """Serializer détaillé pour Hero Section (identique pour l'instant)"""
    pass


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer pour les services"""

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'description', 'icon', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceDetailSerializer(ServiceSerializer):
    """Serializer détaillé pour Service (identique pour l'instant)"""
    pass


class AboutSectionSerializer(serializers.ModelSerializer):
    """Serializer pour la section À propos"""

    class Meta:
        model = AboutSection
        fields = [
            'id', 'title', 'description', 'mission_statement', 'vision_statement',
            'values', 'image', 'show_statistics', 'years_experience', 'clients_count',
            'projects_count', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class AboutSectionDetailSerializer(AboutSectionSerializer):
    """Serializer détaillé pour About Section (identique pour l'instant)"""
    pass


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer pour les membres de l'équipe"""

    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'position', 'bio', 'photo', 'email', 'linkedin_url',
            'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamMemberDetailSerializer(TeamMemberSerializer):
    """Serializer détaillé pour Team Member (identique pour l'instant)"""
    pass


class FAQCategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories FAQ"""
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'description', 'order', 'is_active', 'questions_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_questions_count(self, obj):
        """Retourne le nombre de questions publiées dans cette catégorie"""
        return obj.questions.filter(is_published=True, is_active=True).count()


class FAQSerializer(serializers.ModelSerializer):
    """Serializer pour les questions FAQ"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FAQ
        fields = [
            'id', 'category', 'category_name', 'question', 'answer',
            'order', 'is_published', 'is_active', 'views_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'views_count', 'created_at', 'updated_at']


class FAQPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour FAQ (seulement les champs nécessaires)"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'category_name', 'question', 'answer', 'order', 'is_published', 'is_active']


class FAQDetailSerializer(FAQSerializer):
    """Serializer détaillé pour FAQ avec catégorie complète"""
    category = FAQCategorySerializer(read_only=True)


class FAQCategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour FAQ Category avec questions nested"""
    questions_count = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'description', 'order', 'is_active', 'questions_count', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_questions_count(self, obj):
        """Retourne le nombre de questions publiées dans cette catégorie"""
        return obj.questions.filter(is_published=True, is_active=True).count()

    def get_questions(self, obj):
        """Retourne les questions publiées de cette catégorie"""
        questions = obj.questions.filter(is_published=True, is_active=True).order_by('order')
        return FAQPublicSerializer(questions, many=True).data


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serializer pour les informations de contact"""

    class Meta:
        model = ContactInfo
        fields = [
            'id', 'company_name', 'email', 'phone', 'address', 'city',
            'country', 'linkedin_url', 'twitter_url', 'facebook_url',
            'working_hours', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer pour les soumissions du formulaire de contact"""

    class Meta:
        model = ContactSubmission
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'need_type',
            'message', 'is_processed', 'submitted_at'
        ]
        read_only_fields = ['id', 'is_processed', 'submitted_at']

    def validate_email(self, value):
        """Validation de l'email"""
        if value and '@' not in value:
            raise serializers.ValidationError("Format d'email invalide.")
        return value.lower()

    def validate_phone(self, value):
        """Validation du téléphone"""
        if value:
            # Enlever les espaces et caractères spéciaux
            cleaned = ''.join(filter(str.isdigit, value))
            if len(cleaned) < 10:
                raise serializers.ValidationError("Le numéro de téléphone doit contenir au moins 10 chiffres.")
        return value

    def create(self, validated_data):
        """
        Lors de la création d'une soumission de contact,
        un signal Django créera automatiquement un Lead dans le CRM
        """
        return super().create(validated_data)


class ContactSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création de soumission (API publique)"""

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'company', 'need_type', 'message']

    def validate_email(self, value):
        """Validation de l'email"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Un email valide est requis.")
        return value.lower()

    def validate_name(self, value):
        """Validation du nom"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return value.strip()

    def validate_message(self, value):
        """Validation du message"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
        return value.strip()


class BusinessCardSerializer(serializers.ModelSerializer):
    """Serializer pour la carte de visite digitale"""

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'full_name', 'job_title', 'tagline', 'bio', 'photo',
            'email', 'phone', 'company_name', 'company_logo', 'website_url',
            'linkedin_url', 'twitter_url', 'github_url',
            'accent_color', 'background_gradient_start', 'background_gradient_end',
            'views_count', 'qr_scans_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'views_count', 'qr_scans_count', 'created_at', 'updated_at']


class BusinessCardPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour la carte de visite (sans stats)"""

    class Meta:
        model = BusinessCard
        fields = [
            'id', 'full_name', 'job_title', 'tagline', 'bio', 'photo',
            'email', 'phone', 'company_name', 'company_logo', 'website_url',
            'linkedin_url', 'twitter_url', 'github_url',
            'accent_color', 'background_gradient_start', 'background_gradient_end'
        ]
        read_only_fields = ['id']


class RecruitmentSerializer(serializers.ModelSerializer):
    """Serializer pour la section Recrutement"""

    class Meta:
        model = Recruitment
        fields = [
            'id', 'title', 'description', 'cta_text', 'email',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecruitmentPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour la section Recrutement (seulement les champs actifs)"""

    class Meta:
        model = Recruitment
        fields = ['id', 'title', 'description', 'cta_text', 'email']
        read_only_fields = ['id']


class TeamHeaderSerializer(serializers.ModelSerializer):
    """Serializer pour l'en-tête de la section Team"""

    class Meta:
        model = TeamHeader
        fields = ['id', 'title_part1', 'title_part2', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamHeaderPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour l'en-tête Team (seulement les champs nécessaires)"""

    class Meta:
        model = TeamHeader
        fields = ['id', 'title_part1', 'title_part2', 'description']
        read_only_fields = ['id']


class SEOSettingsSerializer(serializers.ModelSerializer):
    """Serializer pour la configuration SEO"""

    class Meta:
        model = SEOSettings
        fields = [
            'id', 'meta_title', 'meta_description', 'meta_keywords', 'author_name',
            'og_title', 'og_description', 'og_locale', 'og_image',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SEOSettingsPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour la configuration SEO (seulement les champs nécessaires)"""

    class Meta:
        model = SEOSettings
        fields = [
            'id', 'meta_title', 'meta_description', 'meta_keywords', 'author_name',
            'og_title', 'og_description', 'og_locale', 'og_image'
        ]
        read_only_fields = ['id']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer pour les paramètres globaux du site"""

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'company_name', 'company_tagline',
            'navbar_cta_text', 'mobile_menu_cta_text',
            'footer_nav_title', 'footer_services_title', 'footer_follow_title', 'footer_hours_label',
            'footer_copyright_text', 'footer_legal_text', 'footer_privacy_text', 'footer_terms_text',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SiteSettingsPublicSerializer(serializers.ModelSerializer):
    """Serializer public pour les paramètres du site (seulement les champs nécessaires)"""

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'company_name', 'company_tagline',
            'navbar_cta_text', 'mobile_menu_cta_text',
            'footer_nav_title', 'footer_services_title', 'footer_follow_title', 'footer_hours_label',
            'footer_copyright_text', 'footer_legal_text', 'footer_privacy_text', 'footer_terms_text'
        ]
        read_only_fields = ['id']
