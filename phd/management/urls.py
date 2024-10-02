from django.urls import path

from .views import (
    phd,
    phd_delete,
    phd_list,
    phd_main_teacher,
    phd_main_teacher_delete,
    phd_main_teacher_new,
    phd_new,
    phd_other_teacher,
    phd_other_teacher_delete,
    phd_other_teacher_new,
)

app_name = "management"

urlpatterns = []


urlpatterns += path('phd/', phd_list, name='phd-list'),
urlpatterns += path('phd/new/', phd_new, name='phd-new'),
urlpatterns += path('phd/<str:code>/', phd, name='phd-edit'),
urlpatterns += path('phd/<str:code>/delete/', phd_delete, name='phd-delete'),
urlpatterns += path('phd/<str:code>/main-teachers/<str:teacher_id>/', phd_main_teacher, name='phd-main-teacher'),
urlpatterns += path('phd/<str:code>/main-teacher/new/', phd_main_teacher_new, name='phd-main-teacher-new'),
urlpatterns += path('phd/<str:code>/main-teacher/<str:teacher_id>/delete/', phd_main_teacher_delete, name='phd-main-teacher-delete'),
urlpatterns += path('phd/<str:code>/other-teachers/<str:teacher_id>/', phd_other_teacher, name='phd-other-teacher'),
urlpatterns += path('phd/<str:code>/other-teacher/new/', phd_other_teacher_new, name='phd-other-teacher-new'),
urlpatterns += path('phd/<str:code>/other-teacher/<str:teacher_id>/delete/', phd_other_teacher_delete, name='phd-other-teacher-delete'),
