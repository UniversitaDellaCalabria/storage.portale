from cds.models import DidatticaRegolamento
from cds.settings import OFFICE_CDS, OFFICE_CDS_DOCUMENTS, OFFICE_CDS_TEACHING_SYSTEM
from django.utils.translation import gettext_lazy as _
from generics.settings import CURRENT_YEAR
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee


def can_manage_cds(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name__in=[
                OFFICE_CDS,
                OFFICE_CDS_DOCUMENTS,
                OFFICE_CDS_TEACHING_SYSTEM,
            ],
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs["my_offices"] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_cds(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        regdid = (
            DidatticaRegolamento.objects.filter(pk=original_kwargs["regdid_id"])
            .select_related("cds")
            .first()
        )

        original_kwargs["regdid"] = regdid

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        if regdid.aa_reg_did > CURRENT_YEAR:
            return custom_message(
                request,
                _("Educational offer not yet available for the year")
                + f": {regdid.aa_reg_did}",
            )

        departments = []

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_CDS,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        # for myoffice in original_kwargs['my_offices']:
        for myoffice in my_offices:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)

        if regdid.cds.dip.dip_cod in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func


def can_manage_cds_documents(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        regdid = (
            DidatticaRegolamento.objects.filter(pk=original_kwargs["regdid_id"])
            .select_related("cds")
            .first()
        )

        original_kwargs["regdid"] = regdid

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        if regdid.aa_reg_did > CURRENT_YEAR:
            return custom_message(
                request,
                _("Educational offer not yet available for the year")
                + f": {regdid.aa_reg_did}",
            )

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_CDS_DOCUMENTS,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_manage_cds_teaching_system(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        regdid = (
            DidatticaRegolamento.objects.filter(pk=original_kwargs["regdid_id"])
            .select_related("cds")
            .first()
        )

        original_kwargs["regdid"] = regdid

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        if regdid.aa_reg_did > CURRENT_YEAR:
            return custom_message(
                request,
                _("Educational offer not yet available for the year")
                + f": {regdid.aa_reg_did}",
            )

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_CDS_TEACHING_SYSTEM,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
