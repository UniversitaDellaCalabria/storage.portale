from django.urls import path

from . api_views import PentahoIsodid

urlpatterns = []

# pentaho reports
urlpatterns += path('api/ricerca/pentaho/<str:cdscod>/isodid/',
                    PentahoIsodid.as_view(),
                    name='pentaho-isodid'),
