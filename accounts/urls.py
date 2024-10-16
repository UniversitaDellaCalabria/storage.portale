from django.urls import path

from .views import account, changeData, confirmEmail

app_name = "accounts"


urlpatterns = [
    # url(r'^login/$', Login, name='login'),
    # path('logout', Logout, name='logout'),
    path("account/", account, name="account"),
    path("account/edit/", changeData, name="change_data"),
    path("account/edit/confirm-email/", confirmEmail, name="confirm_email"),
]
