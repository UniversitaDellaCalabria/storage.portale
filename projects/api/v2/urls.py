from rest_framework.routers import DefaultRouter
from .views import (
    ProjectsViewSet,
    TerritorialScopesViewSet,
    ProgramTypesViewSet,
    InfrastructuresViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"projects", ProjectsViewSet, basename="projects")
router.register(
    r"territorial-scopes", TerritorialScopesViewSet, basename="territorial-scopes"
)
router.register(r"program-types", ProgramTypesViewSet, basename="program-types")
router.register(r"infrastructures", InfrastructuresViewSet, basename="infrastructures")

urlpatterns += router.urls
