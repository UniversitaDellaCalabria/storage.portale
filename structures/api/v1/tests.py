import datetime

from addressbook.models import Personale, PersonaleUoTipoContatto
from django.test import Client, TestCase
from django.urls import reverse
from phd.models import DidatticaDottoratoAttivitaFormativa
from projects.models import ProgettoAmbitoTerritoriale
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest
from structures.models import (
    UnitaOrganizzativa,
    UnitaOrganizzativaContatti,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaTipoFunzioni,
)


class ApiDepartmentsListUnitTest(TestCase):
    def test_apidepartmentslist(self):
        req = Client()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": "001",
                "dip_des_it": "Dipartimento di Matematica e Informatica",
                "dip_des_eng": "Department of Math and Computer Science",
                "dip_nome_breve": "DEMACS",
            }
        )
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 2,
                "dip_cod": "002",
                "dip_des_it": "Dipartimento di Letteratura",
                "dip_des_eng": "Department of Literature",
                "dip_nome_breve": "LIT",
            }
        )

        url = reverse("structures:apiv1:departments-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["DepartmentName"] == "Department of Literature"

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"][0]["DepartmentName"] == "Dipartimento di Letteratura"
        )


class ApiDepartmentDetailUnitTest(TestCase):
    def test_apidepartmentdetail(self):
        req = Client()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": "001",
                "dip_des_it": "Dipartimento di Matematica e Informatica",
                "dip_des_eng": "Department of Math and Computer Science",
                "dip_nome_breve": "DEMACS",
            }
        )
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 2,
                "dip_cod": "002",
                "dip_des_it": "Dipartimento di Letteratura",
                "dip_des_eng": "Department of Literature",
                "dip_nome_breve": "LIT",
            }
        )

        url = reverse("structures:apiv1:department-detail", kwargs={"departmentcod": "001"})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert (
            res.json()["results"]["DepartmentName"]
            == "Department of Math and Computer Science"
        )

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"]["DepartmentName"]
            == "Dipartimento di Matematica e Informatica"
        )


class ApiStructuresListUnitTest(TestCase):
    def test_apistructureslist(self):
        req = Client()

        UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "ds_tipo_nodo": "rettorato",
                "cd_tipo_nodo": "RET",
                "denominazione": "RETTORATO",
                "uo_padre": "1",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "ds_tipo_nodo": "direzione",
                "cd_tipo_nodo": "DIR",
                "denominazione": "DIREZIONE",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "ds_tipo_nodo": "uffici",
                "cd_tipo_nodo": "UFF",
                "denominazione": "UFFICI",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )

        url = reverse("structures:apiv1:structures-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        assert res.status_code == 200

        # GET

        res = req.get(url)

        data = {"father": "None"}
        res = req.get(url, data=data)

        assert res.json()["results"][1]["StructureTypeName"] == "uffici"
        assert res.json()["results"][0]["StructureCod"] == "2"
        assert len(res.json()["results"]) == 2

        data = {"search": "Direzione"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["StructureCod"] == "2"

        data = {"type": "DIR,UFF"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"type": "DIR,UFF", "search": "Direzione"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"father": "1", "depth": "1"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["StructureCod"] == "1"


class ApiStructuresTypesUnitTest(TestCase):
    def test_apistructurestypes(self):
        req = Client()

        UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "ds_tipo_nodo": "facolta",
                "cd_tipo_nodo": "000",
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "ds_tipo_nodo": "direzione",
                "cd_tipo_nodo": "CDS",
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "uo_padre": "1",
                "ds_tipo_nodo": "rettorato",
                "cd_tipo_nodo": "RET",
            }
        )

        url = reverse("structures:apiv1:structure-types")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["StructureTypeName"] == "facolta"
        assert res.json()["results"][1]["StructureTypeCOD"] == "CDS"
        assert len(res.json()["results"]) == 3

        data = {"father": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiAllStructuresListUnitTest(TestCase):
    def test_apiallstructureslist(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "ds_tipo_nodo": "rettorato",
                "cd_tipo_nodo": "RET",
                "denominazione": "RETTORATO",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "ds_tipo_nodo": "direzione",
                "cd_tipo_nodo": "DIR",
                "denominazione": "DIREZIONE",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )
        UnitaOrganizzativa.objects.create(
            **{
                "uo": "3",
                "ds_tipo_nodo": "uffici",
                "cd_tipo_nodo": "UFF",
                "denominazione": "UFFICI",
                "dt_fine_val": datetime.datetime.today() + datetime.timedelta(days=1),
            }
        )
        Personale.objects.create(
            **{
                "id": 1,
                "nome": "Franco",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 1,
                "matricola": "111111",
                "cd_uo_aff_org": u1,
            }
        )

        url = reverse("addressbook:apiv1:all-structures-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 0

        data = {"search": "Direzione"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"type": "DIR,UFF"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"father": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"father": "None"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0


class ApiRefStructuresListUnitTest(TestCase):
    def test_apirefstructureslist(self):
        req = Client()

        DidatticaDottoratoAttivitaFormativa.objects.create(
            **{
                "id": 1,
                "nome_af": "AAAA",
                "struttura_proponente_origine": "dimes",
                "rif_dottorato": "matematica",
                "ciclo": 1,
            }
        )

        url = reverse("phd:apiv1:ref-structures")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiTerritorialScopesListUnitTest(TestCase):
    def test_apiterritorialscopeslist(self):
        req = Client()

        ProgettoAmbitoTerritoriale.objects.create(
            **{
                "id": 1,
                "ambito_territoriale": "aaa",
            }
        )

        url = reverse("projects:apiv1:projects-territorial-scopes")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiStructureDetailUnitTest(TestCase):
    def test_apistructuredetail(self):
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
                "cd_csa": "1",
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
                "cd_csa": "2",
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
                "id_ab": u1,
                "prg_priorita": 1,
            }
        )

        UnitaOrganizzativaContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": u2,
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

        url = reverse("structures:apiv1:structure-detail", kwargs={"structureid": "1"})

        url1 = reverse("structures:apiv1:structure-detail", kwargs={"structureid": "2"})

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


class ApiStructureFunctionsListUnitTest(TestCase):
    def test_apistructurefunctionslist(self):
        req = Client()

        UnitaOrganizzativaTipoFunzioni.objects.create(
            **{
                "cd_tipo_nod": "apl",
                "funzione": "nbb45",
                "descr_funzione": "aaa",
            }
        )

        url = reverse("structures:apiv1:functions")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1
