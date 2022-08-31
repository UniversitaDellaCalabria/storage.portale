import secrets

from django import template
from django.conf import settings
from django.contrib.auth import get_user_model

import ricerca_crud.settings as app_settings


register = template.Library()


@register.simple_tag
def settings_value(name, **kwargs):
    value = getattr(settings, name, getattr(app_settings, name))
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


@register.simple_tag
def user_from_pk(user_id):
    if not user_id:
        return False
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)
    if not user:
        return False
    return user
