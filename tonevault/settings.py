"""Django settings for tonevault project."""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# insecure default is for local development only — set DJANGO_SECRET_KEY in production
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-siszc^e-a^(p6vkh%k-h@x_4l4c12%40u-4j%c694*k9-8)tt%',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [
    h.strip() for h in
    os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in
    os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'presets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tonevault.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tonevault.wsgi.application'

# PostgreSQL when DATABASE_URL is set (docker compose / production),
# SQLite fallback for simple local usage
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise serves collected static files with compression
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'preset_list'
LOGOUT_REDIRECT_URL = 'preset_list'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# opt-in HTTPS hardening — enable when the site is served over HTTPS
# (kept off by default so plain http://localhost:8000 keeps working)
if os.environ.get('DJANGO_SECURE_SSL', '').lower() in ('1', 'true', 'yes'):
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
