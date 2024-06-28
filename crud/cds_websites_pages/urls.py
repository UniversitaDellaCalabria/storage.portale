from django.urls import path

from . views import *

urlpatterns = []

urlpatterns += path('cds-websites-pages/', cds_websites_pages, name='crud_cds_websites_pages'),
#Topics
urlpatterns += path('cds-websites-pages/<str:code>/topics/', cds_websites_pages_topics_edit, name='crud_cds_websites_pages_topics_edit'),
#Common
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/delete/', cds_websites_pages_item_delete, name='crud_cds_websites_pages_item_delete'),
#Reg Artciles
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulation-articles/', cds_websites_pages_regart_item_edit, name='crud_cds_websites_pages_regart_item_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulation-articles/extra/new', cds_websites_pages_regart_extra_new, name='crud_cds_websites_pages_regart_extra_new'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulation-articles/extra/<str:extra_id>/', cds_websites_pages_regart_extra_edit, name='crud_cds_websites_pages_regart_extra_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/regulation-articles/extra/<str:extra_id>/delete/', cds_websites_pages_regart_extra_delete, name='crud_cds_websites_pages_regart_extra_delete'),
#Objects
urlpatterns += path('cds-websites-pages/<str:code>/topics/objects/', cds_websites_pages_objects_edit, name='crud_cds_websites_pages_objects_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/objects/add/', cds_websites_pages_object_item_add, name='crud_cds_websites_pages_object_item_add'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/objects/', cds_websites_pages_object_item_edit, name='crud_cds_websites_pages_object_item_edit'),
#Shared Objects
urlpatterns += path('cds-websites-pages/<str:code>/topics/objects/new/', cds_websites_pages_object_new, name='crud_cds_websites_pages_object_new'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/object/<str:data_id>/', cds_websites_pages_object_edit, name='crud_cds_websites_pages_object_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/object/<str:data_id>/delete/', cds_websites_pages_object_delete, name='crud_cds_websites_pages_object_delete'),
