from django.urls import path

from .views import (
    cds,
    cds_detail,
    cds_doc_didactic_regulation_delete,
    cds_doc_manifesto_regulation,
    cds_doc_study_manifesto_delete,
    cds_doc_teaching_system,
    cds_doc_teaching_system_delete,
    cds_group,
    cds_group_delete,
    cds_group_member_delete,
    cds_group_member_edit,
    cds_group_members_new,
    cds_group_new,
    cds_office_data_delete,
    cds_office_data_edit,
    cds_office_data_new,
    cds_office_data_responsible,
    cds_office_data_responsible_delete,
    cds_other_data_coordinator,
    cds_other_data_coordinator_delete,
    cds_other_data_delete,
    cds_other_data_deputy_coordinator,
    cds_other_data_deputy_coordinator_delete,
    cds_other_data_edit,
    cds_other_data_import,
    cds_other_data_new,
    cds_regdid_other_data_delete,
    cds_regdid_other_data_edit,
    cds_regdid_other_data_import,
    cds_regdid_other_data_new,
)

app_name = "management"


urlpatterns = []


urlpatterns += path('cds/', cds, name='cds'),
urlpatterns += path('cds/<str:regdid_id>/', cds_detail, name='cds-detail'),
urlpatterns += path('cds/<str:regdid_id>/other-data/import/', cds_other_data_import, name='cds-other-data-import'),
urlpatterns += path('cds/<str:regdid_id>/other-data/new/', cds_other_data_new, name='cds-other-data-new'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/', cds_other_data_edit, name='cds-other-data-edit'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/delete/', cds_other_data_delete, name='cds-other-data-delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/', cds_other_data_coordinator, name='cds-other-data-coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/delete/', cds_other_data_coordinator_delete, name='cds-other-data-coordinator-delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/', cds_other_data_deputy_coordinator, name='cds-other-data-deputy-coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/delete/', cds_other_data_deputy_coordinator_delete, name='cds-other-data-deputy-coordinator-delete'),
urlpatterns += path('cds/<str:regdid_id>/office-data/new/', cds_office_data_new, name='cds-office-data-new'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/', cds_office_data_edit, name='cds-office-data-edit'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/delete/', cds_office_data_delete, name='cds-office-data-delete'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/', cds_office_data_responsible, name='cds-office-data-responsible'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/delete/', cds_office_data_responsible_delete, name='cds-office-data-responsible-delete'),
urlpatterns += path('cds/<str:regdid_id>/teaching-system/', cds_doc_teaching_system, name='cds-doc-teaching-system'),
urlpatterns += path('cds/<str:regdid_id>/teaching-system/delete/', cds_doc_teaching_system_delete, name='cds-doc-teaching-system-delete'),
urlpatterns += path('cds/<str:regdid_id>/manifesto-and-regulation/', cds_doc_manifesto_regulation, name='cds-doc-manifesto-regulation'),
urlpatterns += path('cds/<str:regdid_id>/study-manifesto/delete/', cds_doc_study_manifesto_delete, name='cds-doc-study-manifesto-delete'),
urlpatterns += path('cds/<str:regdid_id>/didactic-regulation/delete/', cds_doc_didactic_regulation_delete, name='cds-doc-didactic-regulation-delete'),

# url groups
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/', cds_group, name='cds-group'),
urlpatterns += path('cds/<str:regdid_id>/groups/new/', cds_group_new, name='cds-group-new'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/delete/', cds_group_delete, name='cds-group-delete'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/new/', cds_group_members_new, name='cds-group-members-new'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/<str:member_id>/edit/', cds_group_member_edit, name='cds-group-member-edit'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/<str:member_id>/delete/', cds_group_member_delete, name='cds-group-member-delete'),

# regdid other data (multimedia)
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:other_data_type_id>/new/', cds_regdid_other_data_new, name='cds-regdid-other-data-new'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:data_id>/edit/', cds_regdid_other_data_edit, name='cds-regdid-other-data-edit'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:data_id>/delete/', cds_regdid_other_data_delete, name='cds-regdid-other-data-delete'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/import/', cds_regdid_other_data_import, name='cds-regdid-other-data-import'),
