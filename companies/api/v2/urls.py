from rest_framework.routers import DefaultRouter
from .views import CompaniesViewSet, TechAreaViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"companies", CompaniesViewSet, basename="companies")
router.register(r"tech-areas", TechAreaViewSet, basename="tech-areas")

urlpatterns += router.urls