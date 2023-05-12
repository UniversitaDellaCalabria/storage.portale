
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import *
from ricerca_app.services import ServiceDocente
from ricerca_app.utils import decrypt

from .. utils.settings import *
from .. utils.utils import custom_message


def can_manage_teachers(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]

        # ok se superuser
        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__name=OFFICE_TEACHERS,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True)
        # ok se nell'ufficio con privilegi per modificare i docenti
        if my_offices:
            original_kwargs['my_offices'] = my_offices
            return func_to_decorate(*original_args, **original_kwargs)

        # ok se io sono un docente
        try:
            my_profile = get_object_or_404(Personale,
                                           cod_fis=request.user.taxpayer_id)
            my_teacher_profile = ServiceDocente.getDocenteInfo(my_profile.matricola)
            original_kwargs['my_teacher_profile'] = my_teacher_profile
            return func_to_decorate(*original_args, **original_kwargs)
        except:
            return custom_message(request, _("Permission denied"))

    return new_func


def can_edit_teacher(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        teacher_code = decrypt(original_kwargs['code'])
        teacher = get_object_or_404(Personale, matricola=teacher_code)
        # materials = DocenteMaterialeDidattico.objects.filter(matricola=teacher)
        # other_data = DocentePtaAltriDati.objects.filter(matricola=teacher)
        # board = DocentePtaBacheca.objects.filter(matricola=teacher)
        original_kwargs['teacher'] = teacher
        # original_kwargs['materials'] = materials
        # original_kwargs['other_data'] = other_data
        # original_kwargs['board'] = board

        if request.user.is_superuser:
            return func_to_decorate(*original_args, **original_kwargs)

        if original_kwargs['my_teacher_profile'][0]['matricola'] == teacher.matricola:
            return func_to_decorate(*original_args, **original_kwargs)

        departments = []
        for myoffice in original_kwargs['my_offices']:
            if myoffice.office.organizational_structure.unique_code not in departments:
                departments.append(
                    myoffice.office.organizational_structure.unique_code)
        if teacher.sede in departments:
            return func_to_decorate(*original_args, **original_kwargs)
        return custom_message(request, _("Permission denied"))

    return new_func
