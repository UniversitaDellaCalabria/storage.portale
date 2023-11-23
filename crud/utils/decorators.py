from . utils import custom_message


def check_if_superuser(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func
