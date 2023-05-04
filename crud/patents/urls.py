from django.urls import path

from . views import *


urlpatterns = []

urlpatterns += path('patents/', patents, name='crud_patents'),
urlpatterns += path('patents/new/', patent_new, name='crud_patent_new'),
urlpatterns += path('patents/<str:code>/', patent, name='crud_patent_edit'),
urlpatterns += path('patents/<str:code>/inventor/new/', patent_inventor_new, name='crud_patent_inventor_new'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/', patent_inventor_edit, name='crud_patent_inventor_edit'),
urlpatterns += path('patents/<str:code>/inventor/<str:inventor_id>/delete/', patent_inventor_delete, name='crud_patent_inventor_delete'),
urlpatterns += path('patents/<str:code>/delete/', patent_delete, name='crud_patent_delete'),
