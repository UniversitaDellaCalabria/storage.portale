from importlib import import_module
from .settings import API_CONTEXTS
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings

API_V1 = 0
API_V2 = 1

def generate_context_urlconf(modules, version):
    patterns = []
    for module in modules:
        try:
            imported_urls = import_module(f"{module}.urls").urlpatterns
            patterns.append(imported_urls[version])
        except ModuleNotFoundError:
            pass
    return patterns

def update_drf_spectacular_settings(schema_urls):

    settings.SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"] = (settings.SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"]
                                                            .format(urls=f"""{[entry for entry in schema_urls]}
                                                                          """
                                                                    )
                                                            )

def generate_context_docs_urlpatterns():
    urlpatterns = []
    schema_urls = []
    for context in API_CONTEXTS:
        # Generate V1 patterns
        v1_patterns = generate_context_urlconf(context.apps, version=API_V1)
        urlpatterns += [
            path(f"api/schema/v1/{context.url_slug}/", SpectacularAPIView.as_view(urlconf=v1_patterns), name=f"schema-v1-{context.url_slug}"),
            path(f"api/v1/{context.url_slug}/", SpectacularSwaggerView.as_view(url_name=f"api-docs:schema-v1-{context.url_slug}"), name=f"swagger-v1-{context.url_slug}"),
        ]
        schema_urls.append({"url": f"/api/schema/v1/{context.url_slug}/", "name": f"{context.display_name} Api V1"})

        # Generate V2 patterns
        v2_patterns = generate_context_urlconf(context.apps, version=API_V2)
        urlpatterns += [
            path(f"api/schema/v2/{context.url_slug}/", SpectacularAPIView.as_view(urlconf=v2_patterns), name=f"schema-v2-{context.url_slug}"),
            path(f"api/v2/{context.url_slug}/", SpectacularSwaggerView.as_view(url_name=f"api-docs:schema-v2-{context.url_slug}"), name=f"swagger-v2-{context.url_slug}"),
        ]
        schema_urls.append({"url": f"/api/schema/v2/{context.url_slug}/", "name": f"{context.display_name} Api V2"})
    
    update_drf_spectacular_settings(schema_urls)
    
    return urlpatterns