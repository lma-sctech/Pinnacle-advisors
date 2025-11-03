# 🚀 NEXT STEPS - Plan d'Action Pinnacle Advisors

**Date:** 03 Novembre 2025
**Phases restantes:** 4/11 (8, 9, 10, 11)
**Temps estimé total:** 15-20 jours

---

## 📋 Vue d'Ensemble

Ce document présente le **plan d'action détaillé** pour compléter les 4 phases restantes du projet Pinnacle Advisors. Chaque phase contient des **tâches concrètes** avec **commandes exactes** et **critères d'acceptation**.

**État actuel:**
- ✅ Phases 1-7 complètes (64%)
- ⏳ Phase 8 en cours (30%)
- ❌ Phases 9-11 à faire (0%)

---

## 🧪 PHASE 8: TESTS COMPLETS

**Durée estimée:** 3-5 jours
**Priorité:** 🔴 CRITIQUE (avant production)

### Objectif

Atteindre **>80% de couverture de code** pour garantir la stabilité et la maintenabilité du projet.

### Étape 1: Compléter Tests Backend (2 jours)

#### 1.1 Tests Analytics Views

**Fichier à créer:** `backend/apps/analytics/tests/test_views.py`

```bash
cd backend
touch apps/analytics/tests/test_views.py
```

**Tests à implémenter:**
- [ ] Test création session (POST /api/analytics/track/session/)
- [ ] Test création pageview (POST /api/analytics/track/pageview/)
- [ ] Test création event (POST /api/analytics/track/event/)
- [ ] Test création heatmap (POST /api/analytics/track/heatmap/)
- [ ] Test batch tracking (POST /api/analytics/track/batch/)
- [ ] Test permissions admin (GET endpoints)
- [ ] Test dashboard view (GET /api/analytics/dashboard/)
- [ ] Test heatmap view (GET /api/analytics/heatmap/)

**Exemple de test:**
```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class AnalyticsTrackingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_session(self):
        url = reverse('analytics:tracking-session')
        data = {
            'session_id': 'test_session_123',
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0...',
            'device_type': 'desktop',
            'browser': 'chrome'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

**Commande:**
```bash
python manage.py test apps.analytics.tests.test_views
```

#### 1.2 Tests Analytics Serializers

**Fichier à créer:** `backend/apps/analytics/tests/test_serializers.py`

```bash
touch apps/analytics/tests/test_serializers.py
```

**Tests à implémenter:**
- [ ] UserSessionSerializer validation
- [ ] PageViewSerializer validation
- [ ] EventSerializer validation
- [ ] HeatmapDataSerializer validation
- [ ] AnalyticsBatchSerializer validation
- [ ] Nested relationships
- [ ] Required fields
- [ ] Invalid data handling

#### 1.3 Tests Analytics Tasks

**Fichier à créer:** `backend/apps/analytics/tests/test_tasks.py`

```bash
touch apps/analytics/tests/test_tasks.py
```

**Tests à implémenter:**
- [ ] Test aggregate_daily_analytics (vérifier calculs)
- [ ] Test cleanup_old_heatmap_data (suppression)
- [ ] Test aggregate_all_missing_days
- [ ] Test generate_analytics_report
- [ ] Test retry logic
- [ ] Test avec Celery eager mode

**Configuration test Celery:**
```python
# Dans test_tasks.py
from django.test import override_settings

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class AnalyticsTasksTestCase(TestCase):
    def test_aggregate_daily_analytics(self):
        # Créer des sessions/pageviews
        # Exécuter la tâche
        # Vérifier DailyAnalytics créé
        # Vérifier calculs corrects
        pass
```

#### 1.4 Tests CRM Tasks

**Fichier à créer:** `backend/apps/crm/tests/test_tasks.py`

```bash
touch apps/crm/tests/test_tasks.py
```

**Tests à implémenter:**
- [ ] Test send_lead_notification_email (mock SMTP)
- [ ] Test send_lead_status_change_email
- [ ] Test cleanup_old_leads
- [ ] Test retry logic emails
- [ ] Test template rendering

#### 1.5 Coverage Report

**Commandes:**
```bash
cd backend

# Installer coverage si pas déjà fait
pip install coverage

# Exécuter tests avec coverage
coverage run --source='apps' manage.py test

# Générer rapport console
coverage report

# Générer rapport HTML détaillé
coverage html

# Ouvrir rapport HTML
start htmlcov/index.html  # Windows
```

**Critère d'acceptation:** Coverage >80% pour apps/analytics et apps/crm

### Étape 2: Tests Frontend (2-3 jours)

#### 2.1 Setup Testing Framework

**Installer dépendances:**
```bash
cd frontend
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitejs/plugin-react
```

**Créer fichier config:** `vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './')
    }
  }
})
```

**Créer setup:** `vitest.setup.ts`

```typescript
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock Next.js
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    pathname: '/',
  }),
}))
```

**Ajouter scripts dans package.json:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

#### 2.2 Tests UI Components

**Créer:** `components/ui/__tests__/Button.test.tsx`

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import Button from '../Button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('applies variant classes', () => {
    render(<Button variant="primary">Primary</Button>)
    const button = screen.getByText('Primary')
    expect(button).toHaveClass('bg-primary-500')
  })
})
```

**Tests à créer:**
- [ ] `components/ui/__tests__/Button.test.tsx`
- [ ] `components/ui/__tests__/Card.test.tsx`
- [ ] `components/ui/__tests__/Input.test.tsx`

#### 2.3 Tests Sections

**Créer:** `components/sections/__tests__/Hero.test.tsx`

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Hero from '../Hero'

const queryClient = new QueryClient()

describe('Hero Section', () => {
  it('renders loading state', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <Hero />
      </QueryClientProvider>
    )
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('displays hero content after load', async () => {
    // Mock API response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          title: 'Test Hero',
          subtitle: 'Test Subtitle'
        })
      })
    )

    render(
      <QueryClientProvider client={queryClient}>
        <Hero />
      </QueryClientProvider>
    )

    await waitFor(() => {
      expect(screen.getByText('Test Hero')).toBeInTheDocument()
    })
  })
})
```

**Tests sections à créer:**
- [ ] `components/sections/__tests__/Hero.test.tsx`
- [ ] `components/sections/__tests__/Services.test.tsx`
- [ ] `components/sections/__tests__/About.test.tsx`
- [ ] `components/sections/__tests__/Team.test.tsx`
- [ ] `components/sections/__tests__/FAQ.test.tsx`
- [ ] `components/sections/__tests__/Contact.test.tsx`

#### 2.4 Test Formulaire Contact (Validation Zod)

**Créer:** `components/sections/__tests__/Contact.validation.test.tsx`

```typescript
import { z } from 'zod'
import { contactSchema } from '../Contact'

describe('Contact Form Validation', () => {
  it('validates correct data', () => {
    const validData = {
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+33612345678',
      company: 'Acme Corp',
      need_type: 'optimization',
      message: 'This is a valid message with more than 20 characters'
    }
    expect(() => contactSchema.parse(validData)).not.toThrow()
  })

  it('rejects invalid email', () => {
    const invalidData = { ...validData, email: 'not-an-email' }
    expect(() => contactSchema.parse(invalidData)).toThrow()
  })

  it('rejects short message', () => {
    const invalidData = { ...validData, message: 'Too short' }
    expect(() => contactSchema.parse(invalidData)).toThrow()
  })
})
```

#### 2.5 Tests E2E (Playwright) - Optionnel

**Installer Playwright:**
```bash
npm init playwright@latest
```

**Exemple test E2E:** `tests/e2e/navigation.spec.ts`

```typescript
import { test, expect } from '@playwright/test'

test('navigation complète', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // Vérifier Hero visible
  await expect(page.locator('h1')).toBeVisible()

  // Cliquer sur Services dans le menu
  await page.click('a[href="#services"]')
  await expect(page.locator('#services')).toBeVisible()

  // Remplir formulaire contact
  await page.fill('input[name="name"]', 'Test User')
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('textarea[name="message"]', 'Test message for E2E testing')
  await page.click('button[type="submit"]')

  // Vérifier succès
  await expect(page.locator('text=Envoyé avec succès')).toBeVisible()
})
```

**Tests E2E à créer:**
- [ ] `tests/e2e/navigation.spec.ts`
- [ ] `tests/e2e/contact-form.spec.ts`
- [ ] `tests/e2e/responsive.spec.ts`

#### 2.6 Coverage Frontend

**Commande:**
```bash
npm run test:coverage
```

**Critère d'acceptation:** Coverage >70% pour composants critiques (Hero, Contact, API client)

### Checklist Phase 8

- [ ] Tests analytics views complétés
- [ ] Tests analytics serializers complétés
- [ ] Tests analytics tasks complétés
- [ ] Tests CRM tasks complétés
- [ ] Coverage backend >80%
- [ ] Vitest configuré frontend
- [ ] Tests UI components (Button, Card, Input)
- [ ] Tests sections (Hero, Services, About, Team, FAQ, Contact)
- [ ] Tests formulaire Contact validation
- [ ] Coverage frontend >70%
- [ ] (Optionnel) Playwright E2E configuré
- [ ] Tous les tests passent en CI

---

## 📈 PHASE 9: SEO & PERFORMANCE

**Durée estimée:** 2-3 jours
**Priorité:** 🟡 MOYENNE

### Objectif

Optimiser le **référencement naturel (SEO)** et les **performances** pour atteindre un score Lighthouse >90.

### Étape 1: SEO (1 jour)

#### 1.1 Sitemap.xml Dynamique

**Créer:** `frontend/app/sitemap.ts`

```typescript
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://pinnacle-advisors.tech'

  // Pages statiques
  const routes = ['', '/card'].map(route => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date().toISOString(),
    changeFrequency: 'weekly' as const,
    priority: route === '' ? 1 : 0.8,
  }))

  // Ajouter pages dynamiques si besoin (blog, etc.)

  return routes
}
```

**Vérifier:** `http://localhost:3000/sitemap.xml`

#### 1.2 Robots.txt

**Créer:** `frontend/app/robots.ts`

```typescript
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/api/', '/admin/'],
    },
    sitemap: 'https://pinnacle-advisors.tech/sitemap.xml',
  }
}
```

**Vérifier:** `http://localhost:3000/robots.txt`

#### 1.3 Structured Data (JSON-LD)

**Créer:** `components/StructuredData.tsx`

```typescript
export default function StructuredData() {
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Pinnacle Advisors',
    url: 'https://pinnacle-advisors.tech',
    logo: 'https://pinnacle-advisors.tech/logo.png',
    description: 'Cabinet de conseil expert en supply chain',
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'FR'
    },
    sameAs: [
      'https://linkedin.com/company/pinnacle-advisors',
      'https://twitter.com/pinnacleadvisors'
    ]
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
    />
  )
}
```

**Intégrer dans:** `app/layout.tsx`

#### 1.4 Alt Text Images

**Vérifier dans tous les composants:**
```tsx
<Image src="/team/expert.jpg" alt="Jean Dupont, Expert Supply Chain" />
```

**Commande grep:**
```bash
cd frontend
grep -r "<Image" --include="*.tsx" | grep -v "alt="
```

**Corriger:** Ajouter alt text descriptif partout

#### 1.5 Google Search Console

**Étapes:**
1. Aller sur [search.google.com/search-console](https://search.google.com/search-console)
2. Ajouter propriété (domain: pinnacle-advisors.tech)
3. Vérifier ownership (DNS TXT record)
4. Soumettre sitemap.xml
5. Demander indexation page d'accueil

### Étape 2: Performance (1-2 jours)

#### 2.1 Lighthouse Audit Baseline

**Commande:**
```bash
cd frontend
npm run build
npm start  # Port 3000

# Dans Chrome DevTools
# Lighthouse → Generate report
```

**Critères:**
- Performance: >90
- Accessibility: >95
- Best Practices: >95
- SEO: >95

**Prendre screenshot du rapport initial**

#### 2.2 Optimisations Frontend

**Bundle Size Analysis:**
```bash
npm install --save-dev @next/bundle-analyzer
```

**Configurer:** `next.config.ts`

```typescript
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // ... config existante
})
```

**Analyser:**
```bash
ANALYZE=true npm run build
```

**Optimisations possibles:**
- [ ] Lazy load sections (dynamic import)
- [ ] Code splitting Framer Motion
- [ ] Tree-shaking libraries inutilisées
- [ ] Compression images (WebP, AVIF)

**Lazy loading exemple:**
```typescript
import dynamic from 'next/dynamic'

const FAQ = dynamic(() => import('@/components/sections/FAQ'), {
  loading: () => <div>Loading FAQ...</div>,
  ssr: false
})
```

#### 2.3 Optimisations Backend

**Database Indexing:**

```bash
cd backend
python manage.py dbshell
```

```sql
-- Vérifier indexes existants
SELECT * FROM sqlite_master WHERE type='index';

-- Créer indexes manquants (exemple)
CREATE INDEX idx_lead_qualification ON crm_lead(qualification);
CREATE INDEX idx_lead_status ON crm_lead(status);
CREATE INDEX idx_session_created ON analytics_usersession(start_time);
```

**OU créer migration Django:**

```bash
python manage.py makemigrations --empty crm -n add_indexes
```

**Éditer migration:**

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='lead',
            index=models.Index(fields=['qualification'], name='idx_lead_qual'),
        ),
        migrations.AddIndex(
            model_name='lead',
            index=models.Index(fields=['status'], name='idx_lead_status'),
        ),
    ]
```

**Query Optimization:**

Éditer `apps/crm/views.py`:

```python
class LeadViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Lead.objects.select_related(
            'pipeline', 'assigned_to'
        ).prefetch_related(
            'interactions', 'notes'
        )
```

#### 2.4 Redis Cache

**Installer Redis (Windows avec Docker):**

```bash
docker run --name redis -d -p 6379:6379 redis:latest
```

**OU installer Redis Stack:**
[Download Redis](https://redis.io/download)

**Vérifier:**
```bash
redis-cli ping
# PONG
```

**Démarrer Celery:**

Terminal 1:
```bash
cd backend
.\venv\Scripts\python.exe -m celery -A config worker -l info
```

Terminal 2:
```bash
cd backend
.\venv\Scripts\python.exe -m celery -A config beat -l info
```

**Configurer cache Django:**

`backend/config/settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Utiliser cache dans views:**

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 5), name='dispatch')  # 5min cache
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    ...
```

### Checklist Phase 9

- [ ] sitemap.xml dynamique créé
- [ ] robots.txt configuré
- [ ] Structured data JSON-LD ajouté
- [ ] Alt text images vérifié
- [ ] Google Search Console configuré
- [ ] Lighthouse audit baseline effectué
- [ ] Bundle size analysé
- [ ] Optimisations frontend appliquées
- [ ] Database indexes créés
- [ ] Query optimization (select_related/prefetch_related)
- [ ] Redis installé et démarré
- [ ] Celery workers + beat démarrés
- [ ] Cache Django configuré
- [ ] Lighthouse score final >90

---

## 🚢 PHASE 10: DÉPLOIEMENT PRODUCTION

**Durée estimée:** 5-7 jours
**Priorité:** 🔴 CRITIQUE (mise en production)

### Objectif

Déployer le projet en **production** sur AWS (backend) et Vercel (frontend) avec toutes les sécurités et monitoring.

### Prérequis

- [ ] Compte AWS créé
- [ ] Carte bancaire validée (AWS)
- [ ] Nom de domaine acheté (ex: pinnacle-advisors.tech)
- [ ] Compte Vercel créé (gratuit)
- [ ] Compte GitHub (repo public ou private)

### Étape 1: Préparer le Code (1 jour)

#### 1.1 Sécurité Production

**Créer:** `backend/.env.production`

```bash
# IMPORTANT: Ne JAMAIS committer ce fichier
# Ajouter à .gitignore

SECRET_KEY=<générer_nouveau_secret_key>
DEBUG=False
ALLOWED_HOSTS=pinnacle-advisors.tech,www.pinnacle-advisors.tech,api.pinnacle-advisors.tech
DATABASE_URL=postgresql://user:password@db-host:5432/pinnacle_db
CELERY_BROKER_URL=redis://redis-host:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contact@pinnacle-advisors.tech
EMAIL_HOST_PASSWORD=<app_password>
AWS_ACCESS_KEY_ID=<aws_key>
AWS_SECRET_ACCESS_KEY=<aws_secret>
AWS_STORAGE_BUCKET_NAME=pinnacle-media
AWS_S3_REGION_NAME=eu-west-3
SENTRY_DSN=<sentry_dsn>
```

**Générer SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 1.2 Settings Production

**Créer:** `backend/config/settings_production.py`

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://pinnacle-advisors.tech',
    'https://www.pinnacle-advisors.tech',
]

# Static/Media files (S3)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='eu-west-3')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Database (PostgreSQL)
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/pinnacle/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

#### 1.3 Requirements Production

**Ajouter dans:** `backend/requirements.txt`

```txt
django-storages==1.14.4
boto3==1.35.95
sentry-sdk==2.19.4
```

**Installer:**
```bash
cd backend
.\venv\Scripts\pip.exe install django-storages boto3 sentry-sdk
pip freeze > requirements.txt
```

### Étape 2: AWS Setup (2 jours)

#### 2.1 EC2 Instance

**Console AWS → EC2 → Launch Instance:**

1. **Nom:** pinnacle-production
2. **AMI:** Ubuntu Server 22.04 LTS
3. **Instance type:** t3.small (2 vCPU, 2 GB RAM) - ~$15/mois
4. **Key pair:** Créer nouvelle (pinnacle-key.pem) - TÉLÉCHARGER
5. **Network:**
   - VPC: default
   - Subnet: default
   - Auto-assign public IP: Yes
6. **Security Group:** pinnacle-sg
   - SSH (22): Your IP only
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
7. **Storage:** 20 GB gp3
8. **Launch**

**Elastic IP:**
- EC2 → Elastic IPs → Allocate
- Associate avec instance
- Noter l'IP: `XX.XX.XX.XX`

#### 2.2 RDS PostgreSQL

**Console AWS → RDS → Create database:**

1. **Engine:** PostgreSQL 15.x
2. **Template:** Free tier OU Production
3. **DB instance identifier:** pinnacle-db
4. **Master username:** pinnacle_admin
5. **Master password:** <strong_password>
6. **Instance class:** db.t3.micro (Free tier) OU db.t3.small
7. **Storage:** 20 GB gp3, autoscaling max 100 GB
8. **VPC:** default (même que EC2)
9. **Public access:** No
10. **Security group:** pinnacle-db-sg
    - PostgreSQL (5432): Source = pinnacle-sg (EC2 security group)
11. **Initial database name:** pinnacle_production
12. **Automated backups:** 7 days retention
13. **Create**

**Noter endpoint:** `pinnacle-db.xxxx.eu-west-3.rds.amazonaws.com`

#### 2.3 ElastiCache Redis

**Console AWS → ElastiCache → Create cluster:**

1. **Engine:** Redis
2. **Cluster mode:** Disabled
3. **Name:** pinnacle-redis
4. **Node type:** cache.t3.micro (Free tier eligible)
5. **Number of replicas:** 0 (dev) OU 1 (prod)
6. **VPC:** default
7. **Subnet:** Redis subnet group (auto)
8. **Security group:** pinnacle-redis-sg
   - Redis (6379): Source = pinnacle-sg
9. **Create**

**Noter endpoint:** `pinnacle-redis.xxxx.0001.euw3.cache.amazonaws.com:6379`

#### 2.4 S3 Buckets

**Console AWS → S3 → Create bucket:**

**Bucket 1: Media files**
1. **Name:** pinnacle-media-prod (unique globalement)
2. **Region:** eu-west-3 (Paris)
3. **ACLs:** Disabled
4. **Block public access:** OFF (décocher tout)
5. **Versioning:** Enabled
6. **Encryption:** SSE-S3
7. **Create**

**Bucket 2: Static files**
1. **Name:** pinnacle-static-prod
2. **Settings:** Identiques

**Bucket Policy (pinnacle-media-prod):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::pinnacle-media-prod/*"
    }
  ]
}
```

**CORS Configuration:**

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "POST", "PUT"],
    "AllowedOrigins": ["https://pinnacle-advisors.tech"],
    "ExposeHeaders": []
  }
]
```

#### 2.5 IAM User

**Console AWS → IAM → Users → Create user:**

1. **Name:** pinnacle-django
2. **Access type:** Programmatic access
3. **Permissions:** Attach existing policies
   - AmazonS3FullAccess
4. **Create**
5. **TÉLÉCHARGER credentials.csv**
   - Access Key ID: AKIAXXXXXXX
   - Secret Access Key: XXXXXXX

### Étape 3: Serveur EC2 Setup (1 jour)

#### 3.1 Connexion SSH

**Windows (PowerShell):**

```powershell
# Donner permissions à la clé
icacls "pinnacle-key.pem" /inheritance:r
icacls "pinnacle-key.pem" /grant:r "%username%:R"

# Se connecter
ssh -i "pinnacle-key.pem" ubuntu@XX.XX.XX.XX
```

**Linux/Mac:**

```bash
chmod 400 pinnacle-key.pem
ssh -i pinnacle-key.pem ubuntu@XX.XX.XX.XX
```

#### 3.2 Installation Dépendances

```bash
# Update système
sudo apt update && sudo apt upgrade -y

# Python
sudo apt install -y python3.11 python3.11-venv python3-pip

# PostgreSQL client
sudo apt install -y postgresql-client

# Nginx
sudo apt install -y nginx

# Supervisor (pour Celery)
sudo apt install -y supervisor

# Git
sudo apt install -y git

# Autres outils
sudo apt install -y htop vim curl
```

#### 3.3 Déployer Code

```bash
# Créer utilisateur
sudo adduser --disabled-password --gecos "" pinnacle
sudo su - pinnacle

# Cloner repo (si GitHub private, configurer SSH key)
git clone https://github.com/your-org/pinnacle-website.git
cd pinnacle-website/backend

# Créer venv
python3.11 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Créer .env (copier depuis .env.production local)
nano .env

# Collectstatic (vers S3)
python manage.py collectstatic --noinput

# Migrer DB
python manage.py migrate

# Créer superuser
python manage.py createsuperuser
```

#### 3.4 Gunicorn Setup

**Créer:** `/home/pinnacle/pinnacle-website/backend/gunicorn_config.py`

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
loglevel = "info"
errorlog = "/var/log/pinnacle/gunicorn-error.log"
accesslog = "/var/log/pinnacle/gunicorn-access.log"
```

**Créer logs dir:**

```bash
sudo mkdir /var/log/pinnacle
sudo chown pinnacle:pinnacle /var/log/pinnacle
```

**Systemd service:** `/etc/systemd/system/gunicorn.service`

```ini
[Unit]
Description=Gunicorn daemon for Pinnacle Advisors
After=network.target

[Service]
User=pinnacle
Group=pinnacle
WorkingDirectory=/home/pinnacle/pinnacle-website/backend
Environment="PATH=/home/pinnacle/pinnacle-website/backend/venv/bin"
ExecStart=/home/pinnacle/pinnacle-website/backend/venv/bin/gunicorn \
          --config gunicorn_config.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Démarrer:**

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

#### 3.5 Nginx Setup

**Créer:** `/etc/nginx/sites-available/pinnacle`

```nginx
upstream pinnacle_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name pinnacle-advisors.tech www.pinnacle-advisors.tech;

    # Redirect HTTP → HTTPS (après SSL setup)
    # return 301 https://$host$request_uri;

    # Temporaire pour obtenir certificat Let's Encrypt
    location / {
        proxy_pass http://pinnacle_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        # Rediriger vers S3 OU servir localement si pas S3
        return 301 https://pinnacle-static-prod.s3.amazonaws.com$request_uri;
    }

    location /media/ {
        return 301 https://pinnacle-media-prod.s3.amazonaws.com$request_uri;
    }
}
```

**Activer:**

```bash
sudo ln -s /etc/nginx/sites-available/pinnacle /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 3.6 SSL Let's Encrypt

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir certificat
sudo certbot --nginx -d pinnacle-advisors.tech -d www.pinnacle-advisors.tech

# Renouvellement auto
sudo systemctl enable certbot.timer
```

**Certbot modifiera automatiquement Nginx config pour HTTPS**

#### 3.7 Celery Supervisor

**Créer:** `/etc/supervisor/conf.d/celery.conf`

```ini
[program:celery-worker]
command=/home/pinnacle/pinnacle-website/backend/venv/bin/celery -A config worker -l info
directory=/home/pinnacle/pinnacle-website/backend
user=pinnacle
autostart=true
autorestart=true
stdout_logfile=/var/log/pinnacle/celery-worker.log
stderr_logfile=/var/log/pinnacle/celery-worker-error.log

[program:celery-beat]
command=/home/pinnacle/pinnacle-website/backend/venv/bin/celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
directory=/home/pinnacle/pinnacle-website/backend
user=pinnacle
autostart=true
autorestart=true
stdout_logfile=/var/log/pinnacle/celery-beat.log
stderr_logfile=/var/log/pinnacle/celery-beat-error.log
```

**Démarrer:**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```

### Étape 4: Frontend Vercel (0.5 jour)

#### 4.1 Préparer Frontend

**Créer:** `frontend/.env.production`

```bash
NEXT_PUBLIC_API_URL=https://api.pinnacle-advisors.tech
```

**Update:** `next.config.ts`

```typescript
{
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'pinnacle-media-prod.s3.amazonaws.com',
        pathname: '/media/**'
      }
    ]
  }
}
```

#### 4.2 Déployer sur Vercel

**Option A: Via Dashboard**

1. Aller sur [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Import Git Repository
4. Choisir `pinnacle-website` repo
5. Root Directory: `frontend`
6. Framework Preset: Next.js (auto-détecté)
7. Environment Variables:
   - `NEXT_PUBLIC_API_URL` = `https://api.pinnacle-advisors.tech`
8. Deploy

**Option B: Via CLI**

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**Custom Domain:**

1. Vercel Dashboard → Project → Settings → Domains
2. Add: `pinnacle-advisors.tech`
3. Add: `www.pinnacle-advisors.tech`
4. Configurer DNS (voir étape suivante)

### Étape 5: DNS Configuration (0.5 jour)

**Chez votre registrar (OVH, Namecheap, etc.):**

**A Records (Backend API):**
```
Type: A
Name: api
Value: XX.XX.XX.XX (Elastic IP EC2)
TTL: 300
```

**CNAME Records (Frontend Vercel):**
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 300

Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 300
```

**Vérifier propagation:**
```bash
nslookup pinnacle-advisors.tech
nslookup api.pinnacle-advisors.tech
```

### Étape 6: Monitoring & Logs (1 jour)

#### 6.1 Sentry Setup

1. Créer compte sur [sentry.io](https://sentry.io)
2. Créer projet Django
3. Copier DSN
4. Ajouter dans .env production

**Tester Sentry:**

```python
# Dans Django shell
from sentry_sdk import capture_exception

try:
    1 / 0
except Exception as e:
    capture_exception(e)
```

**Vérifier erreur dans Sentry Dashboard**

#### 6.2 Uptime Monitoring

**UptimeRobot (gratuit):**

1. [uptimerobot.com](https://uptimerobot.com)
2. Add New Monitor
3. Type: HTTPS
4. URL: `https://pinnacle-advisors.tech`
5. Interval: 5 minutes
6. Alert Contacts: Email
7. Create

**Ajouter monitors:**
- https://pinnacle-advisors.tech
- https://api.pinnacle-advisors.tech/api/health/

#### 6.3 AWS CloudWatch

**EC2 → Monitoring → Enable detailed monitoring**

**Créer alarm:**

1. CloudWatch → Alarms → Create alarm
2. Metric: EC2 → Per-Instance Metrics → CPUUtilization
3. Conditions: >80% for 2 periods
4. Actions: SNS topic → Email notification
5. Create

### Checklist Phase 10

**Pré-déploiement:**
- [ ] .env.production créé (backend + frontend)
- [ ] SECRET_KEY nouveau généré
- [ ] settings_production.py créé
- [ ] django-storages installé
- [ ] Code committé sur GitHub

**AWS:**
- [ ] EC2 instance créée et accessible SSH
- [ ] RDS PostgreSQL créée
- [ ] ElastiCache Redis créé
- [ ] S3 buckets créés (media + static)
- [ ] IAM user créé avec credentials
- [ ] Elastic IP associée

**Backend:**
- [ ] Code déployé sur EC2
- [ ] Dépendances installées (venv)
- [ ] Database migrée
- [ ] Superuser créé
- [ ] Gunicorn configuré et démarré
- [ ] Nginx configuré
- [ ] SSL Let's Encrypt installé
- [ ] Celery workers + beat démarrés (Supervisor)

**Frontend:**
- [ ] Déployé sur Vercel
- [ ] Custom domain configuré
- [ ] Environment variables ajoutées

**DNS:**
- [ ] A record (api.pinnacle-advisors.tech)
- [ ] CNAME records (pinnacle-advisors.tech, www)
- [ ] DNS propagation vérifiée

**Monitoring:**
- [ ] Sentry configuré et testé
- [ ] UptimeRobot monitors créés
- [ ] CloudWatch alarms configurées
- [ ] Backup automatique RDS actif

**Tests Production:**
- [ ] https://pinnacle-advisors.tech accessible
- [ ] https://api.pinnacle-advisors.tech/api/ fonctionne
- [ ] https://api.pinnacle-advisors.tech/admin/ accessible
- [ ] Formulaire contact envoie email
- [ ] Analytics trackent
- [ ] Images S3 chargent
- [ ] Celery tasks s'exécutent

---

## 🎉 PHASE 11: POST-LANCEMENT

**Durée estimée:** Continu (5-7 jours setup initial)
**Priorité:** 🟢 BASSE (amélioration continue)

### Objectif

Monitoring continu, optimisations basées sur données réelles, et ajout de features avancées.

### Étape 1: Launch Checklist (Jour 1)

#### 1.1 Vérifications Finales

**Backend:**
- [ ] `python manage.py check --deploy` → 0 issues
- [ ] Tests production (`python manage.py test`)
- [ ] Tous les endpoints API répondent
- [ ] Admin production accessible
- [ ] Emails production envoyés (tester formulaire)
- [ ] Celery tasks s'exécutent (vérifier logs)
- [ ] Backups DB fonctionnent
- [ ] Logs collectés (CloudWatch, Sentry)

**Frontend:**
- [ ] Toutes les pages chargent
- [ ] Formulaires valident
- [ ] Analytics trackent (vérifier Django admin)
- [ ] Images chargent depuis S3
- [ ] Responsive mobile/tablet/desktop
- [ ] Navigation smooth scroll fonctionne
- [ ] SEO metadata présent (view-source)

**Infrastructure:**
- [ ] DNS propagé (24-48h)
- [ ] SSL actif partout (HTTPS)
- [ ] Monitoring actif (Sentry, UptimeRobot)
- [ ] Firewall EC2 configuré
- [ ] Fail2ban protège SSH

#### 1.2 Tests Utilisateur

**Créer checklist:**
- [ ] Parcourir site complet (mobile + desktop)
- [ ] Remplir formulaire contact → Vérifier email reçu + Lead créé
- [ ] Tester tous les liens
- [ ] Vérifier Analytics dans God View Dashboard
- [ ] Tester vitesse chargement (Lighthouse)
- [ ] Vérifier SEO (Google Search Console)

**Inviter beta testers:**
- [ ] Collègues/amis testent le site
- [ ] Noter bugs/feedback
- [ ] Créer GitHub Issues
- [ ] Prioriser fixes

### Étape 2: Monitoring & Analytics (Continu)

#### 2.1 Métriques à Suivre (Hebdomadaire)

**Business:**
- Nombre de soumissions formulaire
- Qualification leads (Hot/Warm/Cold ratio)
- Taux conversion visiteur → lead
- Pages populaires (God View)
- Sources trafic (UTM)

**Technique:**
- Uptime (>99.9%)
- Response time API (<200ms)
- Erreurs Sentry (0 idéal)
- Taille base de données
- Coûts AWS (budget alert)

**SEO:**
- Impressions Google Search Console
- Clics organiques
- Position moyenne
- Pages indexées

#### 2.2 Rapports Automatiques

**Créer script:** `backend/scripts/weekly_report.py`

```python
from apps.crm.models import Lead
from apps.analytics.models import DailyAnalytics
from django.utils import timezone
from datetime import timedelta

def generate_weekly_report():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    # Leads créés
    leads_count = Lead.objects.filter(
        created_at__date__gte=start_date
    ).count()

    hot_leads = Lead.objects.filter(
        qualification='hot',
        created_at__date__gte=start_date
    ).count()

    # Analytics
    analytics = DailyAnalytics.objects.filter(
        date__gte=start_date
    ).aggregate(
        total_sessions=Sum('total_sessions'),
        total_visitors=Sum('unique_visitors'),
        avg_duration=Avg('avg_session_duration')
    )

    # Email rapport
    subject = f"Rapport Hebdomadaire Pinnacle {start_date} - {end_date}"
    message = f"""
    Leads: {leads_count} ({hot_leads} hot)
    Sessions: {analytics['total_sessions']}
    Visiteurs uniques: {analytics['total_visitors']}
    Durée moyenne: {analytics['avg_duration']:.2f}min
    """

    send_mail(subject, message, 'report@pinnacle-advisors.tech', ['admin@pinnacle-advisors.tech'])
```

**Tâche Celery hebdomadaire:**

```python
# backend/apps/core/tasks.py
from celery import shared_task
from celery.schedules import crontab

@shared_task
def send_weekly_report():
    from scripts.weekly_report import generate_weekly_report
    generate_weekly_report()

# backend/config/settings.py
CELERY_BEAT_SCHEDULE = {
    # ... existing
    'weekly-report': {
        'task': 'core.send_weekly_report',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Lundi 9h
    }
}
```

### Étape 3: Optimisations Basées sur Données (Semaines 1-4)

#### 3.1 Analyse Heatmap

**Django Admin → Analytics → Heatmap:**

1. Identifier zones les plus cliquées
2. Vérifier si CTAs sont cliqués
3. Détecter zones mortes (jamais cliquées)
4. Ajuster design/placement boutons

**Actions possibles:**
- Déplacer CTA principal si peu cliqué
- Agrandir boutons petits
- Supprimer sections ignorées
- A/B test placements

#### 3.2 Analyse Formulaire

**Metrics:**
- Taux abandon formulaire
- Champs avec erreurs fréquentes
- Temps moyen remplissage

**Optimisations:**
- Simplifier formulaire (retirer champs optionnels)
- Améliorer messages erreur
- Ajouter auto-complete
- Tester formulaire en 1 étape vs multi-step

#### 3.3 Performance Réelle

**Google Search Console → Core Web Vitals:**

- LCP (Largest Contentful Paint): <2.5s
- FID (First Input Delay): <100ms
- CLS (Cumulative Layout Shift): <0.1

**Si mauvais scores:**
- Optimiser images (WebP, lazy loading)
- Réduire bundle JS
- Preload fonts
- Minify CSS

### Étape 4: Features Avancées (Mois 2-3)

#### 4.1 Blog Section (Optionnel)

**Backend - Nouveau modèle:**

```python
# apps/website/models.py
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']
```

**Frontend - Nouvelle page:**

```bash
cd frontend
mkdir app/blog
touch app/blog/page.tsx
touch app/blog/[slug]/page.tsx
```

#### 4.2 Newsletter (Optionnel)

**Utiliser Mailchimp/SendGrid:**

1. Créer compte Mailchimp
2. Créer audience
3. Obtenir API key
4. Ajouter formulaire newsletter (Footer)
5. POST vers Mailchimp API

#### 4.3 Multi-langue (Optionnel)

**Backend:**

```bash
pip install django-modeltranslation
```

**Frontend:**

```bash
npm install next-intl
```

**Langues:** Français (défaut) + Anglais

#### 4.4 Dark Mode (Optionnel)

**Frontend - Context + Tailwind:**

```typescript
// context/ThemeContext.tsx
const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

**Tailwind config:**

```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // ... existing
      }
    }
  }
}
```

### Étape 5: Maintenance Continue (Mensuel)

#### 5.1 Updates Sécurité

**Chaque mois:**

```bash
# Backend
cd backend
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt

# Frontend
cd frontend
npm outdated
npm update
npm audit fix
```

**Vérifier breaking changes avant update majeurs (Django, Next.js)**

#### 5.2 Database Maintenance

**Mensuel:**

```bash
# Se connecter à RDS
psql -h pinnacle-db.xxx.rds.amazonaws.com -U pinnacle_admin -d pinnacle_production

# Vacuum
VACUUM ANALYZE;

# Reindex
REINDEX DATABASE pinnacle_production;

# Vérifier taille
SELECT pg_size_pretty(pg_database_size('pinnacle_production'));
```

#### 5.3 Backups Verification

**Tester restore backup:**

```bash
# Créer DB test
createdb pinnacle_test

# Restore dernier backup RDS
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier pinnacle-test \
  --db-snapshot-identifier rds:pinnacle-db-2025-11-03

# Vérifier données
psql -h pinnacle-test.xxx.rds.amazonaws.com -U pinnacle_admin -d pinnacle_test
SELECT COUNT(*) FROM website_service;
```

#### 5.4 Logs Review

**Hebdomadaire:**

1. Sentry → Review errors (viser 0 unresolved)
2. CloudWatch → EC2 logs (errors, warnings)
3. Nginx access logs → Trafic inhabituel
4. Celery logs → Tasks failures

### Checklist Phase 11

**Launch:**
- [ ] Checklist pré-production complétée
- [ ] Beta testers invités
- [ ] Bugs critiques fixés
- [ ] Site annoncé (LinkedIn, email, etc.)

**Monitoring:**
- [ ] Dashboard métriques business créé
- [ ] Rapports hebdomadaires automatisés
- [ ] Alerts configurées (uptime, errors, performance)

**Optimisations:**
- [ ] Heatmap analysée
- [ ] Formulaire optimisé
- [ ] Core Web Vitals >90 (Lighthouse)
- [ ] SEO ranking tracking

**Features Avancées (Optionnel):**
- [ ] Blog section
- [ ] Newsletter integration
- [ ] Multi-langue
- [ ] Dark mode

**Maintenance:**
- [ ] Updates mensuels programmés (calendrier)
- [ ] Database maintenance automatisée
- [ ] Backup restore testé
- [ ] Logs reviewés hebdomadairement

---

## 📊 RÉCAPITULATIF GLOBAL

### Timeline Complète

| Phase | Durée | Début | Fin |
|-------|-------|-------|-----|
| Phase 8: Tests | 3-5 jours | Jour 1 | Jour 5 |
| Phase 9: SEO/Perf | 2-3 jours | Jour 6 | Jour 8 |
| Phase 10: Déploiement | 5-7 jours | Jour 9 | Jour 15 |
| Phase 11: Post-Launch | Continu | Jour 16 | ∞ |

**Total avant production:** 10-15 jours
**Total avec post-launch initial:** 15-22 jours

### Budget Estimé (Mensuel)

**AWS:**
- EC2 t3.small: $15/mois
- RDS db.t3.small: $25/mois
- ElastiCache cache.t3.micro: $12/mois
- S3 + transfert: $5/mois
- **Total AWS:** ~$57/mois

**Services:**
- Domaine (.tech): $30/an = $2.5/mois
- Vercel: $0 (hobby) OU $20/mois (pro)
- Sentry: $0 (developer plan, 5k errors/mois)
- UptimeRobot: $0 (50 monitors)
- **Total Services:** $2.5-22.5/mois

**TOTAL MENSUEL:** $60-80/mois

**Alternatives économiques:**
- DigitalOcean Droplet: $12/mois (remplace EC2 + RDS + Redis)
- Netlify (au lieu de Vercel): $0
- Heroku: $25-50/mois (tout-en-un)

### Commandes Rapides de Référence

**Tests Backend:**
```bash
cd backend
python manage.py test
coverage run --source='apps' manage.py test && coverage report
```

**Tests Frontend:**
```bash
cd frontend
npm run test
npm run test:coverage
```

**Lighthouse Audit:**
```bash
cd frontend
npm run build && npm start
# Chrome DevTools → Lighthouse
```

**Déploiement:**
```bash
# Backend (depuis EC2)
cd ~/pinnacle-website/backend
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart supervisor

# Frontend (local)
cd frontend
git push origin main  # Auto-deploy Vercel
```

**Logs:**
```bash
# Gunicorn
sudo tail -f /var/log/pinnacle/gunicorn-error.log

# Celery
sudo tail -f /var/log/pinnacle/celery-worker.log

# Nginx
sudo tail -f /var/log/nginx/error.log
```

---

## ✅ CHECKLIST FINALE

Avant de considérer le projet 100% terminé:

### Phase 8: Tests
- [ ] Coverage backend >80%
- [ ] Coverage frontend >70%
- [ ] Tous tests passent
- [ ] CI configuré (GitHub Actions)

### Phase 9: SEO & Performance
- [ ] Lighthouse score >90 (tous critères)
- [ ] Sitemap.xml actif
- [ ] Robots.txt configuré
- [ ] Google Search Console configuré
- [ ] Redis cache actif

### Phase 10: Déploiement
- [ ] Site production accessible (HTTPS)
- [ ] API production fonctionne
- [ ] Base de données PostgreSQL migrée
- [ ] S3 media/static fonctionnent
- [ ] Celery workers actifs
- [ ] SSL Let's Encrypt installé
- [ ] Monitoring actif (Sentry, UptimeRobot)
- [ ] Backups automatiques testés

### Phase 11: Post-Launch
- [ ] Rapports hebdomadaires automatisés
- [ ] Metrics business suivies
- [ ] Optimisations basées sur données
- [ ] Plan maintenance défini
- [ ] Updates sécurité programmées

### Documentation
- [ ] README.md à jour
- [ ] PROJECT_STATUS.md complété
- [ ] Credentials documentées (coffre-fort)
- [ ] Runbook incidents créé
- [ ] Onboarding nouveaux devs documenté

---

**Dernière mise à jour:** 03 Novembre 2025
**Créé par:** Claude Code (Sonnet 4.5)
**Projet:** Pinnacle Advisors Website

**Bon courage pour les phases restantes! 🚀**
