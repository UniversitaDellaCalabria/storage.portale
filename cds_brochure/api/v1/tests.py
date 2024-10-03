from cds.api.v1.util_tests import (
    DidatticaCdsUnitTest,
)
from cds_brochure.models import (
    CdsBrochure,
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider,
)
from django.test import Client, TestCase
from django.urls import reverse


class ApiSitoWebCdsListUnitTest(TestCase):
    def test_apisitiwebcdslist(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "cds_id": 1,
                "cds_cod": "aaa",
                "nome_cds_it": "Matematica",
                "nome_cds_eng": "Math",
            }
        )

        s1 = CdsBrochure.objects.create(
            **{
                "id": 1,
                "aa": "2022",
                "cds": cds,
                # 'nome_corso_it': 'Informatica',
                # 'nome_corso_en': 'Computer Science',
                # 'lingua_it': 'italiano',
                # 'lingua_en': "italian",
                # 'classe_laurea_it': 'aaa',
                # 'durata': 50,
                "num_posti": 50,
            }
        )

        CdsBrochureExStudenti.objects.create(
            **{
                "id": 111,
                "ordine": 1,
                "profilo_it": "aaa",
                "profilo_en": "aaa",
                "link_it": "aaa",
                "link_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        CdsBrochureLink.objects.create(
            **{
                "id": 111111,
                "ordine": 1,
                "descrizione_link_it": "aaa",
                "descrizione_link_en": "aaa",
                "link_it": "aaa",
                "link_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        CdsBrochureSlider.objects.create(
            **{
                "id": 123,
                "ordine": 1,
                "slider_it": "aaa",
                "slider_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        s2 = CdsBrochure.objects.create(
            **{
                "id": 2,
                "aa": "2022",
                # 'nome_corso_it': 'Ingegneria',
                # 'nome_corso_en': 'Computer Engineering',
                # 'lingua_it': 'italiano',
                # 'lingua_en': "italian",
                # 'durata': 50,
                "num_posti": 50,
            }
        )

        CdsBrochureSlider.objects.create(
            **{
                "id": 124,
                "ordine": 1,
                "slider_it": "aaa",
                "slider_en": "aaa",
                "id_sito_web_cds_dati_base": s2,
            }
        )

        url = reverse("cds-brochure:apiv1:cds-websites-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {
            "search": "Matematica"
        }  # , 'academic_year': 2022, 'cdslanguage': 'italiano', 'course_class': 'aaa'}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiSitoWebCdsDetailUnitTest(TestCase):
    def test_apisitowebcdsdetail(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "cds_id": 1,
                "cds_cod": "0999",
                "nome_cds_it": "Matematica",
                "nome_cds_eng": "Math",
            }
        )

        s1 = CdsBrochure.objects.create(
            **{
                "id": 1,
                "cds": cds,
                "aa": "2022",
                # 'nome_corso_it': 'Informatica',
                # 'nome_corso_en': 'Computer Science',
                # 'lingua_it': 'italiano',
                # 'lingua_en': "italian",
                # 'durata': 50,
                "num_posti": 50,
            }
        )

        CdsBrochureExStudenti.objects.create(
            **{
                "id": 1,
                "ordine": 1,
                "profilo_it": "aaa",
                "profilo_en": "aaa",
                "link_it": "aaa",
                "link_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        CdsBrochureLink.objects.create(
            **{
                "id": 1,
                "ordine": 1,
                "descrizione_link_it": "aaa",
                "descrizione_link_en": "aaa",
                "link_it": "aaa",
                "link_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        CdsBrochureSlider.objects.create(
            **{
                "id": 1,
                "ordine": 1,
                "slider_it": "aaa",
                "slider_en": "aaa",
                "id_sito_web_cds_dati_base": s1,
            }
        )

        url = reverse("cds-brochure:apiv1:cds-website-detail", kwargs={"cdswebsitecod": "0999"})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert res.json()["results"]["CDSCOD"] == "0999"
