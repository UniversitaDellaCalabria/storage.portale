from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiPhdUnitTestMethods


class PhdUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        dip = ApiPhdUnitTestMethods.create_didatticaDipartimento()
        cds = ApiPhdUnitTestMethods.create_didatticaDottoratoCds(dip_cod=dip)
        ApiPhdUnitTestMethods.create_didatticaDottoratoPds(cds_id_esse3=cds, aa_ord=cds)
        ApiPhdUnitTestMethods.create_didatticaDottoratoRegolamento(
            cds_id_esse3=cds, aa_ord=cds
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def assert_equal_with_data(self, url, campo, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(res.json()["results"][0][campo], result)

    def test_apiphdlist(self):
        url = reverse("phd:apiv2:phd-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["cdsCOD"], "111")

        self.assert_equal_with_data(url, "cdsCOD", {"department": 1}, "111")
        self.assert_equal_with_data(url, "cdsCOD", {"year": 2020}, "111")
        self.assert_equal_with_data(url, "cdsCOD", {"regdidid": "111"}, "111")
        self.assert_equal_with_data(url, "cdsCOD", {"pdscod": "GEN"}, "111")

        self.assert_data_len(url, {"yearTo": 2019, "yearFrom": 2018}, 0)
        self.assert_data_len(url, {"yearTo": 2019}, 0)
        self.assert_data_len(url, {"yearFrom": 2018}, 1)
        self.assert_data_len(url, {"cycle": 0}, 0)

    def test_apicycleslist(self):
        url = reverse("phd:apiv2:phd/cycles-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        
        
class PhdActivitiesListlUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        tipologia = ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaTipologia()
        a1= ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativa(tipologia=tipologia)
        a2= ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativa(id=2,
            nome_af="BBBB",
            struttura_proponente_origine="aaaa",
            rif_dottorato="umanistici",
            tipologia=tipologia
            )
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaDocente(didattica_dottorato_attivita_formativa=a1)
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaAltriDocenti(didattica_dottorato_attivita_formativa=a2)

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_apiphdactivitieslist(self):
        url = reverse("phd:apiv2:phd/activities-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 2)

        self.assert_data_len(url, {"search": "AAA"}, 1)

        self.assert_data_len(url, {"structure": "dimes"}, 1)

        self.assert_data_len(url, {"phd": "umanistici"}, 1)

        self.assert_data_len(url, {"teacher": "simone"}, 1)
        self.assert_data_len(url, {"teacher": "ludovico"}, 0)
        self.assert_data_len(url, {"teacher": "carmine"}, 1)     
class PhdActivitiesDetaillUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        tipologia = ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaTipologia()
        a1= ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativa(tipologia=tipologia)
        p1 = ApiPhdUnitTestMethods.create_personale()
        p2 = ApiPhdUnitTestMethods.create_personale(id=2, nome="Simone", cognome="Munggari", id_ab=2, matricola="11111")
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaDocente(didattica_dottorato_attivita_formativa=a1, cognome_nome_origine="Franco", matricola=p1)
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaAltriDocenti(didattica_dottorato_attivita_formativa=a1, cognome_nome_origine="Simone", matricola=p2)
        
    def test_apiphdactivitieslist(self):
        url = reverse("phd:apiv2:phd/activities-detail", kwargs={"pk": 1})
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], 1)
        
    def test_apiphdactivitiestypologieslist(self):
        url = reverse("phd:apiv2:phd/activities/typologies-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        
        
class RefPhdListUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        tipologia = ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaTipologia()
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativa(tipologia=tipologia, ciclo=True)
        
    def test_apirefphdlist(self):
        url = reverse("phd:apiv2:ref/phd-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        
class PhdSsdLisUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        tipologia = ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativaTipologia()
        ApiPhdUnitTestMethods.create_didatticaDottoratoAttivitaFormativa(tipologia=tipologia, ssd="Convenzionale")
        
    def test_apirefphdlist(self):
        url = reverse("phd:apiv2:phd/ssd-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        
 