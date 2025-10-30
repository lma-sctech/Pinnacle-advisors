"""
URLs pour l'API Website
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HeroSectionViewSet,
    ServiceViewSet,
    AboutSectionViewSet,
    TeamMemberViewSet,
    FAQCategoryViewSet,
    FAQViewSet,
    ContactInfoViewSet,
    ContactSubmissionViewSet,
    BusinessCardViewSet,
    RecruitmentViewSet,
    TeamHeaderViewSet,
    SEOSettingsViewSet,
    SiteSettingsViewSet
)

# Créer le router DRF
router = DefaultRouter()

# Enregistrer les ViewSets
router.register(r'hero', HeroSectionViewSet, basename='hero')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'about', AboutSectionViewSet, basename='about')
router.register(r'team', TeamMemberViewSet, basename='team')
router.register(r'faq-categories', FAQCategoryViewSet, basename='faq-category')
router.register(r'faq', FAQViewSet, basename='faq')
router.register(r'contact-info', ContactInfoViewSet, basename='contact-info')
router.register(r'contact', ContactSubmissionViewSet, basename='contact-submission')
router.register(r'business-card', BusinessCardViewSet, basename='business-card')
router.register(r'recruitment', RecruitmentViewSet, basename='recruitment')
router.register(r'team-header', TeamHeaderViewSet, basename='team-header')
router.register(r'seo-settings', SEOSettingsViewSet, basename='seo-settings')
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')

# URLs de l'app
urlpatterns = [
    path('', include(router.urls)),
]
