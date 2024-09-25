from django.urls import path

from .views import PentahoIsodid

app_name = "apiv1"

urlpatterns = [
    path('api/ricerca/pentaho/<str:cdscod>/isodid/', PentahoIsodid.as_view(), name='pentaho-isodid'),
]
