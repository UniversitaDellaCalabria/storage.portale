from django.urls import path
from .views import ApiCdsWebsiteDetail, ApiCdsWebsiteList

app_name = "apiv1"

urlpatterns = [
    path('cds-websites/', ApiCdsWebsiteList.as_view(), name='cds-websites-list'),
    path('cds-websites/<str:cdswebsitecod>/', ApiCdsWebsiteDetail.as_view(), name='cds-website-detail'),
]
