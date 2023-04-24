from organizational_area.models import OrganizationalStructureOfficeEmployee
from ricerca_app.utils import decrypt

from .. utils.settings import *


def can_manage_teacher(user, teacher_code):
    # se l'utente è un superuser
    if user.is_superuser:
        return True

    # se l'utente è il docente stesso
    my_profile = Personale.objects.filter(cod_fis=user.taxpayer_id).first()
    if my_profile:
        my_teacher_profile = ServiceDocente.getDocenteInfo(my_profile.matricola)

    # teacher_code = decrypt(original_kwargs['code'])
    teacher = Personale.objects.filter(matricola=teacher_code).first()
    if my_teacher_profile and my_teacher_profile == teacher:
        return True

    # se l'utente ha l'abilitazione nel dipartimento di afferenza del docente
    my_offices = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                      office__name=OFFICE_TEACHERS,
                                                                      office__is_active=True,
                                                                      office__organizational_structure__is_active=True)

    departments = []
    for myoffice in my_offices:
        if myoffice.office.organizational_structure.unique_code not in departments:
            departments.append(
                myoffice.office.organizational_structure.unique_code)
    if teacher.sede in departments:
        return True

    # se nessuna condizione è verificata
    return False
