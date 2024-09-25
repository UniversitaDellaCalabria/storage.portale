from addressbook.models import Personale
from companies.models import TipologiaAreaTecnologica
from django.test import Client, TestCase
from django.urls import reverse
from patents.models import BrevettoDatiBase, BrevettoInventori


class ApiPatentsListUnitTest(TestCase):
    def test_apipatentslist(self):
        req = Client()

        p = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Franco",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 1,
                "matricola": "111111",
            }
        )

        t1 = TipologiaAreaTecnologica.objects.create(
            **{
                "id": 1,
                "descr_area_ita": "aaa",
                "descr_area_eng": "aaa",
            }
        )
        b1 = BrevettoDatiBase.objects.create(
            **{
                "id": 1,
                "id_univoco": "100010",
                "titolo": "Ingegneria del sw",
                "url_immagine": "aaaa",
                "breve_descrizione": "applicazione",
                "url_knowledge_share": "aaaa",
                "id_area_tecnologica": t1,
            }
        )

        BrevettoInventori.objects.create(
            **{
                "id": 1,
                "id_brevetto": b1,
                "matricola_inventore": p,
                "cognomenome_origine": "garofalo",
            }
        )

        url = reverse("patents:apiv1:patents")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()["results"]) == 1

        data = {"search": "sw"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"techarea": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiPatentDetailUnitTest(TestCase):
    def test_apipatentdetail(self):
        req = Client()

        p = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Franco",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 1,
                "matricola": "111111",
            }
        )

        t1 = TipologiaAreaTecnologica.objects.create(
            **{
                "id": 1,
                "descr_area_ita": "aaa",
                "descr_area_eng": "aaa",
            }
        )
        b1 = BrevettoDatiBase.objects.create(
            **{
                "id": 1,
                "id_univoco": "100010",
                "titolo": "Ingegneria del sw",
                "url_immagine": "aaaa",
                "breve_descrizione": "applicazione",
                "url_knowledge_share": "aaaa",
                "id_area_tecnologica": t1,
            }
        )

        BrevettoInventori.objects.create(
            **{
                "id": 1,
                "id_brevetto": b1,
                "matricola_inventore": p,
                "cognomenome_origine": "garofalo",
            }
        )

        url = reverse("patents:apiv1:patent-detail", kwargs={"patentid": "1"})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert res.json()["results"]["PatentId"] == 1
