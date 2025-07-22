from rest_framework.routers import DefaultRouter
from .views import (
    AdvancedTrainingMastersViewSet,
    AdvancedTrainingCourseTypesViewSet,
    ErogationModesViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(
    r"advanced-training",
    AdvancedTrainingMastersViewSet,
    basename="advanced-training",
)
router.register(
    r"advanced-training-course-types",
    AdvancedTrainingCourseTypesViewSet,
    basename="advanced-training-course-types",
)
router.register(r"erogation-modes", ErogationModesViewSet, basename="erogation-modes")
urlpatterns += router.urls
