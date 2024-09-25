from django.urls import path

from .views import ApiCompaniesList, ApiCompanyDetail, ApiTechAreasList

app_name="apiv1"

urlpatterns = [
    path('companies/', ApiCompaniesList.as_view(),name='companies'),
    path('companies/<str:companyid>/', ApiCompanyDetail.as_view(),name='company-detail'),
    path('tech-areas/', ApiTechAreasList.as_view(),name='tech-areas-list'),   
]
