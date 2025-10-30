from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Lead, Pipeline, Interaction, Note


class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'qualification_badge', 'status_badge',
                   'score', 'source', 'assigned_to', 'created_at')
    list_filter = ('qualification', 'status', 'source', 'company_size', 'converted_to_client', 'created_at')
    search_fields = ('name', 'email', 'company', 'phone', 'message')
    readonly_fields = ('score', 'created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Informations', {
            'fields': ('name', 'email', 'phone', 'company', 'company_size', 'position')
        }),
        ('Besoin', {
            'fields': ('need_type', 'message', 'budget_mentioned', 'estimated_budget')
        }),
        ('Qualification', {
            'fields': ('qualification', 'score', 'status', 'pipeline')
        }),
        ('Gestion', {
            'fields': ('assigned_to', 'converted_to_client', 'expected_revenue',
                      'last_contact_date', 'next_follow_up_date', 'internal_notes')
        }),
    )

    def qualification_badge(self, obj):
        colors = {'hot': '#EF4444', 'warm': '#F59E0B', 'cold': '#3B82F6', 'unqualified': '#6B7280'}
        icons = {'hot': '🔥', 'warm': '☀️', 'cold': '❄️', 'unqualified': '❔'}
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 600;">{} {}</span>',
            colors.get(obj.qualification, '#6B7280'), icons.get(obj.qualification, ''),
            obj.get_qualification_display()
        )
    qualification_badge.short_description = 'Qualification'

    def status_badge(self, obj):
        colors = {
            'new': '#10B981', 'contacted': '#3B82F6', 'qualified': '#8B5CF6',
            'proposal': '#F59E0B', 'negotiation': '#EC4899', 'won': '#059669',
            'lost': '#DC2626', 'on_hold': '#6B7280'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6B7280'), obj.get_status_display()
        )
    status_badge.short_description = 'Statut'

    actions = ['assign_to_me', 'mark_as_contacted', 'mark_as_won']

    def assign_to_me(self, request, queryset):
        updated = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{updated} lead(s) assigné(s).')
    assign_to_me.short_description = "M'assigner"

    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted', last_contact_date=timezone.now())
        self.message_user(request, f'{updated} lead(s) contacté(s).')
    mark_as_contacted.short_description = 'Marquer contacté'

    def mark_as_won(self, request, queryset):
        updated = queryset.update(status='won', converted_to_client=True, conversion_date=timezone.now())
        self.message_user(request, f'🎉 {updated} lead(s) converti(s)!')
    mark_as_won.short_description = '🎉 Marquer gagné'


class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 50px; height: 20px; background: {}; border-radius: 4px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Couleur'


class InteractionAdmin(admin.ModelAdmin):
    list_display = ('lead', 'type_icon', 'subject', 'duration_minutes', 'created_by', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('lead__name', 'subject', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def type_icon(self, obj):
        icons = {'email': '📧', 'phone': '📞', 'meeting': '🤝', 'note': '📝'}
        return format_html('{} {}', icons.get(obj.type, '📋'), obj.get_type_display())
    type_icon.short_description = 'Type'

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('lead', 'content_preview', 'is_important', 'is_private', 'created_by', 'created_at')
    list_filter = ('is_important', 'is_private', 'created_at')
    search_fields = ('lead__name', 'content')
    ordering = ('-created_at',)

    def content_preview(self, obj):
        preview = obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
        if obj.is_important:
            return format_html('<strong style="color: #EF4444;">⭐ {}</strong>', preview)
        return preview
    content_preview.short_description = 'Contenu'

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Enregistrement des modèles dans l'admin
admin.site.register(Lead, LeadAdmin)
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Note, NoteAdmin)
