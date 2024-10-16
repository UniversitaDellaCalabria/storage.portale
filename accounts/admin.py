from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ("date_joined", "last_login", "manual_user_update")
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_editable = (
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "username",
                        "is_active",
                        "is_staff",
                        "is_superuser",
                    ),
                    ("password"),
                )
            },
        ),
        (
            _("Anagrafica"),
            {"fields": (("first_name", "last_name"), "email", ("taxpayer_id",))},
        ),
        (
            _("Permissions"),
            {"fields": ("groups", "user_permissions"), "classes": ("collapse",)},
        ),
        (
            _("Date accessi sistema"),
            {"fields": (("date_joined", "last_login", "manual_user_update"))},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
