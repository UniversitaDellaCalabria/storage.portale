from rest_framework.routers import DefaultRouter

from .views import CdsViewSet

app_name = "apiv2"


router = DefaultRouter()
router.register(r"cds", CdsViewSet, basename="cds")
urlpatterns = router.urls
