from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


def recursive_clean(val):
    if isinstance(val, dict):
        return {k: recursive_clean(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [recursive_clean(item) for item in val]
    elif val in ("#NULL#", "-999999999", -999999999):
        return None
    return val


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
