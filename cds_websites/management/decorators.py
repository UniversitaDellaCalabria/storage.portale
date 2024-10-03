from cds.models import DidatticaCds
from cds_websites.settings import OFFICE_CDS_WEBSITES, OFFICE_CDS_WEBSITES_STRUCTURES
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee


def can_manage_cds_website(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if original_kwargs.get("cds_id"):
            cds_id = original_kwargs.get("cds_id")
            cds = get_object_or_404(DidatticaCds, pk=cds_id)
            original_kwargs["cds"] = cds

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name__in=[OFFICE_CDS_WEBSITES, OFFICE_CDS_WEBSITES_STRUCTURES],
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices.exists():
            return custom_message(request, _("Permission denied"))
        original_kwargs["my_offices"] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_cds_website(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        cds = original_kwargs["cds"]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []

        for myoffice in original_kwargs["my_offices"]:
            if myoffice.office.name == OFFICE_CDS_WEBSITES_STRUCTURES:
                return func_to_decorate(*original_args, **original_kwargs)
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)

        if cds.dip.dip_cod in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func


def can_edit_cds_website_structure(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        for myoffice in original_kwargs["my_offices"]:
            if myoffice.office.name == OFFICE_CDS_WEBSITES_STRUCTURES:
                return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
