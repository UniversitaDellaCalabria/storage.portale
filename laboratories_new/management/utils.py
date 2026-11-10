import datetime
from contextlib import contextmanager

from django.db import transaction
from django.db.models import Q
from laboratories_new.models import LaboratorioDatiBase, LaboratorioResponsabile
from laboratories_new.snapshot_service import start_edit

ROLE_SCIENTIFIC_DIRECTOR = ("Responsabile scientifico", "Scientific director")
ROLE_SAFETY_MANAGER = ("Preposto alla sicurezza", "Safety manager")
ROLE_RESEARCH_STAFF = ("Personale di ricerca", "Research staff")

RESERVED_ROLES = (
    ROLE_SCIENTIFIC_DIRECTOR,
    ROLE_SAFETY_MANAGER,
    ROLE_RESEARCH_STAFF,
)


def _still_valid(today=None):
    """Q per i record in corso (senza data_fine o con data_fine futura)."""
    today = today or datetime.date.today()
    return (Q(data_fine__isnull=True) | Q(data_fine__gt=today)) & (
        Q(data_inizio__isnull=True) | Q(data_inizio__lte=today)
    )


def _get_allowed_department_codes(request, offices):
    """
    Codici dei dipartimenti gestibili dall'operatore.

    None  -> nessuna restrizione (superuser)
    lista -> solo quei codici (lista vuota: nessun dipartimento)
    """
    if request.user.is_superuser:
        return None
    if offices is None:
        return []
    return list(
        offices.values_list(
            "office_id__organizational_structure_id__unique_code", flat=True
        )
    )


def _scientific_directors(taxpayer_id):
    """Responsabili scientifici interni in corso associati al codice fiscale."""
    return LaboratorioResponsabile.objects.filter(
        _still_valid(),
        laboratorio_ruolo__descr_ruolo_it=ROLE_SCIENTIFIC_DIRECTOR[0],
        matricola_personale__cod_fis__iexact=taxpayer_id,
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
    if (my_offices is not None and my_offices.exists()) or _is_user_scientific_director(
        request, laboratory
    ):
        roles["operator"] = True
    if is_validator:
        roles["validator"] = True
    return roles


@contextmanager
def edit_laboratory(request, laboratory):
    """
    Transazione di modifica di un laboratorio.

    - se il laboratorio e' visibile (approvato), prima di toccare i dati
      salva lo snapshot della versione approvata (start_edit e' idempotente:
      se c'e' gia' uno snapshot aperto lo riusa);
    - esegue il blocco `with`;
    - a fine blocco rende il laboratorio NON visibile, cosi' serve
      una nuova approvazione. L'API continua a servire lo snapshot.
    """
    with transaction.atomic():
        # visibilita' letta dal DB, non dall'istanza (il form potrebbe averla
        # gia' modificata in memoria)
        was_visible = LaboratorioDatiBase.objects.filter(
            pk=laboratory.pk, visibile=True
        ).exists()
        if was_visible:
            start_edit(laboratory.pk, request.user)
        yield
        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()
