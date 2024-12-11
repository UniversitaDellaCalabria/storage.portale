from django.urls import path

from .views import (
    ApiAcademicYearsList,
    ApiAllStudyActivitiesList,
    ApiCdsAreasList,
    ApiCdsExpired,
    ApiCdSInfo,
    ApiCdSList,
    ApiCdsMorphList,
    ApiCdSStudyPlansList,
    ApiDegreeTypesList,
    ApiSortingContacts,
    ApiStudyActivityDetail,
    ApiStudyPlanActivitiesList,
    ApiStudyPlanDetail,
)

app_name = "apiv1"

urlpatterns = [
    path("cds/", ApiCdSList.as_view(), name="cds-list"),
    path("cds/<int:regdidid>/", ApiCdSInfo.as_view(), name="cds-info"),
    path("cds/<int:regdidid>/studyplans/", ApiCdSStudyPlansList.as_view(), name="cds-studyplans"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/", ApiStudyPlanDetail.as_view(), name="studyplan-detail"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/", ApiStudyPlanActivitiesList.as_view(), name="studyplan-activities"),
    path("cds/<int:regdidid>/studyplans/<int:studyplanid>/activities/<int:studyactivityid>/", ApiStudyActivityDetail.as_view(), name="studyactivity-info"),  # TODO same as studyactivity-detail
    

    path("cds-morph/<str:cds_cod>/", ApiCdsMorphList.as_view(), name="cds-morph"), 
    path("cds-expired/", ApiCdsExpired.as_view(), name="cds-expired"), 
    
    path("cds-areas/", ApiCdsAreasList.as_view(), name="cds-areas"),
    path("activities/", ApiAllStudyActivitiesList.as_view(), name="activities"),
    path("activities/<int:studyactivityid>/", ApiStudyActivityDetail.as_view(), name="studyactivity-detail"),  # TODO same as studyactivity-info
    path("academicyears/", ApiAcademicYearsList.as_view(), name="academic-years"),
    path("degreetypes/", ApiDegreeTypesList.as_view(), name="degree-types"),
    path("sorting-contacts/<str:cdscod>/", ApiSortingContacts.as_view(), name="sorting-contacts"),
]
