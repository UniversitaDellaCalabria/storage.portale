from django.urls import path
from .views import ApiCdsBrochureDetail, ApiCdsBrochureList

app_name = "apiv1"

urlpatterns = [
    path('cds-brochures/', ApiCdsBrochureList.as_view(), name='cds-brochures-list'),
    path('cds-brochures/<str:cds_cod>/', ApiCdsBrochureDetail.as_view(), name='cds-brochure-detail'),
]
