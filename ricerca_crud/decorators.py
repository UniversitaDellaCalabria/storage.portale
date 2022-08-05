from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import (OrganizationalStructure,
                                        OrganizationalStructureOfficeEmployee)

from ricerca_app.models import *

from . settings import *


OFFICE_RESEARCHGROUPS = getattr(settings,'OFFICE_RESEARCHGROUPS', OFFICE_RESEARCHGROUPS)
OFFICE_RESEARCHLINES = getattr(settings,'OFFICE_RESARCHLINES', OFFICE_RESEARCHLINES)
OFFICE_CDS = getattr(settings,'OFFICE_CDS', OFFICE_CDS)


def can_manage_researchgroups(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_RESEARCHGROUPS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_researchgroup(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rgroup = get_object_or_404(RicercaGruppo, pk=original_kwargs['code'])
        teachers = RicercaDocenteGruppo.objects.filter(ricerca_gruppo=rgroup)
        original_kwargs['rgroup'] = rgroup
        original_kwargs['teachers'] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede in departments:
                if teacher.dt_inizio and teacher.dt_inizio>now:
                    continue
                if teacher.dt_fine and teacher.dt_fine<now:
                    continue
                return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func


def can_manage_researchlines(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_RESEARCHLINES,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_base_researchline(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(RicercaLineaBase, pk=original_kwargs['code'])
        teachers = RicercaDocenteLineaBase.objects.filter(ricerca_linea_base=rline)
        original_kwargs['rline'] = rline
        original_kwargs['teachers'] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede in departments and teacher.dt_inizio<=now and teacher.dt_fine>=now:
                return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func


def can_edit_applied_researchline(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        rline = get_object_or_404(RicercaLineaApplicata, pk=original_kwargs['code'])
        teachers = RicercaDocenteLineaApplicata.objects.filter(ricerca_linea_applicata=rline)
        original_kwargs['rline'] = rline
        original_kwargs['teachers'] = teachers

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede in departments and teacher.dt_inizio<=now and teacher.dt_fine>=now:
                return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func


def can_manage_cds(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_CDS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_cds(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        cds = get_object_or_404(DidatticaCds, pk=original_kwargs['code'])
        teachers = DidatticaCdsAltriDati.objects.filter(cds_id=cds)
        offices = DidatticaCdsAltriDatiUfficio.objects.filter(cds_id=cds)
        original_kwargs['cds'] = cds
        original_kwargs['teachers'] = teachers
        original_kwargs['offices'] = offices


        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for teacher in teachers:
            if teacher.personale.sede in departments:
                if teacher.dt_inizio and teacher.dt_inizio>now:
                    continue
                if teacher.dt_fine and teacher.dt_fine<now:
                    continue
                return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func