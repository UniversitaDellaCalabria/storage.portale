
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_laboratories(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get('code'):
            laboratory = get_object_or_404(
                LaboratorioDatiBase, pk=original_kwargs['code'])
            original_kwargs['laboratory'] = laboratory

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_LABORATORIES,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func

def can_edit_laboartories(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        laboratory = original_kwargs['laboratory']

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        department_id = laboratory.id_dipartimento_riferimento

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                    office__name=OFFICE_LABORATORIES,
                                                                    office__is_active=True,
                                                                    office__organizational_structure__is_active=True)

        for myoffice in my_offices:
            if myoffice.office.organizational_structure.unique_code == department_id:
                return func_to_decorate(*original_args, **original_kwargs)
        
        return custom_message(request, _("Permission denied"))

    return new_func