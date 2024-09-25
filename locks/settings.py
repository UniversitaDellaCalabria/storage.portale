from django.conf import settings
from django.utils.translation import gettext_lazy as _

STORAGE_CACHE_KEY_PREFIX = getattr(settings, 'STORAGE_CACHE_KEY_PREFIX', 'storage_')
LOCKS_CACHE_TTL = getattr(settings, 'LOCKS_CACHE_TTL', 25) # seconds
LOCKS_CACHE_KEY_PREFIX = getattr(settings, 'LOCKS_CACHE_KEY_PREFIX', f'{STORAGE_CACHE_KEY_PREFIX}locks_')
LOCK_MESSAGE = getattr(settings, 'LOCK_MESSAGE', _("Unable to make changes. "
                                                   "{user} is currently editing this item"))