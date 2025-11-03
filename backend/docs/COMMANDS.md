# 🚀 Commandes Essentielles - Pinnacle Backend

Guide de référence rapide des commandes les plus utilisées.

---

## 🔧 Environnement Virtuel

### Activer venv

**Windows CMD:**
```bash
cd D:\DEV\Pinnacle-website\backend
venv\Scripts\activate.bat
```

**Windows PowerShell** (si erreur):
```powershell
# Solution 1: Utiliser CMD à la place
# Solution 2: Autoriser scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
cd /path/to/Pinnacle-website/backend
source venv/bin/activate
```

### Désactiver venv
```bash
deactivate
```

---

## 📦 Gestion des Packages

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Installer un nouveau package
```bash
pip install nom-du-package
pip freeze > requirements.txt  # Mettre à jour requirements.txt
```

### Mettre à jour pip
```bash
python -m pip install --upgrade pip
```

### Lister les packages installés
```bash
pip list
pip freeze
```

---

## 🗄️ Base de Données

### Créer des migrations
```bash
python manage.py makemigrations
python manage.py makemigrations website  # Pour une app spécifique
```

### Appliquer les migrations
```bash
python manage.py migrate
python manage.py migrate website  # Pour une app spécifique
```

### Voir les migrations
```bash
python manage.py showmigrations
python manage.py showmigrations website  # Par app
```

### Revenir en arrière (rollback)
```bash
python manage.py migrate website 0001  # Revenir à la migration 0001
python manage.py migrate website zero  # Annuler toutes les migrations
```

### Shell base de données
```bash
python manage.py dbshell  # Ouvre le client DB (sqlite3, psql, etc.)
```

### Réinitialiser la base de données (DEV ONLY)
```bash
# ⚠️ ATTENTION: Supprime toutes les données!
rm db.sqlite3
rm -rf apps/*/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 👤 Utilisateurs

### Créer un superutilisateur
```bash
python manage.py createsuperuser
# Suivre les prompts: username, email, password
```

### Changer le mot de passe
```bash
python manage.py changepassword username
```

### Créer un utilisateur via shell
```python
python manage.py shell

from django.contrib.auth.models import User
user = User.objects.create_user('username', 'email@example.com', 'password')
user.is_staff = True  # Pour accès admin
user.is_superuser = True  # Pour superuser
user.save()
exit()
```

---

## 🌐 Serveur de Développement

### Lancer le serveur
```bash
python manage.py runserver
# Par défaut: http://127.0.0.1:8000/
```

### Port personnalisé
```bash
python manage.py runserver 8080
python manage.py runserver 0.0.0.0:8000  # Accessible sur réseau local
```

### Avec script (Windows)
```bash
start.bat
```

### Avec script (Linux/Mac)
```bash
./start.sh
```

### Arrêter le serveur
```
Ctrl + C
```

---

## 🔍 Vérification & Debugging

### Vérifier la configuration
```bash
python manage.py check
python manage.py check --deploy  # Vérifications production
```

### Shell Django interactif
```bash
python manage.py shell

# Exemples dans le shell:
from apps.website.models import Service
Service.objects.all()
Service.objects.create(title="Nouveau service", description="...")

from apps.crm.models import Lead
Lead.objects.filter(qualification='hot').count()

exit()
```

### Shell Django avec IPython (meilleur)
```bash
pip install ipython
python manage.py shell
# Autocomplétion améliorée, highlighting, etc.
```

### Afficher les requêtes SQL
```python
python manage.py shell

from django.conf import settings
settings.DEBUG = True

from apps.website.models import Service
services = Service.objects.all()
print(services.query)  # Affiche la requête SQL

exit()
```

---

## 📁 Fichiers Statiques

### Collecter les fichiers statiques
```bash
python manage.py collectstatic
# Copie tous les fichiers static/ vers staticfiles/
```

### Collecter sans confirmation
```bash
python manage.py collectstatic --noinput
```

### Trouver un fichier statique
```bash
python manage.py findstatic nom_fichier.css
```

### Effacer les fichiers collectés
```bash
python manage.py collectstatic --clear --noinput
```

---

## 🧪 Tests

### Lancer tous les tests
```bash
python manage.py test
```

### Tests d'une app spécifique
```bash
python manage.py test apps.website
python manage.py test apps.crm
python manage.py test apps.analytics
```

### Tests d'un fichier spécifique
```bash
python manage.py test apps.website.tests.test_models
```

### Tests avec verbosity
```bash
python manage.py test --verbosity=2
```

### Coverage (installer d'abord)
```bash
pip install coverage

coverage run manage.py test
coverage report
coverage html  # Génère rapport HTML dans htmlcov/
```

---

## 📊 Django Admin

### Accéder à l'admin
```
http://localhost:8000/admin/
```

### Enregistrer un modèle dans l'admin
```python
# apps/nom_app/admin.py

from django.contrib import admin
from .models import MonModele

@admin.register(MonModele)
class MonModeleAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')
    list_filter = ('field3',)
    search_fields = ('field1', 'field2')
```

---

## 🔐 Variables d'Environnement

### Lire le .env
```python
python manage.py shell

from decouple import config
secret = config('SECRET_KEY')
debug = config('DEBUG', cast=bool)
print(secret, debug)

exit()
```

### Générer une SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Vérifier les variables
```bash
python manage.py shell

from django.conf import settings
print(settings.SECRET_KEY)
print(settings.DEBUG)
print(settings.ALLOWED_HOSTS)

exit()
```

---

## 📤 Import/Export Données

### Exporter données en JSON
```bash
python manage.py dumpdata > backup.json
python manage.py dumpdata website > website_backup.json
python manage.py dumpdata website.Service --indent 2 > services.json
```

### Importer données depuis JSON
```bash
python manage.py loaddata backup.json
python manage.py loaddata services.json
```

### Exporter en CSV (via admin)
```
1. Aller dans Django Admin
2. Sélectionner les objets
3. Choisir action "Export selected items"
4. Choisir format CSV
```

---

## 🎨 Django Admin Interface

### Configurer le thème
```bash
python manage.py shell

from admin_interface.models import Theme
theme = Theme.objects.first()
theme.title = "Pinnacle Advisors"
theme.title_color = "#3B82F6"  # Bleu
theme.save()

exit()
```

### Réinitialiser le thème
```bash
python manage.py loaddata admin_interface_theme_bootstrap.json
```

---

## 🔄 Celery (Tâches Asynchrones)

### Lancer worker Celery
```bash
celery -A config worker -l info
```

### Lancer beat (tâches planifiées)
```bash
celery -A config beat -l info
```

### Lancer ensemble (dev uniquement)
```bash
celery -A config worker -B -l info
```

### Flower (monitoring Celery)
```bash
pip install flower
celery -A config flower
# Accès: http://localhost:5555
```

---

## 📝 Logs & Debugging

### Voir les logs en temps réel
```bash
python manage.py runserver --verbosity 2
```

### Activer logging SQL
```python
# Dans settings.py (dev uniquement)

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## 🚀 Production

### Collecter static + migrate
```bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

### Lancer avec Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Gunicorn avec workers
```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Check déploiement
```bash
python manage.py check --deploy
```

---

## 🗑️ Nettoyage

### Supprimer fichiers .pyc
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### Nettoyer sessions expirées
```bash
python manage.py clearsessions
```

---

## 📚 Documentation

### Générer liste des URLs
```bash
python manage.py show_urls  # Si django-extensions installé
```

### Modèles et champs
```bash
python manage.py inspectdb  # Génère models.py depuis DB existante
```

---

## 🔗 URLs Importantes

```
Site:           http://localhost:8000/
Admin:          http://localhost:8000/admin/
API Root:       http://localhost:8000/api/
Health Check:   http://localhost:8000/api/health/
```

---

## 💡 Astuces

### Alias utiles (ajouter au .bashrc ou .zshrc)
```bash
alias dj="python manage.py"
alias djrun="python manage.py runserver"
alias djmm="python manage.py makemigrations"
alias djm="python manage.py migrate"
alias djsh="python manage.py shell"
alias djsu="python manage.py createsuperuser"
```

### Utilisation avec alias
```bash
dj check
djrun
djmm website
djm
```

---

## 🆘 Dépannage

### Erreur "No module named X"
```bash
pip install X
# ou
pip install -r requirements.txt
```

### Erreur "table doesn't exist"
```bash
python manage.py migrate
```

### Erreur "SECRET_KEY"
```bash
# Vérifier que .env existe et contient SECRET_KEY
cat .env
# Si manquant:
python -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())" >> .env
```

### Port déjà utilisé
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Migrations incohérentes
```bash
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

---

*Dernière mise à jour: 27/10/2025*
*Pour plus d'infos: Consulter la documentation Django officielle*
