from addressbook.models import Personale
from companies.models import TipologiaAreaTecnologica
from django.test import Client, TestCase
from django.urls import reverse
from projects.models import (
    ProgettoAmbitoTerritoriale,
    ProgettoDatiBase,
    ProgettoResponsabileScientifico,
    ProgettoRicercatore,
    ProgettoTipologiaProgramma,
)
from structures.models import UnitaOrganizzativa


class ApiProjectsListUnitTest(TestCase):
    def test_apiprojectslist(self):
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

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "ds_tipo_nodo": "facolta",
                "cd_tipo_nodo": "000",
                "id_ab": 1,
                "denominazione": "aaa",
                "denominazione_padre": "c",
                "uo_padre": "11",
                "cd_csa": 1,
            }
        )

        t1 = TipologiaAreaTecnologica.objects.create(
            **{
                "id": 1,
                "descr_area_ita": "aaa",
                "descr_area_eng": "aaa",
            }
        )

        a1 = ProgettoAmbitoTerritoriale.objects.create(
            **{
                "id": 1,
                "ambito_territoriale": "europeo",
            }
        )

        p1 = ProgettoTipologiaProgramma.objects.create(
            **{"id": 1, "nome_programma": "AAA"}
        )

        pr1 = ProgettoDatiBase.objects.create(
            **{
                "id": 1,
                "uo": u1,
                "ambito_territoriale": a1,
                "tipologia_programma": p1,
                "titolo": "Motore",
                "descr_breve": "Mot",
                "abstract_ita": "Motore",
                "abstract_eng": "Engine",
                "area_tecnologica": t1,
                "anno_avvio": 2021,
            }
        )

        ProgettoDatiBase.objects.create(
            **{
                "id": 2,
                "ambito_territoriale": a1,
                "tipologia_programma": p1,
                "titolo": "Motore",
                "descr_breve": "Mot",
                "abstract_ita": "Motore",
                "abstract_eng": "Engine",
                "area_tecnologica": t1,
                "anno_avvio": 2020,
            }
        )

        ProgettoResponsabileScientifico.objects.create(
            **{
                "matricola": p,
                "nome_origine": "Simone",
                "progetto": pr1,
            }
        )

        ProgettoRicercatore.objects.create(
            **{
                "matricola": p,
                "nome_origine": "Simone",
                "progetto": pr1,
            }
        )

        url = reverse("projects:apiv1:projects")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"search": "mot"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"techarea": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"infrastructure": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"programtype": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"-programtype": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"territorialscope": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"year": 2021}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiProjectDetailUnitTest(TestCase):
    def test_apiprojectdetail(self):
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

        a1 = ProgettoAmbitoTerritoriale.objects.create(
            **{
                "id": 1,
                "ambito_territoriale": "europeo",
            }
        )

        p1 = ProgettoTipologiaProgramma.objects.create(
            **{"id": 1, "nome_programma": "AAA"}
        )

        pr1 = ProgettoDatiBase.objects.create(
            **{
                "id": 1,
                "ambito_territoriale": a1,
                "tipologia_programma": p1,
                "titolo": "Motore",
                "descr_breve": "Mot",
                "abstract_ita": "Motore",
                "abstract_eng": "Engine",
                "area_tecnologica": t1,
            }
        )

        ProgettoResponsabileScientifico.objects.create(
            **{
                "matricola": p,
                "nome_origine": "Simone",
                "progetto": pr1,
            }
        )
        ProgettoRicercatore.objects.create(
            **{
                "matricola": p,
                "nome_origine": "Simone",
                "progetto": pr1,
            }
        )

        url = reverse("projects:apiv1:project-detail", kwargs={"projectid": "1"})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["ProjectId"] == 1


class ApiProgramTypesListUnitTest(TestCase):
    def test_apiprogramtypeslist(self):
        req = Client()

        ProgettoTipologiaProgramma.objects.create(
            **{
                "id": 1,
                "nome_programma": "aaa",
            }
        )

        url = reverse("projects:apiv1:projects-program-types")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiProjectInfrastructuresListUnitTest(TestCase):
    def test_apiprojectinfrastructureslist(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": 1,
                "denominazione": "aaaa",
            }
        )
        ProgettoDatiBase.objects.create(
            **{
                "uo": u1,
            }
        )

        url = reverse("projects:apiv1:projects-infrastructures")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1
