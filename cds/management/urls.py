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


urlpatterns = [
    path('cds/', cds, name='cds'),
    path('cds/<int:regdid_id>/', cds_detail, name='cds-detail'),
    path('cds/<int:regdid_id>/other-data/import/', cds_other_data_import, name='cds-other-data-import'),
    path('cds/<int:regdid_id>/other-data/new/', cds_other_data_new, name='cds-other-data-new'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/', cds_other_data_edit, name='cds-other-data-edit'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/delete/', cds_other_data_delete, name='cds-other-data-delete'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/coordinator/', cds_other_data_coordinator, name='cds-other-data-coordinator'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/coordinator/delete/', cds_other_data_coordinator_delete, name='cds-other-data-coordinator-delete'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/deputy-coordinator/', cds_other_data_deputy_coordinator, name='cds-other-data-deputy-coordinator'),
    path('cds/<int:regdid_id>/other-data/<int:data_id>/deputy-coordinator/delete/', cds_other_data_deputy_coordinator_delete, name='cds-other-data-deputy-coordinator-delete'),
    path('cds/<int:regdid_id>/office-data/new/', cds_office_data_new, name='cds-office-data-new'),
    path('cds/<int:regdid_id>/office-data/<int:data_id>/', cds_office_data_edit, name='cds-office-data-edit'),
    path('cds/<int:regdid_id>/office-data/<int:data_id>/delete/', cds_office_data_delete, name='cds-office-data-delete'),
    path('cds/<int:regdid_id>/office-data/<int:data_id>/responsible/', cds_office_data_responsible, name='cds-office-data-responsible'),
    path('cds/<int:regdid_id>/office-data/<int:data_id>/responsible/delete/', cds_office_data_responsible_delete, name='cds-office-data-responsible-delete'),
    path('cds/<int:regdid_id>/teaching-system/', cds_doc_teaching_system, name='cds-doc-teaching-system'),
    path('cds/<int:regdid_id>/teaching-system/delete/', cds_doc_teaching_system_delete, name='cds-doc-teaching-system-delete'),
    path('cds/<int:regdid_id>/manifesto-and-regulation/', cds_doc_manifesto_regulation, name='cds-doc-manifesto-regulation'),
    path('cds/<int:regdid_id>/study-manifesto/delete/', cds_doc_study_manifesto_delete, name='cds-doc-study-manifesto-delete'),
    path('cds/<int:regdid_id>/didactic-regulation/delete/', cds_doc_didactic_regulation_delete, name='cds-doc-didactic-regulation-delete'),

    # url groups
    path('cds/<int:regdid_id>/groups/<int:group_id>/', cds_group, name='cds-group'),
    path('cds/<int:regdid_id>/groups/new/', cds_group_new, name='cds-group-new'),
    path('cds/<int:regdid_id>/groups/<int:group_id>/delete/', cds_group_delete, name='cds-group-delete'),
    path('cds/<int:regdid_id>/groups/<int:group_id>/members/new/', cds_group_members_new, name='cds-group-members-new'),
    path('cds/<int:regdid_id>/groups/<int:group_id>/members/<int:member_id>/edit/', cds_group_member_edit, name='cds-group-member-edit'),
    path('cds/<int:regdid_id>/groups/<int:group_id>/members/<int:member_id>/delete/', cds_group_member_delete, name='cds-group-member-delete'),

    # regdid other data (multimedia)
    path('cds/<int:regdid_id>/regdid-other-data/<int:other_data_type_id>/new/', cds_regdid_other_data_new, name='cds-regdid-other-data-new'),
    path('cds/<int:regdid_id>/regdid-other-data/<int:data_id>/edit/', cds_regdid_other_data_edit, name='cds-regdid-other-data-edit'),
    path('cds/<int:regdid_id>/regdid-other-data/<int:data_id>/delete/', cds_regdid_other_data_delete, name='cds-regdid-other-data-delete'),
    path('cds/<int:regdid_id>/regdid-other-data/import/', cds_regdid_other_data_import, name='cds-regdid-other-data-import'),
]
