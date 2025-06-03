from rest_framework.routers import DefaultRouter
from .views import PatentsViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"patents", PatentsViewSet, basename="patents")
urlpatterns += router.urls
