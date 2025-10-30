from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo, ContactSubmission, BusinessCard,
    Recruitment, TeamHeader, SEOSettings, SiteSettings
)


class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('Contenu Principal', {
            'fields': ('title', 'subtitle', 'cta_text', 'cta_link')
        }),
        ('Médias', {
            'fields': ('background_image', 'video_url')
        }),
        ('Paramètres', {
            'fields': ('is_active', 'updated_at')
        }),
    )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'title')
    readonly_fields = ('created_at', 'updated_at')


class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'years_experience', 'clients_count', 'projects_count', 'show_statistics')
    list_filter = ('show_statistics',)
    readonly_fields = ('updated_at',)
    exclude = ('is_active',)  # Masquer is_active, toujours à True par défaut

    fieldsets = (
        ('Contenu Principal', {
            'fields': ('title', 'description')
        }),
        ('Mission & Vision', {
            'fields': ('mission_statement', 'vision_statement', 'values'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('show_statistics', 'years_experience', 'clients_count', 'projects_count'),
            'description': 'Cochez "Afficher les statistiques" pour afficher cette section sur le site'
        }),
        ('Médias', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Informations', {
            'fields': ('updated_at',)
        }),
    )


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'email')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at', 'photo_preview')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.photo.url)
        return "Pas de photo"
    photo_preview.short_description = 'Aperçu'


class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'questions_count')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Questions'


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'category', 'order', 'is_published', 'is_active', 'views_count')
    list_filter = ('is_published', 'is_active', 'category')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_published', 'is_active')
    ordering = ('category__order', 'order')
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'

    actions = ['publish_questions', 'unpublish_questions']

    def publish_questions(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} question(s) publiée(s).')
    publish_questions.short_description = 'Publier les questions'

    def unpublish_questions(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} question(s) retirée(s).')
    unpublish_questions.short_description = 'Retirer les questions'


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone', 'city', 'is_active')
    list_filter = ('is_active', 'country')
    readonly_fields = ('updated_at',)


class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'need_type_badge', 'is_processed', 'submitted_at')
    list_filter = ('is_processed', 'need_type', 'submitted_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('name', 'email', 'phone', 'company', 'need_type', 'message',
                      'ip_address', 'user_agent', 'submitted_at')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'

    def need_type_badge(self, obj):
        colors = {
            'optimization': '#10B981',
            'audit': '#3B82F6',
            'strategy': '#8B5CF6',
            'digital': '#F59E0B',
            'training': '#EC4899',
            'other': '#6B7280',
        }
        color = colors.get(obj.need_type, '#6B7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px;">{}</span>',
            color, obj.get_need_type_display()
        )
    need_type_badge.short_description = 'Type de besoin'

    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_processed=True, processed_at=timezone.now())
        self.message_user(request, f'{updated} soumission(s) traitée(s).')
    mark_as_processed.short_description = 'Marquer comme traité'


class BusinessCardAdmin(admin.ModelAdmin):
    """Admin personnalisé pour la carte de visite digitale"""
    list_display = ('full_name', 'job_title', 'company_name', 'is_active_badge', 'views_count', 'qr_scans_count', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'job_title', 'company_name', 'email', 'tagline')
    readonly_fields = ('photo_preview', 'logo_preview', 'views_count', 'qr_scans_count',
                      'created_at', 'updated_at', 'qr_code_url', 'preview_link')

    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('full_name', 'job_title', 'tagline', 'bio', 'photo', 'photo_preview')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Entreprise', {
            'fields': ('company_name', 'company_logo', 'logo_preview', 'website_url')
        }),
        ('Réseaux Sociaux', {
            'fields': ('linkedin_url', 'twitter_url', 'github_url'),
            'classes': ('collapse',)
        }),
        ('Personnalisation Design', {
            'fields': ('accent_color', 'background_gradient_start', 'background_gradient_end'),
            'classes': ('collapse',),
            'description': 'Personnalisez les couleurs de votre carte de visite'
        }),
        ('Statistiques & Paramètres', {
            'fields': ('is_active', 'views_count', 'qr_scans_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Liens Utiles', {
            'fields': ('preview_link', 'qr_code_url'),
            'classes': ('collapse',),
            'description': 'Liens pour accéder et partager votre carte'
        }),
    )

    def photo_preview(self, obj):
        """Affiche un aperçu de la photo de profil"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 150px; border-radius: 50%;" />',
                obj.photo.url
            )
        return "Pas de photo"
    photo_preview.short_description = 'Aperçu Photo'

    def logo_preview(self, obj):
        """Affiche un aperçu du logo entreprise"""
        if obj.company_logo:
            return format_html(
                '<img src="{}" style="max-height: 80px;" />',
                obj.company_logo.url
            )
        return "Pas de logo"
    logo_preview.short_description = 'Aperçu Logo'

    def is_active_badge(self, obj):
        """Badge coloré pour l'état actif"""
        if obj.is_active:
            return format_html(
                '<span style="background: #10B981; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold;">✓ ACTIVE</span>'
            )
        return format_html(
            '<span style="background: #6B7280; color: white; padding: 4px 10px; border-radius: 6px;">INACTIVE</span>'
        )
    is_active_badge.short_description = 'Statut'

    def preview_link(self, obj):
        """Lien pour prévisualiser la carte"""
        if obj.id:
            url = f'/card'  # URL frontend
            return format_html(
                '<a href="{}" target="_blank" style="background: #3B82F6; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; display: inline-block;">🔗 Voir la Carte de Visite</a>',
                url
            )
        return "Sauvegardez d'abord pour obtenir le lien"
    preview_link.short_description = 'Prévisualisation'

    def qr_code_url(self, obj):
        """URL pour générer un QR code"""
        if obj.id:
            card_url = f'http://localhost:3000/card'  # URL complète
            qr_api_url = f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={card_url}'
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>URL de la carte:</strong> <code>{}</code></p>'
                '<p><strong>QR Code:</strong></p>'
                '<img src="{}" style="max-width: 200px; border: 2px solid #ddd; padding: 10px;" />'
                '<p style="margin-top: 10px;">'
                '<a href="{}" download="qr_code.png" style="background: #10B981; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; display: inline-block; margin-right: 10px;">⬇ Télécharger QR Code</a>'
                '<small style="color: #6B7280;">Utilisez ce QR code dans votre signature email</small>'
                '</p>'
                '</div>',
                card_url, qr_api_url, qr_api_url
            )
        return "Sauvegardez d'abord pour générer le QR code"
    qr_code_url.short_description = 'QR Code'
    qr_code_url.allow_tags = True

    actions = ['activate_card', 'deactivate_card', 'reset_stats']

    def activate_card(self, request, queryset):
        """Active la carte sélectionnée (désactive les autres)"""
        if queryset.count() > 1:
            self.message_user(request, "Sélectionnez une seule carte à activer.", level='warning')
            return

        card = queryset.first()
        BusinessCard.objects.all().update(is_active=False)
        card.is_active = True
        card.save()
        self.message_user(request, f'Carte "{card.full_name}" activée avec succès.')
    activate_card.short_description = 'Activer cette carte'

    def deactivate_card(self, request, queryset):
        """Désactive les cartes sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} carte(s) désactivée(s).')
    deactivate_card.short_description = 'Désactiver les cartes'

    def reset_stats(self, request, queryset):
        """Réinitialise les compteurs de vues et scans"""
        updated = queryset.update(views_count=0, qr_scans_count=0)
        self.message_user(request, f'Statistiques réinitialisées pour {updated} carte(s).')
    reset_stats.short_description = 'Réinitialiser les statistiques'


class RecruitmentAdmin(admin.ModelAdmin):
    """Admin pour la section Recrutement"""
    list_display = ('title', 'display_status', 'email', 'order', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'email')
    list_editable = ('order',)
    ordering = ('order',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'description', 'cta_text')
        }),
        ('Contact', {
            'fields': ('email',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order', 'created_at', 'updated_at')
        }),
    )

    def display_status(self, obj):
        """Affiche le statut avec un badge coloré"""
        if obj.is_active:
            color = '#10B981'
            icon = '✅'
            text = 'Actif'
        else:
            color = '#EF4444'
            icon = '❌'
            text = 'Inactif'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; display: inline-block;">'
            '{} {}</span>',
            color, icon, text
        )
    display_status.short_description = 'Statut'

    actions = ['activate_section', 'deactivate_section']

    def activate_section(self, request, queryset):
        """Active les sections sélectionnées (désactive les autres)"""
        # Désactiver toutes les sections
        Recruitment.objects.all().update(is_active=False)
        # Activer seulement la première sélectionnée (une seule peut être active)
        first = queryset.first()
        if first:
            first.is_active = True
            first.save()
            self.message_user(request, f'Section "{first.title}" activée.')
        else:
            self.message_user(request, 'Aucune section sélectionnée.', level='warning')
    activate_section.short_description = 'Activer la section (désactive les autres)'

    def deactivate_section(self, request, queryset):
        """Désactive les sections sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} section(s) désactivée(s).')
    deactivate_section.short_description = 'Désactiver les sections'


class TeamHeaderAdmin(admin.ModelAdmin):
    """Admin pour l'en-tête de la section Team"""
    list_display = ('get_full_title', 'display_status', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title_part1', 'title_part2', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Titre', {
            'fields': ('title_part1', 'title_part2'),
            'description': 'Le titre est composé de deux parties : la première avec gradient, la seconde en noir'
        }),
        ('Contenu', {
            'fields': ('description',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    def get_full_title(self, obj):
        """Affiche le titre complet"""
        return f"{obj.title_part1} {obj.title_part2}"
    get_full_title.short_description = 'Titre complet'

    def display_status(self, obj):
        """Affiche le statut avec un badge coloré"""
        if obj.is_active:
            color = '#10B981'
            icon = '✅'
            text = 'Actif'
        else:
            color = '#EF4444'
            icon = '❌'
            text = 'Inactif'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; display: inline-block;">'
            '{} {}</span>',
            color, icon, text
        )
    display_status.short_description = 'Statut'

    actions = ['activate_header', 'deactivate_header']

    def activate_header(self, request, queryset):
        """Active l'en-tête sélectionné (désactive les autres)"""
        # Désactiver tous les en-têtes
        TeamHeader.objects.all().update(is_active=False)
        # Activer seulement le premier sélectionné
        first = queryset.first()
        if first:
            first.is_active = True
            first.save()
            self.message_user(request, f'En-tête "{first.title_part1} {first.title_part2}" activé.')
        else:
            self.message_user(request, 'Aucun en-tête sélectionné.', level='warning')
    activate_header.short_description = 'Activer l\'en-tête (désactive les autres)'

    def deactivate_header(self, request, queryset):
        """Désactive les en-têtes sélectionnés"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} en-tête(s) désactivé(s).')
    deactivate_header.short_description = 'Désactiver les en-têtes'


class SEOSettingsAdmin(admin.ModelAdmin):
    """Admin pour la configuration SEO du site"""
    list_display = ('meta_title_preview', 'display_status', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('meta_title', 'meta_description', 'meta_keywords')
    readonly_fields = ('created_at', 'updated_at', 'og_image_preview')

    fieldsets = (
        ('Métadonnées SEO Standards', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'author_name'),
            'description': 'Ces informations apparaissent dans les résultats de recherche Google'
        }),
        ('OpenGraph (Réseaux Sociaux)', {
            'fields': ('og_title', 'og_description', 'og_locale', 'og_image', 'og_image_preview'),
            'description': 'Optimisation pour le partage sur Facebook, LinkedIn, Twitter, etc.',
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    def meta_title_preview(self, obj):
        """Affiche un aperçu du titre SEO"""
        return obj.meta_title[:60] + '...' if len(obj.meta_title) > 60 else obj.meta_title
    meta_title_preview.short_description = 'Titre SEO'

    def og_image_preview(self, obj):
        """Affiche un aperçu de l'image OpenGraph"""
        if obj.og_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; border: 2px solid #ddd; padding: 10px;" />',
                obj.og_image.url
            )
        return "Pas d'image OpenGraph (utilisera l'image par défaut)"
    og_image_preview.short_description = 'Aperçu Image OpenGraph'

    def display_status(self, obj):
        """Affiche le statut avec un badge coloré"""
        if obj.is_active:
            color = '#10B981'
            icon = '✅'
            text = 'Actif'
        else:
            color = '#EF4444'
            icon = '❌'
            text = 'Inactif'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; display: inline-block;">'
            '{} {}</span>',
            color, icon, text
        )
    display_status.short_description = 'Statut'

    actions = ['activate_config', 'deactivate_config']

    def activate_config(self, request, queryset):
        """Active la configuration sélectionnée (désactive les autres)"""
        SEOSettings.objects.all().update(is_active=False)
        first = queryset.first()
        if first:
            first.is_active = True
            first.save()
            self.message_user(request, f'Configuration SEO "{first.meta_title[:30]}..." activée.')
        else:
            self.message_user(request, 'Aucune configuration sélectionnée.', level='warning')
    activate_config.short_description = 'Activer cette configuration (désactive les autres)'

    def deactivate_config(self, request, queryset):
        """Désactive les configurations sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} configuration(s) désactivée(s).')
    deactivate_config.short_description = 'Désactiver les configurations'


class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin pour les paramètres globaux du site"""
    list_display = ('company_name', 'display_status', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company_name', 'company_tagline')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Branding', {
            'fields': ('company_name', 'company_tagline'),
            'description': 'Informations affichées sur tout le site'
        }),
        ('Navigation', {
            'fields': ('navbar_cta_text', 'mobile_menu_cta_text'),
            'description': 'Textes des boutons d\'appel à l\'action dans la barre de navigation'
        }),
        ('Footer - Titres de Sections', {
            'fields': ('footer_nav_title', 'footer_services_title', 'footer_follow_title', 'footer_hours_label'),
            'description': 'Titres des différentes sections dans le pied de page'
        }),
        ('Footer - Copyright et Liens Légaux', {
            'fields': ('footer_copyright_text', 'footer_legal_text', 'footer_privacy_text', 'footer_terms_text'),
            'description': 'Textes de copyright et liens légaux (utilisez {year} pour l\'année automatique)'
        }),
        ('Paramètres', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    def display_status(self, obj):
        """Affiche le statut avec un badge coloré"""
        if obj.is_active:
            color = '#10B981'
            icon = '✅'
            text = 'Actif'
        else:
            color = '#EF4444'
            icon = '❌'
            text = 'Inactif'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; display: inline-block;">'
            '{} {}</span>',
            color, icon, text
        )
    display_status.short_description = 'Statut'

    actions = ['activate_settings', 'deactivate_settings']

    def activate_settings(self, request, queryset):
        """Active les paramètres sélectionnés (désactive les autres)"""
        SiteSettings.objects.all().update(is_active=False)
        first = queryset.first()
        if first:
            first.is_active = True
            first.save()
            self.message_user(request, f'Paramètres pour "{first.company_name}" activés.')
        else:
            self.message_user(request, 'Aucun paramètre sélectionné.', level='warning')
    activate_settings.short_description = 'Activer ces paramètres (désactive les autres)'

    def deactivate_settings(self, request, queryset):
        """Désactive les paramètres sélectionnés"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} paramètre(s) désactivé(s).')
    deactivate_settings.short_description = 'Désactiver les paramètres'


# Enregistrement des modèles dans l'admin
admin.site.register(HeroSection, HeroSectionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(ContactSubmission, ContactSubmissionAdmin)
admin.site.register(BusinessCard, BusinessCardAdmin)
admin.site.register(Recruitment, RecruitmentAdmin)
admin.site.register(TeamHeader, TeamHeaderAdmin)
admin.site.register(SEOSettings, SEOSettingsAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
