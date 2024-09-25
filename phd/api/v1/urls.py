from django.urls import path

from .views import (
    ApiPhdActivitiesList,
    ApiPhdActivityDetail,
    ApiPhdActivityTypeList,
    ApiPhdActivityTypologies,
    ApiPhdCycles,
    ApiPhdList,
    ApiPhdSsdList,
    ApiRefPhdList,
    ApiRefStructuresList,
)

app_name="apiv1"

urlpatterns = [
    path("phdlist/", ApiPhdList.as_view(), name="phd-list"),
    path("phd-cycles/", ApiPhdCycles.as_view(), name="phd-cycles"),
    path("phd-activities-list/", ApiPhdActivitiesList.as_view(), name="phd-activities-list"),
    path("phd-activities-list/<int:id>/", ApiPhdActivityDetail.as_view(), name="phd-activity-detail"),
    path("phd-activity-type-list/", ApiPhdActivityTypeList.as_view(), name="phd-activity-type-list"),
    path("phd-activity-typologies/", ApiPhdActivityTypologies.as_view(), name="phd-activity-typologies"),
    path("phd-ssd-list/", ApiPhdSsdList.as_view(), name="phd-ssd-list"),
    path("ref-phd/", ApiRefPhdList.as_view(), name="ref-phd"),
    path("ref-structures/", ApiRefStructuresList.as_view(), name="ref-structures"),
]
