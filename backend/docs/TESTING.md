# 🧪 TESTING GUIDE - Pinnacle Advisors

**Documentation complète des tests backend Django**

---

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Structure des tests](#structure-des-tests)
4. [Exécution des tests](#exécution-des-tests)
5. [Coverage](#coverage)
6. [Linting & Formatting](#linting--formatting)
7. [CI/CD](#cicd)
8. [Best Practices](#best-practices)

---

## 🎯 Vue d'ensemble

Le projet Pinnacle Advisors utilise:
- **Django TestCase** pour les tests unitaires
- **pytest-django** (optionnel) pour des fonctionnalités avancées
- **factory-boy** pour les fixtures
- **faker** pour les données de test réalistes
- **coverage** pour mesurer la couverture de code

**Objectif:** >80% de couverture de code

---

## 📦 Installation

### Packages nécessaires

```bash
cd backend
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install coverage factory-boy faker pytest pytest-django
```

Tous les packages sont listés dans `requirements.txt`.

---

## 📁 Structure des tests

```
backend/
├── pytest.ini              # Configuration pytest
├── .coveragerc             # Configuration coverage
├── apps/
│   ├── website/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py       # 25+ tests
│   │       ├── test_serializers.py  # 15+ tests
│   │       ├── test_views.py        # 25+ tests
│   │       └── test_signals.py      # 15+ tests
│   ├── crm/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py       # 35+ tests (auto_qualify!)
│   │       └── test_tasks.py
│   └── analytics/
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py       # 10+ tests
│           └── test_tasks.py
```

**Total:** ~105 tests créés

---

## ▶️ Exécution des tests

### Tests complets

```bash
cd backend

# Tous les tests
python manage.py test apps

# Avec verbosité
python manage.py test apps --verbosity=2

# Tests parallèles (plus rapide)
python manage.py test apps --parallel
```

### Tests par app

```bash
# Website app uniquement
python manage.py test apps.website

# CRM app uniquement
python manage.py test apps.crm

# Analytics app uniquement
python manage.py test apps.analytics
```

### Tests spécifiques

```bash
# Un fichier de test
python manage.py test apps.website.tests.test_models

# Une classe de test
python manage.py test apps.crm.tests.test_models.LeadAutoQualifyTest

# Un test précis
python manage.py test apps.crm.tests.test_models.LeadAutoQualifyTest.test_auto_qualify_hot_lead_ge_budget_urgent
```

---

## 📊 Coverage

### Mesurer la couverture

```bash
cd backend

# Exécuter tests avec coverage
coverage run manage.py test apps

# Rapport dans le terminal
coverage report

# Rapport détaillé (montre les lignes non couvertes)
coverage report --show-missing

# Ignorer les fichiers couverts à 100%
coverage report --skip-covered

# Rapport HTML (navigateur)
coverage html
# Ouvrir: htmlcov/index.html
```

### Configuration coverage

Fichier `.coveragerc`:

```ini
[run]
source = apps
omit =
    */migrations/*
    */tests/*
    */test_*.py
    */__init__.py
    */apps.py
    */admin.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
    raise AssertionError
    raise NotImplementedError
```

### Objectif coverage

- **Website app:** >85%
- **CRM app:** >90% (critical business logic)
- **Analytics app:** >75%
- **Global:** >80%

---

## 🎨 Linting & Formatting

### Black (Formatter)

```bash
cd backend

# Format tout le code
black apps/ config/

# Check seulement (CI/CD)
black --check apps/ config/

# Voir les changements sans appliquer
black --diff apps/
```

**Configuration:** `pyproject.toml`

```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

### Flake8 (Linter)

```bash
cd backend

# Linter tout le code
flake8 apps/ config/

# Avec statistiques
flake8 --statistics apps/

# Générer rapport HTML
flake8 --format=html --htmldir=flake-report apps/
```

**Configuration:** `.flake8`

```ini
[flake8]
max-line-length = 100
ignore = W503, E203, E501
```

### isort (Import sorting)

```bash
cd backend

# Trier les imports
isort apps/ config/

# Check seulement
isort --check-only apps/

# Voir les changements
isort --diff apps/
```

**Configuration:** `pyproject.toml`

```toml
[tool.isort]
profile = "black"
line_length = 100
```

### Workflow complet

```bash
# 1. Format avec Black
black apps/ config/

# 2. Trier les imports
isort apps/ config/

# 3. Linter avec Flake8
flake8 apps/ config/

# 4. Exécuter les tests
python manage.py test apps
```

---

## 🔄 CI/CD

### GitHub Actions

Fichier `.github/workflows/ci.yml` configuré pour:

**Backend:**
1. ✅ Black check
2. ✅ Flake8 linting
3. ✅ isort check
4. ✅ Migrations check
5. ✅ Django tests
6. ✅ Coverage report

**Frontend:**
1. ✅ ESLint
2. ✅ Prettier check
3. ✅ Next.js build

**Déclenchement:**
- Push sur `main` ou `develop`
- Pull requests vers `main` ou `develop`

### Codecov (optionnel)

Pour activer l'upload automatique des rapports de coverage:

1. Créer compte sur [codecov.io](https://codecov.io)
2. Ajouter le repo GitHub
3. Ajouter le token dans GitHub Secrets: `CODECOV_TOKEN`

---

## ✅ Best Practices

### 1. Organisation des tests

```python
# ❌ Mauvais
def test_something():
    # Test qui fait plein de choses

# ✅ Bon
class LeadModelTest(TestCase):
    """Tests for Lead model"""

    def setUp(self):
        """Set up test data"""
        self.lead = Lead.objects.create(...)

    def test_lead_creation(self):
        """Test lead can be created"""
        self.assertIsInstance(self.lead, Lead)

    def test_lead_auto_qualify(self):
        """Test auto-qualification"""
        ...
```

### 2. Nommage des tests

```python
# ❌ Mauvais
def test1():
def testLeads():

# ✅ Bon
def test_lead_creation():
def test_auto_qualify_hot_lead_with_budget():
def test_validation_fails_with_invalid_email():
```

### 3. Assertions claires

```python
# ❌ Mauvais
self.assertTrue(lead.score >= 70)

# ✅ Bon
self.assertGreaterEqual(lead.score, 70)
self.assertEqual(lead.qualification, 'hot')
```

### 4. Isolation des tests

```python
# ✅ Chaque test doit être indépendant
class MyTest(TestCase):
    def setUp(self):
        # Créer des données fraîches pour chaque test
        self.user = User.objects.create(...)

    def test_something(self):
        # Test utilise self.user
        ...

    def test_something_else(self):
        # Test a sa propre version de self.user
        ...
```

### 5. Tests des cas limites

```python
def test_auto_qualify_edge_cases(self):
    """Test edge cases for auto-qualification"""

    # Score exact = 70 (minimum Hot)
    lead1 = Lead.objects.create(score=70, ...)
    self.assertEqual(lead1.qualification, 'hot')

    # Score exact = 69 (maximum Warm)
    lead2 = Lead.objects.create(score=69, ...)
    self.assertEqual(lead2.qualification, 'warm')

    # Score exact = 40 (minimum Warm)
    lead3 = Lead.objects.create(score=40, ...)
    self.assertEqual(lead3.qualification, 'warm')

    # Score = 0
    lead4 = Lead.objects.create(score=0, ...)
    self.assertEqual(lead4.qualification, 'cold')

    # Score > 100 (should be capped)
    lead5 = Lead.objects.create(score=110, ...)
    self.assertEqual(lead5.score, 100)
```

### 6. Mocking

```python
from unittest.mock import patch, MagicMock

@patch('apps.crm.tasks.send_lead_notification_email.delay')
def test_hot_lead_sends_email(self, mock_task):
    """Test Hot lead triggers email task"""

    submission = ContactSubmission.objects.create(...)

    lead = Lead.objects.get(email=submission.email)

    if lead.qualification == 'hot':
        mock_task.assert_called_once_with(lead.id)
```

---

## 📝 Exemples de tests critiques

### Test de l'algorithme auto_qualify()

```python
def test_auto_qualify_hot_lead_complete(self):
    """Test Hot qualification avec tous les critères"""

    lead = Lead.objects.create(
        name="Jean Dupont",
        email="jean@carrefour.fr",
        phone="+33123456789",
        company="Carrefour",
        company_size="ge",  # 30 pts
        position="Directeur SC",
        need_type="transformation digitale",  # 15 pts
        message="urgent " + " ".join(["word"] * 60),  # 15 + 10 pts
        budget_mentioned=True,  # 20 pts
        estimated_budget=Decimal("150000.00")  # +10 pts
    )

    # Total: 30 + 20 + 10 + 15 + 15 + 10 + 10 = 110, capped at 100
    self.assertEqual(lead.score, 100)
    self.assertEqual(lead.qualification, 'hot')
```

### Test des ViewSets API

```python
def test_contact_submission_creates_lead(self):
    """Test POST /api/website/contact/ creates Lead"""

    url = reverse('website:contactsubmission-list')

    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Test message'
    }

    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Check Lead was created via signal
    lead = Lead.objects.get(email='john@example.com')
    self.assertIsNotNone(lead)
```

### Test des Signals

```python
def test_signal_creates_lead_from_submission(self):
    """Test ContactSubmission signal creates Lead"""

    submission = ContactSubmission.objects.create(
        name="Test User",
        email="test@example.com",
        message="Test message"
    )

    # Signal should create Lead automatically
    lead = Lead.objects.get(email="test@example.com")

    self.assertEqual(lead.name, "Test User")
    self.assertTrue(submission.is_processed)
```

---

## 🐛 Debugging tests

### Tests qui échouent

```bash
# Arrêter au premier échec
python manage.py test apps --failfast

# Mode verbeux
python manage.py test apps --verbosity=3

# Garder la base de test pour inspection
python manage.py test apps --keepdb

# Désactiver les migrations (plus rapide)
python manage.py test apps --nomigrations
```

### PDB (Python Debugger)

```python
def test_something(self):
    lead = Lead.objects.create(...)

    import pdb; pdb.set_trace()  # Breakpoint

    self.assertEqual(lead.score, 70)
```

---

## 📞 Support

**Problèmes courants:**

1. **Tests lents:** Utiliser `--parallel` ou `--nomigrations`
2. **Base de test non créée:** Vérifier permissions PostgreSQL
3. **Import errors:** Vérifier `INSTALLED_APPS` et `PYTHONPATH`
4. **Signals non déclenchés:** Vérifier `apps.py` et `ready()`

**Documentation Django Testing:**
- https://docs.djangoproject.com/en/5.0/topics/testing/

**Coverage.py:**
- https://coverage.readthedocs.io/

---

**Dernière mise à jour:** 28 Octobre 2025
**Maintenu par:** Claude Code
