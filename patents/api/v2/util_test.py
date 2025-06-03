from django.test import TestCase
from addressbook.models import Personale
from companies.models import TipologiaAreaTecnologica
from patents.models import BrevettoDatiBase, BrevettoInventori


class ApiPatentsUnitTestMethods(TestCase):
    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Franco",
            "cognome": "Garofalo",
            "cd_ruolo": "PO",
            "id_ab": 1,
            "matricola": "111111",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_tipologiaAreaTecnologica(cls, **kwargs):
        data = {
            "id": 1,
            "descr_area_ita": "aaa",
            "descr_area_eng": "aaa",
        }
        data.update(kwargs)
        return TipologiaAreaTecnologica.objects.create(**data)

    @classmethod
    def create_brevettoDatiBase(cls, **kwargs):
        data = {
            "id": 1,
            "id_univoco": "100010",
            "titolo": "Ingegneria del sw",
            "url_immagine": "aaaa",
            "breve_descrizione": "applicazione",
            "url_knowledge_share": "aaaa",
        }
        data.update(kwargs)
        return BrevettoDatiBase.objects.create(**data)

    @classmethod
    def create_brevettoInventori(cls, **kwargs):
        data = {
            "id": 1,
            "cognomenome_origine": "garofalo",
        }
        data.update(kwargs)
        return BrevettoInventori.objects.create(**data)
