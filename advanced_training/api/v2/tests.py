from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiAdvancedTrainingUnitTestMethods


class AdvancedTrainingUnitTest(TestCase):
    def setUp(self):
        self.req = Client()
        
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneModalitaErogazione()
        dip = ApiAdvancedTrainingUnitTestMethods.create_didatticaDipartimento()
        doc1 = ApiAdvancedTrainingUnitTestMethods.create_personale()
        aftc = ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneTipoCorso(
            id=3
        )
        afme = ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneModalitaErogazione(id=3)
        a1 = ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneDatiBase(
            matricola_direttore_scientifico=doc1,
            alta_formazione_tipo_corso=aftc,
            alta_formazione_mod_erogazione=afme,
            dipartimento_riferimento=dip,
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneDatiBase(
            id=2,
            matricola_direttore_scientifico=doc1,
            alta_formazione_tipo_corso=aftc,
            alta_formazione_mod_erogazione=afme,
            dipartimento_riferimento=dip,
            anno_rilevazione=2022
            
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneConsiglioScientificoEsterno(
            alta_formazione_dati_base=a1
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneConsiglioScientificoInterno(
            matricola_cons=doc1,
            alta_formazione_dati_base=a1,
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazionePartner(
            alta_formazione_dati_base=a1
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneModalitaSelezione(
            alta_formazione_dati_base=a1
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazioneIncaricoDidattico(
            alta_formazione_dati_base=a1
        )
        ApiAdvancedTrainingUnitTestMethods.create_altaFormazionePianoDidattico(
            alta_formazione_dati_base=a1
        )

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_apierogationmodeslist(self):
        url = reverse("advanced-training:apiv2:erogation-modes-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 2)
        
    def test_apihighformationmasterslist(self):
        url = reverse("advanced-training:apiv2:high-formation-masters-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assert_data_len(url, {"search": "AAA"}, 2)
        self.assert_data_len(url, {"coursetype": "3"}, 2)
        self.assert_data_len(url, {"erogation": "3"}, 2)
        self.assert_data_len(url, {"department": "1111"}, 0)
        self.assert_data_len(url, {"director": "111112"}, 0)
        self.assert_data_len(url, {"year": 2021}, 1)
        
    def test_apihighformationmasterdetail(self):
        url = reverse("advanced-training:apiv2:high-formation-masters-detail", kwargs={"pk": 1})
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["masterTitle"], "AAAA")
        
    def test_apicoursetypeslist(self):
        url = reverse("advanced-training:apiv2:high-formation-course-types-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
