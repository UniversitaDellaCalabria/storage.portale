from rest_framework.routers import DefaultRouter

from .views import CdsViewSet, DegreeTypeViewSet, StudyActivitiesViewSet

app_name = "apiv2"


router = DefaultRouter()
router.register(r"cds", CdsViewSet, basename="cds")
router.register(r"degreetypes", DegreeTypeViewSet, basename="degreetypes")
router.register(r"activities", StudyActivitiesViewSet, basename="activities")
urlpatterns = router.urls
