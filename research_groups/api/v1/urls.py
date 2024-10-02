from django.urls import path

from .views import ApiResearchGroupsList

app_name = "apiv1"

urlpatterns = [
    path('researchgroups/', ApiResearchGroupsList.as_view(), name='research-groups'),
]
