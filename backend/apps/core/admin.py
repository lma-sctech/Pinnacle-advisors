from django.contrib import admin
from django.urls import path
from .admin_dashboard import admin_dashboard_view


class PinnacleAdminSite(admin.AdminSite):
    """
    Custom AdminSite pour Pinnacle Advisors
    avec dashboard personnalise
    """
    site_header = "Pinnacle Advisors"
    site_title = "Pinnacle Admin"
    index_title = "Administration"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard_view), name='admin_dashboard'),
        ]
        return custom_urls + urls


# Remplacer l'admin site par defaut
admin.site = PinnacleAdminSite()
admin.site.site_header = "Pinnacle Advisors"
admin.site.site_title = "Pinnacle Admin"
admin.site.index_title = "Administration"
