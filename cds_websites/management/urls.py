from django.urls import path

from .views import (
    cds_websites,
    cds_websites_article_edit,
    cds_websites_extra_delete,
    cds_websites_extra_edit,
    cds_websites_extra_new,
    cds_websites_extras,
    cds_websites_items_order_edit,
    cds_websites_object_add,
    cds_websites_object_delete,
    cds_websites_object_edit,
    cds_websites_shared_object_delete,
    cds_websites_shared_object_edit,
    cds_websites_shared_object_new,
    cds_websites_shared_objects,
    cds_websites_sub_article_edit,
    cds_websites_sub_articles,
    cds_websites_topics,
)

app_name = "management"

urlpatterns = []


urlpatterns += path('cds-websites/', cds_websites, name='cds-websites'),
# Topics
urlpatterns += path('cds-websites/<int:cds_id>/topics/', cds_websites_topics, name='cds-websites-topics'),
# Common
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/order/', cds_websites_items_order_edit, name='cds-websites-items-order-edit'),
# Shared Objects
urlpatterns += path('cds-websites/<int:cds_id>/shared-objects/', cds_websites_shared_objects, name='cds-websites-shared-objects'),
urlpatterns += path('cds-websites/<int:cds_id>/shared-objects/new/', cds_websites_shared_object_new, name='cds-websites-shared-object-new'),
urlpatterns += path('cds-websites/<int:cds_id>/shared-objects/<int:data_id>/', cds_websites_shared_object_edit, name='cds-websites-shared-object-edit'),
urlpatterns += path('cds-websites/<int:cds_id>/shared-objects/<int:data_id>/delete/', cds_websites_shared_object_delete, name='cds-websites-shared-object-delete'),
# Artciles
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/regulation-articles/<int:data_id>/', cds_websites_article_edit, name='cds-websites-article-edit'),
# Sub articles
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/regulation-articles/<int:data_id>/sub-articles/', cds_websites_sub_articles, name='cds-websites-sub-articles'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/regulation-articles/<int:data_id>/sub-articles/<int:sub_art_id>/', cds_websites_sub_article_edit, name='cds-websites-sub-article-edit'),
# Objects
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/objects/add/', cds_websites_object_add, name='cds-websites-object-add'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/objects/<int:data_id>/', cds_websites_object_edit, name='cds-websites-object-edit'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/objects/<int:data_id>/delete/', cds_websites_object_delete, name='cds-websites-object-delete'),
# Extra
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/<int:data_id>/extras/', cds_websites_extras, name='cds-websites-extras'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/<int:data_id>/extras/new', cds_websites_extra_new, name='cds-websites-extra-new'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/<int:data_id>/extras/<int:extra_id>/', cds_websites_extra_edit, name='cds-websites-extra-edit'),
urlpatterns += path('cds-websites/<int:cds_id>/topics/<int:topic_id>/items/<int:data_id>/extras/<int:extra_id>/delete/', cds_websites_extra_delete, name='cds-websites-extra-delete'),
