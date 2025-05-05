from rest_framework.routers import DefaultRouter
from .views import BaseResearchLinesViewSet, AppliedResearchLinesViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(
    r"baseresearchlines", BaseResearchLinesViewSet, basename="base-researc-lines"
)
router.register(
    r"appliedresearchlines",
    AppliedResearchLinesViewSet,
    basename="applied-research-lines",
)

urlpatterns += router.urls
