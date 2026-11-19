import datetime
from contextlib import contextmanager

from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext as _
from django.db.models import Q
from laboratories_new.models import LaboratorioDatiBase, LaboratorioResponsabile
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

# Stato di lavorazione. Il campo VISIBILE della tabella vale come "approvato":
# ogni modifica lo mette a False, l'approvazione a True. La versione mostrata
# all'esterno e' sempre lo snapshot in corso (vedi snapshot_service).
STATUS_APPROVED = "approved"
STATUS_TO_APPROVE = "to_approve"


# DT_INS/DT_MOD della tabella PERSONALE sono DATE, ma il modello (InsModAbstract)
# li dichiara DateTimeField: se caricati, il backend MySQL fallisce la conversione
# ("'datetime.date' object has no attribute 'utcoffset'"). Vanno sempre esclusi.
PERSONALE_BROKEN_DATE_FIELDS = ("dt_ins", "dt_mod")


def defer_personale_dates(queryset, prefix="matricola_personale__"):
    """Esclude i campi data non convertibili di Personale da un queryset che lo carica."""
    return queryset.defer(*(prefix + f for f in PERSONALE_BROKEN_DATE_FIELDS))


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


def laboratory_statuses(approved):
    """
    {id: stato} a partire da {id: visibile (= approvato)}.

    - approved:   i dati nelle tabelle sono quelli approvati
    - to_approve: ci sono modifiche (o il laboratorio e' nuovo) da approvare
    """
    return {
        lab_id: STATUS_APPROVED if is_approved else STATUS_TO_APPROVE
        for lab_id, is_approved in approved.items()
    }


def laboratory_status(laboratory):
    """Stato di un singolo laboratorio, per la pagina di dettaglio."""
    return laboratory_statuses({laboratory.pk: laboratory.visibile})[laboratory.pk]


def approval_requested(laboratory):
    """True se e' stata inviata una richiesta di approvazione non ancora evasa."""
    return not laboratory.visibile and laboratory.pk in pending_approval_ids(
        [laboratory.pk]
    )


def _not_ended(today=None):
    """
    Q per i record non ancora chiusi (senza data_fine o con data_fine futura).

    Quando un incarico viene chiuso si imposta data_fine = oggi: da quel momento
    il record NON e' piu' in corso. Usare sempre questo criterio (e non
    data_fine >= oggi), altrimenti un incarico appena chiuso risulta ancora attivo
    fino a fine giornata.
    """
    today = today or datetime.date.today()
    return Q(data_fine__isnull=True) | Q(data_fine__gt=today)


def _still_valid(today=None):
    """Q per i record in corso (gia' iniziati e non ancora chiusi)."""
    today = today or datetime.date.today()
    return _not_ended(today) & (
        Q(data_inizio__isnull=True) | Q(data_inizio__lte=today)
    )


def is_still_valid(record, today=None):
    """Come _still_valid, ma su un oggetto gia' caricato (anche da snapshot)."""
    today = today or datetime.date.today()
    data_inizio = getattr(record, "data_inizio", None)
    data_fine = getattr(record, "data_fine", None)
    return (data_fine is None or data_fine > today) and (
        data_inizio is None or data_inizio <= today
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
    - rende il laboratorio NON visibile, cosi' serve una nuova approvazione.

    Lo snapshot NON viene toccato: resta la versione approvata, che l'API
    continua a mostrare finche' le modifiche non vengono approvate
    (vedi snapshot_service).
    """
    with transaction.atomic():
        # letta dal DB: il form potrebbe aver gia' modificato l'istanza in memoria
        was_visible = LaboratorioDatiBase.objects.filter(
            pk=laboratory.pk, visibile=True
        ).exists()
        yield
        laboratory.user_mod = request.user
        laboratory.dt_mod = datetime.datetime.now()
        laboratory.visibile = False
        laboratory.save()

    if was_visible:
        messages.add_message(
            request,
            messages.WARNING,
            _("Request a new approval to publish the changes."),
        )
