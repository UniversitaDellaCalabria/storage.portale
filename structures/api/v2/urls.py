from rest_framework.routers import DefaultRouter
from .views import StructuresViewSet, TypesViewSet, FunctionViewSet, DepartmentsViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"structures", StructuresViewSet, basename="structures")
router.register(r"structuretypes", TypesViewSet, basename="structures-types")
router.register(r"functions", FunctionViewSet, basename="functions")
router.register(r"departments", DepartmentsViewSet, basename="departments")
urlpatterns += router.urls
