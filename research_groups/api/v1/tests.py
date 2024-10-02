from addressbook.models import Personale
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import encrypt
from research_groups.models import RicercaDocenteGruppo, RicercaGruppo
from research_lines.models import RicercaErc0, RicercaErc1


class ApiResearchGroupsUnitTest(TestCase):
    def test_apiresearchgroups(self):
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

        RicercaErc1.objects.create(
            **{
                "id": 1,
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        ricerca_gruppo1 = RicercaGruppo.objects.create(
            **{
                "id": 1,
                "nome": "Intelligenza Artificiale",
                "descrizione": "ricerca su Machine Learning",
                "ricerca_erc1_id": 1,
            }
        )
        RicercaGruppo.objects.create(
            **{
                "id": 2,
                "nome": "machine learning",
                "descrizione": "ricerca su Machine Learning",
                "ricerca_erc1_id": 1,
            }
        )

        RicercaDocenteGruppo.objects.create(
            **{"personale": doc1, "ricerca_gruppo": ricerca_gruppo1}
        )

        url = reverse("research-groups:apiv1:research-groups")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["RGroupID"] == 1

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"teacher": encrypt("111112")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"coderc1": "cod1_erc1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"search": "Intel"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": encrypt("111112"), "department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1
