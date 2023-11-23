from django.urls import path

from . views import project, project_delete, project_director_delete, project_director_edit, project_director_new, project_new, project_researcher_delete, project_researcher_edit, project_researcher_new, project_structure_data_edit, projects


urlpatterns = []

urlpatterns += path('projects/', projects, name='crud_projects'),
urlpatterns += path('projects/new/', project_new, name='crud_project_new'),
urlpatterns += path('projects/<str:code>/', project, name='crud_project_edit'),
urlpatterns += path('projects/<str:code>/structure-data/<str:data_id>/',
                    project_structure_data_edit, name='crud_project_structure_data_edit'),
urlpatterns += path('projects/<str:code>/director-data/<str:director_id>/',
                    project_director_edit, name='crud_project_director_edit'),
urlpatterns += path('projects/<str:code>/director/new/',
                    project_director_new, name='crud_project_director_new'),
urlpatterns += path('projects/<str:code>/director/<str:director_id>/delete/',
                    project_director_delete, name='crud_project_director_delete'),
urlpatterns += path('projects/<str:code>/researcher-data/<str:researcher_id>/',
                    project_researcher_edit, name='crud_project_researcher_edit'),
urlpatterns += path('projects/<str:code>/researcher/new/',
                    project_researcher_new, name='crud_project_researcher_new'),
urlpatterns += path('projects/<str:code>/researcher/<str:researcher_id>/delete/',
                    project_researcher_delete, name='crud_project_researcher_delete'),
urlpatterns += path('projects/<str:code>/delete/',
                    project_delete, name='crud_project_delete'),
