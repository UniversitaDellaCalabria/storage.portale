from cds_brochure.models import CdsBrochure
from cds_brochure.settings import OFFICE_CDS_BROCHURE
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee


def can_manage_cds_brochure(func_to_decorate):
    """ """

    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get("brochure_id"):
            cds_brochure_id = original_kwargs.get("brochure_id")
            cds_brochure = get_object_or_404(CdsBrochure, pk=cds_brochure_id)
            original_kwargs["cds_brochure"] = cds_brochure

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_CDS_BROCHURE,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))
        original_kwargs["my_offices"] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_cds_brochure(func_to_decorate):
    """ """

    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        cds_brochure = original_kwargs["cds_brochure"]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []

        for myoffice in original_kwargs["my_offices"]:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)

        if cds_brochure.cds.dip.dip_cod in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
