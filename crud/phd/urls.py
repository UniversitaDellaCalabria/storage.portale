from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('phd/', phd_list, name='crud_phd_list'),
urlpatterns += path('phd/new/', phd_new, name='crud_phd_new'),
urlpatterns += path('phd/<str:code>/', phd, name='crud_phd_edit'),
urlpatterns += path('phd/<str:code>/main-teachers/<str:teacher_id>/', phd_main_teacher, name='crud_phd_main_teacher'),
urlpatterns += path('phd/<str:code>/main-teacher/new/', phd_main_teacher_new, name='crud_phd_main_teacher_new'),
urlpatterns += path('phd/<str:code>/main-teacher/<str:teacher_id>/delete/', phd_main_teacher_delete, name='crud_phd_main_teacher_delete'),
urlpatterns += path('phd/<str:code>/other-teachers/<str:teacher_id>/', phd_other_teacher, name='crud_phd_other_teacher'),
urlpatterns += path('phd/<str:code>/other-teacher/new/', phd_other_teacher_new, name='crud_phd_other_teacher_new'),
urlpatterns += path('phd/<str:code>/other-teacher/<str:teacher_id>/delete/', phd_other_teacher_delete, name='crud_phd_other_teacher_delete'),
urlpatterns += path('phd/<str:code>/delete/', phd_delete, name='crud_phd_delete'),
