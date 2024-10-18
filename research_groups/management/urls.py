from django.urls import path

from .views import (
    researchgroup,
    researchgroup_delete,
    researchgroup_new,
    researchgroup_teacher_delete,
    researchgroup_teacher_edit,
    researchgroup_teacher_new,
    researchgroups,
)

app_name = "management"

urlpatterns = [
    path('researchgroups/', researchgroups, name='research-groups'),
    path('researchgroups/new/', researchgroup_new, name='research-group-new'),
    path('researchgroups/<int:rgroup_id>/', researchgroup, name='research-group-edit'),
    path('researchgroups/<int:rgroup_id>/delete/', researchgroup_delete, name='research-group-delete'),
    path('researchgroups/<int:rgroup_id>/teacher/new/', researchgroup_teacher_new, name='research-group-teacher-new'),
    path('researchgroups/<int:rgroup_id>/teacher/<int:teacher_rgroup_id>/', researchgroup_teacher_edit, name='research-group-teacher-edit'),
    path('researchgroups/<int:rgroup_id>/teacher/<int:teacher_rgroup_id>/delete/', researchgroup_teacher_delete, name='research-group-teacher-delete'),
]
