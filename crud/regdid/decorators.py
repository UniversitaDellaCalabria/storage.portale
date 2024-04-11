from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *

from .. utils.settings import *
from .. utils.utils import custom_message

def __get_user_roles(request, my_offices, department):
    roles = {
        "department_operator": False,
        "revision_operator": False,
        "approval_operator": False
    }    
    if my_offices.filter(office__name=OFFICE_REGDIDS_DEPARTMENT, office__organizational_structure__unique_code = department.dip_cod).exists():
        roles["department_operator"] = True
    if my_offices.filter(office__name=OFFICE_REGDIDS_REVISION).exists():
        roles["revision_operator"] = True
    if my_offices.filter(office__name=OFFICE_REGDIDS_APPROVAL).exists():
        roles["approval_operator"] = True
    
    return roles

def can_manage_regdid(func_to_decorate):

    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)
        
        offices = OrganizationalStructureOfficeEmployee.objects.filter( employee=request.user,
                                                                        office__is_active=True,
                                                                        office__organizational_structure__is_active=True)
         
        my_offices = offices.filter(office__name__in=[OFFICE_REGDIDS_DEPARTMENT, OFFICE_REGDIDS_REVISION, OFFICE_REGDIDS_APPROVAL])

        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func

def can_edit_regdid(func_to_decorate):

    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        
        regdid_id = original_kwargs.get('regdid_id', None)
        regdid = None
        if regdid_id is not None:
            regdid = get_object_or_404(DidatticaRegolamento, pk=regdid_id)
            original_kwargs["regdid"] = regdid          
        
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)
        
        my_offices = original_kwargs.get("my_offices", None)
        
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        
        if regdid:
            department = regdid.cds.dip
            roles = __get_user_roles(request, my_offices, department)

        original_kwargs["roles"] = roles
        
        for role in roles.values():
            if role == True:
                return func_to_decorate(*original_args, **original_kwargs)
            
        return custom_message(request, _("Permission denied"))

    return new_func
