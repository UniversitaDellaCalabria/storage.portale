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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
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

if 'ricerca_crud' in settings.INSTALLED_APPS:
    import ricerca_crud.urls
    urlpatterns += path('', include((ricerca_crud.urls, 'ricerca_crud',))),

if 'saml2_sp' in settings.INSTALLED_APPS:
    from djangosaml2 import views
    import saml2_sp.urls
    # saml2_url_prefix = 'saml2'

    urlpatterns += path('', include((saml2_sp.urls, 'sp',))),

    urlpatterns += re_path(r'{}/login/?$'.format(settings.SAML2_URL_PREFIX),
                           views.LoginView.as_view(), name='login'),
    urlpatterns += re_path(r'{}/acs/?$'.format(settings.SAML2_URL_PREFIX),
                           views.AssertionConsumerServiceView.as_view(), name='saml2_acs'),
    urlpatterns += re_path(r'{}/logout/?$'.format(settings.SAML2_URL_PREFIX),
                           views.LogoutInitView.as_view(), name='logout'),
    urlpatterns += re_path(r'{}/ls/?$'.format(settings.SAML2_URL_PREFIX),
                           views.LogoutView.as_view(), name='saml2_ls'),
    urlpatterns += re_path(r'{}/ls/post/?$'.format(settings.SAML2_URL_PREFIX),
                           views.LogoutView.as_view(), name='saml2_ls_post'),
    urlpatterns += re_path(r'^{}/metadata/?$'.format(settings.SAML2_URL_PREFIX),
                           views.MetadataView.as_view(), name='saml2_metadata'),

else:
    # local_url_prefix = 'local'
    urlpatterns += re_path('{}/login/?$'.format(settings.LOCAL_URL_PREFIX),
                        LoginView.as_view(template_name='login.html'),
                        name='login'),
    urlpatterns += re_path('{}/logout/?$'.format(settings.LOCAL_URL_PREFIX),
                        LogoutView.as_view(template_name='logout.html', next_page='/'),
                        name='logout'),
