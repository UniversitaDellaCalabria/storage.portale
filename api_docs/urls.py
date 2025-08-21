from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .utils import generate_context_docs_urlpatterns

app_name = "api-docs"


urlpatterns = [
    # Full schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-docs:schema"), name="swagger"),
] + generate_context_docs_urlpatterns()
