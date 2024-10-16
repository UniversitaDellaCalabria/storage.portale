from accounts import settings
from django import template

register = template.Library()


@register.simple_tag
def accounts_settings_value(name, **kwargs):
    value = getattr(settings, name, None)
    if value and kwargs:
        return value.format(**kwargs)
    return value
