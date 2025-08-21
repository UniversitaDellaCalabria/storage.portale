from django.urls import path
from .views import master_info_edit, advancedtraining_masters

app_name = "management"

urlpatterns = [
    path("advanced-training/", advancedtraining_masters, name="advanced-training"),
    path("advanced-training/<int:pk>/", master_info_edit, name="advanced-training-detail"),
]
