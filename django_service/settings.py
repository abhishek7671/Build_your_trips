"""
Django settings for django_service project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("BASE",BASE_DIR)

# import settings from JSON config
PROJECT_SETTINGS_FILE = os.path.join(BASE_DIR, "conf", "config.json")
CUSTOM_SETTINGS_FILE = os.path.join("/etc/django_conf", "config.json")
if os.path.exists(CUSTOM_SETTINGS_FILE):
    JSON_SETTINGS_FILE = CUSTOM_SETTINGS_FILE
else:
    JSON_SETTINGS_FILE = PROJECT_SETTINGS_FILE
JSON_SETTINGS = json.loads(open(JSON_SETTINGS_FILE).read())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'vqua1i2qh8&i!w&mfkeo^uex0v*(u)08x-x!q)ggv!+k94rxxy'
SECRET_KEY='django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    # 'rest_framework_jwt.blacklist',
    'drf_yasg',
    'app',
    'apptrip',
    'django_filters',
    'corsheaders',


    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


 

AUTHENTICATION_BACKENDS = ('app.backend.EmailBackend', )


ROOT_URLCONF = 'django_service.urls'

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

WSGI_APPLICATION = 'django_service.wsgi.application'

1
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'santhosh',
        'ENFORCE_SCHEMA' : False,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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







# LOG_LEVEL = JSON_SETTINGS.get('LOG_LEVEL')
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': 'V1.0.0 %(levelname)s %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s:%(funcName)s %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(asctime)s %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'console': {
#             'level': LOG_LEVEL,
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django_service': {
#             'handlers': ['console'],
#             'level': LOG_LEVEL,
#             'propagate': False,
#         },
#     }
# }




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simpleRe': {
            'format': '%(levelname)s %(asctime)s %(message)s  %(module)s  %(thread)d %(pathname)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },

    },
    'handlers': {
        'file1': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/info.log',
            'formatter': 'simpleRe',
            'delay': True,  # Add this line to delay file creation
        }, 
    },
    'loggers':{
        'django':{
            'handlers':['file1'],
            'level':'DEBUG'

        }    
    },

}





# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'



#SMTP configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'abhisheksuda123@gmail.com'
EMAIL_HOST_PASSWORD = 'yhpo fylx nlgt szib'
DEFAULT_FROM_EMAIL = 'MOURITECH<abhisheksuda123@gmail.com>'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True





