import datetime
import logging

from cds.models import (
    DidatticaCds,
    DidatticaCdsCollegamento,
    DidatticaCdsTipoCorso,
    DidatticaRegolamento,
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
from generics.utils import log_action_on_commit
from import_assistant.exceptions import (
    BaseImportError,
    EntryImportError,
    MissingKeysError,
    MissingValueError,
    InvalidValueError,
)
from import_assistant.settings import (
    ACCEPTED_TIPO_CORSO_COD,
    REGDID_STRUCTURE_FIELDS,
    REGDID_STRUCTURE_MAPPINGS,
)
from regdid.models import (
    DidatticaArticoliRegolamentoStatus,
    DidatticaArticoliRegolamentoStruttura,
    DidatticaCdsArticoliRegolamento,
    DidatticaCdsArticoliRegolamentoTestata,
    DidatticaCdsSubArticoliRegolamento,
    DidatticaCdsTestataStatus,
)

logger = logging.getLogger(__name__)


# ------------------------
# Utility and Helper Functions
# ------------------------


def _handle_entry_import_error(request, error, entry_id, entry_name):
    """Helper function to handle entry import errors."""
    error.set_entry_name(entry_name)
    error.set_entry_id(entry_id)
    error.skip_entry()
    logger.error(str(error))
    messages.error(request, str(error))


def _validate_entry(entry, required_fields):
    """Validates that all required fields and values are present in the data."""
    missing_keys = [key for key in required_fields if key not in entry]
    if missing_keys:
        raise MissingKeysError(keys=missing_keys)
    for key, value in entry.items():
        if key in required_fields and (value is None or value == ""):
            raise MissingValueError(field_name=key)
    if (
        entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"])
        not in ACCEPTED_TIPO_CORSO_COD
    ):
        raise InvalidValueError(
            field_name=REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"],
            value=entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"]),
        )


def _import_structures(request, data, year):
    """
    Imports structures from the given data into the database.
    Returns a map of new structures and counts of created and updated entries.
    """
    tot_created = 0
    tot_updated = 0
    affected_structures_map = {}

    # Prepare a map of `tipo_corso_id` to `tipo_corso_cod` for validation
    tipo_corso_cod_id_map = {
        item["tipo_corso_cod"]: item["id"]
        for item in DidatticaCdsTipoCorso.objects.filter(
            tipo_corso_cod__in=ACCEPTED_TIPO_CORSO_COD
        ).values("id", "tipo_corso_cod")
    }

    testate_approved = _get_all_approved_testate(year)

    for entry_id, entry in enumerate(data):
        try:
            # Validate entry
            required_fields = [
                field["name"] for field in REGDID_STRUCTURE_FIELDS if field["required"]
            ]
            _validate_entry(entry, required_fields)

            # Process entry
            try:
                with transaction.atomic():
                    structure, created = _create_or_update_article_structure(
                        request,
                        entry,
                        entry_id,
                        year,
                        tipo_corso_cod_id_map,
                        testate_approved,
                    )
                    affected_structures_map[structure.id] = structure

                    # Update counts
                    if created:
                        tot_created += 1
                    else:
                        tot_updated += 1
            except (IntegrityError, OperationalError, DatabaseError) as e:
                logger.error(_("Database error during transaction: {}").format(e))

        except EntryImportError as entry_error:
            _handle_entry_import_error(request, entry_error, entry_id, "Structure")

    return affected_structures_map, tot_created, tot_updated


def _create_or_update_article_structure(
    request, entry, entry_id, year, tipo_corso_cod_id_map, testate_approved
):
    created = False
    struttura = DidatticaArticoliRegolamentoStruttura.objects.filter(
        aa=year,
        numero=entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
        didattica_cds_tipo_corso_id=tipo_corso_cod_id_map.get(
            entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"])
        ),
    ).first()
    if struttura:
        # Check for existing Testata with last status approved related to an article, related to the structure, if exists raise BaseImportError
        structure_related_articles = DidatticaCdsArticoliRegolamento.objects.filter(
            didattica_articoli_regolamento_struttura=struttura
        )
        if structure_related_articles.filter(
            didattica_cds_articoli_regolamento_testata__in=testate_approved
        ).exists():
            raise BaseImportError(
                "Cannot create/update structures because some of them are related to one or more approved regdids"
            )

        # Update existing
        struttura.titolo_it = entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"])
        struttura.titolo_en = entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"], None)
        struttura.didattica_articoli_regolamento_titolo_id = entry.get(
            REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"]
        )
        struttura.ordine = entry_id
        struttura.dt_mod = datetime.datetime.now()
        struttura.user_mod = request.user
        struttura.visibile = True
        struttura.save()

        log_action_on_commit(
            request.user,
            struttura,
            CHANGE,
            _(
                "Updated structure from json for: Year {}, Article Number {} and Course Type {}"
            ).format(
                year,
                entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
                entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"]),
            ),
        )

    else:
        struttura = DidatticaArticoliRegolamentoStruttura.objects.create(
            aa=year,
            numero=entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
            titolo_it=entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_IT"]),
            titolo_en=entry.get(REGDID_STRUCTURE_MAPPINGS["TITOLO_EN"]),
            didattica_cds_tipo_corso_id=tipo_corso_cod_id_map.get(
                entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"])
            ),
            didattica_articoli_regolamento_titolo_id=entry.get(
                REGDID_STRUCTURE_MAPPINGS["DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO_ID"]
            ),
            ordine=entry_id,
            dt_mod=datetime.datetime.now(),
            user_mod=request.user,
            visibile=True,
        )
        created = True
        log_action_on_commit(
            request.user,
            struttura,
            ADDITION,
            _(
                "Imported structure from json for: Year {}, Article Number {} and Course Type {}"
            ).format(
                year,
                entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO"]),
                entry.get(REGDID_STRUCTURE_MAPPINGS["TIPO_CORSO_COD"]),
            ),
        )
    struttura.numero_prec = entry.get(REGDID_STRUCTURE_MAPPINGS["NUMERO_PREC"], None)

    return (struttura, created)


def _get_all_approved_testate(year):
    """
    Fetches all Testata, given a year, whose latest status is "Approved"
    """
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


def _remove_previous_articles_for_provided_structures(affected_structures_map):
    articles_to_remove = DidatticaCdsArticoliRegolamento.objects.filter(
        didattica_articoli_regolamento_struttura__in=affected_structures_map.values()
    )
    count = articles_to_remove.count()
    articles_to_remove.delete()
    logger.info(
        _("Removed all {} articles related to the updated structures").format(count)
    )


def _handle_articles_import(request, year, affected_structures_map):
    """
    Handles the import of articles for REGDID structures.
    """

    # Fetch active CDS
    active_cdss = _fetch_active_cds(year)

    # Fetch old testate
    old_testate = _fetch_old_testate(active_cdss, year - 1)

    # Fetch and group structures by `tipo_corso_cod`
    tipo_corso_cod_strutture_map = _fetch_structures_by_year_grouped_by_cds_cod(year)

    for cds in active_cdss:
        old_testata = old_testate.filter(updated_cds_id=cds.cds_id).first()
        try:
            with transaction.atomic():
                _process_testata(
                    request,
                    year,
                    cds,
                    tipo_corso_cod_strutture_map,
                    affected_structures_map,
                    old_testata,
                )
        except (IntegrityError, OperationalError, DatabaseError) as e:
            logger.error(_("Database error during transaction: {}").format(e))
        except EntryImportError as entry_error:
            _handle_entry_import_error(
                request, entry_error, cds.cds_cod, "Regdid for CDS"
            )


def _fetch_active_cds(year):
    """
    Fetches active CDS for a given year.
    """
    return DidatticaCds.objects.filter(
        Exists(
            DidatticaRegolamento.objects.filter(
                cds=OuterRef("cds_id"),
                aa_reg_did=year,
                stato_regdid_cod="A",
            )
        ),
        tipo_corso_cod__in=ACCEPTED_TIPO_CORSO_COD,
    )


def _fetch_old_testate(active_cdss, year):
    """
    Fetches old testate based on current year and active CDS.
    Prefetches articles related to each testata joined with their struttura joined with their tipo_corso
    """
    articoli_regolamento = DidatticaCdsArticoliRegolamento.objects.select_related(
        "didattica_articoli_regolamento_struttura__didattica_cds_tipo_corso"
    ).prefetch_related("didatticacdssubarticoliregolamento_set")

    active_cds_ids = active_cdss.values_list("cds_id", flat=True)

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
    year,
    cds,
    tipo_corso_cod_strutture_map,
    affected_structures_map,
    old_testata=None,
):
    """
    Processes a single testata, importing articles and sub-articles.
    """
    new_testata = _get_or_create_testata(request, year, cds, old_testata)

    strutture = tipo_corso_cod_strutture_map.get(cds.tipo_corso_cod)

    for struttura in strutture:
        corresponding_imported_structure = affected_structures_map.get(
            struttura.id, None
        )
        old_articolo = (
            None
            if not old_testata or corresponding_imported_structure is None
            else old_testata.didatticacdsarticoliregolamento_set.filter(
                didattica_articoli_regolamento_struttura__numero=corresponding_imported_structure.numero_prec
            ).first()
        )
        _process_articolo(request, new_testata, struttura, old_articolo)


def _get_or_create_testata(request, year, cds, old_testata=None):
    new_testata = DidatticaCdsArticoliRegolamentoTestata.objects.filter(
        cds=cds, aa=year
    ).first()
    if not new_testata:
        new_testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            cds=cds,
            aa=year,
            note=old_testata.note if old_testata else "",
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
    return new_testata


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


def handle_regdid_structures_import(request, data, year, copy_previous):
    """
    Handles the import of REGDID structures.
    Optionally copies previous articles.
    """
    # Import structures
    affected_structures_map, total_created, total_updated = _import_structures(
        request, data, year
    )

    # Copy previous articles if requested
    if copy_previous:
        _remove_previous_articles_for_provided_structures(affected_structures_map)
        _handle_articles_import(request, year, affected_structures_map)

    return (total_created, total_updated)