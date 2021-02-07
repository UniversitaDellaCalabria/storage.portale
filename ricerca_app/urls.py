from django.conf import settings
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view
from rest_framework.schemas.agid_schema_views import get_schema_view



from . import api_views

app_name = 'ricerca'
base_url = 'api/ricerca'

agid_api_dict = {'title': "Unical - Ricerca",
                 #  'generator_class': openapi_agid_generator,
                 'permission_classes': (permissions.AllowAny,),
                 'description': "OpenData per la Ricerca in Unical",
                 'termsOfService': 'https://tos.unical.it',
                 'x-api-id': '00000000-0000-0000-0000-000000000001',
                 'x-summary': 'OpenData per la Ricerca in Unical',
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
                 'contact': dict(email='giuseppe.demarco@unical.it',
                                 name='Giuseppe De Marco',
                                 url='https://github.com/UniversitaDellaCalabria'),
                 'version': "0.1.2"
                 }

urlpatterns = [
    # qui le chiamate alle risorse di felix
    # ...

]

if 'rest_framework' in settings.INSTALLED_APPS:
    router = routers.DefaultRouter()
    #  router.register('api/ricerca', api_views.ApiDocenteViewSet)
    urlpatterns += path('api', include(router.urls)),

    # dynamic Schema export resource
    urlpatterns += path('openapi',
                        get_schema_view(**agid_api_dict),
                        name='openapi-schema'),
    # dynamic Schema export resource
    urlpatterns += path('openapi.json',
                        get_schema_view(renderer_classes=[JSONOpenAPIRenderer],
                                        **agid_api_dict),
                        name='openapi-schema-json'),

    # qui API pubbliche
    urlpatterns += path('{}/persone/'.format(base_url),
                        api_views.ApiPersonaleList.as_view()),
    urlpatterns += path('{}/persona/<int:pk>/'.format(base_url),
                        api_views.ApiPersonaleDetail.as_view()),

    urlpatterns += path('{}/aster/1/'.format(base_url),
                        api_views.ApiRicercaAster1List.as_view()),
    urlpatterns += path('{}/aster/1/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaAster1Detail.as_view()),

    urlpatterns += path('{}/aster/2/'.format(base_url),
                        api_views.ApiRicercaAster2List.as_view()),
    urlpatterns += path('{}/aster/2/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaAster2Detail.as_view()),

    urlpatterns += path('{}/erc/1/'.format(base_url),
                        api_views.ApiRicercaErc1List.as_view()),
    urlpatterns += path('{}/erc/1/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaErc1Detail.as_view()),

    urlpatterns += path('{}/erc/2/'.format(base_url),
                        api_views.ApiRicercaErc2List.as_view()),
    urlpatterns += path('{}/erc/2/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaErc2Detail.as_view()),

    urlpatterns += path('{}/docente/gruppo/'.format(base_url),
                        api_views.ApiRicercaDocenteGruppoList.as_view()),
    urlpatterns += path('{}/docente/gruppo/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaDocenteGruppoDetail.as_view()),

    urlpatterns += path('{}/docente/linea-applicata/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaApplicataList.as_view()),
    urlpatterns += path('{}/docente/linea-applicata/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaApplicataDetail.as_view()),

    urlpatterns += path('{}/persona/linea-base/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaBaseList.as_view()),
    urlpatterns += path('{}/persona/linea-base/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaBaseDetail.as_view()),

    urlpatterns += path('{}/gruppo/'.format(base_url),
                        api_views.ApiRicercaGruppoList.as_view()),
    urlpatterns += path('{}/gruppo/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaGruppoDetail.as_view()),

    urlpatterns += path('{}/linea-applicata/'.format(base_url),
                        api_views.ApiRicercaLineaApplicataList.as_view()),
    urlpatterns += path('{}/linea-applicata/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaLineaApplicataDetail.as_view()),

    urlpatterns += path('{}/linea-base/'.format(base_url),
                        api_views.ApiRicercaLineaBaseList.as_view()),
    urlpatterns += path('{}/linea-base/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaLineaBaseDetail.as_view()),

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    urlpatterns += path('{}/cdslist'.format(base_url),
                        api_views.ApiCdSList.as_view(),
                        name='cdslist'),

    urlpatterns += path('{}/cdsinfo'.format(base_url),
                        api_views.ApiCdSInfo.as_view(),
                        name='cdsinfo'),
