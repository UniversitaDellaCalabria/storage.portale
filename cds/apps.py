from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CdsConfig(AppConfig):
    name = "cds"
    verbose_name = _("Courses of Study")

    def ready(self):
        from .management import signals  # noqa: F401
