from django.urls import path

from .views import (
    project,
    project_delete,
    project_director_delete,
    project_director_edit,
    project_director_new,
    project_new,
    project_researcher_delete,
    project_researcher_edit,
    project_researcher_new,
    project_structure_data_edit,
    projects,
)

app_name = "management"

urlpatterns = []


urlpatterns += path('projects/', projects, name='projects'),
urlpatterns += path('projects/new/', project_new, name='project-new'),
urlpatterns += path('projects/<str:code>/', project, name='project-edit'),
urlpatterns += path('projects/<str:code>/delete/', project_delete, name='project-delete'),
urlpatterns += path('projects/<str:code>/director/new/', project_director_new, name='project-director-new'),
urlpatterns += path('projects/<str:code>/director-data/<str:director_id>/', project_director_edit, name='project-director-edit'),
urlpatterns += path('projects/<str:code>/director/<str:director_id>/delete/', project_director_delete, name='project-director-delete'),
urlpatterns += path('projects/<str:code>/researcher/new/', project_researcher_new, name='project-researcher-new'),
urlpatterns += path('projects/<str:code>/researcher-data/<str:researcher_id>/', project_researcher_edit, name='project-researcher-edit'),
urlpatterns += path('projects/<str:code>/researcher/<str:researcher_id>/delete/', project_researcher_delete, name='project-researcher-delete'),
urlpatterns += path('projects/<str:code>/structure-data/<str:data_id>/', project_structure_data_edit, name='project-structure-data-edit'),
