from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('cds/', cds, name='crud_cds'),
urlpatterns += path('cds/<str:regdid_id>/', cds_detail,
                    name='crud_cds_detail'),
urlpatterns += path('cds/<str:regdid_id>/other-data/import/',
                    cds_other_data_import, name='crud_cds_other_data_import'),
urlpatterns += path('cds/<str:regdid_id>/other-data/new/',
                    cds_other_data_new, name='crud_cds_other_data_new'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/',
                    cds_other_data_edit, name='crud_cds_other_data_edit'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/delete/',
                    cds_other_data_delete, name='crud_cds_other_data_delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/',
                    cds_other_data_coordinator, name='crud_cds_other_data_coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/delete/',
                    cds_other_data_coordinator_delete, name='crud_cds_other_data_coordinator_delete'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/',
                    cds_other_data_deputy_coordinator, name='crud_cds_other_data_deputy_coordinator'),
urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/delete/',
                    cds_other_data_deputy_coordinator_delete, name='crud_cds_other_data_deputy_coordinator_delete'),
urlpatterns += path('cds/<str:regdid_id>/office-data/new/',
                    cds_office_data_new, name='crud_cds_office_data_new'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/',
                    cds_office_data_edit, name='crud_cds_office_data_edit'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/delete/',
                    cds_office_data_delete, name='crud_cds_office_data_delete'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/',
                    cds_office_data_responsible, name='crud_cds_office_data_responsible'),
urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/delete/',
                    cds_office_data_responsible_delete, name='crud_cds_office_data_responsible_delete'),
urlpatterns += path('cds/<str:regdid_id>/teaching-system/',
                    cds_doc_teaching_system, name='cds_doc_teaching_system'),
urlpatterns += path('cds/<str:regdid_id>/manifesto-and-regulation/',
                    cds_doc_manifesto_regulation, name='cds_doc_manifesto_regulation'),
urlpatterns += path('cds/<str:regdid_id>/teaching-system/delete/',
                    cds_doc_teaching_system_delete, name='cds_doc_teaching_system_delete'),
urlpatterns += path('cds/<str:regdid_id>/study-manifesto/delete/',
                    cds_doc_study_manifesto_delete, name='cds_doc_study_manifesto_delete'),
urlpatterns += path('cds/<str:regdid_id>/didactic-regulation/delete/',
                    cds_doc_didactic_regulation_delete, name='cds_doc_didactic_regulation_delete'),

# url groups
urlpatterns += path('cds/<str:regdid_id>/groups/new/',
                    cds_group_new, name='crud_cds_group_new'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/',
                    cds_group, name='crud_cds_group'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/delete/',
                    cds_group_delete, name='crud_cds_group_delete'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/new/',
                    cds_group_members_new, name='cds_group_members_new'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/<str:member_id>/edit/',
                    cds_group_member_edit, name='cds_group_member_edit'),
urlpatterns += path('cds/<str:regdid_id>/groups/<str:group_id>/members/<str:member_id>/delete/',
                    cds_group_member_delete, name='cds_group_member_delete'),

# regdid other data (multimedia)
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:other_data_type_id>/new/',
                    cds_regdid_other_data_new, name='crud_cds_regdid_other_data_new'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:data_id>/edit/',
                    cds_regdid_other_data_edit, name='crud_cds_regdid_other_data_edit'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/<str:data_id>/delete/',
                    cds_regdid_other_data_delete, name='crud_cds_regdid_other_data_delete'),
urlpatterns += path('cds/<str:regdid_id>/regdid-other-data/import/',
                    cds_regdid_other_data_import, name='crud_cds_regdid_other_data_import'),