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

urlpatterns = []


urlpatterns += path('cds-brochure/', cds_brochures, name='cds-brochures'),
urlpatterns += path('cds-brochure/<str:code>/', cds_brochure, name='cds-brochure'),
# Dati Base
urlpatterns += path('cds-brochure/<str:code>/info/', cds_brochure_info_edit, name='cds-brochure-info-edit'),
# Sliders
urlpatterns += path('cds-brochure/<str:code>/sliders/', cds_brochure_sliders, name='cds-brochure-sliders'),
urlpatterns += path('cds-brochure/<str:code>/sliders/new/', cds_brochure_sliders_new, name='cds-brochure-sliders-new'),
urlpatterns += path('cds-brochure/<str:code>/sliders/<str:data_id>/', cds_brochure_sliders_edit, name='cds-brochure-sliders-edit'),
urlpatterns += path('cds-brochure/<str:code>/sliders/<str:data_id>/delete/', cds_brochure_sliders_delete, name='cds-brochure-sliders-delete'),
# Ex Students
urlpatterns += path('cds-brochure/<str:code>/ex-students/', cds_brochure_exstudents, name='cds-brochure-exstudents'),
urlpatterns += path('cds-brochure/<str:code>/ex-students/new/', cds_brochure_exstudents_new, name='cds-brochure-exstudents-new'),
urlpatterns += path('cds-brochure/<str:code>/ex-students/<str:data_id>/', cds_brochure_exstudents_edit, name='cds-brochure-exstudents-edit'),
urlpatterns += path('cds-brochure/<str:code>/ex-students/<str:data_id>/delete/', cds_brochure_exstudents_delete, name='cds-brochure-exstudents-delete'),
# Links
urlpatterns += path('cds-brochure/<str:code>/links/', cds_brochure_links, name='cds-brochure-links'),
urlpatterns += path('cds-brochure/<str:code>/links/new/', cds_brochure_links_new, name='cds-brochure-links-new'),
urlpatterns += path('cds-brochure/<str:code>/links/<str:data_id>/', cds_brochure_links_edit, name='cds-brochure-links-edit'),
urlpatterns += path('cds-brochure/<str:code>/links/<str:data_id>/delete/', cds_brochure_links_delete, name='cds-brochure-links-delete'),
