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

app_name = "management"

urlpatterns = [
    path('companies/', companies, name='companies'),
    path('companies/new/', company_new, name='company-new'),
    path('companies/<int:company_id>/', company, name='company-edit'),
    path('companies/<int:company_id>/delete/', company_delete, name='company-delete'),
    path('companies/<int:company_id>/referent/<int:data_id>/', company_unical_referent_edit, name='company-unical-referent-edit'),
    path('companies/<int:company_id>/department/new/', company_unical_department_data_new, name='company-unical-department-data-new'),
    path('companies/<int:company_id>/department/<int:department_id>/', company_unical_department_data_edit, name='company-unical-department-data-edit'),
    path('companies/<int:company_id>/department/<int:department_id>/delete/', company_unical_department_data_delete, name='company-unical-department-data-delete'),

    # path('companies/<int:company_id>/referent/<int:data_id>/delete/', company_unical_referent_data_delete, name='company-unical-referent-data-delete'),
]
