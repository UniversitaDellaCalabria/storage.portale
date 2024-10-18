from django.urls import path

from .views import (
    teacher_board_data_delete,
    teacher_board_data_edit,
    teacher_board_data_new,
    teacher_detail,
    teacher_materials_data_delete,
    teacher_materials_data_edit,
    teacher_materials_data_new,
    teacher_other_data_delete,
    teacher_other_data_edit,
    teacher_other_data_new,
    teachers,
)

app_name = "management"

urlpatterns = [
    path('teachers/', teachers, name='teachers'),
    path('teachers/<str:encrypted_matricola>/', teacher_detail, name='teacher-edit'),
    path('teachers/<str:encrypted_matricola>/other-data/new/', teacher_other_data_new, name='teacher-other-data-new'),
    path('teachers/<str:encrypted_matricola>/other-data/<int:data_id>/', teacher_other_data_edit, name='teacher-other-data-edit'),
    path('teachers/<str:encrypted_matricola>/other-data/<int:data_id>/delete/', teacher_other_data_delete, name='teacher-other-data-delete'),
    path('teachers/<str:encrypted_matricola>/board/new/', teacher_board_data_new, name='teacher-board-data-new'),
    path('teachers/<str:encrypted_matricola>/board/<int:data_id>/', teacher_board_data_edit, name='teacher-board-data-edit'),
    path('teachers/<str:encrypted_matricola>/board/<int:data_id>/delete/', teacher_board_data_delete, name='teacher-board-data-delete'),
    path('teachers/<str:encrypted_matricola>/materials/new/', teacher_materials_data_new, name='teacher-materials-data-new'),
    path('teachers/<str:encrypted_matricola>/materials/<int:data_id>/', teacher_materials_data_edit, name='teacher-materials-data-edit'),
    path('teachers/<str:encrypted_matricola>/materials/<int:data_id>/delete/', teacher_materials_data_delete, name='teacher-materials-data-delete'),
]
