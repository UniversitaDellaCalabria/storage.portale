from django.urls import path
from .views import (
    advancedtraining_duplicate,
    advancedtraining_info_edit,
    advancedtraining_masters,
    advancedtraining_info_create,
    advancedtraining_info_delete,
    advancedtraining_status_change,
    advancedtraining_load_tab,
    consiglio_interno_new,
    consiglio_interno_edit,
    consiglio_interno_delete,
)

app_name = "management"

urlpatterns = [
    path("advanced-training/", advancedtraining_masters, name="advanced-training"),
    path(
        "advanced-training/<int:pk>/",
        advancedtraining_info_edit,
        name="advanced-training-detail",
    ),
    path(
        "advanced-training/new/",
        advancedtraining_info_create,
        name="advanced-training-create",
    ),
    path(
        "advanced-training/<int:pk>/delete/",
        advancedtraining_info_delete,
        name="advanced-training-delete",
    ),
    path(
        "advanced-training/<int:pk>/status/<str:status_cod>/",
        advancedtraining_status_change,
        name="advanced-training-status-change",
    ),
    path(
        "advanced-training/<int:pk>/duplicate/",
        advancedtraining_duplicate,
        name="advanced-training-duplicate",
    ),
    path(
        "advanced-training/<int:pk>/load-tab/<str:tab_name>/",
        advancedtraining_load_tab,
        name="advanced-training-load-tab",
    ),
    path(
        'master/<int:master_id>/consiglio-interno/new/',
        consiglio_interno_new,
        name='consiglio-interno-new'
    ),
    path(
        'master/<int:master_id>/consiglio-interno/<int:consiglio_id>/edit/',
        consiglio_interno_edit,
        name='consiglio-interno-edit'
    ),
    path(
        'master/<int:master_id>/consiglio-interno/<int:consiglio_id>/delete/',
        consiglio_interno_delete,
        name='consiglio-interno-delete'
    ),
]
