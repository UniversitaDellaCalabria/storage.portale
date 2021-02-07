from django.test import TestCase, Client
from django.urls import reverse

from .util_test import *
from .serializers import CreateUpdateAbstract


class ApiCdSListUnitTest(TestCase):

    def test_apicdslist(self):
        req = Client()
        #user = ContextUnitTest.create_user(username='staff',is_staff=True)

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
            'titolo_congiunto_cod': 'N'
        })

        url = reverse('ricerca:cdslist')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: language
        data = {'language': 'it'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: language
        data = {'language': 'eng'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: coursetype
        data = {'coursetype': '1'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: courseclassid
        data = {'courseclassid': '1'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: courseclassname
        data = {'courseclassname': 'laurea in informatica'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: courseclassgroup
        # data = {'courseclassgroup': ''}
        # res = req.get(url, data=data)
        # assert res.json()[0]['RegDidId'] == 1

        # param: departmentid
        data = {'departmentid': 1}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: departmentname
        data = {'departmentname': 'matematica e informatica'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: academicyear
        data = {'academicyear': 2020}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: jointdegree
        data = {'jointdegree': 'N'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: cdslanguage
        data = {'cdslanguage': 'ita'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: keywords ita
        data = {'keywords': 'informatica'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: keywords eng
        data = {'keywords': 'computer', 'language': 'eng'}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: keywords eng wrong
        data = {'keywords': 'math', 'language': 'eng'}
        res = req.get(url, data=data)
        assert len(res.json()) == 0

        # param: all
        data = {'cdslanguage': 'ita',
                'jointdegree': 'N',
                'academicyear': 2020,
                'departmentname': 'math and computer science',
                'departmentid': 1,
                'courseclassname': 'laurea in informatica',
                'courseclassid': '1',
                'coursetype': '1',
                'language': 'eng',
                }
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1


class OpenApiSchemaUnitTest(TestCase):
    def test_openapi(self):
        req = Client()
        url = reverse('ricerca:openapi-schema')
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

        didattica_lingua = DidatticaCdsLinguaUnitTest.create_didatticaCdsLingua(**{
            'cdsord': didattica_cds,
        })
        assert isinstance(didattica_lingua.__str__(), str)

        didattica_regolamento = DidatticaRegolamentoUnitTest.create_didatticaRegolamento(**{
            'regdid_id': 1,
        })
        assert isinstance(didattica_regolamento.__str__(), str)

        didattica_testi_regolamento = DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
            'regdid': didattica_regolamento,
        })
        assert isinstance(didattica_testi_regolamento.__str__(), str)


class ApiCdSInfoUnitTest(TestCase):

    def test_apicdslist(self):
        req = Client()
        #user = ContextUnitTest.create_user(username='staff',is_staff=True)

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
        # DidatticaTestiRegolamentoUnitTest.create_didatticaTestiRegolamento(**{
        #     'txt_id': 3,
        #     'regdid': reg,
        #     'tipo_testo_regdid_cod': 'OBB_SPEC',
        # })

        url = reverse('ricerca:cdsinfo')

        # check url
        res = req.get(url)
        assert res.status_code == 200

        # GET

        # param: language
        data = {'language': 'it', 'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: language
        data = {'language': 'eng', 'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()[0]['RegDidId'] == 1

        # param: language
        data = {'cdsid': 1}
        res = req.get(url, data=data)
        assert res.json()[
            0]['CdSProfiles']['profiloprova']['FUNZIONI'] == 'provadescrizione'
