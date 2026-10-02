from rest_framework.routers import DefaultRouter
from .views import LaboratoriesViewSet

app_name = "apiv2"

router = DefaultRouter()
router.register(r"laboratories_new", LaboratoriesViewSet, basename="laboratories")

urlpatterns = router.urls

