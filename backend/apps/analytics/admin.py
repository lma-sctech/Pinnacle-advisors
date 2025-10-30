from django.contrib import admin
from django.utils.html import format_html
from .models import UserSession, PageView, Event, HeatmapData, DailyAnalytics


class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id_short', 'device_type', 'browser', 'pages_visited',
                   'duration_display', 'converted', 'start_time')
    list_filter = ('device_type', 'browser', 'converted', 'start_time')
    search_fields = ('session_id', 'ip_address', 'landing_page')
    readonly_fields = ('session_id', 'ip_address', 'start_time', 'duration_seconds')
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'

    def session_id_short(self, obj):
        return obj.session_id[:12] + '...'
    session_id_short.short_description = 'Session'

    def duration_display(self, obj):
        minutes = obj.duration_seconds // 60
        return f"{minutes}m" if minutes > 0 else f"{obj.duration_seconds}s"
    duration_display.short_description = 'Durée'


class PageViewAdmin(admin.ModelAdmin):
    list_display = ('page_url_short', 'time_on_page', 'scroll_depth', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('page_url', 'page_title')
    ordering = ('-viewed_at',)
    date_hierarchy = 'viewed_at'

    def page_url_short(self, obj):
        return obj.page_url[:60] + '...' if len(obj.page_url) > 60 else obj.page_url
    page_url_short.short_description = 'URL'


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type_icon', 'event_action', 'element_text_short', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('event_action', 'element_text')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

    def event_type_icon(self, obj):
        icons = {'click': '👆', 'scroll': '📜', 'form_submit': '📝', 'download': '⬇️', 'button': '🔘'}
        return format_html('{} {}', icons.get(obj.event_type, '📋'), obj.get_event_type_display())
    event_type_icon.short_description = 'Type'

    def element_text_short(self, obj):
        if obj.element_text:
            return obj.element_text[:40] + '...' if len(obj.element_text) > 40 else obj.element_text
        return '-'
    element_text_short.short_description = 'Élément'


class HeatmapDataAdmin(admin.ModelAdmin):
    list_display = ('page_url_short', 'position', 'click_count', 'date')
    list_filter = ('date',)
    search_fields = ('page_url',)
    ordering = ('-date', '-click_count')
    date_hierarchy = 'date'

    def page_url_short(self, obj):
        return obj.page_url[:50] + '...' if len(obj.page_url) > 50 else obj.page_url
    page_url_short.short_description = 'Page'

    def position(self, obj):
        return f'({obj.x_position}, {obj.y_position})'
    position.short_description = 'Position'


class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sessions', 'unique_visitors', 'total_pageviews',
                   'avg_session_duration', 'bounce_rate', 'conversion_rate')
    list_filter = ('date',)
    readonly_fields = ('date', 'total_sessions', 'unique_visitors', 'avg_session_duration')
    ordering = ('-date',)
    date_hierarchy = 'date'


# Enregistrement des modèles dans l'admin
admin.site.register(UserSession, UserSessionAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(HeatmapData, HeatmapDataAdmin)
admin.site.register(DailyAnalytics, DailyAnalyticsAdmin)
