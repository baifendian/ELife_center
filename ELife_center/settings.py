"""
Django settings for ELife_center project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tvy5*m#lbugm3_b@=s)gb!m%m*c&g!a2j2ikpjbpas$^7&3nnt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_manage',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ELife_center.urls'

WSGI_APPLICATION = 'ELife_center.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
DEFAULT_CHARSET = 'utf-8'
LANGUAGE_CODE = 'zh-hans'
#LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
TEMPLATE_DIRS=(
               'templates',
               'templates/static',
               )
STATICFILES_DIRS = ( 'templates/static', )
STATIC_PATH = os.path.join(BASE_DIR, 'templates/static').replace('\\','/')


########################
#my default parameters 
#######################

#codis address 
CODIS_ADDRESS='172.24.3.175'
CODIS_POET=6380
CODIS_DB=0


#the name of hash in codis

#the name of hash about Goods
GOODS_HASH_NAME='e_live_goods'
#the name of hash about user
USERS_HASH_NAME='e_live_users'
#the name of hash about  log ,using credits to exchange goods
RECORD_HASH_NAME='e_live_record'

#lucky draw use credits num
LUCKY_DRAW_CREDITS=10
