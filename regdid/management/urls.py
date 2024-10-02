from django.urls import path

from .views import (
    regdid_articles,
    regdid_articles_delete,
    regdid_articles_edit,
    regdid_articles_import_pdf,
    regdid_articles_new,
    regdid_articles_pdf,
    regdid_articles_publish,
    regdid_list,
    regdid_status_change,
    regdid_structure_import,
    regdid_sub_articles_delete,
    regdid_sub_articles_edit,
    regdid_sub_articles_new,
)

app_name = "management"

urlpatterns = []


urlpatterns += path('regdid/', regdid_list, name='regdid'),
# Structure
urlpatterns += path('regdid/structure/import/', regdid_structure_import, name='regdid-structure-import'),
# Status
urlpatterns += path('regdid/<str:regdid_id>/status-change/<str:status_cod>/', regdid_status_change, name='regdid-status-change'),
# Regdid PDF
urlpatterns += path('regdid/<str:regdid_id>/articles/pdf/', regdid_articles_pdf, name='regdid-articles-pdf'),
urlpatterns += path('regdid/<str:regdid_id>/articles/pdf-import/', regdid_articles_import_pdf, name='regdid-articles-import-pdf'),
# Regdid publication
urlpatterns += path('regdid/<str:regdid_id>/articles/publish/', regdid_articles_publish, name='regdid-articles-publish'),

# Regdid Articles
urlpatterns += path('regdid/<str:regdid_id>/articles/', regdid_articles, name='regdid-articles'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/edit/', regdid_articles_edit, name='regdid-articles-edit'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/delete/', regdid_articles_delete, name='regdid-articles-delete'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_num>/new/', regdid_articles_new, name='regdid-articles-new'),
# Regdid Sub Articles
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/<str:sub_article_id>/edit/', regdid_sub_articles_edit, name='regdid-sub-articles-edit'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/<str:sub_article_id>/delete/', regdid_sub_articles_delete, name='regdid-sub-articles-delete'),
urlpatterns += path('regdid/<str:regdid_id>/articles/<str:article_id>/sub/new/', regdid_sub_articles_new, name='regdid-sub-articles-new'),
