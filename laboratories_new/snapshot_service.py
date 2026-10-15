from django.db import transaction
from django.utils import timezone

from .models import LaboratorioDatiBase, LaboratorioSnapshot
from .snapshot_exporter import laboratory_full_json


def _open_snapshots(lab_id):
    return LaboratorioSnapshot.objects.filter(
        laboratorio_id=lab_id, data_fine_validita__isnull=True
    )


def create_snapshot(lab_id, user=None):
    today = timezone.localdate()
    return LaboratorioSnapshot.objects.create(
        laboratorio_id=lab_id,
        json_laboratorio=laboratory_full_json(lab_id, indent=None),
        data_inizio_validita=today,
        dt_mod=today,
        id_user_mod=getattr(user, "pk", None),
    )


@transaction.atomic
def start_edit(lab_id, user=None):
    # il lock evita due snapshot aperti se due modifiche partono insieme
    LaboratorioDatiBase.objects.select_for_update().only("id").get(pk=lab_id)
    return _open_snapshots(lab_id).order_by("-id").first() or create_snapshot(
        lab_id, user
    )


@transaction.atomic
def end_edit(lab_id, user=None):
    today = timezone.localdate()
    return _open_snapshots(lab_id).update(
        data_fine_validita=today,
        dt_mod=today,
        id_user_mod=getattr(user, "pk", None),
    )
