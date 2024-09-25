from django.apps import AppConfig


class CdsConfig(AppConfig):
    name = "cds"
    verbose_name = "Courses of Study"
    
    def ready(self):
        from .management import signals
