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

urlpatterns = []

urlpatterns += path('teachers/', teachers, name='teachers'),
urlpatterns += path('teachers/<str:code>/', teacher_detail, name='teacher-edit'),
urlpatterns += path('teachers/<str:code>/other-data/new/', teacher_other_data_new, name='teacher-other-data-new'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/', teacher_other_data_edit, name='teacher-other-data-edit'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/delete/', teacher_other_data_delete, name='teacher-other-data-delete'),
urlpatterns += path('teachers/<str:code>/board/new/', teacher_board_data_new, name='teacher-board-data-new'),
urlpatterns += path('teachers/<str:code>/board/<str:data_id>/', teacher_board_data_edit, name='teacher-board-data-edit'),
urlpatterns += path('teachers/<str:code>/board/<str:data_id>/delete/', teacher_board_data_delete, name='teacher-board-data-delete'),
urlpatterns += path('teachers/<str:code>/materials/new/', teacher_materials_data_new, name='teacher-materials-data-new'),
urlpatterns += path('teachers/<str:code>/materials/<str:data_id>/', teacher_materials_data_edit, name='teacher-materials-data-edit'),
urlpatterns += path('teachers/<str:code>/materials/<str:data_id>/delete/', teacher_materials_data_delete, name='teacher-materials-data-delete'),
