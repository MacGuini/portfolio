import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))


# SECURITY WARNING: don't run with debug turned on in production!
# NOTE environmental variable to control production and development environments
if str(os.environ.get('DEBUG_VALUE')) == "True":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
else:
    DEBUG = False
    ALLOWED_HOSTS = ["brian-lindsay.com", "https://brian-lindsay.com", "https://www.brian-lindsay.com", "https://blindsay-portfolio-nj2bm.ondigitalocean.app/"]
    # FORM SUBMISSION
    # Comment out the following line and place your railway URL, and your production URL in the array.
    CSRF_TRUSTED_ORIGINS = ["https://brian-lindsay.com", "https://www.brian-lindsay.com", "https://brianlindsay.up.railway.app", "https://blindsay-portfolio-nj2bm.ondigitalocean.app"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',
    'forum.apps.ForumConfig',
    
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'accounts.middleware.BlockIPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mysite.context_processors.site_key', # Custom context processor for reCAPTCHA
                'mysite.context_processors.recaptcha_v2_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# use_pgdb allows debuging the PG database while in DEBUG mode
use_pgdb = os.getenv("USE_PGDB")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# if use_pgdb == "True":
#     # # Original Setup
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ["PGDATABASE"],
#             'USER': os.environ["PGUSER"],
#             'PASSWORD': os.environ["PGPASSWORD"],
#             'HOST': os.environ["PGHOST"],
#             'PORT': os.environ["PGPORT"],
#             'OPTIONS': {
#                 'sslmode': 'require',
#             }
#         }
#     }

# else:

#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if use_pgdb == "True":
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# # Testing Database issues
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('GMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASSWORD')

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RECAPTCHA_SITE_KEY = str(os.getenv('RECAPTCHA_PUBLIC_KEY'))
RECAPTCHA_SECRET_KEY = str(os.getenv('RECAPTCHA_PRIVATE_KEY'))

RECAPTCHA_SITE_KEY_V2 = str(os.getenv('RECAPTCHA_PUBLIC_KEY_V2'))
RECAPTCHA_SECRET_KEY_V2 = str(os.getenv('RECAPTCHA_PRIVATE_KEY_V2'))

RECAPTCHA_REQUIRED_SCORE = 0.95


# Session settings
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Security hardening for production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS for 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS

# SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']