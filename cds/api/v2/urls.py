from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AcademicPathsViewSet,
    AcademicYearsViewSet,
    CdsViewSet,
    DegreeTypeViewSet,
    StudyActivitiesViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = [
    path(
        "academic-pathways/<int:regdid_id>/",
        AcademicPathsViewSet.as_view({"get": "list"}),
        name="academic-pathways-list",
    ),
    path(
        "academic-pathways/<int:regdid_id>/<int:pds_regdid_id>/",
        AcademicPathsViewSet.as_view({"get": "retrieve"}),
        name="academic-pathways-detail",
    ),
]

router.register(r"cds", CdsViewSet, basename="cds")
router.register(r"degree-types", DegreeTypeViewSet, basename="degree-types")
router.register(r"academic-years", AcademicYearsViewSet, basename="academic-years")
router.register(r"activities", StudyActivitiesViewSet, basename="activities")

urlpatterns += router.urls
