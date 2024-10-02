from django.urls import path

from .views import (
    laboratories,
    laboratory,
    laboratory_activities_delete,
    laboratory_activities_edit,
    laboratory_activities_new,
    laboratory_approve,
    laboratory_delete,
    laboratory_equipment_delete,
    laboratory_equipment_edit,
    laboratory_equipment_new,
    laboratory_equipment_value_edit,
    laboratory_extra_departments_delete,
    laboratory_extra_departments_new,
    laboratory_info_sede_edit,
    laboratory_interdepartmental_edit,
    laboratory_locations_delete,
    laboratory_locations_edit,
    laboratory_locations_new,
    laboratory_new,
    laboratory_offered_services_delete,
    laboratory_offered_services_edit,
    laboratory_offered_services_new,
    laboratory_provided_services_delete,
    laboratory_provided_services_edit,
    laboratory_provided_services_new,
    laboratory_request_approval,
    laboratory_research_staff_delete,
    laboratory_research_staff_new,
    laboratory_researches_erc1_edit,
    laboratory_risk_types_edit,
    laboratory_safety_manager_edit,
    laboratory_scientific_director_edit,
    laboratory_scope_edit,
    laboratory_technical_staff_delete,
    laboratory_technical_staff_new,
)

app_name = "management"

urlpatterns = []


# LaboratorioDatiBase
urlpatterns += path('laboratories/', laboratories, name='laboratories'),
urlpatterns += path('laboratories/new/', laboratory_new, name='laboratory-new'),
urlpatterns += path('laboratories/<str:code>/', laboratory, name='laboratory-edit'),
urlpatterns += path('laboratories/<str:code>/delete/', laboratory_delete, name='laboratory-delete'),
# LaboratorioDatiBaseAmbitoForm
urlpatterns += path('laboratories/<str:code>/scope/', laboratory_scope_edit, name='laboratory-scope-edit'),
# LaboratorioDatiBaseInfoSede
urlpatterns += path('laboratories/<str:code>/edit-office/', laboratory_info_sede_edit, name='laboratory-info-sede-edit'),
# LaboratorioDatiBaseStrumentazioneValore
urlpatterns += path('laboratories/<str:code>/equipment-value/', laboratory_equipment_value_edit, name='laboratory-equipment-value-edit'),
# LaboratorioDatiBaseInterdipartimentale
urlpatterns += path('laboratories/<str:code>/interdepartmental/', laboratory_interdepartmental_edit, name='laboratory-interdepartmental-edit'),
urlpatterns += path('laboratories/<str:code>/scientific-director/', laboratory_scientific_director_edit, name='laboratory-scientific-director-edit'),
urlpatterns += path('laboratories/<str:code>/safety-manager/', laboratory_safety_manager_edit, name='laboratory-safety-manager-edit'),
# LaboratorioAltriDipartimenti
urlpatterns += path('laboratories/<str:code>/extra-departments/new/', laboratory_extra_departments_new, name='laboratory-extra-departments-new'),
urlpatterns += path('laboratories/<str:code>/extra-departments/<str:data_id>/delete/', laboratory_extra_departments_delete, name='laboratory-extra-departments-delete'),
urlpatterns += path('laboratories/<str:code>/equipment/new/', laboratory_equipment_new, name='laboratory-equipment-new'),
urlpatterns += path('laboratories/<str:code>/equipment/<str:data_id>/', laboratory_equipment_edit, name='laboratory-equipment-edit'),
urlpatterns += path('laboratories/<str:code>/equipment/<str:data_id>/delete/', laboratory_equipment_delete, name='laboratory-equipment-delete'),
# LaboratorioDatiRicerca
urlpatterns += path('laboratories/<str:code>/researches-erc1/', laboratory_researches_erc1_edit, name='laboratory-researches-erc1-edit'),
# LaboratorioUbicazione
urlpatterns += path('laboratories/<str:code>/locations/new/', laboratory_locations_new, name='laboratory-locations-new'),
urlpatterns += path('laboratories/<str:code>/locations/<str:data_id>/', laboratory_locations_edit, name='laboratory-locations-edit'),
urlpatterns += path('laboratories/<str:code>/locations/<str:data_id>/delete/', laboratory_locations_delete, name='laboratory-locations-delete'),
# LaboratorioPersonaleRicerca
urlpatterns += path('laboratories/<str:code>/research-staff/new/', laboratory_research_staff_new, name='laboratory-research-staff-new'),
urlpatterns += path('laboratories/<str:code>/research-staff/<str:data_id>/delete/', laboratory_research_staff_delete, name='laboratory-research-staff-delete'),
# LaboratorioPersonaleTecnico
urlpatterns += path('laboratories/<str:code>/technical-staff/new/', laboratory_technical_staff_new, name='laboratory-technical-staff-new'),
urlpatterns += path('laboratories/<str:code>/technical-staff/<str:data_id>/delete/', laboratory_technical_staff_delete, name='laboratory-technical-staff-delete'),
# LaboratorioAttivita
urlpatterns += path('laboratories/<str:code>/activities/new/', laboratory_activities_new, name='laboratory-activities-new'),
urlpatterns += path('laboratories/<str:code>/activities/<str:data_id>/', laboratory_activities_edit, name='laboratory-activities-edit'),
urlpatterns += path('laboratories/<str:code>/activities/<str:data_id>/delete/', laboratory_activities_delete, name='laboratory-activities-delete'),
# LaboratorioServiziErogati
urlpatterns += path('laboratories/<str:code>/provided-services/new/', laboratory_provided_services_new, name='laboratory-provided-services-new'),
urlpatterns += path('laboratories/<str:code>/provided-services/<str:data_id>/', laboratory_provided_services_edit, name='laboratory-provided-services-edit'),
urlpatterns += path('laboratories/<str:code>/provided-services/<str:data_id>/delete/', laboratory_provided_services_delete, name='laboratory-provided-services-delete'),
# LaboratorioServiziOfferti
urlpatterns += path('laboratories/<str:code>/offered-services/new/', laboratory_offered_services_new, name='laboratory-offered-services-new'),
urlpatterns += path('laboratories/<str:code>/offered-services/<str:data_id>/', laboratory_offered_services_edit, name='laboratory-offered-services-edit'),
urlpatterns += path('laboratories/<str:code>/offered-services/<str:data_id>/delete/', laboratory_offered_services_delete, name='laboratory-offered-services-delete'),
# LaboratorioTipologiaRischio
urlpatterns += path('laboratories/<str:code>/risk-types/', laboratory_risk_types_edit, name='laboratory-risk-types-edit'),
# utils
urlpatterns += path('laboratories/<str:code>/request-approval/', laboratory_request_approval, name='laboratory-request-approval'),
urlpatterns += path('laboratories/<str:code>/approve/', laboratory_approve, name='laboratory-approve'),


# urlpatterns += path('laboratories/<str:code>/department/', laboratory_unical_department_edit, name='laboratory-unical-department-edit'),
