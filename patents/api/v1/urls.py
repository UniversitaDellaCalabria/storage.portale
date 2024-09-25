from django.urls import path

from .views import ApiPatentDetail, ApiPatentsList

app_name="apiv1"

urlpatterns = [
    path('patents/', ApiPatentsList.as_view(), name='patents'),
    path('patents/<str:patentid>', ApiPatentDetail.as_view(), name='patent-detail'),
]
