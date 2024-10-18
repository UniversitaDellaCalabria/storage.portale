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

urlpatterns = [
    # LaboratorioDatiBase
    path('laboratories/', laboratories, name='laboratories'),
    path('laboratories/new/', laboratory_new, name='laboratory-new'),
    path('laboratories/<int:laboratory_id>/', laboratory, name='laboratory-edit'),
    path('laboratories/<int:laboratory_id>/delete/', laboratory_delete, name='laboratory-delete'),

    # LaboratorioDatiBaseAmbitoForm
    path('laboratories/<int:laboratory_id>/scope/', laboratory_scope_edit, name='laboratory-scope-edit'),

    # LaboratorioDatiBaseInfoSede
    path('laboratories/<int:laboratory_id>/edit-office/', laboratory_info_sede_edit, name='laboratory-info-sede-edit'),

    # LaboratorioDatiBaseintumentazioneValore
    path('laboratories/<int:laboratory_id>/equipment-value/', laboratory_equipment_value_edit, name='laboratory-equipment-value-edit'),

    # LaboratorioDatiBaseInterdipartimentale
    path('laboratories/<int:laboratory_id>/interdepartmental/', laboratory_interdepartmental_edit, name='laboratory-interdepartmental-edit'),
    path('laboratories/<int:laboratory_id>/scientific-director/', laboratory_scientific_director_edit, name='laboratory-scientific-director-edit'),
    path('laboratories/<int:laboratory_id>/safety-manager/', laboratory_safety_manager_edit, name='laboratory-safety-manager-edit'),

    # LaboratorioAltriDipartimenti
    path('laboratories/<int:laboratory_id>/extra-departments/new/', laboratory_extra_departments_new, name='laboratory-extra-departments-new'),
    path('laboratories/<int:laboratory_id>/extra-departments/<int:data_id>/delete/', laboratory_extra_departments_delete, name='laboratory-extra-departments-delete'),
    path('laboratories/<int:laboratory_id>/equipment/new/', laboratory_equipment_new, name='laboratory-equipment-new'),
    path('laboratories/<int:laboratory_id>/equipment/<int:data_id>/', laboratory_equipment_edit, name='laboratory-equipment-edit'),
    path('laboratories/<int:laboratory_id>/equipment/<int:data_id>/delete/', laboratory_equipment_delete, name='laboratory-equipment-delete'),

    # LaboratorioDatiRicerca
    path('laboratories/<int:laboratory_id>/researches-erc1/', laboratory_researches_erc1_edit, name='laboratory-researches-erc1-edit'),

    # LaboratorioUbicazione
    path('laboratories/<int:laboratory_id>/locations/new/', laboratory_locations_new, name='laboratory-locations-new'),
    path('laboratories/<int:laboratory_id>/locations/<int:data_id>/', laboratory_locations_edit, name='laboratory-locations-edit'),
    path('laboratories/<int:laboratory_id>/locations/<int:data_id>/delete/', laboratory_locations_delete, name='laboratory-locations-delete'),

    # LaboratorioPersonaleRicerca
    path('laboratories/<int:laboratory_id>/research-staff/new/', laboratory_research_staff_new, name='laboratory-research-staff-new'),
    path('laboratories/<int:laboratory_id>/research-staff/<int:data_id>/delete/', laboratory_research_staff_delete, name='laboratory-research-staff-delete'),

    # LaboratorioPersonaleTecnico
    path('laboratories/<int:laboratory_id>/technical-staff/new/', laboratory_technical_staff_new, name='laboratory-technical-staff-new'),
    path('laboratories/<int:laboratory_id>/technical-staff/<int:data_id>/delete/', laboratory_technical_staff_delete, name='laboratory-technical-staff-delete'),

    # LaboratorioAttivita
    path('laboratories/<int:laboratory_id>/activities/new/', laboratory_activities_new, name='laboratory-activities-new'),
    path('laboratories/<int:laboratory_id>/activities/<int:data_id>/', laboratory_activities_edit, name='laboratory-activities-edit'),
    path('laboratories/<int:laboratory_id>/activities/<int:data_id>/delete/', laboratory_activities_delete, name='laboratory-activities-delete'),

    # LaboratorioServiziErogati
    path('laboratories/<int:laboratory_id>/provided-services/new/', laboratory_provided_services_new, name='laboratory-provided-services-new'),
    path('laboratories/<int:laboratory_id>/provided-services/<int:data_id>/', laboratory_provided_services_edit, name='laboratory-provided-services-edit'),
    path('laboratories/<int:laboratory_id>/provided-services/<int:data_id>/delete/', laboratory_provided_services_delete, name='laboratory-provided-services-delete'),

    # LaboratorioServiziOfferti
    path('laboratories/<int:laboratory_id>/offered-services/new/', laboratory_offered_services_new, name='laboratory-offered-services-new'),
    path('laboratories/<int:laboratory_id>/offered-services/<int:data_id>/', laboratory_offered_services_edit, name='laboratory-offered-services-edit'),
    path('laboratories/<int:laboratory_id>/offered-services/<int:data_id>/delete/', laboratory_offered_services_delete, name='laboratory-offered-services-delete'),

    # LaboratorioTipologiaRischio
    path('laboratories/<int:laboratory_id>/risk-types/', laboratory_risk_types_edit, name='laboratory-risk-types-edit'),

    # utils
    path('laboratories/<int:laboratory_id>/request-approval/', laboratory_request_approval, name='laboratory-request-approval'),
    path('laboratories/<int:laboratory_id>/approve/', laboratory_approve, name='laboratory-approve'),

    # path('laboratories/<int:laboratory_id>/department/', laboratory_unical_department_edit, name='laboratory-unical-department-edit'),
]
