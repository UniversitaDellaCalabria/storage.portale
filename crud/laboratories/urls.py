from django.urls import path

from . views import laboratories, laboratory, laboratory_new, laboratory_unical_referent_edit, laboratory_delete, laboratory_unical_department_data_edit, laboratory_scientific_director_edit

urlpatterns = []

urlpatterns += path('laboratories/', laboratories, name='crud_laboratories'),
urlpatterns += path('laboratories/new/', laboratory_new, name='crud_laboratory_new'),
urlpatterns += path('laboratories/<str:code>/', laboratory, name='crud_laboratory_edit'),
urlpatterns += path('laboratories/<str:code>/referent/<str:data_id>/', laboratory_unical_referent_edit, name='crud_laboratory_unical_referent_edit'),
urlpatterns += path('laboratories/<str:code>/department/<str:department_id>/', laboratory_unical_department_data_edit, name='crud_laboratory_unical_department_data_edit'),
#urlpatterns += path('companies/<str:code>/department/<str:department_id>/delete/',
#                     company_unical_department_data_delete, name='crud_company_unical_department_data_delete'),
urlpatterns += path('laboratories/<str:code>/delete/',
                    laboratory_delete, name='crud_laboratory_delete'),

urlpatterns += path('laboratories/<str:code>/scientific-director/<str:data_id>/', laboratory_scientific_director_edit, name='crud_laboratory_scientific_director_edit'),
