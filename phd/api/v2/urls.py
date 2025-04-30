from rest_framework.routers import DefaultRouter
from .views import (
    PhdViewSet,
    PhdCyclesViewSet,
    PhdActivitiesViewSet,
    PhdActivitiesTypesViewSet,
    PhdActivitiesTypologiesViewSet,
    PhdSsdViewSet,
    RefPhdViewSet,
    RefStructuresViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"phd", PhdViewSet, basename="phd")
router.register(r"phd/cycles", PhdCyclesViewSet, basename="phd/cycles")
router.register(r"phd/activities", PhdActivitiesViewSet, basename="phd/activities")
router.register(
    r"phd/activities-types", PhdActivitiesTypesViewSet, basename="phd/activities/types"
)
router.register(
    r"phd/activities-typologies",
    PhdActivitiesTypologiesViewSet,
    basename="phd/activities/typologies",
)
router.register(r"phd/ssd", PhdSsdViewSet, basename="phd/ssd")
router.register(r"ref/phd", RefPhdViewSet, basename="ref/phd")
router.register(r"ref/structures", RefStructuresViewSet, basename="ref/structures")
urlpatterns += router.urls
