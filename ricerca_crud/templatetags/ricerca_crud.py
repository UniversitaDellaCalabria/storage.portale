import secrets

from django import template
from django.conf import settings

import ricerca_crud.settings as app_settings


register = template.Library()


@register.simple_tag
def settings_value(name, **kwargs):
    value = getattr(settings, name, '')
    if not value: return ''
    if isinstance(value, str) and kwargs: return value.format(**kwargs)
    return value


@register.simple_tag
def random_id(uid=None):
    return uid or f"id_{secrets.randbelow(9999)}"


@register.simple_tag
def ricerca_settings_value(value):
    app_value = getattr(app_settings, value, None)
    return  getattr(settings, value, app_value)
