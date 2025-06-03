from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiPatentsUnitTestMethods


class PatentsUnitTest(TestCase):
    def setUp(self):
        self.req = Client()
        p = ApiPatentsUnitTestMethods.create_personale()
        t1 = ApiPatentsUnitTestMethods.create_tipologiaAreaTecnologica()
        b1 = ApiPatentsUnitTestMethods.create_brevettoDatiBase(area_tecnologica=t1)
        ApiPatentsUnitTestMethods.create_brevettoInventori(
            brevetto=b1, matricola_inventore=p
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_apipatentslist(self):
        url = reverse("patents:apiv2:patents-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        self.assert_data_len(url, {"search": "sw"}, 1)
        self.assert_data_len(url, {"techarea": 1}, 1)

    def test_apipatentdetail(self):
        url = reverse("patents:apiv2:patents-detail", kwargs={"patentid": "1"})
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], 1)
