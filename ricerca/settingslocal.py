import pathlib
import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^$7^pwc)km7*uzn(!-%n39dw$took9@$q1oaerz=^zcxu031(%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_AGE = 60 * 10 # minutes

# the path corresponding the admin backend, default if not defined: admin/
ADMIN_PATH = 'gestione'

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'accounts.User'

DATA_DIR = os.path.join(BASE_DIR, "data")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
if not os.path.exists(STATIC_ROOT):
    pathlib.Path(STATIC_ROOT).mkdir(parents=True, exist_ok=True)


INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'bootstrap_italia_template',
    'django_unical_bootstrap_italia',

    'ricerca_app',
    # 'djangosaml2'
    'rangefilter',

    # rest
    'rest_framework',
    # OAS 3 specs
    #  'drf_spectacular',
    ]


# API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # OAS 3 specs
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi_agid.AgidAutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.OAS3JSONParser',
        #  'rest_framework.parsers.JSONParser',
        #  'rest_framework.parsers.FormParser',
        #  'rest_framework.parsers.MultiPartParser',
    ],
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'storage_portale',
        'USER': 'storage_portale',
        'PASSWORD': 'St0r4ge_-p..ortal3',
        #  'NAME': 'ricerca',
        #  'USER': 'ricerca',
        #  'PASSWORD': '::ric_sp78',
        'PORT': '',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
    },
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# ldap_peoples related
# LDAP_CONNECTION_USER = 'cn=thatuser,dc=unical,dc=it'
# LDAP_CONNECTION_PASSWD = 'Thatpassword'
# LDAP_DB_URL = 'ldap://localhost:389/'
LDAP_BASE_DOMAIN = 'unical.it'
# LDAP_PEOPLE_DN = 'dc=proxy'

# needed for ldap admin forms
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S',
                          '%d/%m/%Y %H:%M:%S']

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y']

# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'it-it'
# TIME_ZONE = 'Europe/Rome'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True


# email notification on error 500
DEFAULT_FROM_EMAIL = 'idp-noreply@DOMAIN'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = 'smtpservizi.unical.it'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = [('Giuseppe De Marco', 'giuseppe.demarco@unical.it'),
          ('Francesco Filicetti', 'francesco.filicetti@unical.it'),]

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
        'ricerca': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

