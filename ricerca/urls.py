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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, re_path
from rest_framework.schemas.agid_schema_views import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer


urlpatterns = [
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


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
    urlpatterns += re_path(r'^silk/', include('silk.urls', namespace='silk'))

if 'crud.utils' in settings.INSTALLED_APPS:
    import crud.utils.urls
    urlpatterns += path('', include((crud.utils.urls, 'crud_utils',))),
if 'crud.cds' in settings.INSTALLED_APPS:
    import crud.cds.urls
    urlpatterns += path('', include((crud.cds.urls, 'crud_cds',))),
if 'crud.companies' in settings.INSTALLED_APPS:
    import crud.companies.urls
    urlpatterns += path('', include((crud.companies.urls, 'crud_companies',))),
if 'crud.patents' in settings.INSTALLED_APPS:
    import crud.patents.urls
    urlpatterns += path('', include((crud.patents.urls, 'crud_patents',))),
if 'crud.phd' in settings.INSTALLED_APPS:
    import crud.phd.urls
    urlpatterns += path('', include((crud.phd.urls, 'crud_phd',))),
if 'crud.projects' in settings.INSTALLED_APPS:
    import crud.projects.urls
    urlpatterns += path('', include((crud.projects.urls, 'crud_projects',))),
if 'crud.research_groups' in settings.INSTALLED_APPS:
    import crud.research_groups.urls
    urlpatterns += path('', include((crud.research_groups.urls, 'crud_research_groups',))),
if 'crud.research_lines' in settings.INSTALLED_APPS:
    import crud.research_lines.urls
    urlpatterns += path('', include((crud.research_lines.urls, 'crud_research_lines',))),
if 'crud.teachers' in settings.INSTALLED_APPS:
    import crud.teachers.urls
    urlpatterns += path('', include((crud.teachers.urls, 'crud_teachers',))),
if 'crud.cds_websites_brochure' in settings.INSTALLED_APPS:
    import crud.cds_websites_brochure.urls
    urlpatterns += path('', include((crud.cds_websites_brochure.urls, 'crud_cds_websites_brochure',))),
if 'crud.cds_websites_pages' in settings.INSTALLED_APPS:
    import crud.cds_websites_pages.urls
    urlpatterns += path('', include((crud.cds_websites_pages.urls, 'crud_cds_websites_pages',))),
if 'crud.laboratories' in settings.INSTALLED_APPS:
    import crud.laboratories.urls
    urlpatterns += path('', include((crud.laboratories.urls, 'crud_laboratories',))),
if 'crud.regdid' in settings.INSTALLED_APPS:
    import crud.regdid.urls
    urlpatterns += path('', include((crud.regdid.urls, 'crud_regdid',))),

if 'pentaho' in settings.INSTALLED_APPS:
    import pentaho.urls
    urlpatterns += path('', include((pentaho.urls, 'pentaho',))),

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


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
