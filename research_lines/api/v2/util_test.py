from django.test import TestCase
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaErc2,
    RicercaLineaApplicata,
    RicercaLineaBase,
)


class ApiResearchLinesUnitTestMethods(TestCase):
    @classmethod
    def create_ricercaErc2(cls, **kwargs):
        data = {
            "cod_erc2": "cod1_erc2",
            "descrizione": "Machine learning",
            "ricerca_erc1": None,
        }
        data.update(kwargs)
        return RicercaErc2.objects.create(**data)

    @classmethod
    def create_ricercaLineaBase(cls, **kwargs):
        data = {
            "id": 1,
            "descrizione": "regressione lineare",
            "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
            "anno": "2016",
            "visibile": 1,
        }
        data.update(kwargs)
        return RicercaLineaBase.objects.create(**data)

    @classmethod
    def create_ricercaDocenteLineaBase(cls, **kwargs):
        data = {
            "personale": None,
            "ricerca_linea_base": None,
        }
        data.update(kwargs)
        return RicercaDocenteLineaBase.objects.create(**data)

    @classmethod
    def create_ricercaAster1(cls, **kwargs):
        data = {
            "id": 1,
            "descrizione": "ICT & Design",
        }
        data.update(kwargs)
        return RicercaAster1.objects.create(**data)

    @classmethod
    def create_ricercaAster2(cls, **kwargs):
        data = {
            "id": 2,
            "descrizione": "Algorithms. Data and signal processing",
        }
        data.update(kwargs)
        return RicercaAster2.objects.create(**data)

    @classmethod
    def create_ricercaLineaApplicata(cls, **kwargs):
        data = {
            "id": 1,
            "descrizione": "regressione lineare",
            "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
            "anno": "2016",
            "visibile": 1,
        }
        data.update(kwargs)
        return RicercaLineaApplicata.objects.create(**data)

    @classmethod
    def create_ricercaDocenteLineaApplicata(cls, **kwargs):
        data = {
            "dt_ins": "2021-01-03 15:47:21",
        }
        data.update(kwargs)
        return RicercaDocenteLineaApplicata.objects.create(**data)
