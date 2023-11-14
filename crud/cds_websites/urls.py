from django.urls import path

from . views import *

urlpatterns = []

urlpatterns += path('cds-websites/', cds_websites, name='crud_cds_websites'),
urlpatterns += path('cds-websites/<str:code>/topics/', cds_websites_topics_edit, name='crud_cds_websites_topics_edit'),
#Common
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/delete/', cds_websites_item_delete, name='crud_cds_websites_item_delete'),
#Reg Artciles
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/regulament-articles/new', cds_websites_regart_new, name='crud_cds_websites_regart_new'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/', cds_websites_regart_edit, name='crud_cds_websites_regart_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/new', cds_websites_regart_extra_new, name='crud_cds_websites_regart_extra_new'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/<str:extra_id>/', cds_websites_regart_extra_edit, name='crud_cds_websites_regart_extra_edit'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulament-articles/extra/<str:extra_id>/delete/', cds_websites_regart_extra_delete, name='crud_cds_websites_regart_extra_delete'),
#Objects
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/objects/new/', cds_websites_object_new, name='crud_cds_websites_object_new'),
urlpatterns += path('cds-websites/<str:code>/topics/<str:topic_id>/items/<str:data_id>/object/', cds_websites_object_edit, name='crud_cds_websites_object_edit'),

