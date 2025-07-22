from django.urls import path
from .views import advancedtraining_detail, advancedtraining_masters

app_name = "management"

urlpatterns = [
    path("advanced-training/", advancedtraining_masters, name="advanced-training"),
    path("advanced-training/<int:pk>/", advancedtraining_detail, name="advanced-training-detail"),
]
