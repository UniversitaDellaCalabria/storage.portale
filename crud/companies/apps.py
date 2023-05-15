from django.apps import AppConfig


class CRUDCompaniesConfig(AppConfig):
    name = 'crud.companies'
    label = 'crudcompanies'

    def ready(self):
        # Signals
        import crud.companies.signals
