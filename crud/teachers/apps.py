from django.apps import AppConfig

class CRUDTeachersConfig(AppConfig):
    name = 'crud.teachers'
    label = 'crudteachers'

    def ready(self):
        # Signals
        from . import signals
