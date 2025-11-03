# Backend Django - Pinnacle Advisors

**Version:** 2.0 - Dernière mise à jour: 29 Octobre 2025

Backend Django REST API complet pour le site web professionnel du cabinet de conseil en supply chain **Pinnacle Advisors**.

---

## 📋 Vue d'Ensemble du Projet

**Pinnacle Advisors** est une plateforme web professionnelle one-page moderne comprenant :

- ✅ **Backend Django 5.2.7** avec REST API (Django REST Framework 3.16.1)
- ✅ **Frontend Next.js 15** avec TypeScript, Tailwind CSS et Framer Motion
- ✅ **CRM Intégré** avec système de qualification automatique des leads (Hot/Warm/Cold)
- ✅ **God View Analytics** pour tracking complet des utilisateurs (sessions, événements, heatmaps)
- ✅ **Django Admin Personnalisé** avec thème bleu/vert et dashboard KPIs
- ✅ **Celery + Redis** pour tâches asynchrones (emails, agrégations analytics)
- ⏳ **Next.js Frontend** avec design inspiré n8n.io (95% complété)

**Statut Actuel:** ~64% complété (Phases 1-7 complètes, Phase 8 partielle, Phases 9-11 à faire)

---

## 🏗️ Architecture du Projet

### Structure Backend

```
backend/
├── config/              # Configuration Django
│   ├── settings.py      # Settings production-ready
│   ├── urls.py          # URL routing (Admin + API)
│   ├── celery.py        # Configuration Celery
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
├── apps/                # Applications Django (3 apps)
│   ├── core/            # App utilitaire (health check, API root)
│   ├── website/         # Gestion contenu (9 modèles)
│   │   ├── models.py    # HeroSection, Service, About, Team, FAQ, Contact, BusinessCard
│   │   ├── serializers.py # 16 serializers (standard, detail, public, create)
│   │   ├── views.py     # 8 ViewSets ReadOnly + Contact POST
│   │   ├── urls.py      # API endpoints
│   │   ├── admin.py     # Admin personnalisé
│   │   ├── signals.py   # Contact → Lead auto-création
│   │   └── tests/       # Tests unitaires (models, serializers, views, signals)
│   ├── crm/             # CRM (4 modèles)
│   │   ├── models.py    # Lead (auto_qualify), Pipeline, Interaction, Note
│   │   ├── admin.py     # Admin avec badges Hot/Warm/Cold
│   │   ├── tasks.py     # Celery tasks (email notifications)
│   │   ├── utils.py     # Helpers email
│   │   └── tests/       # Tests CRM (auto_qualify exhaustivement testé)
│   │   ⚠️ serializers.py  # ❌ À CRÉER (BLOQUEUR)
│   │   ⚠️ views.py        # ❌ Vide, ViewSets à créer
│   │   ⚠️ urls.py         # ❌ À CRÉER
│   └── analytics/       # God View (5 modèles)
│       ├── models.py    # UserSession, PageView, Event, HeatmapData, DailyAnalytics
│       ├── serializers.py # 13 serializers (batch endpoint, smart increment)
│       ├── views.py     # ViewSets tracking public + admin
│       ├── urls.py      # API endpoints
│       ├── dashboard_views.py # Dashboard analytics avec KPIs + Charts
│       ├── tasks.py     # Celery tasks (agrégation daily, cleanup)
│       ├── admin.py     # Admin analytics
│       └── tests/       # Tests models
├── templates/           # Templates Django
│   ├── admin/           # Templates admin personnalisés
│   │   ├── dashboard.html        # Dashboard CRM/Analytics
│   │   └── analytics/
│   │       ├── dashboard.html    # God View Dashboard (Chart.js)
│   │       └── heatmap.html      # Heatmap viewer (heatmap.js)
│   └── emails/          # Templates emails HTML + TXT
│       └── crm/
│           ├── new_lead_notification.html
│           └── new_lead_notification.txt
├── scripts/             # Scripts utilitaires
│   ├── populate_content.py          # Générer contenu réaliste supply chain
│   └── configure_admin_theme.py     # Configurer thème bleu/vert
├── docs/                # Documentation
│   ├── LEAD_QUALIFICATION.md  # Système qualification automatique (détaillé)
│   ├── TESTING.md            # Guide tests complet (800+ lignes)
│   └── REDIS_WINDOWS.md      # Guide installation Redis sur Windows
├── static/              # Fichiers statiques
├── media/               # Fichiers médias uploadés
├── venv/                # Environnement virtuel Python
├── manage.py            # Script gestion Django
├── requirements.txt     # Dépendances Python (42 packages)
├── pytest.ini           # Configuration pytest
├── .coveragerc          # Configuration coverage
├── pyproject.toml       # Configuration Black + isort
├── .flake8              # Configuration Flake8
├── .env                 # Variables d'environnement (non versionné)
└── .env.example         # Exemple configuration
```

---

## 🎯 Fonctionnalités Principales

### 1. Gestion de Contenu (App `website`)
**9 Modèles Django:**
- `HeroSection` - Section hero avec titre, CTA, background image/video
- `Service` - 8 services supply chain avec descriptions détaillées (300-500 mots)
- `AboutSection` - Mission, vision, valeurs + stats (17 ans, 240 clients, 520 projets)
- `TeamMember` - 6 profils équipe avec bios professionnelles + LinkedIn
- `FAQCategory` - 5 catégories FAQ
- `FAQ` - 18 questions avec réponses ultra-détaillées (400-800 mots)
- `ContactInfo` - Coordonnées cabinet (unique active constraint)
- `ContactSubmission` - Formulaire contact avec auto-création Lead CRM via signal
- `BusinessCard` - Cartes de visite digitales (QR code, vCard export)

**API REST (AllowAny):**
- `GET /api/website/hero/` - Liste sections hero
- `GET /api/website/hero/active/` - Section hero active
- `GET /api/website/services/` - Liste services actifs (ordonnés)
- `GET /api/website/about/active/` - Section about active
- `GET /api/website/team/` - Liste membres équipe
- `GET /api/website/faq-categories/` - Catégories FAQ avec questions nested
- `GET /api/website/faq/` - Liste FAQ publiées
- `POST /api/website/faq/{id}/increment_views/` - Incrémenter vues FAQ
- `GET /api/website/contact-info/active/` - Infos contact actives
- `POST /api/website/contact/` - Soumettre formulaire contact

### 2. CRM (App `crm`)
**4 Modèles Django:**
- `Lead` - Prospects avec **qualification automatique intelligente**
- `Pipeline` - Pipelines de vente (3 pipelines configurés)
- `Interaction` - Historique activités (email, appel, réunion)
- `Note` - Notes privées/publiques

**🔥 Système de Qualification Automatique des Leads:**

Méthode `Lead.auto_qualify()` calcule un **score 0-100** basé sur 6 critères:

| Critère | Points Max | Détails |
|---------|-----------|---------|
| **Taille entreprise** | 30 pts | GE=30, ETI=25, PME=15, TPE=5 |
| **Budget** | 30 pts | Mentionné=20, ≥100k€=+10, ≥50k€=+5 |
| **Urgence** | 15 pts | Mots-clés: "urgent", "rapidement", "immédiat" |
| **Type besoin stratégique** | 15 pts | "transformation", "optimisation", "stratégie" |
| **Qualité message** | 10 pts | >50 mots=10, 20-50=5 |
| **Informations complètes** | 10 pts | Téléphone + Entreprise + Poste = 10 |

**Résultats:**
- 🔥 **Hot (70-100):** Priorité maximale - Contact sous 24h (Badge rouge)
- ☀️ **Warm (40-69):** Priorité moyenne - Contact sous 48-72h (Badge orange)
- ❄️ **Cold (0-39):** Nurturing requis (Badge bleu)

**Workflow Automatique:**
1. Formulaire contact soumis → Signal Django déclenché
2. Lead CRM créé automatiquement avec données contact
3. `auto_qualify()` appelé automatiquement (score calculé)
4. Email notification envoyé via Celery (Hot/Warm uniquement)
5. Dashboard admin mis à jour avec badge coloré

**Documentation complète:** [docs/LEAD_QUALIFICATION.md](docs/LEAD_QUALIFICATION.md)

**⚠️ API CRM:** ❌ **NON IMPLÉMENTÉE** (Bloqueur critique - voir section "Ce qu'il reste à faire")

### 3. God View Analytics (App `analytics`)
**5 Modèles Django:**
- `UserSession` - Sessions utilisateur (device, browser, OS, UTM params, IP, durée)
- `PageView` - Vues pages (URL, title, referrer, scroll depth, temps passé)
- `Event` - Événements (clics, scrolls, interactions) avec coordonnées x/y
- `HeatmapData` - Agrégation clics pour heatmaps (coordonnées + click_count)
- `DailyAnalytics` - Statistiques quotidiennes agrégées (performance, évite queries lourdes)

**API REST Publique (Tracking):**
- `POST /api/analytics/session/` - Créer session
- `POST /api/analytics/pageview/` - Track page view
- `POST /api/analytics/event/` - Track événement
- `POST /api/analytics/heatmap/` - Track clic heatmap (smart increment)
- `POST /api/analytics/batch/` - Batch endpoint (performance)

**API REST Admin (IsAdminUser):**
- `GET /api/analytics/admin/sessions/` - Liste sessions
- `GET /api/analytics/admin/pageviews/` - Liste page views
- `GET /api/analytics/admin/events/` - Liste événements
- `GET /api/analytics/admin/heatmap/` - Données heatmap
- `GET /api/analytics/admin/daily/` - Analytics quotidiennes

**Dashboard Analytics (Staff only):**
- **URL:** `/api/analytics/dashboard/`
- **KPIs:** Sessions, Visiteurs uniques, Pages vues, Durée moyenne, Bounce rate, Conversion
- **Charts Chart.js:** Évolution 7j, Top 10 pages, Devices, Browsers, Sources trafic
- **Funnel de conversion:** 6 étapes (Landing → Services → About → Contact → Submit → Success)
- **Heatmaps:** `/api/analytics/heatmap/` - Visualisation clics avec heatmap.js

**Tâches Celery (Automatiques):**
- `aggregate_daily_analytics()` - Agrégation quotidienne (00:05 via Beat)
- `cleanup_old_heatmap_data()` - Nettoyage données >180 jours (hebdomadaire)
- `aggregate_all_missing_days()` - Rattrapage jours manquants
- `generate_analytics_report()` - Génération rapports périodiques

---

## 🚀 Installation & Configuration

### Prérequis
- Python 3.11+
- Redis Server (optionnel mais recommandé pour Celery)
- PostgreSQL (production) ou SQLite (développement)

### 1. Cloner le Projet

```bash
git clone <repo-url>
cd Pinnacle-website/backend
```

### 2. Créer et Activer l'Environnement Virtuel

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
# Si erreur ExecutionPolicy, exécuter:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Packages principaux (42 total):**
- Django 5.2.7
- djangorestframework 3.16.1
- django-cors-headers 4.9.0
- django-admin-interface 0.30.1
- django-filter 25.2
- celery 5.5.3
- redis 7.0.0
- django-celery-results 2.6.0
- django-celery-beat 2.8.1
- pillow 12.0.0
- psycopg2-binary 2.9.11
- python-decouple 3.8

**Packages dev/test:**
- black, flake8, isort (linting)
- pytest-django, coverage, faker, factory-boy (testing)

### 4. Configuration Variables d'Environnement

Copier `.env.example` vers `.env`:
```bash
cp .env.example .env
```

**Générer une SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Variables principales (.env):**
```bash
# Django Core
SECRET_KEY=<générer-nouvelle-clé>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (dev = SQLite, prod = PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3  # Dev
# DATABASE_URL=postgresql://user:pass@localhost:5432/pinnacle_db  # Prod

# Email (dev = console, prod = SMTP)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Dev
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@pinnacle-advisors.tech
CRM_NOTIFICATION_EMAILS=contact@pinnacle-advisors.tech

# Celery + Redis
CELERY_BROKER_URL=redis://localhost:6379/0  # Ou laisser vide (fallback synchrone)
```

### 5. Appliquer les Migrations

```bash
python manage.py migrate
```

**Migrations appliquées automatiquement:**
- Django auth (10 migrations)
- Django admin (3 migrations)
- django-admin-interface (30 migrations)
- django-celery-results (2 migrations)
- django-celery-beat (18 migrations)
- apps.website (1 migration - 9 tables)
- apps.crm (1 migration - 4 tables)
- apps.analytics (1 migration - 5 tables)

**Total:** ~66 migrations, **18 modèles custom**

### 6. Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

### 7. (Optionnel) Charger le Contenu de Démonstration

Génère du contenu réaliste supply chain (8 services, 6 membres équipe, 18 FAQ, 13 leads):

```bash
python scripts/populate_content.py
```

### 8. Lancer le Serveur de Développement

```bash
python manage.py runserver
```

**Accès:**
- **Django Admin:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/
- **Health Check:** http://localhost:8000/api/health/
- **Dashboard Analytics:** http://localhost:8000/api/analytics/dashboard/ (staff only)
- **Heatmaps:** http://localhost:8000/api/analytics/heatmap/ (staff only)

---

## ⚙️ Configuration Celery (Tâches Asynchrones)

**Celery** gère les tâches asynchrones (emails notifications, agrégations analytics).

### Installation Redis (Windows)

**Option 1: WSL2 (Recommandé)**
```bash
wsl --install
sudo apt update && sudo apt install redis-server
sudo service redis-server start
redis-cli ping  # Doit retourner "PONG"
```

**Option 2: Memurai (Windows natif)**
Télécharger: https://www.memurai.com/get-memurai

**Documentation complète:** [docs/REDIS_WINDOWS.md](docs/REDIS_WINDOWS.md)

### Lancer Celery Worker

**Terminal 1 (Worker):**
```bash
cd backend
venv\Scripts\activate
celery -A config worker -l info --pool=solo  # Windows nécessite --pool=solo
```

**Terminal 2 (Beat Scheduler - optionnel):**
```bash
cd backend
venv\Scripts\activate
celery -A config beat -l info
```

**Terminal 3 (Django Server):**
```bash
python manage.py runserver
```

**Monitoring Celery (Optionnel - Flower):**
```bash
pip install flower
celery -A config flower
# → http://localhost:5555
```

**⚠️ Fallback Automatique:** Si Redis non disponible, l'app fonctionne en mode synchrone (emails envoyés directement au lieu de via Celery).

---

## 🧪 Tests

### Exécuter les Tests

**Tous les tests:**
```bash
python manage.py test apps
```

**Tests par app:**
```bash
python manage.py test apps.website
python manage.py test apps.crm
python manage.py test apps.analytics
```

**Tests spécifiques:**
```bash
python manage.py test apps.crm.tests.test_models.LeadAutoQualifyTestCase
```

**Tests en parallèle (plus rapide):**
```bash
python manage.py test apps --parallel
```

### Coverage

**Mesurer coverage:**
```bash
coverage run manage.py test apps
coverage report --show-missing
coverage html  # Génère htmlcov/index.html
```

**Objectif:** >80% coverage

**Status actuel:** ~40% (105 tests créés, besoin de tests intégration API et CRM)

### Linting & Formatting

**Black (formatting):**
```bash
black apps/ config/              # Formater code
black --check apps/ config/      # Vérifier uniquement (CI/CD)
```

**Flake8 (linting):**
```bash
flake8 apps/ config/
```

**isort (import sorting):**
```bash
isort apps/ config/              # Trier imports
isort --check-only apps/         # Vérifier uniquement
```

**Configuration:**
- `.flake8` - max-line-length=100, ignore W503/E203
- `pyproject.toml` - Black + isort config (line-length=100)

**Documentation complète:** [docs/TESTING.md](docs/TESTING.md)

---

## 📡 API Endpoints

### Website API (Public - AllowAny)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/website/hero/` | Liste sections hero |
| GET | `/api/website/hero/active/` | Section hero active unique |
| GET | `/api/website/services/` | Liste services ordonnés |
| GET | `/api/website/services/{id}/` | Détail service |
| GET | `/api/website/about/active/` | Section about active |
| GET | `/api/website/team/` | Liste membres équipe |
| GET | `/api/website/team/{id}/` | Détail membre |
| GET | `/api/website/faq-categories/` | Catégories FAQ (nested questions) |
| GET | `/api/website/faq/` | Liste FAQ publiées |
| POST | `/api/website/faq/{id}/increment_views/` | Incrémenter compteur vues |
| GET | `/api/website/contact-info/active/` | Infos contact actives |
| POST | `/api/website/contact/` | Soumettre formulaire contact |

### Analytics API (Public Tracking - AllowAny)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analytics/session/` | Créer session utilisateur |
| POST | `/api/analytics/pageview/` | Track page view |
| POST | `/api/analytics/event/` | Track événement (clic, scroll) |
| POST | `/api/analytics/heatmap/` | Track clic heatmap |
| POST | `/api/analytics/batch/` | Batch endpoint (multi-events) |

### Analytics API (Admin - IsAdminUser)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/admin/sessions/` | Liste sessions |
| GET | `/api/analytics/admin/pageviews/` | Liste page views |
| GET | `/api/analytics/admin/events/` | Liste événements |
| GET | `/api/analytics/admin/heatmap/` | Données heatmap |
| GET | `/api/analytics/admin/daily/` | Analytics quotidiennes agrégées |

### CRM API (Admin - IsAdminUser)
⚠️ **NON IMPLÉMENTÉ** - À créer (voir section "Ce qu'il reste à faire")

Endpoints prévus:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/crm/leads/` | Liste/Créer leads |
| GET/PUT/DELETE | `/api/crm/leads/{id}/` | Détail/Modifier/Supprimer lead |
| POST | `/api/crm/leads/{id}/requalify/` | Relancer auto-qualification |
| GET/POST | `/api/crm/pipelines/` | Liste/Créer pipelines |
| GET/POST | `/api/crm/interactions/` | Liste/Créer interactions |
| GET/POST | `/api/crm/notes/` | Liste/Créer notes |

---

## 📚 Commandes Django Utiles

### Gestion Database
```bash
# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Vérifier migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name 0001

# SQL d'une migration
python manage.py sqlmigrate app_name 0001
```

### Django Shell
```bash
# Shell Django
python manage.py shell

# Shell iPython (si installé)
python manage.py shell -i ipython
```

**Exemples shell:**
```python
# Tester auto-qualification
from apps.crm.models import Lead
lead = Lead.objects.first()
lead.auto_qualify()
print(f"Score: {lead.qualification_score}, Niveau: {lead.qualification_level}")

# Compter modèles
from apps.website.models import Service, FAQ
print(f"Services: {Service.objects.count()}, FAQ: {FAQ.objects.count()}")

# Tester signal
from apps.website.models import ContactSubmission
contact = ContactSubmission.objects.first()
# Signal auto-crée Lead dans apps.crm.models.Lead
```

### Admin
```bash
# Créer superuser
python manage.py createsuperuser

# Changer mot de passe user
python manage.py changepassword username
```

### Collecte Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Vérifications
```bash
# Vérifier projet (pas d'erreurs)
python manage.py check

# Vérifier configuration déploiement
python manage.py check --deploy

# Vérifier migrations non appliquées
python manage.py showmigrations | grep "\[ \]"
```

---

## ⚠️ Ce qu'il Reste à Faire

### ❌ Bloqueur Critique #1: CRM API (4-6h)
**Priorité:** IMMÉDIATE

Créer l'API REST admin-only pour le CRM:
1. Créer `apps/crm/serializers.py` avec 4 serializers:
   - `LeadSerializer` (standard, detail, create)
   - `PipelineSerializer`
   - `InteractionSerializer`
   - `NoteSerializer`

2. Créer `apps/crm/views.py` avec 4 ViewSets:
   - `LeadViewSet` (IsAdminUser, action custom `requalify`)
   - `PipelineViewSet`
   - `InteractionViewSet`
   - `NoteViewSet`

3. Créer `apps/crm/urls.py` avec router DRF

4. Ajouter dans `config/urls.py`:
   ```python
   path('api/crm/', include('apps.crm.urls'))
   ```

5. Tests: `apps/crm/tests/test_serializers.py` et `test_views.py`

### ❌ Gap #2: Documentation API (2-3h)
**Priorité:** HAUTE

Implémenter OpenAPI/Swagger:
1. `pip install drf-spectacular`
2. Configurer dans `settings.py`
3. Ajouter endpoints `/api/schema/`, `/api/docs/`, `/api/redoc/`
4. Décorer ViewSets avec `@extend_schema`

### ❌ Gap #3: Tests Coverage (1-2 jours)
**Priorité:** HAUTE

Atteindre 80%+ coverage:
- Tests intégration API (website + analytics + crm)
- Tests permissions (AllowAny vs IsAdminUser)
- Tests filtres et pagination
- Tests Celery tasks

### ⏳ Phase 9: SEO & Performance (2-3 jours)
**Priorité:** MOYENNE

Frontend Next.js:
- Metadata (title, description, OpenGraph, Twitter Cards)
- Sitemap.xml dynamique
- Robots.txt
- Schema.org JSON-LD
- Images WebP + lazy loading
- Core Web Vitals >90

### ⏳ Phase 10: Déploiement AWS (5-7 jours)
**Priorité:** BASSE (pré-production)

Infrastructure:
- EC2 Ubuntu + PostgreSQL + Redis
- Gunicorn + Nginx
- SSL/TLS (Let's Encrypt)
- S3 pour médias
- Frontend Vercel ou même EC2
- Monitoring (Sentry, Uptime)
- Backups automatiques

**Documentation complète:** [Plan.global-dev.md](Plan.global-dev.md) - Section "PROCHAINES ÉTAPES PRIORITAIRES"

---

## 🎨 Design & Branding

**Palette Couleurs:**
- Primary Blue: `#3B82F6`
- Success Green: `#10B981`
- Hot/Danger Red: `#EF4444`
- Warm/Warning Orange: `#F59E0B`
- Cold/Info: `#3B82F6`

**Inspiration Design:** n8n.io (moderne, animations fluides, one-page scroll)

**Thème Admin:** django-admin-interface configuré avec bleu/vert

---

## 📖 Documentation Complète

| Fichier | Description |
|---------|-------------|
| [Plan.global-dev.md](Plan.global-dev.md) | Plan développement complet 11 phases (~2200 lignes) |
| [docs/LEAD_QUALIFICATION.md](docs/LEAD_QUALIFICATION.md) | Système qualification automatique détaillé |
| [docs/TESTING.md](docs/TESTING.md) | Guide tests complet (800+ lignes) |
| [docs/REDIS_WINDOWS.md](docs/REDIS_WINDOWS.md) | Installation Redis sur Windows |
| [CLAUDE.md](../CLAUDE.md) | Instructions pour Claude Code |

---

## 🔧 Technologies & Stack

**Backend:**
- Django 5.2.7
- Django REST Framework 3.16.1
- Celery 5.5.3 + Redis 7.0.0
- PostgreSQL (prod) / SQLite (dev)
- Python 3.11+

**Frontend (séparé):**
- Next.js 15.1.6
- React 19
- TypeScript
- Tailwind CSS
- Framer Motion
- Axios + React Query

**DevOps:**
- GitHub Actions CI/CD
- Black + Flake8 + isort (linting)
- pytest + coverage (testing)

**Production (prévu):**
- AWS EC2 (Ubuntu Server)
- Nginx + Gunicorn
- PostgreSQL + Redis
- AWS S3 (médias)
- Let's Encrypt (SSL)

---

## 📊 Statistiques Projet

**Backend:**
- **18 modèles Django** (Website: 9, CRM: 4, Analytics: 5)
- **13 classes admin** personnalisées
- **29/33 serializers** (88% - CRM manquants)
- **13/17 ViewSets** (76% - CRM manquants)
- **2/3 apps API** complètes (Website ✅, Analytics ✅, CRM ❌)
- **~7100 lignes** de code backend
- **105 tests** unitaires créés
- **~40% coverage** (objectif 80%+)

**Frontend:**
- **~3000 lignes** Next.js/TypeScript
- **6 sections** one-page (Hero, Services, About, Team, FAQ, Contact)
- **Analytics SDK** intégré
- **Business Card** page

**Total:** ~14,100 lignes de code

**Progression globale:** ~64% (5.5/11 phases complètes, 2.5 partielles)

---

## 🤝 Contribution & Développement

### Workflow Git (Recommandé)
```bash
# Créer branche feature
git checkout -b feature/nom-feature

# Développer + tests
black apps/ config/
flake8 apps/ config/
python manage.py test apps

# Commit
git add .
git commit -m "feat: description"

# Push
git push origin feature/nom-feature

# Créer Pull Request
```

### Standards Code
- **PEP 8** (via Flake8)
- **Black** pour formatting (line-length=100)
- **isort** pour imports
- **Docstrings** pour fonctions complexes
- **Type hints** recommandés

### Tests Requis
- Nouveaux modèles → tests models
- Nouveaux serializers → tests serializers + validation
- Nouveaux ViewSets → tests API (CRUD, permissions, filtres)
- Nouveaux signals → tests comportement

**Objectif:** >80% coverage

---

## 📞 Support

**Problèmes courants:**

1. **Port 8000 déjà utilisé:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F

   # Linux/Mac
   lsof -ti:8000 | xargs kill -9
   ```

2. **Erreur migrations:**
   ```bash
   python manage.py showmigrations
   python manage.py migrate --fake-initial
   ```

3. **Redis non disponible:**
   L'app fonctionne sans Redis (fallback synchrone). Pour activer Celery, installer Redis (voir [docs/REDIS_WINDOWS.md](docs/REDIS_WINDOWS.md))

4. **Tests échouent:**
   ```bash
   python manage.py test apps --debug-mode
   python manage.py test apps --keepdb  # Garde DB entre exécutions
   ```

**Documentation:** Consulter [docs/TESTING.md](docs/TESTING.md) pour guide complet

---

## 📄 Licence

Propriétaire - Pinnacle Advisors © 2025

---

**Dernière mise à jour:** 29 Octobre 2025
**Version:** 2.0
**Maintenu par:** Claude Code

**Prochaine étape recommandée:** Implémenter CRM API REST (Bloqueur #1 - 4-6h)
