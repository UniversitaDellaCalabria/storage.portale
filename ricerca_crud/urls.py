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


urlpatterns += path('patents/', patents, name='crud_patents'),
urlpatterns += path('patents/new/', patent_new, name='crud_patent_new'),
urlpatterns += path('patents/<str:code>/', patent, name='crud_patent_edit'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>', patent_inventor, name='crud_patent_inventor'),
urlpatterns += path('patents/<str:code>/inventor/new/', patent_inventor_new, name='crud_patent_inventor_new'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/delete/', patent_inventor_delete, name='crud_patent_inventor_delete'),
# urlpatterns += path('patents/<str:code>/delete/', patent_delete, name='crud_patent_delete'),

