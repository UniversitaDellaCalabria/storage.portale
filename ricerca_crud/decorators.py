from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import (OrganizationalStructure,
                                        OrganizationalStructureOfficeEmployee)

from ricerca_app.models import *
from ricerca_app.utils import decrypt, encrypt


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
            if not teacher.personale.sede in departments: continue
            if teacher.dt_inizio and teacher.dt_inizio>now: continue
            if teacher.dt_fine and teacher.dt_fine<now: continue
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
            if not teacher.personale.sede in departments: continue
            if teacher.dt_inizio and teacher.dt_inizio>now: continue
            if teacher.dt_fine and teacher.dt_fine<now: continue
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
            if not teacher.personale.sede in departments: continue
            if teacher.dt_inizio and teacher.dt_inizio>now: continue
            if teacher.dt_fine and teacher.dt_fine<now: continue
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
        regdid = DidatticaRegolamento.objects\
                                     .filter(pk=original_kwargs['regdid_id'])\
                                     .select_related('cds')\
                                     .first()

        original_kwargs['regdid'] = regdid


        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []

        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)

        if regdid.cds.dip.dip_cod in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func



def can_manage_patents(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_PATENTS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_patent(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        patent = get_object_or_404(BrevettoDatiBase, pk=original_kwargs['code'])
        inventors = BrevettoInventori.objects.filter(id_brevetto=patent)
        original_kwargs['patent'] = patent
        original_kwargs['inventors'] = inventors

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        now = date.today()
        for inventor in inventors:
            if inventor.personale.sede in departments:
                if inventor.dt_inizio and inventor.dt_inizio>now:
                    continue
                if inventor.dt_fine and inventor.dt_fine<now:
                    continue
                return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func


def can_manage_companies(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_COMPANIES,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_company(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        company = get_object_or_404(SpinoffStartupDatiBase, pk=original_kwargs['code'])
        departments = SpinoffStartupDipartimento.objects.filter(id_spinoff_startup_dati_base=company)
        original_kwargs['company'] = company
        original_kwargs['departments'] = departments

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)

        if company.matricola_referente_unical.ds_aff_org in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func


def can_manage_projects(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_PROJECTS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_project(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        project = get_object_or_404(ProgettoDatiBase, pk=original_kwargs['code'])
        researchers = ProgettoRicercatore.objects.filter(id_progetto=project)
        scientific_director = ProgettoResponsabileScientifico.objects.filter(id_progetto=project)
        original_kwargs['project'] = project
        original_kwargs['researchers'] = researchers
        original_kwargs['scientific_director'] = scientific_director


        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        if scientific_director.personale.sede in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        for researcher in researchers:
            if not researcher.personale.sede in departments: continue
            return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func



def can_manage_teachers(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_TEACHERS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices and not request.user.is_superuser:
            raise Exception("Permission denied")
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_teacher(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        teacher_code = decrypt(original_kwargs['code'])
        teacher = get_object_or_404(Personale, matricola=teacher_code)
        materials = DocenteMaterialeDidattico.objects.filter(matricola=teacher)
        other_data = DocentePtaAltriDati.objects.filter(matricola=teacher)
        board = DocentePtaBacheca.objects.filter(matricola=teacher)
        original_kwargs['teacher'] = teacher
        original_kwargs['materials'] = materials
        original_kwargs['other_data'] = other_data
        original_kwargs['board'] = board


        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        # if request.user == rgroup.user_ins:
            # return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(myoffice.office.organizational_structure.unique_code)
        if teacher.sede in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        raise Exception("Permission denied")

    return new_func
