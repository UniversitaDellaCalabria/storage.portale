from organizational_area.models import OrganizationalStructureOfficeEmployee

from ricerca_app.models import Personale
from ricerca_app.services import ServiceDocente

from .. utils.settings import *


def can_manage_teacher(user, teacher_code):
    if not user or not user.is_authenticated:
        return False

    if not teacher_code:
        return False

    teacher = Personale.objects.filter(matricola=teacher_code).first()
    if not teacher:
        return False

    # se l'utente è un superuser
    if user.is_superuser:
        return True

    # se l'utente è il docente stesso
    my_profile = Personale.objects.filter(cod_fis=user.taxpayer_id).first()
    my_teacher_profile = ServiceDocente.getDocenteInfo(my_profile.matricola)

    if my_profile and teacher and my_teacher_profile[0]['matricola'] == teacher:
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
