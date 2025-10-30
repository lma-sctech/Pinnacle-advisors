from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.website'
    verbose_name = 'Contenu du Site Web'

    def ready(self):
        """Importer les signals et admin quand l'app est prête"""
        import apps.website.signals  # noqa: F401
        import apps.website.admin  # noqa: F401
