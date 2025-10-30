# Installation de Redis sur Windows

Redis est le message broker utilisé par Celery pour gérer les tâches asynchrones (envoi d'emails, etc.).

## ⚠️ Note Importante

**Le système fonctionne sans Redis** en mode développement grâce au fallback automatique vers l'envoi synchrone d'emails. Redis n'est nécessaire que pour:
- Production avec gros volume de leads
- Tâches asynchrones en arrière-plan
- Optimisation des performances

## Options d'Installation

### Option 1: Redis via WSL2 (Recommandé pour Windows 10/11)

1. **Installer WSL2**
   ```powershell
   wsl --install
   ```

2. **Installer Redis dans WSL2**
   ```bash
   sudo apt-get update
   sudo apt-get install redis-server
   ```

3. **Démarrer Redis**
   ```bash
   sudo service redis-server start
   ```

4. **Tester la connexion**
   ```bash
   redis-cli ping
   # Devrait retourner: PONG
   ```

### Option 2: Memurai (Redis pour Windows natif)

[Memurai](https://www.memurai.com/) est une version native de Redis pour Windows.

1. **Télécharger** Memurai Developer Edition (gratuit)
2. **Installer** avec l'installateur Windows
3. **Démarrer** le service Memurai
4. **Modifier** `.env`:
   ```
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

### Option 3: Redis via Docker

```powershell
# Lancer Redis dans un conteneur Docker
docker run -d -p 6379:6379 --name redis-pinnacle redis:alpine

# Vérifier que Redis fonctionne
docker logs redis-pinnacle
```

### Option 4: Version Portable Redis

Utiliser une version portable non-officielle de Redis pour Windows:

1. Télécharger depuis [tporadowski/redis](https://github.com/tporadowski/redis/releases)
2. Extraire dans un dossier (ex: `C:\Redis`)
3. Lancer `redis-server.exe`

## Configuration de Celery

Une fois Redis installé:

### 1. Vérifier Redis

```bash
redis-cli ping
# Doit retourner: PONG
```

### 2. Démarrer le Worker Celery

```bash
cd backend
venv\Scripts\activate
celery -A config worker -l info --pool=solo
```

**Note Windows**: Utiliser `--pool=solo` car le pool par défaut n'est pas compatible Windows.

### 3. (Optionnel) Démarrer Celery Beat pour tâches périodiques

```bash
celery -A config beat -l info
```

## Tester Celery

Créer un fichier de test:

```python
# backend/test_celery.py
from apps.crm.tasks import send_lead_notification_email

# Envoyer une task
result = send_lead_notification_email.delay(1)  # ID d'un Lead existant
print(f"Task ID: {result.id}")
```

Exécuter:
```bash
python backend/test_celery.py
```

Vérifier dans les logs du worker Celery que la task est exécutée.

## Monitoring Celery (Optionnel)

### Flower - Interface Web pour Celery

```bash
pip install flower
celery -A config flower
```

Puis ouvrir: http://localhost:5555

## Dépannage

### Redis ne démarre pas

**WSL2**:
```bash
sudo service redis-server status
sudo service redis-server restart
```

**Docker**:
```bash
docker ps | grep redis
docker restart redis-pinnacle
```

### Celery ne se connecte pas à Redis

1. Vérifier que Redis écoute sur le bon port:
   ```bash
   redis-cli -h localhost -p 6379 ping
   ```

2. Vérifier la variable d'environnement:
   ```bash
   echo $CELERY_BROKER_URL
   ```

3. Vérifier les logs Celery pour voir l'erreur exacte

### Erreur "pool implementation not available"

Sur Windows, utiliser `--pool=solo`:
```bash
celery -A config worker -l info --pool=solo
```

## Mode Production

En production (Linux/AWS), Redis sera installé normalement:

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Configurer Celery comme service systemd
sudo nano /etc/systemd/system/celery.service
```

Voir `docs/DEPLOYMENT.md` pour la configuration complète de production.

## Références

- [Documentation Celery](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Celery + Django](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- [Running Celery on Windows](https://docs.celeryq.dev/en/stable/getting-started/platforms.html#windows)
