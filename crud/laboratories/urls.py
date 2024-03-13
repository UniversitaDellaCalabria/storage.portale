from django.urls import path

from . views import *

urlpatterns = []

#LaboratorioDatiBase
urlpatterns += path('laboratories/', laboratories, name='crud_laboratories'),
urlpatterns += path('laboratories/new/', laboratory_new, name='crud_laboratory_new'),
urlpatterns += path('laboratories/<str:code>/', laboratory, name='crud_laboratory_edit'),
urlpatterns += path('laboratories/<str:code>/delete/', laboratory_delete, name='crud_laboratory_delete'),
#LaboratorioDatiBaseInfoSede
urlpatterns += path('laboratories/<str:code>/edit-office/', laboratory_info_sede_edit, name='crud_laboratory_info_sede_edit'),
#LaboratorioDatiBaseInterdipartimentale
urlpatterns += path('laboratories/<str:code>/interdepartmental/', laboratory_interdepartmental_edit, name='crud_laboratory_interdepartmental_edit'),
# urlpatterns += path('laboratories/<str:code>/department/', laboratory_unical_department_edit, name='crud_laboratory_unical_department_edit'),
urlpatterns += path('laboratories/<str:code>/scientific-director/', laboratory_scientific_director_edit, name='crud_laboratory_scientific_director_edit'),
urlpatterns += path('laboratories/<str:code>/safety-manager/', laboratory_safety_manager_edit, name='crud_laboratory_safety_manager_edit'),
#LaboratorioAltriDipartimenti
urlpatterns += path('laboratories/<str:code>/extra-departments/new/', laboratory_extra_departments_new, name='crud_laboratory_extra_departments_new'),
urlpatterns += path('laboratories/<str:code>/extra-departments/<str:data_id>/delete/', laboratory_extra_departments_delete, name='crud_laboratory_extra_departments_delete'),
urlpatterns += path('laboratories/<str:code>/equipment/new/', laboratory_equipment_new, name='crud_laboratory_equipment_new'),
urlpatterns += path('laboratories/<str:code>/equipment/<str:data_id>/', laboratory_equipment_edit, name='crud_laboratory_equipment_edit'),
urlpatterns += path('laboratories/<str:code>/equipment/<str:data_id>/delete/', laboratory_equipment_delete, name='crud_laboratory_equipment_delete'),
#LaboratorioDatiRicerca
urlpatterns += path('laboratories/<str:code>/researches-erc1/', laboratory_researches_erc1_edit, name='crud_laboratory_researches_erc1_edit'),
#LaboratorioUbicazione
urlpatterns += path('laboratories/<str:code>/locations/new', laboratory_locations_new, name='crud_laboratory_locations_new'),
urlpatterns += path('laboratories/<str:code>/locations/<str:data_id>/', laboratory_locations_edit, name='crud_laboratory_locations_edit'),
urlpatterns += path('laboratories/<str:code>/locations/<str:data_id>/delete/', laboratory_locations_delete, name='crud_laboratory_locations_delete'),
#LaboratorioPersonaleRicerca
urlpatterns += path('laboratories/<str:code>/research-staff/new', laboratory_research_staff_new, name='crud_laboratory_research_staff_new'),
urlpatterns += path('laboratories/<str:code>/research-staff/<str:data_id>/delete/', laboratory_research_staff_delete, name='crud_laboratory_research_staff_delete'),
#LaboratorioPersonaleTecnico
urlpatterns += path('laboratories/<str:code>/technical-staff/new/', laboratory_technical_staff_new, name='crud_laboratory_technical_staff_new'),
urlpatterns += path('laboratories/<str:code>/technical-staff/<str:data_id>/delete/', laboratory_technical_staff_delete, name='crud_laboratory_technical_staff_delete'),
#LaboratorioAttivita
urlpatterns += path('laboratories/<str:code>/activities/new', laboratory_activities_new, name='crud_laboratory_activities_new'),
urlpatterns += path('laboratories/<str:code>/activities/<str:data_id>/', laboratory_activities_edit, name='crud_laboratory_activities_edit'),
urlpatterns += path('laboratories/<str:code>/activities/<str:data_id>/delete/', laboratory_activities_delete, name='crud_laboratory_activities_delete'),
#LaboratorioServiziErogati
urlpatterns += path('laboratories/<str:code>/provided-services/new', laboratory_provided_services_new, name='crud_laboratory_provided_services_new'),
urlpatterns += path('laboratories/<str:code>/provided-services/<str:data_id>/', laboratory_provided_services_edit, name='crud_laboratory_provided_services_edit'),
urlpatterns += path('laboratories/<str:code>/provided-services/<str:data_id>/delete/', laboratory_provided_services_delete, name='crud_laboratory_provided_services_delete'),
#LaboratorioServiziOfferti
urlpatterns += path('laboratories/<str:code>/offered-services/new', laboratory_offered_services_new, name='crud_laboratory_offered_services_new'),
urlpatterns += path('laboratories/<str:code>/offered-services/<str:data_id>/', laboratory_offered_services_edit, name='crud_laboratory_offered_services_edit'),
urlpatterns += path('laboratories/<str:code>/offered-services/<str:data_id>/delete/', laboratory_offered_services_delete, name='crud_laboratory_offered_services_delete'),
#LaboratorioTipologiaRischio
urlpatterns += path('laboratories/<str:code>/risk-types/', laboratory_risk_types_edit, name='crud_laboratory_risk_types_edit'),
#utils
urlpatterns += path('laboratories/<str:code>/request-approval/', laboratory_request_approval, name='crud_laboratory_request_approval'),
urlpatterns += path('laboratories/<str:code>/approve/', laboratory_approve, name='crud_laboratory_approve'),