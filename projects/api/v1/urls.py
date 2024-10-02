from django.urls import path

from .views import (
    ApiProjectDetail,
    ApiProjectsInfrastructuresList,
    ApiProjectsList,
    ApiProjectsProgramTypesList,
    ApiProjectsTerritorialScopesList,
)

app_name = "apiv1"

urlpatterns = [
    path('projects/', ApiProjectsList.as_view(), name='projects'),
    path('projects/<str:projectid>/', ApiProjectDetail.as_view(), name='project-detail'),
    path('projects-territorial-scopes/', ApiProjectsTerritorialScopesList.as_view(), name='projects-territorial-scopes'),
    path('projects-program-types/', ApiProjectsProgramTypesList.as_view(), name='projects-program-types'),
    path('projects-infrastructures/', ApiProjectsInfrastructuresList.as_view(), name='projects-infrastructures'),
]
