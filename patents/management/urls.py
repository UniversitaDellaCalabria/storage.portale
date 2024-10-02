from django.urls import path

from .views import (
    patent,
    patent_delete,
    patent_inventor_delete,
    patent_inventor_edit,
    patent_inventor_new,
    patent_new,
    patents,
)

app_name = "management"

urlpatterns = []


urlpatterns += path('patents/', patents, name='patents'),
urlpatterns += path('patents/new/', patent_new, name='patent-new'),
urlpatterns += path('patents/<str:code>/', patent, name='patent-edit'),
urlpatterns += path('patents/<str:code>/delete/', patent_delete, name='patent-delete'),
urlpatterns += path('patents/<str:code>/inventor/new/', patent_inventor_new, name='patent-inventor-new'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/', patent_inventor_edit, name='patent-inventor-edit'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/delete/', patent_inventor_delete, name='patent-inventor-delete'),
