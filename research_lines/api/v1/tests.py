from addressbook.models import Personale
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import encrypt
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
    RicercaLineaApplicata,
    RicercaLineaBase,
)


class ApiBaseResearchLineUnitTest(TestCase):
    def test_apibaseresearchline(self):
        req = Client()

        doc1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "ds_sede": "DIMES",
                "sede": "1111",
            }
        )

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
            }
        )

        erc1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        erc2 = RicercaErc2.objects.create(
            **{
                "cod_erc2": "cod1_erc2",
                "descrizione": "Machine learning",
                "ricerca_erc1": erc1,
            }
        )
        linea_base = RicercaLineaBase.objects.create(
            **{
                "id": 1,
                "ricerca_erc2": erc2,
                "descrizione": "regressione lineare",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
                "anno": "2016",
                "visibile": 1,
            }
        )
        RicercaDocenteLineaBase.objects.create(
            **{"personale": doc1, "ricerca_linea_base": linea_base}
        )

        url = reverse("research-lines:apiv1:base-research-lines")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["RLineDescription"] == "regressione lineare"

        res = req.get(url)
        assert len(res.json()["results"]) == 1

        data = {"search": "reg"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"year": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"teacher": encrypt("111112"), "department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": encrypt("111112")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiAppliedResearchLineUnitTest(TestCase):
    def test_apiappliedresearchline(self):
        req = Client()

        doc1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "ds_sede": "DIMES",
                "sede": "1111",
            }
        )

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
            }
        )

        aster1 = RicercaAster1.objects.create(
            **{
                "id": 1,
                "descrizione": "ICT & Design",
                "ricerca_erc0_cod": erc0,
            }
        )
        aster2 = RicercaAster2.objects.create(
            **{
                "id": 2,
                "descrizione": "Algorithms. Data and signal processing",
                "ricerca_aster1": aster1,
            }
        )
        linea_applicata = RicercaLineaApplicata.objects.create(
            **{
                "id": 1,
                "ricerca_aster2": aster2,
                "descrizione": "regressione lineare",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
                "anno": "2016",
                "visibile": 1,
            }
        )

        RicercaDocenteLineaApplicata.objects.create(
            **{
                "personale": doc1,
                "ricerca_linea_applicata": linea_applicata,
                "dt_ins": "2021-01-03 15:47:21",
            }
        )

        url = reverse("research-lines:apiv1:applied-research-lines")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["RLineDescription"] == "regressione lineare"

        res = req.get(url)
        assert len(res.json()["results"]) == 1

        data = {"search": "reg"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"year": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"teacher": encrypt("111112")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": encrypt("111112"), "department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiAllResearchLinesUnitTest(TestCase):
    def test_apiallbresearchlines(self):
        req = Client()

        doc1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "ds_sede": "DIMES",
                "sede": "1111",
            }
        )

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
            }
        )

        erc1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        erc2 = RicercaErc2.objects.create(
            **{
                "cod_erc2": "cod1_erc2",
                "descrizione": "Machine learning",
                "ricerca_erc1": erc1,
            }
        )
        linea_base = RicercaLineaBase.objects.create(
            **{
                "id": 1,
                "ricerca_erc2": erc2,
                "descrizione": "regressione lineare",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
                "anno": "2016",
                "visibile": 1,
            }
        )

        aster1 = RicercaAster1.objects.create(
            **{
                "id": 1,
                "descrizione": "ICT & Design",
                "ricerca_erc0_cod": erc0,
            }
        )
        aster2 = RicercaAster2.objects.create(
            **{
                "id": 2,
                "descrizione": "Algorithms. Data and signal processing",
                "ricerca_aster1": aster1,
            }
        )
        linea_applicata = RicercaLineaApplicata.objects.create(
            **{
                "id": 1,
                "ricerca_aster2": aster2,
                "descrizione": "regressione lineare",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
                "anno": "2016",
                "visibile": 1,
            }
        )
        RicercaDocenteLineaApplicata.objects.create(
            **{
                "personale": doc1,
                "ricerca_linea_applicata": linea_applicata,
                "dt_ins": "2021-01-03 15:47:21",
            }
        )
        RicercaDocenteLineaBase.objects.create(
            **{"personale": doc1, "ricerca_linea_base": linea_base}
        )

        url = reverse("research-lines:apiv1:all-research-lines")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"search": "reg"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"year": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"ercs": "cod1_erc1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"asters": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"ercs": "cod1_erc1", "asters": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2
