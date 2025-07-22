from addressbook.models import Personale
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from laboratories.models import LaboratorioDatiBase
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from organizational_area.models import OrganizationalStructureOfficeEmployee
from .utils import _is_user_scientific_director


def can_manage_laboratories(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        is_scientific_director = False

        if original_kwargs.get("laboratory_id"):
            laboratory = get_object_or_404(
                LaboratorioDatiBase, pk=original_kwargs["laboratory_id"]
            )
            original_kwargs["laboratory"] = laboratory

            is_scientific_director = _is_user_scientific_director(request, laboratory)

        else:
            if request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(
                    cod_fis=request.user.taxpayer_id
                ).first()
                is_scientific_director = (
                    user_profile is not None
                    and LaboratorioDatiBase.objects.filter(
                        matricola_responsabile_scientifico=user_profile
                    ).exists()
                )

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
