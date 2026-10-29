from django.urls import path

from .views import (
    laboratories,
    laboratory,
    laboratory_approve,
    laboratory_delete,
    laboratory_extra_departments_delete,
    laboratory_extra_departments_new,
    laboratory_locations_delete,
    laboratory_locations_edit,
    laboratory_locations_new,
    laboratory_new,
    laboratory_request_approval,
    laboratory_research_staff_delete,
    laboratory_research_staff_new,
    laboratory_researches_erc1_edit,
    laboratory_safety_manager_delete,
    laboratory_safety_manager_edit,
    laboratory_scientific_director_edit,
    laboratory_services_delete,
    laboratory_services_edit,
    laboratory_services_new,
    laboratory_technical_staff_delete,
    laboratory_technical_staff_new,
)

app_name = "management"

urlpatterns = [
    # LaboratorioDatiBase
    path("laboratories/", laboratories, name="laboratories"),
    path("laboratories/new/", laboratory_new, name="laboratory-new"),
    path("laboratories/<int:laboratory_id>/", laboratory, name="laboratory-edit"),
    path(
        "laboratories/<int:laboratory_id>/delete/",
        laboratory_delete,
        name="laboratory-delete",
    ),
    # Responsabile scientifico / preposto alla sicurezza
    path(
        "laboratories/<int:laboratory_id>/scientific-director/",
        laboratory_scientific_director_edit,
        name="laboratory-scientific-director-edit",
    ),
    path(
        "laboratories/<int:laboratory_id>/safety-manager/",
        laboratory_safety_manager_edit,
        name="laboratory-safety-manager-edit",
    ),
    path(
        "laboratories/<int:laboratory_id>/safety-manager/delete/",
        laboratory_safety_manager_delete,
        name="laboratory-safety-manager-delete",
    ),
    # LaboratorioDipartimenti (extra)
    path(
        "laboratories/<int:laboratory_id>/extra-departments/new/",
        laboratory_extra_departments_new,
        name="laboratory-extra-departments-new",
    ),
    path(
        "laboratories/<int:laboratory_id>/extra-departments/<int:data_id>/delete/",
        laboratory_extra_departments_delete,
        name="laboratory-extra-departments-delete",
    ),
    # LaboratorioDatiErc1
    path(
        "laboratories/<int:laboratory_id>/researches-erc1/",
        laboratory_researches_erc1_edit,
        name="laboratory-researches-erc1-edit",
    ),
    # LaboratorioUbicazione
    path(
        "laboratories/<int:laboratory_id>/locations/new/",
        laboratory_locations_new,
        name="laboratory-locations-new",
    ),
    path(
        "laboratories/<int:laboratory_id>/locations/<int:data_id>/",
        laboratory_locations_edit,
        name="laboratory-locations-edit",
    ),
    path(
        "laboratories/<int:laboratory_id>/locations/<int:data_id>/delete/",
        laboratory_locations_delete,
        name="laboratory-locations-delete",
    ),
    # Personale di ricerca (LaboratorioAffiliati)
    path(
        "laboratories/<int:laboratory_id>/research-staff/new/",
        laboratory_research_staff_new,
        name="laboratory-research-staff-new",
    ),
    path(
        "laboratories/<int:laboratory_id>/research-staff/<int:data_id>/delete/",
        laboratory_research_staff_delete,
        name="laboratory-research-staff-delete",
    ),
    # Personale tecnico (LaboratorioAffiliati)
    path(
        "laboratories/<int:laboratory_id>/technical-staff/new/",
        laboratory_technical_staff_new,
        name="laboratory-technical-staff-new",
    ),
    path(
        "laboratories/<int:laboratory_id>/technical-staff/<int:data_id>/delete/",
        laboratory_technical_staff_delete,
        name="laboratory-technical-staff-delete",
    ),
    # LaboratorioServizi
    path(
        "laboratories/<int:laboratory_id>/services/new/",
        laboratory_services_new,
        name="laboratory-services-new",
    ),
    path(
        "laboratories/<int:laboratory_id>/services/<int:data_id>/",
        laboratory_services_edit,
        name="laboratory-services-edit",
    ),
    path(
        "laboratories/<int:laboratory_id>/services/<int:data_id>/delete/",
        laboratory_services_delete,
        name="laboratory-services-delete",
    ),
    # Approvazione
    path(
        "laboratories/<int:laboratory_id>/request-approval/",
        laboratory_request_approval,
        name="laboratory-request-approval",
    ),
    path(
        "laboratories/<int:laboratory_id>/approve/",
        laboratory_approve,
        name="laboratory-approve",
    ),
]
