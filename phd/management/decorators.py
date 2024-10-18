from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee
from phd.models import DidatticaDottoratoAttivitaFormativa
from phd.settings import PHD_DEFAULT_OFFICE, STRUCTURE_PHD


def can_manage_phd(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__unique_code=STRUCTURE_PHD,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))

        original_kwargs["my_offices"] = my_offices

        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_phd(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        phd = get_object_or_404(
            DidatticaDottoratoAttivitaFormativa, pk=original_kwargs["phd_id"]
        )
        original_kwargs["phd"] = phd

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        for office in original_kwargs["my_offices"]:
            if office.office.name == PHD_DEFAULT_OFFICE:
                return func_to_decorate(*original_args, **original_kwargs)
            if office.office.name == phd.rif_dottorato:
                return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func
