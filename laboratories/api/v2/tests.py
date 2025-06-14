from django.test import TestCase, Client
from django.urls import reverse
from generics.utils import encrypt
from .util_test import ApiLaboratoriesUnitTestMethods


class LaboratoriesUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def assert_equal_with_data(self, url, campo, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(res.json()["results"][0][campo], result)

    def test_apilaboratorieslist(self):
        dip1 = ApiLaboratoriesUnitTestMethods.create_didatticaDipartimento()
        dip2 = ApiLaboratoriesUnitTestMethods.create_didatticaDipartimento(
            dip_id=2,
            dip_cod="2",
            dip_des_it="Lettere e filosofia",
            dip_des_eng="Philosophy",
        )
        p1 = ApiLaboratoriesUnitTestMethods.create_personale()
        p2 = ApiLaboratoriesUnitTestMethods.create_personale(
            id=2,
            nome="Carmine",
            cognome="Carlucci",
            id_ab=2,
            matricola="111112",
        )
        lab2 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            dipartimento_riferimento=dip1,
            matricola_responsabile_scientifico=p1,
        )
        a1 = ApiLaboratoriesUnitTestMethods.create_laboratorioTipologiaAttivita(
            id=2,
            descrizione="ricerca",
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioAttivita(
            id=2,
            laboratorio_dati_base=lab2,
            tipologia_attivita=a1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=2,
            ambito="Scientifico",
            dipartimento_riferimento=dip2,
            sede_dimensione="291",
            responsabile_scientifico="Carlucci Carmine",
            matricola_responsabile_scientifico=p2,
        )
        erc0 = ApiLaboratoriesUnitTestMethods.create_ricercaErc0()
        erc1_1 = ApiLaboratoriesUnitTestMethods.create_ricercaErc1(
            ricerca_erc0_cod=erc0
        )
        i1 = ApiLaboratoriesUnitTestMethods.create_laboratorioInfrastruttura()
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleRicerca(
            laboratorio_dati_base=lab2,
            matricola_personale_ricerca=p2,
        )
        lab1 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=3,
            matricola_referente_compilazione=p1,
            nome_laboratorio="LAB2",
            dipartimento_riferimento=dip2,
            ambito="Tecnologico",
            matricola_responsabile_scientifico=p2,
            infrastruttura_riferimento=i1,
        )
        a1 = ApiLaboratoriesUnitTestMethods.create_laboratorioTipologiaAttivita()
        ApiLaboratoriesUnitTestMethods.create_laboratorioAttivita(
            laboratorio_dati_base=lab1,
            tipologia_attivita=a1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleTecnico(
            laboratorio_dati_base=lab1,
            matricola_personale_tecnico=p1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(
            id=3, laboratorio_dati_base=lab1, ricerca_erc1=erc1_1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioAltriDipartimenti(
            laboratorio_dati_base=lab2,
            didattica_dipartimento=dip1,
        )

        url = reverse("laboratories:apiv2:laboratories-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)

        self.assert_equal_with_data(
            url, "id", {"department": "1", "teacher": encrypt("111111")}, 1
        )
        self.assert_equal_with_data(
            url,
            "scientificDirector",
            {"department": "1", "teacher": encrypt("111111")},
            "Mungari Simone",
        )

        self.assert_equal_with_data(
            url, "id", {"department": "1", "teacher": encrypt("111111")}, 1
        )
        self.assert_equal_with_data(
            url,
            "scientificDirector",
            {"department": "1", "teacher": encrypt("111111")},
            "Mungari Simone",
        )

        self.assert_data_len(url, {"teacher": encrypt("111111")}, 2)
        # self.assert_data_len(url, {"scope": "1"}, 1)
        self.assert_data_len(url, {"teacher": encrypt("111112")}, 3)
        self.assert_data_len(url, {"teacher": encrypt("111112"), "scope": "1"}, 1)
        self.assert_data_len(url, {"teacher": encrypt("111111"), "scope": "1"}, 1)

        self.assert_equal_with_data(url, "id", {"area": "Tecnico"}, 1)
        self.assert_equal_with_data(url, "dimension", {"area": "Tecnico"}, "290")

        self.assert_data_len(url, {"infrastructure": 1}, 1)

        self.assert_equal_with_data(
            url, "id", {"search": "Informatica", "lang": "it"}, 1
        )
        self.assert_equal_with_data(
            url, "dimension", {"search": "Informatica", "lang": "it"}, "290"
        )
        self.assert_equal_with_data(
            url,
            "scientificDirector",
            {"search": "Informatica", "lang": "it"},
            "Mungari Simone",
        )

        self.assert_equal_with_data(url, "id", {"search": "Informatica"}, 1)
        self.assert_equal_with_data(url, "dimension", {"search": "Informatica"}, "290")
        self.assert_equal_with_data(
            url, "scientificDirector", {"search": "Informatica"}, "Mungari Simone"
        )

        self.assert_equal_with_data(url, "id", {"erc1": "cod1_erc1"}, 3)

        self.assert_data_len(url, {}, 3)

        self.assert_equal_with_data(url, "id", {"area": "Scientifico"}, 1)
        self.assert_equal_with_data(url, "dimension", {"area": "Scientifico"}, "290")
        self.assert_equal_with_data(
            url, "id", {"department": "2", "area": "Scientifico"}, 1
        )
        self.assert_equal_with_data(
            url,
            "scientificDirector",
            {"department": "2", "area": "Scientifico"},
            "Mungari Simone",
        )

    def test_apilaboratoriesscopeslist(self):
        ApiLaboratoriesUnitTestMethods.create_laboratorioTipologiaAttivita(
            id=1, descrizione="Ricerca"
        )
        url = reverse("laboratories:apiv2:laboratories-scopes-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiinfrastrucureslist(self):
        ApiLaboratoriesUnitTestMethods.create_laboratorioInfrastruttura()
        url = reverse("laboratories:apiv2:infrastructures-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiLaboratoriesAreasList(self):
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=5,
            nome_laboratorio="LAB1",
            ambito="Tecnologico",
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=6,
            nome_laboratorio="LAB2",
            ambito="Scientifico",
        )
        url = reverse("laboratories:apiv2:laboratories-areas-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 2)
    
    def test_apilaboratorydetail(self):
        u1 = ApiLaboratoriesUnitTestMethods.create_unitaOrganizzativa()
        u2 = ApiLaboratoriesUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
            id_ab=2,
            denominazione="bbb",
            denominazione_padre="d",
            uo_padre="22",
        )
        p1 = ApiLaboratoriesUnitTestMethods.create_personale(
            cd_ruolo="PA = api",
            ds_ruolo_locale="Professore Associato",
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            cod_fis="SMN1",
        )
        p2 = ApiLaboratoriesUnitTestMethods.create_personale(
            id=2,
            nome="Lionel",
            cognome="Messi",
            cd_ruolo="AM",
            ds_ruolo_locale="Amministrazione",
            id_ab=2,
            matricola="111113",
            fl_docente=0,
            flg_cessato=0,
            cd_uo_aff_org=u2,
            cod_fis="LNL1",
        )
        dip1 = ApiLaboratoriesUnitTestMethods.create_didatticaDipartimento()
        dip2 = ApiLaboratoriesUnitTestMethods.create_didatticaDipartimento(
            dip_id=2,
            dip_cod="2",
            dip_des_it="Lettere e filosofia",
            dip_des_eng="Philosophy",
        )
        erc0 = ApiLaboratoriesUnitTestMethods.create_ricercaErc0()
        erc1_1 = ApiLaboratoriesUnitTestMethods.create_ricercaErc1(
            ricerca_erc0_cod=erc0
        )
        erc1_2 = ApiLaboratoriesUnitTestMethods.create_ricercaErc1(
            cod_erc1="cod1_erc2",
            descrizione="Poetica Platone",
            ricerca_erc0_cod=erc0,
        )
        lab1 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            matricola_referente_compilazione=p1,
            nome_laboratorio="LAB1",
            dipartimento_riferimento=dip1,
            ambito="Tecnologico",
            matricola_responsabile_scientifico=p1,
        )
        lab2 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=2,
            matricola_referente_compilazione=p2,
            nome_laboratorio="LAB2",
            dipartimento_riferimento=dip2,
            ambito="Umanistico",
            matricola_responsabile_scientifico=p2,
        )
        a1 = ApiLaboratoriesUnitTestMethods.create_laboratorioTipologiaAttivita()
        ApiLaboratoriesUnitTestMethods.create_laboratorioAttivita(
            id=1, laboratorio_dati_base=lab1, tipologia_attivita=a1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioAttivita(
            id=2, laboratorio_dati_base=lab1, tipologia_attivita=a1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioAttivita(
            id=3, laboratorio_dati_base=lab2, tipologia_attivita=a1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(
            id=1, laboratorio_dati_base=lab1, ricerca_erc1=erc1_1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(
            id=2, laboratorio_dati_base=lab2, ricerca_erc1=erc1_2
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleRicerca(
            laboratorio_dati_base=lab1,
            matricola_personale_ricerca=p2,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleRicerca(
            id=2,
            laboratorio_dati_base=lab1,
            matricola_personale_ricerca=p2,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleRicerca(
            id=3,
            laboratorio_dati_base=lab2,
            matricola_personale_ricerca=p1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleRicerca(
            id=4,
            laboratorio_dati_base=lab2,
            matricola_personale_ricerca=p1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleTecnico(
            laboratorio_dati_base=lab1,
            matricola_personale_tecnico=p1,
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleTecnico(
            id=2, laboratorio_dati_base=lab1, matricola_personale_tecnico=p1, ruolo="R2"
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleTecnico(
            id=3, laboratorio_dati_base=lab1, matricola_personale_tecnico=p1, ruolo="R1"
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioPersonaleTecnico(
            id=4, laboratorio_dati_base=lab1, matricola_personale_tecnico=p1, ruolo="R2"
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioServiziOfferti(
            laboratorio_dati_base=lab1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioServiziOfferti(
            id=2, laboratorio_dati_base=lab2, nome_servizio="S2"
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioUbicazione(
            laboratorio_dati_base=lab1
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioAltriDipartimenti(
            laboratorio_dati_base=lab1,
            didattica_dipartimento=dip2,
        )

        url1 = reverse("laboratories:apiv2:laboratories-detail", args=["1"])
        res1 = self.req.get(url1)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.json()["id"], 1)
        self.assertEqual(res1.json()["departmentReferentName"], "matematica e informatica")
        self.assertEqual(len(res1.json()["researchPersonnel"]), 1)
        
        url2 = reverse("laboratories:apiv2:laboratories-detail", args=["2"])
        res2 = self.req.get(url2)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()["id"], 2)
        self.assertEqual(res2.json()["area"], "Umanistico")
        
    def test_apiLaboratoriesErc1_Erc2(self):
        erc0 = ApiLaboratoriesUnitTestMethods.create_ricercaErc0()        
        erc1 = ApiLaboratoriesUnitTestMethods.create_ricercaErc1(ricerca_erc0_cod=erc0)
        l1 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=1,
            nome_laboratorio="Informatica",
            ambito="Tecnico",
            dipartimento_riferimento_nome="Informatica",
            sede_dimensione="290",
            responsabile_scientifico="Mungari Simone",
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(
            id=1,
            laboratorio_dati_base=l1,
            ricerca_erc1=erc1,
        )
        ApiLaboratoriesUnitTestMethods.create_ricercaErc2(ricerca_erc1=erc1)
        
        url = reverse("laboratories:apiv2:erclist-list", args=["1"])
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assert_data_len(url, {"laboratory": "1"}, 1)
        
        
        url = reverse("laboratories:apiv2:erclist-list", args=["2"])
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assert_data_len(url, {"laboratory": "1"}, 1)
        
    def test_apiLaboratoriesErc0(self):
        erc0 = ApiLaboratoriesUnitTestMethods.create_ricercaErc0()        
        erc01 = ApiLaboratoriesUnitTestMethods.create_ricercaErc0(
            erc0_cod="112",
            description="ITA",
            description_en="ITA",
        )
        erc1 = ApiLaboratoriesUnitTestMethods.create_ricercaErc1(ricerca_erc0_cod=erc0)
        l1 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase()
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(
            id=1,
            laboratorio_dati_base=l1,
            ricerca_erc1=erc1,
        )
        erc12= ApiLaboratoriesUnitTestMethods.create_ricercaErc1(
            cod_erc1="cod1_erc12",
            descrizione="Computer Science and Informatics",
            ricerca_erc0_cod=erc01,
        )
        l2 = ApiLaboratoriesUnitTestMethods.create_laboratorioDatiBase(
            id=2,
            sede_dimensione="291",
        )
        ApiLaboratoriesUnitTestMethods.create_laboratorioDatiErc1(laboratorio_dati_base=l2, ricerca_erc1=erc12)       
        
        url = reverse("laboratories:apiv2:erclist-list", args=["0"])
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["idErc0"], "111")
        self.assertEqual(len(res.json()["results"]), 2)