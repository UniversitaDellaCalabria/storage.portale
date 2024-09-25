from django.urls import path

from .views import (
    ApiDepartmentDetail,
    ApiDepartmentsList,
    ApiStructureDetail,
    ApiStructureFunctionsList,
    ApiStructuresList,
    ApiStructureTypesList,
)

app_name="apiv1"

urlpatterns = [
    path('structures/', ApiStructuresList.as_view(), name='structures-list'),
    path('structuretypes/', ApiStructureTypesList.as_view(), name='structure-types'),
    path('structures/<str:structureid>/', ApiStructureDetail.as_view(), name='structure-detail'),
    path('functions/', ApiStructureFunctionsList.as_view(), name='functions'),
    path('departments/', ApiDepartmentsList.as_view(), name='departments-list'),
    path('departments/<str:departmentcod>/', ApiDepartmentDetail.as_view(), name='department-detail'),
]
