# pyventory\settings.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import cfgpyventory
SECRET_KEY = cfgpyventory.SECRET_KEY
DEBUG = cfgpyventory.DEBUG
TEMPLATE_DEBUG = cfgpyventory.TEMPLATE_DEBUG
ALLOWED_HOSTS = cfgpyventory.ALLOWED_HOSTS
DATABASES = cfgpyventory.DATABASES
STATIC_URL = cfgpyventory.STATIC_URL

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory.application',
    'inventory.category',
    'inventory.domain',
    'inventory.environment',
    'inventory.machine',
    'company',
    'ticket',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pyventory.urls'

WSGI_APPLICATION = 'pyventory.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '_templates'),
)
