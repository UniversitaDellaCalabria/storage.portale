from django.test import TestCase, Client
from django.urls import reverse

from .util_test import ComuniAllUnitTest, DidatticaAttivitaFormativaUnitTest, DidatticaCdsLinguaUnitTest, \
    DidatticaCdsUnitTest, DidatticaCoperturaUnitTest, DidatticaDipartimentoUnitTest, DidatticaPdsRegolamentoUnitTest, \
    DidatticaRegolamentoUnitTest, DidatticaTestiAfUnitTest, DidatticaTestiRegolamentoUnitTest, PersonaleUnitTest, \
    RicercaAster1UnitTest, RicercaAster2UnitTest, RicercaDocenteGruppoUnitTest, RicercaDocenteLineaApplicataUnitTest, \
    RicercaDocenteLineaBaseUnitTest, RicercaErc1UnitTest, RicercaErc2UnitTest, RicercaGruppoUnitTest, \
    RicercaLineaApplicataUnitTest, RicercaLineaBaseUnitTest, TerritorioItUnitTest, RicercaErc0UnitTest, \
    DidatticaDottoratoCdsUnitTest, DidatticaDottoratoPdsUnitTest, DidatticaDottoratoRegolamentoUnitTest
from .serializers import CreateUpdateAbstract


class ApiCdSListUnitTest(TestCase):

    def test_apicdslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
        })
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didatticaCds,
        })
        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'stato_regdid_cod': 'A',
            'titolo_congiunto_cod': 'N',
            'cds_id': 1,
        })

        url = reverse('ricerca:cdslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: lang
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: lang
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: coursetype
        data = {'coursetype': '1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: courseclassid
        data = {'courseclassid': '1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: courseclassname
        data = {'courseclassname': 'laurea in informatica'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: departmentid
        data = {'departmentid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: departmentname
        data = {'departmentname': 'matematica e informatica', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: academicyear
        data = {'academicyear': 2020}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: jointdegree
        data = {'jointdegree': 'N'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: cdslanguage
        data = {'cdslanguage': 'ITALIANO', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: keywords ita
        data = {'keywords': 'informatica', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: keywords eng
        data = {'keywords': 'computer', 'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: keywords eng wrong
        data = {'keywords': 'math', 'lang': 'en'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        # param: all
        data = {'cdslanguage': 'ITALIAN',
                'jointdegree': 'N',
                'academicyear': 2020,
                'departmentname': 'math and computer science',
                'departmentid': 1,
                'courseclassname': 'laurea in informatica',
                'courseclassid': '1',
                'coursetype': '1',
                'lang': 'en',
                }
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1


class OpenApiSchemaUnitTest(TestCase):
    def test_openapi(self):
        req = Client()
        url = reverse('ricerca:openapi-schema')
        res = req.get(url)
        assert res.status_code == 200

        url = reverse('ricerca:openapi-schema-json')
        res = req.get(url)
        assert res.status_code == 200


class SerializersUnitTest(TestCase):
    def test_createUpdateAbstract(self):
        ser = CreateUpdateAbstract()
        ser.create(None)
        ser.update(None, None)


class ModelsToStringUnitTest(TestCase):

    def test_modelstostring(self):
        comuni_all = ComuniAllUnitTest.create_comuniAll(**{
            'id_comune': 1
        })
        assert isinstance(comuni_all.__str__(), str)

        territorio_it = TerritorioItUnitTest.create_territorioIt(**{
            'cd_catasto': comuni_all
        })
        assert isinstance(territorio_it.__str__(), str)

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        assert isinstance(dip.__str__(), str)

        didattica_cds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
        })
        assert isinstance(didattica_cds.__str__(), str)

        didattica_lingua = DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(
            **{'cdsord': didattica_cds, })
        assert isinstance(didattica_lingua.__str__(), str)

        didattica_regolamento = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(
            **{'regdid_id': 1, })
        assert isinstance(didattica_regolamento.__str__(), str)

        didattica_testi_regolamento = DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(
            **{'regdid': didattica_regolamento, })
        assert isinstance(didattica_testi_regolamento.__str__(), str)


class ApiCdSInfoUnitTest(TestCase):

    def test_apicdsinfo(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
        })
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didatticaCds,
        })
        reg = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'stato_regdid_cod': 'A',
            'titolo_congiunto_cod': 'N',
            'cds': didatticaCds,
        })
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'txt_id': 1,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'DESC_COR_BRE',
        })
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'txt_id': 2,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'FUNZIONI',
            'profilo': 'profiloprova',
            'clob_txt_ita': 'provadescrizione',
        })

        url = reverse('ricerca:cdsinfo', kwargs={'cdsid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'cdsid': 1})

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results']['RegDidId'] == 1

        # param: cdsid 10 doesn't exist
        url = reverse('ricerca:cdsinfo', kwargs={'cdsid': 10})
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'cdsid': 1})
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results']['RegDidId'] == 1

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'cdsid': 1})
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][
            'CdSProfiles']['profiloprova']['FUNZIONI'] == 'provadescrizione'


class ApiCdSStudyPlansUnitTest(TestCase):

    def test_apicdsstudyplans(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'regdid': regdid, })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'pds_regdid': pds,
            'regdid': regdid,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'af_id': 1,
            'af_radice_id': 1,
        })

        url = reverse('ricerca:cdsstudyplans', kwargs={'cdsid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['RegDidId'] == 1

        # lang it

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StudyActivityName'] == 'matematica'

        # lang eng
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StudyActivityName'] == 'math'


class ApiCdSStudyPlansUniqueUnitTest(TestCase):

    def test_apicdsstudyplansunique(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'regdid': regdid,
               'pds_regdid_id': 1,
               'pds_cod': 1,
               'pds_des_it': 'Intelligenza Artificiale',
               'pds_des_eng': 'Artificial Intelligence'
               })

        DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'regdid': regdid,
               'pds_regdid_id': 2,
               'pds_cod': 2,
               'pds_des_it': 'Sicurezza',
               'pds_des_eng': 'Security'
               })

        url = reverse('ricerca:cdsstudyplansunique', kwargs={'cdsid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['RegDidId'] == 1

        # lang it
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['StudyPlanName'] == 'Intelligenza Artificiale'

        # lang eng
        data = {'lang': 'eng'}
        res = req.get(url, data=data)
        assert res.json()['results'][1]['StudyPlanName'] == 'Security'

        # wrong cdsid
        url = reverse('ricerca:cdsstudyplans', kwargs={'cdsid': 100})
        data = {'lang': 'eng'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0


class ApiStudyPlanActivitiesUnitTest(TestCase):

    def test_apistudyplanactivities(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds1 = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'pds_regdid_id': 1, 'regdid': regdid, })
        pds2 = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'pds_regdid_id': 2, 'regdid': regdid, })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'pds_regdid': pds1,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'pds_regdid': pds1,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 3,
            'pds_regdid': pds1,
            'des': 'informatica modulo 1',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 4,
            'pds_regdid': pds2,
            'des': 'matematica2',
            'af_gen_des_eng': 'math2',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 4,
        })

        url = reverse(
            'ricerca:studyplanactivities',
            kwargs={
                'cdsid': 1,
                'studyplanid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['StudyActivityID'] == 1

        # 3 courses : 2 main courses, 1 module course, should return 2 courses
        res = req.get(url)
        assert len(res.json()['results']) == 2

        # lang it first semester
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StudyActivityName'] == 'matematica'

        # lang eng first semester
        data = {'lang': 'eng'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StudyActivityName'] == 'math'

        # lang it second semester
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][1]['StudyActivityName'] == 'informatica'

        # lang eng second semester
        data = {'lang': 'eng'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][1]['StudyActivityName'] == 'computer science'

        url = reverse(
            'ricerca:studyplanactivities',
            kwargs={
                'cdsid': 1,
                'studyplanid': 2})
        res = req.get(url)
        assert res.json()['results'][0]['StudyActivityID'] == 4


class ApiStudyActivityInfoUnitTest(TestCase):

    def test_apistudyactivityinfo(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'pds_regdid_id': 1, 'regdid': regdid, })
        course = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'pds_regdid': pds,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'matricola_resp_did': '111111',
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'pds_regdid': pds,
            'des': 'informatica modulo 1',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
        })
        DidatticaTestiAfUnitTest.create_didatticaTestiAf(**{
            'tipo_testo_af_cod': 'CONTENUTI',
            'testo_af_ita': 'Variabili',
            'testo_af_eng': 'Variables',
            'af': course,
        })
        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course,
            'personale': p,
        })

        url = reverse(
            'ricerca:studyactivityinfo',
            kwargs={
                'cdsid': 1,
                'studyplanid': 1,
                'studyactivityid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['StudyActivityID'] == 1

        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results']['StudyActivityContent'] == 'Variables'

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results']['StudyActivityContent'] == 'Variabili'


class ApiCdSMainTeachersUnitTest(TestCase):

    def test_apicdsmainteachers(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
        })
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': True,
        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Franco',
            'middle_name': 'Luigi',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111111',
            'fl_docente': True,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course1,
            'personale': p1,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course2,
            'personale': p2,
        })

        url = reverse('ricerca:cdsmainteachers')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        data = {'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherName'] == 'Mungari Simone'

        data = {'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][1]['TeacherName'] == 'Garofalo Franco Luigi'


class ApiTeacherResearchGroupsUnitTest(TestCase):

    def test_apiteacherresearchgroups(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
        })
        doc2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Franco',
            'middle_name': 'Luigi',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111111',
            'fl_docente': 1,
        })

        r1 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 1,
            'nome': 'Intelligenza Artificiale',
            'descrizione': 'ricerca su Machine Learning',
        })
        r2 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 2,
            'nome': 'Intelligenza Artificiale',
            'descrizione': 'ricerca su Deep Learning',
        })
        r3 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 3,
            'nome': 'Statistica',
            'descrizione': 'ricerca su Variabili Aleatorie',
        })

        RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
            'personale': doc1,
            'ricerca_gruppo': r1,
            'id': 1,
        })
        RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
            'personale': doc1,
            'ricerca_gruppo': r2,
            'id': 2,
        })
        RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
            'personale': doc2,
            'ricerca_gruppo': r3,
            'id': 3,
            'dt_fine': '2021-01-03',
        })
        RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
            'personale': doc2,
            'ricerca_gruppo': r2,
            'id': 4,
        })

        url = reverse(
            'ricerca:teacherresearchgroups', kwargs={
                'teacherid': '111112'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['RGroupID'] == 1

        # two groups for teacherid = 1
        res = req.get(url)
        assert len(res.json()['results']) == 2

        # dt fine not null
        url = reverse(
            'ricerca:teacherresearchgroups', kwargs={
                'teacherid': '111111'})
        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiTeacherResearchLinesUnitTest(TestCase):

    def test_apiteacherresearchlinesunittest(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
        })
        doc2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Franco',
            'middle_name': 'Luigi',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111111',
            'fl_docente': 1,
        })

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
        })

        erc1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        erc2 = RicercaErc2UnitTest.create_ricercaErc2(**{
            'cod_erc2': 'cod1_erc2',
            'descrizione': 'Machine learning',
            'ricerca_erc1': erc1
        })
        linea_base = RicercaLineaBaseUnitTest.create_ricercaLineaBase(**{
            'id': 1,
            'ricerca_erc2': erc2,
            'descrizione': 'regressione lineare',
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2020'
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc1,
            'ricerca_linea_base': linea_base
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc2,
            'ricerca_linea_base': linea_base,
            'dt_fine': '2021-01-03',
        })

        aster1 = RicercaAster1UnitTest.create_ricercaAster1(**{
            'id': 1,
            'descrizione': 'ICT & Design',
            'ricerca_erc0_cod': erc0,
        })
        aster2 = RicercaAster2UnitTest.create_ricercaAster2(**{
            'id': 2,
            'descrizione': 'Algorithms. Data and signal processing',
            'ricerca_aster1': aster1
        })
        linea_applicata = RicercaLineaApplicataUnitTest.create_ricercaLineaApplicata(**{
            'id': 1,
            'ricerca_aster2': aster2,
            'descrizione': 'regressione lineare',
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2020'
        })
        linea_applicata2 = RicercaLineaApplicataUnitTest.create_ricercaLineaApplicata(**{
            'id': 2,
            'ricerca_aster2': aster2,
            'descrizione': 'random forest',
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2019'
        })
        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc1,
            'ricerca_linea_applicata': linea_applicata,
            'dt_ins': '2021-01-03 15:47:21'
        })
        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc1,
            'ricerca_linea_applicata': linea_applicata2,
            'dt_ins': '2021-01-03 15:47:21'
        })
        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc2,
            'ricerca_linea_applicata': linea_applicata,
            'dt_ins': '2021-01-03 15:47:21'
        })

        url = reverse(
            'ricerca:teacherresearchlines', kwargs={
                'teacherid': '111112'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results'][0]['R&SLineDescription'] == 'regressione lineare'

        res = req.get(url)
        assert len(res.json()['results']) == 3

        # teacherid 2 has one ricercalineabase (ended) and one
        # ricercalineaapplicata
        url = reverse(
            'ricerca:teacherresearchlines', kwargs={
                'teacherid': '111111'})
        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiTeachersListUnitTest(TestCase):

    def test_apiteacherslistunittest(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 1,
        })
        PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Franco',
            'middle_name': 'Luigi',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111111',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 2,
        })
        PersonaleUnitTest.create_personale(**{
            'id': 3,
            'nome': 'Pippo',
            'cognome': 'Inzaghi',
            'cd_ruolo': 'PO',
            'id_ab': 3,
            'matricola': '111113',
            'fl_docente': 1,
            'flg_cessato': 1,
            'aff_org': 1,
        })
        PersonaleUnitTest.create_personale(**{
            'id': 4,
            'nome': 'Zlatan',
            'cognome': 'Ibrahimovic',
            'cd_ruolo': 'PO',
            'id_ab': 4,
            'matricola': '111114',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 42,
        })

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': 2,
            'dip_des_it': "Biologia",
            'dip_des_eng': "Biology",
        })

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        regdid2 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 2,
        })
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
        })
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid2,
            'af_radice_id': 2,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course1,
            'personale': doc1,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course2,
            'personale': doc1,
        })

        url = reverse('ricerca:teacherslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()['results']) == 3

        data = {'role': 'PO'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111111'

        data = {'departmentid': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'departmentid': 42}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'departmentid': 1, 'role': 'PO'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'departmentid': 1, 'role': 'PA', 'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['TeacherDepartmentName'] == "Math and Computer Science"

        data = {'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'cdsid': 2}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'cdsid': 1, 'role': 'PA'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'


class ApiTeacherStudyActivitiesUnitTest(TestCase):

    def test_apiteacherstudyactivitiesunittest(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 1,
        })
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'anno_corso': 1,
        })
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
            'anno_corso': 2,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course1,
            'personale': doc1,
            'aa_id': 2019,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course2,
            'personale': doc1,
            'aa_id': 2020,
        })

        url = reverse(
            'ricerca:teacherstudyactivities', kwargs={
                'teacherid': '111112'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['StudyActivityID'] == 1

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'yearFrom': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'yearTo': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'yearFrom': 2019, 'yearTo': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2


class ApiTeacherInfoUnitTest(TestCase):

    def test_apiteacherinfounittest(self):
        req = Client()

        PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 1,
        })
        PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 1,
            'flg_cessato': 0,
            'aff_org': 99,
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })

        url = reverse('ricerca:teacherinfo', kwargs={'teacherid': '111112'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['TeacherID'] == '111112'

        url = reverse('ricerca:teacherinfo', kwargs={'teacherid': '111113'})
        res = req.get(url)
        assert res.json()['results']['TeacherID'] == '111113'


class ApiDoctoratesListUnitTest(TestCase):

    def test_apidoctorateslistunittest(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })

        cds = DidatticaDottoratoCdsUnitTest.create_didatticaDottoratoCds(**{
            'dip_cod': dip,
            'cds_id_esse3': 1,
            'cds_cod': '111',
            'aa_ord_id': 1,

        })

        DidatticaDottoratoPdsUnitTest.create_didatticaDottoratoPds(**{
            'cds_id_esse3': cds,
            'aa_ord': cds,
            'pds_cod': 'GEN',
        })

        DidatticaDottoratoRegolamentoUnitTest.create_didatticaDottoratoRegolamento(**{
            'regdid_id_esse3': 1,
            'cds_id_esse3': cds,
            'aa_ord': cds,
            'aa_regdid_id': 2020,
            'num_ciclo': 10,
        })

        url = reverse('ricerca:doctorateslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'departmentid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'year': 2020}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'yearTo': 2019, 'yearFrom': 2018}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'yearTo': 2019}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'yearFrom': 2018}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'cdsid': '111'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'pdscod': 'GEN'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'cycle': 0}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0
