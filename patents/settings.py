from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Path to patents's logos
PATENT_MEDIA_PATH_BASE = getattr(settings, "PATENT_MEDIA_PATH_BASE", "portale/brevetti/loghi")
def patents_media_path(instance, filename):
    return f'{PATENT_MEDIA_PATH_BASE}/{filename}'

OFFICE_PATENTS = getattr(settings, 'OFFICE_PATENTS', 'patents')