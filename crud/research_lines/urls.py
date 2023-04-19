from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('baseresearchlines/', base_researchlines, name='crud_base_researchlines'),
urlpatterns += path('appliedresearchlines/', applied_researchlines, name='crud_applied_researchlines'),
urlpatterns += path('appliedresearchlines/new/', researchline_new_applied, name='crud_researchline_new_applied'),
urlpatterns += path('baseresearchlines/new/', researchline_new_base, name='crud_researchline_new_base'),
urlpatterns += path('baseresearchlines/<str:code>/', base_researchline, name='crud_base_researchline_edit'),
urlpatterns += path('appliedresearchlines/<str:code>/', applied_researchline, name='crud_applied_researchline_edit'),
urlpatterns += path('baseresearchlines/<str:code>/delete/', base_researchline_delete, name='crud_base_researchline_delete'),
urlpatterns += path('appliedresearchlines/<str:code>/delete/', applied_researchline_delete, name='crud_applied_researchline_delete'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/new/', base_researchline_teacher_new, name='crud_base_researchline_teacher_new'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/new/', applied_researchline_teacher_new, name='crud_applied_researchline_teacher_new'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', base_researchline_teacher_edit, name='crud_base_researchline_teacher_edit'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', applied_researchline_teacher_edit, name='crud_applied_researchline_teacher_edit'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', base_researchline_teacher_delete, name='crud_base_researchline_teacher_delete'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', applied_researchline_teacher_delete, name='crud_applied_researchline_teacher_delete'),
