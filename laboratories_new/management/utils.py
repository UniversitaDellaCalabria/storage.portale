import datetime

from addressbook.models import Personale
from django.db.models import Q
from laboratories.models import LaboratorioResponsabile

ROLE_SCIENTIFIC_DIRECTOR = ("Responsabile scientifico", "Scientific director")
ROLE_SAFETY_MANAGER = ("Preposto alla sicurezza", "Safety manager")
ROLE_RESEARCH_STAFF = ("Personale di ricerca", "Research staff")


def _still_valid():
    """Q per i record in corso (senza data_fine o con data_fine futura)."""
    return Q(data_fine__isnull=True) | Q(data_fine__gte=datetime.date.today())


def _scientific_directors(taxpayer_id):
    """Responsabili scientifici interni in corso associati al codice fiscale."""
    return LaboratorioResponsabile.objects.filter(
        _still_valid(),
        laboratorio_ruolo__descr_ruolo_it=ROLE_SCIENTIFIC_DIRECTOR[0],
        matricola_personale__cod_fis=taxpayer_id,
    )


def _is_user_scientific_director(request, laboratory):
    taxpayer_id = getattr(request.user, "taxpayer_id", None)
    if not taxpayer_id:
        return False
    return (
        _scientific_directors(taxpayer_id)
        .filter(laboratorio_dati_base=laboratory)
        .exists()
    )


def _is_user_scientific_director_of_any(request):
    taxpayer_id = getattr(request.user, "taxpayer_id", None)
    if not taxpayer_id:
        return False
    return _scientific_directors(taxpayer_id).exists()


def _get_user_roles(request, laboratory, my_offices, is_validator):
    roles = {"superuser": False, "operator": False, "validator": False}
    if request.user.is_superuser:
        roles["superuser"] = True
        return roles
    if my_offices.exists() or _is_user_scientific_director(request, laboratory):
        roles["operator"] = True
    if is_validator:
        roles["validator"] = True
    return roles
