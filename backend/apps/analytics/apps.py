from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'
    verbose_name = 'God View - Analytics'

    def ready(self):
        import apps.analytics.admin  # noqa: F401
