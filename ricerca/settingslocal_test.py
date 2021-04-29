from .settings import *

#MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
#INSTALLED_APPS.append('silk')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
