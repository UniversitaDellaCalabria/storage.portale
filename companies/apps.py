from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    name = "companies"
    verbose_name = "Companies"
    
    def ready(self):
        from .management import signals
