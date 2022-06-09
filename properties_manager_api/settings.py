"""
Django settings for properties_manager_api project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gsi^j*kray(m*ii9*6=r*8d^pkmd-q6i$2hpe#ng$i43h4d2-e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['154.12.240.122', 'localhost', '*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # apps in project
    
    'register',
    'properties',
    'candidates',
    'communications',
    'payments',
    'tickets',
    'fill_db',
    'watson',
    'book_keeping',    
    # third party apps
    
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'drf_yasg',
    
]


CORS_ALLOWED_ORIGINS = [
    "http://154.12.240.122",
    "http://localhost:3000",
    "http://app.kumbio.com"
]


MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'properties_manager_api.urls'

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

WSGI_APPLICATION = 'properties_manager_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd2efrclgtbked6',
        'USER': 'ufbpyoglczgsto',
        'PASSWORD': '8e3e707f3b82ab171ed16d2d42d57dcde2c18e3c8ed0174854a1d396573f4e82',
        'HOST': 'ec2-52-86-56-90.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'd1nb2n9q5k1krj',
#         'USER': 'zkxfekidfxgfnp',
#         'PASSWORD': 'ec3b32d508ff316e08ff392647046beb63867b91aa0e72a38e8ab1fcbb682fc8',
#         'HOST': 'ec2-3-228-235-79.compute-1.amazonaws.com',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ]
# }

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Mountain'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'register.CustomUser'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False



