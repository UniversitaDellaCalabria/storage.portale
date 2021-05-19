from django.conf import settings
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from rest_framework.renderers import JSONOpenAPIRenderer
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

    # dynamic Schema export resource
    # urlpatterns += path('openapi',
    #                     get_schema_view(**agid_api_dict),
    #                     name='openapi-schema'),
    # dynamic Schema export resource
    #  urlpatterns += path('openapi.json',
    #                     get_schema_view(renderer_classes=[JSONOpenAPIRenderer],
    #                                    **agid_api_dict),
    #                     name='openapi-schema-json'),

    # qui API pubbliche

    urlpatterns += path('{}/cdslist'.format(base_url),
                        api_views.ApiCdSList.as_view(),
                        name='cdslist'),

    urlpatterns += path('{}/cdsinfo'.format(base_url),
                        api_views.ApiCdSInfo.as_view(),
                        name='cdsinfo'),

    urlpatterns += path('{}/cdsstudyplans'.format(base_url),
                        api_views.ApiCdSStudyPlans.as_view(),
                        name='cdsstudyplans'),

    urlpatterns += path('{}/cdsstudyplansunique'.format(base_url),
                        api_views.ApiCdSStudyPlansUnique.as_view(),
                        name='cdsstudyplansunique'),

    urlpatterns += path('{}/studyplanactivities'.format(base_url),
                        api_views.ApiStudyPlanActivities.as_view(),
                        name='studyplanactivities'),

    urlpatterns += path('{}/studyactivityinfo'.format(base_url),
                        api_views.ApiStudyActivityInfo.as_view(),
                        name='studyactivityinfo'),

    urlpatterns += path('{}/cdsmainteachers'.format(base_url),
                        api_views.ApiCdSMainTeachers.as_view(),
                        name='cdsmainteachers'),

    urlpatterns += path('{}/teacherresearchgroups'.format(base_url),
                        api_views.ApiTeacherResearchGroups.as_view(),
                        name='teacherresearchgroups'),

    urlpatterns += path('{}/teacherresearchlines'.format(base_url),
                        api_views.ApiTeacherResearchLines.as_view(),
                        name='teacherresearchlines'),

    urlpatterns += path('{}/teacherslist'.format(base_url),
                        api_views.ApiTeachersList.as_view(),
                        name='teacherslist'),

    urlpatterns += path('{}/teacherstudyactivities'.format(base_url),
                        api_views.ApiTeacherStudyActivities.as_view(),
                        name='teacherstudyactivities'),

    urlpatterns += path('{}/teacherinfo'.format(base_url),
                        api_views.ApiTeacherInfo.as_view(),
                        name='teacherinfo'),

    urlpatterns += path('{}/doctorateslist'.format(base_url),
                        api_views.ApiDoctoratesList.as_view(),
                        name='doctorateslist'),
