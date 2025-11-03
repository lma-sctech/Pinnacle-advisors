# Guide de Déploiement - Render.com

**Date de création:** 30 Octobre 2025
**Version:** 1.0
**Projet:** Pinnacle Advisors Website

---

## Vue d'ensemble

Ce guide vous accompagne étape par étape pour déployer:
- **Backend Django** sur Render.com (gratuit avec limitations)
- **Frontend Next.js** sur Vercel (gratuit)
- **PostgreSQL** database (gratuit 90 jours)
- **Redis** cache (gratuit 25MB)

**Coût total:** $0/mois (avec limitations free tier)

---

## Prérequis

✅ Compte GitHub avec repository **Pinnacle-advisors** pushé
✅ Compte Render.com créé (https://render.com)
✅ Compte Vercel créé (https://vercel.com)
✅ Compte Cloudinary (optionnel, pour media files) - https://cloudinary.com

---

## Table des matières

1. [Préparation Locale](#1-préparation-locale)
2. [Déploiement Backend sur Render](#2-déploiement-backend-sur-render)
3. [Configuration Base de Données](#3-configuration-base-de-données)
4. [Configuration Redis](#4-configuration-redis)
5. [Configuration Variables d'Environnement](#5-configuration-variables-denvironnement)
6. [Déploiement Frontend sur Vercel](#6-déploiement-frontend-sur-vercel)
7. [Post-Déploiement](#7-post-déploiement)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Préparation Locale

### 1.1 Vérifier que tous les fichiers sont pushés

```bash
cd D:\DEV\Pinnacle-website
git status
git log --oneline -5
```

**Vérifier la présence de:**
- `render.yaml` (racine)
- `backend/build.sh`
- `backend/requirements.txt` (avec gunicorn, whitenoise, dj-database-url)
- `.env.render.example`

### 1.2 Tester localement (optionnel)

```bash
cd backend
venv\Scripts\activate
python manage.py check
python manage.py test apps
```

---

## 2. Déploiement Backend sur Render

### 2.1 Connexion à Render.com

1. Aller sur https://dashboard.render.com
2. Se connecter avec GitHub
3. Click **"New +"** → **"Blueprint"**

### 2.2 Créer depuis Blueprint (Infrastructure as Code)

1. **Select Repository:** `lma-sctech/Pinnacle-advisors`
2. **Branch:** `main`
3. **Blueprint:** `render.yaml` (auto-détecté)
4. Click **"Apply"**

**Render va créer automatiquement:**
- Web Service: `pinnacle-backend`
- Worker Service: `pinnacle-celery-worker`
- PostgreSQL Database: `pinnacle-db`
- Redis: `pinnacle-redis`

⏱️ **Durée:** 5-10 minutes (premier déploiement)

### 2.3 Vérifier les services créés

Dashboard Render → Vous devriez voir:
- ✅ `pinnacle-backend` (Web Service) - **Building...**
- ✅ `pinnacle-celery-worker` (Worker) - **Waiting...**
- ✅ `pinnacle-db` (PostgreSQL) - **Available**
- ✅ `pinnacle-redis` (Redis) - **Available**

---

## 3. Configuration Base de Données

### 3.1 Vérifier PostgreSQL

Dashboard → `pinnacle-db` → **Info**

**Vérifier:**
- Status: ✅ Available
- Plan: Free
- Region: Frankfurt (ou votre choix)
- Connections: External/Internal URLs disponibles

### 3.2 La variable DATABASE_URL est auto-configurée

Render link automatiquement la database au web service via `DATABASE_URL`.

**Pas d'action requise!** ✅

---

## 4. Configuration Redis

Dashboard → `pinnacle-redis` → **Info**

**Vérifier:**
- Status: ✅ Available
- Plan: Free (25MB)
- Maxmemory Policy: allkeys-lru

**La variable REDIS_URL est auto-configurée.**

---

## 5. Configuration Variables d'Environnement

### 5.1 Accéder aux variables

Dashboard → `pinnacle-backend` (Web Service) → **Environment**

### 5.2 Variables déjà configurées (par render.yaml)

✅ `DATABASE_URL` - Auto (depuis PostgreSQL)
✅ `REDIS_URL` - Auto (depuis Redis)
✅ `RENDER` - true
✅ `PYTHON_VERSION` - 3.11.9
✅ `WEB_CONCURRENCY` - 2

### 5.3 Variables à configurer manuellement

Cliquer **"Add Environment Variable"** pour chacune:

#### SECRET_KEY (CRITIQUE!)

Générer une nouvelle clé:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copier le résultat dans Render:
- Key: `SECRET_KEY`
- Value: `<votre-clé-générée>`

#### ALLOWED_HOSTS

Format: domaines séparés par virgules

- Key: `ALLOWED_HOSTS`
- Value: `pinnacle-backend.onrender.com`

*(Ajouter votre domaine custom si vous en avez un)*

#### CORS_ALLOWED_ORIGINS

Votre frontend Vercel (vous l'obtiendrez après déploiement Vercel, revenir ici après)

- Key: `CORS_ALLOWED_ORIGINS`
- Value: `https://pinnacle-advisors.vercel.app`

*(Remplacer par votre vraie URL Vercel)*

#### EMAIL Configuration (SMTP)

**Gmail exemple (avec App Password):**

1. Créer App Password Gmail: https://myaccount.google.com/apppasswords

2. Ajouter les variables:
   - `EMAIL_HOST` = `smtp.gmail.com`
   - `EMAIL_PORT` = `587`
   - `EMAIL_USE_TLS` = `True`
   - `EMAIL_HOST_USER` = `votre-email@gmail.com`
   - `EMAIL_HOST_PASSWORD` = `votre-app-password`

**Alternative:** SendGrid, AWS SES, Mailgun, etc.

#### Autres variables (optionnelles)

- `CRM_NOTIFICATION_EMAILS` = `contact@pinnacle-advisors.tech`
- `DEFAULT_FROM_EMAIL` = `noreply@pinnacle-advisors.tech`
- `DJANGO_LOG_LEVEL` = `WARNING`

### 5.4 Sauvegarder et redéployer

Click **"Save Changes"** en haut → Render redéploie automatiquement

---

## 6. Déploiement Frontend sur Vercel

### 6.1 Connexion à Vercel

1. Aller sur https://vercel.com/dashboard
2. Se connecter avec GitHub
3. Click **"Add New..."** → **"Project"**

### 6.2 Import Repository

1. **Select Repository:** `lma-sctech/Pinnacle-advisors`
2. Click **"Import"**

### 6.3 Configuration projet

**Framework Preset:** Next.js (auto-détecté) ✅

**Root Directory:** `frontend` ⚠️ IMPORTANT!

**Build Command:** `npm run build` (défaut)

**Output Directory:** `.next` (défaut)

**Install Command:** `npm install` (défaut)

### 6.4 Environment Variables

Click **"Environment Variables"** puis ajouter:

| Key | Value | Environment |
|-----|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://pinnacle-backend.onrender.com` | Production |

*(Remplacer par votre vraie URL Render backend)*

**Note:** Vercel préfixe automatiquement avec `https://`

### 6.5 Déployer

Click **"Deploy"** → ⏱️ 2-3 minutes

**Résultat:** URL Vercel générée: `https://pinnacle-advisors.vercel.app`

### 6.6 Retour sur Render - Configurer CORS

Maintenant que vous avez l'URL Vercel:

1. Render Dashboard → `pinnacle-backend` → **Environment**
2. Modifier `CORS_ALLOWED_ORIGINS`:
   - Value: `https://pinnacle-advisors.vercel.app`
3. **Save** → Redéploiement automatique

---

## 7. Post-Déploiement

### 7.1 Créer un superutilisateur Django

Render Dashboard → `pinnacle-backend` → **Shell**

```bash
cd backend
python manage.py createsuperuser
```

Suivre les prompts:
- Username: `admin`
- Email: `admin@pinnacle-advisors.tech`
- Password: ********

### 7.2 Vérifier l'API

**Health Check:**
```
https://pinnacle-backend.onrender.com/api/health/
```

Devrait retourner: `{"status": "ok"}`

**API Root:**
```
https://pinnacle-backend.onrender.com/api/
```

**Django Admin:**
```
https://pinnacle-backend.onrender.com/admin/
```

Se connecter avec superuser créé

### 7.3 Peupler la base de données

Via Django Admin ou Shell Render:

```bash
cd backend
python scripts/populate_content.py
python scripts/seed/create_seo_settings.py
python scripts/seed/create_site_settings.py
```

### 7.4 Tester le frontend

Aller sur: `https://pinnacle-advisors.vercel.app`

**Vérifier:**
- ✅ Page charge correctement
- ✅ Hero section affichée
- ✅ Services chargés depuis API
- ✅ FAQ section fonctionne
- ✅ Formulaire contact fonctionne

### 7.5 Configurer UptimeRobot (Anti-Sleep)

Render Free tier sleep après 15min inactivité.

**Solution:** UptimeRobot ping toutes les 5min

1. Créer compte: https://uptimerobot.com (gratuit)
2. Click **"Add New Monitor"**
3. Type: **HTTP(s)**
4. URL: `https://pinnacle-backend.onrender.com/api/health/`
5. Interval: **5 minutes**
6. Alert: Email ou SMS (optionnel)
7. **Create Monitor**

✅ Votre backend reste éveillé 24/7!

---

## 8. Troubleshooting

### Erreur: Build Failed

**Symptôme:** Render build échoue

**Solutions:**
1. Vérifier `backend/build.sh` est présent
2. Vérifier permissions: `chmod +x backend/build.sh`
3. Vérifier `requirements.txt` contient toutes les dépendances
4. Logs Render → identifier la ligne d'erreur exacte

### Erreur: Database Connection

**Symptôme:** `OperationalError: could not connect to server`

**Solutions:**
1. Vérifier PostgreSQL service est **Available**
2. Vérifier `DATABASE_URL` est bien configurée
3. Dashboard → `pinnacle-db` → **Connections** → Copier Internal URL
4. Tester connexion via Shell Render

### Erreur: Static Files 404

**Symptôme:** Admin CSS manquant

**Solutions:**
1. Vérifier WhiteNoise est dans `MIDDLEWARE`
2. Render Shell: `python manage.py collectstatic --noinput`
3. Vérifier `STATIC_ROOT` = `BASE_DIR / 'staticfiles'`
4. Redéployer

### Erreur: CORS Blocked

**Symptôme:** Frontend ne peut pas appeler API

**Solutions:**
1. Vérifier `CORS_ALLOWED_ORIGINS` contient URL Vercel exacte
2. Vérifier HTTPS (pas HTTP)
3. Browser Console → voir erreur CORS exacte
4. settings.py → vérifier `corsheaders.middleware.CorsMiddleware` présent

### Erreur: Celery Worker Crashed

**Symptôme:** Worker status: **Failed**

**Solutions:**
1. Vérifier Redis est **Available**
2. Logs Worker → identifier erreur
3. Vérifier `REDIS_URL` configurée
4. Si gratuit tier épuisé: désactiver worker temporairement

### Frontend 404 sur routes

**Symptôme:** Rafraîchir page → 404

**Solution:**
Vercel Dashboard → `pinnacle-advisors` → **Settings** → **Rewrites**

Ajouter:
- Source: `/(.*)`
- Destination: `/`

### Build timeout Render

**Symptôme:** Build dépasse 15 minutes

**Solutions:**
1. Optimiser `requirements.txt` (retirer dev dependencies)
2. Build localement: vérifier durée
3. Upgrade Render tier si nécessaire

---

## 9. Limitations Free Tier

### Render Free

| Limitation | Impact | Solution |
|-----------|--------|----------|
| Sleep après 15min | Cold start ~30-60s | UptimeRobot ping |
| 750h runtime/mois | Suffisant 1 service | Activer worker si besoin |
| PostgreSQL 90 jours | Database expire | Renouveler ou upgrade |
| Build time 15min | Build long échoue | Optimiser build |
| Pas persistent disk | Media uploads perdus | Cloudinary |

### Vercel Free

| Limitation | Impact | Solution |
|-----------|--------|----------|
| 100GB bandwidth/mois | Traffic élevé | Upgrade si dépassé |
| Build time 45min | Build long échoue | Optimiser |

---

## 10. Upgrade Payant (Si nécessaire)

### Render Paid Tiers

**Starter ($7/mois par service):**
- Pas de sleep
- PostgreSQL permanent
- 1GB RAM
- Recommend si traffic régulier

**Standard ($25/mois):**
- 4GB RAM
- Auto-scaling
- Production-ready

### Vercel Pro ($20/mois)

- Bandwidth illimité
- Advanced analytics
- Team collaboration

---

## 11. Maintenance

### Mettre à jour le code

**Backend:**

1. Push sur GitHub:
   ```bash
   git add .
   git commit -m "Update: description"
   git push origin main
   ```

2. Render redéploie automatiquement! ✅

**Frontend:**

Push sur GitHub → Vercel redéploie automatiquement! ✅

### Migrations database

Render Shell:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

Ou push migration files → build.sh les applique automatiquement

### Monitoring

- **Render Logs:** Dashboard → Service → **Logs**
- **Vercel Logs:** Dashboard → Deployment → **Logs**
- **UptimeRobot:** Email alerts si down

---

## 12. Sécurité

### Variables sensibles

❌ **Ne JAMAIS commiter:**
- `.env`
- `SECRET_KEY` réelle
- Passwords SMTP
- API keys

✅ **Toujours utiliser:**
- Render Environment Variables
- GitHub Secrets (pour CI/CD)
- `.env.example` pour documentation

### HTTPS

✅ Render et Vercel forcent HTTPS automatiquement

### Backups

**PostgreSQL:**

Render Dashboard → `pinnacle-db` → **Backups**

Free tier: Pas de backups automatiques ⚠️

**Solution manuelle:**

```bash
# Render Shell
pg_dump DATABASE_URL > backup.sql
# Download backup.sql
```

**Recommandation:** Cron job hebdomadaire

---

## 13. Domaine Custom (Optionnel)

### Configurer domaine sur Render

1. Acheter domaine (Namecheap, OVH, etc.)
2. Render Dashboard → `pinnacle-backend` → **Settings** → **Custom Domain**
3. Ajouter: `api.yourdomain.com`
4. Suivre instructions DNS (CNAME record)

### Configurer domaine sur Vercel

1. Vercel Dashboard → `pinnacle-advisors` → **Settings** → **Domains**
2. Ajouter: `www.yourdomain.com` et `yourdomain.com`
3. Suivre instructions DNS

### Mettre à jour CORS

Après domaine configuré:

Render → Environment → `CORS_ALLOWED_ORIGINS`:
```
https://yourdomain.com,https://www.yourdomain.com
```

---

## Support

**Render Docs:** https://render.com/docs
**Vercel Docs:** https://vercel.com/docs
**Django Deployment:** https://docs.djangoproject.com/en/stable/howto/deployment/

**Problème persiste?** Consulter logs détaillés ou contacter support platforms.

---

**Guide créé le:** 30 Octobre 2025
**Dernière mise à jour:** 30 Octobre 2025
**Version:** 1.0
**Auteur:** Claude Code
