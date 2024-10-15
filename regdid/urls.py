from django.conf import settings
from django.urls import include, path
from generics.settings import RICERCA_API_URL

from .api.v1 import urls as apiv1_urls
from .api.v2 import urls as apiv2_urls

app_name = "regdid"

urlpatterns = [
    path(RICERCA_API_URL, include(apiv1_urls)),
    path(RICERCA_API_URL, include(apiv2_urls)),
]

if __package__ not in getattr(settings, "DISABLED_MANAGEMENT_APPS", []):
    from .management import urls as management_urls

    urlpatterns += (path("", include(management_urls)),)