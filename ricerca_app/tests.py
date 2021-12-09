import datetime

from django.test import TestCase, Client
from django.urls import reverse

from .util_test import ComuniAllUnitTest, DidatticaAttivitaFormativaUnitTest, DidatticaCdsLinguaUnitTest, \
    DidatticaCdsUnitTest, DidatticaCoperturaUnitTest, DidatticaDipartimentoUnitTest, DidatticaPdsRegolamentoUnitTest, \
    DidatticaRegolamentoUnitTest, DidatticaTestiAfUnitTest, DidatticaTestiRegolamentoUnitTest, PersonaleUnitTest, \
    RicercaAster1UnitTest, RicercaAster2UnitTest, RicercaDocenteGruppoUnitTest, RicercaDocenteLineaApplicataUnitTest, \
    RicercaDocenteLineaBaseUnitTest, RicercaErc1UnitTest, RicercaErc2UnitTest, RicercaGruppoUnitTest, \
    RicercaLineaApplicataUnitTest, RicercaLineaBaseUnitTest, TerritorioItUnitTest, RicercaErc0UnitTest, \
    DidatticaDottoratoCdsUnitTest, DidatticaDottoratoPdsUnitTest, DidatticaDottoratoRegolamentoUnitTest, \
    PersonaleTipoContattoUnitTest, PersonaleContattiUnitTest, UnitaOrganizzativaFunzioniUnitTest, \
    UnitaOrganizzativaUnitTest, UnitaOrganizzativaContattiUnitTest, LaboratorioDatiBaseUnitTest, \
    LaboratorioAttivitaUnitTest, LaboratorioDatiErc1UnitTest, LaboratorioPersonaleRicercaUnitTest, \
    LaboratorioPersonaleTecnicoUnitTest, LaboratorioServiziOffertiUnitTest, LaboratorioUbicazioneUnitTest, \
    LaboratorioAltriDipartimentiUnitTest, PubblicazioneDatiBaseUnitTest, PubblicazioneCommunityUnitTest, \
    PubblicazioneCollectionUnitTest, PubblicazioneAutoriUnitTest, LaboratorioInfrastrutturaUnitTest, LaboratorioTipologiaAttivitaUnitTest, \
    BrevettoDatiBaseUnitTest, BrevettoInventoriUnitTest, TipologiaAreaTecnologicaUnitTest, SpinoffStartupDatiBaseUnitTest, \
    ProgettoDatiBaseUnitTest, ProgettoTipologiaProgrammaUnitTest, ProgettoAmbitoTerritorialeUnitTest, ProgettoResponsabileScientificoUnitTest,\
    UnitaOrganizzativaTipoFunzioniUnitTest
from .serializers import CreateUpdateAbstract


class ApiCdSListUnitTest(TestCase):

    def test_apicdslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'tipo_corso_cod': 'L',
        })
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didatticaCds,
            'iso6392_cod': 'ita',
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
        data = {'coursetype': 'L'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: courseclasscod
        data = {'courseclasscod': '1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: courseclassname
        data = {'courseclassname': 'laurea in informatica'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: departmentcod
        data = {'departmentcod': 1}
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
        data = {'cdslanguage': 'ita', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: search ita
        data = {'search': 'informatica', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: search eng
        data = {'search': 'computer', 'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['RegDidId'] == 1

        # param: search eng wrong
        data = {'search': 'math', 'lang': 'en'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        # param: all
        data = {'cdslanguage': 'ita',
                'jointdegree': 'N',
                'academicyear': 2020,
                'departmentname': 'math and computer science',
                'departmentcod': 1,
                'courseclassname': 'laurea in informatica',
                'courseclasscod': '1',
                'coursetype': 'L',
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
            'txt_id': 3,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'URL_CDS_VIDEO',
        })
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'txt_id': 2,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'FUNZIONI',
            'profilo': 'profiloprova',
            'clob_txt_ita': 'provadescrizione',
        })

        url = reverse('ricerca:cdsinfo', kwargs={'regdidid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'regdidid': 1})

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results']['RegDidId'] == 1

        # param: cdsid 10 doesn't exist
        url = reverse('ricerca:cdsinfo', kwargs={'regdidid': 10})
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'regdidid': 1})
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()['results']['RegDidId'] == 1

        # param: lang
        url = reverse('ricerca:cdsinfo', kwargs={'regdidid': 1})
        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][
            'CdSProfiles']['profiloprova']['FUNZIONI'] == 'provadescrizione'


class ApiCdSStudyPlansUnitTest(TestCase):

    def test_apicdsstudyplans(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'durata_anni': 3,
        })
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'cds': cds,
        })
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'regdid': regdid, })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'pds_regdid': pds,
            'regdid': regdid,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'af_id': 1,
            'af_radice_id': 1,
            'anno_corso': 1
        })

        url = reverse('ricerca:cdsstudyplans', kwargs={'regdidid': 1})

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
            'results'][0]['StudyActivities']['1'][0]['StudyActivityName'] == 'matematica'

        # lang eng
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['StudyActivities']['1'][0]['StudyActivityName'] == 'math'


class ApiStudyPlanDetailUnitTest(TestCase):

    def test_apicdsstudyplans(self):
        req = Client()

        cds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'durata_anni': 3,
        })
        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'cds': cds,
        })
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'regdid': regdid, })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'pds_regdid': pds,
            'regdid': regdid,
            'des': 'matematica',
            'af_gen_des_eng': 'math',
            'af_id': 1,
            'af_radice_id': 1,
            'anno_corso': 1
        })

        url = reverse(
            'ricerca:studyplandetail',
            kwargs={
                'regdidid': 1,
                'studyplanid': 1})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['RegDidId'] == 1

        # lang it

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()[
            'results']['StudyActivities']['1'][0]['StudyActivityName'] == 'matematica'

        # lang eng
        data = {'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()[
            'results']['StudyActivities']['1'][0]['StudyActivityName'] == 'math'


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
                'regdidid': 1,
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
                'regdidid': 1,
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
            'mutuata_flg': 1,
            'af_master_id': 2,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'pds_regdid': pds,
            'des': 'informatica modulo 1',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'mutuata_flg': 0,
            'af_master_id': 2,
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
                'regdidid': 1,
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

        url = reverse(
            'ricerca:studyactivityinfo',
            kwargs={
                'regdidid': 1,
                'studyplanid': 1,
                'studyactivityid': 2})
        res = req.get(url)
        assert res.json()['results']['StudyActivityID'] == 2


class ApiStudyActivityDetailUnitTest(TestCase):

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
            'mutuata_flg': 1,
            'af_master_id': 2,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'pds_regdid': pds,
            'des': 'informatica modulo 1',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'mutuata_flg': 0,
            'af_master_id': 2,
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
            'ricerca:studyactivitydetail',
            kwargs={'studyactivityid': 1})

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

        url = reverse(
            'ricerca:studyactivitydetail',
            kwargs={'studyactivityid': 2})
        res = req.get(url)
        assert res.json()['results']['StudyActivityID'] == 2


# class ApiCdSMainTeachersUnitTest(TestCase):
#
#     def test_apicdsmainteachers(self):
#         req = Client()
#
#         regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
#         course1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
#             'af_id': 1,
#             'des': 'matematica',
#             'af_gen_des_eng': 'math',
#             'ciclo_des': 'Primo semestre',
#             'regdid': regdid,
#             'af_radice_id': 1,
#         })
#         course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
#             'af_id': 2,
#             'des': 'informatica',
#             'af_gen_des_eng': 'computer science',
#             'ciclo_des': 'Secondo semestre',
#             'regdid': regdid,
#             'af_radice_id': 2,
#         })
#         p1 = PersonaleUnitTest.create_personale(**{
#             'id': 1,
#             'nome': 'Simone',
#             'cognome': 'Mungari',
#             'cd_ruolo': 'PA',
#             'id_ab': 1,
#             'matricola': '111112',
#             'fl_docente': True,
#         })
#         p2 = PersonaleUnitTest.create_personale(**{
#             'id': 2,
#             'nome': 'Franco',
#             'middle_name': 'Luigi',
#             'cognome': 'Garofalo',
#             'cd_ruolo': 'PO',
#             'id_ab': 2,
#             'matricola': '111111',
#             'fl_docente': True,
#         })
#         DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
#             'af': course1,
#             'personale': p1,
#         })
#         DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
#             'af': course2,
#             'personale': p2,
#         })
#
#         url = reverse('ricerca:cdsmainteachers')
#
#         # check url
#         res = req.get(url)
#         assert res.status_code == 200
#
#         # GET
#
#         data = {'regdidid': 1}
#         res = req.get(url, data=data)
#         assert res.json()['results'][0]['TeacherID'] == '111112'
#
#         data = {'regdidid': 1}
#         res = req.get(url, data=data)
#         assert res.json()['results'][0]['TeacherName'] == 'Mungari Simone'
#
#         data = {'regdidid': 1}
#         res = req.get(url, data=data)
#         assert res.json()[
#             'results'][1]['TeacherName'] == 'Garofalo Franco Luigi'


# class ApiTeacherResearchGroupsUnitTest(TestCase):
#
#     def test_apiteacherresearchgroups(self):
#         req = Client()
#
#         doc1 = PersonaleUnitTest.create_personale(**{
#             'id': 1,
#             'nome': 'Simone',
#             'cognome': 'Mungari',
#             'cd_ruolo': 'PA',
#             'id_ab': 1,
#             'matricola': '111112',
#             'fl_docente': 1,
#         })
#         doc2 = PersonaleUnitTest.create_personale(**{
#             'id': 2,
#             'nome': 'Franco',
#             'middle_name': 'Luigi',
#             'cognome': 'Garofalo',
#             'cd_ruolo': 'PO',
#             'id_ab': 2,
#             'matricola': '111111',
#             'fl_docente': 1,
#         })
#
#         r1 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
#             'id': 1,
#             'nome': 'Intelligenza Artificiale',
#             'descrizione': 'ricerca su Machine Learning',
#         })
#         r2 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
#             'id': 2,
#             'nome': 'Intelligenza Artificiale',
#             'descrizione': 'ricerca su Deep Learning',
#         })
#         r3 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
#             'id': 3,
#             'nome': 'Statistica',
#             'descrizione': 'ricerca su Variabili Aleatorie',
#         })
#
#         RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
#             'personale': doc1,
#             'ricerca_gruppo': r1,
#             'id': 1,
#         })
#         RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
#             'personale': doc1,
#             'ricerca_gruppo': r2,
#             'id': 2,
#         })
#         RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
#             'personale': doc2,
#             'ricerca_gruppo': r3,
#             'id': 3,
#             'dt_fine': '2021-01-03',
#         })
#         RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
#             'personale': doc2,
#             'ricerca_gruppo': r2,
#             'id': 4,
#         })
#
#         url = reverse(
#             'ricerca:teacherresearchgroups', kwargs={
#                 'teacherid': '111112'})
#
#         # check url
#         res = req.get(url)
#         assert res.status_code == 200
#
#         # GET
#
#         res = req.get(url)
#         assert res.json()['results'][0]['RGroupID'] == 1
#
#         # two groups for teacher = 1
#         res = req.get(url)
#         assert len(res.json()['results']) == 2
#
#         # dt fine not null
#         url = reverse(
#             'ricerca:teacherresearchgroups', kwargs={
#                 'teacherid': '111111'})
#         res = req.get(url)
#         assert len(res.json()['results']) == 1


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
            'results'][0]['RLineDescription'] == 'regressione lineare'

        res = req.get(url)
        assert len(res.json()['results']) == 3

        # teacher 2 has one ricercalineabase (ended) and one
        # ricercalineaapplicata
        url = reverse(
            'ricerca:teacherresearchlines', kwargs={
                'teacherid': '111111'})
        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiTeachersListUnitTest(TestCase):

    def test_apiteacherslistunittest(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'uo_padre': '1',
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })
        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
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
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cv_full_it': 'AAA',
            'cv_short_it': 'A',
            'cv_full_eng': 'BBB',
            'cv_short_eng': 'B',
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
            'cd_uo_aff_org': u1,
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
            'cd_uo_aff_org': u1,
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
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
            'personale': doc2,
        })

        url = reverse('ricerca:teacherslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'gar'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111111'

        data = {'role': 'PA', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherCVFull'] is None

        data = {'department': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': 1, 'role': 'PO'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'department': 1, 'role': 'PA', 'lang': 'en'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'regdid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'regdid': 2}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111111'

        data = {'regdid': 1, 'role': 'PA'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'cds': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0


class ApiTeacherStudyActivitiesUnitTest(TestCase):

    def test_apiteacherstudyactivitiesunittest(self):
        req = Client()
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })
        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
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
            'aa_off_id': 2019,
            'fat_part_stu_des': '111',
            'fat_part_stu_cod': 'AA',
            'part_stu_des': '11',
            'part_stu_cod': 'A',
            'tipo_fat_stu_cod': 'ALF',
            'part_ini': 'A',
            'part_fine': 'Z'
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course2,
            'personale': doc1,
            'aa_off_id': 2020,
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

        data = {'year': 2020}
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

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'uo_padre': '1',
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'aa',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMNMNG',
            'cv_full_it': 'AAA',
            'cv_short_it': 'A',
            'cv_full_eng': 'BBB',
            'cv_short_eng': 'B',

        })
        PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'PO',
            'ds_ruolo_locale': 'ab',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
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
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course1,
            'personale': p1,
            'aa_off_id': 2019,
            'fat_part_stu_des': '111',
            'fat_part_stu_cod': 'AA',
            'part_stu_des': '11',
            'part_stu_cod': 'A',
            'tipo_fat_stu_cod': 'ALF',
            'part_ini': 'A',
            'part_fine': 'Z'
        })
        tipo_contatto = PersonaleTipoContattoUnitTest.create_personaleTipoContatto(
            **{'cod_contatto': 'EMAIL', 'descr_contatto': 'Posta Elettronica', })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Riferimento Ufficio',
            'descr_contatto': 'Riferimento Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'POSTA ELETTRONICA CERTIFICATA',
            'descr_contatto': 'POSTA ELETTRONICA CERTIFICATA',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Posta Elettronica Privata',
            'descr_contatto': 'Posta Elettronica Privata',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Fax',
            'descr_contatto': 'Fax',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Residenza',
            'descr_contatto': 'Telefono Residenza',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Domicilio',
            'descr_contatto': 'Telefono Domicilio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare',
            'descr_contatto': 'Telefono Cellulare',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare Ufficio',
            'descr_contatto': 'Telefono Cellulare Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Ufficio',
            'descr_contatto': 'Telefono Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB',
            'descr_contatto': 'URL Sito WEB',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Skype',
            'descr_contatto': 'Skype',
        })

        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 1,
            'contatto': 'email@email',
            'prg_priorita': 1,
            'cod_fis': p1,

        })
        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 2,
            'contatto': 'email2@email',
            'prg_priorita': 1,
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'cod_fis': p1,
            'termine': '2222-03-26',
            'decorrenza': '1900-01-01',
            'ds_funzione': 'Direttore',
            'matricola': '111112',
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
        assert len(res.json()['results']) == 0


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

        data = {'department': 1}
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

        data = {'regdidid': '111'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'pdscod': 'GEN'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['DoctorateCdsCOD'] == '111'

        data = {'cycle': 0}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0


class ApiDegreeTypesListUnitTest(TestCase):

    def test_apidegreetypeslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'cds_id': 1,
            'tipo_corso_cod': 'L',
            'tipo_corso_des': 'Laurea',
            'cdsord_id': 1,
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'cds_id': 2,
            'tipo_corso_cod': 'LM5',
            'tipo_corso_des': 'Laurea magistrale ciclo unico',
            'cdsord_id': 2,
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'cds_id': 3,
            'tipo_corso_cod': 'LM',
            'tipo_corso_des': 'Laurea Magistrale',
            'cdsord_id': 3,
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'cds_id': 4,
            'tipo_corso_cod': 'L',
            'tipo_corso_des': 'Laurea',
            'cdsord_id': 4,
        })

        url = reverse('ricerca:degreetypes')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['CourseType'] == 'L'
        assert len(res.json()['results']) == 3


class ApiDepartmentsListUnitTest(TestCase):

    def test_apidepartmentslist(self):
        req = Client()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '001',
            'dip_des_it': 'Dipartimento di Matematica e Informatica',
            'dip_des_eng': 'Department of Math and Computer Science',
            'dip_nome_breve': 'DEMACS',
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': '002',
            'dip_des_it': 'Dipartimento di Letteratura',
            'dip_des_eng': 'Department of Literature',
            'dip_nome_breve': 'LIT',
        })

        url = reverse('ricerca:departmentslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results'][0]['DepartmentName'] == 'Department of Literature'

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['DepartmentName'] == 'Dipartimento di Letteratura'


class ApiDepartmentsFilterListUnitTest(TestCase):

    def test_apidepartmentsfilterlist(self):
        req = Client()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '001',
            'dip_des_it': 'Dipartimento di Matematica e Informatica',
            'dip_des_eng': 'Department of Math and Computer Science',
            'dip_nome_breve': 'DEMACS',
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': '002',
            'dip_des_it': 'Dipartimento di Letteratura',
            'dip_des_eng': 'Department of Literature',
            'dip_nome_breve': 'LIT',
        })

        url = reverse('ricerca:departmentsfilterlist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results'][0]['DepartmentName'] == 'Department of Literature'

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['DepartmentName'] == 'Dipartimento di Letteratura'


class ApiDepartmentDetailUnitTest(TestCase):

    def test_apidepartmentdetail(self):
        req = Client()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '001',
            'dip_des_it': 'Dipartimento di Matematica e Informatica',
            'dip_des_eng': 'Department of Math and Computer Science',
            'dip_nome_breve': 'DEMACS',
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': '002',
            'dip_des_it': 'Dipartimento di Letteratura',
            'dip_des_eng': 'Department of Literature',
            'dip_nome_breve': 'LIT',
        })

        url = reverse(
            'ricerca:departmentdetail', kwargs={
                'departmentcod': '001'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results']['DepartmentName'] == 'Department of Math and Computer Science'

        data = {'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()[
            'results']['DepartmentName'] == 'Dipartimento di Matematica e Informatica'


class ApiAddressbookStructuresListUnitTest(TestCase):

    def test_apiaddressbookstructureslist(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'uo_padre': '2',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',
            'cv_full_it': 'AAA',
            'cv_short_it': 'A',
            'cv_full_eng': 'BBB',
            'cv_short_eng': 'B',
        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'AM',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'LNL1',
            'cv_full_it': 'BBB',
            'cv_short_it': 'B',
            'cv_full_eng': 'AA',
            'cv_short_eng': 'A',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 10,
            'nome': 'Simone10',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 10,
            'matricola': '111119',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN10',

        })
        PersonaleUnitTest.create_personale(**{
            'id': 55,
            'nome': 'Simone2',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 55,
            'matricola': '111166',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN25',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 13,
            'nome': 'Simone13',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 13,
            'matricola': '1111145',
            'fl_docente': 0,
            'flg_cessato': 1,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN13',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 4,
            'nome': 'Simone4',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 4,
            'matricola': '111115',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN4',
        })
        p3 = PersonaleUnitTest.create_personale(**{
            'id': 3,
            'nome': 'Zlatan',
            'cognome': 'Ibra',
            'cd_ruolo': 'PO',
            'ds_ruolo_locale': 'Professore Ordinario',
            'id_ab': 3,
            'matricola': '111114',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': None,
            'cod_fis': 'ZLT',
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })
        tipo_contatto = PersonaleTipoContattoUnitTest.create_personaleTipoContatto(
            **{'cod_contatto': 'EMAIL', 'descr_contatto': 'Posta Elettronica', })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Riferimento Ufficio',
            'descr_contatto': 'Riferimento Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'POSTA ELETTRONICA CERTIFICATA',
            'descr_contatto': 'POSTA ELETTRONICA CERTIFICATA',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Posta Elettronica Privata',
            'descr_contatto': 'Posta Elettronica Privata',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Fax',
            'descr_contatto': 'Fax',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Residenza',
            'descr_contatto': 'Telefono Residenza',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Domicilio',
            'descr_contatto': 'Telefono Domicilio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare',
            'descr_contatto': 'Telefono Cellulare',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare Ufficio',
            'descr_contatto': 'Telefono Cellulare Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Telefono Ufficio',
            'descr_contatto': 'Telefono Ufficio',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB',
            'descr_contatto': 'URL Sito WEB',
        })
        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'Skype',
            'descr_contatto': 'Skype',
        })

        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 1,
            'cod_fis': p1,
            'contatto': 'email@email',
            'prg_priorita': 1,

        })
        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 2,
            'cod_fis': p2,
            'contatto': 'email2@email',
            'prg_priorita': 1,
        })
        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 2,
            'ds_funzione': 'Amministrazione Rettorato',
            'cod_fis': p2,
        })
        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'cod_fis': p3,
            'termine': '2222-03-26',
            'decorrenza': '1900-01-01',
            'ds_funzione': 'Direttore',
            'matricola': '111114',
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '99',
            'denominazione': 'Rettorato',
            'cd_tipo_nodo': 'AMM',
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'denominazione': 'Dipartimento di Matematica e Informatica',
        })

        url = reverse('ricerca:addressbooklist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()['results']) == 1
        assert res.json()[
            'results'][0]['Role'] == 'PO'

        data = {'structure': '99', 'lang': 'it'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'search': 'Ibra'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'search': 'Mungar', 'structure': '99'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'search': 'Mungar', 'structure': '99'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'role': 'PO'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['Name'] == 'Ibra Zlatan'

        data = {'structuretree': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'structuretree': '2'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0



class ApiStructuresListUnitTest(TestCase):

    def test_apistructureslist(self):
        req = Client()

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'rettorato',
            'cd_tipo_nodo': 'RET',
            'denominazione': 'RETTORATO',
            'uo_padre': '1',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'DIR',
            'denominazione': 'DIREZIONE',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'ds_tipo_nodo': 'uffici',
            'cd_tipo_nodo': 'UFF',
            'denominazione': 'UFFICI',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })

        url = reverse('ricerca:structureslist')

        url_filter = reverse('ricerca:structuresfilterlist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        res = req.get(url_filter)
        assert res.status_code == 200

        # GET

        res = req.get(url)

        data = {'father': 'None'}
        res = req.get(url, data=data)

        assert res.json()['results'][1]['StructureTypeName'] == 'uffici'
        assert res.json()['results'][0]['StructureCod'] == '2'
        assert len(res.json()['results']) == 2

        data = {'search': 'Direzione'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StructureCod'] == '2'

        data = {'type': 'DIR,UFF'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'type': 'DIR,UFF', 'search': 'Direzione'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'father': '1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StructureCod'] == '1'

        res = req.get(url_filter)
        assert res.json()['results'][0]['StructureTypeName'] == 'direzione'
        assert res.json()['results'][1]['StructureCod'] == '1'
        assert len(res.json()['results']) == 3

        data = {'type': 'DIR,UFF'}
        res = req.get(url_filter, data=data)
        assert len(res.json()['results']) == 2


class ApiStructuresTypesUnitTest(TestCase):

    def test_apistructurestypes(self):
        req = Client()

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'uo_padre': '1',
            'ds_tipo_nodo': 'rettorato',
            'cd_tipo_nodo': 'RET',
        })

        url = reverse('ricerca:structuretypes')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['StructureTypeName'] == 'facolta'
        assert res.json()['results'][1]['StructureTypeCOD'] == 'CDS'
        assert len(res.json()['results']) == 3

        data = {'father': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiRolesListUnitTest(TestCase):

    def test_apiroleslist(self):
        req = Client()

        PersonaleUnitTest.create_personale(**{
            'id': 1,
            'id_ab': 1,
            'matricola': '111112',
            'cd_ruolo': 'f',
            'ds_ruolo_locale': 'g',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 2,
            'id_ab': 2,
            'matricola': '111113',
            'cd_ruolo': 'g',
            'ds_ruolo_locale': 'h',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 3,
            'id_ab': 3,
            'matricola': '111115',
            'cd_ruolo': 'l',
            'ds_ruolo_locale': 'o',
        })

        url = reverse('ricerca:roleslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['Role'] == 'f'
        assert res.json()['results'][1]['RoleDescription'] == 'h'
        assert len(res.json()['results']) == 3


class ApiAcademicYearsUnitTest(TestCase):

    def test_apiacademicyears(self):
        req = Client()

        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'aa_reg_did': 2015,
        })
        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 2,
            'aa_reg_did': 2016,
        })
        DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 3,
            'aa_reg_did': 2017,
        })

        url = reverse('ricerca:academicyears')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert res.json()['results'][1]['AcademicYear'] == 2016
        assert len(res.json()['results']) == 3


class ApiPersonaleDetailUnitTest(TestCase):

    def test_apipersonaledetail(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',
            'cv_full_it': 'AAA',
            'cv_short_it': 'A',
            'cv_full_eng': 'BBB',
            'cv_short_eng': 'B',

        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'AM',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'LNL1',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 3,
            'nome': 'A',
            'cognome': 'B',
            'cd_ruolo': 'AB',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 3,
            'matricola': '111114',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cod_fis': 'AB',
        })

        tipo_contatto = PersonaleTipoContattoUnitTest.create_personaleTipoContatto(
            **{'cod_contatto': 'EMAIL', 'descr_contatto': 'Posta Elettronica', })

        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 1,
            'cod_fis': p1,
            'prg_priorita': 1
        })
        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': 2,
            'cod_fis': p2,
            'prg_priorita': 2
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 1,
            'ds_funzione': 'Amministrazione',
            'termine': "2999-12-1",
            'cod_fis': p1

        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 2,
            'ds_funzione': 'Delega',
            'termine': None,
            'cod_fis': p2,
        })

        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'denominazione': 'Dipartimento di Matematica e Informatica',
        })

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '99',
            'denominazione': 'Dipartimento di Matematica e Informatica',
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'cod_fis': p1,
            'termine': '2222-03-26',
            'decorrenza': '1900-01-01',
            'ds_funzione': 'Direttore',
            'matricola': '111112',
        })

        url = reverse(
            'ricerca:personaledetail', kwargs={
                'personaleid': "111112"})
        url1 = reverse(
            'ricerca:personaledetail', kwargs={
                'personaleid': "111113"})
        url2 = reverse(
            'ricerca:personaledetail', kwargs={
                'personaleid': "111114"})

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

        assert res.json()['results']['TeacherCVFull'] == "BBB"
        assert res.json()['results']['ID'] == "111112"
        assert res1.json()['results']['ID'] == "111113"


class ApiStructureDetailUnitTest(TestCase):

    def test_apistructuredetail(self):
        req = Client()
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',
            'cd_csa': '1',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
            'cd_csa': '2',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',

        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'AM',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'LNL1',
        })

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'ds_tipo_nodo': 'rettorato',
            'cd_tipo_nodo': 'RET',
            'id_ab': 3,
            'denominazione': 'ccc',
            'denominazione_padre': 'd',
            'uo_padre': '33',
        })

        tipo_contatto = PersonaleTipoContattoUnitTest.create_personaleTipoContatto(
            **{'cod_contatto': 'PEC', 'descr_contatto': 'Posta Elettronica Certificata', })

        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })

        UnitaOrganizzativaContattiUnitTest.create_unitaOrganizzativaContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': u1,
            'prg_priorita': 1,

        })

        UnitaOrganizzativaContattiUnitTest.create_unitaOrganizzativaContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': u2,
            'prg_priorita': 2,
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 1,
            'ds_funzione': 'Amministrazione',
            'termine': "2999-12-1",
            'cod_fis': p1,
            'cd_csa': u1,
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 2,
            'ds_funzione': 'Delega',
            'termine': None,
            'cod_fis': p2,
            'cd_csa': u2,
        })

        url = reverse('ricerca:structuredetail', kwargs={
            'structureid': "1"})

        url1 = reverse('ricerca:structuredetail', kwargs={
            'structureid': "2"})

        # check url
        res = req.get(url)
        res1 = req.get(url1)

        assert res.status_code == 200
        assert res1.status_code == 200

        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert res.json()['results']['StructureCod'] == '1'
        assert res1.json()['results']['StructureCod'] == '2'


class ApiLaboratoriesListUnitTest(TestCase):
    def test_apilaboratorieslist(self):
        req = Client()

        dip1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '1',
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })

        dip2 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': '2',
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'responsabile',
            'id_ab': 1,
            'matricola': '111111',
        })

        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Carmine',
            'cognome': 'Carlucci',
            'cd_ruolo': 'responsabile',
            'id_ab': 2,
            'matricola': '111112',
        })

        lab2 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'id_dipartimento_riferimento': dip1,
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
            'matricola_responsabile_scientifico': p1,
            'laboratorio_interdipartimentale': 'SI',
        })

        a1 = LaboratorioTipologiaAttivitaUnitTest.create_laboratorioTipologiaAttivita(
            **{"id": 2, "descrizione": "ricerca", })

        LaboratorioAttivitaUnitTest.create_laboratorioAttivita(**{
            "id": 2,
            "id_laboratorio_dati": lab2,
            "id_tipologia_attivita": a1,
        })

        LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 2,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Scientifico',
            'dipartimento_riferimento': 'Matematica',
            'id_dipartimento_riferimento': dip2,
            'sede_dimensione': "291",
            'responsabile_scientifico': 'Carlucci Carmine',
            'matricola_responsabile_scientifico': p2,
        })

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })

        erc1_1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })

        LaboratorioPersonaleRicercaUnitTest.create_laboratorioPersonaleRicerca(**{
            'id': 1,
            'id_laboratorio_dati': lab2,
            'matricola_personale_ricerca': p2,
        })

        lab1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 3,
            'matricola_referente_compilazione': p1,
            'nome_laboratorio': 'LAB2',
            'id_dipartimento_riferimento': dip2,
            'ambito': 'Tecnologico',
            'matricola_responsabile_scientifico': p2,
        })

        a1 = LaboratorioTipologiaAttivitaUnitTest.create_laboratorioTipologiaAttivita(
            **{"id": 1, "descrizione": "aaa"})
        LaboratorioAttivitaUnitTest.create_laboratorioAttivita(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            "id_tipologia_attivita": a1
        })

        LaboratorioPersonaleTecnicoUnitTest.create_laboratorioPersonaleTecnico(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'matricola_personale_tecnico': p1,
            'ruolo': 'R1'
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 3,
            'id_laboratorio_dati': lab1,
            'id_ricerca_erc1': erc1_1,
        })

        LaboratorioAltriDipartimentiUnitTest.create_laboratorioAltriDipartimenti(
            **{'id': 1, 'id_laboratorio_dati': lab2, 'id_dip': dip1, })

        url = reverse('ricerca:laboratorieslist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {'department': '1', 'teacher': '111111'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 1
        assert res.json()[
            'results'][0]['ScientificDirector'] == 'Mungari Simone'

        data = {'teacher': '111111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'scope': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111112'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 3

        data = {'teacher': '111112', 'scope': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111111', 'scope': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': '2', 'area': 'Scientifico'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 2
        assert res.json()[
            'results'][0]['ScientificDirector'] == 'Carlucci Carmine'

        data = {'area': 'Tecnico'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 1
        assert res.json()['results'][0]['Dimension'] == '290'

        data = {'area': 'Scientifico'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 2
        assert res.json()['results'][0]['Dimension'] == '291'

        data = {'search': 'Informatica'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 1
        assert res.json()['results'][0]['Dimension'] == '290'
        assert res.json()[
            'results'][0]['ScientificDirector'] == 'Mungari Simone'

        data = {'erc1': 'cod1_erc1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 3

        res = req.get(url)
        assert len(res.json()['results']) == 3


class ApiLaboratoryDetailUnitTest(TestCase):

    def test_apilaboratorydetail(self):
        req = Client()
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',

        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'AM',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'LNL1',
        })
        dip1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })
        dip2 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 2,
            'dip_cod': 2,
            'dip_des_it': "Lettere e filosofia",
            'dip_des_eng': "Philosophy",
        })
        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        erc1_1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        erc1_2 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc2',
            'descrizione': 'Poetica Platone',
            'ricerca_erc0_cod': erc0,
        })

        lab1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'matricola_referente_compilazione': p1,
            'nome_laboratorio': 'LAB1',
            'id_dipartimento_riferimento': dip1,
            'ambito': 'Tecnologico',
            'matricola_responsabile_scientifico': p1,
            'laboratorio_interdipartimentale': 'SI',
        })

        lab2 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 2,
            'matricola_referente_compilazione': p2,
            'nome_laboratorio': 'LAB2',
            'id_dipartimento_riferimento': dip2,
            'ambito': 'Umanistico',
            'matricola_responsabile_scientifico': p2,
        })
        a1 = LaboratorioTipologiaAttivitaUnitTest.create_laboratorioTipologiaAttivita(
            **{"id": 1, "descrizione": "aaa"})
        LaboratorioAttivitaUnitTest.create_laboratorioAttivita(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            "id_tipologia_attivita": a1
        })
        LaboratorioAttivitaUnitTest.create_laboratorioAttivita(**{
            'id': 2,
            'id_laboratorio_dati': lab1,
            "id_tipologia_attivita": a1

        })
        LaboratorioAttivitaUnitTest.create_laboratorioAttivita(**{
            'id': 3,
            'id_laboratorio_dati': lab2,
            "id_tipologia_attivita": a1
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'id_ricerca_erc1': erc1_1,
        })
        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 2,
            'id_laboratorio_dati': lab2,
            'id_ricerca_erc1': erc1_2,
        })

        LaboratorioPersonaleRicercaUnitTest.create_laboratorioPersonaleRicerca(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'matricola_personale_ricerca': p2,
        })
        LaboratorioPersonaleRicercaUnitTest.create_laboratorioPersonaleRicerca(**{
            'id': 2,
            'id_laboratorio_dati': lab1,
            'matricola_personale_ricerca': p2,
        })
        LaboratorioPersonaleRicercaUnitTest.create_laboratorioPersonaleRicerca(**{
            'id': 3,
            'id_laboratorio_dati': lab2,
            'matricola_personale_ricerca': p1,
        })
        LaboratorioPersonaleRicercaUnitTest.create_laboratorioPersonaleRicerca(**{
            'id': 4,
            'id_laboratorio_dati': lab2,
            'matricola_personale_ricerca': p1,
        })

        LaboratorioPersonaleTecnicoUnitTest.create_laboratorioPersonaleTecnico(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'matricola_personale_tecnico': p1,
            'ruolo': 'R1'
        })
        LaboratorioPersonaleTecnicoUnitTest.create_laboratorioPersonaleTecnico(**{
            'id': 2,
            'id_laboratorio_dati': lab1,
            'matricola_personale_tecnico': p1,
            'ruolo': 'R2'
        })
        LaboratorioPersonaleTecnicoUnitTest.create_laboratorioPersonaleTecnico(**{
            'id': 3,
            'id_laboratorio_dati': lab2,
            'matricola_personale_tecnico': p2,
            'ruolo': 'R1'
        })
        LaboratorioPersonaleTecnicoUnitTest.create_laboratorioPersonaleTecnico(**{
            'id': 4,
            'id_laboratorio_dati': lab2,
            'matricola_personale_tecnico': p2,
            'ruolo': 'R2'
        })

        LaboratorioServiziOffertiUnitTest.create_laboratorioServiziOfferti(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'nome_servizio': "S1"
        })
        LaboratorioServiziOffertiUnitTest.create_laboratorioServiziOfferti(**{
            'id': 2,
            'id_laboratorio_dati': lab2,
            'nome_servizio': "S2"
        })

        LaboratorioUbicazioneUnitTest.create_laboratorioUbicazione(**{
            'id': 1,
            'id_laboratorio_dati': lab1,
            'edificio': '31B',
            'piano': '1',
        })

        LaboratorioAltriDipartimentiUnitTest.create_laboratorioAltriDipartimenti(
            **{'id': 1, 'id_laboratorio_dati': lab1, 'id_dip': dip2, })

        url = reverse('ricerca:laboratorydetail', kwargs={
            'laboratoryid': "1"})

        url1 = reverse('ricerca:laboratorydetail', kwargs={
            'laboratoryid': "2"})

        # check url
        res = req.get(url)
        res1 = req.get(url1)

        assert res.status_code == 200
        assert res1.status_code == 200

        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert res.json()['results']['LaboratoryId'] == 1
        assert res1.json()['results']['LaboratoryId'] == 2

        assert res.json()[
            'results']['DepartmentReferentName'] == 'Math and Computer Science'
        assert res1.json()['results']['LaboratoryScope'] == 'Umanistico'

        assert len(res.json()['results']['LaboratoryResearchPersonnel']) == 2
        assert len(res1.json()['results']['LaboratoryTechPersonnel']) == 2


class ApiLaboratoriesAreasListUnitTest(TestCase):

    def test_apiLaboratoriesAreasList(self):
        req = Client()

        LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'LAB1',
            'ambito': 'Tecnologico',
        })

        LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 2,
            'nome_laboratorio': 'LAB2',
            'ambito': 'Umanistico',
        })

        url = reverse('ricerca:laboratoriesareas')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()['results']) == 2


class ApiErc1ListUnitTest(TestCase):

    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        erc1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        l1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 1,
            'id_laboratorio_dati': l1,
            'id_ricerca_erc1': erc1,
        })

        url = reverse('ricerca:erc1list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {'laboratory': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        assert len(res.json()['results']) == 1


class ApiErc1FilterListUnitTest(TestCase):

    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        erc1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        l1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 1,
            'id_laboratorio_dati': l1,
            'id_ricerca_erc1': erc1,
        })

        url = reverse('ricerca:erc1filterlist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {'laboratory': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        assert len(res.json()['results']) == 1


class ApiErc2ListUnitTest(TestCase):

    def test_apiLaboratoriesAreasList(self):
        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        erc1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        l1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 1,
            'id_laboratorio_dati': l1,
            'id_ricerca_erc1': erc1,
        })
        RicercaErc2UnitTest.create_ricercaErc2(**{
            'cod_erc2': 'cod_erc2',
            'descrizione': 'Sicurezza Informatica',
            'ricerca_erc1': erc1

        })
        url = reverse('ricerca:erc2list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        data = {'laboratory': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        assert len(res.json()['results']) == 1


class ApiErc0ListUnitTest(TestCase):

    def test_apiLaboratoriesAreasList(self):

        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })

        erc01 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '112',
            'description': 'ITA',
            'description_en': 'ITA',
        })

        erc1 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })

        l1 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 1,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 1,
            'id_laboratorio_dati': l1,
            'id_ricerca_erc1': erc1,
        })

        erc12 = RicercaErc1UnitTest.create_ricercaErc1(**{
            'cod_erc1': 'cod1_erc12',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc01,
        })

        l2 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 2,
            'nome_laboratorio': 'Informatica',
            'ambito': 'Tecnico',
            'dipartimento_riferimento': 'Informatica',
            'sede_dimensione': "291",
            'responsabile_scientifico': 'Mungari Simone',
        })

        LaboratorioDatiErc1UnitTest.create_laboratorioDatiErc1(**{
            'id': 2,
            'id_laboratorio_dati': l2,
            'id_ricerca_erc1': erc12,
        })

        url = reverse('ricerca:erc0list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert res.json()['results'][0]['IdErc0'] == '111'

        assert len(res.json()['results']) == 2


class ApiPublicationsListUnitTest(TestCase):

    def test_apiPublicationsList(self):
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',
        })

        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 2,
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN2',
        })

        p3 = PersonaleUnitTest.create_personale(**{
            'id': 3,
            'nome': 'Simone',
            'cognome': 'Pino',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 3,
            'fl_docente': 1,
            'matricola': '111119',
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN3',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 1,
            'community_name': 'Community 1',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 2,
            'community_name': 'Community 2',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 1,
            'community_id': 1,
            'collection_name': 'Collection 1',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 2,
            'community_id': 2,
            'collection_name': 'Collection 2',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 1,
            'title': 'pub1',
            'des_abstract': 'abstract italiano',
            'des_abstracteng': 'abstract inglese',
            'date_issued_year': 2020,
            'pubblicazione': 'Giornale 1',
            'label_pubblicazione': 'Rivista',
            'collection_id': 1,
            'url_pubblicazione': 'aaa',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 2,
            'title': 'pub2',
            'des_abstract': 'abstract italiano2',
            'des_abstracteng': 'abstract inglese2',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
            'url_pubblicazione': 'aba',

        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 3,
            'title': 'pub3',
            'des_abstract': 'abstract italiano3',
            'des_abstracteng': 'abstract inglese3',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
            'url_pubblicazione': 'ccc',

        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 1,
            'id_ab': p1,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 3,
            'id_ab': p2,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 1,
            'id_ab': p3,
        })

        req = Client()

        url = reverse('ricerca:publications', kwargs={'teacherid': '111112'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()[
            'results'][0]['PublicationAbstract'] == 'abstract inglese'

        data = {
            'year': 2020,
            'search': 'pub',
            'type': 1,
            'contributor': '111119'}

        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiPublicationsCommunityTypesListUnitTest(TestCase):

    def test_apiPublicationsCommunityTypesList(self):
        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 1,
            'community_name': 'Comm 1',
        })
        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 2,
            'community_name': 'Comm 2',
        })

        req = Client()

        url = reverse('ricerca:publicationscommunitytypes')

        # check url
        res = req.get(url)

        assert res.status_code == 200
        assert res.json()['results'][0]['CommunityName'] == 'Comm 1'


class ApiPublicationDetailUnitTest(TestCase):

    def test_apiPublicationDetail(self):
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',
        })

        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 2,
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN2',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 1,
            'community_name': 'Community 1',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 2,
            'community_name': 'Community 2',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 1,
            'community_id': 1,
            'collection_name': 'Collection 1',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 2,
            'community_id': 2,
            'collection_name': 'Collection 2',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 1,
            'title': 'pub1',
            'des_abstract': 'abstract italiano',
            'des_abstracteng': 'abstract inglese',
            'date_issued_year': 2020,
            'pubblicazione': 'Giornale 1',
            'label_pubblicazione': 'Rivista',
            'collection_id': 1,
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 2,
            'title': 'pub2',
            'des_abstract': 'abstract italiano2',
            'des_abstracteng': 'abstract inglese2',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 3,
            'title': 'pub3',
            'des_abstract': 'abstract italiano3',
            'des_abstracteng': 'abstract inglese3',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 1,
            'id_ab': p1,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 3,
            'id_ab': p2,
        })

        req = Client()

        url = reverse(
            'ricerca:publicationdetail',
            kwargs={
                'teacherid': '111112',
                'publicationid': '1'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()[
            'results']['PublicationAbstract'] == 'abstract inglese'

        url = reverse(
            'ricerca:publicationdetail',
            kwargs={
                'teacherid': '111112',
                'publicationid': '2'})

        res = req.get(url)
        assert res.json()['results']['PublicationYear'] == 2019


class ApiResearchGroupsUnitTest(TestCase):

    def test_apiresearchgroups(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'ds_sede': 'DIMES',
            'sede': '1111',

        })
        ricerca_gruppo1 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 1,
            'nome': 'Intelligenza Artificiale',
            'descrizione': 'ricerca su Machine Learning',

        })

        RicercaDocenteGruppoUnitTest.create_ricercaDocenteGruppo(**{
            'personale': doc1,
            'ricerca_gruppo': ricerca_gruppo1
        })

        url = reverse(
            'ricerca:researchgroups')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['RGroupID'] == 1

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111112'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'search': 'Intel'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiBaseResearchLineUnitTest(TestCase):

    def test_apibaseresearchline(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'ds_sede': 'DIMES',
            'sede': '1111'
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
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2020',
            'anno': '2016',

        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc1,
            'ricerca_linea_base': linea_base
        })

        url = reverse('ricerca:baseresearchlines')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results'][0]['RLineDescription'] == 'regressione lineare'

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'search': 'reg'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'year': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'teacher': '111112', 'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111112'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiAppliedResearchLineUnitTest(TestCase):

    def test_apiappliedresearchline(self):
        req = Client()

        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'ds_sede': 'DIMES',
            'sede': '1111'
        })

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
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
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2020',
            'anno': '2016'
        })

        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc1,
            'ricerca_linea_applicata': linea_applicata,
            'dt_ins': '2021-01-03 15:47:21'
        })

        url = reverse('ricerca:appliedresearchlines')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()[
            'results'][0]['RLineDescription'] == 'regressione lineare'

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'search': 'reg'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'year': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'teacher': '111112'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': '111112', 'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiTeachingsCoveragesListUnitTest(TestCase):

    def test_apiteachingCoverageslistunittest(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
        })
        doc1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
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
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cv_full_it': 'AAA',
            'cv_short_it': 'A',
            'cv_full_eng': 'BBB',
            'cv_short_eng': 'B',
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
            'cd_uo_aff_org': u1,
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
            'cd_uo_aff_org': u2,
        })

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
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
            'personale': doc2,
        })

        url = reverse('ricerca:teachingcoverageslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'gar'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111111'

        data = {'role': 'PA', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherCVFull'] is None

        data = {'department': 42}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'department': 1, 'role': 'PO'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'department': 1, 'role': 'PA', 'lang': 'en'}
        res = req.get(url, data=data)
        assert res.json()[
            'results'][0]['TeacherDepartmentName'] == "Math and Computer Science"

        data = {'regdid': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'regdid': 2}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111111'

        data = {'regdid': 1, 'role': 'PA'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherID'] == '111112'

        data = {'cds': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0


class ApiAllPublicationsListUnitTest(TestCase):

    def test_apiAllPublicationsList(self):

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 1,
            'community_name': 'Community 1',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 2,
            'community_name': 'Community 2',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 1,
            'community_id': 1,
            'collection_name': 'Collection 1',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 2,
            'community_id': 2,
            'collection_name': 'Collection 2',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 1,
            'title': 'pub1',
            'des_abstract': 'abstract italiano',
            'des_abstracteng': 'abstract inglese',
            'date_issued_year': 2020,
            'pubblicazione': 'Giornale 1',
            'contributors': 'Pinnola',
            'label_pubblicazione': 'Rivista',
            'collection_id': 1,
            'url_pubblicazione': 'aaa',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 2,
            'title': 'pub2',
            'des_abstract': 'abstract italiano2',
            'des_abstracteng': 'abstract inglese2',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
            'url_pubblicazione': 'aba',

        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 3,
            'title': 'pub3',
            'des_abstract': 'abstract italiano3',
            'des_abstracteng': 'abstract inglese3',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
            'url_pubblicazione': 'ccc',

        })

        req = Client()

        url = reverse('ricerca:publicationslist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()[
            'results'][0]['PublicationAbstract'] == 'abstract inglese'

        data = {
            'year': 2020,
            'search': 'pub',
            'type': 1,
            'contributors': 'Pinnola'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiPublicationInfoUnitTest(TestCase):

    def test_apiPublicationInfo(self):
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',

        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',
        })

        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 2,
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'SMN2',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 1,
            'community_name': 'Community 1',
        })

        PubblicazioneCommunityUnitTest.create_pubblicazioneCommunity(**{
            'community_id': 2,
            'community_name': 'Community 2',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 1,
            'community_id': 1,
            'collection_name': 'Collection 1',
        })

        PubblicazioneCollectionUnitTest.create_pubblicazioneCollection(**{
            'collection_id': 2,
            'community_id': 2,
            'collection_name': 'Collection 2',
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 1,
            'title': 'pub1',
            'des_abstract': 'abstract italiano',
            'des_abstracteng': 'abstract inglese',
            'date_issued_year': 2020,
            'pubblicazione': 'Giornale 1',
            'label_pubblicazione': 'Rivista',
            'collection_id': 1,
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 2,
            'title': 'pub2',
            'des_abstract': 'abstract italiano2',
            'des_abstracteng': 'abstract inglese2',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
        })

        PubblicazioneDatiBaseUnitTest.create_pubblicazioneDatiBase(**{
            'item_id': 3,
            'title': 'pub3',
            'des_abstract': 'abstract italiano3',
            'des_abstracteng': 'abstract inglese3',
            'date_issued_year': 2019,
            'pubblicazione': 'Convegno Cosenza',
            'label_pubblicazione': 'Convegno',
            'collection_id': 2,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 1,
            'id_ab': p1,
        })

        PubblicazioneAutoriUnitTest.create_pubblicazioneAutori(**{
            'item_id': 3,
            'id_ab': p2,
        })

        req = Client()

        url = reverse(
            'ricerca:publicationinfo',
            kwargs={
                'publicationid': '1'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET
        assert res.json()[
            'results']['PublicationAbstract'] == 'abstract inglese'

        url = reverse('ricerca:publicationinfo', kwargs={'publicationid': '1'})
        res = req.get(url)
        assert res.json()['results']['PublicationYear'] == 2020

        url = reverse('ricerca:publicationinfo', kwargs={'publicationid': '3'})
        res = req.get(url)
        assert res.json()['results']['PublicationYear'] == 2019


class ApiAllStructuresListUnitTest(TestCase):

    def test_apiallstructureslist(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'rettorato',
            'cd_tipo_nodo': 'RET',
            'denominazione': 'RETTORATO',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'DIR',
            'denominazione': 'DIREZIONE',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })
        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'ds_tipo_nodo': 'uffici',
            'cd_tipo_nodo': 'UFF',
            'denominazione': 'UFFICI',
            'dt_fine_val': datetime.datetime.today() + datetime.timedelta(days=1),
        })
        PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
            'cd_uo_aff_org': u1,
        })

        url = reverse('ricerca:allstructureslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 0

        data = {'search': 'Direzione'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'type': 'DIR,UFF'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'father': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'father': 'None'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0


class ApiAddressbookStructureDetailUnitTest(TestCase):

    def test_apiaddressbookstructuredetail(self):
        req = Client()
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',
            'cd_csa':1,
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
            'cd_csa':2,
        })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'ds_ruolo_locale': 'Professore Associato',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'cod_fis': 'SMN1',

        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Lionel',
            'cognome': 'Messi',
            'cd_ruolo': 'AM',
            'ds_ruolo_locale': 'Amministrazione',
            'id_ab': 2,
            'matricola': '111113',
            'fl_docente': 0,
            'flg_cessato': 0,
            'cd_uo_aff_org': u2,
            'cod_fis': 'LNL1',
        })

        UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'ds_tipo_nodo': 'rettorato',
            'cd_tipo_nodo': 'RET',
            'id_ab': 3,
            'denominazione': 'ccc',
            'denominazione_padre': 'd',
            'uo_padre': '33',
            'cd_csa': 3,
        })

        tipo_contatto = PersonaleTipoContattoUnitTest.create_personaleTipoContatto(
            **{'cod_contatto': 'PEC', 'descr_contatto': 'Posta Elettronica Certificata', })

        PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })

        UnitaOrganizzativaContattiUnitTest.create_unitaOrganizzativaContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': u1,
            'prg_priorita': 1,

        })

        UnitaOrganizzativaContattiUnitTest.create_unitaOrganizzativaContatti(**{
            'cd_tipo_cont': tipo_contatto,
            'id_ab': u2,
            'prg_priorita': 2,
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 1,
            'ds_funzione': 'Amministrazione',
            'termine': "2999-12-1",
            'cod_fis': p1,
            'cd_csa': u1,
        })

        UnitaOrganizzativaFunzioniUnitTest.create_unitaOrganizzativaFunzioni(**{
            'id_ab': 2,
            'ds_funzione': 'Delega',
            'termine': None,
            'cod_fis': p2,
            'cd_csa': u2,
        })

        url = reverse('ricerca:addressbookstructuredetail', kwargs={
            'structureid': "1"})

        url1 = reverse('ricerca:addressbookstructuredetail', kwargs={
            'structureid': "2"})

        # check url
        res = req.get(url)
        res1 = req.get(url1)

        assert res.status_code == 200
        assert res1.status_code == 200

        # GET

        res = req.get(url)
        res1 = req.get(url1)

        assert res.json()['results']['StructureCod'] == '1'
        assert res1.json()['results']['StructureCod'] == '2'


class ApiInfrastructuresListUnitTest(TestCase):

    def test_apiinfrastrucureslist(self):

        req = Client()

        LaboratorioInfrastrutturaUnitTest.create_laboratorioInfrastruttura(**{
            "id": 1,
            "descrizione": "SILA"
        })

        url = reverse('ricerca:infrastructures')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()['results']) == 1


class ApiLaboratoriesScopesListUnitTest(TestCase):

    def test_apilaboratoriesscopeslist(self):

        req = Client()

        LaboratorioTipologiaAttivitaUnitTest.create_laboratorioTipologiaAttivita(
            **{"id": 1, "descrizione": "Ricerca"})

        url = reverse('ricerca:laboratories-scopes')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()['results']) == 1


class ApiPatentsListUnitTest(TestCase):

    def test_apipatentslist(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })
        b1 = BrevettoDatiBaseUnitTest.create_brevettoDatiBase(**{
            "id": 1,
            "id_univoco": '100010',
            "titolo": 'Ingegneria del sw',
            "url_immagine": 'aaaa',
            "breve_descrizione": 'applicazione',
            "url_knowledge_share": 'aaaa',
            "id_area_tecnologica": t1,
        })

        BrevettoInventoriUnitTest.create_brevettoInventori(**{
            "id": 1,
            "id_brevetto": b1,
            "matricola_inventore": p,
            "cognomenome_origine": "garofalo"
        })

        url = reverse('ricerca:patents')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert len(res.json()['results']) == 1

        data = {'search': 'sw'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'techarea': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiPatentDetailUnitTest(TestCase):

    def test_apipatentdetail(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })
        b1 = BrevettoDatiBaseUnitTest.create_brevettoDatiBase(**{
            "id": 1,
            "id_univoco": '100010',
            "titolo": 'Ingegneria del sw',
            "url_immagine": 'aaaa',
            "breve_descrizione": 'applicazione',
            "url_knowledge_share": 'aaaa',
            "id_area_tecnologica": t1,
        })

        BrevettoInventoriUnitTest.create_brevettoInventori(**{
            "id": 1,
            "id_brevetto": b1,
            "matricola_inventore": p,
            "cognomenome_origine": "garofalo"
        })

        url = reverse('ricerca:patentdetail', kwargs={'patentid': '1'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)

        assert res.json()['results']['PatentId'] == 1


class ApiCompaniesListUnitTest(TestCase):

    def test_apicompanieslist(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        SpinoffStartupDatiBaseUnitTest.create_spinoffStartupDatiBase(**{
            "id": 1,
            "piva": '1111sc',
            "nome_azienda": 'Revelis',
            "nome_file_logo": 'aaaa',
            "url_sito_web": 'bbbb',
            "descrizione_ita": 'applicazione',
            "descrizione_eng": "description",
            "id_area_tecnologica": t1,
            "referente_unical": "Garofalo",
            "matricola_referente_unical": p,
            "is_spinoff": 1,
            "is_startup": 0,
        })

        url = reverse('ricerca:companies')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'search': 'appl', 'spinoff': '1', 'startup': '0'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'techarea': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiCompanyDetailUnitTest(TestCase):

    def test_apicompanydetail(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        SpinoffStartupDatiBaseUnitTest.create_spinoffStartupDatiBase(**{
            "id": 1,
            "piva": '1111sc',
            "nome_azienda": 'Revelis',
            "nome_file_logo": 'aaaa',
            "url_sito_web": 'bbbb',
            "descrizione_ita": 'applicazione',
            "descrizione_eng": "description",
            "id_area_tecnologica": t1,
            "referente_unical": "Garofalo",
            "matricola_referente_unical": p,
            "is_spinoff": 1,
            "is_startup": 0,
        })

        url = reverse('ricerca:companydetail', kwargs={'companyid': '1'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['SpinoffId'] == 1


class ApiTechAreasListUnitTest(TestCase):

    def test_apitechareaslist(self):

        req = Client()

        TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        url = reverse('ricerca:techareaslist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiProjectsListUnitTest(TestCase):

    def test_apiprojectslist(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        a1 = ProgettoAmbitoTerritorialeUnitTest.create_progettoAmbitoTerritoriale(
            **{"id": 1, "ambito_territoriale": "europeo", })

        p1 = ProgettoTipologiaProgrammaUnitTest.create_progettoTipologiaProgramma(
            **{"id": 1, "nome_programma": "AAA"})

        ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
            "id": 1,
            "id_ambito_territoriale": a1,
            "id_tipologia_programma": p1,
            "titolo": "Motore",
            "descr_breve": "Mot",
            "abstract_ita": "Motore",
            "abstract_eng": "Engine",
            "id_area_tecnologica": t1,
        })

        ProgettoResponsabileScientificoUnitTest.create_progettoResponsabileScientifico(
            **{"matricola": p, "nome_origine": "Simone", "id_progetto": 1, })

        url = reverse('ricerca:projects')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'search': 'mot'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'techarea': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiProjectDetailUnitTest(TestCase):

    def test_apiprojectdetail(self):

        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        a1 = ProgettoAmbitoTerritorialeUnitTest.create_progettoAmbitoTerritoriale(
            **{"id": 1, "ambito_territoriale": "europeo", })

        p1 = ProgettoTipologiaProgrammaUnitTest.create_progettoTipologiaProgramma(
            **{"id": 1, "nome_programma": "AAA"})

        ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
            "id": 1,
            "id_ambito_territoriale": a1,
            "id_tipologia_programma": p1,
            "titolo": "Motore",
            "descr_breve": "Mot",
            "abstract_ita": "Motore",
            "abstract_eng": "Engine",
            "id_area_tecnologica": t1,
        })

        ProgettoResponsabileScientificoUnitTest.create_progettoResponsabileScientifico(
            **{"matricola": p, "nome_origine": "Simone", "id_progetto": 1, })

        url = reverse('ricerca:projectdetail', kwargs={'projectid': '1'})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['ProjectId'] == 1


class ApiStructureFunctionsListUnitTest(TestCase):

    def test_apistructurefunctionslist(self):

        req = Client()

        UnitaOrganizzativaTipoFunzioniUnitTest.create_unitaOrganizzativaTipoFunzioni(
            **{"cd_tipo_nod": 'apl', "funzione": "nbb45", "descr_funzione": "aaa", })

        url = reverse('ricerca:functions')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1
