"""
ViewSets pour l'API Website
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import (
    HeroSection,
    Service,
    AboutSection,
    TeamMember,
    FAQCategory,
    FAQ,
    ContactInfo,
    ContactSubmission,
    BusinessCard,
    Recruitment,
    TeamHeader,
    SEOSettings,
    SiteSettings
)
from .serializers import (
    HeroSectionSerializer,
    HeroSectionDetailSerializer,
    ServiceSerializer,
    ServiceDetailSerializer,
    AboutSectionSerializer,
    AboutSectionDetailSerializer,
    TeamMemberSerializer,
    TeamMemberDetailSerializer,
    FAQCategorySerializer,
    FAQCategoryDetailSerializer,
    FAQSerializer,
    FAQDetailSerializer,
    FAQPublicSerializer,
    ContactInfoSerializer,
    ContactSubmissionSerializer,
    ContactSubmissionCreateSerializer,
    BusinessCardSerializer,
    BusinessCardPublicSerializer,
    RecruitmentSerializer,
    RecruitmentPublicSerializer,
    TeamHeaderSerializer,
    TeamHeaderPublicSerializer,
    SEOSettingsSerializer,
    SEOSettingsPublicSerializer,
    SiteSettingsSerializer,
    SiteSettingsPublicSerializer
)


class HeroSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les sections Hero
    GET /api/website/hero/
    GET /api/website/hero/{id}/
    GET /api/website/hero/active/ (custom action)
    """
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HeroSectionDetailSerializer
        return HeroSectionSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la section hero active"""
        try:
            hero = HeroSection.objects.get(is_active=True)
            serializer = HeroSectionDetailSerializer(hero)
            return Response(serializer.data)
        except HeroSection.DoesNotExist:
            return Response(
                {'detail': 'Aucune section hero active trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les services
    GET /api/website/services/
    GET /api/website/services/{id}/
    Filtres: is_active
    """
    queryset = Service.objects.filter(is_active=True).order_by('order')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceSerializer


class AboutSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les sections À propos
    GET /api/website/about/
    GET /api/website/about/{id}/
    GET /api/website/about/active/ (custom action)
    """
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AboutSectionDetailSerializer
        return AboutSectionSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la section à propos active"""
        try:
            about = AboutSection.objects.get(is_active=True)
            serializer = AboutSectionDetailSerializer(about)
            return Response(serializer.data)
        except AboutSection.DoesNotExist:
            return Response(
                {'detail': 'Aucune section à propos active trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les membres de l'équipe
    GET /api/website/team/
    GET /api/website/team/{id}/
    Filtres: is_active
    """
    queryset = TeamMember.objects.filter(is_active=True).order_by('order')
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamMemberDetailSerializer
        return TeamMemberSerializer


class FAQCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories FAQ
    GET /api/website/faq-categories/
    GET /api/website/faq-categories/{id}/
    Retourne les catégories avec leurs questions publiées
    """
    queryset = FAQCategory.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        # Utiliser DetailSerializer pour list et retrieve pour inclure les questions
        if self.action in ['list', 'retrieve']:
            return FAQCategoryDetailSerializer
        return FAQCategorySerializer


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les FAQ
    GET /api/website/faq/
    GET /api/website/faq/{id}/
    POST /api/website/faq/{id}/increment_views/
    Filtres: category, is_published
    """
    queryset = FAQ.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = FAQPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'is_published']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FAQDetailSerializer
        return FAQPublicSerializer

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """
        Incrémente le compteur de vues pour une FAQ
        POST /api/website/faq/{id}/increment_views/
        """
        faq = self.get_object()
        faq.views_count += 1
        faq.save(update_fields=['views_count'])

        return Response({
            'detail': 'Compteur de vues incrémenté',
            'views_count': faq.views_count
        })


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les informations de contact
    GET /api/website/contact-info/
    GET /api/website/contact-info/active/ (custom action)
    """
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne les informations de contact actives"""
        try:
            contact_info = ContactInfo.objects.get(is_active=True)
            serializer = ContactInfoSerializer(contact_info)
            return Response(serializer.data)
        except ContactInfo.DoesNotExist:
            return Response(
                {'detail': 'Aucune information de contact active trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class ContactSubmissionViewSet(viewsets.GenericViewSet):
    """
    ViewSet pour les soumissions de formulaire de contact
    POST /api/website/contact/ (create only)
    Capture automatiquement l'IP et le User-Agent
    """
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Crée une nouvelle soumission de contact
        Capture automatiquement l'IP et le User-Agent
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Capturer l'IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Capturer le User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Sauvegarder avec IP et User-Agent
        contact_submission = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Retourner la réponse
        response_serializer = ContactSubmissionSerializer(contact_submission)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class BusinessCardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la carte de visite digitale
    GET /api/website/business-card/
    GET /api/website/business-card/active/ (custom action)
    POST /api/website/business-card/{id}/increment_views/ (custom action)
    """
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardPublicSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la carte de visite active"""
        try:
            card = BusinessCard.objects.get(is_active=True)
            serializer = BusinessCardPublicSerializer(card)
            return Response(serializer.data)
        except BusinessCard.DoesNotExist:
            return Response(
                {'detail': 'Aucune carte de visite active trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """
        Incrémente le compteur de vues de la carte
        POST /api/website/business-card/{id}/increment_views/
        """
        card = self.get_object()
        card.increment_views()

        return Response({
            'detail': 'Compteur de vues incrémenté',
            'views_count': card.views_count
        })

    @action(detail=True, methods=['post'])
    def increment_qr_scans(self, request, pk=None):
        """
        Incrémente le compteur de scans QR code
        POST /api/website/business-card/{id}/increment_qr_scans/
        """
        card = self.get_object()
        card.increment_qr_scans()

        return Response({
            'detail': 'Compteur de scans QR code incrémenté',
            'qr_scans_count': card.qr_scans_count
        })

    @action(detail=True, methods=['get'])
    def vcard(self, request, pk=None):
        """
        Génère et télécharge un fichier vCard (.vcf)
        GET /api/website/business-card/{id}/vcard/
        """
        from django.http import HttpResponse

        card = self.get_object()

        # Générer le contenu vCard
        vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{card.full_name}
N:{card.full_name.split()[-1]};{' '.join(card.full_name.split()[:-1])};;;
TITLE:{card.job_title}
ORG:{card.company_name}
EMAIL;TYPE=INTERNET,WORK:{card.email}
TEL;TYPE=WORK,VOICE:{card.phone}
URL:{card.website_url}
URL;TYPE=LinkedIn:{card.linkedin_url}"""

        if card.twitter_url:
            vcard_content += f"\nURL;TYPE=Twitter:{card.twitter_url}"

        if card.github_url:
            vcard_content += f"\nURL;TYPE=GitHub:{card.github_url}"

        vcard_content += f"\nNOTE:{card.tagline}"
        vcard_content += "\nEND:VCARD"

        # Créer la réponse HTTP avec le fichier vCard
        response = HttpResponse(vcard_content, content_type='text/vcard; charset=utf-8')
        filename = f"{card.full_name.replace(' ', '_')}.vcf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


class RecruitmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la section Recrutement
    GET /api/website/recruitment/
    GET /api/website/recruitment/{id}/
    GET /api/website/recruitment/active/ (custom action)
    """
    queryset = Recruitment.objects.all()
    serializer_class = RecruitmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retourne uniquement les sections actives pour le public"""
        return Recruitment.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Utilise le serializer public pour les endpoints publics"""
        return RecruitmentPublicSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la section recrutement active"""
        try:
            recruitment = Recruitment.objects.get(is_active=True)
            serializer = RecruitmentPublicSerializer(recruitment)
            return Response(serializer.data)
        except Recruitment.DoesNotExist:
            return Response(
                {'detail': 'Aucune section recrutement active'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Recruitment.MultipleObjectsReturned:
            # Si plusieurs actives (ne devrait pas arriver), prendre la première
            recruitment = Recruitment.objects.filter(is_active=True).first()
            serializer = RecruitmentPublicSerializer(recruitment)
            return Response(serializer.data)


class TeamHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour l'en-tête de la section Team
    GET /api/website/team-header/
    GET /api/website/team-header/{id}/
    GET /api/website/team-header/active/ (custom action)
    """
    queryset = TeamHeader.objects.all()
    serializer_class = TeamHeaderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retourne uniquement les en-têtes actifs pour le public"""
        return TeamHeader.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Utilise le serializer public pour les endpoints publics"""
        return TeamHeaderPublicSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne l'en-tête de la section Team active"""
        try:
            header = TeamHeader.objects.get(is_active=True)
            serializer = TeamHeaderPublicSerializer(header)
            return Response(serializer.data)
        except TeamHeader.DoesNotExist:
            return Response(
                {'detail': 'Aucun en-tête Team actif'},
                status=status.HTTP_404_NOT_FOUND
            )
        except TeamHeader.MultipleObjectsReturned:
            # Si plusieurs actives (ne devrait pas arriver), prendre la première
            header = TeamHeader.objects.filter(is_active=True).first()
            serializer = TeamHeaderPublicSerializer(header)
            return Response(serializer.data)


class SEOSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la configuration SEO
    GET /api/website/seo-settings/
    GET /api/website/seo-settings/{id}/
    GET /api/website/seo-settings/active/ (custom action)
    """
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retourne uniquement la configuration active pour le public"""
        return SEOSettings.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Utilise le serializer public pour les endpoints publics"""
        return SEOSettingsPublicSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la configuration SEO active"""
        try:
            seo_settings = SEOSettings.objects.get(is_active=True)
            serializer = SEOSettingsPublicSerializer(seo_settings)
            return Response(serializer.data)
        except SEOSettings.DoesNotExist:
            return Response(
                {'detail': 'Aucune configuration SEO active'},
                status=status.HTTP_404_NOT_FOUND
            )
        except SEOSettings.MultipleObjectsReturned:
            # Si plusieurs actives (ne devrait pas arriver), prendre la première
            seo_settings = SEOSettings.objects.filter(is_active=True).first()
            serializer = SEOSettingsPublicSerializer(seo_settings)
            return Response(serializer.data)


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les paramètres globaux du site
    GET /api/website/site-settings/
    GET /api/website/site-settings/{id}/
    GET /api/website/site-settings/active/ (custom action)
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retourne uniquement les paramètres actifs pour le public"""
        return SiteSettings.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Utilise le serializer public pour les endpoints publics"""
        return SiteSettingsPublicSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne les paramètres du site actifs"""
        try:
            site_settings = SiteSettings.objects.get(is_active=True)
            serializer = SiteSettingsPublicSerializer(site_settings)
            return Response(serializer.data)
        except SiteSettings.DoesNotExist:
            return Response(
                {'detail': 'Aucun paramètre de site actif'},
                status=status.HTTP_404_NOT_FOUND
            )
        except SiteSettings.MultipleObjectsReturned:
            # Si plusieurs actifs (ne devrait pas arriver), prendre le premier
            site_settings = SiteSettings.objects.filter(is_active=True).first()
            serializer = SiteSettingsPublicSerializer(site_settings)
            return Response(serializer.data)
