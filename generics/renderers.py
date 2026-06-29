from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from generics.utils import is_nullable


def recursive_clean(val):
    if isinstance(val, dict):
        return {k: recursive_clean(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [recursive_clean(item) for item in val]
    return is_nullable(val)


# 1. Questo pulisce il JSON puro (es. Postman / Axios / Fetch)
class CleanJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        cleaned_data = recursive_clean(data)
        return super().render(cleaned_data, accepted_media_type, renderer_context)


# 2. Questo pulisce la pagina Web di DRF
class CleanBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Puliamo i dati prima che il BrwosableRenderer li impacchetti nel template HTML
        cleaned_data = recursive_clean(data)
        return super().render(cleaned_data, accepted_media_type, renderer_context)
