from django.test import TestCase
from structures.models import ComuniAll, DidatticaDipartimento, TerritorioIt


class DidatticaDipartimentoUnitTest(TestCase):
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": "1",
            "dip_des_it": "matematica e informatica",
            "dip_des_eng": "math and computer science",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDipartimento.objects.create(**data)
        return obj


class ComuniAllUnitTest(TestCase):
    @classmethod
    def create_comuniAll(cls, **kwargs):
        data = {
            "id_comune": 1,
            "ds_comune": "comune 1",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = ComuniAll.objects.create(**data)
        return obj


class TerritorioItUnitTest(TestCase):
    @classmethod
    def create_territorioIt(cls, **kwargs):
        data = {
            "cd_istat": "1",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = TerritorioIt.objects.create(**data)
        return obj
