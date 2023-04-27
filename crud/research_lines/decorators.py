from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_researchlines(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_RESEARCHLINES,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_base_researchline(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(RicercaLineaBase, pk=original_kwargs['code'])
        teachers = RicercaDocenteLineaBase.objects.filter(
            ricerca_linea_base=rline)
        original_kwargs['rline'] = rline
        original_kwargs['teachers'] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

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


def can_edit_applied_researchline(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(
            RicercaLineaApplicata, pk=original_kwargs['code'])
        teachers = RicercaDocenteLineaApplicata.objects.filter(
            ricerca_linea_applicata=rline)
        original_kwargs['rline'] = rline
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
