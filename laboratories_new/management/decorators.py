from functools import wraps

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from laboratories.models import LaboratorioDatiBase, LaboratorioDipartimenti
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from organizational_area.models import OrganizationalStructureOfficeEmployee

from .utils import (
    _is_user_scientific_director,
    _is_user_scientific_director_of_any,
    _still_valid,
)


def can_manage_laboratories(func_to_decorate):
    @wraps(func_to_decorate)
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get("laboratory_id"):
            laboratory = get_object_or_404(
                LaboratorioDatiBase, pk=original_kwargs["laboratory_id"]
            )
            original_kwargs["laboratory"] = laboratory
            is_scientific_director = _is_user_scientific_director(request, laboratory)
        else:
            is_scientific_director = _is_user_scientific_director_of_any(request)

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )

        my_offices = offices.filter(office__name=OFFICE_LABORATORIES)
        is_validator = offices.filter(
            office__name=OFFICE_LABORATORY_VALIDATORS
        ).exists()

        original_kwargs["my_offices"] = my_offices
        original_kwargs["is_validator"] = is_validator

        if not (my_offices.exists() or is_validator or is_scientific_director):
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


# Does not prevent POST from validator users
def can_view_laboratories(func_to_decorate):
    @wraps(func_to_decorate)
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        laboratory = original_kwargs["laboratory"]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # Un laboratorio può avere più dipartimenti: l'operatore lo vede se il
        # suo ufficio appartiene a uno di quelli attualmente associati
        department_codes = LaboratorioDipartimenti.objects.filter(
            _still_valid(), laboratorio_dati_base=laboratory
        ).values_list("didattica_dipartimento__dip_cod", flat=True)

        my_offices = original_kwargs["my_offices"].filter(
            office__organizational_structure__unique_code__in=list(department_codes)
        )
        original_kwargs["my_offices"] = my_offices

        if (
            original_kwargs["is_validator"]
            or my_offices.exists()
            or _is_user_scientific_director(request, laboratory)
        ):
            return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func


def check_if_superuser(func_to_decorate):
    @wraps(func_to_decorate)
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        return custom_message(request, _("Permission denied"))

    return new_func


def can_edit_laboratories(func_to_decorate):
    @wraps(func_to_decorate)
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        laboratory = original_kwargs["laboratory"]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = original_kwargs["my_offices"]

        if not (
            my_offices.exists() or _is_user_scientific_director(request, laboratory)
        ):
            return custom_message(request, _("Permission denied"))

        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
