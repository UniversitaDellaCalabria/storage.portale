from rest_framework.routers import DefaultRouter
from .views import BrochuresViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"cds-brochures", BrochuresViewSet, basename="cds-brochures")
urlpatterns += router.urls
