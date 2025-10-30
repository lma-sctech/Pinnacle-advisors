from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('health/', views.health_check, name='health_check'),
]
