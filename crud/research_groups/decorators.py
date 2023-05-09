from datetime import date

from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_researchgroups(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_RESEARCHGROUPS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_researchgroup(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rgroup = get_object_or_404(RicercaGruppo, pk=original_kwargs['code'])
        teachers = RicercaDocenteGruppo.objects.filter(ricerca_gruppo=rgroup)
        original_kwargs['rgroup'] = rgroup
        original_kwargs['teachers'] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(
                    myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if not teacher.personale.sede in departments:
                continue
            if teacher.dt_inizio and teacher.dt_inizio > now:
                continue
            if teacher.dt_fine and teacher.dt_fine < now:
                continue
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
