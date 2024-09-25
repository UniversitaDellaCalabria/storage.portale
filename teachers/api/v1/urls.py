from django.urls import path

from .views import (
    ApiPublicationDetail,
    ApiPublicationsCommunityTypesList,
    ApiPublicationsList,
    ApiTeacherDetail,
    ApiTeacherMaterials,
    ApiTeacherNews,
    ApiTeacherPublicationDetail,
    ApiTeacherPublicationsList,
    ApiTeacherResearchLinesList,
    ApiTeachersList,
    ApiTeacherStudyActivitiesList,
    ApiTeachingCoverageActivitiesList,
    ApiTeachingCoverageDetail,
    ApiTeachingCoveragePublicationDetail,
    ApiTeachingCoveragePublicationsList,
    ApiTeachingCoveragesList,
)

app_name = "apiv1"

urlpatterns = [
    path("teachers/", ApiTeachersList.as_view(), name="teachers-list"),
    path("teachers/<str:teacherid>/", ApiTeacherDetail.as_view(), name="teacher-info"),
    path("teachers/<str:teacherid>/studyactivities/", ApiTeacherStudyActivitiesList.as_view(), name="teacher-study-activities"),
    path("teachers/<str:teacherid>/materials/", ApiTeacherMaterials.as_view(), name="teacher-materials"),
    path("teachers/<str:teacherid>/researchlines/", ApiTeacherResearchLinesList.as_view(), name="teacher-research-lines"),
    path("teachers/<str:teacherid>/news/", ApiTeacherNews.as_view(), name="teacher-news"),
    path("teachers/<str:teacherid>/publications/", ApiTeacherPublicationsList.as_view(), name="publications"),
    path("teachers/<str:teacherid>/publications/<str:publicationid>/", ApiTeacherPublicationDetail.as_view(), name="publication-detail"),
    path("publications/", ApiPublicationsList.as_view(), name="publications-list"),
    path("publications/<str:publicationid>/", ApiPublicationDetail.as_view(), name="publication-info"),
    path("teachers:apiv1:publications-community-types/", ApiPublicationsCommunityTypesList.as_view(), name="publications-community-types"),
    path("teaching-coverages/", ApiTeachingCoveragesList.as_view(), name="teaching-coverages-list"),
    path("teaching-coverages/<str:teacherid>/studyactivities/", ApiTeachingCoverageActivitiesList.as_view(), name="teaching-coverages-studyactivities"),
    path("teaching-coverages/<str:teacherid>/", ApiTeachingCoverageDetail.as_view(), name="teaching-coverages-info"),
    path("teaching-coverages/<str:teacherid>/publications/", ApiTeachingCoveragePublicationsList.as_view(), name="teaching-coverages-publications"),
    path("teaching-coverages/<str:teacherid>/publications/<str:publicationid>/", ApiTeachingCoveragePublicationDetail.as_view(), name="teaching-coverages-publication-detail"),
]
