from django.urls import path

from . views import *

#router.register(r'cds-websites-external-shared-objects', ExternalOggettiPortaleViewSet, basename='cds-websites-external-shared-objects')

urlpatterns = []

urlpatterns += path('cds-websites-pages/', cds_websites_pages, name='crud_cds_websites_pages'),
#Topics
urlpatterns += path('cds-websites-pages/<str:code>/topics/', cds_websites_pages_topics, name='crud_cds_websites_pages_topics'),
#Common
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/order/', cds_websites_pages_items_order_edit, name='crud_cds_websites_pages_items_order_edit'),
#Shared Objects
urlpatterns += path('cds-websites-pages/<str:code>/shared-objects/', cds_websites_pages_shared_objects, name='crud_cds_websites_pages_shared_objects'),
urlpatterns += path('cds-websites-pages/<str:code>/shared-objects/new/', cds_websites_pages_shared_object_new, name='crud_cds_websites_pages_shared_object_new'),
urlpatterns += path('cds-websites-pages/<str:code>/shared-objects/<str:data_id>/', cds_websites_pages_shared_object_edit, name='crud_cds_websites_pages_shared_object_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/shared-objects/<str:data_id>/delete/', cds_websites_pages_shared_object_delete, name='crud_cds_websites_pages_shared_object_delete'),
#Artciles
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/regulation-articles/<str:data_id>/', cds_websites_pages_article_edit, name='crud_cds_websites_pages_article_edit'),
#Sub articles
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/regulation-articles/<str:data_id>/sub-articles/', cds_websites_pages_sub_articles, name='crud_cds_websites_pages_sub_articles'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/regulation-articles/<str:data_id>/sub-articles/<str:sub_art_id>/', cds_websites_pages_sub_article_edit, name='crud_cds_websites_pages_sub_article_edit'),
#Objects
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/objects/add/', cds_websites_pages_object_add, name='crud_cds_websites_pages_object_add'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/objects/<str:data_id>/', cds_websites_pages_object_edit, name='crud_cds_websites_pages_object_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/objects/<str:data_id>/delete/', cds_websites_pages_object_delete, name='crud_cds_websites_pages_object_delete'),
#Extra
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/extras/', cds_websites_pages_extras, name='crud_cds_websites_pages_extras'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/extras/new', cds_websites_pages_extra_new, name='crud_cds_websites_pages_extra_new'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/extras/<str:extra_id>/', cds_websites_pages_extra_edit, name='crud_cds_websites_pages_extra_edit'),
urlpatterns += path('cds-websites-pages/<str:code>/topics/<str:topic_id>/items/<str:data_id>/extras/<str:extra_id>/delete/', cds_websites_pages_extra_delete, name='crud_cds_websites_pages_extra_delete'),
#Apis
urlpatterns += path('cds-websites-pages/api/<int:code>/shared-objects/', SitoWebCdsOggettiPortaleViewSet.as_view({'get' : 'list'}), name="cds_websites_shared_objects_list"),
urlpatterns += path('cds-websites-pages/api/<int:code>/shared-objects/<int:pk>/', SitoWebCdsOggettiPortaleViewSet.as_view({'get' : 'retrieve'}), name="cds_websites_shared_objects_detail"),
urlpatterns += path('cds-websites-pages/api/portal-objects/', ExternalOggettiPortaleViewSet.as_view({'get' : 'list'}), name="cds_websites_external_objects_list"),
urlpatterns += path('cds-websites-pages/api/portal-objects/<int:pk>/', ExternalOggettiPortaleViewSet.as_view({'get' : 'retrieve'}), name="cds_websites_external_objects_detail"),