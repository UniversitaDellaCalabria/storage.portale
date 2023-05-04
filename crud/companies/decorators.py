from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_companies(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get('code'):
            company = get_object_or_404(
                SpinoffStartupDatiBase, pk=original_kwargs['code'])
            original_kwargs['company'] = company

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_COMPANIES,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
