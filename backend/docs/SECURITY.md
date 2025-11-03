# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Pinnacle Advisors, please report it to:
**security@pinnacle-advisors.tech**

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Measures

### Backend Security
- **SECRET_KEY**: Stored in environment variables only (`.env` never committed)
- **Database credentials**: Environment variables only, never hardcoded
- **HTTPS**: Enforced in production (SECURE_SSL_REDIRECT=True)
- **CORS**: Configured for specific origins only
- **SQL Injection**: Protected via Django ORM (no raw queries)
- **XSS Protection**: Django template auto-escaping enabled
- **CSRF Protection**: Django CSRF middleware enabled
- **Password Hashing**: PBKDF2 algorithm with SHA256 hash
- **Admin Access**: Staff/superuser permissions required
- **API Authentication**: Token-based authentication for sensitive endpoints

### Frontend Security
- **Environment Variables**: `NEXT_PUBLIC_*` prefix for client-side only
- **XSS Protection**: React's automatic escaping
- **CSP**: Content Security Policy headers configured
- **HTTPS**: All production traffic encrypted
- **Input Validation**: Client + server-side validation
- **Secure Cookies**: httpOnly and secure flags in production

### Data Protection
- **User Data**: Personal information encrypted at rest
- **Passwords**: Never stored in plain text (Django's built-in hashing)
- **Sessions**: Secure session cookies with SameSite protection
- **File Uploads**: Validated and sanitized (if applicable)
- **Backups**: Daily automated backups of production database

### Dependency Management
- **Regular Updates**: Dependencies updated monthly
- **Vulnerability Scanning**: Automated security audits via GitHub Dependabot
- **CVE Monitoring**: Critical vulnerabilities patched within 48h

## Environment Variables

All sensitive configuration is stored in `.env` files which are **never committed** to version control.

See:
- `backend/.env.example` for required backend variables
- `frontend/.env.example` for required frontend variables

### Required Environment Variables (Production)

**Backend**:
- `SECRET_KEY` - Django secret key (required, no default)
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed domains
- `EMAIL_HOST_PASSWORD` - SMTP password for email notifications
- `CELERY_BROKER_URL` - Redis URL for Celery tasks

**Frontend**:
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Security Best Practices for Contributors

1. **Never commit**:
   - `.env` files
   - Database files (`db.sqlite3`)
   - API keys or tokens
   - Passwords or credentials

2. **Always**:
   - Use environment variables for secrets
   - Sanitize user inputs
   - Validate data on both client and server
   - Use parameterized queries (Django ORM)
   - Keep dependencies up to date

3. **Before committing**:
   - Run `git status` and verify no sensitive files are staged
   - Review your changes for hardcoded secrets
   - Run security linters (flake8, eslint)

## Incident Response

In case of a security incident:

1. **Immediate**: Isolate affected systems
2. **Notify**: Contact security@pinnacle-advisors.tech
3. **Investigate**: Determine scope and impact
4. **Remediate**: Deploy security patches
5. **Communicate**: Notify affected users (if applicable)
6. **Document**: Post-mortem and lessons learned

## Compliance

This project follows:
- OWASP Top 10 security guidelines
- Django security best practices
- Next.js security recommendations
- GDPR principles for data protection (EU users)

## Security Audits

Last security audit: Never (project in development)
Next scheduled audit: Post-production launch

---

**Last updated**: October 30, 2025
**Maintainer**: Pinnacle Advisors Development Team
