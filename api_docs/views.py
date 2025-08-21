from drf_spectacular.views import SpectacularSwaggerView

class SpectacularSwaggerView(SpectacularSwaggerView):
    url_name: str = 'api-docs:schema'
