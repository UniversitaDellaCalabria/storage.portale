import datetime
import logging

from django.conf import settings
from django.core.cache import cache

from . import settings as app_settings
from . exceptions import *


logger = logging.getLogger(__name__)

# locks timed cache
LOCKS_CACHE_TTL = getattr(settings, 'LOCKS_CACHE_TTL',
                          app_settings.LOCKS_CACHE_TTL)
LOCKS_CACHE_KEY_PREFIX = getattr(settings, 'LOCKS_CACHE_KEY_PREFIX',
                                 app_settings.LOCKS_CACHE_KEY_PREFIX)
LOCK_MESSAGE = getattr(settings, 'LOCK_MESSAGE', app_settings.LOCK_MESSAGE)


def get_lock_from_cache(content_type_id, object_id):
    key = f'{LOCKS_CACHE_KEY_PREFIX}{content_type_id}_{object_id}'
    res = cache.get(key)
    if res: # pragma: no cover
        exp_info = cache._expire_info.get(cache.make_key(key), None)
        exp_info_seconds = 0
        if exp_info is not None:
            exp_info_seconds = (datetime.datetime.fromtimestamp(exp_info) - datetime.datetime.now()).seconds
        return (res, exp_info_seconds)
    return (0, 0)

def set_lock_to_cache(user_id, content_type_id, object_id):
    key = f'{LOCKS_CACHE_KEY_PREFIX}{content_type_id}_{object_id}'
    cache.set(key, user_id, LOCKS_CACHE_TTL)
    
def acquire_lock(user_id, content_type_id, object_id):
    # check for existing locks on the object
    lock = get_lock_from_cache(content_type_id, object_id)
    if lock[0] and not lock[0] == user_id:
        raise LockCannotBeAcquiredException(lock)
    set_lock_to_cache(user_id, content_type_id, object_id)