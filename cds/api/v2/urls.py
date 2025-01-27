
from rest_framework.routers import DefaultRouter

from .views import (
    AcademicPathwaysViewSet,
    AcademicYearsViewSet,
    CdsViewSet,
    DegreeTypeViewSet,
    StudyActivitiesViewSet,
    CdsAreasViewSet,
    CdsExpiredViewSet,
    CdsMorphViewSet
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"academic-pathways/(?P<regdid_id>\d+)", AcademicPathwaysViewSet, basename="academic-pathways")
router.register(r"degree-types", DegreeTypeViewSet, basename="degree-types")
router.register(r"academic-years", AcademicYearsViewSet, basename="academic-years")
router.register(r"activities", StudyActivitiesViewSet, basename="activities")
router.register(r"cds", CdsViewSet, basename="cds")
router.register(r"cds/areas", CdsAreasViewSet, basename="cds-areas")
router.register(r"cds/expired", CdsExpiredViewSet, basename="cds-expired")
router.register(r"cds/morph", CdsMorphViewSet, basename="cds-morph")
urlpatterns += router.urls
