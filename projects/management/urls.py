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

urlpatterns = [
    path('projects/', projects, name='projects'),
    path('projects/new/', project_new, name='project-new'),
    path('projects/<int:project_id>/', project, name='project-edit'),
    path('projects/<int:project_id>/delete/', project_delete, name='project-delete'),
    path('projects/<int:project_id>/director/new/', project_director_new, name='project-director-new'),
    path('projects/<int:project_id>/director-data/<int:director_id>/', project_director_edit, name='project-director-edit'),
    path('projects/<int:project_id>/director/<int:director_id>/delete/', project_director_delete, name='project-director-delete'),
    path('projects/<int:project_id>/researcher/new/', project_researcher_new, name='project-researcher-new'),
    path('projects/<int:project_id>/researcher-data/<int:researcher_id>/', project_researcher_edit, name='project-researcher-edit'),
    path('projects/<int:project_id>/researcher/<int:researcher_id>/delete/', project_researcher_delete, name='project-researcher-delete'),
    path('projects/<int:project_id>/structure-data/<int:data_id>/', project_structure_data_edit, name='project-structure-data-edit'),
]
