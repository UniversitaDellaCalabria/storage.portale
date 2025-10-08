from django.urls import path
from .views import (
    advancedtraining_info_edit,
    advancedtraining_masters,
    advancedtraining_info_create,
    advancedtraining_info_delete
)

app_name = "management"

urlpatterns = [
    path("advanced-training/", advancedtraining_masters, name="advanced-training"),
    path(
        "advanced-training/<int:pk>/",
        advancedtraining_info_edit,
        name="advanced-training-detail",
    ),
    path("masters/new/", advancedtraining_info_create, name="advanced-training-create"),
    path(
    "advanced-training/<int:pk>/delete/",
    advancedtraining_info_delete,
    name="advanced-training-delete",
),

]
