from django.urls import path

from .views import home

app_name = "generics"

urlpatterns = [
    path("", home, name="dashboard"),
]
