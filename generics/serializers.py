from django.utils.translation import get_language
from rest_framework import serializers


class LanguageAwareMixin:
    """
    A mix-in to dynamically adjust sources for fields based on the language
    """

    def get_fields(self):
        fields = super().get_fields()
        current_language = get_language()
        field_map = getattr(self.Meta, "language_field_map", {})

        for field_name, sources in field_map.items():
            if field_name in fields:
                fields[field_name].source = sources.get(
                    current_language, sources.get("default", None)
                )
        return fields


class ReadOnlyMixin:
    """
    A mix-in to dynamically set the `read_only` attribute to every field
    """

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class ReadOnlyModelSerializer(
    LanguageAwareMixin, ReadOnlyMixin, serializers.ModelSerializer
):
    pass


"""
The `__doc__` attribute of the classes is set to `None` to avoid inheritance of the docstrings
"""
LanguageAwareMixin.__doc__ = None
ReadOnlyMixin.__doc__ = None
ReadOnlyModelSerializer.__doc__ = None
