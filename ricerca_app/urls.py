from django.conf import settings
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view

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
    # router = routers.DefaultRouter()
    #  router.register('api/ricerca', api_views.ApiDocenteViewSet)
    # urlpatterns += path('api', include(router.urls)),

    urlpatterns += path('api/',
                        TemplateView.as_view(template_name='redoc.html',
                                             extra_context={'schema_url': 'openapi-schema'}),
                        name='api-redoc'),

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

    # urlpatterns += path('status/',
    #                     api_views.ApiStatus.as_view(),
    #                     name='status'),

    urlpatterns += path('{}/cds/'.format(base_url),
                        api_views.ApiCdSList.as_view(),
                        name='cdslist'),

    urlpatterns += path('{}/cds/<int:regdidid>/'.format(base_url),
                        api_views.ApiCdSDetail.as_view(),
                        name='cdsinfo'),

    urlpatterns += path('{}/cds/<int:regdidid>/studyplans/'.format(base_url),
                        api_views.ApiCdSStudyPlansList.as_view(),
                        name='cdsstudyplans'),

    urlpatterns += path(
        '{}/cds/<int:regdidid>/studyplans/<int:studyplanid>/'.format(base_url),
        api_views.ApiStudyPlanDetail.as_view(),
        name='studyplandetail'),

    urlpatterns += path(
        '{}/cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/'.format(base_url),
        api_views.ApiStudyPlanActivitiesList.as_view(),
        name='studyplanactivities'),

    urlpatterns += path(
        '{}/cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/<int:studyactivityid>/'.format(base_url),
        api_views.ApiStudyActivityInfo.as_view(),
        name='studyactivityinfo'),

    urlpatterns += path('{}/activities/<int:studyactivityid>/'.format(base_url),
                        api_views.ApiStudyActivityDetail.as_view(),
                        name='studyactivitydetail'),

    # urlpatterns += path('{}/cdsmainteachers/'.format(base_url),
    #                     api_views.ApiCdSMainTeachersList.as_view(),
    #                     name='cdsmainteachers'),

    # urlpatterns += path(
    #     '{}/teachers/<str:teacherid>/researchgroups/'.format(base_url),
    #     api_views.ApiTeacherResearchGroupsList.as_view(),
    #     name='teacherresearchgroups'),

    urlpatterns += path(
        '{}/researchgroups/'.format(base_url),
        api_views.ApiResearchGroupsList.as_view(),
        name='researchgroups'),

    urlpatterns += path(
        '{}/teachers/<str:teacherid>/researchlines/'.format(base_url),
        api_views.ApiTeacherResearchLinesList.as_view(),
        name='teacherresearchlines'),

    urlpatterns += path(
        '{}/baseresearchlines/'.format(base_url),
        api_views.ApiBaseResearchLinesList.as_view(),
        name='baseresearchlines'),

    urlpatterns += path(
        '{}/appliedresearchlines/'.format(base_url),
        api_views.ApiAppliedResearchLinesList.as_view(),
        name='appliedresearchlines'),

    urlpatterns += path('{}/teachers/'.format(base_url),
                        api_views.ApiTeachersList.as_view(),
                        name='teacherslist'),

    urlpatterns += path('{}/teaching-coverages/'.format(base_url),
                        api_views.ApiTeachingCoveragesList.as_view(),
                        name='teachingcoverageslist'),

    urlpatterns += path(
        '{}/teaching-coverages/<str:teacherid>/studyactivities/'.format(base_url),
        api_views.ApiTeachingCoverageActivitiesList.as_view(),
        name='teachingcoveragesstudyactivities'),

    urlpatterns += path(
        '{}/teaching-coverages/<str:teacherid>/'.format(base_url),
        api_views.ApiTeachingCoverageDetail.as_view(),
        name='teachingcoveragesinfo'),

    urlpatterns += path(
        '{}/teaching-coverages/<str:teacherid>/publications/'.format(base_url),
        api_views.ApiTeachingCoveragePublicationsList.as_view(),
        name='teachingcoveragespublications'),

    urlpatterns += path(
        '{}/teaching-coverages/<str:teacherid>/publications/<str:publicationid>/'.format(base_url),
        api_views.ApiTeachingCoveragePublicationDetail.as_view(),
        name='teachingcoveragespublicationdetail'),

    urlpatterns += path(
        '{}/teachers/<str:teacherid>/studyactivities/'.format(base_url),
        api_views.ApiTeacherStudyActivitiesList.as_view(),
        name='teacherstudyactivities'),

    urlpatterns += path('{}/teachers/<str:teacherid>/'.format(base_url),
                        api_views.ApiTeacherDetail.as_view(),
                        name='teacherinfo'),

    urlpatterns += path('{}/teachers/<str:teacherid>/publications/'.format(base_url),
                        api_views.ApiPublicationsList.as_view(),
                        name='publications'),

    urlpatterns += path(
        '{}/teachers/<str:teacherid>/publications/<str:publicationid>/'.format(base_url),
        api_views.ApiPublicationDetail.as_view(),
        name='publicationdetail'),

    urlpatterns += path('{}/doctorateslist/'.format(base_url),
                        api_views.ApiDoctoratesList.as_view(),
                        name='doctorateslist'),

    urlpatterns += path('{}/degreetypes/'.format(base_url),
                        api_views.ApiDegreeTypesList.as_view(),
                        name='degreetypes'),

    urlpatterns += path('{}/departments/'.format(base_url),
                        api_views.ApiDepartmentsList.as_view(),
                        name='departmentslist'),

    urlpatterns += path('{}/departmentsfilter/'.format(base_url),
                        api_views.ApiDepartmentsFilterList.as_view(),
                        name='departmentsfilterlist'),

    urlpatterns += path('{}/departments/<str:departmentcod>/'.format(base_url),
                        api_views.ApiDepartmentDetail.as_view(),
                        name='departmentdetail'),

    urlpatterns += path('{}/addressbook/'.format(base_url),
                        api_views.ApiAddressbookList.as_view(),
                        name='addressbooklist'),

    urlpatterns += path('{}/addressbook/<str:personaleid>/'.format(base_url),
                        api_views.ApiPersonaleDetail.as_view(),
                        name='personaledetail'),

    urlpatterns += path('{}/structures/'.format(base_url),
                        api_views.ApiStructuresList.as_view(),
                        name='structureslist'),

    urlpatterns += path('{}/structuresfilter/'.format(base_url),
                        api_views.ApiStructuresFilterList.as_view(),
                        name='structuresfilterlist'),

    urlpatterns += path('{}/structuretypes/'.format(base_url),
                        api_views.ApiStructureTypesList.as_view(),
                        name='structuretypes'),

    urlpatterns += path('{}/academicyears/'.format(base_url),
                        api_views.ApiAcademicYearsList.as_view(),
                        name='academicyears'),

    urlpatterns += path('{}/roles/'.format(base_url),
                        api_views.ApiRolesList.as_view(),
                        name='roleslist'),

    urlpatterns += path('{}/structures/<str:structureid>/'.format(base_url),
                        api_views.ApiStructureDetail.as_view(),
                        name='structuredetail'),

    urlpatterns += path('{}/laboratories/<str:laboratoryid>/'.format(base_url),
                        api_views.ApiLaboratoryDetail.as_view(),
                        name='laboratorydetail'),

    urlpatterns += path('{}/laboratories/'.format(base_url),
                        api_views.ApiLaboratoriesList.as_view(),
                        name='laboratorieslist'),

    urlpatterns += path('{}/laboratoriesareas/'.format(base_url),
                        api_views.ApiLaboratoriesAreasList.as_view(),
                        name='laboratoriesareas'),

    urlpatterns += path('{}/erc1list/'.format(base_url),
                        api_views.ApiErc1List.as_view(),
                        name='erc1list'),

    urlpatterns += path('{}/erc1filter/'.format(base_url),
                        api_views.ApiErc1FilterList.as_view(),
                        name='erc1filterlist'),

    urlpatterns += path('{}/erc0list/'.format(base_url),
                        api_views.ApiErc0List.as_view(),
                        name='erc0list'),

    urlpatterns += path('{}/erc2list/'.format(base_url),
                        api_views.ApiErc2List.as_view(),
                        name='erc2list'),

    urlpatterns += path('{}/publicationscommunitytypes/'.format(base_url),
                        api_views.ApiPublicationsCommunityTypesList.as_view(),
                        name='publicationscommunitytypes'),

    urlpatterns += path(
        '{}/publications/'.format(base_url),
        api_views.ApiPublicationsList.as_view(),
        name='publicationslist'),

    urlpatterns += path(
        '{}/publications/<str:publicationid>/'.format(base_url),
        api_views.ApiPublicationDetail.as_view(),
        name='publicationinfo'),

    urlpatterns += path(
        '{}/addressbookstructures/'.format(base_url),
        api_views.ApiAddressbookStructuresList.as_view(),
        name='allstructureslist'),

    urlpatterns += path(
        '{}/addressbookstructures/<str:structureid>/'.format(base_url),
        api_views.ApiAddressbookStructureDetail.as_view(),
        name='addressbookstructuredetail'),
