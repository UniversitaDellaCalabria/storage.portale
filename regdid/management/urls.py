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

urlpatterns = [
    path('regdid/', regdid_list, name='regdid'),

    # Structure
    path('regdid/structure/import/', regdid_structure_import, name='regdid-structure-import'),

    # Status
    path('regdid/<str:regdid_id>/status-change/<str:status_cod>/', regdid_status_change, name='regdid-status-change'),

    # Regdid PDF
    path('regdid/<int:regdid_id>/articles/pdf/', regdid_articles_pdf, name='regdid-articles-pdf'),
    path('regdid/<int:regdid_id>/articles/pdf-import/', regdid_articles_import_pdf, name='regdid-articles-import-pdf'),

    # Regdid publication
    path('regdid/<int:regdid_id>/articles/publish/', regdid_articles_publish, name='regdid-articles-publish'),

    # Regdid Articles
    path('regdid/<int:regdid_id>/articles/', regdid_articles, name='regdid-articles'),
    path('regdid/<int:regdid_id>/articles/<int:article_id>/edit/', regdid_articles_edit, name='regdid-articles-edit'),
    path('regdid/<int:regdid_id>/articles/<int:article_id>/delete/', regdid_articles_delete, name='regdid-articles-delete'),
    path('regdid/<int:regdid_id>/articles/<int:article_num>/new/', regdid_articles_new, name='regdid-articles-new'),

    # Regdid Sub Articles
    path('regdid/<int:regdid_id>/articles/<int:article_id>/sub/<int:sub_article_id>/edit/', regdid_sub_articles_edit, name='regdid-sub-articles-edit'),
    path('regdid/<int:regdid_id>/articles/<int:article_id>/sub/<int:sub_article_id>/delete/', regdid_sub_articles_delete, name='regdid-sub-articles-delete'),
    path('regdid/<int:regdid_id>/articles/<int:article_id>/sub/new/', regdid_sub_articles_new, name='regdid-sub-articles-new'),
]
