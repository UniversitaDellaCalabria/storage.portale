from django.urls import path

from .views import (
    ApiCdsWebsitesTopicArticlesList,
    ApiCdsWebsitesTopicList,
    ExternalOggettiPortaleViewSet,
    SitoWebCdsOggettiPortaleViewSet,
    ApiCdsWebsitesStudyPlansList
)

app_name = "apiv1"

urlpatterns = [
    path('cds-websites/api/<int:cds_id>/shared-objects/', SitoWebCdsOggettiPortaleViewSet.as_view({'get': 'list'}), name="cds-websites-shared-objects-list"),
    path('cds-websites/api/<int:cds_id>/shared-objects/<int:pk>/', SitoWebCdsOggettiPortaleViewSet.as_view({'get': 'retrieve'}), name="cds-websites-shared-objects-detail"),
    path('cds-websites/api/portal-objects/', ExternalOggettiPortaleViewSet.as_view({'get': 'list'}), name="cds-websites-external-objects-list"),
    path('cds-websites/api/portal-objects/<int:pk>/', ExternalOggettiPortaleViewSet.as_view({'get': 'retrieve'}), name="cds-websites-external-objects-detail"),
    path('cds-websites-topic/', ApiCdsWebsitesTopicList.as_view(), name='cds-websites-topic-list'),
    path('cds-websites-topic-articles/', ApiCdsWebsitesTopicArticlesList.as_view(), name='cds-websites-topic-articles-list'),
    path("cds-websites-studyplans/", ApiCdsWebsitesStudyPlansList.as_view(), name="cds-websites-studyplans-list"),
]
