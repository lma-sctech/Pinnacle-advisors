"""
URLs pour l'app CRM
API REST admin-only pour gérer les leads, pipelines, interactions et notes
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, PipelineViewSet, InteractionViewSet, NoteViewSet

# Router DRF pour enregistrer les ViewSets
router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'pipelines', PipelineViewSet, basename='pipeline')
router.register(r'interactions', InteractionViewSet, basename='interaction')
router.register(r'notes', NoteViewSet, basename='note')

app_name = 'crm'

urlpatterns = [
    path('', include(router.urls)),
]

"""
Endpoints générés automatiquement:

LEADS:
    GET    /api/crm/leads/                      - Liste leads
    POST   /api/crm/leads/                      - Créer lead
    GET    /api/crm/leads/{id}/                 - Détail lead
    PUT    /api/crm/leads/{id}/                 - Modifier lead (complet)
    PATCH  /api/crm/leads/{id}/                 - Modifier lead (partiel)
    DELETE /api/crm/leads/{id}/                 - Supprimer lead
    POST   /api/crm/leads/{id}/requalify/       - Requalifier lead
    POST   /api/crm/leads/{id}/assign/          - Assigner lead
    POST   /api/crm/leads/{id}/convert/         - Convertir lead
    GET    /api/crm/leads/hot_leads/            - Leads hot
    GET    /api/crm/leads/overdue_followups/    - Suivis en retard
    GET    /api/crm/leads/stats/                - Statistiques

PIPELINES:
    GET    /api/crm/pipelines/                  - Liste pipelines
    POST   /api/crm/pipelines/                  - Créer pipeline
    GET    /api/crm/pipelines/{id}/             - Détail pipeline
    PUT    /api/crm/pipelines/{id}/             - Modifier pipeline
    PATCH  /api/crm/pipelines/{id}/             - Modifier pipeline (partiel)
    DELETE /api/crm/pipelines/{id}/             - Supprimer pipeline
    GET    /api/crm/pipelines/active/           - Pipelines actifs

INTERACTIONS:
    GET    /api/crm/interactions/               - Liste interactions
    POST   /api/crm/interactions/               - Créer interaction
    GET    /api/crm/interactions/{id}/          - Détail interaction
    PUT    /api/crm/interactions/{id}/          - Modifier interaction
    PATCH  /api/crm/interactions/{id}/          - Modifier interaction (partiel)
    DELETE /api/crm/interactions/{id}/          - Supprimer interaction
    GET    /api/crm/interactions/recent/        - Interactions récentes (7j)
    GET    /api/crm/interactions/by_lead/?lead_id=1  - Par lead

NOTES:
    GET    /api/crm/notes/                      - Liste notes
    POST   /api/crm/notes/                      - Créer note
    GET    /api/crm/notes/{id}/                 - Détail note
    PUT    /api/crm/notes/{id}/                 - Modifier note
    PATCH  /api/crm/notes/{id}/                 - Modifier note (partiel)
    DELETE /api/crm/notes/{id}/                 - Supprimer note
    GET    /api/crm/notes/important/            - Notes importantes
    GET    /api/crm/notes/by_lead/?lead_id=1    - Par lead

Filtres disponibles:
    - Leads: ?qualification=hot&status=new&source=website&company_size=ge
    - Pipelines: ?is_active=true
    - Interactions: ?lead=1&type=email&created_by=1
    - Notes: ?lead=1&is_private=false&is_important=true

Recherche (search):
    - Leads: ?search=entreprise (nom, email, company, message, need_type)
    - Pipelines: ?search=vente (name, description)
    - Interactions: ?search=réunion (subject, content, lead__name, lead__company)
    - Notes: ?search=important (content, lead__name, lead__company)

Tri (ordering):
    - Leads: ?ordering=-score ou ?ordering=created_at
    - Pipelines: ?ordering=order
    - Interactions: ?ordering=-created_at
    - Notes: ?ordering=-is_important

Pagination:
    - Par défaut: 10 items par page
    - Changer: ?page_size=25
    - Navigation: ?page=2
"""
