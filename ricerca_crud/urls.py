from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, re_path

from . views import *

urlpatterns = []

urlpatterns += path('', home, name='crud_dashboard'),

# research groups
urlpatterns += path('researchgroups/', researchgroups, name='crud_researchgroups'),
urlpatterns += path('researchgroups/new/', researchgroup_new, name='crud_researchgroup_new'),
urlpatterns += path('researchgroups/<str:code>/', researchgroup, name='crud_researchgroup_edit'),
urlpatterns += path('researchgroups/<str:code>/delete/', researchgroup_delete, name='crud_researchgroup_delete'),
urlpatterns += path('researchgroups/<str:code>/teacher/new/', researchgroup_teacher_new, name='crud_researchgroup_teacher_new'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/', researchgroup_teacher_edit, name='crud_researchgroup_teacher_edit'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/delete/', researchgroup_teacher_delete, name='crud_researchgroup_teacher_delete'),

# research lines
urlpatterns += path('baseresearchlines/', base_researchlines, name='crud_base_researchlines'),
urlpatterns += path('appliedresearchlines/', applied_researchlines, name='crud_applied_researchlines'),
urlpatterns += path('appliedresearchlines/new/', researchline_new_applied, name='crud_researchline_new_applied'),
urlpatterns += path('baseresearchlines/new/', researchline_new_base, name='crud_researchline_new_base'),
urlpatterns += path('baseresearchlines/<str:code>/', base_researchline, name='crud_base_researchline_edit'),
urlpatterns += path('appliedresearchlines/<str:code>/', applied_researchline, name='crud_applied_researchline_edit'),
urlpatterns += path('baseresearchlines/<str:code>/delete/', base_researchline_delete, name='crud_base_researchline_delete'),
urlpatterns += path('appliedresearchlines/<str:code>/delete/', applied_researchline_delete, name='crud_applied_researchline_delete'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/new/', base_researchline_teacher_new, name='crud_base_researchline_teacher_new'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/new/', applied_researchline_teacher_new, name='crud_applied_researchline_teacher_new'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', base_researchline_teacher_edit, name='crud_base_researchline_teacher_edit'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', applied_researchline_teacher_edit, name='crud_applied_researchline_teacher_edit'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', base_researchline_teacher_delete, name='crud_base_researchline_teacher_delete'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', applied_researchline_teacher_delete, name='crud_applied_researchline_teacher_delete'),

# cds
urlpatterns += path('cds/', cds, name='crud_cds'),
urlpatterns += path('cds/<str:regdid_id>/', cds_detail, name='crud_cds_detail'),
urlpatterns += path('cds/<str:regdid_id>/other-data/new/', cds_other_data_new, name='crud_cds_other_data_new'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/', cds_other_data_edit, name='crud_cds_other_data_edit'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/delete/', cds_other_data_delete, name='crud_cds_other_data_delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/', cds_other_data_coordinator, name='crud_cds_other_data_coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/delete/', cds_other_data_coordinator_delete, name='crud_cds_other_data_coordinator_delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/', cds_other_data_deputy_coordinator, name='crud_cds_other_data_deputy_coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/delete/', cds_other_data_deputy_coordinator_delete, name='crud_cds_other_data_deputy_coordinator_delete'),

urlpatterns += path('cds/<str:regdid_id>/office-data/new/', cds_office_data_new, name='crud_cds_office_data_new'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/', cds_office_data_edit, name='crud_cds_office_data_edit'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/delete/', cds_office_data_delete, name='crud_cds_office_data_delete'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/', cds_office_data_responsible, name='crud_cds_office_data_responsible'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/delete/', cds_office_data_responsible_delete, name='crud_cds_office_data_responsible_delete'),

# patents
urlpatterns += path('patents/', patents, name='crud_patents'),
urlpatterns += path('patents/new/', patent_new, name='crud_patent_new'),
urlpatterns += path('patents/<str:code>/', patent, name='crud_patent_edit'),
urlpatterns += path('patents/<str:code>/inventor-data/<str:inventor_id>/', patent_inventor_data, name='crud_patent_inventor_data'),
urlpatterns += path('patents/<str:code>/inventor-data/<str:inventor_id>/inventor/', patent_inventor_data_edit, name='crud_patent_inventor_data_edit'),
urlpatterns += path('patents/<str:code>/inventor/new/', patent_inventor_new, name='crud_patent_inventor_new'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/delete/', patent_inventor_delete, name='crud_patent_inventor_delete'),
urlpatterns += path('patents/<str:code>/delete/', patent_delete, name='crud_patent_delete'),


# companies
urlpatterns += path('companies/', companies, name='crud_companies'),
urlpatterns += path('companies/new/', company_new, name='crud_company_new'),
urlpatterns += path('companies/<str:code>/', company, name='crud_company_edit'),
urlpatterns += path('companies/<str:code>/teacher-data/<str:data_id>/', company_unical_referent_data, name='crud_company_unical_referent_data'),
urlpatterns += path('companies/<str:code>/teacher-data/<str:data_id>/unical-referent/', company_unical_referent_data_edit, name='crud_company_unical_referent_data_edit'),
urlpatterns += path('companies/<str:code>/teacher-data/<str:data_id>/unical-referent/delete/', company_unical_referent_data_delete, name='crud_company_unical_referent_data_delete'),
urlpatterns += path('companies/<str:code>/department-data/new/', company_unical_department_data_new, name='crud_company_unical_department_data_new'),
urlpatterns += path('companies/<str:code>/department-data/<str:department_id>/', company_unical_department_data_edit, name='crud_company_unical_department_data_edit'),
urlpatterns += path('companies/<str:code>/department-data/<str:department_id>/delete', company_unical_department_data_delete, name='crud_company_unical_department_data_delete'),
urlpatterns += path('companies/<str:code>/delete/', company_delete, name='crud_company_delete'),


# projects
urlpatterns += path('projects/', projects, name='crud_projects'),
urlpatterns += path('projects/new/', project_new, name='crud_project_new'),
urlpatterns += path('projects/<str:code>/', project, name='crud_project_edit'),
urlpatterns += path('projects/<str:code>/structure-data/<str:data_id>/', project_structure_data_edit, name='crud_project_structure_data_edit'),
urlpatterns += path('projects/<str:code>/director-data/<str:director_id>/', project_director_data, name='crud_project_director_data'),
urlpatterns += path('projects/<str:code>/director-data/<str:director_id>/director/', project_director_data_edit, name='crud_project_director_data_edit'),
urlpatterns += path('projects/<str:code>/director/new/', project_director_new, name='crud_project_director_new'),
urlpatterns += path('projects/<str:code>/director/<str:director_id>/delete/', project_director_delete, name='crud_project_director_delete'),
urlpatterns += path('projects/<str:code>/researcher-data/<str:researcher_id>/', project_researcher_data, name='crud_project_researcher_data'),
urlpatterns += path('projects/<str:code>/researcher-data/<str:researcher_id>/researcher/', project_researcher_data_edit, name='crud_project_researcher_data_edit'),
urlpatterns += path('projects/<str:code>/researcher/new/', project_researcher_new, name='crud_project_researcher_new'),
urlpatterns += path('projects/<str:code>/researcher/<str:researcher_id>/delete/', project_researcher_delete, name='crud_project_researcher_delete'),
urlpatterns += path('projects/<str:code>/delete/', project_delete, name='crud_project_delete'),



# teachers
urlpatterns += path('teachers/', teachers, name='crud_teachers'),
urlpatterns += path('teachers/<str:code>/', teacher_detail, name='crud_teacher_edit'),
urlpatterns += path('teachers/<str:code>/other-data/new/', teacher_other_data_new, name='crud_teacher_other_data_new'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/', teacher_other_data_edit, name='crud_teacher_other_data_edit'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/delete/', teacher_other_data_delete, name='crud_teacher_other_data_delete'),
urlpatterns += path('teachers/<str:code>/board-data/new/', teacher_board_data_new, name='crud_teacher_board_data_new'),
urlpatterns += path('teachers/<str:code>/board-data/<str:data_id>/', teacher_board_data_edit, name='crud_teacher_board_data_edit'),
urlpatterns += path('teachers/<str:code>/board-data/<str:data_id>/delete/', teacher_board_data_delete, name='crud_teacher_board_data_delete'),
urlpatterns += path('teachers/<str:code>/teaching-material-data/new/', teacher_materials_data_new, name='crud_teacher_materials_data_new'),
urlpatterns += path('teachers/<str:code>/teaching-material-data/<str:data_id>/', teacher_materials_data_edit, name='crud_teacher_materials_data_edit'),
urlpatterns += path('teachers/<str:code>/teaching-material-data/<str:data_id>/delete/', teacher_materials_data_delete, name='crud_teacher_materials_data_delete'),


# doctorates
urlpatterns += path('doctorates/', doctorates, name='crud_doctorates'),
urlpatterns += path('doctorates/new/', doctorate_new, name='crud_doctorate_new'),
urlpatterns += path('doctorates/<str:code>/', doctorate, name='crud_doctorate_edit'),
urlpatterns += path('doctorates/<str:code>/main-teachers-data/<str:teacher_id>/', doctorate_main_teacher_data, name='crud_doctorate_main_teacher_data'),
urlpatterns += path('doctorates/<str:code>/main-teachers-data/<str:teacher_id>/teacher/', doctorate_main_teacher_data_edit, name='crud_doctorate_main_teacher_data_edit'),
urlpatterns += path('doctorates/<str:code>/main-teacher/new/', doctorate_main_teacher_new, name='crud_doctorate_main_teacher_new'),
urlpatterns += path('doctorates/<str:code>/main-teacher/<str:teacher_id>/delete/', doctorate_main_teacher_delete, name='crud_doctorate_main_teacher_delete'),
urlpatterns += path('doctorates/<str:code>/other-teachers-data/<str:teacher_id>/', doctorate_other_teacher_data, name='crud_doctorate_other_teacher_data'),
urlpatterns += path('doctorates/<str:code>/other-teachers-data/<str:teacher_id>/teacher/', doctorate_other_teacher_data_edit, name='crud_doctorate_other_teacher_data_edit'),
urlpatterns += path('doctorates/<str:code>/other-teacher/new/', doctorate_other_teacher_new, name='crud_doctorate_other_teacher_new'),
urlpatterns += path('doctorates/<str:code>/other-teacher/<str:teacher_id>/delete/', doctorate_other_teacher_delete, name='crud_doctorate_other_teacher_delete'),
urlpatterns += path('doctorates/<str:code>/delete/', doctorate_delete, name='crud_doctorate_delete'),














