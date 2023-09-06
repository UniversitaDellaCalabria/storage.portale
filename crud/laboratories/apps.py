from django.apps import AppConfig


class CRUDLaboratoriesConfig(AppConfig):
    name = 'crud.laboratories'
    label = 'crudlaboratories'

    def ready(self):
        # Signals
        import crud.laboratories.signals
