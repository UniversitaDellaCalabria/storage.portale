from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from generics.utils import custom_message
from organizational_area.models import OrganizationalStructureOfficeEmployee
from projects.models import ProgettoDatiBase
from projects.settings import OFFICE_PROJECTS


def can_manage_projects(func_to_decorate):
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if original_kwargs.get("code"):
            project = get_object_or_404(ProgettoDatiBase, pk=original_kwargs["code"])
            original_kwargs["project"] = project

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
            employee=request.user,
            office__name=OFFICE_PROJECTS,
            office__is_active=True,
            office__organizational_structure__is_active=True,
        )
        if not my_offices:
            return custom_message(request, _("Permission denied"))
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


# def can_edit_project(func_to_decorate):
# """
# """
# def new_func(*original_args, **original_kwargs):
# request = original_args[0]
# project = get_object_or_404(
# ProgettoDatiBase, pk=original_kwargs['code'])
# researchers = ProgettoRicercatore.objects.filter(id_progetto=project)
# scientific_director = ProgettoResponsabileScientifico.objects.filter(
# id_progetto=project)
# original_kwargs['project'] = project
# original_kwargs['researchers'] = researchers
# original_kwargs['scientific_director'] = scientific_director

# if request.user.is_superuser:
# return func_to_decorate(*original_args, **original_kwargs)

# departments = []
# for myoffice in original_kwargs['my_offices']:
# if myoffice.office.organizational_structure.unique_code not in departments:
# departments.append(
# myoffice.office.organizational_structure.unique_code)
# if project.uo.uo in departments:
# return func_to_decorate(*original_args, **original_kwargs)
# return custom_message(request, _("Permission denied"))

# return new_func
