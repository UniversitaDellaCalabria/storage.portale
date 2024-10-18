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

urlpatterns = [
    path('phd/', phd_list, name='phd-list'),
    path('phd/new/', phd_new, name='phd-new'),
    path('phd/<int:phd_id>/', phd, name='phd-edit'),
    path('phd/<int:phd_id>/delete/', phd_delete, name='phd-delete'),
    path('phd/<int:phd_id>/main-teachers/<int:teacher_id>/', phd_main_teacher, name='phd-main-teacher'),
    path('phd/<int:phd_id>/main-teacher/new/', phd_main_teacher_new, name='phd-main-teacher-new'),
    path('phd/<int:phd_id>/main-teacher/<int:teacher_id>/delete/', phd_main_teacher_delete, name='phd-main-teacher-delete'),
    path('phd/<int:phd_id>/other-teachers/<int:teacher_id>/', phd_other_teacher, name='phd-other-teacher'),
    path('phd/<int:phd_id>/other-teacher/new/', phd_other_teacher_new, name='phd-other-teacher-new'),
    path('phd/<int:phd_id>/other-teacher/<int:teacher_id>/delete/', phd_other_teacher_delete, name='phd-other-teacher-delete'),
]
