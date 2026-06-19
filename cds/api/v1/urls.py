from django.urls import path, re_path

from rest_framework.routers import DefaultRouter

from .views import (
    ApiAcademicYearsList,
    ApiAllStudyActivitiesList,
    ApiCdsAreasList,
    ApiCdsExpired,
    ApiCdSInfo,
    ApiCdSList,
    ApiCdsMorphDetail,
    ApiCdsMorphList,
    ApiCdSStudyPlansList,
    ApiDegreeTypesList,
    ApiSortingContacts,
    ApiStudyActivityDetail,
    ApiStudyPlanActivitiesList,
    ApiStudyPlanDetail,
)

from cds.api.v2.views import (
    AcademicPathwaysViewSet,
    StudyActivitiesViewSet,
    StudyActivitiesViewSetV1,
    StudyPlansViewSetV1,
    StudyPlansActivitiesViewSetV1,
)

app_name = "apiv1"

urlpatterns = [
    path("cds/", ApiCdSList.as_view(), name="cds-list"),
    path("cds/<int:regdidid>/", ApiCdSInfo.as_view(), name="cds-info"),
    path("cds/<int:regdidid>/studyplans/", ApiCdSStudyPlansList.as_view(), name="cds-studyplans"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/", ApiStudyPlanDetail.as_view(), name="studyplan-detail"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/", ApiStudyPlanActivitiesList.as_view(), name="studyplan-activities"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/<int:studyactivityid>/", ApiStudyActivityDetail.as_view(), name="studyactivity-info"),  # TODO same as studyactivity-detail


    path("cds-morph/<str:cds_cod>/", ApiCdsMorphDetail.as_view(), name="cds-morph-detail"),
    path("cds-morph/", ApiCdsMorphList.as_view(), name="cds-morph-list"),
    path("cds-expired/", ApiCdsExpired.as_view(), name="cds-expired"),

    path("cds-areas/", ApiCdsAreasList.as_view(), name="cds-areas"),
    # ~ path("activities/", ApiAllStudyActivitiesList.as_view(), name="activities"),
    # ~ path("activities/<int:studyactivityid>/", ApiStudyActivityDetail.as_view(), name="studyactivity-detail"),  # TODO same as studyactivity-info
    path("academicyears/", ApiAcademicYearsList.as_view(), name="academic-years"),
    path("degreetypes/", ApiDegreeTypesList.as_view(), name="degree-types"),
    path("sorting-contacts/<str:cdscod>/", ApiSortingContacts.as_view(), name="sorting-contacts"),
]

router = DefaultRouter()

router.register(r"activities", StudyActivitiesViewSetV1, basename="activities")
router.register(r"studyplans/(?P<cds_cod>\d+)/(?P<year>\d+)",StudyPlansViewSetV1, basename="studyplans",)
# ~ router.register(r"cds/(?P<regdidid>\d+)/studyplans-activities/", study_plans_list, basename="studyplans-activities")

urlpatterns += router.urls

study_plans_list = StudyPlansActivitiesViewSetV1.as_view({
    'get': 'list',
})
urlpatterns.append(
    re_path(r"^cds/(?P<regdidid>\d+)/studyplans-activities/", study_plans_list, name="studyplans-activities")
)
