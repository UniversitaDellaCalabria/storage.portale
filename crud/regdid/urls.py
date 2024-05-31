from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('regdid/', regdid_list, name='crud_regdid'),
# Structure
urlpatterns += path('regdid/structure/import/', regdid_structure_import, name='crud_regdid_structure_import'),
# Status
urlpatterns += path('regdid/<str:regdid_id>/status-change/<str:status_cod>/', regdid_status_change, name='crud_regdid_status_change'),
# Regdid PDF
urlpatterns += path('regdid/<str:regdid_id>/articles/pdf', regdid_articles_pdf, name='crud_regdid_articles_pdf'),
urlpatterns += path('regdid/<str:regdid_id>/articles/pdf-import', regdid_articles_import_pdf, name='crud_regdid_articles_import_pdf'),

# Regdid Articles
urlpatterns += path('regdid/<str:regdid_id>/articles/', regdid_articles, name='crud_regdid_articles'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/edit/', regdid_articles_edit, name='crud_regdid_articles_edit'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/delete/', regdid_articles_delete, name='crud_regdid_articles_delete'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_num>/new/', regdid_articles_new, name='crud_regdid_articles_new'),
# Regdid Sub Articles
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/<str:sub_article_id>/edit/', regdid_sub_articles_edit, name='crud_regdid_sub_articles_edit'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/<str:sub_article_id>/delete/', regdid_sub_articles_delete, name='crud_regdid_sub_articles_delete'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/new/', regdid_sub_articles_new, name='crud_regdid_sub_articles_new'),