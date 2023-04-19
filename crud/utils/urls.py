from django.urls import path

from . views import home

urlpatterns = []

urlpatterns += path('', home, name='crud_dashboard'),
