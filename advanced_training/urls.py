from django.urls import include, path
from generics.settings import RICERCA_API_URL

from .api.v1 import urls as apiv1_urls
from .api.v2 import urls as apiv2_urls

app_name = "advanced-training"

urlpatterns = [
    path(RICERCA_API_URL, include(apiv1_urls)),
    path(RICERCA_API_URL, include(apiv2_urls)),
]
