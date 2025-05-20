from rest_framework.routers import DefaultRouter
from .views import HighFormationMastersViewSet, HighFormationCourseTypesViewSet, ErogationModesViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(
    r"high-formation-masters", HighFormationMastersViewSet, basename="high-formation-masters"
)
router.register(
    r"high-formation-course-types", HighFormationCourseTypesViewSet, basename="high-formation-course-types"
)
router.register(
    r"erogation-modes", ErogationModesViewSet, basename="erogation-modes"
)
urlpatterns += router.urls
