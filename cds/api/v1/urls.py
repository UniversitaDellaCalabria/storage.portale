from django.urls import path

from .views import (
    ApiAcademicYearsList,
    ApiAllStudyActivitiesList,
    ApiCdsAreasList,
    ApiCdSDetail,
    ApiCdSList,
    ApiCdSStudyPlansList,
    ApiCdsWebsitesStudyPlansList,
    ApiDegreeTypesList,
    ApiErogationModesList,
    ApiSortingContacts,
    ApiStudyActivityDetail,
    ApiStudyActivityInfo,
    ApiStudyPlanActivitiesList,
    ApiStudyPlanDetail,
)

app_name = "apiv1"

urlpatterns = [
    path("cds/", ApiCdSList.as_view(), name="cds-list"),
    path("cds/<int:regdidid>/", ApiCdSDetail.as_view(), name="cds-info"),
    path("cds/<int:regdidid>/studyplans/", ApiCdSStudyPlansList.as_view(), name="cds-studyplans"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/", ApiStudyPlanDetail.as_view(), name="studyplan-detail"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/", ApiStudyPlanActivitiesList.as_view(), name="studyplan-activities"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/<int:studyactivityid>/", ApiStudyActivityInfo.as_view(), name="studyactivity-info"),
    path("cds-websites-studyplans/", ApiCdsWebsitesStudyPlansList.as_view(), name="cds-websites-studyplans-list"),
    path("cds-areas/", ApiCdsAreasList.as_view(), name="cds-areas"),
    path("activities/", ApiAllStudyActivitiesList.as_view(), name="activities"),
    path("activities/<int:studyactivityid>/", ApiStudyActivityDetail.as_view(), name="studyactivity-detail"),
    path("academicyears/", ApiAcademicYearsList.as_view(), name="academic-years"),
    path("degreetypes/", ApiDegreeTypesList.as_view(), name="degree-types"),
    path("erogation-modes/", ApiErogationModesList.as_view(), name="erogation-modes"),
    path("sorting-contacts/<str:cdscod>/", ApiSortingContacts.as_view(), name="sorting-contacts"),
]