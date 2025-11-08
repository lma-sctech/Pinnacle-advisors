# 🚀 Pinnacle Advisors - Roadmap Projet (64% → 100%)

**Dernière mise à jour** : 8 novembre 2025
**Statut actuel** : Phase 7/11 complétée (64%)
**Site en production** : https://pinnacle-advisors.tech

---

## 📊 Vue d'Ensemble

| Phase | Tâches | Durée estimée | Priorité | Statut |
|-------|--------|---------------|----------|--------|
| **Phase 8 - Tests Complets** | 12 | 2-3 jours | 🔴 Critique | ⏳ À faire |
| **Phase 9 - Performance & Sécurité** | 11 | 2-3 jours | 🔴 Critique | ⏳ À faire |
| **Phase 10 - Infrastructure & SEO** | 8 | 1-2 jours | 🟡 Importante | ⏳ À faire |
| **Phase 11 - Documentation & Post-Launch** | 7 | 1-2 jours | 🟢 Recommandée | ⏳ À faire |
| **TOTAL** | **38 tâches** | **6-10 jours** | - | **64% complet** |

---

## ✅ Phases Complétées (1-7)

### Phase 1-6 : Développement Initial ✅
- ✅ Backend Django complet (117 endpoints API)
- ✅ CRM avec auto-qualification des leads
- ✅ Analytics "God View" complet
- ✅ Frontend Next.js responsive et animé
- ✅ Déploiement Render + Vercel
- ✅ CI/CD GitHub Actions

### Phase 7 : Optimisation SEO ✅ (Complétée le 4 nov 2025)
- ✅ **Phase 7.1** : Fondations SEO (robots.txt, sitemap.xml, métadonnées)
- ✅ **Phase 7.2** : Métadonnées avancées (OpenGraph, Twitter Cards)
- ✅ **Phase 7.3** : Optimisation performance et images
- ✅ **Phase 7.4** : Structured Data (Organization, Service, FAQ, Person schemas)
- ✅ **Score SEO actuel** : 90/100

---

## 🎯 PHASE 8 : Tests Complets

**Objectif** : Atteindre 80%+ de couverture de code et garantir la stabilité
**Durée estimée** : 2-3 jours
**Priorité** : 🔴 CRITIQUE

### 8A - Configuration Suite Tests Frontend (3 tâches)

#### 🧪 Tâche 8.1 : Installer Vitest + React Testing Library + Playwright
**Description** : Configuration initiale de l'environnement de tests frontend

**Actions** :
- [ ] Installer Vitest, React Testing Library, jsdom
- [ ] Installer Playwright pour tests E2E
- [ ] Installer @testing-library/user-event
- [ ] Ajouter scripts de test dans package.json

**Commandes** :
```bash
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
npm install -D playwright @playwright/test
npx playwright install
```

**Fichiers modifiés** :
- `frontend/package.json`

---

#### 🧪 Tâche 8.2 : Configurer vitest.config.ts et setup de tests
**Description** : Configuration complète de Vitest et setup global

**Actions** :
- [ ] Créer `vitest.config.ts` avec configuration Next.js
- [ ] Créer `__tests__/setup.ts` pour setup global
- [ ] Créer `./__mocks__/` pour mocks API et Analytics
- [ ] Configurer coverage reporter (Istanbul)

**Fichiers à créer** :
- `frontend/vitest.config.ts`
- `frontend/__tests__/setup.ts`
- `frontend/__mocks__/api.ts`
- `frontend/__mocks__/analytics.ts`

**Configuration coverage** :
```typescript
coverage: {
  provider: 'istanbul',
  reporter: ['text', 'json', 'html'],
  exclude: ['node_modules/', '__tests__/', '*.config.ts']
}
```

---

#### 🧪 Tâche 8.3 : Créer structure de fichiers tests
**Description** : Organisation des répertoires de tests

**Actions** :
- [ ] Créer `frontend/__tests__/components/ui/`
- [ ] Créer `frontend/__tests__/components/sections/`
- [ ] Créer `frontend/__tests__/lib/`
- [ ] Créer `frontend/e2e/` pour Playwright
- [ ] Créer fichier `playwright.config.ts`

**Structure attendue** :
```
frontend/
├── __tests__/
│   ├── setup.ts
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.test.tsx
│   │   │   ├── Card.test.tsx
│   │   │   └── Input.test.tsx
│   │   └── sections/
│   │       ├── Hero.test.tsx
│   │       ├── Services.test.tsx
│   │       ├── About.test.tsx
│   │       ├── Team.test.tsx
│   │       ├── FAQ.test.tsx
│   │       └── Contact.test.tsx
│   └── lib/
│       ├── api.test.ts
│       └── analytics.test.ts
├── e2e/
│   ├── navigation.spec.ts
│   └── contact-form.spec.ts
└── playwright.config.ts
```

---

### 8B - Tests Unitaires Frontend (4 tâches)

#### ✅ Tâche 8.4 : Tests Components UI
**Description** : Tests unitaires pour Button, Card, Input

**Actions** :
- [ ] Tests Button : render, variants, onClick, disabled state
- [ ] Tests Card : render, children, className
- [ ] Tests Input : render, onChange, validation, error states

**Couverture attendue** : 90%+

**Exemple de test** :
```typescript
// __tests__/components/ui/Button.test.tsx
describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const onClick = vi.fn()
    render(<Button onClick={onClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(onClick).toHaveBeenCalledTimes(1)
  })
})
```

---

#### ✅ Tâche 8.5 : Tests sections Hero, Services, About
**Description** : Tests pour les 3 premières sections

**Actions** :
- [ ] **Hero** : Render titre, stats animation, CTA, scroll indicator
- [ ] **Services** : Render 8 services, descriptions, icônes
- [ ] **About** : Render mission, vision, valeurs, counter animation

**Mocks nécessaires** :
- Mock API pour récupération données sections
- Mock Framer Motion pour animations

**Couverture attendue** : 80%+

---

#### ✅ Tâche 8.6 : Tests sections Team, FAQ, Contact
**Description** : Tests pour les 3 dernières sections

**Actions** :
- [ ] **Team** : Render 6 membres, photos, liens sociaux
- [ ] **FAQ** : Render questions, accordion toggle, search
- [ ] **Contact** : Render formulaire, validation, soumission, success/error states

**Tests Contact critiques** :
- Validation email format
- Validation champs requis
- Soumission formulaire (mock API)
- Affichage message succès/erreur
- CSRF token handling

**Couverture attendue** : 85%+

---

#### ✅ Tâche 8.7 : Tests lib/api.ts et lib/analytics.ts
**Description** : Tests pour les utilitaires critiques

**Actions** :
- [ ] **api.ts** : Tests hooks React Query, error handling, retry logic
- [ ] **analytics.ts** : Tests tracking sessions, events, heatmap, batch processing

**Tests API** :
```typescript
describe('useHeroData', () => {
  it('fetches hero data successfully', async () => {
    const { result } = renderHook(() => useHeroData())
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toHaveProperty('title')
  })
})
```

**Tests Analytics** :
```typescript
describe('Analytics SDK', () => {
  it('tracks page view on init', () => {
    const tracker = new Analytics()
    expect(mockFetch).toHaveBeenCalledWith('/api/analytics/pageviews/')
  })
})
```

**Couverture attendue** : 90%+

---

### 8C - Tests E2E (2 tâches)

#### 🎭 Tâche 8.8 : Configuration Playwright
**Description** : Setup environnement tests E2E

**Actions** :
- [ ] Créer `playwright.config.ts`
- [ ] Configurer base URL (localhost:3000)
- [ ] Configurer browsers (chromium, firefox, webkit)
- [ ] Ajouter scripts dans package.json

**Configuration** :
```typescript
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
})
```

---

#### 🎭 Tâche 8.9 : Tests E2E navigation et formulaire contact
**Description** : Tests parcours utilisateur complets

**Actions** :
- [ ] **Test navigation** : Scroll sections, menu sticky, smooth scroll
- [ ] **Test formulaire** : Remplir champs, validation, soumission
- [ ] **Test responsive** : Mobile, tablet, desktop
- [ ] **Test analytics** : Vérifier tracking events

**Tests critiques** :
```typescript
test('user can submit contact form', async ({ page }) => {
  await page.goto('/')
  await page.click('a[href="#contact"]')
  await page.fill('input[name="name"]', 'John Doe')
  await page.fill('input[name="email"]', 'john@example.com')
  await page.fill('textarea[name="message"]', 'Hello!')
  await page.click('button[type="submit"]')
  await expect(page.locator('.success-message')).toBeVisible()
})
```

**Couverture attendue** : 5+ scénarios critiques

---

### 8D - Compléter Tests Backend (3 tâches)

#### 📊 Tâche 8.10 : Tests tâches Celery
**Description** : Tests pour send_lead_notification et aggregate_daily_analytics

**Actions** :
- [ ] Tests `send_lead_notification_email` (hot, warm, cold)
- [ ] Tests `aggregate_daily_analytics` avec données réelles
- [ ] Tests retry logic et error handling

**Fichier** : `backend/tests/test_tasks.py`

**Tests critiques** :
```python
class TestLeadNotificationTask(TestCase):
    def test_hot_lead_sends_email_immediately(self):
        lead = Lead.objects.create(
            name="Test", email="test@example.com",
            qualification_score=85, status="new"
        )
        send_lead_notification_email.apply(args=[lead.id])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Hot Lead", mail.outbox[0].subject)
```

**Couverture attendue** : 90%+

---

#### 📊 Tâche 8.11 : Tests agrégation Analytics
**Description** : Tests pour DailyAnalytics aggregation

**Actions** :
- [ ] Tests création DailyAnalytics avec données multiples
- [ ] Tests calculs agrégés (total sessions, avg duration, bounce rate)
- [ ] Tests gestion doublons et idempotence

**Fichier** : `backend/apps/analytics/tests/test_aggregation.py`

**Tests critiques** :
- Aggrégation quotidienne correcte
- Calcul bounce rate (< 30s = bounce)
- Performance avec 1000+ sessions

**Couverture attendue** : 85%+

---

#### 📊 Tâche 8.12 : Augmenter couverture backend à 80%+
**Description** : Combler les gaps de couverture

**Actions** :
- [ ] Analyser rapport de couverture actuel : `coverage run && coverage report`
- [ ] Identifier fichiers < 70% couverture
- [ ] Créer tests manquants (edge cases, error handling)
- [ ] Atteindre 80%+ global

**Commande** :
```bash
cd backend
coverage run --source='.' manage.py test
coverage report -m
coverage html
```

**Objectif** : 80%+ sur tous les apps (core, website, crm, analytics)

---

## 🔥 PHASE 9 : Performance & Sécurité

**Objectif** : Sécuriser l'application et optimiser les performances
**Durée estimée** : 2-3 jours
**Priorité** : 🔴 CRITIQUE

### 9A - Rate Limiting (2 tâches)

#### 🔒 Tâche 9.1 : Installer et configurer Rate Limiting
**Description** : Protection anti-spam des endpoints publics

**Actions** :
- [ ] Installer `django-ratelimit`
- [ ] Créer décorateur custom pour DRF
- [ ] Configurer cache backend (Redis ou DB)

**Installation** :
```bash
cd backend
pip install django-ratelimit
pip freeze > requirements.txt
```

**Configuration** (`config/settings.py`) :
```python
INSTALLED_APPS += ['django_ratelimit']

RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'  # Utilise Redis si disponible
```

---

#### 🔒 Tâche 9.2 : Protéger endpoints Contact et Analytics
**Description** : Appliquer rate limiting aux endpoints critiques

**Actions** :
- [ ] `/api/website/contact/` : 5 requêtes / 5 minutes par IP
- [ ] `/api/analytics/events/` : 100 requêtes / minute par session
- [ ] `/api/analytics/heatmap/` : 50 requêtes / minute par session
- [ ] Retourner HTTP 429 avec message clair

**Implémentation** :
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/5m', method='POST')
def contact_submit(request):
    # Existing code
    pass
```

**Tests** :
- [ ] Test dépassement limite retourne 429
- [ ] Test réinitialisation après période
- [ ] Test bypass pour users authentifiés (admin)

**Fichiers modifiés** :
- `backend/apps/website/views.py`
- `backend/apps/analytics/views.py`

---

### 9B - Monitoring Sentry (2 tâches)

#### 🚨 Tâche 9.3 : Intégrer Sentry (backend + frontend)
**Description** : Installation et configuration tracking erreurs temps réel

**Actions** :
- [ ] Créer compte Sentry (sentry.io)
- [ ] Créer 2 projets : "pinnacle-backend", "pinnacle-frontend"
- [ ] Installer SDK backend : `pip install sentry-sdk`
- [ ] Installer SDK frontend : `npm install @sentry/nextjs`

**Backend** (`config/settings.py`) :
```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN_BACKEND'),
    environment=os.environ.get('ENVIRONMENT', 'production'),
    traces_sample_rate=0.1,
)
```

**Frontend** (`sentry.client.config.ts`) :
```typescript
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
})
```

**Variables d'environnement** :
- `SENTRY_DSN_BACKEND`
- `NEXT_PUBLIC_SENTRY_DSN`

---

#### 🚨 Tâche 9.4 : Configurer alertes et error tracking
**Description** : Setup notifications et contexte enrichi

**Actions** :
- [ ] Configurer alertes email/Slack pour erreurs critiques
- [ ] Activer release tracking (git commits)
- [ ] Ajouter contexte utilisateur (user ID, email si disponible)
- [ ] Configurer breadcrumbs pour navigation
- [ ] Filtrer erreurs non critiques (404, CORS, etc.)

**Configuration alertes** :
- Erreurs 500+ : Alerte immédiate
- Taux d'erreur > 5% : Alerte critique
- Performance dégradée (> 3s) : Warning

**Tests** :
- [ ] Déclencher erreur test backend : `raise Exception("Test Sentry")`
- [ ] Déclencher erreur test frontend : `throw new Error("Test Sentry")`
- [ ] Vérifier réception dans dashboard Sentry

---

### 9C - Redis & Celery (2 tâches)

#### ⚡ Tâche 9.5 : Configurer Redis sur Render
**Description** : Setup Redis pour broker Celery et cache

**Actions** :
- [ ] Créer service Redis dans Render dashboard
- [ ] Récupérer `REDIS_URL` (format: `redis://...`)
- [ ] Ajouter variable d'environnement au service backend
- [ ] Tester connexion Redis

**Configuration Render** :
1. Dashboard → "New" → "Redis"
2. Plan : Free (25 MB, suffit pour démarrage)
3. Copier Internal Redis URL

**Test connexion** :
```python
import redis
r = redis.from_url(os.environ['REDIS_URL'])
r.set('test', 'hello')
print(r.get('test'))  # b'hello'
```

---

#### ⚡ Tâche 9.6 : Optimiser Celery avec Redis broker
**Description** : Migrer Celery de mode synchrone vers Redis

**Actions** :
- [ ] Installer `redis` : `pip install redis`
- [ ] Modifier `config/celery.py` pour utiliser Redis
- [ ] Configurer result backend Redis
- [ ] Redémarrer worker Celery sur Render

**Configuration** (`config/celery.py`) :
```python
app.conf.broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.conf.result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
```

**Render configuration** (render.yaml) :
```yaml
- type: worker
  name: pinnacle-celery
  env: python
  buildCommand: "pip install -r requirements.txt"
  startCommand: "celery -A config worker -l info"
  envVars:
    - key: REDIS_URL
      fromService:
        type: redis
        name: pinnacle-redis
```

**Tests** :
- [ ] Tâches exécutées en asynchrone (non bloquant)
- [ ] Vérifier résultats dans Redis
- [ ] Performance amélioration (email < 5s)

**Amélioration attendue** : 10x plus rapide pour tâches async

---

### 9D - Core Web Vitals (2 tâches)

#### 🎯 Tâche 9.7 : Mesurer performance actuelle
**Description** : Audit performance avec Lighthouse et Web Vitals

**Actions** :
- [ ] Audit Lighthouse (Chrome DevTools)
- [ ] Installer `web-vitals` npm package
- [ ] Créer rapport baseline (LCP, FID, CLS, TTFB, INP)
- [ ] Identifier bottlenecks

**Installation Web Vitals** :
```bash
cd frontend
npm install web-vitals
```

**Implémentation** (`app/layout.tsx`) :
```typescript
import { onCLS, onFID, onLCP, onINP, onTTFB } from 'web-vitals'

export function WebVitals() {
  useEffect(() => {
    onCLS(console.log)
    onFID(console.log)
    onLCP(console.log)
    onINP(console.log)
    onTTFB(console.log)
  }, [])
}
```

**Objectifs cibles** :
- LCP (Largest Contentful Paint) : < 2.5s ✅
- FID (First Input Delay) : < 100ms ✅
- CLS (Cumulative Layout Shift) : < 0.1 ✅
- TTFB (Time to First Byte) : < 600ms ✅
- INP (Interaction to Next Paint) : < 200ms ✅

**Rapport baseline attendu** :
```
Current Performance:
- LCP: 3.2s ⚠️ (target: < 2.5s)
- FID: 45ms ✅
- CLS: 0.15 ⚠️ (target: < 0.1)
- TTFB: 520ms ✅
- INP: 180ms ✅
```

---

#### 🎯 Tâche 9.8 : Optimiser LCP, CLS, FID pour score 90+
**Description** : Optimisations ciblées pour atteindre score parfait

**Actions** :
- [ ] **LCP Optimization** :
  - Précharger image Hero : `<link rel="preload" as="image" href="/hero.jpg">`
  - Optimiser font loading (font-display: swap)
  - Réduire taille bundle JavaScript (code splitting)

- [ ] **CLS Optimization** :
  - Ajouter dimensions explicites images : `width` et `height`
  - Réserver espace pour contenu dynamique
  - Éviter insertion contenu au-dessus du fold

- [ ] **FID/INP Optimization** :
  - Réduire JavaScript bloquant
  - Utiliser `useTransition` React pour updates lourdes
  - Defer scripts non critiques

**Optimisations Next.js** (`next.config.ts`) :
```typescript
const config = {
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['framer-motion', 'lucide-react'],
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
}
```

**Font Optimization** (`app/layout.tsx`) :
```typescript
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Évite FOIT (Flash of Invisible Text)
  preload: true,
})
```

**Tests après optimisation** :
- [ ] Lighthouse score > 90
- [ ] Tous Core Web Vitals dans zone verte
- [ ] Test sur mobile + desktop

**Objectif final** : Performance score 95+/100

---

### 9E - Optimisation Images (2 tâches)

#### 🖼️ Tâche 9.9 : Générer blur placeholders (backend)
**Description** : Créer blur data URLs pour images Team

**Actions** :
- [ ] Installer Pillow : `pip install Pillow`
- [ ] Créer management command `generate_blur_placeholders`
- [ ] Ajouter champ `blur_data_url` au modèle Team
- [ ] Générer blur hash 20x20px pour chaque photo
- [ ] Exposer dans serializer

**Modèle** (`apps/website/models.py`) :
```python
class Team(models.Model):
    # ... existing fields
    photo = models.ImageField(upload_to='team/')
    blur_data_url = models.TextField(blank=True, null=True)

    def generate_blur_placeholder(self):
        from PIL import Image
        import base64
        from io import BytesIO

        img = Image.open(self.photo.path)
        img = img.resize((20, 20), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=50)
        data = base64.b64encode(buffer.getvalue()).decode()
        self.blur_data_url = f"data:image/jpeg;base64,{data}"
        self.save()
```

**Management command** :
```bash
python manage.py generate_blur_placeholders
```

**Tests** :
- [ ] Génération réussie pour toutes les photos
- [ ] Taille < 2KB par blur hash
- [ ] Format base64 valide

---

#### 🖼️ Tâche 9.10 : Implémenter blur placeholders (frontend)
**Description** : Utiliser blur placeholders dans Next.js Image

**Actions** :
- [ ] Modifier TeamSerializer pour inclure `blur_data_url`
- [ ] Mettre à jour type TypeScript `TeamMember`
- [ ] Utiliser prop `placeholder="blur"` dans Image component
- [ ] Tester amélioration UX (progressive loading)

**Implémentation** (`components/sections/Team.tsx`) :
```typescript
<Image
  src={member.photo}
  alt={member.name}
  width={300}
  height={300}
  placeholder="blur"
  blurDataURL={member.blur_data_url}
  className="rounded-full"
/>
```

**Type** (`types/index.ts`) :
```typescript
export interface TeamMember {
  name: string
  role: string
  photo: string
  blur_data_url?: string  // Nouveau champ
  bio: string
  linkedin?: string
}
```

**Tests** :
- [ ] Images chargent avec blur effect
- [ ] Transition smooth blur → image
- [ ] Performance amélioration (perception)

**Amélioration UX attendue** : Élimination du "pop-in" d'images

---

## 🏗️ PHASE 10 : Infrastructure & SEO

**Objectif** : Solidifier l'infrastructure et maximiser la visibilité SEO
**Durée estimée** : 1-2 jours
**Priorité** : 🟡 IMPORTANTE

### 10A - Backups Automatiques (2 tâches)

#### 💾 Tâche 10.1 : Configurer backups automatiques PostgreSQL
**Description** : Backups quotidiens automatiques via Render

**Actions** :
- [ ] Activer Point-in-Time Recovery (PITR) dans Render
- [ ] Configurer rétention 7 jours (plan gratuit)
- [ ] Configurer backup schedule (daily 3:00 AM UTC)
- [ ] Documenter procédure de restauration

**Configuration Render** :
1. Dashboard → PostgreSQL service → "Backups"
2. Activer "Automatic Backups"
3. Schedule : Daily at 03:00 UTC
4. Retention : 7 days

**Alternative script custom** (`backend/scripts/backup_db.py`) :
```python
import subprocess
import os
from datetime import datetime

def backup_database():
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    database_url = os.environ['DATABASE_URL']

    subprocess.run([
        'pg_dump',
        database_url,
        '-f', backup_file
    ])

    # Upload to S3 or cloud storage
    print(f"Backup created: {backup_file}")
```

**Cron job** (si hébergement supporte cron) :
```bash
0 3 * * * cd /app && python scripts/backup_db.py
```

---

#### 💾 Tâche 10.2 : Créer script de restauration et test
**Description** : Procédure testée de restauration

**Actions** :
- [ ] Créer script `restore_db.py`
- [ ] Documenter étapes de restauration dans README
- [ ] Tester restauration sur environnement staging
- [ ] Créer checklist incident response

**Script restauration** (`backend/scripts/restore_db.py`) :
```python
import subprocess
import sys

def restore_database(backup_file):
    """
    Restore database from backup file
    Usage: python restore_db.py backup_20251108.sql
    """
    database_url = os.environ['DATABASE_URL']

    # Warning
    confirm = input(f"⚠️  This will OVERWRITE current database. Continue? (yes/no): ")
    if confirm != 'yes':
        sys.exit("Restoration cancelled")

    subprocess.run([
        'psql',
        database_url,
        '-f', backup_file
    ])

    print("✅ Database restored successfully")

if __name__ == '__main__':
    restore_database(sys.argv[1])
```

**Documentation** (ajout au README) :
```markdown
## Database Backup & Restore

### Backup
Automatic daily backups at 3:00 AM UTC (7-day retention)

### Manual Restore
1. Download backup from Render dashboard
2. Run: `python scripts/restore_db.py backup_file.sql`
3. Verify data integrity
4. Restart services
```

**Tests** :
- [ ] Créer backup de test
- [ ] Restaurer sur DB staging
- [ ] Vérifier intégrité données
- [ ] Documenter temps de restauration

---

### 10B - Uptime Monitoring (2 tâches)

#### 📡 Tâche 10.3 : Setup uptime monitoring
**Description** : Surveillance 24/7 de la disponibilité

**Options** :
1. **UptimeRobot** (gratuit, 50 monitors)
2. **Render Health Checks** (intégré)
3. **Pingdom** (payant, plus features)

**Actions** :
- [ ] Créer compte UptimeRobot
- [ ] Configurer monitors :
  - Frontend : `https://pinnacle-advisors.tech` (HTTP, interval 5min)
  - Backend API : `https://api.pinnacle-advisors.tech/health/` (HTTP 200, interval 5min)
  - Backend Admin : `https://api.pinnacle-advisors.tech/admin/` (HTTP 200/302)
- [ ] Configurer alertes email + SMS
- [ ] Configurer public status page

**Configuration UptimeRobot** :
```
Monitor 1: Frontend
- URL: https://pinnacle-advisors.tech
- Type: HTTP(s)
- Interval: 5 minutes
- Alert contacts: your-email@example.com

Monitor 2: Backend Health
- URL: https://api.pinnacle-advisors.tech/health/
- Type: HTTP(s) - Keyword
- Keyword: "status": "healthy"
- Interval: 5 minutes
```

**Status Page** :
- Public URL : `https://stats.uptimerobot.com/your-key`
- À ajouter en footer du site

---

#### 📡 Tâche 10.4 : Configurer healthcheck endpoints avancés
**Description** : Endpoints détaillés pour monitoring infrastructure

**Actions** :
- [ ] Améliorer endpoint `/health/` avec checks détaillés
- [ ] Ajouter `/health/db/` - test connexion PostgreSQL
- [ ] Ajouter `/health/redis/` - test connexion Redis
- [ ] Ajouter `/health/celery/` - test worker status
- [ ] Retourner status codes appropriés (200, 503)

**Implémentation** (`apps/core/views.py`) :
```python
from django.db import connection
from django.core.cache import cache
import redis

@api_view(['GET'])
def health_check(request):
    """Comprehensive health check"""
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'celery': check_celery(),
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return Response({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks,
        'timestamp': timezone.now().isoformat()
    }, status=status_code)

def check_database():
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False

def check_redis():
    try:
        cache.set('health_check', 'ok', 10)
        return cache.get('health_check') == 'ok'
    except Exception:
        return False
```

**Tests** :
- [ ] `/health/` retourne 200 quand tout OK
- [ ] `/health/` retourne 503 si DB down
- [ ] Logs détaillés des échecs

---

### 10C - Google Search Console (3 tâches)

#### 🔍 Tâche 10.5 : Intégrer Google Search Console
**Description** : Setup et vérification propriété site

**Actions** :
- [ ] Créer compte Google Search Console
- [ ] Ajouter propriété `https://pinnacle-advisors.tech`
- [ ] Vérifier propriété (méthode DNS ou HTML meta tag)
- [ ] Lier à Google Analytics (optionnel)

**Méthode vérification DNS** (Namecheap) :
1. Search Console → Add Property → Domain
2. Copier TXT record : `google-site-verification=abc123...`
3. Namecheap → Advanced DNS → Add TXT record
4. Host: `@`, Value: `google-site-verification=abc123...`
5. Wait 10-60min, verify

**Méthode HTML meta tag** :
```html
<!-- app/layout.tsx -->
<meta name="google-site-verification" content="abc123..." />
```

---

#### 🔍 Tâche 10.6 : Vérifier schemas avec Google Rich Results Test
**Description** : Validation schemas JSON-LD pour Rich Snippets

**Actions** :
- [ ] Tester Organization schema : [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Tester Service schema (ItemList)
- [ ] Tester FAQ schema (FAQPage)
- [ ] Tester Person schema (Team members)
- [ ] Corriger erreurs/warnings éventuels

**URLs à tester** :
- `https://pinnacle-advisors.tech` (Organization)
- `https://pinnacle-advisors.tech#services` (Service)
- `https://pinnacle-advisors.tech#faq` (FAQ)
- `https://pinnacle-advisors.tech#team` (Person)

**Critères validation** :
- ✅ 0 erreurs
- ✅ 0 warnings (ou justifiés)
- ✅ Preview correct dans Rich Results

**Corrections possibles** :
- Ajouter champs manquants (priceRange, aggregateRating)
- Valider formats (ISO dates, URLs, etc.)
- Tester sur Google Mobile-Friendly Test

---

#### 🔍 Tâche 10.7 : Soumettre sitemap et tester indexation
**Description** : Accélérer indexation Google

**Actions** :
- [ ] Soumettre sitemap : Search Console → Sitemaps → Add `https://pinnacle-advisors.tech/sitemap.xml`
- [ ] Demander indexation page principale : URL Inspection → Request Indexing
- [ ] Vérifier robots.txt accessible : `https://pinnacle-advisors.tech/robots.txt`
- [ ] Monitorer erreurs crawl (Coverage report)
- [ ] Attendre 3-7 jours pour indexation complète

**Vérifications** :
```bash
# Test robots.txt
curl https://pinnacle-advisors.tech/robots.txt

# Test sitemap
curl https://pinnacle-advisors.tech/sitemap.xml

# Test structured data
curl -H "User-Agent: Googlebot" https://pinnacle-advisors.tech
```

**Suivi indexation** :
- Search Console → Coverage → Valid pages
- Objectif : 100% pages indexées dans 7 jours

**Optimisations additionnelles** :
- [ ] Créer Google Business Profile (GMB)
- [ ] Soumettre à Bing Webmaster Tools
- [ ] Créer profil LinkedIn entreprise avec lien site

---

## 📚 PHASE 11 : Documentation & Post-Launch

**Objectif** : Documentation complète et préparation maintenance long terme
**Durée estimée** : 1-2 jours
**Priorité** : 🟢 RECOMMANDÉE

### 11A - Documentation Technique (3 tâches)

#### 📚 Tâche 11.1 : Guide API avec exemples
**Description** : Documentation complète des 117 endpoints

**Actions** :
- [ ] Créer `API_DOCUMENTATION.md`
- [ ] Documenter chaque endpoint avec :
  - Méthode HTTP, URL, description
  - Paramètres (query, body)
  - Exemple requête/réponse (cURL + JavaScript)
  - Codes d'erreur possibles
- [ ] Ajouter guide authentification
- [ ] Exemples intégration (React, Vue, vanilla JS)

**Structure** :
```markdown
# API Documentation - Pinnacle Advisors

## Authentication
Public endpoints (no auth required):
- `GET /api/website/*` - Read-only content
- `POST /api/website/contact/` - Submit contact form
- `POST /api/analytics/*` - Analytics tracking

Admin endpoints (auth required):
- `GET /api/crm/leads/` - Manage leads
- All POST/PUT/DELETE on content

## Endpoints

### GET /api/website/hero/
Fetch hero section data

**Response:**
```json
{
  "id": 1,
  "title": "Optimisez Votre Chaîne d'Approvisionnement",
  "subtitle": "Expertise en Supply Chain...",
  "cta_text": "Demander une consultation",
  "stats": [...]
}
```

**Example (cURL):**
```bash
curl https://api.pinnacle-advisors.tech/api/website/hero/
```

**Example (JavaScript):**
```javascript
const response = await fetch('https://api.pinnacle-advisors.tech/api/website/hero/')
const data = await response.json()
```
```

**Fichier** : `API_DOCUMENTATION.md` (15+ pages attendues)

---

#### 📚 Tâche 11.2 : Documentation composants frontend
**Description** : Props, usage, exemples pour chaque composant

**Actions** :
- [ ] Créer `COMPONENTS.md`
- [ ] Documenter 11 composants principaux
- [ ] Ajouter props TypeScript avec descriptions
- [ ] Exemples d'utilisation
- [ ] Screenshots (optionnel)

**Structure** :
```markdown
# Components Documentation

## UI Components

### Button
Reusable button component with variants

**Props:**
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' | 'primary' | Button style |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Button size |
| onClick | () => void | - | Click handler |
| disabled | boolean | false | Disabled state |

**Usage:**
```tsx
<Button variant="primary" size="lg" onClick={handleClick}>
  Click me
</Button>
```

**Variants:**
- Primary: Blue background (#3B82F6)
- Secondary: Transparent with border
```

**Alternative** : Setup Storybook pour documentation interactive
```bash
npx storybook@latest init
```

---

#### 📚 Tâche 11.3 : Guide de déploiement et maintenance
**Description** : Procédures opérationnelles complètes

**Actions** :
- [ ] Créer `DEPLOYMENT.md`
- [ ] Documenter workflow Git (branches, PR, merge)
- [ ] Procédures déploiement (staging, production)
- [ ] Procédures rollback
- [ ] Checklist pre-deployment
- [ ] Incident response guide

**Contenu** :
```markdown
# Deployment & Maintenance Guide

## Git Workflow
1. Create feature branch: `git checkout -b feature/new-feature`
2. Commit changes: `git commit -m "feat: description"`
3. Push branch: `git push origin feature/new-feature`
4. Create Pull Request on GitHub
5. Wait for CI/CD checks ✅
6. Merge to main → Auto-deploy to production

## Deployment Pipeline
- **Trigger**: Push to `main` branch
- **Backend**: Auto-deploy to Render (3-5 min)
- **Frontend**: Auto-deploy to Vercel (2-3 min)
- **Migrations**: Run automatically on Render

## Pre-Deployment Checklist
- [ ] All tests passing locally
- [ ] No console errors
- [ ] Database migrations tested
- [ ] Environment variables updated
- [ ] Backup database

## Rollback Procedure
1. Identify bad commit SHA
2. Revert: `git revert <commit-sha>`
3. Push: `git push origin main`
4. Wait for auto-deploy (3-5 min)
5. Verify rollback successful

## Incident Response
1. **Detect**: Sentry alert, uptime monitor, user report
2. **Assess**: Check logs, Sentry errors, database
3. **Fix**: Hotfix or rollback
4. **Deploy**: Emergency deploy
5. **Post-mortem**: Document incident

## Maintenance Tasks
- **Daily**: Check Sentry errors, uptime reports
- **Weekly**: Review analytics, CRM leads, database size
- **Monthly**: Update dependencies, security patches
```

---

### 11B - Formation Utilisateurs (2 tâches)

#### 🎓 Tâche 11.4 : Guide utilisateur Admin Django
**Description** : Manuel pour équipe non-technique

**Actions** :
- [ ] Créer `USER_GUIDE_ADMIN.md` avec screenshots
- [ ] Tutoriel connexion admin
- [ ] Tutoriel modification contenu (Hero, Services, FAQ, Team)
- [ ] Tutoriel gestion newsletter subscribers
- [ ] Guide permissions et rôles

**Contenu** :
```markdown
# Guide Utilisateur - Admin Django

## 1. Connexion à l'Administration

**URL**: https://api.pinnacle-advisors.tech/admin/

**Identifiants**: Fournis par l'administrateur système

**Étapes**:
1. Ouvrir navigateur (Chrome recommandé)
2. Aller sur https://api.pinnacle-advisors.tech/admin/
3. Entrer username et password
4. Cliquer "Log in"

[Screenshot: Page de login]

## 2. Modifier le Contenu de la Page d'Accueil

### 2.1 Modifier la Section Hero
1. Cliquer "Website" → "Hero sections"
2. Cliquer sur la ligne existante
3. Modifier les champs :
   - **Title**: Titre principal (max 100 caractères)
   - **Subtitle**: Sous-titre (max 255 caractères)
   - **CTA Text**: Texte bouton (ex: "Contactez-nous")
4. Cliquer "Save"

[Screenshot: Hero section edit]

### 2.2 Ajouter/Modifier un Service
1. Cliquer "Website" → "Services"
2. Cliquer "Add Service" (ou modifier existant)
3. Remplir :
   - **Title**: Nom du service
   - **Description**: Description complète
   - **Icon**: Nom icône (voir liste disponible)
4. Cliquer "Save"

[Screenshot: Service edit]

## 3. Gestion des Abonnés Newsletter
1. Cliquer "Website" → "Newsletter subscribers"
2. Voir liste complète avec email + date
3. Export CSV : Cliquer "Export" en haut
4. Delete : Sélectionner lignes → "Delete selected"

## 4. Bonnes Pratiques
- ⚠️ Ne pas supprimer de contenu sans backup
- ✅ Tester modifications sur staging si disponible
- ✅ Utiliser preview avant save
- ✅ Optimiser images avant upload (< 500 KB)
```

**Format** : PDF + Markdown avec screenshots

---

#### 🎓 Tâche 11.5 : Guide CRM et gestion des leads
**Description** : Tutoriel utilisation CRM pour sales team

**Actions** :
- [ ] Créer `USER_GUIDE_CRM.md`
- [ ] Expliquer auto-qualification (Hot/Warm/Cold)
- [ ] Tutoriel gestion pipeline
- [ ] Tutoriel ajout interactions et notes
- [ ] Best practices suivi leads

**Contenu** :
```markdown
# Guide CRM - Gestion des Leads

## 1. Comprendre l'Auto-Qualification

Le système qualifie automatiquement chaque lead sur 100 points :

**🔥 Hot Lead (70-100 points)**
- Forte probabilité de conversion
- Email automatique envoyé sous 24h
- **Action**: Contacter immédiatement

**☀️ Warm Lead (40-69 points)**
- Potentiel moyen
- Email envoyé sous 48-72h
- **Action**: Planifier suivi cette semaine

**❄️ Cold Lead (0-39 points)**
- Faible probabilité court terme
- Nurturing seulement
- **Action**: Newsletter mensuelle

## 2. Consulter les Leads

1. Admin → "CRM" → "Leads"
2. Filtres disponibles :
   - Par statut (New, Contacted, Qualified, etc.)
   - Par score (Hot/Warm/Cold)
   - Par date
3. Trier par colonne (clic sur header)

[Screenshot: Lead list]

## 3. Gérer un Lead

### Ouvrir le lead
1. Cliquer sur nom du lead
2. Voir détails complets :
   - Info contact (nom, email, téléphone, entreprise)
   - Score qualification + critères
   - Message original
   - Historique interactions

### Changer le statut
1. "Status" dropdown → Sélectionner nouveau statut
2. Options :
   - **New**: Nouveau lead (non traité)
   - **Contacted**: Premier contact effectué
   - **Qualified**: Lead qualifié (intéressé)
   - **Proposal Sent**: Proposition commerciale envoyée
   - **Negotiation**: En négociation
   - **Won**: Client gagné ✅
   - **Lost**: Opportunité perdue ❌
3. Cliquer "Save"

### Ajouter une interaction
1. Scroll → "Interactions" section
2. Cliquer "Add another Interaction"
3. Remplir :
   - **Type**: Email, Phone, Meeting, etc.
   - **Notes**: Résumé de l'échange
   - **Date**: Date/heure interaction
   - **Outcome**: Positive, Neutral, Negative
4. Cliquer "Save"

### Ajouter une note
1. Scroll → "Notes" section
2. Cliquer "Add another Note"
3. Écrire note libre
4. "Save"

## 4. Pipeline de Vente

1. Admin → "CRM" → "Pipelines"
2. Créer pipeline personnalisé :
   - Ex: "Enterprise Sales Q4 2025"
   - Stages: Prospect → Demo → Proposal → Closed
3. Assigner leads au pipeline
4. Tracker progression

## 5. Rapports et Analytics

1. Admin → "Analytics" → "Daily analytics"
2. Voir :
   - Total leads / jour
   - Taux conversion
   - Sources leads (Google, LinkedIn, Direct)
3. Export CSV pour analyse externe

## 6. Best Practices

✅ **DO**:
- Répondre aux Hot Leads dans les 4h
- Mettre à jour statut après chaque interaction
- Ajouter notes détaillées (facilite handoff)
- Vérifier CRM 2x par jour minimum

❌ **DON'T**:
- Laisser Hot Lead > 24h sans réponse
- Oublier de logger interactions
- Spam Cold Leads (respecter préférences)
- Supprimer leads (archive instead)
```

---

### 11C - Analytics Avancés (2 tâches)

#### 📊 Tâche 11.6 : Dashboard insights et rapports
**Description** : Interface visualisation analytics avancée

**Actions** :
- [ ] Créer vue admin custom `AnalyticsDashboardView`
- [ ] Graphiques avec Chart.js ou Recharts :
  - Trafic quotidien (7 derniers jours)
  - Taux de rebond par source
  - Top 5 pages vues
  - Heatmap clics agrégée
- [ ] Filtres par date range
- [ ] Export graphiques en PNG

**Implémentation** (`apps/analytics/admin.py`) :
```python
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

class AnalyticsAdminSite(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='analytics_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Fetch analytics data
        daily_stats = DailyAnalytics.objects.filter(
            date__gte=timezone.now() - timedelta(days=7)
        ).order_by('date')

        context = {
            'daily_stats': daily_stats,
            'total_sessions': Session.objects.count(),
            'avg_duration': Session.objects.aggregate(Avg('duration'))['duration__avg'],
        }

        return render(request, 'admin/analytics_dashboard.html', context)
```

**Template** (`templates/admin/analytics_dashboard.html`) :
```html
{% extends "admin/base_site.html" %}

{% block content %}
<h1>Analytics Dashboard</h1>

<div class="dashboard-stats">
  <div class="stat-card">
    <h3>Total Sessions</h3>
    <p class="stat-value">{{ total_sessions }}</p>
  </div>
  <div class="stat-card">
    <h3>Avg Duration</h3>
    <p class="stat-value">{{ avg_duration|floatformat:0 }}s</p>
  </div>
</div>

<canvas id="trafficChart"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('trafficChart')
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: [{% for stat in daily_stats %}'{{ stat.date }}'{% if not forloop.last %},{% endif %}{% endfor %}],
      datasets: [{
        label: 'Sessions',
        data: [{% for stat in daily_stats %}{{ stat.total_sessions }}{% if not forloop.last %},{% endif %}{% endfor %}],
        borderColor: 'rgb(59, 130, 246)',
        tension: 0.1
      }]
    }
  })
</script>
{% endblock %}
```

**Accès** : `https://api.pinnacle-advisors.tech/admin/analytics/dashboard/`

---

#### 📊 Tâche 11.7 : Export données (CSV/Excel)
**Description** : Fonctionnalité export pour leads et analytics

**Actions** :
- [ ] Ajouter action admin "Export selected to CSV"
- [ ] Endpoint API `/api/crm/leads/export/?format=csv`
- [ ] Endpoint `/api/analytics/sessions/export/?format=csv`
- [ ] Support date range filters
- [ ] Format Excel (.xlsx) optionnel

**Implémentation** (`apps/crm/admin.py`) :
```python
import csv
from django.http import HttpResponse

class LeadAdmin(admin.ModelAdmin):
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Company', 'Status', 'Score', 'Created'])

        for lead in queryset:
            writer.writerow([
                lead.name,
                lead.email,
                lead.company,
                lead.status,
                lead.qualification_score,
                lead.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        return response

    export_to_csv.short_description = "Export selected leads to CSV"
```

**API Endpoint** (`apps/crm/views.py`) :
```python
@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_leads(request):
    format_type = request.query_params.get('format', 'csv')

    leads = Lead.objects.all()

    # Filters
    if 'status' in request.query_params:
        leads = leads.filter(status=request.query_params['status'])

    if 'date_from' in request.query_params:
        leads = leads.filter(created_at__gte=request.query_params['date_from'])

    # Generate CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="leads_{timezone.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Company', 'Phone', 'Status', 'Score', 'Created'])

    for lead in leads:
        writer.writerow([
            lead.name, lead.email, lead.company, lead.phone,
            lead.status, lead.qualification_score, lead.created_at
        ])

    return response
```

**Usage** :
```bash
# Admin interface: Select leads → Actions → "Export selected to CSV"

# API:
curl -H "Authorization: Token YOUR_TOKEN" \
  "https://api.pinnacle-advisors.tech/api/crm/leads/export/?format=csv&status=qualified"
```

**Excel support** (optionnel avec openpyxl) :
```python
pip install openpyxl

import openpyxl
from openpyxl.utils import get_column_letter

def export_to_excel(queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads"

    # Headers
    headers = ['Name', 'Email', 'Company', 'Status', 'Score']
    ws.append(headers)

    # Data
    for lead in queryset:
        ws.append([lead.name, lead.email, lead.company, lead.status, lead.qualification_score])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="leads.xlsx"'
    wb.save(response)

    return response
```

---

### 11D - Post-Launch (2 tâches)

#### 🚀 Tâche 11.8 : Audit final sécurité et performance
**Description** : Revue complète avant release 100%

**Actions** :
- [ ] **Sécurité** :
  - Scan vulnérabilités : `safety check` (Python), `npm audit` (JS)
  - Test injection SQL (même si Django ORM protège)
  - Test XSS sur formulaires
  - Vérifier HTTPS force (pas de HTTP)
  - Vérifier headers sécurité (CSP, X-Frame-Options, etc.)

- [ ] **Performance** :
  - Lighthouse audit final (desktop + mobile)
  - Test charge avec Apache Bench ou k6
  - Vérifier temps réponse API (< 200ms)
  - Database query optimization (Django Debug Toolbar)

- [ ] **Accessibilité** :
  - WCAG 2.1 AA compliance
  - Test lecteur écran (NVDA/JAWS)
  - Contraste couleurs (ratio 4.5:1 min)
  - Navigation clavier complète

**Outils** :
```bash
# Security scan
cd backend
safety check
bandit -r apps/

cd frontend
npm audit fix

# Performance
lighthouse https://pinnacle-advisors.tech --view

# Load test (1000 requests, 10 concurrent)
ab -n 1000 -c 10 https://pinnacle-advisors.tech/

# Accessibility
npm install -g pa11y
pa11y https://pinnacle-advisors.tech
```

**Checklist finale** :
- [ ] 0 vulnérabilités critiques
- [ ] Performance score > 90
- [ ] Accessibility score > 95
- [ ] SEO score > 90
- [ ] Best Practices score > 90
- [ ] Tous tests passent (backend + frontend)
- [ ] 0 erreurs Sentry en 7 jours
- [ ] Uptime > 99.9% sur 30 jours

---

#### 🚀 Tâche 11.9 : Créer roadmap fonctionnalités futures
**Description** : Plan évolution 3-6 mois

**Actions** :
- [ ] Créer `ROADMAP_FUTURE.md`
- [ ] Prioriser features (MoSCoW method)
- [ ] Estimer complexité (T-shirt sizing)
- [ ] Définir OKRs (Objectives & Key Results)

**Contenu** :
```markdown
# Roadmap Fonctionnalités Futures - Pinnacle Advisors

## Q1 2026 (Jan-Mar) - Internationalization & Multi-language

### 🎯 Objectifs
- Support Français + Anglais
- Augmenter audience internationale de 30%

### ✅ Features
1. **i18n Integration** (Complexité: L, Priorité: MUST)
   - Next-intl pour frontend
   - Django modeltranslation pour backend
   - Détection langue automatique (browser + geolocation)
   - Toggle FR/EN dans navbar

2. **Content Translation** (Complexité: M, Priorité: MUST)
   - Traduire tous textes statiques
   - Interface admin multilingue
   - URLs localisées (/fr/, /en/)

3. **SEO Multi-langue** (Complexité: S, Priorité: SHOULD)
   - hreflang tags
   - Sitemap multilingue
   - Structured data traduit

**Effort total** : 2-3 semaines
**ROI attendu** : +30% trafic organique

---

## Q2 2026 (Apr-Jun) - Advanced CRM & Automation

### 🎯 Objectifs
- Automatiser 80% du nurturing
- Réduire temps qualification de 50%

### ✅ Features
1. **Email Drip Campaigns** (Complexité: XL, Priorité: SHOULD)
   - Séquences automatiques (Welcome, Nurturing, Re-engagement)
   - Templates personnalisables
   - A/B testing subject lines
   - Tracking open rate, click rate

2. **Lead Scoring v2** (Complexité: M, Priorité: COULD)
   - ML-based scoring (scikit-learn)
   - Facteurs prédictifs : industry, job title, page views
   - Auto-reassignment hot leads

3. **Calendar Integration** (Complexité: L, Priorité: SHOULD)
   - Booking page (Calendly-style)
   - Google Calendar sync
   - Auto-send meeting reminders

**Effort total** : 4-6 semaines
**ROI attendu** : -50% temps qualification, +20% conversion

---

## Q3 2026 (Jul-Sep) - Client Portal & Self-Service

### 🎯 Objectifs
- Réduire support queries de 40%
- Augmenter satisfaction client (NPS > 70)

### ✅ Features
1. **Client Dashboard** (Complexité: XL, Priorité: COULD)
   - Login sécurisé (OAuth2)
   - View projects en cours
   - Download rapports/documents
   - Messaging avec consultant

2. **Knowledge Base** (Complexité: L, Priorité: SHOULD)
   - Articles blog SEO-optimisés
   - Guides téléchargeables (PDF)
   - Search functionality
   - Related articles recommendations

3. **Case Studies** (Complexité: M, Priorité: COULD)
   - Showcase projets réussis
   - Before/After metrics
   - Client testimonials vidéo
   - Social proof (logos clients)

**Effort total** : 5-7 semaines
**ROI attendu** : -40% support, +15% inbound leads

---

## Q4 2026 (Oct-Dec) - Advanced Analytics & AI

### 🎯 Objectifs
- Predictive insights pour sales team
- Optimisation conversion +25%

### ✅ Features
1. **Predictive Lead Scoring** (Complexité: XL, Priorité: WON'T - 2027)
   - Machine learning model (TensorFlow/PyTorch)
   - Training sur historique conversions
   - Real-time predictions

2. **Chatbot AI** (Complexité: L, Priorité: COULD)
   - GPT-4 powered chatbot
   - Réponses FAQ automatiques
   - Lead qualification conversationnelle
   - Handoff to human si nécessaire

3. **Advanced Heatmaps** (Complexité: M, Priorité: SHOULD)
   - Rage clicks detection
   - Scroll depth heatmap
   - Session recordings (privacy-compliant)
   - Conversion funnels visualization

**Effort total** : 6-8 semaines
**ROI attendu** : +25% conversion rate

---

## Backlog (Non priorisé)

### Features Ideas
- Mobile app (React Native)
- Webinars integration (Zoom API)
- Podcast section avec episodes
- Job board (Recruitment section)
- Partner portal
- Multilingual blog (WordPress headless CMS)
- Live chat (Intercom/Drift)
- SMS notifications (Twilio)
- WhatsApp Business integration

### Technical Debt
- Upgrade Django 6.x (quand disponible)
- Migrate to Bun (faster than npm)
- Database sharding (si > 1M records)
- CDN pour static assets (Cloudflare)
- GraphQL API (alternative REST)

---

## Méthodologie Priorisation

**MoSCoW**:
- **MUST** : Critique pour business
- **SHOULD** : Important mais pas bloquant
- **COULD** : Nice-to-have
- **WON'T** : Pas cette année

**T-Shirt Sizing**:
- **S** (Small) : < 1 semaine
- **M** (Medium) : 1-2 semaines
- **L** (Large) : 2-4 semaines
- **XL** (Extra Large) : > 1 mois

**OKRs (Objectives & Key Results)**:
- O1: Devenir leader supply chain consulting Quebec
  - KR1: 10,000 visiteurs/mois
  - KR2: 50 leads qualifiés/mois
  - KR3: Taux conversion 15%

- O2: Excellence opérationnelle
  - KR1: Uptime 99.95%
  - KR2: Temps réponse < 200ms
  - KR3: 0 incidents critiques

- O3: Satisfaction client maximale
  - KR1: NPS score > 70
  - KR2: Support response < 2h
  - KR3: Retention rate > 90%
```

---

## ✅ FINAL : Review Complète et Livraison 100%

#### Tâche 11.10 : Review finale et livraison
**Description** : Validation complète avant livraison

**Actions** :
- [ ] Revue complète checklist 38 tâches
- [ ] Vérification tous tests passent
- [ ] Vérification monitoring actif
- [ ] Documentation complète livrée
- [ ] Formation équipe effectuée
- [ ] Handoff procédures maintenance
- [ ] Célébration 🎉

**Checklist finale** :
```markdown
## ✅ Tests & Qualité
- [ ] Tests frontend : 80%+ coverage
- [ ] Tests backend : 80%+ coverage
- [ ] Tests E2E : 5+ scénarios critiques
- [ ] 0 tests failing
- [ ] Linting 0 erreurs

## ✅ Performance
- [ ] Lighthouse score > 90 (mobile + desktop)
- [ ] Core Web Vitals: All green
- [ ] API response time < 200ms
- [ ] Images optimisées avec blur placeholders

## ✅ Sécurité
- [ ] Rate limiting actif
- [ ] Sentry monitoring actif
- [ ] 0 vulnérabilités critiques
- [ ] HTTPS force
- [ ] Security headers configurés

## ✅ Infrastructure
- [ ] Redis configuré et opérationnel
- [ ] Backups automatiques quotidiens
- [ ] Uptime monitoring actif (UptimeRobot)
- [ ] Healthchecks avancés

## ✅ SEO
- [ ] Google Search Console configuré
- [ ] Sitemap soumis et indexé
- [ ] Structured data validée (Rich Results)
- [ ] Score SEO 90+/100

## ✅ Documentation
- [ ] API_DOCUMENTATION.md complet
- [ ] COMPONENTS.md complet
- [ ] DEPLOYMENT.md complet
- [ ] USER_GUIDE_ADMIN.md complet
- [ ] USER_GUIDE_CRM.md complet
- [ ] ROADMAP_FUTURE.md complet

## ✅ Formation
- [ ] Équipe formée sur Admin Django
- [ ] Équipe formée sur CRM
- [ ] Procédures maintenance documentées
- [ ] Support contact défini

## ✅ Analytics
- [ ] Dashboard insights opérationnel
- [ ] Export CSV/Excel fonctionnel
- [ ] Tracking actif et testé

## ✅ Production
- [ ] Backend déployé et stable
- [ ] Frontend déployé et stable
- [ ] DNS configuré correctement
- [ ] SSL/HTTPS actif
- [ ] Email SMTP opérationnel
```

**Livraison finale** :
- Package complet code source
- Accès repositories GitHub
- Accès admin production
- Documentation complète (8 fichiers)
- Credentials et accès (Render, Vercel, Sentry, etc.)
- Rapport final performances/métriques

**Post-livraison** :
- Support 30 jours (bug fixes)
- Session review 1 mois après lancement
- Assistance évolutions futures (selon roadmap)

---

## 📈 Métriques de Succès

### Objectifs Techniques
| Métrique | Actuel | Objectif | Status |
|----------|--------|----------|--------|
| Test Coverage Frontend | 0% | 80%+ | ⏳ À faire |
| Test Coverage Backend | 40% | 80%+ | ⏳ À faire |
| Performance Score | 85 | 95+ | ⏳ À faire |
| SEO Score | 90 | 95+ | ⏳ À faire |
| Uptime | 99.5% | 99.9%+ | ⏳ À faire |
| API Response Time | 250ms | < 200ms | ⏳ À faire |

### Objectifs Business (3 mois post-launch)
| Métrique | Objectif |
|----------|----------|
| Trafic organique | 5,000 visiteurs/mois |
| Leads qualifiés | 25 leads/mois |
| Taux conversion | 10%+ |
| NPS Score | > 60 |
| Taux rebond | < 50% |
| Durée session avg | > 3 min |

---

## 🎯 Prochaines Actions

1. **Valider ce roadmap** avec stakeholders
2. **Lancer Phase 8** (Tests) dès validation
3. **Review hebdomadaire** de la progression
4. **Ajuster timeline** si nécessaire

---

**Document créé le** : 8 novembre 2025
**Dernière mise à jour** : 8 novembre 2025
**Auteur** : Claude Code
**Version** : 1.0
