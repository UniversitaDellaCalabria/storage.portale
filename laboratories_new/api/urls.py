from rest_framework.routers import DefaultRouter
from .views import (
    ErcListViewSet,
    InfrastructuresViewSet,
    InfrastructuresViewSet,
    LaboratoriesAreaViewSet,
    LaboratoriesScopesViewSet,
    LaboratoriesViewSet,
)

app_name = "apiv2"

router = DefaultRouter()
router.register(r"laboratories_new", LaboratoriesViewSet, basename="laboratories")
router.register(
    r"laboratories_new_area", LaboratoriesAreaViewSet, basename="laboratories-area"
)
router.register(
    r"laboratories_new_scopes",
    LaboratoriesScopesViewSet,
    basename="laboratories-scopes",
)
router.register(r"infrastructures_new", InfrastructuresViewSet, basename="infrastructures")
router.register(r"erclist_new/(?P<level>\d+)", ErcListViewSet, basename="erclist")
# router.register(r"asterlist/(?P<level>\d+)", AsterListViewSet, basename="asterlist")

urlpatterns = router.urls
