from django.urls import path

from .views import (
    ApiHighFormationCourseTypesList,
    ApiHighFormationMastersDetail,
    ApiHighFormationMastersList,
)

app_name="apiv1"

urlpatterns = [
    path('high-formation-masters/', ApiHighFormationMastersList.as_view(), name='high-formation-masters'),
    path('high-formation-masters/<int:id>/', ApiHighFormationMastersDetail.as_view(), name='high-formation-master-detail'),
    path('high-formation-course-types/', ApiHighFormationCourseTypesList.as_view(), name='high-formation-course-types'),
]