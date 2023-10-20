
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *

from .. utils.settings import *
from .. utils.utils import custom_message

def can_manage_laboratories(func_to_decorate):
    """
    List
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get('code'):
            laboratory = get_object_or_404(
                LaboratorioDatiBase, pk=original_kwargs['code'])
            original_kwargs['laboratory'] = laboratory


        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        
        my_offices = offices.filter(office__name=OFFICE_LABORATORIES)
        is_validator = offices.filter(office__name=OFFICE_LABORATORY_VALIDATORS).exists()

        
        original_kwargs['my_offices'] = my_offices
        original_kwargs['is_validator'] = is_validator
        
        if not (my_offices.exists() or is_validator):
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func

#Does not prevent POST from validator users
def can_view_laboratories(func_to_decorate):
    """
    Detail
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        laboratory = original_kwargs['laboratory']

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = original_kwargs['my_offices'] 
        department_id = laboratory.id_dipartimento_riferimento

        my_offices = my_offices.filter(office__organizational_structure__unique_code = department_id.dip_cod)
        original_kwargs['my_offices'] = my_offices
            
        if original_kwargs['is_validator'] or my_offices.exists():
            return func_to_decorate(*original_args, **original_kwargs)
               
        
        return custom_message(request, _("Permission denied"))

    return new_func

def check_if_superuser(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func

def can_edit_laboratories(func_to_decorate):
    """
    Detail
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)
        
        laboratory = original_kwargs['laboratory']
        my_offices = original_kwargs['my_offices']

        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))
        
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func