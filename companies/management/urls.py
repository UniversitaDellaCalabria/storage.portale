from django.urls import path

from .views import (
    companies,
    company,
    company_delete,
    company_new,
    company_unical_department_data_delete,
    company_unical_department_data_edit,
    company_unical_department_data_new,
    company_unical_referent_edit,
)

app_name="management"

urlpatterns = []

urlpatterns += path('companies/', companies, name='companies'),
urlpatterns += path('companies/new/', company_new, name='company-new'),
urlpatterns += path('companies/<str:code>/', company, name='company-edit'),
urlpatterns += path('companies/<str:code>/delete/', company_delete, name='company-delete'),
urlpatterns += path('companies/<str:code>/referent/<str:data_id>/', company_unical_referent_edit, name='company-unical-referent-edit'),
urlpatterns += path('companies/<str:code>/department/new/', company_unical_department_data_new, name='company-unical-department-data-new'),
urlpatterns += path('companies/<str:code>/department/<str:department_id>/', company_unical_department_data_edit, name='company-unical-department-data-edit'),
urlpatterns += path('companies/<str:code>/department/<str:department_id>/delete/', company_unical_department_data_delete, name='company-unical-department-data-delete'),

# urlpatterns += path('companies/<str:code>/referent/<str:data_id>/delete/', company_unical_referent_data_delete, name='company-unical-referent-data-delete'),