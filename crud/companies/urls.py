from django.urls import path

from . views import companies, company, company_delete, company_new, company_unical_department_data_delete, company_unical_department_data_edit, company_unical_department_data_new, company_unical_referent_edit


urlpatterns = []

urlpatterns += path('companies/', companies, name='crud_companies'),
urlpatterns += path('companies/new/', company_new, name='crud_company_new'),
urlpatterns += path('companies/<str:code>/', company,
                    name='crud_company_edit'),
urlpatterns += path('companies/<str:code>/referent/<str:data_id>/',
                    company_unical_referent_edit, name='crud_company_unical_referent_edit'),
# urlpatterns += path('companies/<str:code>/referent/<str:data_id>/delete/', company_unical_referent_data_delete, name='crud_company_unical_referent_data_delete'),
urlpatterns += path('companies/<str:code>/department/new/',
                    company_unical_department_data_new, name='crud_company_unical_department_data_new'),
urlpatterns += path('companies/<str:code>/department/<str:department_id>/',
                    company_unical_department_data_edit, name='crud_company_unical_department_data_edit'),
urlpatterns += path('companies/<str:code>/department/<str:department_id>/delete/',
                    company_unical_department_data_delete, name='crud_company_unical_department_data_delete'),
urlpatterns += path('companies/<str:code>/delete/',
                    company_delete, name='crud_company_delete'),
