from rest_framework.routers import DefaultRouter
from .views import ResearchGroupsViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"researchgroups", ResearchGroupsViewSet, basename="research-groups")
urlpatterns += router.urls
