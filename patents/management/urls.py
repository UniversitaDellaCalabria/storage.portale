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

urlpatterns = [
    path('patents/', patents, name='patents'),
    path('patents/new/', patent_new, name='patent-new'),
    path('patents/<int:patent_id>/', patent, name='patent-edit'),
    path('patents/<int:patent_id>/delete/', patent_delete, name='patent-delete'),
    path('patents/<int:patent_id>/inventor/new/', patent_inventor_new, name='patent-inventor-new'),
    path('patents/<int:patent_id>/inventor/<int:inventor_id>/', patent_inventor_edit, name='patent-inventor-edit'),
    path('patents/<int:patent_id>/inventor/<int:inventor_id>/delete/', patent_inventor_delete, name='patent-inventor-delete'),
]
