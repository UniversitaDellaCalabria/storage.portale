from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('cds-websites/', cds_websites, name='crud_cdswebsites'),
urlpatterns += path('cds-websites/<str:code>/', cds_website, name='crud_cds_website_edit'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/new/', cds_other_data_new, name='crud_cds_other_data_new'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/', cds_other_data_edit, name='crud_cds_other_data_edit'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/delete/', cds_other_data_delete, name='crud_cds_other_data_delete'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/', cds_other_data_coordinator, name='crud_cds_other_data_coordinator'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/coordinator/delete/', cds_other_data_coordinator_delete, name='crud_cds_other_data_coordinator_delete'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/', cds_other_data_deputy_coordinator, name='crud_cds_other_data_deputy_coordinator'),
# urlpatterns += path('cds/<str:regdid_id>/other-data/<str:data_id>/deputy-coordinator/delete/', cds_other_data_deputy_coordinator_delete, name='crud_cds_other_data_deputy_coordinator_delete'),
# urlpatterns += path('cds/<str:regdid_id>/office-data/new/', cds_office_data_new, name='crud_cds_office_data_new'),
# urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/', cds_office_data_edit, name='crud_cds_office_data_edit'),
# urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/delete/', cds_office_data_delete, name='crud_cds_office_data_delete'),
# urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/', cds_office_data_responsible, name='crud_cds_office_data_responsible'),
# urlpatterns += path('cds/<str:regdid_id>/office-data/<str:data_id>/responsible/delete/', cds_office_data_responsible_delete, name='crud_cds_office_data_responsible_delete'),
