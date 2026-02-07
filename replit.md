# MIfolio - Django Portfolio Platform

## Overview
MIfolio is a Django-based portfolio platform that allows users to register and create personalized portfolios. Users can showcase their skills, experiences, education, employment history, projects, and contact information.

## Project Architecture
- **Framework**: Django 4.2 with Python 3.11
- **Database**: PostgreSQL (via Replit's built-in database, accessed through `DATABASE_URL`)
- **Authentication**: django-allauth (username/email-based)
- **Static Files**: WhiteNoise for serving, collected to `staticfiles/`
- **Image Storage**: Cloudinary integration
- **Frontend**: Bootstrap 5, jQuery, Django templates

## Project Structure
```
portfolio/          - Django project settings and configuration
portfolio_app/      - Main application (models, views, forms, templates)
templates/          - Global templates (allauth overrides, base templates)
static/             - Static assets (CSS, JS, images)
staticfiles/        - Collected static files (auto-generated)
documentation/      - Project documentation and screenshots
```

## Key Configuration
- **Settings**: `portfolio/settings.py`
- **URLs**: `portfolio/urls.py`
- **ALLOWED_HOSTS**: Set to `['*']` for development
- **CSRF_TRUSTED_ORIGINS**: Includes `*.replit.dev`, `*.repl.co`, `*.replit.app`
- **DEBUG**: Controlled via `DEBUG` environment variable (defaults to True)

## Running the Project
- **Development**: `python manage.py runserver 0.0.0.0:5000`
- **Production**: `gunicorn --bind=0.0.0.0:5000 portfolio.wsgi`

## Recent Changes
- Configured for Replit environment (ALLOWED_HOSTS, CSRF origins, port 5000)
- Set up PostgreSQL database connection via DATABASE_URL
- Used psycopg2-binary instead of psycopg2 for easier installation
