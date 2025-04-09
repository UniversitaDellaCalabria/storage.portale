from rest_framework.routers import DefaultRouter
from .views import BaseResearchLinesViewSet#, AppliedResearchLinesViewSet, AllResearchLinesViewSet
app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"baseresearchlines", BaseResearchLinesViewSet, basename="baseresearchlines")
# router.register(r"appliedresearchlines", AppliedResearchLinesViewSet, basename="appliedresearchlines")
# router.register(r"allresearchlines", AllResearchLinesViewSet, basename="allresearchlines")

urlpatterns += router.urls
