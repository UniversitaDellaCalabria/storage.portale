from django.utils.translation import get_language
from rest_framework import serializers


class LanguageAwareMixin:
    """
    A mix-in to dynamically adjust sources for fields based on the language
    """

    def get_fields(self):
        fields = super().get_fields()
        current_language = self._get_lang() 
        field_map = getattr(self.Meta, "language_field_map", {})

        for field_name, sources in field_map.items():
            if field_name in fields:
                fields[field_name].source = sources.get(
                    current_language, sources.get("default", None)
                )
        return fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        field_map = getattr(self.Meta, "language_field_map", {})
        current_language = self._get_lang()

        for field_name, sources in field_map.items():
            if data.get(field_name) is not None:
                continue

        
            languages_order = ("it", "en") if current_language == "it" else ("en", "it")
            for fallback_lang in languages_order:
                fallback_source = sources.get(fallback_lang)
                if not fallback_source:
                    continue
                value = self._get_by_path(instance, fallback_source)
                if value is not None:
                    data[field_name] = value
                    break

        return data

    def _get_by_path(self, obj, path):
        current = obj
        parts = path.replace("__", ".").split(".")
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            if current is None:
                return None
        return current
    
    def _get_lang(self):
        request = self.context.get('request')
        if request:
            url_lang = request.query_params.get('lang') or request.GET.get('lang')
            if url_lang:
                return url_lang.lower()       
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '') if hasattr(request, 'META') else ''
            if accept_language:
                return accept_language.split(',')[0].split('-')[0].lower()
        return getattr(self, 'lang', 'it').lower()


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


class GenericErrorSerializer(serializers.Serializer):
    """
    A serializer class to handle errors
    """

    detail = serializers.CharField()
        

"""
The `__doc__` attribute of the classes is set to `None` to avoid inheritance of the docstrings
"""
LanguageAwareMixin.__doc__ = None
ReadOnlyMixin.__doc__ = None
ReadOnlyModelSerializer.__doc__ = None
GenericErrorSerializer.__doc__ = None
