# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pinnacle Advisors** is a professional one-page website for a supply chain consulting cabinet featuring:
- **Django Backend** with REST API (DRF)
- **Next.js Frontend** (planned, not yet implemented)
- **Integrated CRM** with automatic lead qualification system (Hot/Warm/Cold)
- **God View Analytics** for comprehensive user tracking
- **Django Admin** for content management with custom theme

**Current Status:** Phase 1 (Backend) complete. Ready for Phase 2 (API REST implementation).

## Key Commands

### Development Server
```bash
cd backend
venv\Scripts\activate  # Windows CMD
python manage.py runserver
```

**Admin:** http://localhost:8000/admin/
**API:** http://localhost:8000/api/

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Django shell for debugging
python manage.py shell
```

### Testing
```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test apps.website
python manage.py test apps.crm
python manage.py test apps.analytics

# Check for issues
python manage.py check
```

### Package Management
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Add new package and update requirements
pip install package-name
pip freeze > backend/requirements.txt
```

## Architecture

### Django Project Structure
```
backend/
├── config/          # Django settings, URLs, WSGI/ASGI
├── apps/
│   ├── core/        # Base functionality
│   ├── website/     # Content management (8 models)
│   ├── crm/         # CRM with auto-qualification (4 models)
│   └── analytics/   # God View tracking (5 models)
├── docs/            # Markdown documentation
├── static/          # Static files
└── media/           # User uploads
```

### Three Django Apps

**1. website app (Content Management):**
- `HeroSection` - Hero section with title/CTA/background
- `Service` - Supply chain services with ordering
- `AboutSection` - Mission/vision/stats
- `TeamMember` - Team profiles with photos
- `FAQCategory` - FAQ categories
- `FAQ` - Questions with `is_published` toggle
- `ContactInfo` - Contact information
- `ContactSubmission` - Contact form submissions (auto-creates Lead)

**2. crm app (Customer Relationship Management):**
- `Lead` - Prospects with **automatic qualification** via `auto_qualify()` method
- `Pipeline` - Sales pipelines
- `Interaction` - Activity history (emails, calls, meetings)
- `Note` - Private/public notes

**3. analytics app (God View Tracking):**
- `UserSession` - Complete session data (device, browser, UTM, duration)
- `PageView` - Page views with scroll depth and time spent
- `Event` - User events with x/y coordinates
- `HeatmapData` - Click heatmap data
- `DailyAnalytics` - Aggregated daily statistics

### Lead Auto-Qualification Algorithm

The CRM's `Lead.auto_qualify()` method scores leads 0-100 based on 6 criteria:

1. **Company Size (30pts):** GE=30, ETI=25, PME=15, TPE=5
2. **Budget (30pts):** Mentioned=20, ≥100k€=+10, ≥50k€=+5
3. **Urgency (15pts):** Keywords: "urgent", "rapidement", "immédiat"
4. **Strategic Need (15pts):** "transformation", "optimisation", "stratégie"
5. **Message Quality (10pts):** >50 words=10, 20-50=5
6. **Complete Info (10pts):** Phone + Company + Position = 10

**Results:**
- 🔥 **Hot (70-100):** Contact within 24h
- ☀️ **Warm (40-69):** Contact within 48-72h
- ❄️ **Cold (0-39):** Nurturing

Detailed documentation: `backend/docs/LEAD_QUALIFICATION.md`

### Django Admin Customization

All models have custom admin classes with:
- **Colored badges** for qualifications (Hot 🔥, Warm ☀️, Cold ❄️)
- **Bulk actions** (publish/unpublish, assign leads, mark status)
- **Inline editing** with `list_editable`
- **Advanced filters** and search
- **Custom displays** using `format_html()`

Theme: `django-admin-interface` with blue/green color scheme

## Important Configuration

### Settings (backend/config/settings.py)
- **Language:** French (fr-fr)
- **Timezone:** Europe/Paris
- **CORS:** Configured for localhost:3000 (Next.js frontend)
- **REST Framework:** Pagination=10, AllowAny permissions (to be restricted)
- **Database:** SQLite (dev), PostgreSQL planned (prod)

### Environment Variables (.env)
```bash
SECRET_KEY=<django-secret-key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Current Work & Next Steps

**Phase 1: Backend Django** ✅ COMPLETE
- All models created and migrated
- Django Admin fully configured
- Documentation complete

**Phase 2: API REST Django** 🔜 IN PROGRESS
- Create serializers for all models (website app done)
- Create ViewSets with proper permissions
- Configure API URLs and routing
- Add OpenAPI/Swagger documentation

See `ROADMAP.md` for complete 11-phase implementation plan.

## Code Patterns

### Model Conventions
- French verbose names for admin interface
- `is_active` boolean for soft deletes
- `order` field for sortable items
- Auto-timestamps with `auto_now`/`auto_now_add`
- Comprehensive help text

### Admin Registration Pattern
```python
@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = (...)
    list_filter = (...)
    search_fields = (...)
    list_editable = (...)
    actions = [...]
```

### Serializer Pattern
Use multiple serializers per model:
- `ModelSerializer` - Standard full serializer
- `ModelDetailSerializer` - With nested relationships
- `ModelPublicSerializer` - Public API (limited fields)
- `ModelCreateSerializer` - For POST requests with validation

### Signal Pattern
Contact form submissions auto-create CRM Leads via Django signals (to be implemented in Phase 6).

## Testing Strategy

Write tests for:
- **Models:** Validation, `auto_qualify()` logic, constraints
- **Serializers:** Field validation, nested data
- **ViewSets:** CRUD operations, permissions, filters
- **Admin actions:** Bulk operations, custom methods

Target: >80% coverage

## File References

Key documentation files:
- `ROADMAP.md` - Complete 11-phase implementation plan
- `backend/README.md` - Backend setup guide
- `backend/README_COMPLETE.md` - Full project vision (30+ pages)
- `backend/PROJECT_STRUCTURE.md` - Directory structure
- `backend/COMMANDS.md` - Command reference (this is comprehensive!)
- `backend/docs/LEAD_QUALIFICATION.md` - Detailed qualification system docs
- `backend/STATUS.md` - Current project state

## Common Issues

### PowerShell Execution Policy
If `venv\Scripts\activate.ps1` fails:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Or use CMD instead of PowerShell.

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Migration Issues
```bash
# View migration status
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate app_name 0001

# Fake migration if DB already in sync
python manage.py migrate --fake
```

## Infrastructure Notes

**Planned deployment:**
- AWS EC2 (Ubuntu Server)
- PostgreSQL database
- Gunicorn + Nginx
- AWS S3 for media files
- SSL/TLS via Let's Encrypt

**Frontend (not yet created):**
- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS (blue/green palette: #3B82F6, #10B981)
- Framer Motion for animations
- Axios + React Query for API

## Design Guidelines

**Colors:**
- Primary Blue: #3B82F6
- Success Green: #10B981
- Hot/Danger Red: #EF4444
- Warm/Warning Orange: #F59E0B

**Inspiration:** n8n.io (modern, animated, one-page scroll design)
**NOT** violet like n8n - use blue/green instead.

## Development Workflow

When creating new Django apps:
```bash
cd backend/apps
python ../manage.py startapp app_name
```

Then:
1. Add to `INSTALLED_APPS` as `'apps.app_name'`
2. Create models with French verbose names
3. Register in admin with custom admin class
4. Create serializers (standard, detail, public, create)
5. Create viewsets with proper permissions
6. Add to API URLs
7. Write tests (models, serializers, viewsets)
8. Update documentation

## Python Path
Use `backend/venv/Scripts/python.exe` for all commands to ensure virtual environment is used.
