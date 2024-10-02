from django.urls import path
from .views import ApiAllResearchLinesList, ApiAppliedResearchLinesList, ApiBaseResearchLinesList

app_name = "apiv1"

urlpatterns = [
    path('baseresearchlines/', ApiBaseResearchLinesList.as_view(), name='base-research-lines'),
    path('appliedresearchlines/', ApiAppliedResearchLinesList.as_view(), name='applied-research-lines'),
    path('allresearchlines/', ApiAllResearchLinesList.as_view(), name='all-research-lines'),
]
