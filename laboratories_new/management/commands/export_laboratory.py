from django.core.management.base import BaseCommand
from laboratories_new.export import laboratory_full_json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("lab_id", type=int)

    def handle(self, *args, **opts):
        self.stdout.write(laboratory_full_json(opts["lab_id"]))