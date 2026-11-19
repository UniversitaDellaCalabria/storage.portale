from django.core.management.base import BaseCommand

from laboratories_new.snapshot_service import create_all_snapshots


class Command(BaseCommand):
    help = (
        "Crea lo snapshot di tutti i laboratori dai dati attuali delle tabelle "
        "(chiude gli snapshot in corso). Da lanciare una volta a mano."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Crea lo snapshot solo per i laboratori che non ne hanno uno in corso.",
        )

    def handle(self, *args, only_missing=False, **options):
        created, errors = create_all_snapshots(only_missing=only_missing)
        self.stdout.write(self.style.SUCCESS(f"Snapshot creati: {created}"))
        for lab_id, err in errors:
            self.stderr.write(self.style.ERROR(f"Laboratorio {lab_id}: {err}"))
