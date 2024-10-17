from addressbook.models import Personale
from django.test import Client, TestCase
from django.urls import reverse
from phd.models import (
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaAltriDocenti,
    DidatticaDottoratoAttivitaFormativaDocente,
    DidatticaDottoratoCds,
    DidatticaDottoratoPds,
    DidatticaDottoratoRegolamento,
)
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest


class ApiPhdListUnitTest(TestCase):
    def test_apiphdlistunittest(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": 1,
                "dip_des_it": "Matematica e Informatica",
                "dip_des_eng": "Math and Computer Science",
            }
        )

        cds = DidatticaDottoratoCds.objects.create(
            **{
                "dip_cod": dip,
                "cds_id_esse3": 1,
                "cds_cod": "111",
                "aa_ord_id": 1,
            }
        )

        DidatticaDottoratoPds.objects.create(
            **{
                "cds_id_esse3": cds,
                "aa_ord": cds,
                "pds_cod": "GEN",
            }
        )

        DidatticaDottoratoRegolamento.objects.create(
            **{
                "regdid_id_esse3": 1,
                "cds_id_esse3": cds,
                "aa_ord": cds,
                "aa_regdid_id": 2020,
                "num_ciclo": 10,
            }
        )

        url = reverse("phd:apiv1:phd-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["PhdCdsCOD"] == "111"

        data = {"department": 1}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["PhdCdsCOD"] == "111"

        data = {"year": 2020}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["PhdCdsCOD"] == "111"

        data = {"yearTo": 2019, "yearFrom": 2018}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"yearTo": 2019}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"yearFrom": 2018}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"regdidid": "111"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["PhdCdsCOD"] == "111"

        data = {"pdscod": "GEN"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["PhdCdsCOD"] == "111"

        data = {"cycle": 0}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        url = reverse("phd:apiv1:phd-cycles")
        # check url
        res = req.get(url)
        assert res.status_code == 200


class ApiPhdActivitiesListlUnitTest(TestCase):
    def test_apiphdactivitieslist(self):
        req = Client()

        a1 = DidatticaDottoratoAttivitaFormativa.objects.create(
            **{
                "id": 1,
                "nome_af": "AAAA",
                "struttura_proponente_origine": "dimes",
                "rif_dottorato": "matematica",
                "ciclo": 1,
            }
        )

        a2 = DidatticaDottoratoAttivitaFormativa.objects.create(
            **{
                "id": 2,
                "nome_af": "BBBB",
                "struttura_proponente_origine": "aaaa",
                "rif_dottorato": "umanistici",
                "ciclo": 1,
            }
        )

        DidatticaDottoratoAttivitaFormativaDocente.objects.create(
            **{
                "didattica_dottorato_attivita_formativa": a1,
                "cognome_nome_origine": "Simone",
            }
        )

        DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(
            **{
                "didattica_dottorato_attivita_formativa": a2,
                "cognome_nome_origine": "Carmine",
            }
        )

        url = reverse("phd:apiv1:phd-activities-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"search": "AAA"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"structure": "dimes"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"phd": "umanistici"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": "simone"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": "ludovico"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"teacher": "carmine"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiPhdActivityDetailUnitTest(TestCase):
    def test_apiphdactivitydetail(self):
        req = Client()

        a1 = DidatticaDottoratoAttivitaFormativa.objects.create(
            **{"id": 1, "nome_af": "AAAA", "ciclo": 1}
        )

        p1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Franco",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 1,
                "matricola": "111111",
            }
        )
        p2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Simone",
                "cognome": "Munggari",
                "cd_ruolo": "PO",
                "id_ab": 2,
                "matricola": "111112",
            }
        )
        DidatticaDottoratoAttivitaFormativaDocente.objects.create(
            **{
                "didattica_dottorato_attivita_formativa": a1,
                "cognome_nome_origine": "Franco",
                "matricola": p1,
            }
        )

        DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(
            **{
                "didattica_dottorato_attivita_formativa": a1,
                "cognome_nome_origine": "Simone",
                "matricola": p2,
            }
        )

        url = reverse("phd:apiv1:phd-activity-detail", kwargs={"id": 1})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["ID"] == 1

        url = reverse("phd:apiv1:phd-activity-typologies")
        res = req.get(url)
        assert res.status_code == 200


class ApiRefPhdListUnitTest(TestCase):
    def test_apirefphdlist(self):
        req = Client()

        DidatticaDottoratoAttivitaFormativa.objects.create(
            **{
                "id": 1,
                "nome_af": "AAAA",
                "struttura_proponente_origine": "dimes",
                "rif_dottorato": "matematica",
                "ciclo": True,
            }
        )

        url = reverse("phd:apiv1:ref-phd")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiPhdSsdListUnitTest(TestCase):
    def test_apiphdssdlist(self):
        req = Client()

        DidatticaDottoratoAttivitaFormativa.objects.create(
            **{"id": 1, "ssd": "Convenzionale", "ciclo": 1}
        )

        url = reverse("phd:apiv1:phd-ssd-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1
