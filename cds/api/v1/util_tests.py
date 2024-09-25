from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsLingua,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaTestiRegolamento,
)
from django.test import TestCase


class DidatticaCdsUnitTest(TestCase):
    @classmethod
    def create_didatticaCds(cls, **kwargs):
        data = {
            "cds_id": 1,
            "nome_cds_it": "informatica",
            "nome_cds_eng": "computer science",
            "tipo_corso_cod": "1",
            "cla_miur_cod": "1",
            "cla_miur_des": "laurea in informatica",
            "durata_anni": 3,
            "valore_min": 180,
            "cdsord_id": 1,
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCds.objects.create(**data)
        return obj


class DidatticaCdsLinguaUnitTest(TestCase):
    @classmethod
    def create_didatticaCdsLingua(cls, **kwargs):
        data = {
            "lin_did_ord_id": 1,
            "lingua_des_it": "ITALIANO",
            "lingua_des_eng": "ITALIAN",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsLingua.objects.create(**data)
        return obj


class DidatticaRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaRegolamento(cls, **kwargs):
        data = {
            "regdid_id": 1,
            "aa_reg_did": 2020,
            "frequenza_obbligatoria": 0,
            "titolo_congiunto_cod": "N",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaRegolamento.objects.create(**data)
        return obj


class DidatticaTestiRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaTestiRegolamento(cls, **kwargs):
        data = {
            "txt_id": 1,
            "tipo_testo_regdid_cod": "testo regolamento",
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaTestiRegolamento.objects.create(**data)
        return obj


class DidatticaAttivitaFormativaUnitTest(TestCase):
    @classmethod
    def create_didatticaAttivitaFormativa(cls, **kwargs):
        data = {"af_id": "1", "anno_corso": 1}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaAttivitaFormativa.objects.create(**data)
        return obj


class DidatticaPdsRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaPdsRegolamento(cls, **kwargs):
        data = {
            # 'aa_ord_id': 1,
            "pds_regdid_id": 1,
        }

        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPdsRegolamento.objects.create(**data)
        return obj
