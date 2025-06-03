from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiCdsBrochureUnitTestMethods


class ApiCdsBrochureUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

    def test_apisitiwebcdslist(self):
        cds = ApiCdsBrochureUnitTestMethods.create_didatticaCds()

        cds2 = ApiCdsBrochureUnitTestMethods.create_didatticaCds(
            cds_id=2,
            nome_cds_it="Informatica",
            nome_cds_eng="Computer Science",
            cdsord_id=2,
        )

        s1 = ApiCdsBrochureUnitTestMethods.create_cdsBrochure(cds=cds)
        s2 = ApiCdsBrochureUnitTestMethods.create_cdsBrochure(
            id=2,
            aa="2022",
            cds=cds2,
            num_posti=50,
        )
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureExStudenti(cds_brochure=s1)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureLink(cds_brochure=s1)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureSlider(cds_brochure=s1)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureSlider(id=124, cds_brochure=s2)

        url = reverse("cds-brochure:apiv2:cds-brochures-list")

        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 2)
        res = self.req.get(url, data={"search": "Matematica"})
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apisitiwebcdsdetail(self):
        cds = ApiCdsBrochureUnitTestMethods.create_didatticaCds(cds_cod="0999")

        s1 = ApiCdsBrochureUnitTestMethods.create_cdsBrochure(cds=cds)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureExStudenti(cds_brochure=s1)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureLink(cds_brochure=s1)
        ApiCdsBrochureUnitTestMethods.create_cdsBrochureSlider(cds_brochure=s1)

        url = reverse(
            "cds-brochure:apiv2:cds-brochures-detail",
            kwargs={"cds__cds_cod": "0999"},
        )
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"]["cdsCod"], "0999")
