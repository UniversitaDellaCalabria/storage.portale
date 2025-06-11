from django.test import TestCase, Client
from django.urls import reverse
from generics.utils import encrypt
from .util_test import ApiResearchGroupsUnitTestMethods


class ResearchGroupsUnitTest(TestCase):
    def setUp(self):
        self.req = Client()
        
        doc = ApiResearchGroupsUnitTestMethods.create_personale()
        erc0 = ApiResearchGroupsUnitTestMethods.create_ricercaErc0()
        ApiResearchGroupsUnitTestMethods.create_ricercaErc1(ricerca_erc0_cod=erc0)
        ricerca_gruppo1 = ApiResearchGroupsUnitTestMethods.create_ricercaGruppo()
        ApiResearchGroupsUnitTestMethods.create_ricercaGruppo(id=2, nome="machine learning")
        ApiResearchGroupsUnitTestMethods.create_ricercaDocenteGruppo(personale=doc, ricerca_gruppo=ricerca_gruppo1)

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def assert_equal_with_data(self, url, campo, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(res.json()["results"][0][campo], result)

    def test_researchgroups(self):
        url = reverse("research-groups:apiv2:research-groups-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["id"], 1)
        self.assertEqual(len(res.json()["results"]), 2)
        self.assert_data_len(url, {"teacher": encrypt("111112")}, 1)
        self.assert_data_len(url, {"coderc1": "cod1_erc1"}, 2)
        self.assert_data_len(url, {"search": "Intel"}, 1)
        self.assert_data_len(url, {"teacher": encrypt("111112"), "department": "1111"}, 1)
        self.assert_data_len(url, {"department": "1111"}, 1)

        
        