from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_phd(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_PHD,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_phd(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        phd = get_object_or_404(DidatticaDottoratoAttivitaFormativa, pk=original_kwargs['code'])
        teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(id_didattica_dottorato_attivita_formativa=phd.id)
        other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(id_didattica_dottorato_attivita_formativa=phd.id)
        original_kwargs['phd'] = phd
        original_kwargs['teachers'] = teachers
        original_kwargs['other_teachers'] = other_teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        for teacher in teachers:
            if not teacher.personale.sede in departments: continue
            return func_to_decorate(*original_args, **original_kwargs)
        for teacher in other_teachers:
            if not teacher.personale.sede in departments: continue
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
