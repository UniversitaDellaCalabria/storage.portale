"""
Snapshot dei laboratori.

Lo snapshot in corso (data_fine_validita NULL) e' la versione VISIBILE del
laboratorio:

- all'avvio si crea lo snapshot di tutti i laboratori approvati, una volta sola a mano
  (create_all_snapshots / `manage.py create_laboratory_snapshots`);
- le modifiche vanno solo nelle tabelle e non toccano lo snapshot: mentre il
  laboratorio e' da approvare l'API continua a mostrare lo snapshot in corso;
- all'approvazione lo snapshot in corso viene chiuso e se ne crea uno nuovo dai
  dati attuali delle tabelle, che diventa quello attivo (refresh_snapshot).
"""

import json
import logging

from django.db import transaction
from django.utils import timezone

from .models import LaboratorioDatiBase, LaboratorioSnapshot
from .snapshot_exporter import laboratory_full_json

logger = logging.getLogger(__name__)


def _open_snapshots(lab_id):
    return LaboratorioSnapshot.objects.filter(
        laboratorio_id=lab_id, data_fine_validita__isnull=True
    )


def published_lab_ids():
    """Subquery con gli id dei laboratori visibili (con uno snapshot in corso)."""
    return LaboratorioSnapshot.objects.filter(
        data_fine_validita__isnull=True
    ).values("laboratorio_id")


def _snapshot_logo(json_laboratorio):
    """Percorso del logo salvato in un JSON di snapshot (None se assente)."""
    try:
        return json.loads(json_laboratorio).get("nome_file_logo") or None
    except (ValueError, AttributeError):
        return None


def published_logo_names(lab_id):
    """Percorsi dei loghi usati dagli snapshot in corso (la versione visibile)."""
    names = (
        _snapshot_logo(j)
        for j in _open_snapshots(lab_id).values_list("json_laboratorio", flat=True)
    )
    return {n for n in names if n}


def delete_logo_on_commit(name):
    """Cancella il file del logo solo se la transazione corrente va a buon fine."""
    if not name:
        return
    storage = LaboratorioDatiBase._meta.get_field("nome_file_logo").storage
    transaction.on_commit(lambda: storage.delete(name))


@transaction.atomic
def refresh_snapshot(lab_id, user=None):
    """
    Chiude lo snapshot in corso (se c'e') e ne crea uno nuovo dai dati attuali
    delle tabelle, che diventa quello attivo. Va chiamata all'approvazione,
    dentro la stessa transazione che segna il laboratorio come approvato.

    Il logo della versione pubblicata precedente, se e' stato sostituito, viene
    cancellato qui: durante le modifiche serviva ancora all'API (vedi signals).
    """
    # il lock evita due snapshot in corso se due approvazioni partono insieme
    LaboratorioDatiBase.objects.select_for_update().only("id").get(pk=lab_id)
    today = timezone.localdate()
    user_id = getattr(user, "pk", None)
    old_logos = published_logo_names(lab_id)
    _open_snapshots(lab_id).update(
        data_fine_validita=today, dt_mod=today, id_user_mod=user_id
    )
    json_laboratorio = laboratory_full_json(lab_id, indent=None)
    snapshot = LaboratorioSnapshot.objects.create(
        laboratorio_id=lab_id,
        json_laboratorio=json_laboratorio,
        data_inizio_validita=today,
        dt_mod=today,
        id_user_mod=user_id,
    )
    for name in old_logos - {_snapshot_logo(json_laboratorio)}:
        delete_logo_on_commit(name)
    return snapshot


def create_all_snapshots(user=None, only_missing=False):
    """
    Crea lo snapshot di TUTTI i laboratori presenti nel DB a partire dai dati
    attuali delle tabelle (da lanciare una volta a mano, es. con
    `manage.py create_laboratory_snapshots`). Gli snapshot in corso vengono chiusi.

    Solo i laboratori APPROVATI (visibile=True): lo snapshot in corso e' la
    versione pubblica, quindi crearlo per un laboratorio mai approvato lo
    pubblicherebbe, e per uno con modifiche in attesa sostituirebbe la versione
    approvata con dati non ancora approvati. Quelli esclusi vengono pubblicati
    all'approvazione.

    only_missing=True: salta i laboratori che hanno gia' uno snapshot in corso.
    Ritorna (creati, errori).
    """
    lab_ids = (
        LaboratorioDatiBase.objects.filter(visibile=True)
        .order_by("id")
        .values_list("id", flat=True)
    )
    if only_missing:
        lab_ids = lab_ids.exclude(id__in=published_lab_ids())

    created, errors = 0, []
    for lab_id in list(lab_ids):
        try:
            refresh_snapshot(lab_id, user)
            created += 1
        except Exception as e:  # un laboratorio rotto non blocca gli altri
            logger.exception("Snapshot del laboratorio %s non creato", lab_id)
            errors.append((lab_id, e))
    return created, errors


def current_snapshots(lab_ids):
    """{id_laboratorio: dati JSON dello snapshot corrente} per gli id dati."""
    out = {}
    qs = LaboratorioSnapshot.objects.filter(
        data_fine_validita__isnull=True, laboratorio_id__in=list(lab_ids)
    ).order_by("id")
    for s in qs:  # se ce ne fosse piu' di uno vince il piu' recente
        try:
            out[s.laboratorio_id] = s.data
        except ValueError:
            logger.error("JSON non valido nello snapshot %s", s.pk)
    return out
