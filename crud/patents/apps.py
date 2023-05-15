from django.apps import AppConfig


class CRUDPatentsConfig(AppConfig):
    name = 'crud.patents'
    label = 'crudpatents'

    def ready(self):
        # Signals
        import crud.patents.signals
