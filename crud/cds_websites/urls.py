from django.urls import path

from . views import *

urlpatterns = []

urlpatterns += path('cds-websites/', cds_websites, name='crud_cds_websites'),
urlpatterns += path('cds-websites/<str:code>/', cds_websites_edit, name='crud_cds_websites_edit'),
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/', cds_websites_tregart_edit, name='crud_cds_websites_tregart_edit'),
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/delete/', cds_websites_tregart_delete, name='crud_cds_websites_tregart_delete'),
#Reg Artciles
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/extra/new/', cds_websites_tregart_extra_new, name='crud_cds_websites_tregart_extra_new'),
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/extra/<str:data_id>/', cds_websites_tregart_extra_edit, name='crud_cds_websites_tregart_extra_edit'),
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/extra/<str:data_id>/delete/', cds_websites_tregart_extra_delete, name='crud_cds_websites_tregart_extra_delete'),
#Objects
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/objects/new/', cds_websites_objects_new, name='crud_cds_websites_objects_new'),
urlpatterns += path('cds-websites/<str:code>/reg-arts-objects/<str:tregart_id>/objects/<str:data_id>/', cds_websites_objects_edit, name='crud_cds_websites_objects_edit'),

