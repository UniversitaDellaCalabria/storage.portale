import datetime

from addressbook.models import (
    Personale,
    PersonaleAttivoTuttiRuoli,
    PersonaleContatti,
    PersonalePrioritaRuolo,
    PersonaleUoTipoContatto,
)
from cds.models import DidatticaCopertura
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import decrypt, encrypt
from rest_framework.authtoken.models import Token
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest
from structures.models import (
    UnitaOrganizzativa,
    UnitaOrganizzativaContatti,
    UnitaOrganizzativaFunzioni,
)


class ApiAddressbookStructuresListUnitTest(TestCase):
    def test_apiaddressbookstructureslist(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
                "cd_tipo_nodo": "DRZ",
                "ds_tipo_nodo": "Direzione",
                "dt_fine_val": "2222-01-01",
            }
        )
        u2 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "uo_padre": "2",
                "dt_fine_val": "2222-01-01",
            }
        )
        PersonaleAttivoTuttiRuoli.objects.create(
            **{
                "matricola": "111114",
                "cd_ruolo": "PO",
                "ds_ruolo": "Professore Ordinario",
                "cd_uo_aff_org": u1,
                "ds_aff_org": "Direzione",
            }
        )

        PersonalePrioritaRuolo.objects.create(
            **{
                "cd_ruolo": "PO",
                "priorita": 1,
            }
        )
        p1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN1",
                "cv_full_it": "AAA",
                "cv_short_it": "A",
                "cv_full_eng": "BBB",
                "cv_short_eng": "B",
            }
        )
        p2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Lionel",
                "cognome": "Messi",
                "cd_ruolo": "AM",
                "ds_ruolo_locale": "Amministrazione",
                "id_ab": 2,
                "matricola": "111113",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "LNL1",
                "cv_full_it": "BBB",
                "cv_short_it": "B",
                "cv_full_eng": "AA",
                "cv_short_eng": "A",
            }
        )
        Personale.objects.create(
            **{
                "id": 10,
                "nome": "Simone10",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 10,
                "matricola": "111119",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN10",
            }
        )
        Personale.objects.create(
            **{
                "id": 55,
                "nome": "Simone2",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 55,
                "matricola": "111166",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN25",
            }
        )
        Personale.objects.create(
            **{
                "id": 13,
                "nome": "Simone13",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 13,
                "matricola": "1111145",
                "fl_docente": 0,
                "flg_cessato": 1,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN13",
            }
        )
        Personale.objects.create(
            **{
                "id": 4,
                "nome": "Simone4",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 4,
                "matricola": "111115",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN4",
            }
        )
        p3 = Personale.objects.create(
            **{
                "id": 3,
                "nome": "Zlatan",
                "cognome": "Ibra",
                "id_ab": 3,
                "matricola": "111114",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cod_fis": "ZLT",
                "cd_uo_aff_org": u2,
                "dt_rap_fin": "2222-02-02",
            }
        )
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": 1,
                "dip_des_it": "Matematica e Informatica",
                "dip_des_eng": "Math and Computer Science",
            }
        )
        tipo_contatto = PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "EMAIL",
                "descr_contatto": "Posta Elettronica",
            }
        )
        tipo_contatto_phone = PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Ufficio",
                "descr_contatto": "Telefono Ufficio",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Riferimento Ufficio",
                "descr_contatto": "Riferimento Ufficio",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "POSTA ELETTRONICA CERTIFICATA",
                "descr_contatto": "POSTA ELETTRONICA CERTIFICATA",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Posta Elettronica Privata",
                "descr_contatto": "Posta Elettronica Privata",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Fax",
                "descr_contatto": "Fax",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Residenza",
                "descr_contatto": "Telefono Residenza",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Domicilio",
                "descr_contatto": "Telefono Domicilio",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Cellulare",
                "descr_contatto": "Telefono Cellulare",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Cellulare Ufficio",
                "descr_contatto": "Telefono Cellulare Ufficio",
            }
        )
        # PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
        # 'cod_contatto': 'Telefono Ufficio',
        # 'descr_contatto': 'Telefono Ufficio',
        # })
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "URL Sito WEB Curriculum Vitae",
                "descr_contatto": "URL Sito WEB Curriculum Vitae",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "URL Sito WEB",
                "descr_contatto": "URL Sito WEB",
            }
        )
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Skype",
                "descr_contatto": "Skype",
            }
        )

        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": 1,
                "cod_fis": p1,
                "contatto": "email@email",
                "prg_priorita": 1,
            }
        )
        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": 2,
                "cod_fis": p2,
                "contatto": "email2@email",
                "prg_priorita": 1,
            }
        )
        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto_phone,
                "id_ab": 3,
                "cod_fis": p3,
                "contatto": "999",
                "prg_priorita": 1000,
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "id_ab": 2,
                "ds_funzione": "Amministrazione Rettorato",
                "cod_fis": p2,
            }
        )
        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "cod_fis": p3,
                "termine": "2222-03-26",
                "decorrenza": "1900-01-01",
                "ds_funzione": "Direttore",
                "matricola": "111114",
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "99",
                "denominazione": "Rettorato",
                "cd_tipo_nodo": "AMM",
                "dt_fine_val": "2222-01-01",
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "denominazione": "Dipartimento di Matematica e Informatica",
                "dt_fine_val": "2222-01-01",
            }
        )

        url = reverse("addressbook:apiv1:addressbook-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()["results"]) == 1

        data = {"structure": "99", "lang": "it"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"search": "Ibra", "function": "Direttore"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"search": "Mungar", "structure": "99"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"search": "Mungar", "structure": "99"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"role": "PO"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["Name"] == "Ibra Zlatan"

        data = {"phone": "999"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"phone": "999", "role": "PO", "structuretypes": "DRZ"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"phone": "999", "role": "PO", "structuretypes": "DRZ", "structureid": 3}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"role": "PO", "structuretypes": "DRZ"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"phone": "999", "structuretypes": "DRZ"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"phone": "999", "role": "PO"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"structuretypes": "DRZ"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"structuretree": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"structuretree": "2"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse("addressbook:apiv1:addressbook-list-full")
        res = req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 200


class ApiRolesListUnitTest(TestCase):
    def test_apiroleslist(self):
        req = Client()

        Personale.objects.create(
            **{
                "id": 1,
                "id_ab": 1,
                "matricola": "111112",
                "cd_ruolo": "f",
                "ds_ruolo_locale": "g",
            }
        )
        Personale.objects.create(
            **{
                "id": 2,
                "id_ab": 2,
                "matricola": "111113",
                "cd_ruolo": "g",
                "ds_ruolo_locale": "h",
            }
        )
        Personale.objects.create(
            **{
                "id": 3,
                "id_ab": 3,
                "matricola": "111115",
                "cd_ruolo": "l",
                "ds_ruolo_locale": "o",
            }
        )

        url = reverse("addressbook:apiv1:roles-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["Role"] == "f"
        assert res.json()["results"][1]["RoleDescription"] == "h"
        assert len(res.json()["results"]) == 3


class ApiPersonaleDetailUnitTest(TestCase):
    def test_apipersonaledetail(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
            }
        )

        p1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN1",
                "cv_full_it": "AAA",
                "cv_short_it": "A",
                "cv_full_eng": "BBB",
                "cv_short_eng": "B",
            }
        )
        p2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Lionel",
                "cognome": "Messi",
                "cd_ruolo": "AM",
                "ds_ruolo_locale": "Amministrazione",
                "id_ab": 2,
                "matricola": "111113",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "LNL1",
            }
        )
        Personale.objects.create(
            **{
                "id": 3,
                "nome": "A",
                "cognome": "B",
                "cd_ruolo": "AB",
                "ds_ruolo_locale": "Amministrazione",
                "id_ab": 3,
                "matricola": "111114",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cod_fis": "AB",
            }
        )

        tipo_contatto = PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "EMAIL",
                "descr_contatto": "Posta Elettronica",
            }
        )

        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": 1,
                "cod_fis": p1,
                "prg_priorita": 1,
            }
        )
        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": 2,
                "cod_fis": p2,
                "prg_priorita": 2,
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "id_ab": 1,
                "ds_funzione": "Amministrazione",
                "termine": "2999-12-1",
                "cod_fis": p1,
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "id_ab": 2,
                "ds_funzione": "Delega",
                "termine": None,
                "cod_fis": p2,
            }
        )

        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "URL Sito WEB Curriculum Vitae",
                "descr_contatto": "URL Sito WEB Curriculum Vitae",
            }
        )

        UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "denominazione": "Dipartimento di Matematica e Informatica",
            }
        )

        UnitaOrganizzativa.objects.create(
            **{
                "uo": "99",
                "denominazione": "Dipartimento di Matematica e Informatica",
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "cod_fis": p1,
                "termine": "2222-03-26",
                "decorrenza": "1900-01-01",
                "ds_funzione": "Direttore",
                "matricola": "111112",
            }
        )

        PersonaleAttivoTuttiRuoli.objects.create(
            **{"matricola": "111114", "ds_ruolo": "test"}
        )

        url = reverse(
            "addressbook:apiv1:personale-detail", kwargs={"personaleid": encrypt("111112")}
        )
        url1 = reverse(
            "addressbook:apiv1:personale-detail", kwargs={"personaleid": encrypt("111113")}
        )
        url2 = reverse(
            "addressbook:apiv1:personale-detail", kwargs={"personaleid": encrypt("111114")}
        )

        # check url
        res = req.get(url)
        res1 = req.get(url1)
        res2 = req.get(url2)

        assert res.status_code == 200
        assert res1.status_code == 200
        assert res2.status_code == 200
        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert decrypt(res.json()["results"]["ID"]) == "111112"
        assert decrypt(res1.json()["results"]["ID"]) == "111113"

        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse(
            "addressbook:apiv1:personale-detail", kwargs={"personaleid": encrypt("111112")}
        )
        res = req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 200


class ApiPersonaleFullDetail(TestCase):
    def test_apipersonalefulldetail(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
            }
        )

        Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN1",
                "cv_full_it": "AAA",
                "cv_short_it": "A",
                "cv_full_eng": "BBB",
                "cv_short_eng": "B",
            }
        )

        PersonaleAttivoTuttiRuoli.objects.create(
            **{
                "matricola": "111112",
                "cd_ruolo": "PO",
                "ds_ruolo": "Professore Ordinario",
                "cd_uo_aff_org": u1,
                "ds_aff_org": "Direzione",
                "dt_rap_ini": "2015-01-01",
            }
        )

        url = reverse("addressbook:apiv1:personale-detail-full", kwargs={"personaleid": "111112"})

        # GET
        res = req.get(url)
        assert res.status_code == 401

        # Authenticated request
        usr = get_user_model().objects.create(
            **{"username": "test", "password": "password"}
        )
        token = Token.objects.create(user=usr)

        # Search by id
        url = reverse("addressbook:apiv1:personale-detail-full", kwargs={"personaleid": "111112"})
        res = req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")

        assert res.status_code == 200
        assert res.json()["results"]["Taxpayer_ID"] == "SMN1"
        assert res.json()["results"]["ID"] == "111112"
        assert (
            datetime.datetime(year=2015, month=1, day=1).isoformat()
            == res.json()["results"]["Roles"][0]["Start"]
        )

        # Search by taxpayer_id
        url = reverse("addressbook:apiv1:personale-detail-full", kwargs={"personaleid": "SMN1"})

        res = req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")

        assert res.status_code == 200
        assert res.json()["results"]["Taxpayer_ID"] == "SMN1"
        assert res.json()["results"]["ID"] == "111112"
        assert (
            datetime.datetime(year=2015, month=1, day=1).isoformat()
            == res.json()["results"]["Roles"][0]["Start"]
        )


class ApiAddressbookStructureDetailUnitTest(TestCase):
    def test_apiaddressbookstructuredetail(self):
        req = Client()
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
                "dt_fine_val": "2222-01-01",
            }
        )
        u2 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "ds_tipo_nodo": "direzione",
                "cd_tipo_nodo": "CDS",
                "id_ab": 2,
                "denominazione": "bbb",
                "denominazione_padre": "d",
                "uo_padre": "22",
                "cd_csa": 2,
                "dt_fine_val": "2222-01-01",
            }
        )
        p1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMN1",
            }
        )
        p2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Lionel",
                "cognome": "Messi",
                "cd_ruolo": "AM",
                "ds_ruolo_locale": "Amministrazione",
                "id_ab": 2,
                "matricola": "111113",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "LNL1",
            }
        )

        UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "ds_tipo_nodo": "rettorato",
                "cd_tipo_nodo": "RET",
                "id_ab": 3,
                "denominazione": "ccc",
                "denominazione_padre": "d",
                "uo_padre": "33",
                "cd_csa": 3,
                "dt_fine_val": "2222-01-01",
            }
        )

        tipo_contatto = PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "PEC",
                "descr_contatto": "Posta Elettronica Certificata",
            }
        )

        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "URL Sito WEB Curriculum Vitae",
                "descr_contatto": "URL Sito WEB Curriculum Vitae",
            }
        )

        UnitaOrganizzativaContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "ab": u1,
                "prg_priorita": 1,
            }
        )

        UnitaOrganizzativaContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "ab": u2,
                "prg_priorita": 2,
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "id_ab": 1,
                "ds_funzione": "Amministrazione",
                "termine": "2999-12-1",
                "cod_fis": p1,
                "cd_csa": u1,
            }
        )

        UnitaOrganizzativaFunzioni.objects.create(
            **{
                "id_ab": 2,
                "ds_funzione": "Delega",
                "termine": None,
                "cod_fis": p2,
                "cd_csa": u2,
            }
        )

        url = reverse(
            "addressbook:apiv1:addressbook-structure-detail", kwargs={"structureid": "1"}
        )

        url1 = reverse(
            "addressbook:apiv1:addressbook-structure-detail", kwargs={"structureid": "2"}
        )

        # check url
        res = req.get(url)
        res1 = req.get(url1)

        assert res.status_code == 200
        assert res1.status_code == 200

        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert res.json()["results"]["StructureCod"] == "1"
        assert res1.json()["results"]["StructureCod"] == "2"


class ApiPersonIdUnitTest(TestCase):
    def test_apipersonid(self):
        req = Client()

        Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "ds_aff_org": "aaaa",
            }
        )

        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse("addressbook:apiv1:get-person-id")

        # GET
        res = req.get(url, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 405

        # POST
        res = req.post(url, {"test": "test"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = req.post(url, {"id": "99999"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = req.post(url, {"id": "111112"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 200

        url = reverse("addressbook:apiv1:get-decrypted-person-id")

        # GET
        res = req.get(url, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 405

        # POST
        res = req.post(url, {"test": "test"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = req.post(url, {"id": "99999"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        m_test_encrypted = encrypt("111111")
        res = req.post(
            url, {"id": m_test_encrypted}, HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        assert res.status_code == 200


class ApiPersonnelCfsListUnitTest(TestCase):
    def test_apipersonnelcfslist(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
            }
        )
        u2 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "uo_padre": "2",
            }
        )
        Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "dt_rap_fin": "2023-01-03",
                "ds_aff_org": "aaa",
                "cod_fis": "SMN1",
            }
        )
        Personale.objects.create(
            **{
                "id": 2,
                "nome": "Lionel",
                "cognome": "Messi",
                "cd_ruolo": "AM",
                "ds_ruolo_locale": "Amministrazione",
                "id_ab": 2,
                "matricola": "111113",
                "fl_docente": 0,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "dt_rap_fin": "2023-01-03",
                "ds_aff_org": "bbb",
                "cod_fis": "LNL1",
            }
        )
        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse("addressbook:apiv1:personnel-cfs")

        # GET
        res = req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert len(res.json()["results"]) == 0

        data = {"roles": "PA"}
        res = req.get(url, data=data, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert len(res.json()["results"]) == 0


class ApiSortingContactsUnitTest(TestCase):
    def test_apisortingcontactslist(self):
        req = Client()
        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "uo_padre": "1",
            }
        )
        Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "ds_aff_org": "aaaa",
            }
        )
        Personale.objects.create(
            **{
                "id": 2,
                "nome": "Franco",
                "middle_name": "Luigi",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 2,
                "matricola": "111111",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "ds_aff_org": "bbbb",
            }
        )

        DidatticaCopertura.objects.create(
            **{"personale_id": 1, "cds_cod": "1", "aa_off_id": 2021}
        )
        DidatticaCopertura.objects.create(
            **{
                "personale_id": 2,
                "cds_cod": "1",
                "aa_off_id": datetime.datetime.now().year - 1,
            }
        )

        url = reverse("cds:apiv1:sorting-contacts", kwargs={"cdscod": "1"})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()["results"]) == 1
