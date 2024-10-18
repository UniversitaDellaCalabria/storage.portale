from datetime import date

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)
from research_lines.settings import OFFICE_RESEARCH_LINES


def can_manage_research_lines(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_RESEARCH_LINES,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs["my_offices"] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_base_research_line(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(RicercaLineaBase, pk=original_kwargs["rline_id"])
        teachers = RicercaDocenteLineaBase.objects.filter(ricerca_linea_base=rline)
        original_kwargs["rline"] = rline
        original_kwargs["teachers"] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
        # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs["my_offices"]:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede not in departments:
                continue
            if teacher.dt_inizio and teacher.dt_inizio > now:
                continue
            if teacher.dt_fine and teacher.dt_fine < now:
                continue
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func


def can_edit_applied_research_line(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(RicercaLineaApplicata, pk=original_kwargs["rline_id"])
        teachers = RicercaDocenteLineaApplicata.objects.filter(
            ricerca_linea_applicata=rline
        )
        original_kwargs["rline"] = rline
        original_kwargs["teachers"] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs["my_offices"]:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede not in departments:
                continue
            if teacher.dt_inizio and teacher.dt_inizio > now:
                continue
            if teacher.dt_fine and teacher.dt_fine < now:
                continue
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
