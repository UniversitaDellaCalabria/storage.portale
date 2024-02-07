import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.authtoken.models import Token

from . models import SitoWebCdsTipoDato
from . utils import encrypt, decrypt
from . util_test import ComuniAllUnitTest, DidatticaAttivitaFormativaUnitTest, DidatticaCdsLinguaUnitTest, \
    DidatticaCdsUnitTest, DidatticaCoperturaUnitTest, DidatticaDipartimentoUnitTest, DidatticaPdsRegolamentoUnitTest, \
    DidatticaRegolamentoUnitTest, DidatticaTestiAfUnitTest, DidatticaTestiRegolamentoUnitTest, PersonaleUnitTest, \
    RicercaAster1UnitTest, RicercaAster2UnitTest, RicercaDocenteGruppoUnitTest, RicercaDocenteLineaApplicataUnitTest, \
    RicercaDocenteLineaBaseUnitTest, RicercaErc1UnitTest, RicercaErc2UnitTest, RicercaGruppoUnitTest, \
    RicercaLineaApplicataUnitTest, RicercaLineaBaseUnitTest, TerritorioItUnitTest, RicercaErc0UnitTest, \
    DidatticaDottoratoCdsUnitTest, DidatticaDottoratoPdsUnitTest, DidatticaDottoratoRegolamentoUnitTest, \
    PersonaleUoTipoContattoUnitTest, PersonaleContattiUnitTest, UnitaOrganizzativaFunzioniUnitTest, \
    UnitaOrganizzativaUnitTest, UnitaOrganizzativaContattiUnitTest, LaboratorioDatiBaseUnitTest, \
    LaboratorioAttivitaUnitTest, LaboratorioDatiErc1UnitTest, LaboratorioPersonaleRicercaUnitTest, \
    LaboratorioPersonaleTecnicoUnitTest, LaboratorioServiziOffertiUnitTest, LaboratorioUbicazioneUnitTest, \
    LaboratorioAltriDipartimentiUnitTest, PubblicazioneDatiBaseUnitTest, PubblicazioneCommunityUnitTest, \
    PubblicazioneCollectionUnitTest, PubblicazioneAutoriUnitTest, LaboratorioInfrastrutturaUnitTest, LaboratorioTipologiaAttivitaUnitTest, \
    BrevettoDatiBaseUnitTest, BrevettoInventoriUnitTest, TipologiaAreaTecnologicaUnitTest, SpinoffStartupDatiBaseUnitTest, \
    ProgettoDatiBaseUnitTest, ProgettoTipologiaProgrammaUnitTest, ProgettoAmbitoTerritorialeUnitTest, ProgettoResponsabileScientificoUnitTest,\
    UnitaOrganizzativaTipoFunzioniUnitTest, ProgettoRicercatoreUnitTest, AltaFormazioneDatiBaseUnitTest, AltaFormazioneTipoCorsoUnitTest, AltaFormazioneModalitaErogazioneUnitTest,\
    AltaFormazioneModalitaSelezioneUnitTest, AltaFormazionePartnerUnitTest, AltaFormazioneConsiglioScientificoEsternoUnitTest, AltaFormazioneConsiglioScientificoInternoUnitTest, \
    AltaFormazioneIncaricoDidatticoUnitTest, AltaFormazionePianoDidatticoUnitTest, DidatticaCdsAltriDatiUnitTest, DidatticaCdsAltriDatiUfficioUnitTest, DidatticaAttivitaFormativaModalitaUnitTest, \
    DidatticaCoperturaDettaglioOreUnitTest, DidatticaDottoratoAttivitaFormativaUnitTest, DidatticaDottoratoAttivitaFormativaAltriDocentiUnitTest, \
    DidatticaDottoratoAttivitaFormativaDocenteUnitTest, SpinoffStartupDipartimentoUnitTest, PersonaleAttivoTuttiRuoliUnitTest, PersonalePrioritaRuoloUnitTest, DocentePtaMaterialeDidatticoUnitTest, \
    DocentePtaBachecaUnitTest, DocentePtaAltriDatiUnitTest, SitoWebCdsDatiBaseUnitTest, SitoWebCdsSliderUnitTest, SitoWebCdsExStudentiUnitTest, SitoWebCdsLinkUnitTest, SitoWebCdsTopicListUnitTest, \
    SitoWebCdsTopicArticoliRegAltriDatiUnitTest, SitoWebCdsArticoliRegolamentoUnitTest, SitoWebCdsTopicArticoliRegUnitTest, SitoWebCdsOggettiPortaleUnitTest, \
    DidatticaPianoRegolamentoUnitTest, DidatticaPianoScheUnitTest, DidatticaPianoSceltaSchePianoUnitTest, DidatticaPianoSceltaVincoliUnitTest, DidatticaAmbitiUnitTest, \
    DidatticaPianoSceltaAfUnitTest
from . serializers import CreateUpdateAbstract


class ApiCdSListUnitTest(TestCase):

    def test_apicdslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
        })
        didatticaCds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'dip': dip,
            'tipo_corso_cod': 'L',
            'area_cds': 'scienze',
            'cds_id': 1,
        })
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didatticaCds,
            'iso6392_cod': 'ita',
        })
        r1 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'stato_regdid_cod': 'A',
            'titolo_congiunto_cod': 'N',
            'cds_id': 1,
        })

        DidatticaCdsAltriDatiUfficioUnitTest.create_didatticaCdsAltriDatiUfficio(**{
            'cds_id': 1,
            'edificio': 2,
            'ordine': 1,
        })

        DidatticaCdsAltriDatiUnitTest.create_didatticaCdsAltriDati(**{
            'regdid_id': r1,
            'num_posti': 2
        })

        r1.get_ordinamento_didattico()

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

        # param: area
        data = {'area': 'scienze'}
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
            'area_cds': 'Scienze',
        })
        DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didatticaCds,
        })
        reg = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'stato_regdid_cod': 'A',
            'titolo_congiunto_cod': 'N',
            'cds': didatticaCds,
            'modalita_erogazione': 'Convenzionale'
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
            'clob_txt_ita':'https:....',
        })
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'txt_id': 2,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'FUNZIONI',
            'profilo': 'profiloprova',
            'clob_txt_ita': 'provadescrizione',
        })
        DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'txt_id': 4,
            'regdid': reg,
            'tipo_testo_regdid_cod': 'URL_CDS_VIDEO',
            'clob_txt_ita': 'pdf',
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
            'anno_corso': 1
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'pds_regdid': pds1,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
            'anno_corso': 1
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 3,
            'pds_regdid': pds1,
            'des': 'informatica modulo 1',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 2,
            'anno_corso': 1
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 4,
            'pds_regdid': pds2,
            'des': 'matematica2',
            'af_gen_des_eng': 'math2',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 4,
            'anno_corso': 1
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
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })
        course = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'pds_regdid': pds,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'anno_corso': 2,
            'af_radice_id': 1,
            'matricola_resp_did': p1,
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
            'anno_corso': 1,
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

        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course,
            'personale': p1,
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



class ApiAllStudyActivitiesListUnitTest(TestCase):

    def test_apiallstudyactivitieslist(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()

        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 'aaaa',
            'dip_des_it': 'storia',
            'dip_des_eng': 'history'
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'cds_id': 1,
            'cds_cod': 'aaa',
            'nome_cds_it': 'Matematica',
            'nome_cds_eng': 'Math',
            'dip_id': 1,
        })

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })

        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af_id': 1,
            'personale_id': 1
        })

        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'anno_corso': 1,
            'af_radice_id': 1,
            'matricola_resp_did': p1,
            'mutuata_flg': 1,
            'af_master_id': 2,
            'sett_cod': 'INF/01',
            'sett_des': 'Interdisciplinare',
            'cds_id': 1,
            'anno_corso': 1,
            'aa_off_id': 2015,

        })

        # p = PersonaleUnitTest.create_personale(**{
        #     'id': 1,
        #     'nome': 'Franco',
        #     'cognome': 'Garofalo',
        #     'cd_ruolo': 'PO',
        #     'id_ab': 1,
        #     'matricola': '111111',
        # })

        url = reverse(
            'ricerca:activities')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1

        data = {'department': 'aaaa'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teaching': 'informatica'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'teacher': 'Garofalo'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'cds_cod': 'aaa'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher_code': encrypt('111111')}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'cds': 'Matematica'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'ssd': 'INF'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'period': 'Primo semestre'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'course_year': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'academic_year': 2015}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiStudyActivityDetailUnitTest(TestCase):

    def test_apistudyactivityinfo(self):
        req = Client()

        regdid = DidatticaRegolamentoUnitTest.create_didatticaRegolamento()
        pds = DidatticaPdsRegolamentoUnitTest.create_didatticaPdsRegolamento(
            **{'pds_regdid_id': 1, 'regdid': regdid, })
        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })
        course = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 1,
            'pds_regdid': pds,
            'anno_corso': 1,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Primo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'matricola_resp_did': p1,
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
            'anno_corso': 2,
            'af_radice_id': 1,
            'af_pdr_id': 1,
            'fat_part_stu_cod': 'GRP',
            'fat_part_stu_des': 'des',
            'mutuata_flg': 0,
            'af_master_id': 2,
        })
        DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 3,
            'pds_regdid': pds,
            'des': 'informatica modulo 2',
            'af_gen_des_eng': 'computer science modulo 1',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid,
            'af_radice_id': 1,
            'af_pdr_id': 2,
            'fat_part_stu_cod': 'GRP',
            'fat_part_stu_des': 'des',
            'mutuata_flg': 0,
            'af_master_id': 2,
        })
        DidatticaTestiAfUnitTest.create_didatticaTestiAf(**{
            'tipo_testo_af_cod': 'CONTENUTI',
            'testo_af_ita': 'Variabili',
            'testo_af_eng': 'Variables',
            'af': course,
        })

        # p1 = PersonaleUnitTest.create_personale(**{
        #     'id': 1,
        #     'nome': 'Franco',
        #     'cognome': 'Garofalo',
        #     'cd_ruolo': 'PO',
        #     'id_ab': 1,
        #     'matricola': '111111',
        # })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'coper_id': 1,
            'af': course,
            'personale': p1,
        })

        DidatticaAttivitaFormativaModalitaUnitTest.create_didatticaAttivitaFormativaModalita(**{
            'mod_did_af_id': 1,
            'af_id': 1,
            'mod_did_cod': 'c',
            'mod_did_des': 'convenzionale'
        })

        DidatticaCoperturaDettaglioOreUnitTest.create_didatticaCoperturaDettaglioOre(**{
            'tipo_att_did_cod': 444,
            'coper_id': 1,
            'ore': 3,
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
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2020',
            'visibile': 1
        })

        linea_base2 = RicercaLineaBaseUnitTest.create_ricercaLineaBase(**{
            'id': 7,
            'ricerca_erc2': erc2,
            'descrizione': 'regressione lineare',
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 20201',
            'visibile': 1
        })

        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc1,
            'ricerca_linea_base': linea_base
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc2,
            'ricerca_linea_base': linea_base2
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc2,
            'ricerca_linea_base': linea_base,
            'dt_fine': '2021-01-03',
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc2,
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
            'visibile': 1
        })
        linea_applicata2 = RicercaLineaApplicataUnitTest.create_ricercaLineaApplicata(**{
            'id': 2,
            'ricerca_aster2': aster2,
            'descrizione': 'random forest',
            'descr_pubblicaz_prog_brevetto': 'pubblicazione 2019',
            'visibile': 1
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
        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc2,
            'dt_ins': '2021-01-03 15:47:21'
        })

        url = reverse(
            'ricerca:teacherresearchlines', kwargs={
                'teacherid': encrypt('111112')})

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
                'teacherid': encrypt('111111')})
        res = req.get(url)
        assert len(res.json()['results']) == 2


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
            'anno_corso': 1,
        })
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid2,
            'af_radice_id': 2,
            'anno_corso': 2
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course1,
            'personale': doc1,
            'aa_off_id': datetime.datetime.now().year,
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'af': course2,
            'personale': doc2,
            'aa_off_id': datetime.datetime.now().year
        })

        url = reverse('ricerca:teacherslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # Three professor have flg_cessato = 0
        res = req.get(url)
        assert len(res.json()['results']) == 3

        data = {'search': 'gar'}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111111'

        data = {'role': 'PA', 'lang': 'it'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['TeacherCVFull'] is None

        data = {'department': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'department': 1, 'role': 'PO'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': 1, 'role': 'PA', 'lang': 'en', 'year': '2015'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'regdid': 1}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111112'

        data = {'regdid': 2}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111111'

        data = {'regdid': 1, 'role': 'PA'}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111112'

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
                'teacherid': encrypt('111112')})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['StudyActivityID'] == 2

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
        p2 = PersonaleUnitTest.create_personale(**{
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
        tipo_contatto = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
            **{'cod_contatto': 'EMAIL', 'descr_contatto': 'Posta Elettronica', })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Riferimento Ufficio',
            'descr_contatto': 'Riferimento Ufficio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'POSTA ELETTRONICA CERTIFICATA',
            'descr_contatto': 'POSTA ELETTRONICA CERTIFICATA',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Posta Elettronica Privata',
            'descr_contatto': 'Posta Elettronica Privata',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Fax',
            'descr_contatto': 'Fax',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Residenza',
            'descr_contatto': 'Telefono Residenza',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Domicilio',
            'descr_contatto': 'Telefono Domicilio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare',
            'descr_contatto': 'Telefono Cellulare',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare Ufficio',
            'descr_contatto': 'Telefono Cellulare Ufficio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Ufficio',
            'descr_contatto': 'Telefono Ufficio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'URL Sito WEB',
            'descr_contatto': 'URL Sito WEB',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
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

        DocentePtaAltriDatiUnitTest.create_docentePtaAltriDati(**{
            'id': 1,
            'matricola': p1,
            'path_foto': 'aaaa',
            'path_cv_ita': 'aaaa',
            'path_cv_en': 'aaaaadc',
            'breve_bio': 'prova',
            'breve_bio_en': 'test',
            'orario_ricevimento': 'lunedi',
            'orario_ricevimento_en': 'monday',
            'orcid': '1111-2222-3333-4444'
        })

        DocentePtaAltriDatiUnitTest.create_docentePtaAltriDati(**{
            'id': 2,
            'matricola': p2,
            'path_foto': 'aaaa',
            'path_cv_ita': 'aaaa',
            'path_cv_en': 'aaaaadc',
            'breve_bio': 'prova',
            'breve_bio_en': 'test',
            'orario_ricevimento': 'lunedi',
            'orario_ricevimento_en': 'monday',
            'orcid': '1111-2222-3333-4445'
        })

        url = reverse('ricerca:teacherinfo', kwargs={'teacherid': encrypt('111112')})


        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert decrypt(res.json()['results']['TeacherID']) == '111112'

        url = reverse('ricerca:teacherinfo', kwargs={'teacherid': encrypt('111113')})
        res = req.get(url)
        assert res.json()['results']['TeacherFirstName'] == 'Lionel'


class ApiTeacherNewsUnitTest(TestCase):

    def test_apiteachernewslist(self):

        req = Client()

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'ds_aff_org': 'aaaa'
        })

        DocentePtaBachecaUnitTest.create_docentePtaBacheca(**{
            'id': 1,
            'matricola': p1,
            'tipo_testo': 'a',
            'tipo_testo_en': 'a',
            'titolo': 'evento',
            'titolo_en': 'event',
            'testo': 'evento',
            'testo_en': 'event',
            'url_testo': 'aaaa',
            'url_testo_en': 'aaaa',
            'ordine': 1,
            'attivo': 1,
            'dt_pubblicazione': '2222-02-02',
            'dt_inizio_validita': '2022-10-13',
            'dt_fine_validita': '2099-10-13',

        })



        url = reverse('ricerca:teachernews', kwargs={'teacherid': encrypt('111112')})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1



class ApiTeacherMaterialsUnitTest(TestCase):

    def test_apiteachermaterialslist(self):

        req = Client()

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'ds_aff_org': 'aaaa'
        })

        DocentePtaMaterialeDidatticoUnitTest.create_docentePtaMaterialeDidattico(**{
            'id': 1,
            'matricola': p1,
            'titolo': 'evento',
            'titolo_en': 'event',
            'testo': 'evento',
            'testo_en': 'event',
            'url_testo': 'aaaa',
            'url_testo_en': 'aaaa',
            'ordine': 1,
            'attivo': 1,
            'dt_pubblicazione': '2222-02-02',
            'dt_inizio_validita': '2022-10-13',
            'dt_fine_validita': '2099-10-13',

        })

        url = reverse('ricerca:teachermaterials', kwargs={'teacherid': encrypt('111112')})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiPhdListUnitTest(TestCase):

    def test_apiphdlistunittest(self):
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

        url = reverse('ricerca:phdlist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results'][0]['PhdCdsCOD'] == '111'

        data = {'department': 1}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['PhdCdsCOD'] == '111'

        data = {'year': 2020}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['PhdCdsCOD'] == '111'

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
        assert res.json()['results'][0]['PhdCdsCOD'] == '111'

        data = {'pdscod': 'GEN'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['PhdCdsCOD'] == '111'

        data = {'cycle': 0}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        url = reverse('ricerca:phd-cycles')
        # check url
        res = req.get(url)
        assert res.status_code == 200


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
            'cd_tipo_nodo': 'DRZ',
            'ds_tipo_nodo': 'Direzione'
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'uo_padre': '2',
        })
        PersonaleAttivoTuttiRuoliUnitTest.create_personaleAttivoTuttiRuoli(**{
            'matricola': '111114',
            'cd_ruolo': 'PO',
            'ds_ruolo': 'Professore Ordinario',
            'cd_uo_aff_org': u1,
            'ds_aff_org': 'Direzione'
        })

        PersonalePrioritaRuoloUnitTest.create_personalePrioritaRuolo(**{
            'cd_ruolo': 'PO',
            'priorita': 1,
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
            'id_ab': 3,
            'matricola': '111114',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cod_fis': 'ZLT',
            "cd_uo_aff_org": u2,
            'dt_rap_fin': '2222-02-02'
        })
        DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 1,
            'dip_des_it': "Matematica e Informatica",
            'dip_des_eng': "Math and Computer Science",
        })
        tipo_contatto = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
            **{'cod_contatto': 'EMAIL', 'descr_contatto': 'Posta Elettronica', })
        tipo_contatto_phone = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
            **{'cod_contatto': 'Telefono Ufficio', 'descr_contatto': 'Telefono Ufficio', })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Riferimento Ufficio',
            'descr_contatto': 'Riferimento Ufficio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'POSTA ELETTRONICA CERTIFICATA',
            'descr_contatto': 'POSTA ELETTRONICA CERTIFICATA',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Posta Elettronica Privata',
            'descr_contatto': 'Posta Elettronica Privata',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Fax',
            'descr_contatto': 'Fax',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Residenza',
            'descr_contatto': 'Telefono Residenza',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Domicilio',
            'descr_contatto': 'Telefono Domicilio',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare',
            'descr_contatto': 'Telefono Cellulare',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'Telefono Cellulare Ufficio',
            'descr_contatto': 'Telefono Cellulare Ufficio',
        })
        # PersonaleTipoContattoUnitTest.create_personaleTipoContatto(**{
            # 'cod_contatto': 'Telefono Ufficio',
            # 'descr_contatto': 'Telefono Ufficio',
        # })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'URL Sito WEB Curriculum Vitae',
            'descr_contatto': 'URL Sito WEB Curriculum Vitae',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
            'cod_contatto': 'URL Sito WEB',
            'descr_contatto': 'URL Sito WEB',
        })
        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
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
        PersonaleContattiUnitTest.create_personaleContatti(**{
            'cd_tipo_cont': tipo_contatto_phone,
            'id_ab': 3,
            'cod_fis': p3,
            'contatto': '999',
            'prg_priorita': 1000,
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


        data = {'structure': '99', 'lang': 'it'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'search': 'Ibra', 'function': 'Direttore'}
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

        data = {'phone': '999'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'phone': '999', 'role': 'PO', 'structuretypes': 'DRZ'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'phone': '999', 'role': 'PO', 'structuretypes': 'DRZ','structureid':3}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'role': 'PO', 'structuretypes': 'DRZ'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'phone': '999', 'structuretypes': 'DRZ'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'phone': '999', 'role': 'PO'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'structuretypes': 'DRZ'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'structuretree': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


        data = {'structuretree': '2'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        usr = get_user_model().objects.create(
            **{
                'username': 'test',
                'password': 'password',
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse('ricerca:addressbooklist-full')
        res = req.get(url,{},HTTP_AUTHORIZATION= f'Token {token.key}')
        assert res.status_code == 200


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

        # check url
        res = req.get(url)
        assert res.status_code == 200

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

        data = {'father': '1', 'depth': '1'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['StructureCod'] == '1'



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

        tipo_contatto = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
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

        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
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
                'personaleid': encrypt("111112")})
        url1 = reverse(
            'ricerca:personaledetail', kwargs={
                'personaleid': encrypt("111113")})
        url2 = reverse(
            'ricerca:personaledetail', kwargs={
                'personaleid': encrypt("111114")})

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

        assert decrypt(res.json()['results']['ID']) == "111112"
        assert decrypt(res1.json()['results']['ID']) == "111113"

        usr = get_user_model().objects.create(
            **{
                'username': 'test',
                'password': 'password',
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse('ricerca:personaledetail', kwargs={
                      'personaleid': encrypt("111112")})
        res = req.get(url,{},HTTP_AUTHORIZATION= f'Token {token.key}')
        assert res.status_code == 200


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

        tipo_contatto = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
            **{'cod_contatto': 'PEC', 'descr_contatto': 'Posta Elettronica Certificata', })

        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
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
            'dipartimento_riferimento': 'Informatica, demacs',
            'id_dipartimento_riferimento': dip1,
            'sede_dimensione': "290",
            'responsabile_scientifico': 'Mungari Simone',
            'matricola_responsabile_scientifico': p1,
            'laboratorio_interdipartimentale': 'SI',
            'visibile': True
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
            'dipartimento_riferimento': 'Matematica, demacs',
            'id_dipartimento_riferimento': dip2,
            'sede_dimensione': "291",
            'responsabile_scientifico': 'Carlucci Carmine',
            'matricola_responsabile_scientifico': p2,
            'visibile': True
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

        i1 = LaboratorioInfrastrutturaUnitTest.create_laboratorioInfrastruttura(
            **{'id': 1, })

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
            'id_infrastruttura_riferimento': i1,
            'visibile': True
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

        data = {'department': '1', 'teacher': encrypt('111111')}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 1
        assert res.json()[
            'results'][0]['ScientificDirector'] == 'Mungari Simone'

        data = {'teacher': encrypt('111111')}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'scope': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': encrypt('111112')}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 3

        data = {'teacher': encrypt('111112'), 'scope': '1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': encrypt('111111'), 'scope': '1'}
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

        data = {'infrastructure': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'area': 'Scientifico'}
        res = req.get(url, data=data)
        assert res.json()['results'][0]['LaboratoryId'] == 2
        assert res.json()['results'][0]['Dimension'] == '291'

        data = {'search': 'Informatica', 'lang': 'it'}
        res = req.get(url, data=data)
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
            'visibile': True
        })

        lab2 = LaboratorioDatiBaseUnitTest.create_laboratorioDatiBase(**{
            'id': 2,
            'matricola_referente_compilazione': p2,
            'nome_laboratorio': 'LAB2',
            'id_dipartimento_riferimento': dip2,
            'ambito': 'Umanistico',
            'matricola_responsabile_scientifico': p2,
            'visibile': True
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
            'date_issued_year': 9999,
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

        url = reverse('ricerca:publications', kwargs={'teacherid': encrypt('111112')})

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
            'contributor': '111119',
            'structure': '1'}

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
                'teacherid': encrypt('111112'),
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
                'teacherid': encrypt('111112'),
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
        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
        })

        RicercaErc1UnitTest.create_ricercaErc1(**{
            'id': 1,
            'cod_erc1': 'cod1_erc1',
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })
        ricerca_gruppo1 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 1,
            'nome': 'Intelligenza Artificiale',
            'descrizione': 'ricerca su Machine Learning',
            'ricerca_erc1_id': 1,
        })
        ricerca_gruppo2 = RicercaGruppoUnitTest.create_ricercaGruppo(**{
            'id': 2,
            'nome': 'machine learning',
            'descrizione': 'ricerca su Machine Learning',
            'ricerca_erc1_id': 1,
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
        assert len(res.json()['results']) == 2

        data = {'teacher': encrypt('111112')}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'coderc1': 'cod1_erc1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'search': 'Intel'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': encrypt('111112'),'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

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
            'visibile': 1
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

        data = {'teacher': encrypt('111112'), 'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': encrypt('111112')}
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
            'anno': '2016',
            'visibile': 1
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

        data = {'teacher': encrypt('111112')}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': encrypt('111112'), 'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiAllResearchLinesUnitTest(TestCase):

    def test_apiallbresearchlines(self):
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
            'visibile': 1
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
            'anno': '2016',
            'visibile': 1
        })
        RicercaDocenteLineaApplicataUnitTest.create_ricercaDocenteLineaApplicata(**{
            'personale': doc1,
            'ricerca_linea_applicata': linea_applicata,
            'dt_ins': '2021-01-03 15:47:21'
        })
        RicercaDocenteLineaBaseUnitTest.create_ricercaDocenteLineaBase(**{
            'personale': doc1,
            'ricerca_linea_base': linea_base
        })


        url = reverse('ricerca:allresearchlines')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'reg'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'year': 2020}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'ercs': 'cod1_erc1'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'asters': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'ercs': 'cod1_erc1','asters': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2



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
            'uo_padre': '22'
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
            'profilo': '111',
            'ds_profilo': 'abcds',
            'ds_profilo_breve': 'afv'
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
            'profilo': '111',
            'ds_profilo': 'abcds',
            'ds_profilo_breve': 'afv'
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
            'profilo': '111',
            'ds_profilo': 'abcds',
            'ds_profilo_breve': 'afv'
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
            'profilo': '111',
            'ds_profilo': 'abcds',
            'ds_profilo_breve': 'afv'
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
            'anno_corso': 1
        })
        course2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'des': 'informatica',
            'af_gen_des_eng': 'computer science',
            'ciclo_des': 'Secondo semestre',
            'regdid': regdid2,
            'af_radice_id': 2,
            'anno_corso': 1
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
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111111'

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
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111112'

        data = {'regdid': 2}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111111'

        data = {'regdid': 1, 'role': 'PA'}
        res = req.get(url, data=data)
        assert decrypt(res.json()['results'][0]['TeacherID']) == '111112'

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
            'date_issued_year': 9999,
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
            'results'][1]['PublicationAbstract'] == 'abstract inglese'

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
            'cd_csa': 1,
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'ds_tipo_nodo': 'direzione',
            'cd_tipo_nodo': 'CDS',
            'id_ab': 2,
            'denominazione': 'bbb',
            'denominazione_padre': 'd',
            'uo_padre': '22',
            'cd_csa': 2,
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

        tipo_contatto = PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(
            **{'cod_contatto': 'PEC', 'descr_contatto': 'Posta Elettronica Certificata', })

        PersonaleUoTipoContattoUnitTest.create_personaleUoTipoContatto(**{
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

        d1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': 111,
            'dip_des_it': 'Informatica'
        })

        s1 = SpinoffStartupDatiBaseUnitTest.create_spinoffStartupDatiBase(**{
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

        SpinoffStartupDipartimentoUnitTest.create_spinoffStartupDipartimento(**{
            'id_spinoff_startup_dati_base': s1,
            'id_didattica_dipartimento': d1,

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

        data = {'departments': 111}
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

        d1 = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_des_it': 'Informatica'
        })

        s1 = SpinoffStartupDatiBaseUnitTest.create_spinoffStartupDatiBase(**{
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

        SpinoffStartupDipartimentoUnitTest.create_spinoffStartupDipartimento(**{
            'id_spinoff_startup_dati_base': s1,
            'id_didattica_dipartimento': d1,

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

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'ds_tipo_nodo': 'facolta',
            'cd_tipo_nodo': '000',
            'id_ab': 1,
            'denominazione': 'aaa',
            'denominazione_padre': 'c',
            'uo_padre': '11',
            'cd_csa': 1,
        })

        t1 = TipologiaAreaTecnologicaUnitTest.create_tipologiaAreaTecnologica(
            **{"id": 1, "descr_area_ita": "aaa", "descr_area_eng": "aaa", })

        a1 = ProgettoAmbitoTerritorialeUnitTest.create_progettoAmbitoTerritoriale(
            **{"id": 1, "ambito_territoriale": "europeo", })

        p1 = ProgettoTipologiaProgrammaUnitTest.create_progettoTipologiaProgramma(
            **{"id": 1, "nome_programma": "AAA"})

        pr1 = ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
            "id": 1,
            "uo": u1,
            "id_ambito_territoriale": a1,
            "id_tipologia_programma": p1,
            "titolo": "Motore",
            "descr_breve": "Mot",
            "abstract_ita": "Motore",
            "abstract_eng": "Engine",
            "id_area_tecnologica": t1,
            "anno_avvio": 2021
        })

        pr2 = ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
            "id": 2,
            "id_ambito_territoriale": a1,
            "id_tipologia_programma": p1,
            "titolo": "Motore",
            "descr_breve": "Mot",
            "abstract_ita": "Motore",
            "abstract_eng": "Engine",
            "id_area_tecnologica": t1,
            "anno_avvio": 2020
        })

        ProgettoResponsabileScientificoUnitTest.create_progettoResponsabileScientifico(
            **{"matricola": p, "nome_origine": "Simone", "id_progetto": pr1, })

        ProgettoRicercatoreUnitTest.create_progettoRicercatore(**{
            "matricola": p,
            "nome_origine": 'Simone',
            "id_progetto": pr1,
        })

        url = reverse('ricerca:projects')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'mot'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'techarea': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'infrastructure': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'programtype': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'-programtype': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'territorialscope': 1}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'year': 2021}
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

        pr1 = ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
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
            **{"matricola": p, "nome_origine": "Simone", "id_progetto": pr1, })
        ProgettoRicercatoreUnitTest.create_progettoRicercatore(**{
            "matricola": p,
            "nome_origine": 'Simone',
            "id_progetto": pr1,
        })

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


class ApiTerritorialScopesListUnitTest(TestCase):

    def test_apiterritorialscopeslist(self):

        req = Client()

        ProgettoAmbitoTerritorialeUnitTest.create_progettoAmbitoTerritoriale(
            **{'id': 1, 'ambito_territoriale': 'aaa', })

        url = reverse('ricerca:projects-territorial-scopes')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiProgramTypesListUnitTest(TestCase):

    def test_apiprogramtypeslist(self):

        req = Client()

        ProgettoTipologiaProgrammaUnitTest.create_progettoTipologiaProgramma(
            **{'id': 1, 'nome_programma': 'aaa', })

        url = reverse('ricerca:projects-program-types')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiCdsAreasListUnitTest(TestCase):

    def test_apicdsareaslist(self):

        req = Client()

        DidatticaCdsUnitTest.create_didatticaCds(**{
            'area_cds': 'aaa',
        })
        DidatticaCdsUnitTest.create_didatticaCds(**{
            'cds_id':2,
            'cdsord_id':3,
            'area_cds': None,
        })

        url = reverse('ricerca:cds-areas')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiProjectInfrastructuresListUnitTest(TestCase):

    def test_apiprojectinfrastructureslist(self):

        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': 1,
            'denominazione': 'aaaa',
        })
        ProgettoDatiBaseUnitTest.create_progettoDatiBase(**{
            'uo': u1,
        })

        url = reverse('ricerca:projects-infrastructures')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiPersonnelCfsListUnitTest(TestCase):

    def test_apipersonnelcfslist(self):
        req = Client()

        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '2',
            'uo_padre': '1',
        })
        u2 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '3',
            'uo_padre': '2',
        })
        PersonaleUnitTest.create_personale(**{
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
            'dt_rap_fin': '2023-01-03',
            'ds_aff_org': 'aaa',
            'cod_fis': 'SMN1',
        })
        PersonaleUnitTest.create_personale(**{
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
            'dt_rap_fin': '2023-01-03',
            'ds_aff_org': 'bbb',
            'cod_fis': 'LNL1',
        })
        usr = get_user_model().objects.create(
            **{
                'username': 'test',
                'password': 'password',
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse('ricerca:personnel-cfs')

        # GET
        res = req.get(url,{},HTTP_AUTHORIZATION= f'Token {token.key}')
        assert len(res.json()['results']) == 0

        data = {'roles': 'PA'}
        res = req.get(url, data=data, HTTP_AUTHORIZATION= f'Token {token.key}')
        assert len(res.json()['results']) == 0


class ApiSortingContactsUnitTest(TestCase):

    def test_apisortingcontactslist(self):

        req = Client()
        u1 = UnitaOrganizzativaUnitTest.create_unitaOrganizzativa(**{
            'uo': '1',
            'uo_padre': '1',
        })
        PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'cd_uo_aff_org': u1,
            'ds_aff_org': 'aaaa'
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
            'cd_uo_aff_org': u1,
            'ds_aff_org': 'bbbb'
        })

        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'personale_id': 1,
            'cds_cod': '1',
            'aa_off_id': 2021
        })
        DidatticaCoperturaUnitTest.create_didatticaCopertura(**{
            'personale_id': 2,
            'cds_cod': '1',
            'aa_off_id': datetime.datetime.now().year - 1
        })

        url = reverse('ricerca:sorting-contacts',kwargs={'cdscod': '1'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiHighFormationMastersListUnitTest(TestCase):

    def test_apihighformationmasterslist(self):

        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '1111',
            'dip_des_it': 'Informatica'
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
            'ds_aff_org': 'aaaa'
        })

        aftc = AltaFormazioneTipoCorsoUnitTest.create_altaFormazioneTipoCorso(**{
            'id': 3,
            'tipo_corso_descr': 'AAAA'
        })

        afme = AltaFormazioneModalitaErogazioneUnitTest.create_altaFormazioneModalitaErogazione(**{
            'id': 3,
            'descrizione': 'AAAA'
        })

        a1 = AltaFormazioneDatiBaseUnitTest.create_altaFormazioneDatiBase(**{
            'id': 1,
            'titolo_it': 'AAAA',
            'titolo_en': 'AAAA',
            'lingua': 'ita',
            'matricola_direttore_scientifico': doc1,
            'id_alta_formazione_tipo_corso': aftc,
            'id_alta_formazione_mod_erogazione': afme,
            'id_dipartiento_riferimento': dip,
            'anno_rilevazione': 2021,
        })

        AltaFormazioneDatiBaseUnitTest.create_altaFormazioneDatiBase(**{
            'id': 2,
            'titolo_it': 'AAAA',
            'titolo_en': 'AAAA',
            'matricola_direttore_scientifico': doc1,
            'id_alta_formazione_tipo_corso': aftc,
            'id_alta_formazione_mod_erogazione': afme,
        })

        AltaFormazioneConsiglioScientificoEsternoUnitTest.create_altaFormazioneConsiglioScientificoEsterno(**{
            'nome_cons': 'Simone',
            'ruolo_cons': 'docente',
            'ente_cons': 'università',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneConsiglioScientificoInternoUnitTest.create_altaFormazioneConsiglioScientificoInterno(**{
            'nome_origine_cons': 'Simone',
            'matricola_cons': doc1,
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazionePartnerUnitTest.create_altaFormazionePartner(**{
            'denominazione': 'aaaa',
            'tipologia': 'bbbb',
            'sito_web': 'aaaa',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneModalitaSelezioneUnitTest.create_altaFormazioneModalitaSelezione(**{
            'tipo_selezione': 'chiusa',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneIncaricoDidatticoUnitTest.create_altaFormazioneIncaricoDidattico(**{
            'id': 1,
            'modulo': 'AAA',
            'qualifica': 'SSF',
            'num_ore': 13,
            'ente': 'Università',
            'tipologia': 'Prova',
            'docente': 'Mungari',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazionePianoDidatticoUnitTest.create_altaFormazionePianoDidattico(**{
            'id': 1,
            'modulo': 'AAA',
            'ssd': 'SSF',
            'num_ore': 13,
            'cfu': 2,
            'verifica_finale': 1,
            'id_alta_formazione_dati_base': a1
        })

        url = reverse('ricerca:high-formation-masters')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'AAA'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'language': 'ita'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'coursetype': '3'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'erogation': '3'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'department': '1111'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'director': '111112'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 2

        data = {'year': 2021}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1


class ApiHighFormationMasterDetailUnitTest(TestCase):

    def test_apihighformationmasterdetail(self):

        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(**{
            'dip_id': 1,
            'dip_cod': '1111',
            'dip_des_it': 'Informatica'
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
            'ds_aff_org': 'aaaa'
        })

        aftc = AltaFormazioneTipoCorsoUnitTest.create_altaFormazioneTipoCorso(**{
            'id': 3,
            'tipo_corso_descr': 'AAAA'
        })

        afme = AltaFormazioneModalitaErogazioneUnitTest.create_altaFormazioneModalitaErogazione(**{
            'id': 3,
            'descrizione': 'AAAA'
        })

        a1 = AltaFormazioneDatiBaseUnitTest.create_altaFormazioneDatiBase(**{
            'id': 1,
            'titolo_it': 'AAAA',
            'titolo_en': 'AAAA',
            'matricola_direttore_scientifico': doc1,
            'id_alta_formazione_tipo_corso': aftc,
            'id_alta_formazione_mod_erogazione': afme,
            'id_dipartiento_riferimento': dip,
        })

        AltaFormazioneConsiglioScientificoEsternoUnitTest.create_altaFormazioneConsiglioScientificoEsterno(**{
            'nome_cons': 'Simone',
            'ruolo_cons': 'docente',
            'ente_cons': 'università',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneConsiglioScientificoInternoUnitTest.create_altaFormazioneConsiglioScientificoInterno(**{
            'nome_origine_cons': 'Simone',
            'matricola_cons': doc1,
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazionePartnerUnitTest.create_altaFormazionePartner(**{
            'denominazione': 'aaaa',
            'tipologia': 'bbbb',
            'sito_web': 'aaaa',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneModalitaSelezioneUnitTest.create_altaFormazioneModalitaSelezione(**{
            'tipo_selezione': 'chiusa',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazioneIncaricoDidatticoUnitTest.create_altaFormazioneIncaricoDidattico(**{
            'id': 1,
            'modulo': 'AAA',
            'qualifica': 'SSF',
            'num_ore': 13,
            'ente': 'Università',
            'tipologia': 'Prova',
            'docente': 'Mungari',
            'id_alta_formazione_dati_base': a1
        })

        AltaFormazionePianoDidatticoUnitTest.create_altaFormazionePianoDidattico(**{
            'id': 1,
            'modulo': 'AAA',
            'ssd': 'SSF',
            'num_ore': 13,
            'cfu': 2,
            'verifica_finale': 1,
            'id_alta_formazione_dati_base': a1
        })

        url = reverse('ricerca:high-formation-master-detail',kwargs={'id': 1})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['ID'] == 1


class ApiErogationModesListUnitTest(TestCase):

    def test_apierogationmodeslist(self):

        req = Client()

        AltaFormazioneModalitaErogazioneUnitTest.create_altaFormazioneModalitaErogazione(**{
            'id': 1,
            'descrizione': 'AAAA'
        })

        url = reverse('ricerca:erogation-modes')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiHighFormationCourseTypesListUnitTest(TestCase):

    def test_apicoursetypeslist(self):

        req = Client()

        AltaFormazioneTipoCorsoUnitTest.create_altaFormazioneTipoCorso(**{
            'id': 1,
            'tipo_corso_descr': 'AAAA'
        })

        url = reverse('ricerca:high-formation-course-types')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiPersonIdUnitTest(TestCase):

    def test_apipersonid(self):
        req = Client()

        p = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Simone',
            'cognome': 'Mungari',
            'cd_ruolo': 'PA',
            'id_ab': 1,
            'matricola': '111112',
            'fl_docente': 1,
            'flg_cessato': 0,
            'ds_aff_org': 'aaaa'
        })

        usr = get_user_model().objects.create(
            **{
                'username': 'test',
                'password': 'password',
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse('ricerca:get-person-id')

        # GET
        res = req.get(url,HTTP_AUTHORIZATION= f'Token {token.key}')
        assert res.status_code == 405

        # POST
        res = req.post(url,{"test":"test"}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 404

        # POST
        res = req.post(url,{"id":"99999"}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 404

        # POST
        res = req.post(url, {"id": "111112"}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 200

        url = reverse('ricerca:get-decrypted-person-id')

        # GET
        res = req.get(url,HTTP_AUTHORIZATION= f'Token {token.key}')
        assert res.status_code == 405

        # POST
        res = req.post(url,{"test":"test"}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 404

        # POST
        res = req.post(url,{"id":"99999"}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 404

        # POST
        m_test_encrypted = encrypt("111111")
        res = req.post(url, {"id": m_test_encrypted}, HTTP_AUTHORIZATION=f'Token {token.key}')
        assert res.status_code == 200


class ApiAster1ListUnitTest(TestCase):

    def test_apiaster1list(self):
        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        RicercaAster1UnitTest.create_ricercaAster1(**{
            'id': 1,
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })

        url = reverse('ricerca:aster1list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert len(res.json()['results']) == 1


class ApiAster2ListUnitTest(TestCase):

    def test_apiaster2list(self):
        req = Client()

        erc0 = RicercaErc0UnitTest.create_ricercaErc0(**{
            'erc0_cod': '111',
            'description': 'IT',
            'description_en': 'IT',
        })
        aster1 = RicercaAster1UnitTest.create_ricercaAster1(**{
            'id': 1,
            'descrizione': 'Computer Science and Informatics',
            'ricerca_erc0_cod': erc0,
        })

        RicercaAster2UnitTest.create_ricercaAster2(**{
            'id': 1,
            'descrizione': 'Sicurezza Informatica',
            'ricerca_aster1_id': 1

        })
        url = reverse('ricerca:aster2list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        assert len(res.json()['results']) == 1



class ApiPhdActivitiesListlUnitTest(TestCase):

    def test_apiphdactivitieslist(self):

        req = Client()

        a1 = DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 1,
            'nome_af': 'AAAA',
            'struttura_proponente_origine': 'dimes',
            'rif_dottorato': 'matematica',
            'ciclo': 1

        })

        a2 = DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 2,
            'nome_af': 'BBBB',
            'struttura_proponente_origine': 'aaaa',
            'rif_dottorato': 'umanistici',
            'ciclo': 1

        })

        DidatticaDottoratoAttivitaFormativaDocenteUnitTest.create_didatticaDottoratoAttivitaFormativaDocente(**{
            'id_didattica_dottorato_attivita_formativa': a1,
            'cognome_nome_origine': 'Simone',
        })

        DidatticaDottoratoAttivitaFormativaAltriDocentiUnitTest.create_didatticaDottoratoAttivitaFormativaAltriDocenti(**{
            'id_didattica_dottorato_attivita_formativa': a2,
            'cognome_nome_origine': 'Carmine',
        })



        url = reverse('ricerca:phd-activities-list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'AAA'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'structure': 'dimes'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'phd': 'umanistici'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': 'simone'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

        data = {'teacher': 'ludovico'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 0

        data = {'teacher': 'carmine'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1

class ApiPhdActivityDetailUnitTest(TestCase):

    def test_apiphdactivitydetail(self):

        req = Client()

        a1 = DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 1,
            'nome_af': 'AAAA',
            'ciclo': 1

        })

        p1 = PersonaleUnitTest.create_personale(**{
            'id': 1,
            'nome': 'Franco',
            'cognome': 'Garofalo',
            'cd_ruolo': 'PO',
            'id_ab': 1,
            'matricola': '111111',
        })
        p2 = PersonaleUnitTest.create_personale(**{
            'id': 2,
            'nome': 'Simone',
            'cognome': 'Munggari',
            'cd_ruolo': 'PO',
            'id_ab': 2,
            'matricola': '111112',
        })
        DidatticaDottoratoAttivitaFormativaDocenteUnitTest.create_didatticaDottoratoAttivitaFormativaDocente(**{
            'id_didattica_dottorato_attivita_formativa': a1,
            'cognome_nome_origine': 'Franco',
            'matricola': p1,
        })

        DidatticaDottoratoAttivitaFormativaAltriDocentiUnitTest.create_didatticaDottoratoAttivitaFormativaAltriDocenti(**{
            'id_didattica_dottorato_attivita_formativa': a1,
            'cognome_nome_origine': 'Simone',
            'matricola': p2,
        })



        url = reverse('ricerca:phd-activity-detail',kwargs={'id': 1})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()['results']['ID'] == 1



class ApiRefPhdListUnitTest(TestCase):

    def test_apirefphdlist(self):

        req = Client()

        DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 1,
            'nome_af': 'AAAA',
            'struttura_proponente_origine': 'dimes',
            'rif_dottorato': 'matematica',
            'ciclo': True

        })


        url = reverse('ricerca:ref-phd')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1



class ApiRefStructuresListUnitTest(TestCase):

    def test_apirefstructureslist(self):

        req = Client()

        DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 1,
            'nome_af': 'AAAA',
            'struttura_proponente_origine': 'dimes',
            'rif_dottorato': 'matematica',
            'ciclo': 1

        })


        url = reverse('ricerca:ref-structures')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1



class ApiPhdSsdListUnitTest(TestCase):

    def test_apiphdssdlist(self):

        req = Client()

        DidatticaDottoratoAttivitaFormativaUnitTest.create_didatticaDottoratoAttivitaFormativa(**{
            'id': 1,
            'ssd': 'Convenzionale',
            'ciclo': 1

        })


        url = reverse('ricerca:phd-ssd-list')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiSitoWebCdsListUnitTest(TestCase):
    def test_apisitiwebcdslist(self):
        req = Client()

        s1 = SitoWebCdsDatiBaseUnitTest.create_sitoWebCdsDatiBase(**{
            'id': 1,
            'aa': '2022',
            'nome_corso_it': 'Informatica',
            'nome_corso_en': 'Computer Science',
            'lingua_it': 'italiano',
            'lingua_en': "italian",
            'classe_laurea_it': 'aaa',
            'durata': 50,
            'num_posti': 50
        })

        SitoWebCdsExStudentiUnitTest.create_sitoWebCdsExStudenti(**{
            'id': 111,
            'ordine': 1,
            'profilo_it': 'aaa',
            'profilo_en': 'aaa',
            'link_it': 'aaa',
            'link_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        SitoWebCdsLinkUnitTest.create_sitoWebCdsLink(**{
            'id': 111111,
            'ordine': 1,
            'descrizione_link_it': 'aaa',
            'descrizione_link_en': 'aaa',
            'link_it': 'aaa',
            'link_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        SitoWebCdsSliderUnitTest.create_sitoWebCdsSlider(**{
            'id': 123,
            'ordine': 1,
            'slider_it': 'aaa',
            'slider_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        s2 = SitoWebCdsDatiBaseUnitTest.create_sitoWebCdsDatiBase(**{
            'id': 2,
            'aa': '2022',
            'nome_corso_it': 'Ingegneria',
            'nome_corso_en': 'Computer Engineering',
            'lingua_it': 'italiano',
            'lingua_en': "italian",
            'durata': 50,
            'num_posti': 50
        })

        DidatticaCdsUnitTest.create_didatticaCds(**{
            'cds_id': 1,
            'cds_cod': 'aaa',
            'nome_cds_it': 'Matematica',
            'nome_cds_eng': 'Math',
        })


        SitoWebCdsSliderUnitTest.create_sitoWebCdsSlider(**{
            'id': 124,
            'ordine': 1,
            'slider_it': 'aaa',
            'slider_en': 'aaa',
            'id_sito_web_cds_dati_base': s2,
        })


        url = reverse('ricerca:cdswebsitelist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 2

        data = {'search': 'Informatica', 'academic_year': 2022, 'cdslanguage': 'italiano', 'course_class': 'aaa'}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1



class ApiSitoWebCdsDetailUnitTest(TestCase):

    def test_apisitowebcdsdetail(self):
        req = Client()

        s1 = SitoWebCdsDatiBaseUnitTest.create_sitoWebCdsDatiBase(**{
            'id': 1,
            'cds_cod': '1',
            'aa': '2022',
            'nome_corso_it': 'Informatica',
            'nome_corso_en': 'Computer Science',
            'lingua_it': 'italiano',
            'lingua_en': "italian",
            'durata': 50,
            'num_posti': 50
        })


        SitoWebCdsExStudentiUnitTest.create_sitoWebCdsExStudenti(**{
            'id': 1,
            'ordine': 1,
            'profilo_it': 'aaa',
            'profilo_en': 'aaa',
            'link_it': 'aaa',
            'link_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        SitoWebCdsLinkUnitTest.create_sitoWebCdsLink(**{
            'id': 1,
            'ordine': 1,
            'descrizione_link_it': 'aaa',
            'descrizione_link_en': 'aaa',
            'link_it': 'aaa',
            'link_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        SitoWebCdsSliderUnitTest.create_sitoWebCdsSlider(**{
            'id': 1,
            'ordine': 1,
            'slider_it': 'aaa',
            'slider_en': 'aaa',
            'id_sito_web_cds_dati_base': s1,
        })

        url = reverse('ricerca:cdswebsitedetail', kwargs={'cdswebsitecod': '1'})

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET
        res = req.get(url)
        assert res.json()['results']['CDSCOD'] == '1'



class ApiSitoWebCdsDegreeTypesUnitTest(TestCase):
    def test_apisitiwebcdsdegreetypes(self):
        req = Client()

        SitoWebCdsDatiBaseUnitTest.create_sitoWebCdsDatiBase(**{
            'classe_laurea_it': 'Laurea Triennale',
        })



        url = reverse('ricerca:cdswebsitesdegreetypes')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1




class ApiSitoWebCdsTopicListUnitTest(TestCase):
    def test_apisitiwebcdstopics(self):
        req = Client()


        SitoWebCdsTopicListUnitTest.create_sitoWebCdsTopicList(**{
            'id': 1,
            'descr_topic_it': 'prova',
            'descr_topic_en': 'test',
            'visibile': 0,
            'dt_mod': datetime.datetime.today(),
        })



        url = reverse('ricerca:cdswebsitestopiclist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 1


class ApiSitoWebCdsTopicArticlesListUnitTest(TestCase):

    def setUp(self, *args, **kwargs):
        self.uname = "user"
        self.passw = "pass"
        self.user = get_user_model().objects.create_superuser(username=self.uname, password=self.passw)
        self.token = Token.objects.create(user=self.user)


    def test_apisitiwebcdstopicarticles(self):

        tipo_dato = SitoWebCdsTipoDato.objects.create(descr_breve='TICKET')

        topic = SitoWebCdsTopicListUnitTest.create_sitoWebCdsTopicList(**{
            'id': 1,
            'descr_topic_it': 'prova',
            'descr_topic_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        topic2 = SitoWebCdsTopicListUnitTest.create_sitoWebCdsTopicList(**{
            'id': 2,
            'descr_topic_it': 'prova',
            'descr_topic_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        cds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'cds_id': 1,
            'cds_cod': '1',
            'nome_cds_it': 'Matematica',
            'nome_cds_eng': 'Math',
        })

        # Regulament Article 1 visible
        a1 = SitoWebCdsArticoliRegolamentoUnitTest.create_sitoWebCdsArticoliRegolamento(**{
            'id': 1,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'numero': 11,
            'titolo_articolo_it': 'Prova',
            'testo_it': 'Contenuto',
            'titolo_articolo_en': 'Test',
            'testo_en': 'Content',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),

        })

        # Regulament Article 2 NOT visible
        a2 = SitoWebCdsArticoliRegolamentoUnitTest.create_sitoWebCdsArticoliRegolamento(**{
            'id': 2,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'numero': 11,
            'titolo_articolo_it': 'Prova',
            'testo_it': 'Contenuto',
            'titolo_articolo_en': 'Test',
            'testo_en': 'Content',
            'visibile': 0,
            'dt_mod': datetime.datetime.today(),
        })

        # Portal Object 1 visible
        o1 = SitoWebCdsOggettiPortaleUnitTest.create_sitoWebCdsOggettiPortale(**{
            'id': 1,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'id_oggetto_portale': 1,
            'id_classe_oggetto_portale': 1,
            'testo_it': 'prova',
            'testo_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })


        # Item art_reg 1 visible - linked to a1
        item1 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 1,
            'titolo_it': 'Item1',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_articoli_regolamento': a1,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 2 visible - linked to a2
        item2 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 2,
            'titolo_it': 'Item2',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_articoli_regolamento': a2,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 3 visible - linked to o1
        item3 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 3,
            'titolo_it': 'Item3',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_oggetti_portale': o1,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 5 NOT visible - linked to a1
        item5 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 5,
            'titolo_it': 'Item5',
            'id_sito_web_cds_topic': topic2,
            'id_sito_web_cds_articoli_regolamento': a1,
            'ordine': 0,
            'visibile': 0,
            'dt_mod': datetime.datetime.today()
        })

        # art_reg_altri_dati visible - linked to item1
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 1,
            'id_sito_web_cds_topic_articoli_reg': item1,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        # art_reg_altri_dati NOT visible - linked to item1
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 2,
            'id_sito_web_cds_topic_articoli_reg': item1,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 0,
            'dt_mod': datetime.datetime.today(),
        })

        # art_reg_altri_dati visible - linked to item5
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 3,
            'id_sito_web_cds_topic_articoli_reg': item5,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        url = reverse('ricerca:cdswebsitestopicarticleslist')

        # check url
        res = self.client.get(url)

        assert res.status_code == 200

        # GET

        res = self.client.get(url)
        assert len(res.json()['results']) == 0

        data = {'cds_cod': '1', 'topic_id': 1}
        res = self.client.get(url, data=data)

        # 3 visible, 1 not visible
        assert len(res.json()['results']) == 3
        r_items = res.json()['results']
        r_item1, r_item2 = None, None

        for r_item in r_items:
            if r_item["ID"] == 1:
                r_item1 = r_item
            elif r_item["ID"] == 2:
                r_item2 = r_item

        assert(r_item1 is not None)
        assert(len(r_item1["OtherData"]) == 1)
        assert(r_item1["CdsArticle"] is not None)

        assert(r_item2 is not None)
        assert(len(r_item2["OtherData"]) == 0)
        assert(r_item2["CdsArticle"] is None)

    def test_apisitiwebcdstopicarticleswithpermissions(self):

        self.client.login(username=self.uname, password=self.passw)

        tipo_dato = SitoWebCdsTipoDato.objects.create(descr_breve='TICKET')

        topic = SitoWebCdsTopicListUnitTest.create_sitoWebCdsTopicList(**{
            'id': 1,
            'descr_topic_it': 'prova',
            'descr_topic_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        topic2 = SitoWebCdsTopicListUnitTest.create_sitoWebCdsTopicList(**{
            'id': 2,
            'descr_topic_it': 'prova',
            'descr_topic_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        cds = DidatticaCdsUnitTest.create_didatticaCds(**{
            'cds_id': 1,
            'cds_cod': '1',
            'nome_cds_it': 'Matematica',
            'nome_cds_eng': 'Math',
        })

        # Regulament Article 1 visible
        a1 = SitoWebCdsArticoliRegolamentoUnitTest.create_sitoWebCdsArticoliRegolamento(**{
            'id': 1,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'numero': 11,
            'titolo_articolo_it': 'Prova',
            'testo_it': 'Contenuto',
            'titolo_articolo_en': 'Test',
            'testo_en': 'Content',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),

        })

        # Regulament Article 2 NOT visible
        a2 = SitoWebCdsArticoliRegolamentoUnitTest.create_sitoWebCdsArticoliRegolamento(**{
            'id': 2,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'numero': 11,
            'titolo_articolo_it': 'Prova',
            'testo_it': 'Contenuto',
            'titolo_articolo_en': 'Test',
            'testo_en': 'Content',
            'visibile': 0,
            'dt_mod': datetime.datetime.today(),
        })

        # Portal Object 1 visible
        o1 = SitoWebCdsOggettiPortaleUnitTest.create_sitoWebCdsOggettiPortale(**{
            'id': 1,
            'cds_id': 1,
            'aa_regdid_id': 2023,
            'id_oggetto_portale': 1,
            'id_classe_oggetto_portale': 1,
            'testo_it': 'prova',
            'testo_en': 'test',
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })


        # Item art_reg 1 visible - linked to a1
        item1 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 1,
            'titolo_it': 'Item1',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_articoli_regolamento': a1,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 2 visible - linked to a2
        item2 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 2,
            'titolo_it': 'Item2',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_articoli_regolamento': a2,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 3 visible - linked to o1
        item3 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 3,
            'titolo_it': 'Item3',
            'id_sito_web_cds_topic': topic,
            'id_sito_web_cds_oggetti_portale': o1,
            'ordine': 0,
            'visibile': 1,
            'dt_mod': datetime.datetime.today()
        })

        # Item art_reg 5 NOT visible - linked to a1
        item5 = SitoWebCdsTopicArticoliRegUnitTest.create_sitoWebCdsTopicArticoliReg(**{
            'id': 5,
            'titolo_it': 'Item5',
            'id_sito_web_cds_topic': topic2,
            'id_sito_web_cds_articoli_regolamento': a1,
            'ordine': 0,
            'visibile': 0,
            'dt_mod': datetime.datetime.today()
        })

        # art_reg_altri_dati visible - linked to item1
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 1,
            'id_sito_web_cds_topic_articoli_reg': item1,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        # art_reg_altri_dati NOT visible - linked to item1
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 2,
            'id_sito_web_cds_topic_articoli_reg': item1,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 0,
            'dt_mod': datetime.datetime.today(),
        })

        # art_reg_altri_dati visible - linked to item5
        SitoWebCdsTopicArticoliRegAltriDatiUnitTest.create_sitoWebCdsTopicArticoliRegAltriDati(**{
            'id': 3,
            'id_sito_web_cds_topic_articoli_reg': item5,
            'titolo_it': 'prova',
            'titolo_en': 'test',
            'testo_it': 'prova',
            'testo_en': 'test',
            'id_sito_web_cds_tipo_dato': tipo_dato,
            'ordine': 1,
            'visibile': 1,
            'dt_mod': datetime.datetime.today(),
        })

        url = reverse('ricerca:cdswebsitestopicarticleslist')


        # check url
        res = self.client.get(url)

        assert res.status_code == 200

        # GET

        res = self.client.get(url)
        assert len(res.json()['results']) == 0

        data = {'cds_cod': '1', 'topic_id': "1,2"}


        res = self.client.get(url, data=data, HTTP_AUTHORIZATION= f'Token {self.token.key}')

        assert len(res.json()['results']) == 4




class ApiSitoWebCdsStudyPlansListUnitTest(TestCase):
    def test_apisitiwebcdsstudyplans(self):
        req = Client()

        cds1 = DidatticaCdsUnitTest.create_didatticaCds(**{
            'tipo_corso_cod': 'L',
            'area_cds': 'scienze',
            'cds_id': 1,
            'cds_cod': '1'
        })

        r1 = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
            'stato_regdid_cod': 'A',
            'titolo_congiunto_cod': 'N',
            'cds_id': 1,
            'aa_reg_did': 2022
        })

        dpr1 = DidatticaPianoRegolamentoUnitTest.create_didatticaPianoRegolamento(**{
            'regpiani_id': 1,
            'regdid_id': 1,
            'aa_coorte_id': 2022,
            'aa_regpiani_id': 2022,
            'des': 'prova',
            'def_flg': 1,
            'stato_cod': 'A',
            'stato_des': 'A',
            'regpiani_pdr_id': 1,
            'regpiani_pdr_cod': 'test',
            'regpiani_pdr_des': 'test',
            'flg_exp_seg_stu': 1,

        })

        dps1= DidatticaPianoScheUnitTest.create_didatticaPianoSche(**{
            'sche_piano_id': 1,
            'sche_piano_des': 'prova',
            'sche_piano_cod': 'test',
            'regpiani_id': 1,
            'pds_cod': 'GEN',
            'pds_des': 'Generico',
            'comune_flg': 1,

        })

        dps2 = DidatticaPianoScheUnitTest.create_didatticaPianoSche(**{
            'sche_piano_id': 2,
            'sche_piano_des': 'prova',
            'sche_piano_cod': 'test',
            'regpiani_id': 1,
            'pds_cod': 'GEN',
            'pds_des': 'Generico',
            'comune_flg': 1,

        })

        dps3 = DidatticaPianoScheUnitTest.create_didatticaPianoSche(**{
            'sche_piano_id': 3,
            'sche_piano_des': 'prova',
            'sche_piano_cod': 'test',
            'regpiani_id': 1,
            'pds_cod': 'GEN',
            'pds_des': 'Generico',
            'comune_flg': 1,

        })
        dpsv1 = DidatticaPianoSceltaVincoliUnitTest.create_didatticaPianoSceltaVincoli(**{
            'sce_id': 1,
        })
        dpsv2 = DidatticaPianoSceltaVincoliUnitTest.create_didatticaPianoSceltaVincoli(**{
            'sce_id': 2,
        })
        dpsv3 = DidatticaPianoSceltaVincoliUnitTest.create_didatticaPianoSceltaVincoli(**{
            'sce_id': 3,
        })
        dpssp1 = DidatticaPianoSceltaSchePianoUnitTest.create_didatticaPianoSceltaSchePiano(**{
            'sce_id': 1,
            'sche_piano_id': 1,
            'tipo_sce_cod': 'O',
            'apt_slot_ord_num': 5,
        })

        af1 = DidatticaPianoSceltaAfUnitTest.create_didatticaPianoSceltaAf(**{
            'sce_id': 1,
            'anno_corso_af': 2022,
            'ciclo_des': 'Prova',
            'af_gen_des': 'Prova',
            'af_id': 1,
            'tipo_af_des_af': 'Contenuto',
            'ambito_des_af': 'Test',
            'sett_cod': 'Content',
            'peso': 6,

        })

        af2 = DidatticaPianoSceltaAfUnitTest.create_didatticaPianoSceltaAf(**{
            'sce_id': 2,
            'anno_corso_af': 2022,
            'ciclo_des': 'Prova',
            'af_gen_des': 'Prova',
            'af_id': 1,
            'tipo_af_des_af': 'Contenuto',
            'ambito_des_af': 'Test',
            'sett_cod': 'Content',
            'peso': 6,

        })

        af3 = DidatticaPianoSceltaAfUnitTest.create_didatticaPianoSceltaAf(**{
            'sce_id': 3,
            'anno_corso_af': 2022,
            'ciclo_des': 'Prova',
            'af_gen_des': 'Prova',
            'af_id': 2,
            'tipo_af_des_af': 'Contenuto',
            'ambito_des_af': 'Test',
            'sett_cod': 'Content',
            'peso': 6,

        })

        da1 = DidatticaAmbitiUnitTest.create_didatticaAmbiti(**{
            'amb_id': 1
        })

        dpssp2 = DidatticaPianoSceltaSchePianoUnitTest.create_didatticaPianoSceltaSchePiano(**{
            'sce_id': 2,
            'sche_piano_id': 2,
            'tipo_sce_cod': 'N',
            'amb_id': 1,
            'ambito_des': 'Prova',
            'min_unt': 1,
            'max_unt': 2,
            'sce_des': 'Content',
            'apt_slot_ord_num': 1,
            'tipo_sce_cod': 'Pr',
            'tipo_sce_des': 'Prova',
            'tipo_regsce_cod': 'P',
            'tipo_regsce_des': 'Prova',
            'tipo_um_regsce_cod': 'P',
            'vin_sce_des': 1,
            'vin_id': 1,

        })

        dpssp3 = DidatticaPianoSceltaSchePianoUnitTest.create_didatticaPianoSceltaSchePiano(**{
            'sce_id': 3,
            'sche_piano_id': 3,
            'tipo_sce_cod': 'N',
            'ambito_des': 'Prova',
            'min_unt': 1,
            'max_unt': 2,
            'sce_des': 'Content',
            'apt_slot_ord_num': 1,
            'tipo_sce_cod': 'Pr',
            'tipo_sce_des': 'Prova',
            'tipo_regsce_cod': 'P',
            'tipo_regsce_des': 'Prova',
            'tipo_um_regsce_cod': 'P',
            'amb_id_af_regsce': 1

        })

        daf1 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'amb_id': 1,
            'af_gen_id': 1,
            'af_gen_cod': 'AAA',
            'des': 'Prova',
            'af_gen_des_eng': 'Test',
            'anno_corso': 1,
            'sett_cod': 'Sem',
            'sett_des': 'Semestere',
            'peso': 6,
            'fat_part_stu_cod': 'AA',

        })

        daf2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 2,
            'amb_id': 2,
            'af_gen_id': 2,
            'af_gen_cod': 'AAA',
            'des': 'Prova',
            'af_gen_des_eng': 'Test',
            'anno_corso': 1,
            'sett_cod': 'Sem',
            'sett_des': 'Semestere',
            'peso': 6,
            'fat_part_stu_cod': 'AA',

        })

        daf2 = DidatticaAttivitaFormativaUnitTest.create_didatticaAttivitaFormativa(**{
            'af_id': 3,
            'amb_id': 3,
            'af_gen_id': 3,
            'af_gen_cod': 'AAA',
            'des': 'Prova',
            'af_gen_des_eng': 'Test',
            'anno_corso': 1,
            'sett_cod': 'Sem',
            'sett_des': 'Semestere',
            'peso': 6,
            'fat_part_stu_cod': 'AA',

        })


        url = reverse('ricerca:cdswebsitestudyplanslist')

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()['results']) == 0

        data = {'cds_cod': '1', 'year': 2022}
        res = req.get(url, data=data)
        assert len(res.json()['results']) == 1
