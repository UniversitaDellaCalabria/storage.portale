from functools import wraps

from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404


from ricerca_app.models import *

from .. utils.settings import *
from .. utils.utils import custom_message

def check_model_permissions(model):
    def decorator(view_function=None):
        @wraps(view_function)
        def wrapper(request, *original_args, **original_kwargs):
            if request.user.is_superuser or model.get_all_user_offices(request.user).exists():
                return view_function(request, *original_args, **original_kwargs)
            
            return custom_message(request, _("Permission denied"))
        
        return wrapper
    return decorator
    