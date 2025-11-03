# Pinnacle Advisors - Site Web Professionnel

Cabinet de conseil expert en supply chain - Site one-page moderne avec Backend Django + Frontend Next.js

![Phase](https://img.shields.io/badge/Phase-7%2F11%20Compl%C3%A9t%C3%A9e-success)
![Backend](https://img.shields.io/badge/Backend-Django%205.2.7-green)
![Frontend](https://img.shields.io/badge/Frontend-Next.js%2015.1.6-blue)
![License](https://img.shields.io/badge/License-Private-red)

---

## 📊 Vue d'Ensemble du Projet

**Pinnacle Advisors** est un projet web complet et professionnel comprenant :

### Backend Django (100% Complet)
- ✅ **26 modèles Django** répartis en 4 apps (core, website, crm, analytics)
- ✅ **API REST complète** avec 117 endpoints (Django REST Framework)
- ✅ **CRM intégré** avec qualification automatique des leads (Hot/Warm/Cold)
- ✅ **Analytics "God View"** - Tracking complet utilisateurs (sessions, events, heatmap)
- ✅ **Django Admin personnalisé** avec badges colorés, actions bulk, filtres avancés
- ✅ **Tâches Celery** pour emails asynchrones et agrégation analytics quotidienne
- ✅ **Signaux Django** - Création automatique de leads depuis le formulaire contact
- ✅ **Documentation OpenAPI/Swagger** complète

### Frontend Next.js (100% Complet)
- ✅ **6 sections animées** (Hero, Services, About, Team, FAQ, Contact)
- ✅ **Responsive 100%** - Mobile/Tablet/Desktop optimisé
- ✅ **Animations Framer Motion** au scroll avec effets fluides
- ✅ **Intégration API complète** - React Query + Axios
- ✅ **Analytics SDK** - Tracking automatique (255 lignes de code)
- ✅ **Formulaire validé** - React Hook Form + Zod
- ✅ **TypeScript strict** - Types 100% alignés avec Django
- ✅ **Tailwind CSS** - Design moderne bleu/vert

### Infrastructure
- ✅ **Scripts PowerShell** pour lancement automatique (start-all.ps1)
- ✅ **VS Code Tasks** intégrés (Ctrl+Shift+P → Run Task)
- ✅ **Configuration complète** (.vscode, .env, configs)
- ✅ **Documentation exhaustive** (LANCEMENT.md, SECURITY.md, CLAUDE.md)

---

## 📈 Statistiques du Projet

```
┌─────────────────────────────────────────────────────────────┐
│               PINNACLE ADVISORS - STATISTIQUES              │
├─────────────────────────────────────────────────────────────┤
│ Backend Django                                              │
│   • Fichiers Python:         65 fichiers                    │
│   • Lignes de code:          9,379 lignes                   │
│   • Modèles Django:          26 modèles                     │
│   • Endpoints API:           117 endpoints                  │
│   • Serializers:             37 serializers                 │
│   • ViewSets:                15 ViewSets                    │
│   • Tâches Celery:           7 tâches                       │
│   • Tests:                   9 fichiers tests               │
│                                                             │
│ Frontend Next.js                                            │
│   • Fichiers TS/TSX:         30 fichiers                    │
│   • Lignes de code:          3,256 lignes                   │
│   • Composants:              11 composants                  │
│   • Sections:                6 sections                     │
│   • Analytics SDK:           255 lignes                     │
│                                                             │
│ Total Projet                                                │
│   • Lignes de code:          ~12,635 lignes                 │
│   • Dépendances:             68 (backend) + 19 (frontend)   │
│   • Progression:             7/11 phases (64%)              │
│   • Temps investi:           ~25 jours                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Démarrage Rapide

### Prérequis
- **Python 3.10+** (backend)
- **Node.js 18+** (frontend)
- **Git**

### Configuration Initiale (UNE FOIS)

PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lancer le Projet

**Option A - Script automatique (⭐ Recommandé):**
```powershell
.\start-all.ps1
```

**Option B - VS Code Tasks:**
1. `Ctrl + Shift + P`
2. `Tasks: Run Task`
3. `🔥 Start ALL (Backend + Frontend)`

**Option C - Manuellement:**

Terminal 1 - Backend:
```powershell
cd backend
.\venv\Scripts\python.exe manage.py runserver
```

Terminal 2 - Frontend:
```powershell
cd frontend
npm run dev
```

### Accès

- **Site Web:** http://localhost:3000
- **API Django:** http://localhost:8000/api/
- **API Docs (Swagger):** http://localhost:8000/api/docs/
- **Django Admin:** http://localhost:8000/admin/
- **Analytics Dashboard:** http://localhost:8000/api/analytics/dashboard/

**Compte Admin:**
- Utilisateur: `admin` (à créer via `python manage.py createsuperuser`)

---

## 📁 Structure du Projet

```
Pinnacle-website/
├── backend/                          # Django Backend
│   ├── apps/
│   │   ├── core/                     # App utilitaire (health check, API root)
│   │   ├── website/                  # Contenu site (13 modèles)
│   │   │   ├── models.py             # HeroSection, Service, About, Team, FAQ, etc.
│   │   │   ├── serializers.py        # 14 serializers (standard, detail, public)
│   │   │   ├── views.py              # 13 ViewSets publics
│   │   │   ├── admin.py              # Admin personnalisé
│   │   │   ├── signals.py            # ContactSubmission → Lead
│   │   │   └── urls.py               # 54 endpoints
│   │   ├── crm/                      # CRM Leads (4 modèles)
│   │   │   ├── models.py             # Lead (auto_qualify), Pipeline, Interaction, Note
│   │   │   ├── serializers.py        # 13 serializers
│   │   │   ├── views.py              # 4 ViewSets (admin-only)
│   │   │   ├── tasks.py              # 3 tâches Celery (emails)
│   │   │   └── urls.py               # 40 endpoints
│   │   └── analytics/                # God View (5 modèles)
│   │       ├── models.py             # Session, PageView, Event, Heatmap, DailyAnalytics
│   │       ├── serializers.py        # 10 serializers
│   │       ├── views.py              # 6 ViewSets (tracking public + admin read)
│   │       ├── tasks.py              # 4 tâches Celery (agrégation quotidienne)
│   │       └── urls.py               # 18 endpoints
│   ├── config/                       # Settings Django
│   │   ├── settings.py               # Configuration complète
│   │   └── urls.py                   # Routing principal
│   ├── templates/                    # Templates Django
│   │   ├── admin/analytics/          # Dashboard analytics, heatmap
│   │   └── emails/crm/               # Email notifications
│   ├── static/                       # Fichiers statiques
│   ├── media/                        # Uploads utilisateur
│   ├── venv/                         # Environnement virtuel
│   ├── requirements.txt              # 68 packages
│   └── manage.py
│
├── frontend/                         # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx                # Layout racine avec metadata
│   │   ├── page.tsx                  # Page one-page
│   │   ├── providers.tsx             # React Query + Analytics init
│   │   ├── globals.css               # Styles globaux Tailwind
│   │   └── card/                     # Business card digitale
│   ├── components/
│   │   ├── sections/                 # 6 sections
│   │   │   ├── Hero.tsx              # Section hero animée
│   │   │   ├── Services.tsx          # Grid 8 services
│   │   │   ├── About.tsx             # Counter animé + mission/vision
│   │   │   ├── Team.tsx              # 6 profils experts
│   │   │   ├── FAQ.tsx               # Accordion + recherche
│   │   │   └── Contact.tsx           # Formulaire validé
│   │   ├── layout/                   # Layout
│   │   │   ├── Navbar.tsx            # Navbar sticky
│   │   │   └── Footer.tsx            # Footer 4 colonnes
│   │   └── ui/                       # UI Components
│   │       ├── Button.tsx            # 4 variants, 3 sizes
│   │       ├── Card.tsx              # Card composable
│   │       └── Input.tsx             # Input/Textarea/Select
│   ├── lib/
│   │   ├── api.ts                    # Client Axios + React Query (274 lignes)
│   │   ├── analytics.ts              # SDK Analytics complet (255 lignes)
│   │   └── utils.ts                  # Utilitaires
│   ├── types/
│   │   └── index.ts                  # Types TypeScript (22 interfaces)
│   ├── public/                       # Assets (vide)
│   ├── package.json                  # 19 packages
│   ├── next.config.ts                # Config Next.js
│   ├── tailwind.config.ts            # Config Tailwind (palette bleu/vert)
│   └── tsconfig.json                 # Config TypeScript
│
├── .vscode/                          # Configuration VS Code
│   ├── tasks.json                    # 3 tasks (backend, frontend, all)
│   ├── settings.json                 # Paramètres workspace
│   └── launch.json                   # Debug Django
│
├── start-all.ps1                     # Script lancement complet
├── start-backend.ps1                 # Script backend seul
├── start-frontend.ps1                # Script frontend seul
├── LANCEMENT.md                      # Guide lancement détaillé
├── SECURITY.md                       # Politique sécurité
├── CLAUDE.md                         # Instructions Claude Code
├── PROJECT_STATUS.md                 # État détaillé du projet
├── NEXT_STEPS.md                     # Plan d'action phases 8-11
└── README.md                         # Ce fichier
```

---

## 🛠️ Stack Technique

### Backend
| Technologie | Version | Usage |
|-------------|---------|-------|
| **Django** | 5.2.7 | Framework web Python |
| **Django REST Framework** | 3.16.1 | API REST |
| **Celery** | 5.5.3 | Tâches asynchrones |
| **Redis** | 7.0.0 | Broker Celery + Cache |
| **PostgreSQL** | psycopg2-binary 2.9.11 | Database (prod) |
| **SQLite** | - | Database (dev) |
| **drf-spectacular** | 0.28.0 | OpenAPI/Swagger |
| **django-admin-interface** | 0.30.1 | Thème admin |
| **django-celery-beat** | 2.8.1 | Tâches périodiques |
| **pytest** | 8.4.2 | Tests unitaires |

### Frontend
| Technologie | Version | Usage |
|-------------|---------|-------|
| **Next.js** | 15.1.6 | Framework React |
| **React** | 19.0.0 | UI Library |
| **TypeScript** | 5.7.3 | Typage statique |
| **Tailwind CSS** | 3.4.17 | Styling utility-first |
| **Framer Motion** | 11.15.0 | Animations fluides |
| **React Query** | 5.62.13 | Data fetching + cache |
| **Axios** | 1.7.9 | HTTP client |
| **React Hook Form** | 7.54.2 | Formulaires |
| **Zod** | 3.24.1 | Validation schema |
| **Heroicons** | 2.2.0 | Icônes |

### Outils
- **VS Code** - Éditeur recommandé
- **PowerShell** - Scripts de lancement
- **Git** - Version control

---

## 📊 Fonctionnalités Principales

### 🌐 Site Web (Frontend)

**6 Sections Animées:**

1. **Hero Section**
   - Animation d'entrée Framer Motion
   - Stats animées (17+ ans d'expérience, 240+ clients)
   - CTA principal
   - Scroll indicator animé

2. **Services**
   - Grid responsive 3 colonnes (1 col mobile)
   - 8 services supply chain
   - Icônes Heroicons
   - Expand/collapse descriptions

3. **About**
   - Counter animé au scroll (IntersectionObserver)
   - Mission et Vision cards
   - 5 valeurs avec icônes
   - Stats dynamiques

4. **Team**
   - 6 profils experts
   - Photos avec hover overlay
   - Liens LinkedIn/Email
   - Section recrutement optionnelle

5. **FAQ**
   - Accordion animé (AnimatePresence)
   - Barre de recherche live
   - 5 catégories
   - 18 questions

6. **Contact**
   - Formulaire validé (React Hook Form + Zod)
   - Validation temps réel
   - Success/Error states
   - Contact info cards

**Features:**
- ✅ Responsive 100% (mobile/tablet/desktop)
- ✅ Animations Framer Motion au scroll
- ✅ Tracking analytics complet
- ✅ Navbar sticky avec scroll spy
- ✅ Footer 4 colonnes avec socials
- ✅ Dark/Light scrollbar custom
- ✅ SEO optimisé (metadata dynamique)

### 🔧 Backend API REST

**117 Endpoints répartis:**

**Website API (54 endpoints - Public):**
- `/api/website/hero/` - Hero section
- `/api/website/services/` - Services supply chain
- `/api/website/about/` - Section à propos
- `/api/website/team/` - Membres équipe
- `/api/website/faq/` - Questions FAQ
- `/api/website/faq-categories/` - Catégories FAQ
- `/api/website/contact-info/` - Informations contact
- `/api/website/contact/` - Soumission formulaire (POST)
- `/api/website/business-card/` - Cartes de visite
- `/api/website/recruitment/` - Section recrutement
- `/api/website/seo-settings/` - Configuration SEO
- `/api/website/site-settings/` - Paramètres globaux

**CRM API (40 endpoints - Admin Only):**
- `/api/crm/leads/` - Gestion leads
  - Actions: `requalify`, `assign`, `convert`, `hot_leads`, `overdue_followups`, `stats`
- `/api/crm/pipelines/` - Pipelines de vente
- `/api/crm/interactions/` - Interactions avec leads
- `/api/crm/notes/` - Notes privées/publiques

**Analytics API (18 endpoints - Mixte):**
- Tracking public (write-only):
  - `/api/analytics/track/session/` - Créer session
  - `/api/analytics/track/pageview/` - Tracker page view
  - `/api/analytics/track/event/` - Tracker événement
  - `/api/analytics/track/heatmap/` - Tracker clic heatmap
  - `/api/analytics/track/batch/` - Batch tracking
- Admin (read-only):
  - `/api/analytics/sessions/` - Voir sessions
  - `/api/analytics/daily/` - Stats quotidiennes
  - `/api/analytics/dashboard/` - Dashboard HTML
  - `/api/analytics/heatmap/` - Heatmap visualisation

**Core API (5 endpoints):**
- `/api/` - API root
- `/api/health/` - Health check
- `/api/schema/` - OpenAPI schema
- `/api/docs/` - Swagger UI
- `/api/redoc/` - ReDoc

### 🎯 CRM avec Qualification Automatique

**Algorithme `Lead.auto_qualify()` (Score 0-100):**

| Critère | Points | Détails |
|---------|--------|---------|
| **Taille entreprise** | 30 pts | GE=30, ETI=25, PME=15, TPE=5 |
| **Budget** | 20-30 pts | Mentionné=20, ≥100k€=+10, ≥50k€=+5 |
| **Urgence** | 15 pts | Keywords: "urgent", "rapidement", "immédiat" |
| **Besoin stratégique** | 15 pts | "transformation", "optimisation", "stratégie" |
| **Qualité message** | 10 pts | >50 mots=10, 20-50=5 |
| **Infos complètes** | 10 pts | Téléphone + Entreprise + Poste |

**Classification:**
- 🔥 **Hot (70-100):** Contact sous 24h - Email auto envoyé
- ☀️ **Warm (40-69):** Contact sous 48-72h - Email auto envoyé
- ❄️ **Cold (0-39):** Nurturing - Pas d'email

### 📈 Analytics "God View"

**Tracking automatique via SDK JavaScript (255 lignes):**

1. **Sessions Utilisateur:**
   - Device type (mobile/tablet/desktop)
   - Browser (Chrome/Firefox/Safari/Edge)
   - OS (Windows/macOS/Linux/Android/iOS)
   - Screen resolution
   - Referrer, Landing page
   - UTM params (source/medium/campaign)
   - Durée session, Pages visitées, Conversion

2. **Page Views:**
   - URL + titre
   - Temps passé sur la page
   - Scroll depth max (%)

3. **Événements Trackés:**
   - Clics navigation (`nav_click`)
   - Clics CTA (`cta_click`)
   - Soumissions formulaires (`form_submit`)
   - Vues sections (`section_view`)
   - Clics socials (`social_click`)
   - Coordonnées x/y pour chaque clic

4. **Heatmap Clics:**
   - Position x/y de chaque clic
   - Agrégation par page
   - Click count

5. **Agrégation Quotidienne (Celery 00:05):**
   - Total sessions, visiteurs uniques
   - Total page views
   - Durée moyenne session
   - Bounce rate, Conversion rate
   - Top 20 pages (JSON)

**Dashboard Analytics:** Visualisation complète avec charts (template Django)

---

## 🎨 Design & UX

**Palette de Couleurs:**
- **Primary Blue:** `#3B82F6` 🔵
- **Success Green:** `#10B981` 🟢
- **Danger Red:** `#EF4444` 🔴 (Hot leads)
- **Warning Orange:** `#F59E0B` 🟠 (Warm leads)

**Inspiration Design:** n8n.io (moderne, animé, one-page scroll)

**Typographie:** Inter (Google Fonts)

**Animations:**
- Fade-in au scroll (Framer Motion)
- Slide-up entry animations
- Counter animé (About stats)
- Accordion smooth (FAQ)
- Hover effects (Cards, Buttons)
- Loading spinners

---

## 🧪 Tests & Qualité

### Tests Backend (Pytest)
- ✅ `apps/website/tests/` - test_models, test_views, test_signals, test_serializers
- ✅ `apps/crm/tests/` - test_models, test_serializers, test_views
- ✅ `apps/analytics/tests/` - test_models
- ⚠️ **Coverage partielle** - À compléter pour tests tasks, vues analytics

**Commandes:**
```bash
cd backend
python manage.py test                    # Tous les tests
python manage.py test apps.website       # Tests website
coverage run --source='apps' manage.py test
coverage report                          # Rapport coverage
```

### Tests Frontend
- ❌ **Aucun test** - À implémenter (Vitest + React Testing Library + Playwright)

---

## 📖 Documentation

| Fichier | Description |
|---------|-------------|
| **[README.md](README.md)** | Ce fichier - Vue d'ensemble |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | État détaillé par phase (✅/❌/🔄) |
| **[NEXT_STEPS.md](NEXT_STEPS.md)** | Plan d'action phases 8-11 |
| **[LANCEMENT.md](LANCEMENT.md)** | Guide lancement détaillé |
| **[SECURITY.md](SECURITY.md)** | Politique sécurité |
| **[CLAUDE.md](CLAUDE.md)** | Instructions Claude Code |
| **[backend/docs/LEAD_QUALIFICATION.md](backend/docs/LEAD_QUALIFICATION.md)** | Système qualification leads |

---

## 🚢 Déploiement (À faire - Phase 10)

### Stack Production Prévue

**Backend:**
- AWS EC2 (Ubuntu Server)
- PostgreSQL (RDS)
- Gunicorn (WSGI server)
- Nginx (reverse proxy + static)
- Redis (Celery broker + cache)
- Celery + Celery Beat (workers)
- AWS S3 (media files)
- Let's Encrypt (SSL/TLS)

**Frontend:**
- Vercel (recommandé) OU
- AWS S3 + CloudFront

**CI/CD:**
- GitHub Actions (à configurer)

**Monitoring:**
- Sentry (error tracking - recommandé)
- AWS CloudWatch (logs)

---

## 📊 État du Projet

| Phase | Description | Statut | Progression |
|-------|-------------|--------|-------------|
| **Phase 1** | Backend Django | ✅ Complet | 100% |
| **Phase 2** | API REST Django | ✅ Complet | 100% |
| **Phase 3** | Admin Interface | ✅ Complet | 100% |
| **Phase 4** | Contenu Réaliste | ✅ Complet | 100% |
| **Phase 5** | Frontend Next.js | ✅ Complet | 100% |
| **Phase 6** | Intégrations (Signals, Emails) | ✅ Complet | 100% |
| **Phase 7** | Analytics Dashboard | ✅ Complet | 100% |
| **Phase 8** | Tests Complets | ⏳ À faire | 30% |
| **Phase 9** | SEO & Performance | ⏳ À faire | 0% |
| **Phase 10** | Déploiement Production | ⏳ À faire | 0% |
| **Phase 11** | Post-Lancement | ⏳ À faire | 0% |

**Progrès Global:** 7/11 phases complètes (64%)

**Temps investi:** ~25 jours
**Temps restant estimé:** 15-20 jours

---

## 🐛 Problèmes Courants & Solutions

### PowerShell: "Exécution de scripts désactivée"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8000 déjà utilisé
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Django introuvable
```powershell
cd backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Redis/Celery non configuré
- **Impact:** Emails envoyés en mode synchrone (OK mais moins optimal)
- **Solution:** Installer Redis localement, puis:
```bash
celery -A config worker -l info
celery -A config beat -l info
```

Voir [LANCEMENT.md](LANCEMENT.md) pour plus de solutions.

---

## 🔐 Sécurité

**Points forts:**
- ✅ SECRET_KEY dans .env (jamais committée)
- ✅ Permissions API (AllowAny public, IsAdminUser admin)
- ✅ CORS configuré (localhost:3000 en dev)
- ✅ CSRF Protection activé
- ✅ Validation stricte (serializers + Zod)
- ✅ SQL Injection impossible (ORM Django)
- ✅ XSS Protection (React auto-escape)

**Recommandations production:**
- [ ] DEBUG=False
- [ ] HTTPS forcé (SECURE_SSL_REDIRECT=True)
- [ ] Rate limiting API (django-ratelimit)
- [ ] Nouveau SECRET_KEY généré
- [ ] ALLOWED_HOSTS restrictif
- [ ] Logs Sentry configurés

Voir [SECURITY.md](SECURITY.md) pour la politique complète.

---

## 👥 Contribution

Ce projet est **privé**. Pour toute question, contactez l'équipe de développement.

---

## 📝 License

**Propriétaire** - Tous droits réservés © 2025 Pinnacle Advisors

---

## 🎉 Remerciements

Développé avec ❤️ pour Pinnacle Advisors

**Stack:** Django 5.2.7 + Next.js 15.1.6 + TypeScript + Tailwind CSS + Framer Motion

---

**Dernière mise à jour:** 03 Novembre 2025
**Version:** 2.0.0
**Audit complet effectué le:** 03 Novembre 2025
