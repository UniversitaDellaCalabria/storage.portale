import pathlib
import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE=True
# SESSION_COOKIE_AGE = 60 * 10 # minutes

# the path corresponding the admin backend, default if not defined: admin/
ADMIN_PATH = 'admin_path'

DEFAULT_HOST = ''
ALLOWED_HOSTS = [DEFAULT_HOST, '*']
CSRF_TRUSTED_ORIGINS = [f'https://{DEFAULT_HOST}']
AUTH_USER_MODEL = 'accounts.User'

DATA_DIR = os.path.join(BASE_DIR, "data")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
if not os.path.exists(STATIC_ROOT):
    pathlib.Path(STATIC_ROOT).mkdir(parents=True, exist_ok=True)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',

    # cors headers
    'corsheaders.middleware.CorsMiddleware',

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

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ricerca_app',
    'rangefilter',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',
    # OAS 3 specs
    #  'drf_spectacular',
    'corsheaders',

    'django_ckeditor_5',

    # frontend apps
    'django_unical_bootstrap_italia',
    'bootstrap_italia_template',
    'organizational_area',
    'crud.utils',
    'crud.cds',
    'crud.companies',
    'crud.patents',
    'crud.phd',
    'crud.projects',
    'crud.research_groups',
    'crud.research_lines',
    'crud.teachers',
    'crud.cds_websites_brochure',
    'crud.cds_websites_pages',
    'crud.laboratories',
    'crud.regdid',

    # SAML2
    # 'djangosaml2',
    # 'saml2_sp'
    ]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# API
# REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    # OAS 3 specs
  #   'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi_agid.AgidAutoSchema',
  #   'DEFAULT_PARSER_CLASSES': [
  #       'rest_framework.parsers.OAS3JSONParser',
        #  'rest_framework.parsers.JSONParser',
        #  'rest_framework.parsers.FormParser',
        #  'rest_framework.parsers.MultiPartParser',
#    ],
#}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '1000/day'
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'host',
        'NAME': 'db_name',
        'USER': 'user',
        'PASSWORD': 'password',
        'PORT': '',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
    },
}

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# custom date/datetime format
DEFAULT_DATE_FORMAT = '%d/%m/%Y'
DEFAULT_TIME_FORMAT = '%H:%M'
DEFAULT_DATETIME_FORMAT = f'{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}'

# override globals
DATE_INPUT_FORMATS = [DEFAULT_DATE_FORMAT, '%Y-%m-%d']
DATETIME_INPUT_FORMATS = [DEFAULT_DATETIME_FORMAT, f'%Y-%m-%d {DEFAULT_TIME_FORMAT}']

# for javascript datepickers
# BootstrapItalia datepicker
JS_DEFAULT_DATE_FORMAT = "dd/MM/yyyy"
# Cutstom datetimepicker
JS_DEFAULT_DATETIME_FORMAT = 'DD/MM/YYYY HH:mm'

# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# email notification on error 500
DEFAULT_FROM_EMAIL = 'dummy_email'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = 'smtp_host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = []

OAS3_CONFIG = {'title': "Unical - Ricerca",
               # 'permission_classes': (permissions.AllowAny,),
               'description': "OpenData per la Ricerca in Unical",
               'termsOfService': 'https://tos.unical.it',
               'x-api-id': '00000000-0000-0000-0000-000000000024',
               'x-summary': "OpenData per la Ricerca in Unical",
               'license': dict(name='apache2',
                               url='http://www.apache.org/licenses/LICENSE-2.0.html'),
               'servers': [dict(description='description',
                                url='https://storage.portale.unical.it'),
                           dict(description='description',
                                url='https://ricerca.unical.it')],
               'tags': [dict(description='description',
                             name='api'),
                        dict(description='description',
                             name='public')],
               'contact': dict(email = 'giuseppe.demarco@unical.it',
                               name = 'Giuseppe De Marco',
                               url = 'https://github.com/UniversitaDellaCalabria'),
               'version': "0.1.2"
}


# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'detailed': {
            'format': '[%(asctime)s] %(message)s [(%(levelname)s)] %(name)s.%(funcName)s:%(lineno)s]'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'formatter': 'detailed',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'formatter': 'detailed',
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'ricerca': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.utils': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.cds': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.companies': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.patents': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.phd': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.projects': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.research_groups': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.research_lines': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.teachers': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'crud.laboratories': {
             'handlers': ['console'],
             'level': 'DEBUG',
             'propagate': False,
        },
        'crud.cds_websites_brochure': {
             'handlers': ['console'],
             'level': 'DEBUG',
             'propagate': False,
        },
        'crud.cds_websites_pages': {
             'handlers': ['console', 'mail_admins'],
             'level': 'DEBUG',
             'propagate': False,
        },
    }
}

LABORATORIES_MEDIA_PATH = f'{MEDIA_URL}portale/laboratori/loghi'
COMPANIES_MEDIA_PATH = f'{MEDIA_URL}portale/spinoff-startup/loghi'
PATENTS_MEDIA_PATH = f'{MEDIA_URL}portale/brevetti/loghi'
CDS_BROCHURE_MEDIA_PATH = f'{MEDIA_URL}portale/cds_media_brochure'
TEACHER_PHOTO_MEDIA_PATH = f'{MEDIA_URL}portale/docenti_pta/foto'
TEACHER_CV_EN_MEDIA_PATH = f'{MEDIA_URL}portale/docenti_pta/cv_en'
TEACHER_CV_IT_MEDIA_PATH = f'{MEDIA_URL}portale/docenti_pta/cv_ita'

ENCRYPTION_KEY = b'key'

DJANGO_BOOSTRAP_ITALIA_USE_CDN = True

# SECURITY
SAML_SESSION_COOKIE_NAME = 'cookie_name'
X_FRAME_OPTIONS = 'SAMEORIGIN'
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
CSRF_COOKIE_HTTPONLY = True

# DjangoSAML2 conf
if 'djangosaml2'  in INSTALLED_APPS:
    MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
    from saml2_sp.settings import *
    # pySAML2 SP mandatory
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True

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

LOGOUT_REDIRECT_URL=f'/'

UNICMS_AUTH_TOKEN = 'secret_token'
UNICMS_ROOT_URL = 'root_url'
UNICMS_PUBLICATION_API_URL = UNICMS_ROOT_URL + '/api/publications/{}/?format=json'
UNICMS_WEBPATH_API_URL = UNICMS_ROOT_URL + '/api/webpaths/{}/?format=json'

UNICMS_OBJECT_API = {'Publication': UNICMS_PUBLICATION_API_URL,
                     'WebPath': UNICMS_WEBPATH_API_URL}


# University Planner
KEY_API_UP =''
UTENTE_API_UP =''
PASSWORD_API_UP =''
URL_UP_API = 'https://unical.prod.up.cineca.it/api/'

# cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# ck editor
customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', '|', 'RemoveFormat']

    },
}

CURRENT_YEAR = ""
HIGH_FORMATION_YEAR = ""
