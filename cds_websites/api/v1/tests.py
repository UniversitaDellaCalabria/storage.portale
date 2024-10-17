import datetime

from cds.api.v1.util_tests import (
    DidatticaAttivitaFormativaUnitTest,
    DidatticaCdsUnitTest,
    DidatticaRegolamentoUnitTest,
)
from cds.models import (
    DidatticaAmbiti,
    DidatticaCdsTipoCorso,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSceltaVincoli,
    DidatticaPianoSche,
)
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
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


class ApiSitoWebCdsTopicListUnitTest(TestCase):
    def test_apisitiwebcdstopics(self):
        req = Client()

        SitoWebCdsTopic.objects.create(
            **{
                "id": 1,
                "descr_topic_it": "prova",
                "descr_topic_en": "test",
                "visibile": 0,
                "dt_mod": datetime.datetime.today(),
            }
        )

        url = reverse("cds-websites:apiv1:cds-websites-topic-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiSitoWebCdsTopicArticlesListUnitTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.uname = "user"
        self.passw = "pass"
        self.user = get_user_model().objects.create_superuser(
            username=self.uname, password=self.passw
        )

        self.current_datetime = datetime.datetime.now()
        self.current_year = self.current_datetime.year

        _swc_topic_data = {
            "id": 1,
            "descr_topic_it": "Topic 1",
            "descr_topic_en": "Topic 1",
            "visibile": 1,
            "dt_mod": self.current_datetime,
        }

        # Topics
        self.swc_topic_1 = SitoWebCdsTopic.objects.create(**_swc_topic_data)

        _swc_topic_data["id"] += 1
        _swc_topic_data["descr_topic_it"] = "Topic 2"
        _swc_topic_data["descr_topic_en"] = "Topic 2"
        self.swc_topic_2 = SitoWebCdsTopic.objects.create(**_swc_topic_data)

        # Cds
        self.cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "cds_id": 1,
                "cds_cod": "1",
                "nome_cds_it": "Matematica",
                "nome_cds_eng": "Math",
                "tipo_corso_cod": "L",
            }
        )

        # Articles
        self.dct_corso = DidatticaCdsTipoCorso.objects.create(
            **{
                "id": 1,
                "tipo_corso_cod": "L",
                "tipo_corso_des": "Laurea",
                "user_mod": self.user,
            }
        )

        self.dar_titolo = DidatticaArticoliRegolamentoTitolo.objects.create(
            **{
                "id": 1,
                "descr_titolo_it": "TITOLO I",
                "ordine": 10,
                "id_user_mod": self.user,
            }
        )

        _dar_struttura_data = {
            "id": 1,
            "aa": self.current_year,
            "numero": 1,
            "titolo_it": "Test Titolo Articolo 1",
            "titolo_en": "Test Title Article 1",
            "ordine": 10,
            "visibile": 1,
            "id_didattica_cds_tipo_corso": self.dct_corso,
            "id_didattica_articoli_regolamento_titolo": self.dar_titolo,
            "dt_mod": self.current_datetime,
            "id_user_mod": self.user,
        }

        self.dar_struttura_1 = DidatticaArticoliRegolamentoStruttura.objects.create(
            **_dar_struttura_data
        )

        _dar_struttura_data["id"] += 1
        _dar_struttura_data["numero"] += 1
        _dar_struttura_data["ordine"] += 10
        self.dar_struttura_2 = DidatticaArticoliRegolamentoStruttura.objects.create(
            **_dar_struttura_data
        )

        _dar_struttura_data["id"] += 1
        _dar_struttura_data["numero"] += 1
        _dar_struttura_data["ordine"] += 10
        self.dar_struttura_3 = DidatticaArticoliRegolamentoStruttura.objects.create(
            **_dar_struttura_data
        )

        self.dcar_testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            **{
                "id": 1,
                "cds_id": self.cds.cds_id,
                "aa": self.current_year,
                "note": "",
                "visibile": 1,
                "dt_mod": self.current_datetime,
                "id_user_mod": self.user,
            }
        )

        _dca_regolamento_data = {
            "id": 1,
            "id_didattica_cds_articoli_regolamento_testata": self.dcar_testata,
            "id_didattica_articoli_regolamento_struttura": self.dar_struttura_1,
            "testo_it": "Testo articolo IT",
            "testo_en": "Testo articolo EN",
            "visibile": 1,
            "dt_mod": self.current_datetime,
            "id_user_mod": self.user,
        }

        self.dca_regolamento_1 = DidatticaCdsArticoliRegolamento.objects.create(
            **_dca_regolamento_data
        )

        _dca_regolamento_data["id"] += 1
        _dca_regolamento_data["id_didattica_articoli_regolamento_struttura"] = (
            self.dar_struttura_2
        )
        self.dca_regolamento_2 = DidatticaCdsArticoliRegolamento.objects.create(
            **_dca_regolamento_data
        )

        _dca_regolamento_data["id"] += 1
        _dca_regolamento_data["id_didattica_articoli_regolamento_struttura"] = (
            self.dar_struttura_3
        )
        self.dca_regolamento_3 = DidatticaCdsArticoliRegolamento.objects.create(
            **_dca_regolamento_data
        )

        _dca_regolamento_list = [
            self.dca_regolamento_1,
            self.dca_regolamento_2,
            self.dca_regolamento_3,
        ]

        # Sub articles
        _dcsa_regolamento_data = {
            "id": 1,
            "id_didattica_cds_articoli_regolamento": self.dca_regolamento_1,
            "titolo_it": "Titolo sub articolo",
            "titolo_en": "Title sub article",
            "testo_it": "Testo sub articolo IT",
            "testo_en": "Testo sub articolo EN",
            "ordine": 10,
            "visibile": 1,
            "dt_mod": self.current_datetime,
            "id_user_mod": self.user,
        }

        self.dcsa_regolamento_visbile_1 = (
            DidatticaCdsSubArticoliRegolamento.objects.create(**_dcsa_regolamento_data)
        )

        _dcsa_regolamento_data["id"] += 1
        self.dcsa_regolamento_visbile_2 = (
            DidatticaCdsSubArticoliRegolamento.objects.create(**_dcsa_regolamento_data)
        )

        _dcsa_regolamento_data["id"] += 1
        _dcsa_regolamento_data["id_didattica_cds_articoli_regolamento"] = (
            self.dca_regolamento_3
        )
        self.dcsa_regolamento_visbile_3 = (
            DidatticaCdsSubArticoliRegolamento.objects.create(**_dcsa_regolamento_data)
        )

        _dcsa_regolamento_list = [
            self.dcsa_regolamento_visbile_1,
            self.dcsa_regolamento_visbile_2,
            self.dcsa_regolamento_visbile_3,
        ]

        # CMS objects
        _swco_portale_data = {
            "id": 1,
            "cds_id": self.cds.cds_id,
            "aa_regdid_id": self.current_year,
            "id_oggetto_portale": 1,
            "id_classe_oggetto_portale": "WebPath",
            "testo_it": "TESTO IT",
            "testo_en": "TESTO EN",
            "titolo_it": "TITOLO IT",
            "titolo_en": "TITOLO EN",
            "visibile": 1,
            "dt_mod": self.current_datetime,
            "id_user_mod": self.user,
        }

        self.swco_portale_visibile_1 = SitoWebCdsOggettiPortale.objects.create(
            **_swco_portale_data
        )

        _swco_portale_data["id"] += 1
        self.swco_portale_visibile_2 = SitoWebCdsOggettiPortale.objects.create(
            **_swco_portale_data
        )

        _swco_portale_data["id"] += 1
        _swco_portale_data["visibile"] = 0
        self.swco_portale_non_visibile_1 = SitoWebCdsOggettiPortale.objects.create(
            **_swco_portale_data
        )

        _swco_portale_list = [
            self.swco_portale_visibile_1,
            self.swco_portale_visibile_2,
            self.swco_portale_non_visibile_1,
        ]

        # Struttura topic
        _swars_topic_data = {
            "id": 1,
            "id_sito_web_cds_topic": self.swc_topic_1,
            "id_did_art_regolamento_struttura": self.dar_struttura_1,
            "titolo_it": self.dar_struttura_1.titolo_it,
            "titolo_en": self.dar_struttura_1.titolo_en,
            "ordine": self.dar_struttura_1.ordine,
            "visibile": 1,
            "dt_mod": self.current_datetime,
            "id_user_mod": self.user,
        }

        _swars_topic_list = []
        for _ in range(3):
            _swars_topic_list.append(
                SitoWebArticoliRegolamentoStrutturaTopic.objects.create(
                    **_swars_topic_data
                )
            )
            _swars_topic_data["id"] += 1

        self._swcta_reg_list = []

        # SitoWebCdsArticoliReg for Articles
        for idx, swars_topic in enumerate(_swars_topic_list, 0):
            _dca_regolamento = _dca_regolamento_list[idx]
            self._swcta_reg_list.append(
                SitoWebCdsTopicArticoliReg.objects.create(
                    **{
                        "id": idx + 1,
                        "titolo_it": swars_topic.titolo_it,
                        "titolo_en": swars_topic.titolo_en,
                        "testo_it": _dca_regolamento.testo_it,
                        "testo_en": _dca_regolamento.testo_en,
                        "id_sito_web_cds_topic": swars_topic.id_sito_web_cds_topic,
                        "id_sito_web_cds_oggetti_portale": None,
                        "id_didattica_cds_articoli_regolamento": _dca_regolamento,
                        "ordine": swars_topic.ordine,
                        "visibile": 1 if idx < 2 else 0,
                        "dt_mod": self.current_datetime,
                        "id_user_mod": self.user,
                    }
                )
            )

        # SitoWebCdsSubArticoliRegolamento
        for idx, _ in enumerate(_dcsa_regolamento_list, 0):
            _swcta_reg = self._swcta_reg_list[0 if idx < 2 else idx]
            SitoWebCdsSubArticoliRegolamento.objects.create(
                **{
                    "id": idx + 1,
                    "id_sito_web_cds_topic_articoli_reg": _swcta_reg,
                    "titolo_it": "TITOLO SUB IT",
                    "titolo_en": "TITOLO SUB EN",
                    "testo_it": "TESTO SUB IT",
                    "testo_en": "TESTO SUB EN",
                    "ordine": (idx + 1) * 10,
                    "visibile": 1 if idx != 1 else 0,
                    "dt_mod": self.current_datetime,
                    "id_user_mod": self.user,
                }
            )

        # SitoWebCdsArticoliReg for Objects
        for idx, swars_topic in enumerate(_swars_topic_list, 0):
            _swco_portale = _swco_portale_list[0 if idx < 2 else idx]
            self._swcta_reg_list.append(
                SitoWebCdsTopicArticoliReg.objects.create(
                    **{
                        "id": idx + 4,
                        "titolo_it": swars_topic.titolo_it,
                        "titolo_en": swars_topic.titolo_en,
                        "testo_it": _swco_portale.testo_it,
                        "testo_en": _swco_portale.testo_en,
                        "id_sito_web_cds_topic": swars_topic.id_sito_web_cds_topic,
                        "id_sito_web_cds_oggetti_portale": _swco_portale,
                        "id_didattica_cds_articoli_regolamento": None,
                        "ordine": swars_topic.ordine,
                        "visibile": 1,
                        "dt_mod": self.current_datetime,
                        "id_user_mod": self.user,
                    }
                )
            )

        # SitoWebCdsTopicArticoliRegAltriDati
        self.swct_dato = SitoWebCdsTipoDato.objects.create(descr_breve="TICKET")

        for idx, swcta_reg in enumerate(self._swcta_reg_list, 0):
            if swcta_reg.pk not in [1, 3, 4]:
                continue
            SitoWebCdsTopicArticoliRegAltriDati.objects.create(
                **{
                    "id": idx + 1,
                    "id_sito_web_cds_topic_articoli_reg": swcta_reg,
                    "ordine": 1,
                    "id_sito_web_cds_tipo_dato": self.swct_dato,
                    "titolo_en": "TITOLO ALTRO DATO IT",
                    "titolo_it": "TITOLO ALTRO DATO EN",
                    "testo_it": "TESTO ALTRO DATO IT",
                    "testo_en": "TESTO ALTRO DATO EN",
                    "link": "",
                    "visibile": 1,
                    "dt_mod": self.current_datetime,
                    "id_user_mod": self.user,
                }
            )

        self.num_swcta_reg = len(self._swcta_reg_list)
        self.num_swcta_reg_visibili = self.num_swcta_reg - 1

    def test_apisitiwebcdstopicarticles(self):
        url = reverse("cds-websites:apiv1:cds-websites-topic-articles-list")

        # Call without parameters
        res = self.client.get(url)
        assert res.status_code == 200
        assert len(res.json()["results"]) == 0

        # Call with parameters
        data = {"cds_cod": "1", "topic_id": 1}
        res = self.client.get(url, data=data)

        assert res.status_code == 200

        # Number of returned items
        assert len(res.json()["results"]) == self.num_swcta_reg_visibili

        for result in res.json()["results"]:
            if result["ID"] == 1:
                assert len(result["SubArticles"]) == 1
            else:
                assert len(result["SubArticles"]) == 0

            if result["ID"] >= 4:
                assert result["Type"] == "Object"

            if result["ID"] in [1, 3, 4]:
                assert result["OtherData"]
            else:
                assert not result["OtherData"]

            assert result["Visible"]


class ApiSitoWebCdsStudyPlansListUnitTest(TestCase):
    def test_apisitiwebcdsstudyplans(self):
        req = Client()

        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "tipo_corso_cod": "L",
                "area_cds": "scienze",
                "cds_id": 1,
                "cds_cod": "1",
            }
        )

        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 1,
                "stato_regdid_cod": "A",
                "titolo_congiunto_cod": "N",
                "cds_id": 1,
                "aa_reg_did": 2022,
            }
        )

        DidatticaPianoRegolamento.objects.create(
            **{
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
        )

        DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 1,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )

        DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 2,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )

        DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 3,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )
        DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 1,
            }
        )
        DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 2,
            }
        )
        DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 3,
            }
        )
        DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 1,
                "sche_piano_id": 1,
                "tipo_sce_cod": "O",
                "apt_slot_ord_num": 5,
            }
        )

        DidatticaPianoSceltaAf.objects.create(
            **{
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
        )

        DidatticaPianoSceltaAf.objects.create(
            **{
                "sce_id": 2,
                "anno_corso_af": 2022,
                "ciclo_des": "Prova",
                "af_gen_des": "Prova",
                "af_id": 1,
                "tipo_af_des_af": "Contenuto",
                "ambito_des_af": "Test",
                "sett_cod": "Content",
                "peso": 6,
            }
        )

        DidatticaPianoSceltaAf.objects.create(
            **{
                "sce_id": 3,
                "anno_corso_af": 2022,
                "ciclo_des": "Prova",
                "af_gen_des": "Prova",
                "af_id": 2,
                "tipo_af_des_af": "Contenuto",
                "ambito_des_af": "Test",
                "sett_cod": "Content",
                "peso": 6,
            }
        )

        DidatticaAmbiti.objects.create(**{"amb_id": 1})

        DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 2,
                "sche_piano_id": 2,
                "amb_id": 1,
                "ambito_des": "Prova",
                "min_unt": 1,
                "max_unt": 2,
                "sce_des": "Content",
                "apt_slot_ord_num": 1,
                "tipo_sce_cod": "Pr",
                "tipo_sce_des": "Prova",
                "tipo_regsce_cod": "P",
                "tipo_regsce_des": "Prova",
                "tipo_um_regsce_cod": "P",
                "vin_sce_des": 1,
                "vin_id": 1,
            }
        )

        DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 3,
                "sche_piano_id": 3,
                "ambito_des": "Prova",
                "min_unt": 1,
                "max_unt": 2,
                "sce_des": "Content",
                "apt_slot_ord_num": 1,
                "tipo_sce_cod": "Pr",
                "tipo_sce_des": "Prova",
                "tipo_regsce_cod": "P",
                "tipo_regsce_des": "Prova",
                "tipo_um_regsce_cod": "P",
                "amb_id_af_regsce": 1,
            }
        )

        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "amb_id": 1,
                "af_gen_id": 1,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "amb_id": 2,
                "af_gen_id": 2,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 3,
                "amb_id": 3,
                "af_gen_id": 3,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        url = reverse("cds-websites:apiv1:cds-websites-studyplans-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 0

        data = {"cds_cod": "1", "year": 2022}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1
