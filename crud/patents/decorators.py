from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_patents(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get('code'):
            patent = get_object_or_404(
                BrevettoDatiBase, pk=original_kwargs['code'])
            inventors = BrevettoInventori.objects.filter(id_brevetto=patent)
            original_kwargs['patent'] = patent
            original_kwargs['inventors'] = inventors

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_PATENTS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
