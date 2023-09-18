from django.urls import path

from . views import laboratories, laboratory, laboratory_new, laboratory_unical_referent_edit, laboratory_delete, laboratory_unical_department_data_edit, laboratory_scientific_director_edit, laboratory_safety_responsible_new, laboratory_safety_responsible_edit, laboratory_safety_responsible_delete

urlpatterns = []

urlpatterns += path('laboratories/', laboratories, name='crud_laboratories'),
urlpatterns += path('laboratories/new/', laboratory_new, name='crud_laboratory_new'),
urlpatterns += path('laboratories/<str:code>/', laboratory, name='crud_laboratory_edit'),
urlpatterns += path('laboratories/<str:code>/referent/<str:data_id>/', laboratory_unical_referent_edit, name='crud_laboratory_unical_referent_edit'),
urlpatterns += path('laboratories/<str:code>/department/<str:department_id>/', laboratory_unical_department_data_edit, name='crud_laboratory_unical_department_data_edit'),
urlpatterns += path('laboratories/<str:code>/delete/', laboratory_delete, name='crud_laboratory_delete'),
urlpatterns += path('laboratories/<str:code>/scientific-director/<str:data_id>/', laboratory_scientific_director_edit, name='crud_laboratory_scientific_director_edit'),
urlpatterns += path('laboratories/<str:code>/safety-responsible/<str:data_id>/', laboratory_safety_responsible_edit, name='crud_laboratory_safety_responsible_edit'),
urlpatterns += path('laboratories/<str:code>/safety-responsible/<str:data_id>/delete/', laboratory_safety_responsible_delete, name='crud_laboratory_safety_responsible_delete'),
