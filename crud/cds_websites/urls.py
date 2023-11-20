from django.urls import path

from . views import *

urlpatterns = []

urlpatterns += path('cds-websites/', cds_websites, name='crud_cds_websites'),
#Dati Base
urlpatterns += path('cds-websites/<str:code>/', cds_website, name='crud_cds_website'),
urlpatterns += path('cds-websites/<str:code>/base/', cds_websites_base_edit, name='crud_cds_website_base_edit'),
#Sliders
urlpatterns += path('cds-websites/<str:code>/sliders/', cds_websites_sliders, name='crud_cds_websites_sliders'),
urlpatterns += path('cds-websites/<str:code>/sliders/new/', cds_websites_sliders_new, name='crud_cds_websites_sliders_new'),
urlpatterns += path('cds-websites/<str:code>/sliders/<str:data_id>/', cds_websites_sliders_edit, name='crud_cds_websites_sliders_edit'),
urlpatterns += path('cds-websites/<str:code>/sliders/<str:data_id>/delete/', cds_websites_sliders_delete, name='crud_cds_websites_sliders_delete'),
#Ex Students
urlpatterns += path('cds-websites/<str:code>/ex-students/', cds_websites_exstudents, name='crud_cds_websites_exstudents'),
urlpatterns += path('cds-websites/<str:code>/ex-students/new/', cds_websites_exstudents_new, name='crud_cds_websites_exstudents_new'),
urlpatterns += path('cds-websites/<str:code>/ex-students/<str:data_id>/', cds_websites_exstudents_edit, name='crud_cds_websites_exstudents_edit'),
urlpatterns += path('cds-websites/<str:code>/ex-students/<str:data_id>/delete/', cds_websites_exstudents_delete, name='crud_cds_websites_exstudents_delete'),
#Topics
urlpatterns += path('cds-websites/<str:code>/topics/', cds_websites_topics_edit, name='crud_cds_websites_topics_edit'),
#Common
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/delete/', cds_websites_item_delete, name='crud_cds_websites_item_delete'),
#Reg Artciles
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/regulament-articles/add/', cds_websites_regart_add, name='crud_cds_websites_regart_add'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/', cds_websites_regart_item_edit, name='crud_cds_websites_regart_item_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/new', cds_websites_regart_extra_new, name='crud_cds_websites_regart_extra_new'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/<str:extra_id>/', cds_websites_regart_extra_edit, name='crud_cds_websites_regart_extra_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/<str:extra_id>/delete/', cds_websites_regart_extra_delete, name='crud_cds_websites_regart_extra_delete'),
#Objects
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/objects/add/', cds_websites_object_add, name='crud_cds_websites_object_add'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/objects/', cds_websites_object_item_edit, name='crud_cds_websites_object_item_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/objects/new/', cds_websites_object_new, name='crud_cds_websites_object_new'),
urlpatterns += path('cds-websites/<str:code>/topics/object/<str:data_id>/', cds_websites_object_edit, name='crud_cds_websites_object_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/object/<str:data_id>/delete/', cds_websites_object_delete, name='crud_cds_websites_object_delete'),
