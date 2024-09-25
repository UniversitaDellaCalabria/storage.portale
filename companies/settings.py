from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Path to companies's logos
COMPANIES_MEDIA_PATH_BASE = getattr(settings, "COMPANIES_MEDIA_PATH_BASE", "portale/spinoff-startup/loghi")
def companies_media_path(instance, filename):
    return f'{COMPANIES_MEDIA_PATH_BASE}/{filename}'

OFFICE_COMPANIES = getattr(settings, 'OFFICE_COMPANIES', 'companies')