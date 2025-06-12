import datetime
from django.test import TestCase
from structures.models import DidatticaDipartimento
from phd.models import DidatticaDottoratoAttivitaFormativa
from projects.models import ProgettoAmbitoTerritoriale
from structures.models import (
    UnitaOrganizzativa,
    UnitaOrganizzativaContatti,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaTipoFunzioni,
)
from addressbook.models import Personale, PersonaleUoTipoContatto


class ApiStructuresUnitTestMethods(TestCase):
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": "001",
            "dip_des_it": "Dipartimento di Matematica e Informatica",
            "dip_des_eng": "Department of Math and Computer Science",
            "dip_nome_breve": "DEMACS",
        }
        data.update(kwargs)
        return DidatticaDipartimento.objects.create(**data)

    @classmethod
    def create_unitaOrganizzativa(cls, **kwargs):
        data = {
            "uo": "1",
            "ds_tipo_nodo": "rettorato",
            "cd_tipo_nodo": "RET",
            "denominazione": "RETTORATO",
            "uo_padre": "1",
            "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
        }
        data.update(kwargs)
        return UnitaOrganizzativa.objects.create(**data)

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
    def create_progettoAmbitoTerritoriale(cls, **kwargs):
        data = {
            "id": 1,
            "ambito_territoriale": "aaa",
        }
        data.update(kwargs)
        return ProgettoAmbitoTerritoriale.objects.create(**data)

    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Simone",
            "cognome": "Mungari",
            "cd_ruolo": "PA",
            "ds_ruolo_locale": "Professore Associato",
            "id_ab": 1,
            "matricola": "111112",
            "fl_docente": 1,
            "flg_cessato": 0,
            "cod_fis": "SMN1",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_personaleUoTipoContatto(cls, **kwargs):
        data = {
            "cod_contatto": "PEC",
            "descr_contatto": "Posta Elettronica Certificata",
        }
        data.update(kwargs)
        return PersonaleUoTipoContatto.objects.create(**data)

    @classmethod
    def create_unitaOrganizzativaContatti(cls, **kwargs):
        data = {
            "prg_priorita": 1,
        }
        data.update(kwargs)
        return UnitaOrganizzativaContatti.objects.create(**data)

    @classmethod
    def create_unitaOrganizzativaFunzioni(cls, **kwargs):
        data = {
            "id_ab": 1,
            "ds_funzione": "Amministrazione",
            "termine": "2999-12-1",
        }
        data.update(kwargs)
        return UnitaOrganizzativaFunzioni.objects.create(**data)

    @classmethod
    def create_unitaOrganizzativaTipoFunzioni(cls, **kwargs):
        data = {
            "cd_tipo_nod": "apl",
            "funzione": "nbb45",
            "descr_funzione": "aaa",
        }
        data.update(kwargs)
        return UnitaOrganizzativaTipoFunzioni.objects.create(**data)
