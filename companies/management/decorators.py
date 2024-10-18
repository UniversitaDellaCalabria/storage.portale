from companies.models import SpinoffStartupDatiBase
from companies.settings import OFFICE_COMPANIES
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee


def can_manage_companies(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get("company_id"):
            company = get_object_or_404(
                SpinoffStartupDatiBase, pk=original_kwargs["company_id"]
            )
            original_kwargs["company"] = company

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_COMPANIES,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
