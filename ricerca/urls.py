from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas.agid_schema_views import get_schema_view


urlpatterns = [
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    path("api/token", obtain_auth_token, name="auth-token"),
    path('', include('accounts.urls')),

    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck-editor-5-upload-file"),

    path('', include('addressbook.urls')),
    path('', include('advanced_training.urls')),
    path('', include('cds.urls')),
    path('', include('cds_brochure.urls')),
    path('', include('cds_websites.urls')),
    path('', include('companies.urls')),
    path('', include('esse3.urls')),
    path('', include('generics.urls')),
    path('', include('laboratories.urls')),
    path('', include('locks.urls')),
    path('', include('patents.urls')),
    path('', include('pentaho.urls')),
    path('', include('phd.urls')),
    path('', include('projects.urls')),
    path('', include('regdid.urls')),
    path('', include('research_groups.urls')),
    path('', include('research_lines.urls')),
    path('', include('structures.urls')),
    path('', include('teachers.urls')),
]

# API schemas
urlpatterns += path('api/', TemplateView.as_view(template_name='redoc.html', extra_context={'schema_url': 'openapi-schema'}), name='api-redoc'),
try:
    urlpatterns += re_path('^openapi$', get_schema_view(**settings.OAS3_CONFIG), name='openapi-schema'),
    urlpatterns += re_path('^openapi.json$', get_schema_view(renderer_classes=[JSONOpenAPIRenderer], **settings.OAS3_CONFIG), name='openapi-schema-json'),
except BaseException:
    urlpatterns += re_path('^openapi$', get_schema_view(**{}), name='openapi-schema'),
    urlpatterns += re_path('^openapi.json$', get_schema_view(renderer_classes=[JSONOpenAPIRenderer], **{}), name='openapi-schema-json'),


if 'silk' in settings.INSTALLED_APPS:
    urlpatterns += re_path(r'^silk/', include('silk.urls', namespace='silk'))


if 'saml2_sp' in settings.INSTALLED_APPS:
    import saml2_sp.urls
    from djangosaml2 import views
    # saml2_url_prefix = 'saml2'
    urlpatterns += path('', include((saml2_sp.urls, 'sp',))),
    urlpatterns += re_path(r'{}/login/?$'.format(settings.SAML2_URL_PREFIX), views.LoginView.as_view(), name='login'),
    urlpatterns += re_path(r'{}/acs/?$'.format(settings.SAML2_URL_PREFIX), views.AssertionConsumerServiceView.as_view(), name='saml2_acs'),
    urlpatterns += re_path(r'{}/logout/?$'.format(settings.SAML2_URL_PREFIX), views.LogoutInitView.as_view(), name='logout'),
    urlpatterns += re_path(r'{}/ls/?$'.format(settings.SAML2_URL_PREFIX), views.LogoutView.as_view(), name='saml2_ls'),
    urlpatterns += re_path(r'{}/ls/post/?$'.format(settings.SAML2_URL_PREFIX), views.LogoutView.as_view(), name='saml2_ls_post'),
    urlpatterns += re_path(r'^{}/metadata/?$'.format(settings.SAML2_URL_PREFIX), views.MetadataView.as_view(), name='saml2_metadata'),

else:
    # local_url_prefix = 'local'
    urlpatterns += re_path('{}/login/?$'.format(settings.LOCAL_URL_PREFIX), LoginView.as_view(template_name='login.html'), name='login'),
    urlpatterns += re_path('{}/logout/?$'.format(settings.LOCAL_URL_PREFIX), LogoutView.as_view(template_name='logout.html', next_page='/'), name='logout'),

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
