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

urlpatterns = [
    path('baseresearchlines/', base_research_lines, name='base-research-lines'),
    path('baseresearchlines/new/', base_research_line_new, name='base-research-line-new'),
    path('baseresearchlines/<int:rline_id>/', base_research_line, name='base-research-line-edit'),
    path('baseresearchlines/<int:rline_id>/delete/', base_research_line_delete, name='base-research-line-delete'),

    path('baseresearchlines/<int:rline_id>/teacher/new/', base_research_line_teacher_new, name='base-research-line-teacher-new'),
    path('baseresearchlines/<int:rline_id>/teacher/<int:teacher_rline_id>/', base_research_line_teacher_edit, name='base-research-line-teacher-edit'),
    path('baseresearchlines/<int:rline_id>/teacher/<int:teacher_rline_id>/delete/', base_research_line_teacher_delete, name='base-research-line-teacher-delete'),

    path('appliedresearchlines/', applied_research_lines, name='applied-research-lines'),
    path('appliedresearchlines/new/', applied_research_lines_new, name='applied-research-line-new'),
    path('appliedresearchlines/<int:rline_id>/', applied_research_line, name='applied-research-line-edit'),
    path('appliedresearchlines/<int:rline_id>/delete/', applied_research_lines_delete, name='applied-research-line-delete'),

    path('appliedresearchlines/<int:rline_id>/teacher/new/', applied_researchline_teacher_new, name='applied-research-line-teacher-new'),
    path('appliedresearchlines/<int:rline_id>/teacher/<int:teacher_rline_id>/', applied_researchline_teacher_edit, name='applied-research-line-teacher-edit'),
    path('appliedresearchlines/<int:rline_id>/teacher/<int:teacher_rline_id>/delete/', applied_researchline_teacher_delete, name='applied-research-line-teacher-delete'),

    ]
