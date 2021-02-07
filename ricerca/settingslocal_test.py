import os

from . settings import *

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '82^w&ie47r^!c8f6yeui@#6e*myi*o4sf3^u*o7+#3qk!tn^=s'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS.append('silk')

AUTH_USER_MODEL = 'accounts.User'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEBUG=True
