from django.urls import path

from . views import researchgroup, researchgroup_delete, researchgroup_new, researchgroup_teacher_delete, researchgroup_teacher_edit, researchgroup_teacher_new, researchgroups


urlpatterns = []

urlpatterns += path('researchgroups/', researchgroups,
                    name='crud_researchgroups'),
urlpatterns += path('researchgroups/new/', researchgroup_new,
                    name='crud_researchgroup_new'),
urlpatterns += path('researchgroups/<str:code>/',
                    researchgroup, name='crud_researchgroup_edit'),
urlpatterns += path('researchgroups/<str:code>/delete/',
                    researchgroup_delete, name='crud_researchgroup_delete'),
urlpatterns += path('researchgroups/<str:code>/teacher/new/',
                    researchgroup_teacher_new, name='crud_researchgroup_teacher_new'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/',
                    researchgroup_teacher_edit, name='crud_researchgroup_teacher_edit'),
urlpatterns += path('researchgroups/<str:code>/teacher/<str:teacher_rgroup_id>/delete/',
                    researchgroup_teacher_delete, name='crud_researchgroup_teacher_delete'),
