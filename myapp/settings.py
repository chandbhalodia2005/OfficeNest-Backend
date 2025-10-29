"""
Django settings for OfficeNest project (deployment-ready).
"""

import os
from pathlib import Path
import dj_database_url

# ----------------------------
# PATHS
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# BASIC SETTINGS
# ----------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-local-dev-secret')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'officenest-backend.onrender.com',  # ← your Render backend URL
]

# ----------------------------
# APPLICATIONS
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Your apps
    'myapp',
]

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OfficeNest.urls'  # ✅ Make sure this matches your project folder name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OfficeNest.wsgi.application'  # ✅ Matches your project folder

# ----------------------------
# DATABASE
# ----------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ----------------------------
# REST FRAMEWORK
# ----------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

# ----------------------------
# MEDIA FILES
# ----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------
# STATIC FILES
# ----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compression for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ----------------------------
# CORS SETTINGS
# ----------------------------
CORS_ALLOWED_ORIGINS = [
    "https://officenest.netlify.app",   # your Netlify frontend
    "http://localhost:3000",            # local dev
    "http://127.0.0.1:5173",            # Vite local dev
]

# If you want to temporarily allow all origins during testing:
# CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------
# SECURITY
# ----------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://officenest.netlify.app",
    "https://officenest-backend.onrender.com",
]

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ----------------------------
# DEFAULT PRIMARY KEY FIELD
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
