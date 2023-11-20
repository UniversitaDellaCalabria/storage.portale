from django.apps import AppConfig


class CRUDCdsWebsitesConfig(AppConfig):
    name = 'crud.cds_websites'
    label = 'crudcdswebsites'

    def ready(self):
            # Signals
            import crud.cds_websites.signals