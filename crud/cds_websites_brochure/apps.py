from django.apps import AppConfig


class CRUDCdsWebsitesBrochureConfig(AppConfig):
    name = 'crud.cds_websites_brochure'
    label = 'crudcdswebsitesbrochure'

    def ready(self):
            # Signals
            import crud.cds_websites_brochure.signals