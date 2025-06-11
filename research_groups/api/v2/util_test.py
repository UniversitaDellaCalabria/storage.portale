from django.test import TestCase
from research_groups.models import RicercaDocenteGruppo, RicercaGruppo
from research_lines.models import RicercaErc0, RicercaErc1
from addressbook.models import Personale


class ApiResearchGroupsUnitTestMethods(TestCase):
    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Simone",
            "cognome": "Mungari",
            "cd_ruolo": "PA",
            "id_ab": 1,
            "matricola": "111112",
            "fl_docente": 1,
            "ds_sede": "DIMES",
            "sede": "1111",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_ricercaErc0(cls, **kwargs):
        data = {
            "erc0_cod": "111",
            "description": "IT",
        }
        data.update(kwargs)
        return RicercaErc0.objects.create(**data)

    @classmethod
    def create_ricercaErc1(cls, **kwargs):
        data = {
            "id": 1,
            "cod_erc1": "cod1_erc1",
            "descrizione": "Computer Science and Informatics",
        }
        data.update(kwargs)
        return RicercaErc1.objects.create(**data)

    @classmethod
    def create_ricercaGruppo(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Intelligenza Artificiale",
            "descrizione": "ricerca su Machine Learning",
            "ricerca_erc1_id": 1,
        }
        data.update(kwargs)
        return RicercaGruppo.objects.create(**data)
    
    @classmethod
    def create_ricercaDocenteGruppo(cls, **kwargs):
        data = {
            "personale": None,
            "ricerca_gruppo": None,
        }
        data.update(kwargs)
        return RicercaDocenteGruppo.objects.create(**data)
