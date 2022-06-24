from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, re_path

from . views import *

urlpatterns = []

urlpatterns += path('', home, name='crud_dashboard'),
urlpatterns += path('researchgroups/', researchgroups, name='crud_researchgroups'),
urlpatterns += path('researchgroups/new/', researchgroup_new, name='crud_researchgroup_new'),
urlpatterns += path('researchgroups/<str:code>/', researchgroup, name='crud_researchgroup_edit'),
urlpatterns += path('researchgroups/<str:code>/delete/', researchgroup_delete, name='crud_researchgroup_delete'),
urlpatterns += path('researchgroups/<str:code>/teacher/new/', researchgroup_teacher_new, name='crud_researchgroup_teacher_new'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/', researchgroup_teacher_edit, name='crud_researchgroup_teacher_edit'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/delete/', researchgroup_teacher_delete, name='crud_researchgroup_teacher_delete'),
