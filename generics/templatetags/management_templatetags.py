import secrets
from importlib import import_module

from django import template
from django.conf import settings
from django.contrib.auth import get_user_model

register = template.Library()


@register.simple_tag
def settings_value(name, package=None, **kwargs):
    value = None
    if package is not None:
        try:
            package = import_module(".settings", package)
            value = getattr(package, name, None)
        except ImportError:
            pass
    else:
        value = getattr(settings, name, None)

    if value and isinstance(value, str) and kwargs:
        return value.format(**kwargs)
    return value


@register.simple_tag
def random_id(uid=None):
    return uid or f"id_{secrets.randbelow(9999)}"


@register.simple_tag
def user_from_pk(user_id):
    if not user_id:
        return False
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)
    return user if user else False


@register.simple_tag
def latin_enum(value):
    latin_numerals = [
        "bis",
        "ter",
        "quater",
        "quinquies",
        "sexies",
        "septies",
        "octies",
        "novies",
        "decies",
    ]
    if 0 <= value < len(latin_numerals):
        return latin_numerals[value]
    else:
        return ""
