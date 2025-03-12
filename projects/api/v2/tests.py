import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .util_test import ApiProjectsUnitTestMethods


class ProjectsUnitTest(TestCase):
    def setUp(self):
        self.req = Client()
        
        p = ApiProjectsUnitTestMethods.create_personale()
        u1 = ApiProjectsUnitTestMethods.create_unitaOrganizzativa()
        t1 = ApiProjectsUnitTestMethods.create_tipologiaAreaTecnologica()
        a1 = ApiProjectsUnitTestMethods.create_progettoAmbitoTerritoriale()
        p1 = ApiProjectsUnitTestMethods.create_progettoTipologiaProgramma()
        pr1 = ApiProjectsUnitTestMethods.create_progettoDatiBase(
            uo=u1,
            ambito_territoriale=a1,
            tipologia_programma=p1,
            area_tecnologica=t1,
        )
        ApiProjectsUnitTestMethods.create_progettoResponsabileScientifico(
            matricola=p,
            progetto=pr1
        )
        ApiProjectsUnitTestMethods.create_progettoRicercatore(
            matricola=p,
            progetto=pr1
        )
    
    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)
        
    def test_apiprojectslist(self):
        ApiProjectsUnitTestMethods.create_progettoDatiBase(
            id=2,
            ambito_territoriale=self.a1,
            tipologia_programma=self.p1,
            area_tecnologica=self.t1,
            anno_avvio=2020,
        )
       
         
        url = reverse("projects:apiv2:projects-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 2)
        
        self.assert_data_len(url, {"search": "mot"}, 2)      
        self.assert_data_len(url, {"techarea": 1}, 2)  
        self.assert_data_len(url, {"infrastructure": 1}, 1)
        self.assert_data_len(url, {"programtype": 1}, 2)
        self.assert_data_len(url, {"-programtyp": 1}, 0)
        self.assert_data_len(url, {"territorialscope": 1}, 2)
        self.assert_data_len(url, {"year": 2021}, 1)
        
        
    def test_apiprojectdetail(self):
        url = reverse("projects:apiv2:projects-detail", kwargs={"pk": "1"})
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], 1)

    def test_apiprogramtypeslist(self):
        url = reverse("projects:apiv2:program-types-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        
    def test_apiprojectinfrastructureslist(self):
        url = reverse("projects:apiv2:infrastructures-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)