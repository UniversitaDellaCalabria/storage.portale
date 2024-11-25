from django.urls import path

from .views import dashboard, cds_import, cds_export, regdid_structure_import, regdid_structure_export


app_name = "management"

urlpatterns = [
    path('import-assistant/dashboard/', dashboard, name='dashboard'),
    path('import-assistant/cds-import/', cds_import, name='cds-import'),
    path('import-assistant/cds-export/', cds_export, name='cds-export'),
    path('import-assistant/regdid-structure-import/', regdid_structure_import, name='regdid-structure-import'),
    path('import-assistant/regdid-structure-export/', regdid_structure_export, name='regdid-structure-export'),
]
