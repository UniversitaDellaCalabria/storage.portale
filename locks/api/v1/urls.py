from django.urls import path

from .views import LockView, LockSetView

app_name = "apiv1"

urlpatterns = [
    path('lock/<int:content_type_id>/<int:object_id>/', LockView.as_view(), name='check-lock'),
    path('lock/set/', LockSetView.as_view(), name='set-lock'),
]
