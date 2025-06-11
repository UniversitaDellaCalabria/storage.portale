from django.test import TestCase
from phd.models import (
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaAltriDocenti,
    DidatticaDottoratoAttivitaFormativaDocente,
    DidatticaDottoratoCds,
    DidatticaDottoratoPds,
    DidatticaDottoratoRegolamento,
    DidatticaDottoratoAttivitaFormativaTipologia
)
from addressbook.models import Personale
from structures.models import DidatticaDipartimento


class ApiPhdUnitTestMethods(TestCase):
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": "1",
            "dip_des_it": "matematica e informatica",
            "dip_des_eng": "math and computer science",
        }
        data.update(kwargs)
        return DidatticaDipartimento.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoCds(cls, **kwargs):
        data = {
            "cds_id_esse3": 1,
            "cds_cod": "111",
            "aa_ord_id": 1,
        }
        data.update(kwargs)
        return DidatticaDottoratoCds.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoPds(cls, **kwargs):
        data = {
            "pds_cod": "GEN",
        }
        data.update(kwargs)
        return DidatticaDottoratoPds.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoRegolamento(cls, **kwargs):
        data = {
            "regdid_id_esse3": 1,
            "aa_regdid_id": 2020,
            "num_ciclo": 10,
        }
        data.update(kwargs)
        return DidatticaDottoratoRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoAttivitaFormativa(cls, **kwargs):
        data = {
            "id": 1,
            "nome_af": "AAAA",
            "struttura_proponente_origine": "dimes",
            "rif_dottorato": "matematica",
            "ciclo": 1,
        }
        data.update(kwargs)
        return DidatticaDottoratoAttivitaFormativa.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoAttivitaFormativaDocente(cls, **kwargs):
        data = {
            "cognome_nome_origine": "Simone",
        }
        data.update(kwargs)
        return DidatticaDottoratoAttivitaFormativaDocente.objects.create(**data)

    @classmethod
    def create_didatticaDottoratoAttivitaFormativaAltriDocenti(cls, **kwargs):
        data = {
            "cognome_nome_origine": "Carmine",
        }
        data.update(kwargs)
        return DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(**data)
    
    @classmethod
    def create_didatticaDottoratoAttivitaFormativaTipologia(cls, **kwargs):
        data = {
            "nome_it": "Didattica",
            "nome_en": "Didactic"
        }
        data.update(kwargs)
        return DidatticaDottoratoAttivitaFormativaTipologia.objects.create(**data)
    
    
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