from django.conf import settings
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view


from . import views
from . import api_views

app_name = 'ricerca'
base_url = 'api/ricerca'

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
                        get_schema_view(title="Unical - Ricerca",
                                        permission_classes=(permissions.AllowAny,),
                                        description="OpenData per la Ricerca in Unical",
                                        version="0.1"),
                        name='openapi-schema'),

    # qui API pubbliche
    urlpatterns += path('{}/docenti/'.format(base_url),
                        api_views.ApiDocenteList.as_view()),
    urlpatterns += path('{}/docente/<int:pk>/'.format(base_url),
                        api_views.ApiDocenteDetail.as_view()),

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

    urlpatterns += path('{}/docente/linea_applicata/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaApplicataList.as_view()),
    urlpatterns += path('{}/docente/linea_applicata/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaApplicataDetail.as_view()),

    urlpatterns += path('{}/docente/linea_base/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaBaseList.as_view()),
    urlpatterns += path('{}/docente/linea_base/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaDocenteLineaBaseDetail.as_view()),

    urlpatterns += path('{}/gruppo/'.format(base_url),
                        api_views.ApiRicercaGruppoList.as_view()),
    urlpatterns += path('{}/gruppo/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaGruppoDetail.as_view()),

    urlpatterns += path('{}/linea_applicata/'.format(base_url),
                        api_views.ApiRicercaLineaApplicataList.as_view()),
    urlpatterns += path('{}/linea_applicata/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaLineaApplicataDetail.as_view()),

    urlpatterns += path('{}/linea_base/'.format(base_url),
                        api_views.ApiRicercaLineaBaseList.as_view()),
    urlpatterns += path('{}/linea_base/<int:pk>/'.format(base_url),
                        api_views.ApiRicercaLineaBaseDetail.as_view()),
