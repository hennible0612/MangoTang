"""
Django settings for MangoTang project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '...'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [] 나중에 고정 아이피 입력


# Application definition

INSTALLED_APPS = [

    'store.apps.StoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_crontab',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.google',
]
# CRONJOBS = [
#     ('* * * * *','MangoTang.cron.every_minute','>> /logs/criticall.log')
# ]

imp_key = '...'
imp_secret = "..."

naver_client_id = '...'
naver_client_secret = '...'
sweet_tracker_key = '...'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MangoTang.urls'
# X_FRAME_OPTIONS = 'SAMEORIGIN'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'MangoTang.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/product_image/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/product_image')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# 로깅설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {  # asctime : 현재 시간 #levelname: 로그의 레벨 #name 로거명 #message 출력내용
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },

        'file': {
            'level': 'INFO',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',  # 5메가 이상 넘어가면 파일뒤에 index를 붙여 백업
            'filename': BASE_DIR / 'logs/mysite.log',
            'maxBytes': 1024 * 1024 * 5,  # 5메가
            'backupCount': 5,  # 백업 최대 개수
            'formatter': 'standard',  # format은 standard 사용
        },
        'critical_file': {
            'level': 'CRITICAL',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',  # 5메가 이상 넘어가면 파일뒤에 index를 붙여 백업
            'filename': BASE_DIR / 'logs/critical.log',
            'maxBytes': 1024 * 1024 * 5,  # 5메가
            'backupCount': 5,  # 백업 최대 개수
            'formatter': 'standard',  # format은 standard 사용
        },
        'error_file': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',  # 5메가 이상 넘어가면 파일뒤에 index를 붙여 백업
            'filename': BASE_DIR / 'logs/error.log',
            'maxBytes': 1024 * 1024 * 5,  # 5메가
            'backupCount': 5,  # 백업 최대 개수
            'formatter': 'standard',  # format은 standard 사용
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'critical_file', 'file','error_file'],
            'level': 'INFO',  # info 이상의 레벨만 출력력
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'store': {
            'handlers': ['console', 'file', 'critical_file','error_file'],
            'level': 'INFO'
        },
    }
}

SITE_ID = 1
