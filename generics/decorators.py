from functools import wraps

from django.utils.translation import gettext_lazy as _

from .utils import custom_message


def check_if_superuser(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func


def check_model_permissions(model):
    def decorator(view_function=None):
        @wraps(view_function)
        def wrapper(request, *original_args, **original_kwargs):
            if request.user.is_superuser or model.user_has_offices(request.user):
                return view_function(request, *original_args, **original_kwargs)

            return custom_message(request, _("Permission denied"))

        return wrapper

    return decorator
