import datetime
from contextlib import contextmanager

from django.db import transaction
from django.db.models import Q
from laboratories_new.models import LaboratorioDatiBase, LaboratorioResponsabile
from laboratories_new.snapshot_service import refresh_snapshot
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

ROLE_SCIENTIFIC_DIRECTOR = ("Responsabile scientifico", "Scientific director")
ROLE_SAFETY_MANAGER = ("Preposto alla sicurezza", "Safety manager")
ROLE_RESEARCH_STAFF = ("Personale di ricerca", "Research staff")

RESERVED_ROLES = (
    ROLE_SCIENTIFIC_DIRECTOR,
    ROLE_SAFETY_MANAGER,
    ROLE_RESEARCH_STAFF,
)
LOG_REQUESTED_APPROVAL = "Requested approval"
LOG_APPROVED = "Approved Laboratory"

STATUS_VISIBLE = "visible"
STATUS_EDIT = "edit"
STATUS_APPROVAL = "approval"
STATUS_HIDDEN = "hidden"


def _approval_log(lab_ids):
    """({id: ultima richiesta di approvazione}, {id: ultima approvazione})."""
    lab_ids = [str(i) for i in lab_ids]
    last_request, last_approval = {}, {}
    if not lab_ids:
        return last_request, last_approval
    entries = LogEntry.objects.filter(
        content_type=ContentType.objects.get_for_model(LaboratorioDatiBase),
        object_id__in=lab_ids,
        change_message__in=[LOG_REQUESTED_APPROVAL, LOG_APPROVED],
    ).order_by("action_time", "id")

    for e in entries:
        target = (
            last_request
            if e.change_message == LOG_REQUESTED_APPROVAL
            else last_approval
        )
        target[int(e.object_id)] = e.action_time
    return last_request, last_approval


def _pending(last_request, last_approval):
    return {
        lab_id
        for lab_id, requested_at in last_request.items()
        if lab_id not in last_approval or requested_at > last_approval[lab_id]
    }


def pending_approval_ids(lab_ids):
    """Id dei laboratori con una richiesta di approvazione più recente dell'ultima approvazione."""
    return _pending(*_approval_log(lab_ids))


def laboratory_statuses(visibility):
    """
    {id: stato} a partire da {id: visibile}.

    - approval: richiesta di approvazione in attesa
    - visible:  laboratorio visibile
    - edit:     non visibile, ma gia' approvato in passato (modificato dopo l'approvazione)
    - hidden:   non visibile e mai approvato
    """
    last_request, last_approval = _approval_log(visibility)
    pending = _pending(last_request, last_approval)
    out = {}
    for lab_id, visible in visibility.items():
        if lab_id in pending:
            out[lab_id] = STATUS_APPROVAL
        elif visible:
            out[lab_id] = STATUS_VISIBLE
        elif lab_id in last_approval:
            out[lab_id] = STATUS_EDIT
        else:
            out[lab_id] = STATUS_HIDDEN
    return out


def laboratory_status(laboratory):
    """Stato di un singolo laboratorio, per la pagina di dettaglio."""
    return laboratory_statuses({laboratory.pk: laboratory.visibile})[laboratory.pk]


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

    - esegue il blocco `with` (le modifiche vanno sulle tabelle);
    - rende il laboratorio NON visibile, cosi' serve una nuova approvazione;
    - crea un nuovo snapshot dai dati aggiornati (chiudendo il precedente).
    """
    with transaction.atomic():
        yield
        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()
        refresh_snapshot(laboratory.pk, request.user)
