"""
Django settings for ricerca project.
Generated by 'django-admin startproject' using Django 3.0.8.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# flake8: noqa
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '82^w&ie47r^!c8f6yeui@#6e*myi*o4sf3^u*o7+#3qk!tn^=s'
DEFAULT_HOST = 'localhost'
ALLOWED_HOSTS = ['*']
ADMIN_PATH = 'test_admin'
DATA_DIR = os.path.join(BASE_DIR, "data")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_URL = '/static/'

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'accounts.apps.AccountsConfig',
    'rest_framework',
    'rest_framework.authtoken',

    # 'silk',
   
    # OAS 3 specs
    # 'drf_spectacular',
   
    # frontend apps
    'django_unical_bootstrap_italia',
    'bootstrap_italia_template',
    'organizational_area',
    'generics',
    'esse3',
    'locks',
    'structures',
    'addressbook',
    'advanced_training',
    'cds',
    'companies',
    'patents',
    'phd',
    'pentaho',
    'projects',
    'research_lines',
    'teachers',
    'cds_brochure',
    'cds_websites',
    'research_groups',
    'laboratories',
    'regdid',

    # cors headers
    'corsheaders',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
AUTH_USER_MODEL = 'accounts.User'
LABORATORIES_MEDIA_PATH = f'{MEDIA_URL}laboratori/loghi'
COMPANIES_MEDIA_PATH = f'{MEDIA_URL}spinoff-startup/loghi'
PATENTS_MEDIA_PATH = f'{MEDIA_URL}brevetti/loghi'
CDS_BROCHURE_MEDIA_PATH = f'{MEDIA_URL}cds_media_brochure'
TEACHER_PHOTO_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/foto'
TEACHER_CV_EN_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/cv_en'
TEACHER_CV_ITA_MEDIA_PATH = f'{MEDIA_URL}docenti_pta/cv_ita'
ENCRYPTION_KEY = b'ZQrQunzh7RizTreT3uO1TC3pF1KrLOvZMJsbx1AQIns='

MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # SameSite Cookie workaround
    #  'djangosaml2.middleware.SamlSessionMiddleware'
]

# GETTEXT LOCALIZATION
MIDDLEWARE.append('django.middleware.locale.LocaleMiddleware')
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
#

ROOT_URLCONF = 'ricerca.urls'

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

WSGI_APPLICATION = 'ricerca.wsgi.application'


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# DjangoSAML2 conf
if 'djangosaml2' in INSTALLED_APPS:
    MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
    from saml2_sp.settings import *
    # pySAML2 SP mandatory
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    SAML2_URL_PREFIX = 'saml2'
    LOGIN_URL = f'/{SAML2_URL_PREFIX}/login'
    LOGOUT_URL = f'/{SAML2_URL_PREFIX}/logout'

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'djangosaml2.backends.Saml2Backend',
    )
else:
    LOCAL_URL_PREFIX = 'local'
    LOGIN_URL = f'/{LOCAL_URL_PREFIX}/login/'
    LOGOUT_URL = f'/{LOCAL_URL_PREFIX}/logout/'

LOGOUT_REDIRECT_URL = '/'

PERSON_CONTACTS_TO_TAKE = [
    'Posta Elettronica',
    'Fax',
    'POSTA ELETTRONICA CERTIFICATA',
    'Telefono Cellulare Ufficio',
    'Telefono Ufficio',
    'Riferimento Ufficio',
    'URL Sito WEB',
    'URL Sito WEB Curriculum Vitae']

CURRENT_YEAR = 2023
HIGH_FORMATION_YEAR = 2023
