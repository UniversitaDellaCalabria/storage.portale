from rest_framework.routers import DefaultRouter
from .views import TeachersViewSet, CoveragesViewSet
app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"teachers", TeachersViewSet, basename="teachers")
router.register(r"coverages", CoveragesViewSet, basename="coverages")
urlpatterns += router.urls
