from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *


def can_manage_cds(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_CDS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_cds(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        regdid = DidatticaRegolamento.objects\
                                     .filter(pk=original_kwargs['regdid_id'])\
                                     .select_related('cds')\
                                     .first()

        original_kwargs['regdid'] = regdid

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []

        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(
                    myoffice.office.organizational_structure.unique_code)

        if regdid.cds.dip.dip_cod in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func
