from django.test import TestCase, Client
from django.urls import reverse
from generics.utils import encrypt
from .util_test import ApiResearchLinesUnitTestMethods
from research_groups.api.v2.util_test import ApiResearchGroupsUnitTestMethods


class ResearchLinesUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        doc = ApiResearchGroupsUnitTestMethods.create_personale()
        erc0 = ApiResearchGroupsUnitTestMethods.create_ricercaErc0()
        erc1 = ApiResearchGroupsUnitTestMethods.create_ricercaErc1(
            ricerca_erc0_cod=erc0
        )
        erc2 = ApiResearchLinesUnitTestMethods.create_ricercaErc2(ricerca_erc1=erc1)
        linea_base = ApiResearchLinesUnitTestMethods.create_ricercaLineaBase(
            ricerca_erc2=erc2
        )
        ApiResearchLinesUnitTestMethods.create_ricercaDocenteLineaBase(
            personale=doc, ricerca_linea_base=linea_base
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_researchgroups(self):
        url = reverse("research-lines:apiv2:base-research-lines-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["description"], "regressione lineare")
        self.assertEqual(len(res.json()["results"]), 1)
        self.assert_data_len(url, {"search": "reg"}, 1)
        self.assert_data_len(url, {"year": 2020}, 0)
        self.assert_data_len(
            url, {"teacher": encrypt("111112"), "department": "1111"}, 1
        )
        self.assert_data_len(url, {"teacher": encrypt("111112")}, 1)
        self.assert_data_len(url, {"department": "1111"}, 1)

class AppliedResearchLinesUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

        doc = ApiResearchGroupsUnitTestMethods.create_personale()
        erc0 = ApiResearchGroupsUnitTestMethods.create_ricercaErc0()
        aster1 = ApiResearchLinesUnitTestMethods.create_ricercaAster1(ricerca_erc0_cod=erc0)
        aster2 = ApiResearchLinesUnitTestMethods.create_ricercaAster2(ricerca_aster1=aster1)
        linea_applicata = ApiResearchLinesUnitTestMethods.create_ricercaLineaApplicata(ricerca_aster2=aster2)
        ApiResearchLinesUnitTestMethods.create_ricercaDocenteLineaApplicata(personale=doc, ricerca_linea_applicata=linea_applicata)


    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    # def assert_equal_with_data(self, url, campo, data, result):
    #     res = self.req.get(url, data=data)
    #     self.assertEqual(res.json()["results"][0][campo], result)

    def test_researchgroups(self):
        url = reverse("research-lines:apiv2:applied-research-lines-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["description"], "regressione lineare")
        self.assertEqual(len(res.json()["results"]), 1)
        self.assert_data_len(url, {"search": "reg"}, 1)
        self.assert_data_len(url, {"year": 2020}, 0)
        
        self.assert_data_len(
            url, {"teacher": encrypt("111112"), "department": "1111"}, 1
        )
        self.assert_data_len(url, {"teacher": encrypt("111112")}, 1)
        self.assert_data_len(url, {"department": "1111"}, 1)