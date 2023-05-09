from django.urls import path

from . views import teacher_board_data_delete, teacher_board_data_edit, teacher_board_data_new, teacher_detail, teacher_materials_data_delete, teacher_materials_data_edit, teacher_materials_data_new, teacher_other_data_delete, teacher_other_data_edit, teacher_other_data_new, teachers


urlpatterns = []

urlpatterns += path('teachers/', teachers, name='crud_teachers'),
urlpatterns += path('teachers/<str:code>/', teacher_detail,
                    name='crud_teacher_edit'),
urlpatterns += path('teachers/<str:code>/other-data/new/',
                    teacher_other_data_new, name='crud_teacher_other_data_new'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/',
                    teacher_other_data_edit, name='crud_teacher_other_data_edit'),
urlpatterns += path('teachers/<str:code>/other-data/<str:data_id>/delete/',
                    teacher_other_data_delete, name='crud_teacher_other_data_delete'),
urlpatterns += path('teachers/<str:code>/board/new/',
                    teacher_board_data_new, name='crud_teacher_board_data_new'),
urlpatterns += path('teachers/<str:code>/board/<str:data_id>/',
                    teacher_board_data_edit, name='crud_teacher_board_data_edit'),
urlpatterns += path('teachers/<str:code>/board/<str:data_id>/delete/',
                    teacher_board_data_delete, name='crud_teacher_board_data_delete'),
urlpatterns += path('teachers/<str:code>/materials/new/',
                    teacher_materials_data_new, name='crud_teacher_materials_data_new'),
urlpatterns += path('teachers/<str:code>/materials/<str:data_id>/',
                    teacher_materials_data_edit, name='crud_teacher_materials_data_edit'),
urlpatterns += path('teachers/<str:code>/materials/<str:data_id>/delete/',
                    teacher_materials_data_delete, name='crud_teacher_materials_data_delete'),
