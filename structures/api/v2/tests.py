from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiStructuresUnitTestMethods


class StructuresUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        ApiStructuresUnitTestMethods.create_didatticaDipartimento()
        ApiStructuresUnitTestMethods.create_didatticaDipartimento(
            dip_id=2,
            dip_cod="002",
            dip_des_it="Dipartimento di Letteratura",
            dip_des_eng="Department of Literature",
            dip_nome_breve="LIT",
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def assert_equal_with_data(self, url, campo, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(res.json()["results"][0][campo], result)

    def assert_equal_with_lang(self, url, campo, result, lang="it"):
        res = self.req.get(url, HTTP_ACCEPT_LANGUAGE=lang)
        self.assertEqual(res.json()["results"][0][campo], result)

    def test_apidepartmentslist(self):
        url = reverse("structures:apiv2:departments-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)

        self.assert_equal_with_lang(
            url, "name", "Dipartimento di Letteratura", lang="it"
        )
        
    def test_apidepartmentdetail(self):
        url = reverse("structures:apiv2:departments-detail", kwargs={"dip_cod": "001"})
        
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        
        self.assertEqual(res.json()["name"], "Dipartimento di Matematica e Informatica")
        
    def test_apistructureslist(self):
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa()
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="DIR",
            denominazione="DIREZIONE",
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            ds_tipo_nodo="uffici",
            cd_tipo_nodo="UFF",
            denominazione="UFFICI",
        )
        
        url = reverse("structures:apiv2:structures-list")
        
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        
        self.assertEqual(res.json()["results"][2]["typeName"], "uffici")
        self.assertEqual(res.json()["results"][0]["cod"], "2")
        
        self.assertEqual(len(res.json()["results"]), 3)
        
        self.assert_equal_with_data(url, "cod", {"search": "Direzione"}, "2")
            
        self.assert_data_len(url,  {"type": "DIR,UFF"}, 2)
        self.assert_data_len(url,  {"type": "DIR,UFF", "search": "Direzione"}, 1)
    
    def test_apistructurestypes(self):
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            ds_tipo_nodo="facolta",
            cd_tipo_nodo="000",
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            ds_tipo_nodo="rettorato",
            cd_tipo_nodo="RET",
        )

        url = reverse("structures:apiv2:types-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][1]["typeName"], "facolta")
        self.assertEqual(res.json()["results"][0]["typeCOD"], "CDS")
        self.assertEqual(len(res.json()["results"]), 3)

    def test_apiallstructureslist(self):
        u1 = ApiStructuresUnitTestMethods.create_unitaOrganizzativa()
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="DIR",
            denominazione="DIREZIONE",
            uo_padre=0
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            ds_tipo_nodo="uffici",
            cd_tipo_nodo="UFF",
            denominazione="UFFICI",
            uo_padre=0
        )
        ApiStructuresUnitTestMethods.create_personale(cd_uo_aff_org=u1)

        url = reverse("addressbook:apiv2:addressbookstructures-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 3)
        self.assert_data_len(url,  {"search": "Direzione"}, 1)
        self.assert_data_len(url,  {"type": "DIR,UFF"}, 2)
        self.assert_data_len(url,  {"father": "1"}, 1)
        self.assert_data_len(url,  {"father": "None"}, 0)
    
    def test_apirefstructureslist(self):
        ApiStructuresUnitTestMethods.create_didatticaDottoratoAttivitaFormativa()
        
        url = reverse("phd:apiv2:ref/structures-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiterritorialscopeslist(self):
        ApiStructuresUnitTestMethods.create_progettoAmbitoTerritoriale()
        
        url = reverse("projects:apiv2:territorial-scopes-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        
    def test_apistructurefunctionstypeslist(self):
        ApiStructuresUnitTestMethods.create_unitaOrganizzativaTipoFunzioni()
        url = reverse("structures:apiv2:functions-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        
    def test_apistructuredetail(self):
        u1 = ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            ds_tipo_nodo="facolta",
            cd_tipo_nodo="000",
            id_ab=1,
            denominazione="aaa",
            denominazione_padre="c",
            uo_padre="11",
            cd_csa="1",
            dt_fine_val="2222-01-01",
        )
        
        u2 = ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
            id_ab=2,
            denominazione="bbb",
            denominazione_padre="d",
            uo_padre="22",
            cd_csa="2",
            dt_fine_val="2222-01-01",
        )
        
        ApiStructuresUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            ds_tipo_nodo="rettorato",
            cd_tipo_nodo="RET",
            id_ab=3,
            denominazione="ccc",
            denominazione_padre="d",
            uo_padre="33",
            dt_fine_val="2222-01-01",
        )
        
        p1 = ApiStructuresUnitTestMethods.create_personale(
            id=1,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            ds_ruolo_locale="Professore Associato",
            id_ab=1,
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            cod_fis="SMN1",
        )
        
        p2 = ApiStructuresUnitTestMethods.create_personale(
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
        
        tipo_contatto = ApiStructuresUnitTestMethods.create_personaleUoTipoContatto()
        ApiStructuresUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="URL Sito WEB Curriculum Vitae",
            descr_contatto="URL Sito WEB Curriculum Vitae",
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativaContatti(
            cd_tipo_cont=tipo_contatto,
            ab=u1,
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativaContatti(
            cd_tipo_cont=tipo_contatto,
            ab=u2,
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=1,
            ds_funzione="Amministrazione",
            termine="2999-12-1",
            cod_fis=p1,
            cd_csa=u1,
        )
        ApiStructuresUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=2,
            ds_funzione="Delega",
            termine=None,
            cod_fis=p2,
            cd_csa=u2,
        )
        
        
        url1 = reverse("structures:apiv2:structures-detail", kwargs={"pk": "1"})
        url2 = reverse("structures:apiv2:structures-detail", kwargs={"pk": "2"})
        
        res1 = self.req.get(url1)
        self.assertEqual(res1.status_code, 200)
        
        res2 = self.req.get(url2)
        self.assertEqual(res2.status_code, 200)
        
        self.assertEqual(res1.json()["cod"], "1")
        self.assertEqual(res2.json()["cod"], "2")
