import os
from pathlib import Path
import dj_database_url

# -------------------------------
# BASE DIRECTORY
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# SECURITY
# -------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = False
ALLOWED_HOSTS = ['samc-sharp.herokuapp.com', 'www.samc-sharp.com', 'samc-sharp.com']

# Production security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # Only if using HTTPS

# -------------------------------
# INSTALLED APPS
# -------------------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    # Project apps
    'accounts',
    'posts',
    'notifications',
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# URL CONFIGURATION
# -------------------------------
ROOT_URLCONF = 'social_media_api.urls'

# -------------------------------
# TEMPLATES
# -------------------------------
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

# -------------------------------
# WSGI APPLICATION
# -------------------------------
WSGI_APPLICATION = 'social_media_api.wsgi.application'

# -------------------------------
# DATABASE
# -------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override DB for Heroku
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# -------------------------------
# AUTHENTICATION
# -------------------------------
AUTH_USER_MODEL = 'accounts.User'

# -------------------------------
# PASSWORD VALIDATORS
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# INTERNATIONALIZATION
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------
# MEDIA FILES
# -------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------
# REST FRAMEWORK CONFIGURATION
# -------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    ],
}

# -------------------------------
# DEFAULT PRIMARY KEY
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 ["PORT"]