from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *

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
                                                                          office__is_active=True,
                                                                          office__organizational_structure__unique_code=STRUCTURE_PHD,
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

        phd = get_object_or_404(
            DidatticaDottoratoAttivitaFormativa, pk=original_kwargs['code'])
        teachers = DidatticaDottoratoAttivitaFormativaDocente.objects.filter(
            id_didattica_dottorato_attivita_formativa=phd.id)
        other_teachers = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.filter(
            id_didattica_dottorato_attivita_formativa=phd.id)
        original_kwargs['phd'] = phd
        original_kwargs['teachers'] = teachers
        original_kwargs['other_teachers'] = other_teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        for office in original_kwargs['my_offices']:
            if office.office.name == phd.rif_dottorato:
                return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func
