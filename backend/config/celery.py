"""
Configuration Celery pour le projet Pinnacle Advisors
"""

import os
from celery import Celery

# Définir le module de settings Django par défaut
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Créer l'instance Celery
app = Celery('pinnacle')

# Charger la configuration depuis Django settings avec le namespace 'CELERY'
# Tous les paramètres Celery dans settings.py doivent commencer par CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-découvrir les tasks dans tous les fichiers tasks.py des apps Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Task de debug pour tester Celery"""
    print(f'Request: {self.request!r}')
