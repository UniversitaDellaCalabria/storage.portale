import datetime
import logging

from cds.models import (
    DidatticaCds,
    DidatticaCdsCollegamento,
    DidatticaRegolamento,
    DidatticaCdsTipoCorso,
)
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE
from django.db import DatabaseError, IntegrityError, OperationalError, transaction
from django.db.models import (
    Case,
    Exists,
    F,
    IntegerField,
    Max,
    OuterRef,
    Prefetch,
    Subquery,
    When,
)
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from generics.utils import log_action, log_action_on_commit
from import_assistant.exceptions import (
    BaseImportError,
    EntryImportError,
    InvalidValueError,
    MissingKeysError,
    MissingValueError,
)
from import_assistant.settings import (
    ACCEPTED_TIPO_CORSO_COD,
    REGDID_IMPORT_DEFINE_NEW_STRUCTURE,
    REGDID_STRUCTURE_FIELDS,
    REGDID_STRUCTURE_MAPPINGS,
)
from regdid.models import (
    DidatticaArticoliRegolamentoStatus,
    DidatticaArticoliRegolamentoStruttura,
    DidatticaArticoliRegolamentoTitolo,
    DidatticaCdsArticoliRegolamento,
    DidatticaCdsArticoliRegolamentoTestata,
    DidatticaCdsSubArticoliRegolamento,
    DidatticaCdsTestataStatus,
)

logger = logging.getLogger(__name__)


# ------------------------
# Utility and Helper Functions
# ------------------------


def _handle_entry_import_error(request, error, entry_id, entry_name, ignore=True):
    """Helper function to handle entry import errors."""
    error.set_entry_name(entry_name)
    error.set_entry_id(entry_id)
    logger.error(str(error))
    messages.error(request, str(error))
    if ignore:
        error.skip_entry()
    else:
        raise BaseImportError(_("Import procedure FAILED: Bad Entry"))


def _handle_articles_import(request, year):
    """
    Handles the import of articles for REGDID structures.
    """
    testate_to_handle = 0
    testate_handled_successfully = 0

    # Fetch active CDS
    active_cds = _fetch_active_cds(year)

    # Fetch old testate
    old_testate = _fetch_old_testate(active_cds, year - 1)

    # Fetch and group structures by `tipo_corso_cod`
    tipo_corso_cod_strutture_map = _fetch_structures_by_year_grouped_by_cds_cod(year)

    for cds in active_cds:
        old_testata = old_testate.filter(updated_cds_id=cds.cds_id).first()
        try:
            with transaction.atomic():
                created, new_testata = _get_or_create_testata(
                    request, year, cds, old_testata
                )
                if not created:  # Skip existing testata
                    continue
                testate_to_handle += 1
                _process_testata(
                    request,
                    cds,
                    tipo_corso_cod_strutture_map,
                    new_testata,
                    old_testata,
                )
                testate_handled_successfully += 1
        except (IntegrityError, OperationalError, DatabaseError) as e:
            logger.error(_("Database error during transaction: {}").format(e))
        except EntryImportError as entry_error:
            _handle_entry_import_error(
                request, entry_error, cds.cds_cod, "Regdid for CDS"
            )

    return (testate_to_handle, testate_handled_successfully)


def _fetch_active_cds(year):
    """
    Fetches active CDS for a given year.
    """
    return DidatticaCds.objects.filter(
        Exists(
            DidatticaRegolamento.objects.filter(
                cds=OuterRef("cds_id"),
                aa_reg_did=year,
            ).exclude(stato_regdid_cod="R")
        ),
        tipo_corso_cod__in=ACCEPTED_TIPO_CORSO_COD,
    )


def _fetch_old_testate(active_cds, year):
    """
    Fetches old testate based on current year and active CDS.
    Prefetches articles related to each testata joined with their struttura joined with their tipo_corso
    """
    articoli_regolamento = DidatticaCdsArticoliRegolamento.objects.select_related(
        "didattica_articoli_regolamento_struttura__didattica_cds_tipo_corso"
    ).prefetch_related("didatticacdssubarticoliregolamento_set")

    active_cds_ids = active_cds.values_list("cds_id", flat=True)

    cds_collegamento_prec_ids = DidatticaCdsCollegamento.objects.values_list(
        "cds_prec_id", flat=True
    )

    return (
        DidatticaCdsArticoliRegolamentoTestata.objects.filter(aa=year)
        .prefetch_related(
            Prefetch(
                "didatticacdsarticoliregolamento_set", queryset=articoli_regolamento
            )
        )
        .select_related("cds")
        .annotate(
            updated_cds_id=Case(
                When(
                    cds_id__in=cds_collegamento_prec_ids,
                    then=Subquery(
                        DidatticaCdsCollegamento.objects.filter(
                            cds_prec_id=OuterRef("cds_id")
                        ).values("cds_id")[:1]
                    ),
                ),
                default=F("cds_id"),
                output_field=IntegerField(),
            )
        )
        .filter(updated_cds_id__in=active_cds_ids)
    )


def _fetch_structures_by_year_grouped_by_cds_cod(year):
    """
    Fetches and organizes structures for a given year by `tipo_corso_cod`.
    """
    strutture = (
        DidatticaArticoliRegolamentoStruttura.objects.select_related(
            "didattica_cds_tipo_corso"
        )
        .filter(
            didattica_cds_tipo_corso__tipo_corso_cod__in=ACCEPTED_TIPO_CORSO_COD,
            aa=year,
        )
        .order_by("didattica_cds_tipo_corso", "numero")
    )
    return {
        tipo_corso_cod: strutture.filter(
            didattica_cds_tipo_corso__tipo_corso_cod=tipo_corso_cod
        )
        for tipo_corso_cod in ACCEPTED_TIPO_CORSO_COD
    }


def _process_testata(
    request,
    cds,
    tipo_corso_cod_strutture_map,
    new_testata,
    old_testata=None,
):
    """
    Processes a single testata, importing articles and sub-articles.
    """
    strutture = tipo_corso_cod_strutture_map.get(cds.tipo_corso_cod)

    for struttura in strutture:
        old_articolo = (
            None
            if not old_testata
            else old_testata.didatticacdsarticoliregolamento_set.filter(
                didattica_articoli_regolamento_struttura__numero=struttura.numero_prec
            ).first()
        )
        _process_articolo(request, new_testata, struttura, old_articolo)


def _get_or_create_testata(request, year, cds, old_testata=None):
    created = False
    new_testata = DidatticaCdsArticoliRegolamentoTestata.objects.filter(
        cds=cds, aa=year
    ).first()
    if not new_testata:
        created = True
        new_testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            cds=cds,
            aa=year,
            note="",
            dt_mod=datetime.datetime.now(),
            user_mod=request.user,
        )
        log_action_on_commit(
            request.user,
            new_testata,
            ADDITION,
            _("Imported regulation testata from json for: Year {} and Cds {}").format(
                new_testata.aa, new_testata.cds.cds_cod
            ),
        )
        bozza_status = DidatticaArticoliRegolamentoStatus.objects.get(status_cod="0")
        DidatticaCdsTestataStatus.objects.create(
            didattica_articoli_regolamento_status=bozza_status,
            didattica_cds_articoli_regolamento_testata=new_testata,
            motivazione=_("Import from previous year"),
            data_status=datetime.datetime.now(),
            dt_mod=datetime.datetime.now(),
            user_mod=request.user,
        )
        log_action_on_commit(
            request.user,
            new_testata,
            CHANGE,
            _("Changed regdid status to '{}'.").format(bozza_status.status_desc),
        )
    return created, new_testata


def _process_articolo(request, new_testata, struttura_new, old_articolo=None):
    """
    Processes a single article, creating it and its sub-articles if it does not exist.
    """
    if DidatticaCdsArticoliRegolamento.objects.filter(
        didattica_cds_articoli_regolamento_testata=new_testata,
        didattica_articoli_regolamento_struttura=struttura_new,
    ).exists():
        return

    articolo_new = _create_new_articolo(
        request, new_testata, struttura_new, old_articolo
    )

    if not old_articolo:
        return

    for sub_old_articolo in old_articolo.didatticacdssubarticoliregolamento_set.all():
        _create_new_sub_articolo(request, sub_old_articolo, articolo_new)


def _create_new_articolo(request, new_testata, struttura_new, old_articolo=None):
    """
    Creates a new article based on the old one.
    """
    articolo = DidatticaCdsArticoliRegolamento.objects.create(
        didattica_articoli_regolamento_struttura=struttura_new,
        didattica_cds_articoli_regolamento_testata=new_testata,
        testo_it=old_articolo.testo_it if old_articolo else "",
        testo_en=old_articolo.testo_en if old_articolo else "",
        dt_mod=datetime.datetime.now(),
        user_mod=request.user,
        visibile=True,
    )

    log_action_on_commit(
        request.user,
        articolo,
        ADDITION,
        _("Imported Article number {} for Cds {}").format(
            articolo.didattica_articoli_regolamento_struttura.numero,
            new_testata.cds.cds_cod,
        ),
    )

    return articolo


def _create_new_sub_articolo(request, sub_old_articolo, articolo_new):
    """
    Creates a new sub-article based on the old one.
    """
    sub_articolo_new = DidatticaCdsSubArticoliRegolamento.objects.create(
        didattica_cds_articoli_regolamento=articolo_new,
        dt_mod=datetime.datetime.now(),
        ordine=sub_old_articolo.ordine,
        titolo_it=sub_old_articolo.titolo_it,
        titolo_en=sub_old_articolo.titolo_en,
        testo_it=sub_old_articolo.testo_it,
        testo_en=sub_old_articolo.testo_en,
        user_mod=request.user,
        visibile=True,
    )

    log_action_on_commit(
        request.user,
        sub_articolo_new,
        ADDITION,
        _("Imported sub-article with Order {} of Article number {} for Cds {}").format(
            sub_articolo_new.ordine,
            articolo_new.didattica_articoli_regolamento_struttura.numero,
            articolo_new.didattica_cds_articoli_regolamento_testata.cds.cds_cod,
        ),
    )


# ------------------------
# Main Import Logic
# ------------------------


def handle_regdid_structures_import(request, data, year, procedure_cod):
    """
    SCENARIO 1: REGDID_IMPORT_DEFINE_NEW_STRUCTURE

    IMPORT REGDID STRUCTURES VIA JSON

    GOAL: Remove structures for the year entered in the form

    -- Delete structures (year), testate, articles, and sub-articles:
        1) Validate entries provided via json.
        2) Delete the articles.
        3) Delete the testate and related testata statuses.
        4) Delete the structures.

    GOAL: Define regdid structures, create a testata and a testata status for each active CDS and import articles/sub-articles from the previous year

    -- Import new structures, create testate, and import articles and sub-articles:
        1) Import new structures.
        2) For each active course, create a testata and the associated testata status.
        3) Create/import articles:
            3.1) Import from the previous year if NUMERO_PREC is populated for the relevant structure.
            3.2) Create from scratch.

    SCENARIO 2: REGDID_IMPORT_USE_CURR_STRUCTURE

    GOAL: For each active CDS who's missing its testata, create one and a testata status, then import articles/sub-articles from the previous year

    -- Create missing testate and import articles and sub-articles only for these:
        1) For each active course lacking a testata, create the testata and the associated testata status.
        2) Create/import articles:
            3.1) Import from the previous year if NUMERO_PREC is populated for the relevant structure; otherwise create it from scratch.
    """
    created_structures = 0
    total_structures = len(data)

    if procedure_cod == REGDID_IMPORT_DEFINE_NEW_STRUCTURE:
        _validate_entries(request, data)
        _handle_existing_data_deletion(year)
        created_structures = _import_structures(request, data, year)
        messages.success(
            request,
            _("Structures created {}, out of {}").format(
                created_structures, total_structures
            ),
        )

    testate_to_handle, handled_testate = _handle_articles_import(request, year)

    imported_regdids_message = _("Done. Regdid imported {} out of {}").format(
        handled_testate, testate_to_handle, len(data)
    )

    if testate_to_handle == handled_testate:
        messages.warning(request, imported_regdids_message)
    else:
        messages.success(request, imported_regdids_message)


def _handle_existing_data_deletion(year):
    _check_for_approved_regulations(year)
    _delete_existing_articles_and_sub_articles(year)
    _delete_existing_testate(year)
    _delete_existing_structures(year)


def _check_for_approved_regulations(year):
    """Verify there is no approved regulation for the year, otherwise rise BaseImportError"""
    approved_testate = _get_all_approved_testate(year)
    # If any regulation is already approved abort procedure!
    if approved_testate.exists():
        raise BaseImportError(
            "Cannot create/update structures because some of them are related to one or more approved regdids"
        )


def _delete_existing_articles_and_sub_articles(year):
    """Delete articles (and sub-articles cascade)"""
    existing_articles = DidatticaCdsArticoliRegolamento.objects.filter(
        didattica_articoli_regolamento_struttura__aa=year
    )
    existing_articles_count = existing_articles.count()
    existing_articles.delete()
    logger.info(
        _("Removed {} articles (and potential sub-articles) for the year {}").format(
            existing_articles_count, year
        )
    )


def _delete_existing_testate(year):
    """Delete testate and testata status"""
    existing_testate = DidatticaCdsArticoliRegolamentoTestata.objects.filter(aa=year)
    existing_testate_count = existing_testate.count()
    existing_testata_statuses = DidatticaCdsTestataStatus.objects.filter(
        didattica_cds_articoli_regolamento_testata__in=existing_testate
    )
    existing_testata_statuses_count = existing_testata_statuses.count()
    existing_testata_statuses.delete()
    logger.info(
        _("Removed {} testata status for the year {}").format(
            existing_testata_statuses_count, year
        )
    )
    existing_testate.delete()
    logger.info(
        _("Removed {} structures for the year {}").format(existing_testate_count, year)
    )


def _delete_existing_structures(year):
    """Delete structures"""
    existing_structures = DidatticaArticoliRegolamentoStruttura.objects.filter(aa=year)
    existing_structures_count = existing_structures.count()
    existing_structures.delete()
    logger.info(
        _("Removed {} structures for the year {}").format(
            existing_structures_count, year
        )
    )


def _get_all_approved_testate(year):
    """Fetches all Testata, given a year, whose latest status is 'Approved'"""
    # Subquery to get the latest status ID for each testata
    latest_status_subquery = (
        DidatticaCdsTestataStatus.objects.filter(
            didattica_cds_articoli_regolamento_testata=OuterRef(
                "didattica_cds_articoli_regolamento_testata"
            )
        )
        .values("didattica_cds_articoli_regolamento_testata")
        .annotate(latest_id=Coalesce(Max("id"), 0))
        .values("latest_id")[:1]
    )
    testate = DidatticaCdsArticoliRegolamentoTestata.objects.filter(
        Exists(
            DidatticaCdsTestataStatus.objects.filter(
                id=Subquery(latest_status_subquery),  # Ensure it's the latest record
                didattica_cds_articoli_regolamento_testata_id=OuterRef("pk"),
                didattica_articoli_regolamento_status__status_cod="3",  # Approved status
            )
        ),
        aa=year,
    )
    return testate


def _validate_entries(request, data):
    """Loops through the given data and validates all the entries"""
    required_fields = [
        field["name"] for field in REGDID_STRUCTURE_FIELDS if field["required"]
    ]
    titolo_ids = DidatticaArticoliRegolamentoTitolo.objects.values_list("id", flat=True)
    for entry_id, entry in enumerate(data):
        try:
            # Validate entry
            _validate_entry(entry, required_fields, titolo_ids)
        except EntryImportError as entry_error:
            _handle_entry_import_error(
                request, entry_error, entry_id, "Structure", ignore=False
            )


def _validate_entry(entry, required_fields, titolo_ids):
    """Validates that all required fields and values are present in the data and acceptable."""
    missing_keys = [key for key in required_fields if key not in entry]
    if missing_keys:
        raise MissingKeysError(keys=missing_keys)

    def is_field_required(field_name):
        return field_name in required_fields

    tipo_corso_cod = entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"], None)
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"],
        value=tipo_corso_cod,
        is_required=is_field_required,
        extra_predicates=[lambda name, value: value in ACCEPTED_TIPO_CORSO_COD],
    )

    numero = entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"], None)
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["NUMERO"],
        value=numero,
        is_required=is_field_required,
        extra_predicates=[
            lambda name, value: isinstance(value, int)
            and not isinstance(value, bool)
            and value > 1
        ],
    )

    numero_prec = entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"], None)
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"],
        value=numero_prec,
        is_required=is_field_required,
        extra_predicates=[
            lambda name, value: isinstance(value, int) and not isinstance(value, bool)
        ],
    )

    titolo_id = entry.get(
        REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"], None
    )
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"],
        value=titolo_id,
        is_required=is_field_required,
        extra_predicates=[
            lambda name, value: isinstance(value, int)
            and not isinstance(value, bool)
            and value in titolo_ids
        ],
    )

    titolo_it = entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"], None)
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"],
        value=titolo_it,
        is_required=is_field_required,
        extra_predicates=[lambda name, value: isinstance(value, str)],
    )

    titolo_en = entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"], None)
    _validate_field(
        name=REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"],
        value=titolo_en,
        is_required=is_field_required,
        extra_predicates=[lambda name, value: value is None or isinstance(value, str)],
    )


def _validate_field(name, value, is_required, extra_predicates):
    # Check for missing values
    if is_required(name) and (value is None or value == ""):
        raise MissingValueError(field_name=name)
    # do other checks
    for predicate in extra_predicates:
        if not predicate(name, value):
            raise InvalidValueError(
                field_name=name,
                value=value,
            )


def _import_structures(request, data, year):
    created_structures = 0
    tipi_corso = DidatticaCdsTipoCorso.objects.all()
    for entry in data:
        structure = DidatticaArticoliRegolamentoStruttura.objects.create(
            aa=year,
            numero=entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
            numero_prec=entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"], None),
            titolo_it=entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"]),
            titolo_en=entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"], None),
            ordine=entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]) - 1,
            didattica_cds_tipo_corso=tipi_corso.filter(
                tipo_corso_cod=entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"])
            ).first(),
            didattica_articoli_regolamento_titolo_id=entry.get(
                REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"]
            ),
            visibile=True,
            dt_mod=datetime.datetime.now(),
            user_mod=request.user,
        )
        created_structures += 1
        log_action(
            request.user,
            structure,
            CHANGE,
            _(
                "Updated structure from json for: Year {}, Article Number {} and Course Type {}"
            ).format(
                year,
                entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
                entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"]),
            ),
        )
