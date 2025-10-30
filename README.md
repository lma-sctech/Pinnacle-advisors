# Pinnacle Advisors - Site Web Complet

Cabinet de conseil expert en supply chain - Site one-page moderne avec Backend Django + Frontend Next.js

![Status](https://img.shields.io/badge/Phase-5%2F11%20Complétée-success)
![Backend](https://img.shields.io/badge/Backend-Django%205.2.7-green)
![Frontend](https://img.shields.io/badge/Frontend-Next.js%2015-blue)
![License](https://img.shields.io/badge/License-Private-red)

## 🎯 Vue d'ensemble

Site web professionnel one-page pour **Pinnacle Advisors**, incluant:

- ✅ **Backend Django REST API** - 17 modèles, 28 serializers, 13 ViewSets
- ✅ **Frontend Next.js** - 6 sections animées, TypeScript, Tailwind CSS
- ✅ **CRM Intégré** - Qualification automatique leads (Hot/Warm/Cold)
- ✅ **Analytics "God View"** - Tracking complet utilisateurs
- ✅ **Django Admin** - Interface de gestion avec thème personnalisé
- ✅ **Contenu Réaliste** - 8 services, 18 FAQ, 13 leads, 6 profils équipe

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.10+ (backend)
- Node.js 18+ (frontend)
- Git

### 1️⃣ Configuration Initiale PowerShell (UNE FOIS)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2️⃣ Lancer le Projet

**Option A - Script automatique (⭐ Recommandé):**
```powershell
.\start-all.ps1
```

**Option B - Manuellement:**

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\python.exe manage.py runserver
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

### 3️⃣ Accéder au Site

- **Site Web:** http://localhost:3000
- **API Django:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/

**Compte Admin:**
- Utilisateur: `admin` (à créer via `python manage.py createsuperuser`)
- Mot de passe: *à définir*

## 📁 Structure du Projet

```
Pinnacle-website/
├── backend/                     # Django Backend
│   ├── apps/
│   │   ├── core/               # App principale
│   │   ├── website/            # Contenu site (8 modèles)
│   │   ├── crm/                # CRM + leads (4 modèles)
│   │   └── analytics/          # God View (5 modèles)
│   ├── config/                 # Settings Django
│   ├── scripts/                # Scripts utilitaires
│   ├── static/                 # Fichiers statiques
│   ├── media/                  # Uploads
│   ├── venv/                   # Environnement virtuel
│   └── manage.py
│
├── frontend/                   # Next.js Frontend
│   ├── app/                    # Next.js App Router
│   ├── components/
│   │   ├── ui/                 # Composants UI (Button, Card, Input)
│   │   ├── layout/             # Navbar, Footer
│   │   └── sections/           # 6 sections du site
│   ├── lib/                    # API client, Analytics SDK
│   ├── types/                  # Types TypeScript
│   ├── public/                 # Assets publics
│   └── package.json
│
├── .vscode/                    # Config VS Code
│   ├── tasks.json              # Tâches intégrées
│   ├── settings.json           # Paramètres
│   └── launch.json             # Debug Django
│
├── start-backend.ps1           # Script lancement backend
├── start-frontend.ps1          # Script lancement frontend
├── start-all.ps1               # Script lancement complet
├── LANCEMENT.md                # Guide de lancement détaillé
└── README.md                   # Ce fichier
```

## 🛠️ Stack Technique

### Backend
- **Django 5.2.7** - Framework web Python
- **Django REST Framework 3.16.1** - API REST
- **SQLite** (dev) → PostgreSQL (prod)
- **Python 3.10+**

### Frontend
- **Next.js 15.1.6** - Framework React
- **React 19.0.0** - UI Library
- **TypeScript 5.7.3** - Typage statique
- **Tailwind CSS 3.4.17** - Styling
- **Framer Motion 11.15.0** - Animations
- **React Query 5.62.13** - Data fetching
- **Axios 1.7.9** - HTTP client

### Outils
- **VS Code** - Éditeur recommandé
- **PowerShell** - Terminal Windows
- **Git** - Version control

## 📊 Fonctionnalités

### ✨ Site Web (Frontend)

**6 Sections Animées:**
1. **Hero** - Animation entrée, stats animées (17+ ans, 240+ clients)
2. **Services** - 8 services supply chain avec expand/collapse
3. **About** - Counter animé, mission/vision, 5 valeurs
4. **Team** - 6 profils experts avec hover effects
5. **FAQ** - 18 questions (5 catégories) + barre de recherche
6. **Contact** - Formulaire validé (React Hook Form + Zod)

**Fonctionnalités:**
- ✅ Responsive 100% (mobile/tablet/desktop)
- ✅ Animations Framer Motion au scroll
- ✅ Tracking analytics complet (sessions, events, heatmap)
- ✅ Navbar sticky avec scroll spy
- ✅ Footer complet avec socials

### 🔧 Backend API

**17 Modèles Django:**
- `HeroSection`, `Service`, `AboutSection`, `TeamMember`
- `FAQCategory`, `FAQ`, `ContactInfo`, `ContactSubmission`
- `Lead`, `Pipeline`, `Interaction`, `Note` (CRM)
- `UserSession`, `PageView`, `Event`, `HeatmapData`, `DailyAnalytics`

**28 Serializers:**
- Standard, Detail, Public, Create variants
- Nested relationships

**13 ViewSets:**
- CRUD complet pour tous les modèles
- Permissions configurables
- Pagination (10 items/page)

### 📈 Analytics "God View"

**Tracking Automatique:**
- ✅ Sessions utilisateurs (device, browser, OS, UTM)
- ✅ Page views (temps passé, scroll depth)
- ✅ Événements custom (CTA, navigation, formulaires)
- ✅ Heatmap clics (coordonnées x/y)

### 🎯 CRM avec Qualification Automatique

**Algorithme auto_qualify():**
- Score 0-100 basé sur 6 critères
- Classification: Hot (70-100), Warm (40-69), Cold (0-39)
- Critères: taille entreprise, budget, urgence, besoin stratégique, qualité message, infos complètes

## 📖 Documentation

- **[LANCEMENT.md](LANCEMENT.md)** - Guide de lancement détaillé
- **[backend/README.md](backend/README.md)** - Doc backend Django
- **[frontend/README.md](frontend/README.md)** - Doc frontend Next.js
- **[backend/Plan.global-dev.md](backend/Plan.global-dev.md)** - Plan de développement complet
- **[backend/COMMANDS.md](backend/COMMANDS.md)** - Référence des commandes

## 🎨 Design

**Palette de Couleurs:**
- Primary Blue: `#3B82F6` 🔵
- Success Green: `#10B981` 🟢
- Danger Red: `#EF4444` 🔴
- Warning Orange: `#F59E0B` 🟠

**Inspiration:** n8n.io (design moderne, animations fluides)

## 🧪 Tests (À faire - Phase 8)

```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm run test
```

## 🚢 Déploiement (À faire - Phase 10)

**Backend:** AWS EC2 + PostgreSQL + Nginx + Gunicorn
**Frontend:** Vercel (recommandé) ou AWS S3 + CloudFront

## 📊 État du Projet

| Phase | Description | Statut | Progression |
|-------|-------------|--------|-------------|
| **1** | Backend Django | ✅ | 100% |
| **2** | API REST | ✅ | 100% |
| **3** | Admin Interface | ✅ | 100% |
| **4** | Contenu | ✅ | 100% |
| **5** | Frontend Next.js | ✅ | 100% |
| **6** | Intégrations (Signals, Emails) | ⏳ | 0% |
| **7** | Analytics Dashboard | ⏳ | 0% |
| **8** | Tests | ⏳ | 0% |
| **9** | SEO & Performance | ⏳ | 0% |
| **10** | Déploiement AWS | ⏳ | 0% |
| **11** | Post-Lancement | ⏳ | 0% |

**Progrès Global:** 5/11 phases (45%)

**Temps investi:** ~15 jours
**Temps restant estimé:** 15-25 jours

## 🐛 Problèmes Courants

Voir **[LANCEMENT.md](LANCEMENT.md)** pour les solutions détaillées.

## 👥 Contribution

Ce projet est privé. Pour toute question, contactez l'équipe de développement.

## 📝 License

Propriétaire - Tous droits réservés © 2025 Pinnacle Advisors

---

**Développé avec ❤️ pour Pinnacle Advisors**

*Dernière mise à jour: 27 Octobre 2025*
