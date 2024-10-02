from addressbook.models import Personale
from cds.models import (
    DidatticaAmbiti,
    DidatticaAttivitaFormativaModalita,
    DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio,
    DidatticaCopertura,
    DidatticaCoperturaDettaglioOre,
    DidatticaPianoRegolamento,
    DidatticaPianoSceltaAf,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSceltaVincoli,
    DidatticaPianoSche,
    DidatticaTestiAf,
)
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import encrypt

from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest

from .util_tests import (
    DidatticaAttivitaFormativaUnitTest,
    DidatticaCdsLinguaUnitTest,
    DidatticaCdsUnitTest,
    DidatticaPdsRegolamentoUnitTest,
    DidatticaRegolamentoUnitTest,
    DidatticaTestiRegolamentoUnitTest,
)


class ApiCdSListUnitTest(TestCase):
    def test_apicdslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "tipo_corso_cod": "L",
                "area_cds": "scienze",
                "cds_id": 1,
            }
        )
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(
            **{
                "cdsord": didatticaCds,
                "iso6392_cod": "ita",
            }
        )
        r1 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 1,
                "stato_regdid_cod": "A",
                "titolo_congiunto_cod": "N",
                "cds_id": 1,
            }
        )

        DidatticaCdsAltriDatiUfficio.objects.create(
            **{
                "cds_id": 1,
                "edificio": 2,
                "ordine": 1,
            }
        )

        DidatticaCdsAltriDati.objects.create(
            **{"regdid_id": r1, "nome_origine_coordinatore": "Test coordinatore"}
        )

        r1.get_ordinamento_didattico()

        url = reverse("cds:apiv1:cds-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: lang
        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: lang
        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: coursetype
        data = {"coursetype": "L"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: courseclasscod
        data = {"courseclasscod": "1"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: area
        data = {"area": "scienze"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: courseclassname
        data = {"courseclassname": "laurea in informatica"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: departmentcod
        data = {"departmentcod": 1}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: departmentname
        data = {"departmentname": "matematica e informatica", "lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: academicyear
        data = {"academicyear": 2020}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: jointdegree
        data = {"jointdegree": "N"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: cdslanguage
        data = {"cdslanguage": "ita", "lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: search ita
        data = {"search": "informatica", "lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: search eng
        data = {"search": "computer", "lang": "en"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1

        # param: search eng wrong
        data = {"search": "math", "lang": "en"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        # param: all
        data = {
            "cdslanguage": "ita",
            "jointdegree": "N",
            "academicyear": 2020,
            "departmentname": "math and computer science",
            "departmentcod": 1,
            "courseclassname": "laurea in informatica",
            "courseclasscod": "1",
            "coursetype": "L",
            "lang": "en",
        }
        res = req.get(url, data=data)
        assert res.json()["results"][0]["RegDidId"] == 1


class ApiCdSInfoUnitTest(TestCase):
    def test_apicdsinfo(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "area_cds": "Scienze",
            }
        )
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(
            **{
                "cdsord": didatticaCds,
            }
        )
        reg = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 1,
                "stato_regdid_cod": "A",
                "titolo_congiunto_cod": "N",
                "cds": didatticaCds,
                "modalita_erogazione": "Convenzionale",
            }
        )
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
            **{
                "txt_id": 1,
                "regdid": reg,
                "tipo_testo_regdid_cod": "DESC_COR_BRE",
            }
        )
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
            **{
                "txt_id": 3,
                "regdid": reg,
                "tipo_testo_regdid_cod": "URL_CDS_VIDEO",
                "clob_txt_ita": "https:....",
            }
        )
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
            **{
                "txt_id": 2,
                "regdid": reg,
                "tipo_testo_regdid_cod": "FUNZIONI",
                "profilo": "profiloprova",
                "clob_txt_ita": "provadescrizione",
            }
        )
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
            **{
                "txt_id": 4,
                "regdid": reg,
                "tipo_testo_regdid_cod": "URL_CDS_VIDEO",
                "clob_txt_ita": "pdf",
            }
        )

        url = reverse("cds:apiv1:cds-info", kwargs={"regdidid": 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: lang
        url = reverse("cds:apiv1:cds-info", kwargs={"regdidid": 1})

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"]["RegDidId"] == 1

        # param: cdsid 10 doesn't exist
        url = reverse("cds:apiv1:cds-info", kwargs={"regdidid": 10})
        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        # param: lang
        url = reverse("cds:apiv1:cds-info", kwargs={"regdidid": 1})
        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert res.json()["results"]["RegDidId"] == 1

        # param: lang
        url = reverse("cds:apiv1:cds-info", kwargs={"regdidid": 1})
        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"]["CdSProfiles"]["profiloprova"]["FUNZIONI"]
            == "provadescrizione"
        )


class ApiCdSStudyPlansUnitTest(TestCase):
    def test_apicdsstudyplans(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "durata_anni": 3,
            }
        )
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "cds": cds,
            }
        )
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "regdid": regdid,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "pds_regdid": pds,
                "regdid": regdid,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "af_id": 1,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )

        url = reverse("cds:apiv1:cds-studyplans", kwargs={"regdidid": 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["RegDidId"] == 1

        # lang it

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"][0]["StudyActivities"]["1"][0]["StudyActivityName"]
            == "matematica"
        )

        # lang eng
        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"][0]["StudyActivities"]["1"][0]["StudyActivityName"]
            == "math"
        )


class ApiStudyPlanDetailUnitTest(TestCase):
    def test_apicdsstudyplans(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "durata_anni": 3,
            }
        )
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "cds": cds,
            }
        )
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "regdid": regdid,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "pds_regdid": pds,
                "regdid": regdid,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "af_id": 1,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )

        url = reverse(
            "cds:apiv1:studyplan-detail", kwargs={"regdidid": 1, "studyplanid": 1}
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["RegDidId"] == 1

        # lang it

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"]["StudyActivities"]["1"][0]["StudyActivityName"]
            == "matematica"
        )

        # lang eng
        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"]["StudyActivities"]["1"][0]["StudyActivityName"]
            == "math"
        )


class ApiStudyPlanActivitiesUnitTest(TestCase):
    def test_apistudyplanactivities(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds1 = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "pds_regdid_id": 1,
                "regdid": regdid,
            }
        )
        pds2 = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "pds_regdid_id": 2,
                "regdid": regdid,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "pds_regdid": pds1,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "pds_regdid": pds1,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "af_radice_id": 2,
                "anno_corso": 1,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 3,
                "pds_regdid": pds1,
                "des": "informatica modulo 1",
                "af_gen_des_eng": "computer science modulo 1",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "af_radice_id": 2,
                "anno_corso": 1,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 4,
                "pds_regdid": pds2,
                "des": "matematica2",
                "af_gen_des_eng": "math2",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 4,
                "anno_corso": 1,
            }
        )

        url = reverse(
            "cds:apiv1:studyplan-activities", kwargs={"regdidid": 1, "studyplanid": 1}
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["StudyActivityID"] == 1

        # 3 courses : 2 main courses, 1 module course, should return 2 courses
        res = req.get(url)
        assert len(res.json()["results"]) == 2

        # lang it first semester
        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["StudyActivityName"] == "matematica"

        # lang eng first semester
        data = {"lang": "eng"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["StudyActivityName"] == "math"

        # lang it second semester
        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][1]["StudyActivityName"] == "informatica"

        # lang eng second semester
        data = {"lang": "eng"}
        res = req.get(url, data=data)
        assert res.json()["results"][1]["StudyActivityName"] == "computer science"

        url = reverse(
            "cds:apiv1:studyplan-activities", kwargs={"regdidid": 1, "studyplanid": 2}
        )
        res = req.get(url)
        assert res.json()["results"][0]["StudyActivityID"] == 4


class ApiStudyActivityInfoUnitTest(TestCase):
    def test_apistudyactivityinfo(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "pds_regdid_id": 1,
                "regdid": regdid,
            }
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
        course = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "pds_regdid": pds,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "anno_corso": 2,
                "af_radice_id": 1,
                "matricola_resp_did": p1,
                "mutuata_flg": 1,
                "af_master_id": 2,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "pds_regdid": pds,
                "des": "informatica modulo 1",
                "af_gen_des_eng": "computer science modulo 1",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "anno_corso": 1,
                "af_radice_id": 1,
                "mutuata_flg": 0,
                "af_master_id": 2,
            }
        )
        DidatticaTestiAf.objects.create(
            **{
                "tipo_testo_af_cod": "CONTENUTI",
                "testo_af_ita": "Variabili",
                "testo_af_eng": "Variables",
                "af": course,
            }
        )

        DidatticaCopertura.objects.create(
            **{
                "af": course,
                "personale": p1,
            }
        )

        url = reverse(
            "cds:apiv1:studyactivity-info",
            kwargs={"regdidid": 1, "studyplanid": 1, "studyactivityid": 1},
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["StudyActivityID"] == 1

        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert res.json()["results"]["StudyActivityContent"] == "Variables"

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"]["StudyActivityContent"] == "Variabili"

        url = reverse(
            "cds:apiv1:studyactivity-info",
            kwargs={"regdidid": 1, "studyplanid": 1, "studyactivityid": 2},
        )
        res = req.get(url)
        assert res.json()["results"]["StudyActivityID"] == 2


class ApiAllStudyActivitiesListUnitTest(TestCase):
    def test_apiallstudyactivitieslist(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
                "dip_cod": "aaaa",
                "dip_des_it": "storia",
                "dip_des_eng": "history",
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "cds_id": 1,
                "cds_cod": "aaa",
                "nome_cds_it": "Matematica",
                "nome_cds_eng": "Math",
                "dip_id": 1,
            }
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

        DidatticaCopertura.objects.create(**{"af_id": 1, "personale_id": 1})

        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "anno_corso": 1,
                "af_radice_id": 1,
                "matricola_resp_did": p1,
                "mutuata_flg": 1,
                "af_master_id": 2,
                "sett_cod": "INF/01",
                "sett_des": "Interdisciplinare",
                "cds_id": 1,
                "aa_off_id": 2015,
            }
        )

        # p = Personale.objects.create(**{
        #     'id': 1,
        #     'nome': 'Franco',
        #     'cognome': 'Garofalo',
        #     'cd_ruolo': 'PO',
        #     'id_ab': 1,
        #     'matricola': '111111',
        # })

        url = reverse("cds:apiv1:activities")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1

        data = {"department": "aaaa"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teaching": "informatica"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"teacher": "Garofalo"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"cds_cod": "aaa"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"teacher_code": encrypt("111111")}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"cds": "Matematica"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"ssd": "INF"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"period": "Primo semestre"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"course_year": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"academic_year": 2015}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiStudyActivityDetailUnitTest(TestCase):
    def test_apistudyactivityinfo(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{
                "pds_regdid_id": 1,
                "regdid": regdid,
            }
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
        course = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "pds_regdid": pds,
                "anno_corso": 1,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "matricola_resp_did": p1,
                "mutuata_flg": 1,
                "af_master_id": 2,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "pds_regdid": pds,
                "des": "informatica modulo 1",
                "af_gen_des_eng": "computer science modulo 1",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "anno_corso": 2,
                "af_radice_id": 1,
                "af_pdr_id": 1,
                "fat_part_stu_cod": "GRP",
                "fat_part_stu_des": "des",
                "mutuata_flg": 0,
                "af_master_id": 2,
            }
        )
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 3,
                "pds_regdid": pds,
                "des": "informatica modulo 2",
                "af_gen_des_eng": "computer science modulo 1",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "af_pdr_id": 2,
                "fat_part_stu_cod": "GRP",
                "fat_part_stu_des": "des",
                "mutuata_flg": 0,
                "af_master_id": 2,
            }
        )
        DidatticaTestiAf.objects.create(
            **{
                "tipo_testo_af_cod": "CONTENUTI",
                "testo_af_ita": "Variabili",
                "testo_af_eng": "Variables",
                "af": course,
            }
        )

        # p1 = Personale.objects.create(**{
        #     'id': 1,
        #     'nome': 'Franco',
        #     'cognome': 'Garofalo',
        #     'cd_ruolo': 'PO',
        #     'id_ab': 1,
        #     'matricola': '111111',
        # })
        DidatticaCopertura.objects.create(
            **{
                "coper_id": 1,
                "af": course,
                "personale": p1,
            }
        )

        DidatticaAttivitaFormativaModalita.objects.create(
            **{
                "mod_did_af_id": 1,
                "af_id": 1,
                "mod_did_cod": "c",
                "mod_did_des": "convenzionale",
            }
        )

        DidatticaCoperturaDettaglioOre.objects.create(
            **{
                "tipo_att_did_cod": 444,
                "coper_id": 1,
                "ore": 3,
            }
        )

        url = reverse("cds:apiv1:studyactivity-detail", kwargs={"studyactivityid": 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["StudyActivityID"] == 1

        data = {"lang": "en"}
        res = req.get(url, data=data)
        assert res.json()["results"]["StudyActivityContent"] == "Variables"

        data = {"lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"]["StudyActivityContent"] == "Variabili"

        url = reverse("cds:apiv1:studyactivity-detail", kwargs={"studyactivityid": 2})
        res = req.get(url)
        assert res.json()["results"]["StudyActivityID"] == 2


class ApiAcademicYearsUnitTest(TestCase):
    def test_apiacademicyears(self):
        req = Client()

        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 1,
                "aa_reg_did": 2015,
            }
        )
        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 2,
                "aa_reg_did": 2016,
            }
        )
        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 3,
                "aa_reg_did": 2017,
            }
        )

        url = reverse("cds:apiv1:academic-years")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert res.json()["results"][1]["AcademicYear"] == 2016
        assert len(res.json()["results"]) == 3


class ApiDegreeTypesListUnitTest(TestCase):
    def test_apidegreetypeslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "cds_id": 1,
                "tipo_corso_cod": "L",
                "tipo_corso_des": "Laurea",
                "cdsord_id": 1,
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "cds_id": 2,
                "tipo_corso_cod": "LM5",
                "tipo_corso_des": "Laurea magistrale ciclo unico",
                "cdsord_id": 2,
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "cds_id": 3,
                "tipo_corso_cod": "LM",
                "tipo_corso_des": "Laurea Magistrale",
                "cdsord_id": 3,
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": dip,
                "cds_id": 4,
                "tipo_corso_cod": "L",
                "tipo_corso_des": "Laurea",
                "cdsord_id": 4,
            }
        )

        url = reverse("cds:apiv1:degree-types")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["CourseType"] == "L"
        assert len(res.json()["results"]) == 3


class ApiCdsAreasListUnitTest(TestCase):
    def test_apicdsareaslist(self):
        req = Client()

        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "area_cds": "aaa",
            }
        )
        DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "cds_id": 2,
                "cdsord_id": 3,
                "area_cds": None,
            }
        )

        url = reverse("cds:apiv1:cds-areas")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiSitoWebCdsStudyPlansListUnitTest(TestCase):
    def test_apisitiwebcdsstudyplans(self):
        req = Client()

        cds1 = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "tipo_corso_cod": "L",
                "area_cds": "scienze",
                "cds_id": 1,
                "cds_cod": "1",
            }
        )

        r1 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 1,
                "stato_regdid_cod": "A",
                "titolo_congiunto_cod": "N",
                "cds_id": 1,
                "aa_reg_did": 2022,
            }
        )

        dpr1 = DidatticaPianoRegolamento.objects.create(
            **{
                "regpiani_id": 1,
                "regdid_id": 1,
                "aa_coorte_id": 2022,
                "aa_regpiani_id": 2022,
                "des": "prova",
                "def_flg": 1,
                "stato_cod": "A",
                "stato_des": "A",
                "regpiani_pdr_id": 1,
                "regpiani_pdr_cod": "test",
                "regpiani_pdr_des": "test",
                "flg_exp_seg_stu": 1,
            }
        )

        dps1 = DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 1,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )

        dps2 = DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 2,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )

        dps3 = DidatticaPianoSche.objects.create(
            **{
                "sche_piano_id": 3,
                "sche_piano_des": "prova",
                "sche_piano_cod": "test",
                "regpiani_id": 1,
                "pds_cod": "GEN",
                "pds_des": "Generico",
                "comune_flg": 1,
            }
        )
        dpsv1 = DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 1,
            }
        )
        dpsv2 = DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 2,
            }
        )
        dpsv3 = DidatticaPianoSceltaVincoli.objects.create(
            **{
                "sce_id": 3,
            }
        )
        dpssp1 = DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 1,
                "sche_piano_id": 1,
                "tipo_sce_cod": "O",
                "apt_slot_ord_num": 5,
            }
        )

        af1 = DidatticaPianoSceltaAf.objects.create(
            **{
                "sce_id": 1,
                "anno_corso_af": 2022,
                "ciclo_des": "Prova",
                "af_gen_des": "Prova",
                "af_id": 1,
                "tipo_af_des_af": "Contenuto",
                "ambito_des_af": "Test",
                "sett_cod": "Content",
                "peso": 6,
            }
        )

        af2 = DidatticaPianoSceltaAf.objects.create(
            **{
                "sce_id": 2,
                "anno_corso_af": 2022,
                "ciclo_des": "Prova",
                "af_gen_des": "Prova",
                "af_id": 1,
                "tipo_af_des_af": "Contenuto",
                "ambito_des_af": "Test",
                "sett_cod": "Content",
                "peso": 6,
            }
        )

        af3 = DidatticaPianoSceltaAf.objects.create(
            **{
                "sce_id": 3,
                "anno_corso_af": 2022,
                "ciclo_des": "Prova",
                "af_gen_des": "Prova",
                "af_id": 2,
                "tipo_af_des_af": "Contenuto",
                "ambito_des_af": "Test",
                "sett_cod": "Content",
                "peso": 6,
            }
        )

        da1 = DidatticaAmbiti.objects.create(**{"amb_id": 1})

        dpssp2 = DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 2,
                "sche_piano_id": 2,
                "amb_id": 1,
                "ambito_des": "Prova",
                "min_unt": 1,
                "max_unt": 2,
                "sce_des": "Content",
                "apt_slot_ord_num": 1,
                "tipo_sce_cod": "Pr",
                "tipo_sce_des": "Prova",
                "tipo_regsce_cod": "P",
                "tipo_regsce_des": "Prova",
                "tipo_um_regsce_cod": "P",
                "vin_sce_des": 1,
                "vin_id": 1,
            }
        )

        dpssp3 = DidatticaPianoSceltaSchePiano.objects.create(
            **{
                "sce_id": 3,
                "sche_piano_id": 3,
                "ambito_des": "Prova",
                "min_unt": 1,
                "max_unt": 2,
                "sce_des": "Content",
                "apt_slot_ord_num": 1,
                "tipo_sce_cod": "Pr",
                "tipo_sce_des": "Prova",
                "tipo_regsce_cod": "P",
                "tipo_regsce_des": "Prova",
                "tipo_um_regsce_cod": "P",
                "amb_id_af_regsce": 1,
            }
        )

        daf1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "amb_id": 1,
                "af_gen_id": 1,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        daf2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "amb_id": 2,
                "af_gen_id": 2,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        daf2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 3,
                "amb_id": 3,
                "af_gen_id": 3,
                "af_gen_cod": "AAA",
                "des": "Prova",
                "af_gen_des_eng": "Test",
                "anno_corso": 1,
                "sett_cod": "Sem",
                "sett_des": "Semestere",
                "peso": 6,
                "fat_part_stu_cod": "AA",
            }
        )

        url = reverse("cds:apiv1:cds-websites-studyplans-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 0

        data = {"cds_cod": "1", "year": 2022}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1
