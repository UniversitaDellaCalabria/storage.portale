"""ricerca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas.agid_schema_views import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer



urlpatterns = [
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
]


# API schemas
try:
    urlpatterns += re_path('^openapi$',
                               get_schema_view(**settings.OAS3_CONFIG),
                               name='openapi-schema'),
    urlpatterns += re_path('^openapi.json$',
                               get_schema_view(renderer_classes=[JSONOpenAPIRenderer],
                                               **settings.OAS3_CONFIG),
                               name='openapi-schema-json'),
except BaseException:
    urlpatterns += re_path('^openapi$',
                               get_schema_view(**{}),
                               name='openapi-schema'),
    urlpatterns += re_path('^openapi.json$',
                               get_schema_view(renderer_classes=[JSONOpenAPIRenderer],
                                               **{}),
                               name='openapi-schema-json'),

if 'ricerca_app' in settings.INSTALLED_APPS:
    import ricerca_app.urls
    urlpatterns += path('', include((ricerca_app.urls, 'ricerca',))),

if 'silk' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
