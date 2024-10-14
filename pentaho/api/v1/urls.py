from django.urls import path

from .views import ApiPentahoIsodid

app_name = "apiv1"

urlpatterns = [
    path('pentaho/<str:cdscod>/isodid/', ApiPentahoIsodid.as_view(), name='pentaho-isodid'),
]
