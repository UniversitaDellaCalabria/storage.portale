import datetime

from addressbook.models import Personale, PersonaleContatti, PersonaleUoTipoContatto
from cds.api.v1.util_tests import (
    DidatticaAttivitaFormativaUnitTest,
    DidatticaRegolamentoUnitTest,
)
from cds.models import DidatticaCopertura
from django.test import Client, TestCase
from django.urls import reverse
from generics.utils import decrypt, encrypt
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
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest
from structures.models import UnitaOrganizzativa, UnitaOrganizzativaFunzioni
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaAltriDati,
    DocentePtaBacheca,
    PubblicazioneAutori,
    PubblicazioneCollection,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)


class ApiTeacherResearchLinesUnitTest(TestCase):
    def test_apiteacherresearchlinesunittest(self):
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
            }
        )
        doc2 = Personale.objects.create(
            **{
                "id": 2,
                "nome": "Franco",
                "middle_name": "Luigi",
                "cognome": "Garofalo",
                "cd_ruolo": "PO",
                "id_ab": 2,
                "matricola": "111111",
                "fl_docente": 1,
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
                "visibile": 1,
            }
        )

        linea_base2 = RicercaLineaBase.objects.create(
            **{
                "id": 7,
                "ricerca_erc2": erc2,
                "descrizione": "regressione lineare",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 20201",
                "visibile": 1,
            }
        )

        RicercaDocenteLineaBase.objects.create(
            **{"personale": doc1, "ricerca_linea_base": linea_base}
        )
        RicercaDocenteLineaBase.objects.create(
            **{"personale": doc2, "ricerca_linea_base": linea_base2}
        )
        RicercaDocenteLineaBase.objects.create(
            **{
                "personale": doc2,
                "ricerca_linea_base": linea_base,
                "dt_fine": "2021-01-03",
            }
        )
        RicercaDocenteLineaBase.objects.create(
            **{
                "personale": doc2,
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
                "visibile": 1,
            }
        )
        linea_applicata2 = RicercaLineaApplicata.objects.create(
            **{
                "id": 2,
                "ricerca_aster2": aster2,
                "descrizione": "random forest",
                "descr_pubblicaz_prog_brevetto": "pubblicazione 2019",
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
        RicercaDocenteLineaApplicata.objects.create(
            **{
                "personale": doc1,
                "ricerca_linea_applicata": linea_applicata2,
                "dt_ins": "2021-01-03 15:47:21",
            }
        )
        RicercaDocenteLineaApplicata.objects.create(
            **{
                "personale": doc2,
                "ricerca_linea_applicata": linea_applicata,
                "dt_ins": "2021-01-03 15:47:21",
            }
        )
        RicercaDocenteLineaApplicata.objects.create(
            **{"personale": doc2, "dt_ins": "2021-01-03 15:47:21"}
        )

        url = reverse(
            "teachers:apiv1:teacher-research-lines", kwargs={"teacherid": encrypt("111112")}
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["RLineDescription"] == "regressione lineare"

        res = req.get(url)
        assert len(res.json()["results"]) == 3

        # teacher 2 has one ricercalineabase (ended) and one
        # ricercalineaapplicata
        url = reverse(
            "teachers:apiv1:teacher-research-lines", kwargs={"teacherid": encrypt("111111")}
        )
        res = req.get(url)
        assert len(res.json()["results"]) == 2


class ApiTeachersListUnitTest(TestCase):
    def test_apiteacherslistunittest(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "uo_padre": "1",
            }
        )
        u2 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
            }
        )
        doc1 = Personale.objects.create(
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
            }
        )
        doc2 = Personale.objects.create(
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
                "cd_uo_aff_org": u2,
                "cv_full_it": "AAA",
                "cv_short_it": "A",
                "cv_full_eng": "BBB",
                "cv_short_eng": "B",
            }
        )
        Personale.objects.create(
            **{
                "id": 3,
                "nome": "Pippo",
                "cognome": "Inzaghi",
                "cd_ruolo": "PO",
                "id_ab": 3,
                "matricola": "111113",
                "fl_docente": 1,
                "flg_cessato": 1,
                "cd_uo_aff_org": u1,
            }
        )
        Personale.objects.create(
            **{
                "id": 4,
                "nome": "Zlatan",
                "cognome": "Ibrahimovic",
                "cd_ruolo": "PO",
                "id_ab": 4,
                "matricola": "111114",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
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
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        regdid2 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 2,
            }
        )
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid2,
                "af_radice_id": 2,
                "anno_corso": 2,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course1,
                "personale": doc1,
                "aa_off_id": datetime.datetime.now().year,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course2,
                "personale": doc2,
                "aa_off_id": datetime.datetime.now().year,
            }
        )

        url = reverse("teachers:apiv1:teachers-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()["results"]) == 3

        data = {"search": "gar"}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111111"

        data = {"role": "PA", "lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["TeacherCVFull"] is None

        data = {"department": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"department": 1, "role": "PO"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"department": 1, "role": "PA", "lang": "en", "year": "2015"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"regdid": 1}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111112"

        data = {"regdid": 2}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111111"

        data = {"regdid": 1, "role": "PA"}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111112"

        data = {"cds": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0


class ApiTeacherStudyActivitiesUnitTest(TestCase):
    def test_apiteacherstudyactivitiesunittest(self):
        req = Client()
        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "2",
                "uo_padre": "1",
            }
        )
        doc1 = Personale.objects.create(
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
            }
        )
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid,
                "af_radice_id": 2,
                "anno_corso": 2,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course1,
                "personale": doc1,
                "aa_off_id": 2019,
                "fat_part_stu_des": "111",
                "fat_part_stu_cod": "AA",
                "part_stu_des": "11",
                "part_stu_cod": "A",
                "tipo_fat_stu_cod": "ALF",
                "part_ini": "A",
                "part_fine": "Z",
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course2,
                "personale": doc1,
                "aa_off_id": 2020,
            }
        )

        url = reverse(
            "teachers:apiv1:teacher-study-activities", kwargs={"teacherid": encrypt("111112")}
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"][0]["StudyActivityID"] == 2

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"yearFrom": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"year": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"yearTo": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"yearFrom": 2019, "yearTo": 2020}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2


class ApiTeacherInfoUnitTest(TestCase):
    def test_apiteacherinfounittest(self):
        req = Client()

        u1 = UnitaOrganizzativa.objects.create(
            **{
                "uo": "1",
                "uo_padre": "1",
            }
        )
        u2 = UnitaOrganizzativa.objects.create(
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
                "ds_ruolo_locale": "aa",
                "id_ab": 1,
                "matricola": "111112",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u1,
                "cod_fis": "SMNMNG",
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
                "cd_ruolo": "PO",
                "ds_ruolo_locale": "ab",
                "id_ab": 2,
                "matricola": "111113",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
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
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course1,
                "personale": p1,
                "aa_off_id": 2019,
                "fat_part_stu_des": "111",
                "fat_part_stu_cod": "AA",
                "part_stu_des": "11",
                "part_stu_cod": "A",
                "tipo_fat_stu_cod": "ALF",
                "part_ini": "A",
                "part_fine": "Z",
            }
        )
        tipo_contatto = PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "EMAIL",
                "descr_contatto": "Posta Elettronica",
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
        PersonaleUoTipoContatto.objects.create(
            **{
                "cod_contatto": "Telefono Ufficio",
                "descr_contatto": "Telefono Ufficio",
            }
        )
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
                "contatto": "email@email",
                "prg_priorita": 1,
                "cod_fis": p1,
            }
        )
        PersonaleContatti.objects.create(
            **{
                "cd_tipo_cont": tipo_contatto,
                "id_ab": 2,
                "contatto": "email2@email",
                "prg_priorita": 1,
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

        DocentePtaAltriDati.objects.create(
            **{
                "id": 1,
                "matricola": p1,
                "path_foto": "aaaa",
                "path_cv_ita": "aaaa",
                "path_cv_en": "aaaaadc",
                "breve_bio": "prova",
                "breve_bio_en": "test",
                "orario_ricevimento": "lunedi",
                "orario_ricevimento_en": "monday",
                "orcid": "1111-2222-3333-4444",
            }
        )

        DocentePtaAltriDati.objects.create(
            **{
                "id": 2,
                "matricola": p2,
                "path_foto": "aaaa",
                "path_cv_ita": "aaaa",
                "path_cv_en": "aaaaadc",
                "breve_bio": "prova",
                "breve_bio_en": "test",
                "orario_ricevimento": "lunedi",
                "orario_ricevimento_en": "monday",
                "orcid": "1111-2222-3333-4445",
            }
        )

        url = reverse("teachers:apiv1:teacher-info", kwargs={"teacherid": encrypt("111112")})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert decrypt(res.json()["results"]["TeacherID"]) == "111112"

        url = reverse("teachers:apiv1:teacher-info", kwargs={"teacherid": encrypt("111113")})
        res = req.get(url)
        assert res.json()["results"]["TeacherFirstName"] == "Lionel"


class ApiTeacherNewsUnitTest(TestCase):
    def test_apiteachernewslist(self):
        req = Client()

        p1 = Personale.objects.create(
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

        DocentePtaBacheca.objects.create(
            **{
                "id": 1,
                "matricola": p1,
                "tipo_testo": "a",
                "tipo_testo_en": "a",
                "titolo": "evento",
                "titolo_en": "event",
                "testo": "evento",
                "testo_en": "event",
                "url_testo": "aaaa",
                "url_testo_en": "aaaa",
                "ordine": 1,
                "attivo": 1,
                "dt_pubblicazione": "2222-02-02",
                "dt_inizio_validita": "2022-10-13",
                "dt_fine_validita": "2099-10-13",
            }
        )

        url = reverse("teachers:apiv1:teacher-news", kwargs={"teacherid": encrypt("111112")})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiTeacherMaterialsUnitTest(TestCase):
    def test_apiteachermaterialslist(self):
        req = Client()

        p1 = Personale.objects.create(
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

        DocenteMaterialeDidattico.objects.create(
            **{
                "id": 1,
                "matricola": p1,
                "titolo": "evento",
                "titolo_en": "event",
                "testo": "evento",
                "testo_en": "event",
                "url_testo": "aaaa",
                "url_testo_en": "aaaa",
                "ordine": 1,
                "attivo": 1,
                "dt_pubblicazione": "2222-02-02",
                "dt_inizio_validita": "2022-10-13",
                "dt_fine_validita": "2099-10-13",
            }
        )

        url = reverse(
            "teachers:apiv1:teacher-materials", kwargs={"teacherid": encrypt("111112")}
        )

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiPublicationsListUnitTest(TestCase):
    def test_apiPublicationsList(self):
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
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 2,
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN2",
            }
        )

        p3 = Personale.objects.create(
            **{
                "id": 3,
                "nome": "Simone",
                "cognome": "Pino",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 3,
                "fl_docente": 1,
                "matricola": "111119",
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN3",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 1,
                "community_name": "Community 1",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 2,
                "community_name": "Community 2",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 1,
                "community_id": 1,
                "collection_name": "Collection 1",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 2,
                "community_id": 2,
                "collection_name": "Collection 2",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 1,
                "title": "pub1",
                "des_abstract": "abstract italiano",
                "des_abstracteng": "abstract inglese",
                "date_issued_year": 2020,
                "pubblicazione": "Giornale 1",
                "label_pubblicazione": "Rivista",
                "collection_id": 1,
                "url_pubblicazione": "aaa",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 2,
                "title": "pub2",
                "des_abstract": "abstract italiano2",
                "des_abstracteng": "abstract inglese2",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
                "url_pubblicazione": "aba",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 3,
                "title": "pub3",
                "des_abstract": "abstract italiano3",
                "des_abstracteng": "abstract inglese3",
                "date_issued_year": 9999,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
                "url_pubblicazione": "ccc",
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 1,
                "id_ab": p1,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 3,
                "id_ab": p2,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 1,
                "id_ab": p3,
            }
        )

        req = Client()

        url = reverse("teachers:apiv1:publications", kwargs={"teacherid": encrypt("111112")})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()["results"][0]["PublicationAbstract"] == "abstract inglese"

        data = {
            "year": 2020,
            "search": "pub",
            "type": 1,
            "contributor": "111119",
            "structure": "1",
        }

        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiPublicationsCommunityTypesListUnitTest(TestCase):
    def test_apiPublicationsCommunityTypesList(self):
        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 1,
                "community_name": "Comm 1",
            }
        )
        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 2,
                "community_name": "Comm 2",
            }
        )

        req = Client()

        url = reverse("teachers:apiv1:publications-community-types")

        # check url
        res = req.get(url)

        assert res.status_code == 200
        assert res.json()["results"][0]["CommunityName"] == "Comm 1"


class ApiPublicationDetailUnitTest(TestCase):
    def test_apiPublicationDetail(self):
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
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 2,
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN2",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 1,
                "community_name": "Community 1",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 2,
                "community_name": "Community 2",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 1,
                "community_id": 1,
                "collection_name": "Collection 1",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 2,
                "community_id": 2,
                "collection_name": "Collection 2",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 1,
                "title": "pub1",
                "des_abstract": "abstract italiano",
                "des_abstracteng": "abstract inglese",
                "date_issued_year": 2020,
                "pubblicazione": "Giornale 1",
                "label_pubblicazione": "Rivista",
                "collection_id": 1,
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 2,
                "title": "pub2",
                "des_abstract": "abstract italiano2",
                "des_abstracteng": "abstract inglese2",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 3,
                "title": "pub3",
                "des_abstract": "abstract italiano3",
                "des_abstracteng": "abstract inglese3",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 1,
                "id_ab": p1,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 3,
                "id_ab": p2,
            }
        )

        req = Client()

        url = reverse(
            "teachers:apiv1:publication-detail",
            kwargs={"teacherid": encrypt("111112"), "publicationid": "1"},
        )

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()["results"]["PublicationAbstract"] == "abstract inglese"

        url = reverse(
            "teachers:apiv1:publication-detail",
            kwargs={"teacherid": encrypt("111112"), "publicationid": "2"},
        )

        res = req.get(url)
        assert res.json()["results"]["PublicationYear"] == 2019


class ApiAllPublicationsListUnitTest(TestCase):
    def test_apiAllPublicationsList(self):
        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 1,
                "community_name": "Community 1",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 2,
                "community_name": "Community 2",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 1,
                "community_id": 1,
                "collection_name": "Collection 1",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 2,
                "community_id": 2,
                "collection_name": "Collection 2",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 1,
                "title": "pub1",
                "des_abstract": "abstract italiano",
                "des_abstracteng": "abstract inglese",
                "date_issued_year": 2020,
                "pubblicazione": "Giornale 1",
                "contributors": "Pinnola",
                "label_pubblicazione": "Rivista",
                "collection_id": 1,
                "url_pubblicazione": "aaa",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 2,
                "title": "pub2",
                "des_abstract": "abstract italiano2",
                "des_abstracteng": "abstract inglese2",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
                "url_pubblicazione": "aba",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 3,
                "title": "pub3",
                "des_abstract": "abstract italiano3",
                "des_abstracteng": "abstract inglese3",
                "date_issued_year": 9999,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
                "url_pubblicazione": "ccc",
            }
        )

        req = Client()

        url = reverse("teachers:apiv1:publications-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        assert res.json()["results"][1]["PublicationAbstract"] == "abstract inglese"

        data = {"year": 2020, "search": "pub", "type": 1, "contributors": "Pinnola"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiPublicationInfoUnitTest(TestCase):
    def test_apiPublicationInfo(self):
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
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "PA",
                "ds_ruolo_locale": "Professore Associato",
                "id_ab": 2,
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "cod_fis": "SMN2",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 1,
                "community_name": "Community 1",
            }
        )

        PubblicazioneCommunity.objects.create(
            **{
                "community_id": 2,
                "community_name": "Community 2",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 1,
                "community_id": 1,
                "collection_name": "Collection 1",
            }
        )

        PubblicazioneCollection.objects.create(
            **{
                "collection_id": 2,
                "community_id": 2,
                "collection_name": "Collection 2",
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 1,
                "title": "pub1",
                "des_abstract": "abstract italiano",
                "des_abstracteng": "abstract inglese",
                "date_issued_year": 2020,
                "pubblicazione": "Giornale 1",
                "label_pubblicazione": "Rivista",
                "collection_id": 1,
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 2,
                "title": "pub2",
                "des_abstract": "abstract italiano2",
                "des_abstracteng": "abstract inglese2",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
            }
        )

        PubblicazioneDatiBase.objects.create(
            **{
                "item_id": 3,
                "title": "pub3",
                "des_abstract": "abstract italiano3",
                "des_abstracteng": "abstract inglese3",
                "date_issued_year": 2019,
                "pubblicazione": "Convegno Cosenza",
                "label_pubblicazione": "Convegno",
                "collection_id": 2,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 1,
                "id_ab": p1,
            }
        )

        PubblicazioneAutori.objects.create(
            **{
                "item_id": 3,
                "id_ab": p2,
            }
        )

        req = Client()

        url = reverse("teachers:apiv1:publication-info", kwargs={"publicationid": "1"})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()["results"]["PublicationAbstract"] == "abstract inglese"

        url = reverse("teachers:apiv1:publication-info", kwargs={"publicationid": "1"})
        res = req.get(url)
        assert res.json()["results"]["PublicationYear"] == 2020

        url = reverse("teachers:apiv1:publication-info", kwargs={"publicationid": "3"})
        res = req.get(url)
        assert res.json()["results"]["PublicationYear"] == 2019


class ApiTeachingsCoveragesListUnitTest(TestCase):
    def test_apiteachingCoverageslistunittest(self):
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
        doc1 = Personale.objects.create(
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
                "profilo": "111",
                "ds_profilo": "abcds",
                "ds_profilo_breve": "afv",
            }
        )
        doc2 = Personale.objects.create(
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
                "cd_uo_aff_org": u2,
                "cv_full_it": "AAA",
                "cv_short_it": "A",
                "cv_full_eng": "BBB",
                "cv_short_eng": "B",
                "profilo": "111",
                "ds_profilo": "abcds",
                "ds_profilo_breve": "afv",
            }
        )
        Personale.objects.create(
            **{
                "id": 3,
                "nome": "Pippo",
                "cognome": "Inzaghi",
                "cd_ruolo": "PO",
                "id_ab": 3,
                "matricola": "111113",
                "fl_docente": 1,
                "flg_cessato": 1,
                "cd_uo_aff_org": u1,
                "profilo": "111",
                "ds_profilo": "abcds",
                "ds_profilo_breve": "afv",
            }
        )
        Personale.objects.create(
            **{
                "id": 4,
                "nome": "Zlatan",
                "cognome": "Ibrahimovic",
                "cd_ruolo": "PO",
                "id_ab": 4,
                "matricola": "111114",
                "fl_docente": 1,
                "flg_cessato": 0,
                "cd_uo_aff_org": u2,
                "profilo": "111",
                "ds_profilo": "abcds",
                "ds_profilo_breve": "afv",
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
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        regdid2 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{
                "regdid_id": 2,
            }
        )
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 1,
                "des": "matematica",
                "af_gen_des_eng": "math",
                "ciclo_des": "Primo semestre",
                "regdid": regdid,
                "af_radice_id": 1,
                "anno_corso": 1,
            }
        )
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(
            **{
                "af_id": 2,
                "des": "informatica",
                "af_gen_des_eng": "computer science",
                "ciclo_des": "Secondo semestre",
                "regdid": regdid2,
                "af_radice_id": 2,
                "anno_corso": 1,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course1,
                "personale": doc1,
            }
        )
        DidatticaCopertura.objects.create(
            **{
                "af": course2,
                "personale": doc2,
            }
        )

        url = reverse("teachers:apiv1:teaching-coverages-list")

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"search": "gar"}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111111"

        data = {"role": "PA", "lang": "it"}
        res = req.get(url, data=data)
        assert res.json()["results"][0]["TeacherCVFull"] is None

        data = {"department": 42}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"department": 1, "role": "PO"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0

        data = {"department": 1, "role": "PA", "lang": "en"}
        res = req.get(url, data=data)
        assert (
            res.json()["results"][0]["TeacherDepartmentName"]
            == "Math and Computer Science"
        )

        data = {"regdid": 1}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111112"

        data = {"regdid": 2}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111111"

        data = {"regdid": 1, "role": "PA"}
        res = req.get(url, data=data)
        assert decrypt(res.json()["results"][0]["TeacherID"]) == "111112"

        data = {"cds": 1}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 0


class ApiAster1ListUnitTest(TestCase):
    def test_apiaster1list(self):
        req = Client()

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )
        RicercaAster1.objects.create(
            **{
                "id": 1,
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )

        url = reverse("laboratories:apiv1:aster1-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert len(res.json()["results"]) == 1


class ApiAster2ListUnitTest(TestCase):
    def test_apiaster2list(self):
        req = Client()

        erc0 = RicercaErc0.objects.create(
            **{
                "erc0_cod": "111",
                "description": "IT",
                "description_en": "IT",
            }
        )
        aster1 = RicercaAster1.objects.create(
            **{
                "id": 1,
                "descrizione": "Computer Science and Informatics",
                "ricerca_erc0_cod": erc0,
            }
        )

        RicercaAster2.objects.create(
            **{"id": 1, "descrizione": "Sicurezza Informatica", "ricerca_aster1_id": 1}
        )
        url = reverse("laboratories:apiv1:aster2-list")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert len(res.json()["results"]) == 1
