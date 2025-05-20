from rest_framework.routers import DefaultRouter
from .views import PersonnelCfViewSet, RolesViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(
    r"personnel-cfs", PersonnelCfViewSet, basename="personnel-cfs"
)
router.register(
    r"roles", RolesViewSet, basename="roles"
)

urlpatterns += router.urls
