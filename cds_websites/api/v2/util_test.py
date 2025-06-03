from django.test import TestCase
from regdid.models import (
    DidatticaArticoliRegolamentoStruttura,
    DidatticaArticoliRegolamentoTitolo,
    DidatticaCdsArticoliRegolamento,
    DidatticaCdsArticoliRegolamentoTestata,
    DidatticaCdsSubArticoliRegolamento,
)

from cds_websites.models import (
    SitoWebArticoliRegolamentoStrutturaTopic,
    SitoWebCdsOggettiPortale,
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTipoDato,
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliReg,
    SitoWebCdsTopicArticoliRegAltriDati,
)
from cds.models import (
    DidatticaCds,
    DidatticaAmbiti,
    DidatticaCdsTipoCorso,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSceltaVincoli,
    DidatticaPianoSche,
    DidatticaRegolamento,
    DidatticaAttivitaFormativa,
)
import datetime


class ApiCdsWebsitesUnitTestMethods(TestCase):
    @classmethod
    def create_sitoWebCdsTopic(cls, **kwargs):
        data = {
            "id": 1,
            "descr_topic_it": "Topic 1",
            "descr_topic_en": "Topic 1",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return SitoWebCdsTopic.objects.create(**data)

    @classmethod
    def create_didatticaCds(cls, **kwargs):
        data = {
            "cds_id": 1,
            "cds_cod": "1",
            "nome_cds_it": "Matematica",
            "nome_cds_eng": "Math",
            "tipo_corso_cod": "L",
        }
        data.update(kwargs)
        return DidatticaCds.objects.create(**data)

    @classmethod
    def create_dct_corso(cls, **kwargs):
        data = {
            "id": 1,
            "tipo_corso_cod": "L",
            "tipo_corso_des": "Laurea",
        }
        data.update(kwargs)
        return DidatticaCdsTipoCorso.objects.create(**data)

    @classmethod
    def create_dar_titolo(cls, **kwargs):
        data = {
            "id": 1,
            "descr_titolo_it": "TITOLO I",
            "ordine": 10,
        }
        data.update(kwargs)
        return DidatticaArticoliRegolamentoTitolo.objects.create(**data)

    @classmethod
    def create_dar_struttura(cls, **kwargs):
        data = {
            "id": 1,
            "aa": datetime.datetime.now().year,
            "numero": 1,
            "titolo_it": "Test Titolo Articolo 1",
            "titolo_en": "Test Title Article 1",
            "ordine": 10,
            "visibile": 1,
        }
        data.update(kwargs)
        return DidatticaArticoliRegolamentoStruttura.objects.create(**data)

    @classmethod
    def create_dcar_testata(cls, **kwargs):
        data = {
            "id": 1,
            "aa": datetime.datetime.now().year,
            "note": "",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return DidatticaCdsArticoliRegolamentoTestata.objects.create(**data)

    @classmethod
    def create_dca_regolamento(cls, **kwargs):
        data = {
            "id": 1,
            "testo_it": "Testo articolo IT",
            "testo_en": "Testo articolo EN",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return DidatticaCdsArticoliRegolamento.objects.create(**data)

    @classmethod
    def create_dcsa_regolamento_visbile(cls, **kwargs):
        data = {
            "id": 1,
            "titolo_it": "Titolo sub articolo",
            "titolo_en": "Title sub article",
            "testo_it": "Testo sub articolo IT",
            "testo_en": "Testo sub articolo EN",
            "ordine": 10,
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return DidatticaCdsSubArticoliRegolamento.objects.create(**data)

    @classmethod
    def create_swco_portale_data(cls, **kwargs):
        data = {
            "id": 1,
            "aa_regdid_id": datetime.datetime.now().year,
            "id_oggetto_portale": 1,
            "id_classe_oggetto_portale": "WebPath",
            "testo_it": "TESTO IT",
            "testo_en": "TESTO EN",
            "titolo_it": "TITOLO IT",
            "titolo_en": "TITOLO EN",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return SitoWebCdsOggettiPortale.objects.create(**data)

    @classmethod
    def create_swars_topic_data(cls, **kwargs):
        data = {"id": 1, "visibile": 1, "dt_mod": datetime.datetime.today()}
        data.update(kwargs)
        return SitoWebArticoliRegolamentoStrutturaTopic.objects.create(**data)

    @classmethod
    def create_WebSiteCdsTopicArticoliReg(cls, **kwargs):
        data = {
            "id": 1,
            "sito_web_cds_oggetti_portale": None,
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return SitoWebCdsTopicArticoliReg.objects.create(**data)

    @classmethod
    def create_WebSiteCdsSubArticoliRegolamento(cls, **kwargs):
        data = {
            "id": 1,
            "titolo_it": "TITOLO SUB IT",
            "titolo_en": "TITOLO SUB EN",
            "testo_it": "TESTO SUB IT",
            "testo_en": "TESTO SUB EN",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return SitoWebCdsSubArticoliRegolamento.objects.create(**data)

    @classmethod
    def create_WebSiteCdsTipoDato(cls, **kwargs):
        data = {
            "descr_breve": "TICKET",
        }
        data.update(kwargs)
        return SitoWebCdsTipoDato.objects.create(**data)

    @classmethod
    def create_WebSiteCdsTopicArticoliRegAltriDati(cls, **kwargs):
        data = {
            "id": 1,
            "ordine": 1,
            "titolo_en": "TITOLO ALTRO DATO IT",
            "titolo_it": "TITOLO ALTRO DATO EN",
            "testo_it": "TESTO ALTRO DATO IT",
            "testo_en": "TESTO ALTRO DATO EN",
            "link": "",
            "visibile": 1,
            "dt_mod": datetime.datetime.today(),
        }
        data.update(kwargs)
        return SitoWebCdsTopicArticoliRegAltriDati.objects.create(**data)

    @classmethod
    def create_didatticaRegolamento(cls, **kwargs):
        data = {
            "regdid_id": 1,
            "aa_reg_did": 2022,
            "frequenza_obbligatoria": 0,
            "titolo_congiunto_cod": "N",
            "stato_regdid_cod": "A",
            "cds_id": 1,
        }
        data.update(kwargs)
        return DidatticaRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaPianoRegolamento(cls, **kwargs):
        data = {
            "regpiani_id": 1,
            "regdid_id": 1,
            "aa_coorte_id": 2022,
            "aa_regpiani_id": 2022,
            "des": "prova",
            "def_flg": 1,
            "stato_cod": "A",
            "stato_des": "A",
            "regpiani_pdr_id": 1,
            "regpiani_pdr_cod": "test",
            "regpiani_pdr_des": "test",
            "flg_exp_seg_stu": 1,
        }
        data.update(kwargs)
        return DidatticaPianoRegolamento.objects.create(**data)

    @classmethod
    def create_didatticaPianoSche(cls, **kwargs):
        data = {
            "sche_piano_id": 1,
            "sche_piano_des": "prova",
            "sche_piano_cod": "test",
            "regpiani_id": 1,
            "pds_cod": "GEN",
            "pds_des": "Generico",
            "comune_flg": 1,
        }
        data.update(kwargs)
        return DidatticaPianoSche.objects.create(**data)

    @classmethod
    def create_didatticaPianoSceltaVincoli(cls, **kwargs):
        data = {
            "sce_id": 1,
        }
        data.update(kwargs)
        return DidatticaPianoSceltaVincoli.objects.create(**data)

    @classmethod
    def create_didatticaPianoSceltaSchePiano(cls, **kwargs):
        data = {
            "sce_id": 1,
            "sche_piano_id": 1,
            "tipo_sce_cod": "O",
            "apt_slot_ord_num": 5,
        }
        data.update(kwargs)
        return DidatticaPianoSceltaSchePiano.objects.create(**data)

    @classmethod
    def create_didatticaPianoSceltaAf(cls, **kwargs):
        data = {
            "sce_id": 1,
            "anno_corso_af": 2022,
            "ciclo_des": "Prova",
            "af_gen_des": "Prova",
            "af_id": 1,
            "tipo_af_des_af": "Contenuto",
            "ambito_des_af": "Test",
            "sett_cod": "Content",
            "peso": 6,
        }
        data.update(kwargs)
        return DidatticaPianoSceltaAf.objects.create(**data)

    @classmethod
    def create_didatticaAmbiti(cls, **kwargs):
        data = {"amb_id": 1}
        data.update(kwargs)
        return DidatticaAmbiti.objects.create(**data)

    @classmethod
    def create_didatticaAttivitaFormativa(cls, **kwargs):
        data = {
            "af_id": "1",
            "anno_corso": 1,
            "amb_id": 1,
            "af_gen_id": 1,
            "af_gen_cod": "AAA",
            "des": "Prova",
            "af_gen_des_eng": "Test",
            "sett_cod": "Sem",
            "sett_des": "Semestere",
            "peso": 6,
            "fat_part_stu_cod": "AA",
        }
        data.update(kwargs)
        return DidatticaAttivitaFormativa.objects.create(**data)
