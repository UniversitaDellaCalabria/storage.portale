
"""
Django settings for ricerca project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '82^w&ie47r^!c8f6yeui@#6e*myi*o4sf3^u*o7+#3qk!tn^=s'
ALLOWED_HOSTS = ['*']
ADMIN_PATH = 'test_admin'
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
    'ricerca_app',
    # 'silk',
    # 'ricerca_app.apps.RicercaAppConfig',
]
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    #'silk.middleware.SilkyMiddleware',
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

LABEL_MAPPING = {
    'RegDidId': 'ID Regolamento Didattico',
    'CdSId': 'ID Corso di Studi',
    'AcademicYear': 'Anno Accademico',
    'CdSName': 'Nome Corso di Studi',
    'DepartmentId': 'ID Dipartimento',
    'DepartmentName': 'Nome Dipartimento',
    'CourseType': 'Tipologia Corso',
    'CourseClassId': 'ID Classe Corso',
    'CourseClassName': 'Nome Classe Corso',
    'CdSLanguage': 'Lingua Corso di Studi',
    'CdSDuration': 'Durata Corso di Studi',
    'CdSECTS': 'ECTS Corso di Studi',
    'CdSAttendance': 'Frequenza Obbligatoria',
}

DEBUG=True
