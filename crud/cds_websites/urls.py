from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('cds-websites/', cds_websites, name='crud_cdswebsites'),
urlpatterns += path('cds-websites/<str:code>/', cds_website, name='crud_cds_website_edit'),
