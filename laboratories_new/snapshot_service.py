"""
Snapshot dei laboratori.

Lo snapshot in corso (data_fine_validita NULL) e' la versione VISIBILE del
laboratorio:

- all'avvio si crea lo snapshot di tutti i laboratori, una volta sola a mano
  (create_all_snapshots / `manage.py create_laboratory_snapshots`);
- le modifiche vanno solo nelle tabelle e non toccano lo snapshot: mentre il
  laboratorio e' da approvare l'API continua a mostrare lo snapshot in corso;
- all'approvazione lo snapshot in corso viene chiuso e se ne crea uno nuovo dai
  dati attuali delle tabelle, che diventa quello attivo (refresh_snapshot).
"""

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


@transaction.atomic
def refresh_snapshot(lab_id, user=None):
    """
    Chiude lo snapshot in corso (se c'e') e ne crea uno nuovo dai dati attuali
    delle tabelle, che diventa quello attivo. Va chiamata all'approvazione,
    dentro la stessa transazione che segna il laboratorio come approvato.
    """
    # il lock evita due snapshot in corso se due approvazioni partono insieme
    LaboratorioDatiBase.objects.select_for_update().only("id").get(pk=lab_id)
    today = timezone.localdate()
    user_id = getattr(user, "pk", None)
    _open_snapshots(lab_id).update(
        data_fine_validita=today, dt_mod=today, id_user_mod=user_id
    )
    return LaboratorioSnapshot.objects.create(
        laboratorio_id=lab_id,
        json_laboratorio=laboratory_full_json(lab_id, indent=None),
        data_inizio_validita=today,
        dt_mod=today,
        id_user_mod=user_id,
    )


def create_all_snapshots(user=None, only_missing=False):
    """
    Crea lo snapshot di TUTTI i laboratori presenti nel DB a partire dai dati
    attuali delle tabelle (da lanciare una volta a mano, es. con
    `manage.py create_laboratory_snapshots`). Gli snapshot in corso vengono chiusi.

    only_missing=True: salta i laboratori che hanno gia' uno snapshot in corso.
    Ritorna (creati, errori).
    """
    lab_ids = LaboratorioDatiBase.objects.order_by("id").values_list("id", flat=True)
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
