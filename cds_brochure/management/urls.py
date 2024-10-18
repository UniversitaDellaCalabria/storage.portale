from django.urls import path

from .views import (
    cds_brochure,
    cds_brochure_exstudents,
    cds_brochure_exstudents_delete,
    cds_brochure_exstudents_edit,
    cds_brochure_exstudents_new,
    cds_brochure_info_edit,
    cds_brochure_links,
    cds_brochure_links_delete,
    cds_brochure_links_edit,
    cds_brochure_links_new,
    cds_brochure_sliders,
    cds_brochure_sliders_delete,
    cds_brochure_sliders_edit,
    cds_brochure_sliders_new,
    cds_brochures,
)

app_name = "management"

urlpatterns = [
    path('cds-brochure/', cds_brochures, name='cds-brochures'),
    path('cds-brochure/<int:brochure_id>/', cds_brochure, name='cds-brochure'),

    # Dati Base
    path('cds-brochure/<int:brochure_id>/info/', cds_brochure_info_edit, name='cds-brochure-info-edit'),

    # Sliders
    path('cds-brochure/<int:brochure_id>/sliders/', cds_brochure_sliders, name='cds-brochure-sliders'),
    path('cds-brochure/<int:brochure_id>/sliders/new/', cds_brochure_sliders_new, name='cds-brochure-sliders-new'),
    path('cds-brochure/<int:brochure_id>/sliders/<int:data_id>/', cds_brochure_sliders_edit, name='cds-brochure-sliders-edit'),
    path('cds-brochure/<int:brochure_id>/sliders/<int:data_id>/delete/', cds_brochure_sliders_delete, name='cds-brochure-sliders-delete'),

    # Ex Students
    path('cds-brochure/<int:brochure_id>/ex-students/', cds_brochure_exstudents, name='cds-brochure-exstudents'),
    path('cds-brochure/<int:brochure_id>/ex-students/new/', cds_brochure_exstudents_new, name='cds-brochure-exstudents-new'),
    path('cds-brochure/<int:brochure_id>/ex-students/<int:data_id>/', cds_brochure_exstudents_edit, name='cds-brochure-exstudents-edit'),
    path('cds-brochure/<int:brochure_id>/ex-students/<int:data_id>/delete/', cds_brochure_exstudents_delete, name='cds-brochure-exstudents-delete'),

    # Links
    path('cds-brochure/<int:brochure_id>/links/', cds_brochure_links, name='cds-brochure-links'),
    path('cds-brochure/<int:brochure_id>/links/new/', cds_brochure_links_new, name='cds-brochure-links-new'),
    path('cds-brochure/<int:brochure_id>/links/<int:data_id>/', cds_brochure_links_edit, name='cds-brochure-links-edit'),
    path('cds-brochure/<int:brochure_id>/links/<int:data_id>/delete/', cds_brochure_links_delete, name='cds-brochure-links-delete'),
]
