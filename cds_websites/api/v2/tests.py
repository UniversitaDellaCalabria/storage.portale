import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .util_test import ApiCdsWebsitesUnitTestMethods


class CdsWebsitesUnitTest(TestCase):
    def setUp(self):
        self.req = Client()
        
    def test_apisitiwebcdstopics(self):
        ApiCdsWebsitesUnitTestMethods.create_sitoWebCdsTopic()
        
        url = reverse("cds-websites:apiv2:studyplans-list", kwargs={"cds_cod": 123, "year": 2025})
        
        res = self.req.get(url)
        
        self.assertEqual(res.status_code, 200)
        
    def test_apisitiwebcdstopicarticles(self):
        self.uname = "user"
        self.passw = "pass"
        self.user = get_user_model().objects.create_superuser(
            username=self.uname, password=self.passw
        )

        self.current_datetime = datetime.datetime.now()
        self.current_year = self.current_datetime.year
        
        # Topics
        swc_topic_1 = ApiCdsWebsitesUnitTestMethods.create_sitoWebCdsTopic()
        swc_topic_2 = ApiCdsWebsitesUnitTestMethods.create_sitoWebCdsTopic(id=2, descr_topic_it="Topic 2", descr_topic_en="Topic 2")
        
        # Cds
        cds = ApiCdsWebsitesUnitTestMethods.create_didatticaCds()
        
        # Articles
        self.dct_corso = ApiCdsWebsitesUnitTestMethods.create_dct_corso(user_mod=self.user)
        self.dar_titolo = ApiCdsWebsitesUnitTestMethods.create_dar_titolo(user_mod=self.user)

        dar_struttura_1 = ApiCdsWebsitesUnitTestMethods.create_dar_struttura(
            didattica_cds_tipo_corso=self.dct_corso,
            didattica_articoli_regolamento_titolo=self.dar_titolo,
            dt_mod=self.current_datetime,
            user_mod=self.user
        )
        dar_struttura_2 = ApiCdsWebsitesUnitTestMethods.create_dar_struttura(
            id=2,
            numero=2,
            ordine=20,
            didattica_cds_tipo_corso=self.dct_corso,
            didattica_articoli_regolamento_titolo=self.dar_titolo,
            dt_mod=self.current_datetime,
            user_mod=self.user
        )
        dar_struttura_3 = ApiCdsWebsitesUnitTestMethods.create_dar_struttura(
            id=3,
            numero=3,
            ordine=30,
            didattica_cds_tipo_corso=self.dct_corso,
            didattica_articoli_regolamento_titolo=self.dar_titolo,
            dt_mod=self.current_datetime,
            user_mod=self.user
        )

        self.dcar_testata = ApiCdsWebsitesUnitTestMethods.create_dcar_testata(cds_id=cds.cds_id, user_mod=self.user)
        dca_regolamento_1 = ApiCdsWebsitesUnitTestMethods.create_dca_regolamento(
            didattica_cds_articoli_regolamento_testata=self.dcar_testata,
            didattica_articoli_regolamento_struttura=dar_struttura_1,
            user_mod=self.user
        )
        dca_regolamento_2 = ApiCdsWebsitesUnitTestMethods.create_dca_regolamento(
            id=2,
            didattica_cds_articoli_regolamento_testata=self.dcar_testata,
            didattica_articoli_regolamento_struttura=dar_struttura_2,
            user_mod=self.user
        )
        dca_regolamento_3 = ApiCdsWebsitesUnitTestMethods.create_dca_regolamento(
            id=3,
            didattica_cds_articoli_regolamento_testata=self.dcar_testata,
            didattica_articoli_regolamento_struttura=dar_struttura_3,
            user_mod=self.user
        )

        _dca_regolamento_list = [
            dca_regolamento_1,
            dca_regolamento_2,
            dca_regolamento_3,
        ]

        # Sub articles
        dcsa_regolamento_visbile_1 = ApiCdsWebsitesUnitTestMethods.create_dcsa_regolamento_visbile(
            didattica_cds_articoli_regolamento=dca_regolamento_1,
            user_mod=self.user)
        dcsa_regolamento_visbile_2 = ApiCdsWebsitesUnitTestMethods.create_dcsa_regolamento_visbile(
            id=2,
            didattica_cds_articoli_regolamento=dca_regolamento_1,
            user_mod=self.user)
        dcsa_regolamento_visbile_3 = ApiCdsWebsitesUnitTestMethods.create_dcsa_regolamento_visbile(
            id=3,
            didattica_cds_articoli_regolamento=dca_regolamento_2,
            user_mod=self.user)
        _dcsa_regolamento_list = [
            dcsa_regolamento_visbile_1,
            dcsa_regolamento_visbile_2,
            dcsa_regolamento_visbile_3,
        ]

        # CMS objects
        swco_portale_visibile_1 = ApiCdsWebsitesUnitTestMethods.create_swco_portale_data(
            cds_id=cds.cds_id,
            user_mod=self.user
        )
        swco_portale_visibile_2 = ApiCdsWebsitesUnitTestMethods.create_swco_portale_data(
            id=2,
            cds_id=cds.cds_id,
            user_mod=self.user
        )
        swco_portale_non_visibile_1 = ApiCdsWebsitesUnitTestMethods.create_swco_portale_data(
            id=3,
            visibile=0,
            cds_id=cds.cds_id,
            user_mod=self.user
        )
        
        _swco_portale_list = [
            swco_portale_visibile_1,
            swco_portale_visibile_2,
            swco_portale_non_visibile_1,
        ]

        # Struttura topic
        swars_topic_list = []
        idinc = 1
        for _ in range(3):
            swars_topic_list.append(
                ApiCdsWebsitesUnitTestMethods.create_swars_topic_data(
                    id=idinc,
                    sito_web_cds_topic=swc_topic_1,
                    did_art_regolamento_struttura=dar_struttura_1,
                    titolo_it=dar_struttura_1.titolo_it,
                    titolo_en=dar_struttura_1.titolo_en,
                    ordine=dar_struttura_1.ordine,
                    user_mod=self.user,
                )
            )
            idinc += 1
            
        # SitoWebCdsArticoliReg for Articles
        _swcta_reg_list = []
        for idx, swars_topic in enumerate(swars_topic_list, 0):
            _dca_regolamento = _dca_regolamento_list[idx]
            _swcta_reg_list.append(
                ApiCdsWebsitesUnitTestMethods.create_WebSiteCdsTopicArticoliReg(
                    id=idx + 1,
                    titolo_it=swars_topic.titolo_it,
                    titolo_en=swars_topic.titolo_en,
                    testo_it=_dca_regolamento.testo_it,
                    testo_en=_dca_regolamento.testo_en,
                    sito_web_cds_topic=swars_topic.sito_web_cds_topic,
                    sito_web_cds_oggetti_portale=None,
                    didattica_cds_articoli_regolamento=_dca_regolamento,
                    ordine=swars_topic.ordine,
                    visibile=1 if idx < 2 else 0,
                    dt_mod=self.current_datetime,
                    user_mod=self.user,
                )

            )
            
        # SitoWebCdsSubArticoliRegolamento
        for idx, _ in enumerate(_dcsa_regolamento_list, 0):
            _swcta_reg = _swcta_reg_list[0 if idx < 2 else idx]
            ApiCdsWebsitesUnitTestMethods.create_WebSiteCdsSubArticoliRegolamento(
                id=idx + 1,
                sito_web_cds_topic_articoli_reg=_swcta_reg,
                ordine=(idx + 1) * 10,
                visibile=1 if idx != 1 else 0,
                user_mod=self.user, 
            )
            
        # SitoWebCdsArticoliReg for Objects
        for idx, swars_topic in enumerate(swars_topic_list, 0):
            _swco_portale = _swco_portale_list[0 if idx < 2 else idx]
            _swcta_reg_list.append(
                ApiCdsWebsitesUnitTestMethods.create_WebSiteCdsTopicArticoliReg(
                    id=idx + 4,
                    titolo_it=swars_topic.titolo_it,
                    titolo_en=swars_topic.titolo_en,
                    testo_it=_swco_portale.testo_it,
                    testo_en=_swco_portale.testo_en,
                    sito_web_cds_topic=swars_topic.sito_web_cds_topic,
                    sito_web_cds_oggetti_portale=_swco_portale,
                    didattica_cds_articoli_regolamento=None,
                    ordine=swars_topic.ordine,
                    user_mod=self.user,
                )
            )
            
        # SitoWebCdsTopicArticoliRegAltriDati
        swct_dato = ApiCdsWebsitesUnitTestMethods.create_WebSiteCdsTipoDato()
        
        for idx, swcta_reg in enumerate(_swcta_reg_list, 0):
            if swcta_reg.pk not in [1, 3, 4]:
                continue
            ApiCdsWebsitesUnitTestMethods.create_WebSiteCdsTopicArticoliRegAltriDati(
                id=idx + 1,
                sito_web_cds_topic_articoli_reg=swcta_reg,
                sito_web_cds_tipo_dato=swct_dato,
                user_mod=self.user, 
            )
        
        self.num_swcta_reg = len(_swcta_reg_list)
        self.num_swcta_reg_visibili = self.num_swcta_reg - 1
        
        url = reverse("cds-websites:apiv2:topic-articles-list", kwargs={"cds_cod":"1", "topic_id": 1})
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), self.num_swcta_reg_visibili)
        
        for result in res.json()["results"]:
            self.assertEqual(len(result["subArticles"]), 1) if result["id"] == 1 else self.assertEqual(len(result["subArticles"]), 0)
            if result["id"] >= 4:
                self.assertEqual(result["type"], "Object") 

            # self.assertIsNot(result["otherData"], []) if result["id"] in [1, 3, 4] else self.assertIs(result["otherData"], []) 
            self.assertIsNot(result["visibile"], [])
            
    def test_apisitiwebcdsstudyplans(self):
        ApiCdsWebsitesUnitTestMethods.create_didatticaCds(
            nome_cds_it="informatica",
            nome_cds_eng="computer science",
            tipo_corso_cod="L",
            cla_miur_cod="1",
            cla_miur_des="laurea in informatica",
            durata_anni=3,
            valore_min=180,
            cdsord_id=1,
            area_cds="scienze",
            cds_id=1,
            cds_cod="1",
        )        
        
        ApiCdsWebsitesUnitTestMethods.create_didatticaRegolamento()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoRegolamento()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSche()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSche(
            sche_piano_id=2,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSche(
            sche_piano_id=3,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaVincoli()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaVincoli(
            sce_id=2,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaVincoli(
            sce_id=3,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaSchePiano()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaAf()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaAf(
            sce_id=2,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaAf(
            sce_id=3,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaAmbiti()
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaSchePiano(
            sce_id=2,
            sche_piano_id=2,
            amb_id=1,
            ambito_des="Prova",
            min_unt=1,
            max_unt=2,
            sce_des="Content",
            apt_slot_ord_num=1,
            tipo_sce_cod="Pr",
            tipo_sce_des="Prova",
            tipo_regsce_cod="P",
            tipo_regsce_des="Prova",
            tipo_um_regsce_cod="P",
            vin_sce_des=1,
            vin_id=1,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaPianoSceltaSchePiano(
            sce_id=3,
            sche_piano_id=3,
            ambito_des="Prova",
            min_unt=1,
            max_unt=2,
            sce_des="Content",
            apt_slot_ord_num=1,
            tipo_sce_cod="Pr",
            tipo_sce_des="Prova",
            tipo_regsce_cod="P",
            tipo_regsce_des="Prova",
            tipo_um_regsce_cod="P",
            amb_id_af_regsce=1,
        )
        
        ApiCdsWebsitesUnitTestMethods.create_didatticaAttivitaFormativa()
        ApiCdsWebsitesUnitTestMethods.create_didatticaAttivitaFormativa(
            af_id=2,
            amb_id=2,
            af_gen_id=2,
        )
        ApiCdsWebsitesUnitTestMethods.create_didatticaAttivitaFormativa(
            af_id=3,
            amb_id=3,
            af_gen_id=3,
        )
        
        url = reverse("cds-websites:apiv2:studyplans-list", kwargs={"cds_cod": "1", "year": 2022})
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        