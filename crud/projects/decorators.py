from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_projects(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_PROJECTS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        original_kwargs['my_offices'] = my_offices
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_edit_project(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        project = get_object_or_404(
            ProgettoDatiBase, pk=original_kwargs['code'])
        researchers = ProgettoRicercatore.objects.filter(id_progetto=project)
        scientific_director = ProgettoResponsabileScientifico.objects.filter(
            id_progetto=project)
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
                departments.append(
                    myoffice.office.organizational_structure.unique_code)
        if project.uo.uo in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func