from django.apps import AppConfig


class CRUDCdsConfig(AppConfig):
    name = 'crud.cds'
    label = 'crudcds'

    def ready(self):
        # Signals
        import crud.cds.signals
