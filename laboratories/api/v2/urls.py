from rest_framework.routers import DefaultRouter
from .views import (
    LaboratoriesViewSet,
    LaboratoriesAreaViewSet, 
    LaboratoriesScopesViewSet, 
    InfrastructuresViewSet, 
    ErcListViewSet,
    AsterListViewSet
)
app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

# router.register(r"laboratories", LaboratoriesViewSet, basename="laboratories")
router.register(r"laboratories-areas", LaboratoriesAreaViewSet, basename="laboratories-areas")
router.register(r"laboratories-scopes", LaboratoriesScopesViewSet, basename="laboratories-scopes")
router.register(r"infrastructures", InfrastructuresViewSet, basename="infrastructures")
router.register(r"erclist/(?P<level>\d+)", ErcListViewSet, basename="erclist")
router.register(r"asterlist/(?P<level>\d+)", AsterListViewSet, basename="asterlist")
urlpatterns += router.urls