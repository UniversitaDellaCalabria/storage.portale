from addressbook.models import Personale
from companies.models import (
    SpinoffStartupDatiBase,
    SpinoffStartupDipartimento,
    TipologiaAreaTecnologica,
)
from django.test import Client, TestCase
from django.urls import reverse
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest


class ApiCompaniesListUnitTest(TestCase):
    def test_apicompanieslist(self):
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

        d1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{"dip_id": 1, "dip_cod": 111, "dip_des_it": "Informatica"}
        )

        s1 = SpinoffStartupDatiBase.objects.create(
            **{
                "id": 1,
                "piva": "1111sc",
                "nome_azienda": "Revelis",
                "nome_file_logo": "aaaa",
                "url_sito_web": "bbbb",
                "descrizione_ita": "applicazione",
                "descrizione_eng": "description",
                "id_area_tecnologica": t1,
                "referente_unical": "Garofalo",
                "matricola_referente_unical": p,
                "is_spinoff": 1,
                "is_startup": 0,
            }
        )

        SpinoffStartupDipartimento.objects.create(
            **{
                "id_spinoff_startup_dati_base": s1,
                "id_didattica_dipartimento": d1,
            }
        )

        url = reverse("companies:apiv1:companies")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1

        data = {"search": "appl", "spinoff": "1", "startup": "0"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"techarea": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"departments": 111}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiCompanyDetailUnitTest(TestCase):
    def test_apicompanydetail(self):
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

        d1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{"dip_id": 1, "dip_des_it": "Informatica"}
        )

        s1 = SpinoffStartupDatiBase.objects.create(
            **{
                "id": 1,
                "piva": "1111sc",
                "nome_azienda": "Revelis",
                "nome_file_logo": "aaaa",
                "url_sito_web": "bbbb",
                "descrizione_ita": "applicazione",
                "descrizione_eng": "description",
                "id_area_tecnologica": t1,
                "referente_unical": "Garofalo",
                "matricola_referente_unical": p,
                "is_spinoff": 1,
                "is_startup": 0,
            }
        )

        SpinoffStartupDipartimento.objects.create(
            **{
                "id_spinoff_startup_dati_base": s1,
                "id_didattica_dipartimento": d1,
            }
        )

        url = reverse("companies:apiv1:company-detail", kwargs={"companyid": "1"})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["SpinoffId"] == 1


class ApiTechAreasListUnitTest(TestCase):
    def test_apitechareaslist(self):
        req = Client()

        TipologiaAreaTecnologica.objects.create(
            **{
                "id": 1,
                "descr_area_ita": "aaa",
                "descr_area_eng": "aaa",
            }
        )

        url = reverse("companies:apiv1:tech-areas-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1
