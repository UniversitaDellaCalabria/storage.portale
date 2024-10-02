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

urlpatterns = []


urlpatterns += path('researchgroups/', researchgroups, name='research-groups'),
urlpatterns += path('researchgroups/new/', researchgroup_new, name='research-group-new'),
urlpatterns += path('researchgroups/<str:code>/', researchgroup, name='research-group-edit'),
urlpatterns += path('researchgroups/<str:code>/delete/', researchgroup_delete, name='research-group-delete'),
urlpatterns += path('researchgroups/<str:code>/teacher/new/', researchgroup_teacher_new, name='research-group-teacher-new'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/', researchgroup_teacher_edit, name='research-group-teacher-edit'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/delete/', researchgroup_teacher_delete, name='research-group-teacher-delete'),
