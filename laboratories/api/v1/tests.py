from addressbook.models import Personale
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import encrypt
from laboratories.models import (
    LaboratorioAltriDipartimenti,
    LaboratorioAttivita,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioInfrastruttura,
    LaboratorioPersonaleRicerca,
    LaboratorioPersonaleTecnico,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)
from research_lines.models import RicercaErc0, RicercaErc1, RicercaErc2
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest
from structures.models import UnitaOrganizzativa


class ApiLaboratoriesListUnitTest(TestCase):
    def test_apilaboratorieslist(self):
        req = Client()

        dip1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": "1",
                "dip_des_it": "Matematica e Informatica",
                "dip_des_eng": "Math and Computer Science",
            }
        )

        dip2 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 2,
                "dip_cod": "2",
                "dip_des_it": "Matematica e Informatica",
                "dip_des_eng": "Math and Computer Science",
            }
        )

        p1 = Personale.objects.create(
            **{
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "responsabile",
                "id_ab": 1,
                "matricola": "111111",
            }
        )

        p2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Carmine",
                "cognome": "Carlucci",
                "cd_ruolo": "responsabile",
                "id_ab": 2,
                "matricola": "111112",
            }
        )

        lab2 = LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "nome_laboratorio": "Informatica",
                "ambito": "Tecnico",
                "dipartimento_riferimento_nome": "Informatica, demacs",
                "dipartimento_riferimento": dip1,
                "sede_dimensione": "290",
                "responsabile_scientifico": "Mungari Simone",
                "matricola_responsabile_scientifico": p1,
                "laboratorio_interdipartimentale": "SI",
                "visibile": True,
            }
        )

        a1 = LaboratorioTipologiaAttivita.objects.create(
            **{
                "id": 2,
                "descrizione": "ricerca",
            }
        )

        LaboratorioAttivita.objects.create(
            **{
                "id": 2,
                "laboratorio_dati_base": lab2,
                "tipologia_attivita": a1,
            }
        )

        LaboratorioDatiBase.objects.create(
            **{
                "id": 2,
                "nome_laboratorio": "Informatica",
                "ambito": "Scientifico",
                "dipartimento_riferimento_nome": "Matematica, demacs",
                "dipartimento_riferimento": dip2,
                "sede_dimensione": "291",
                "responsabile_scientifico": "Carlucci Carmine",
                "matricola_responsabile_scientifico": p2,
                "visibile": True,
            }
        )

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )

        erc1_1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )

        i1 = LaboratorioInfrastruttura.objects.create(
            **{
                "id": 1,
            }
        )

        LaboratorioPersonaleRicerca.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab2,
                "matricola_personale_ricerca": p2,
            }
        )

        lab1 = LaboratorioDatiBase.objects.create(
            **{
                "id": 3,
                "matricola_referente_compilazione": p1,
                "nome_laboratorio": "LAB2",
                "dipartimento_riferimento": dip2,
                "ambito": "Tecnologico",
                "matricola_responsabile_scientifico": p2,
                "infrastruttura_riferimento": i1,
                "visibile": True,
            }
        )

        a1 = LaboratorioTipologiaAttivita.objects.create(
            **{"id": 1, "descrizione": "aaa"}
        )
        LaboratorioAttivita.objects.create(
            **{"id": 1, "laboratorio_dati_base": lab1, "tipologia_attivita": a1}
        )

        LaboratorioPersonaleTecnico.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "matricola_personale_tecnico": p1,
                "ruolo": "R1",
            }
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 3,
                "laboratorio_dati_base": lab1,
                "ricerca_erc1": erc1_1,
            }
        )

        LaboratorioAltriDipartimenti.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab2,
                "didattica_dipartimento": dip1,
            }
        )

        url = reverse("laboratories:apiv1:laboratories-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {"department": "1", "teacher": encrypt("111111")}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 1
        assert res.json()["results"][0]["ScientificDirector"] == "Mungari Simone"

        data = {"teacher": encrypt("111111")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"scope": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": encrypt("111112")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 3

        data = {"teacher": encrypt("111112"), "scope": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher": encrypt("111111"), "scope": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"department": "2", "area": "Scientifico"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 2
        assert res.json()["results"][0]["ScientificDirector"] == "Carlucci Carmine"

        data = {"area": "Tecnico"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 1
        assert res.json()["results"][0]["Dimension"] == "290"

        data = {"infrastructure": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"area": "Scientifico"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 2
        assert res.json()["results"][0]["Dimension"] == "291"

        data = {"search": "Informatica", "lang": "it"}
        res = req.get(url, data=data)
        data = {"search": "Informatica"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 1
        assert res.json()["results"][0]["Dimension"] == "290"
        assert res.json()["results"][0]["ScientificDirector"] == "Mungari Simone"

        data = {"erc1": "cod1_erc1"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["LaboratoryId"] == 3

        res = req.get(url)
        assert len(res.json()["results"]) == 3


class ApiLaboratoryDetailUnitTest(TestCase):
    def test_apilaboratorydetail(self):
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
        dip1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": 1,
                "dip_des_it": "Matematica e Informatica",
                "dip_des_eng": "Math and Computer Science",
            }
        )
        dip2 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 2,
                "dip_cod": 2,
                "dip_des_it": "Lettere e filosofia",
                "dip_des_eng": "Philosophy",
            }
        )
        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )
        erc1_1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        erc1_2 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc2",
                "descrizione": "Poetica Platone",
                "ricerca_erc0_cod": erc0,
            }
        )

        lab1 = LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "matricola_referente_compilazione": p1,
                "nome_laboratorio": "LAB1",
                "dipartimento_riferimento": dip1,
                "ambito": "Tecnologico",
                "matricola_responsabile_scientifico": p1,
                "laboratorio_interdipartimentale": "SI",
                "visibile": True,
            }
        )

        lab2 = LaboratorioDatiBase.objects.create(
            **{
                "id": 2,
                "matricola_referente_compilazione": p2,
                "nome_laboratorio": "LAB2",
                "dipartimento_riferimento": dip2,
                "ambito": "Umanistico",
                "matricola_responsabile_scientifico": p2,
                "visibile": True,
            }
        )
        a1 = LaboratorioTipologiaAttivita.objects.create(
            **{"id": 1, "descrizione": "aaa"}
        )
        LaboratorioAttivita.objects.create(
            **{"id": 1, "laboratorio_dati_base": lab1, "tipologia_attivita": a1}
        )
        LaboratorioAttivita.objects.create(
            **{"id": 2, "laboratorio_dati_base": lab1, "tipologia_attivita": a1}
        )
        LaboratorioAttivita.objects.create(
            **{"id": 3, "laboratorio_dati_base": lab2, "tipologia_attivita": a1}
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "ricerca_erc1": erc1_1,
            }
        )
        LaboratorioDatiErc1.objects.create(
            **{
                "id": 2,
                "laboratorio_dati_base": lab2,
                "ricerca_erc1": erc1_2,
            }
        )

        LaboratorioPersonaleRicerca.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "matricola_personale_ricerca": p2,
            }
        )
        LaboratorioPersonaleRicerca.objects.create(
            **{
                "id": 2,
                "laboratorio_dati_base": lab1,
                "matricola_personale_ricerca": p2,
            }
        )
        LaboratorioPersonaleRicerca.objects.create(
            **{
                "id": 3,
                "laboratorio_dati_base": lab2,
                "matricola_personale_ricerca": p1,
            }
        )
        LaboratorioPersonaleRicerca.objects.create(
            **{
                "id": 4,
                "laboratorio_dati_base": lab2,
                "matricola_personale_ricerca": p1,
            }
        )

        LaboratorioPersonaleTecnico.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "matricola_personale_tecnico": p1,
                "ruolo": "R1",
            }
        )
        LaboratorioPersonaleTecnico.objects.create(
            **{
                "id": 2,
                "laboratorio_dati_base": lab1,
                "matricola_personale_tecnico": p1,
                "ruolo": "R2",
            }
        )
        LaboratorioPersonaleTecnico.objects.create(
            **{
                "id": 3,
                "laboratorio_dati_base": lab2,
                "matricola_personale_tecnico": p2,
                "ruolo": "R1",
            }
        )
        LaboratorioPersonaleTecnico.objects.create(
            **{
                "id": 4,
                "laboratorio_dati_base": lab2,
                "matricola_personale_tecnico": p2,
                "ruolo": "R2",
            }
        )

        LaboratorioServiziOfferti.objects.create(
            **{"id": 1, "laboratorio_dati_base": lab1, "nome_servizio": "S1"}
        )
        LaboratorioServiziOfferti.objects.create(
            **{"id": 2, "laboratorio_dati_base": lab2, "nome_servizio": "S2"}
        )

        LaboratorioUbicazione.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "edificio": "31B",
                "piano": "1",
            }
        )

        LaboratorioAltriDipartimenti.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": lab1,
                "didattica_dipartimento": dip2,
            }
        )

        url = reverse(
            "laboratories:apiv1:laboratory-detail", kwargs={"laboratoryid": "1"}
        )

        url1 = reverse(
            "laboratories:apiv1:laboratory-detail", kwargs={"laboratoryid": "2"}
        )

        # check url
        res = req.get(url)
        res1 = req.get(url1)

        assert res.status_code == 200
        assert res1.status_code == 200

        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert res.json()["results"]["LaboratoryId"] == 1
        assert res1.json()["results"]["LaboratoryId"] == 2

        assert (
            res.json()["results"]["DepartmentReferentName"]
            == "Math and Computer Science"
        )
        assert res1.json()["results"]["LaboratoryScope"] == "Umanistico"

        assert len(res.json()["results"]["LaboratoryResearchPersonnel"]) == 2
        assert len(res1.json()["results"]["LaboratoryTechPersonnel"]) == 2


class ApiLaboratoriesAreasListUnitTest(TestCase):
    def test_apiLaboratoriesAreasList(self):
        req = Client()

        LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "nome_laboratorio": "LAB1",
                "ambito": "Tecnologico",
            }
        )

        LaboratorioDatiBase.objects.create(
            **{
                "id": 2,
                "nome_laboratorio": "LAB2",
                "ambito": "Umanistico",
            }
        )

        url = reverse("laboratories:apiv1:laboratories-areas")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()["results"]) == 2


class ApiErc1ListUnitTest(TestCase):
    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )
        erc1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        l1 = LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "nome_laboratorio": "Informatica",
                "ambito": "Tecnico",
                "dipartimento_riferimento_nome": "Informatica",
                "sede_dimensione": "290",
                "responsabile_scientifico": "Mungari Simone",
            }
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": l1,
                "ricerca_erc1": erc1,
            }
        )

        url = reverse("laboratories:apiv1:erc1-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {"laboratory": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        assert len(res.json()["results"]) == 1


class ApiErc2ListUnitTest(TestCase):
    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )
        erc1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )
        l1 = LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "nome_laboratorio": "Informatica",
                "ambito": "Tecnico",
                "dipartimento_riferimento_nome": "Informatica",
                "sede_dimensione": "290",
                "responsabile_scientifico": "Mungari Simone",
            }
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": l1,
                "ricerca_erc1": erc1,
            }
        )
        RicercaErc2.objects.create(
            **{
                "cod_erc2": "cod_erc2",
                "descrizione": "Sicurezza Informatica",
                "ricerca_erc1": erc1,
            }
        )
        url = reverse("laboratories:apiv1:erc2-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {"laboratory": "1"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        assert len(res.json()["results"]) == 1


class ApiErc0ListUnitTest(TestCase):
    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )

        erc01 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "112",
                "description": "ITA",
                "description_en": "ITA",
            }
        )

        erc1 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )

        l1 = LaboratorioDatiBase.objects.create(
            **{
                "id": 1,
                "nome_laboratorio": "Informatica",
                "ambito": "Tecnico",
                "dipartimento_riferimento_nome": "Informatica",
                "sede_dimensione": "290",
                "responsabile_scientifico": "Mungari Simone",
            }
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 1,
                "laboratorio_dati_base": l1,
                "ricerca_erc1": erc1,
            }
        )

        erc12 = RicercaErc1.objects.create(
            **{
                "cod_erc1": "cod1_erc12",
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc01,
            }
        )

        l2 = LaboratorioDatiBase.objects.create(
            **{
                "id": 2,
                "nome_laboratorio": "Informatica",
                "ambito": "Tecnico",
                "dipartimento_riferimento_nome": "Informatica",
                "sede_dimensione": "291",
                "responsabile_scientifico": "Mungari Simone",
            }
        )

        LaboratorioDatiErc1.objects.create(
            **{
                "id": 2,
                "laboratorio_dati_base": l2,
                "ricerca_erc1": erc12,
            }
        )

        url = reverse("laboratories:apiv1:erc0-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert res.json()["results"][0]["IdErc0"] == "111"

        assert len(res.json()["results"]) == 2


class ApiInfrastructuresListUnitTest(TestCase):
    def test_apiinfrastrucureslist(self):
        req = Client()

        LaboratorioInfrastruttura.objects.create(**{"id": 1, "descrizione": "SILA"})

        url = reverse("laboratories:apiv1:infrastructures")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()["results"]) == 1


class ApiLaboratoriesScopesListUnitTest(TestCase):
    def test_apilaboratoriesscopeslist(self):
        req = Client()

        LaboratorioTipologiaAttivita.objects.create(
            **{"id": 1, "descrizione": "Ricerca"}
        )

        url = reverse("laboratories:apiv1:laboratories-scopes")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()["results"]) == 1
