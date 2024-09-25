from django.urls import path

from .views import (
    applied_research_line,
    applied_research_lines,
    applied_research_lines_delete,
    applied_research_lines_new,
    applied_researchline_teacher_delete,
    applied_researchline_teacher_edit,
    applied_researchline_teacher_new,
    base_research_line,
    base_research_line_delete,
    base_research_line_new,
    base_research_line_teacher_delete,
    base_research_line_teacher_edit,
    base_research_line_teacher_new,
    base_research_lines,
)

app_name = "management"

urlpatterns = []

urlpatterns += path('baseresearchlines/', base_research_lines, name='base-research-lines'),
urlpatterns += path('baseresearchlines/new/', base_research_line_new, name='base-research-line-new'),
urlpatterns += path('baseresearchlines/<str:code>/', base_research_line, name='base-research-line-edit'),
urlpatterns += path('baseresearchlines/<str:code>/delete/', base_research_line_delete, name='base-research-line-delete'),

urlpatterns += path('appliedresearchlines/', applied_research_lines, name='applied-research-lines'),
urlpatterns += path('appliedresearchlines/new/', applied_research_lines_new, name='applied-research-line-new'),
urlpatterns += path('appliedresearchlines/<str:code>/', applied_research_line, name='applied-research-line-edit'),
urlpatterns += path('appliedresearchlines/<str:code>/delete/', applied_research_lines_delete, name='applied-research-line-delete'),

urlpatterns += path('appliedresearchlines/<str:code>/teacher/new/', applied_researchline_teacher_new, name='applied-research-line-teacher-new'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', applied_researchline_teacher_edit, name='applied-research-line-teacher-edit'),
urlpatterns += path('appliedresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', applied_researchline_teacher_delete, name='applied-research-line-teacher-delete'),

urlpatterns += path('baseresearchlines/<str:code>/teacher/new/', base_research_line_teacher_new, name='base-research-line-teacher-new'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/', base_research_line_teacher_edit, name='base-research-line-teacher-edit'),
urlpatterns += path('baseresearchlines/<str:code>/teacher/<str:teacher_rline_id>/delete/', base_research_line_teacher_delete, name='base-research-line-teacher-delete'),
