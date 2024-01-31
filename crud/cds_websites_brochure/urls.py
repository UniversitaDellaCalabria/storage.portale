from django.urls import path

from . views import *

urlpatterns = []

urlpatterns += path('cds-websites-brochure/', cds_websites_brochure, name='crud_cds_websites_brochure'),
urlpatterns += path('cds-websites-brochure/<str:code>/', cds_website_brochure, name='crud_cds_website_brochure'),
#Dati Base
urlpatterns += path('cds-websites-brochure/<str:code>/info/', cds_websites_brochure_info_edit, name='crud_cds_websites_brochure_info_edit'),
#Sliders
urlpatterns += path('cds-websites-brochure/<str:code>/sliders/', cds_websites_brochure_sliders, name='crud_cds_websites_brochure_sliders'),
urlpatterns += path('cds-websites-brochure/<str:code>/sliders/new/', cds_websites_brochure_sliders_new, name='crud_cds_websites_brochure_sliders_new'),
urlpatterns += path('cds-websites-brochure/<str:code>/sliders/<str:data_id>/', cds_websites_brochure_sliders_edit, name='crud_cds_websites_brochure_sliders_edit'),
urlpatterns += path('cds-websites-brochure/<str:code>/sliders/<str:data_id>/delete/', cds_websites_brochure_sliders_delete, name='crud_cds_websites_brochure_sliders_delete'),
#Ex Students
urlpatterns += path('cds-websites-brochure/<str:code>/ex-students/', cds_websites_brochure_exstudents, name='crud_cds_websites_brochure_exstudents'),
urlpatterns += path('cds-websites-brochure/<str:code>/ex-students/new/', cds_websites_brochure_exstudents_new, name='crud_cds_websites_brochure_exstudents_new'),
urlpatterns += path('cds-websites-brochure/<str:code>/ex-students/<str:data_id>/', cds_websites_brochure_exstudents_edit, name='crud_cds_websites_brochure_exstudents_edit'),
urlpatterns += path('cds-websites-brochure/<str:code>/ex-students/<str:data_id>/delete/', cds_websites_brochure_exstudents_delete, name='crud_cds_websites_brochure_exstudents_delete'),
#Links
urlpatterns += path('cds-websites-brochure/<str:code>/links/', cds_websites_brochure_links, name='crud_cds_websites_brochure_links'),
urlpatterns += path('cds-websites-brochure/<str:code>/links/new/', cds_websites_brochure_links_new, name='crud_cds_websites_brochure_links_new'),
urlpatterns += path('cds-websites-brochure/<str:code>/links/<str:data_id>/', cds_websites_brochure_links_edit, name='crud_cds_websites_brochure_links_edit'),
urlpatterns += path('cds-websites-brochure/<str:code>/links/<str:data_id>/delete/', cds_websites_brochure_links_delete, name='crud_cds_websites_brochure_links_delete'),