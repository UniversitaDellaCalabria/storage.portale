from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiCompaniesUnitTestMethods


class CompaniesUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        p = ApiCompaniesUnitTestMethods.create_personale()
        t1 = ApiCompaniesUnitTestMethods.create_tipologiaAreaTecnologica()
        d1 = ApiCompaniesUnitTestMethods.create_didatticaDipartimento()
        s1 = ApiCompaniesUnitTestMethods.create_spinoffStartupDatiBase(
            area_tecnologica=t1, matricola_referente_unical=p
        )
        ApiCompaniesUnitTestMethods.create_spinoffStartupDipartimento(
            spinoff_startup_dati_base=s1, didattica_dipartimento=d1
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_apicompanieslist(self):
        url = reverse("companies:apiv2:companies-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

        self.assert_data_len(url, {"search": "appl", "spinoff": "1", "startup": "0"}, 1)
        self.assert_data_len(url, {"techarea": 1}, 1)
        self.assert_data_len(url, {"cod": 111}, 1)

    def test_apicompanydetail(self):
        url = reverse("companies:apiv2:companies-detail", kwargs={"pk": "1"})
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], 1)

    def test_apitechareaslist(self):
        url = reverse("companies:apiv2:tech-areas-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
