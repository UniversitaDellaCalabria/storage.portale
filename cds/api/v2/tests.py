from generics.utils import encrypt
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiCdsUnitTestMethods


class ApiCdsUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def assert_data_regDidId(self, url, data):
        res = self.req.get(url, data=data)
        self.assertEqual(res.json()["results"][0]["regDidId"], 1)

    def test_apiacademicyears(self):
        ApiCdsUnitTestMethods.create_didatticaRegolamento(regdid_id=1, aa_reg_did=2015)
        ApiCdsUnitTestMethods.create_didatticaRegolamento(regdid_id=2, aa_reg_did=2016)
        ApiCdsUnitTestMethods.create_didatticaRegolamento(regdid_id=3, aa_reg_did=2017)

        url = reverse("cds:apiv2:academic-years-list")

        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 3)
        self.assertEqual(res.json()["results"][1]["aaRegDid"], "2016")

    def test_apidegreetypeslist(self):
        dip = ApiCdsUnitTestMethods.create_didatticaDipartimento(dip_id=1)
        ApiCdsUnitTestMethods.create_didatticaCds(
            dip=dip, cds_id=1, tipo_corso_cod="L", tipo_corso_des="Laurea", cdsord_id=1
        )
        ApiCdsUnitTestMethods.create_didatticaCds(
            dip=dip,
            cds_id=2,
            tipo_corso_cod="LM5",
            tipo_corso_des="Laurea magistrale ciclo unico",
            cdsord_id=2,
        )
        ApiCdsUnitTestMethods.create_didatticaCds(
            dip=dip,
            cds_id=3,
            tipo_corso_cod="LM",
            tipo_corso_des="Laurea Magistrale",
            cdsord_id=3,
        )
        ApiCdsUnitTestMethods.create_didatticaCds(
            dip=dip, cds_id=4, tipo_corso_cod="L", tipo_corso_des="Laurea", cdsord_id=4
        )

        url = reverse("cds:apiv2:degree-types-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 3)
        self.assertEqual(res.json()["results"][0]["courseType"], "L")

    def test_apicdsareaslist(self):
        ApiCdsUnitTestMethods.create_didatticaCds(
            area_cds="aaa", area_cds_en="Study Area AAA"
        )
        ApiCdsUnitTestMethods.create_didatticaCds(
            cds_id=2, cdsord_id=3, area_cds=None, area_cds_en=None
        )

        url = reverse("cds:apiv2:cds-areas-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiallstudyactivitieslist(self):
        ApiCdsUnitTestMethods.create_didatticaDipartimento(dip_des_it="qualcosa")
        regdid = ApiCdsUnitTestMethods.create_didatticaRegolamento()
        ApiCdsUnitTestMethods.create_didatticaCds(
            cds_id=1,
            cds_cod="aaaa",
            nome_cds_it="Matematica",
            nome_cds_eng="Math",
            dip_id=1,
        )
        p1 = ApiCdsUnitTestMethods.create_personale(
            id=1,
            nome="Franco",
            cognome="Garofalo",
            cd_ruolo="PO",
            id_ab=1,
            matricola="111111",
        )
        ApiCdsUnitTestMethods.create_didatticaCopertura(af_id=1, personale_id=1)
        ApiCdsUnitTestMethods.create_didatticaAttivitaFormativa(
            af_id=1,
            des="informatica",
            af_gen_des_eng="computer science",
            regdid=regdid,
            anno_corso=1,
            af_radice_id=1,
            matricola_resp_did=p1,
            mutuata_flg=1,
            af_master_id=2,
            sett_cod="INF/01",
            sett_des="Interdisciplinare",
            aa_off_id=2015,
        )

        url = reverse("cds:apiv2:activities-list")
        res = self.req.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)
        self.assert_data_len(url, {"department_cod": "DIP01"}, 1)
        self.assert_data_len(url, {"name": "matematica"}, 0)
        self.assert_data_len(url, {"teacher_last_name": "Garofalo"}, 1)
        self.assert_data_len(url, {"cds_cod": "aaaa"}, 1)
        self.assert_data_len(url, {"teacher_matricola": encrypt("111111")}, 1)
        self.assert_data_len(url, {"cds_name": "Informatica"}, 0)
        self.assert_data_len(url, {"ssd": "INF"}, 1)
        self.assert_data_len(url, {"ssd": "MAT"}, 0)
        self.assert_data_len(url, {"cycle": "Primo semestre"}, 1)
        self.assert_data_len(url, {"course_year": 1}, 1)
        self.assert_data_len(url, {"academic_year": 2015}, 1)

    def test_apiAcademicPathways(self):
        cds = ApiCdsUnitTestMethods.create_didatticaCds(durata_anni=3)
        regdid = ApiCdsUnitTestMethods.create_didatticaRegolamento(cds=cds)
        pds = ApiCdsUnitTestMethods.create_didatticaPdsRegolamento(regdid=regdid)
        ApiCdsUnitTestMethods.create_didatticaAttivitaFormativa(
            pds_regdid=pds,
            regdid=regdid,
            des="matematica",
            af_gen_des_eng="math",
            af_id=1,
            af_radice_id=1,
            anno_corso=1,
        )

        ## LIST
        url = reverse(
            "cds:apiv2:academic-pathways-list", kwargs={"regdid_id": regdid.regdid_id}
        )
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["id"], 1)
        self.assertEqual(res.json()["results"][0]["duration"], 3)

        res = self.req.get(url, data={"lang": "en"})
        self.assertEqual(res.json()["results"][0]["name"], "des_eng")

        ## DETAIL
        url = reverse(
            "cds:apiv2:academic-pathways-detail",
            kwargs={"regdid_id": regdid.regdid_id, "pds_regdid_id": pds.pds_regdid_id},
        )
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], 1)

        res = self.req.get(url)
        self.assertEqual(res.json()["activities"]["1"][0]["name"], "matematica")

        res = self.req.get(url, data={"lang": "en"})
        self.assertEqual(res.json()["activities"]["1"][0]["name"], "math")

    def test_apicdslist(self):
        dip = ApiCdsUnitTestMethods.create_didatticaDipartimento(dip_id=1)
        didatticaCds = ApiCdsUnitTestMethods.create_didatticaCds(
            dip=dip, tipo_corso_cod="L", area_cds="scienze", cds_id=1
        )
        ApiCdsUnitTestMethods.create_didatticaCdsLingua(
            cdsord=didatticaCds, iso6392_cod="ita"
        )
        r1 = ApiCdsUnitTestMethods.create_didatticaRegolamento(
            regdid_id=1, stato_regdid_cod="A", titolo_congiunto_cod="N", cds_id=1
        )
        ApiCdsUnitTestMethods.create_didatticaCdsAltriDatiUfficio()
        ApiCdsUnitTestMethods.create_didatticaCdsAltriDati(regdid=r1)
        r1.get_ordinamento_didattico()

        ## LIST
        url = reverse("cds:apiv2:cds-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)

        self.assert_data_regDidId(url, {"type": "L"})
        self.assert_data_regDidId(url, {"lang": "it"})
        self.assert_data_regDidId(url, {"lang": "en"})
        self.assert_data_regDidId(url, {"course_class_cod": "1"})
        self.assert_data_regDidId(url, {"area": "scienze"})
        self.assert_data_regDidId(url, {"course_class_name": "laurea in informatica"})
        self.assert_data_regDidId(url, {"department_cod": "DIP01"})
        self.assert_data_regDidId(
            url, {"department_name": "Dipartimento di Informatica", "lang": "it"}
        )
        self.assert_data_regDidId(url, {"academic_year": 2020})
        self.assert_data_regDidId(url, {"joint_degree": "N"})
        self.assert_data_regDidId(url, {"language": "ITALIANO", "lang": "it"})
        self.assert_data_regDidId(url, {"search": "informatica", "lang": "it"})
        self.assert_data_regDidId(url, {"search": "computer", "lang": "en"})
        self.assert_data_regDidId(url, {"search": "math", "lang": "en"})
        self.assert_data_regDidId(
            url,
            {
                "cdslanguage": "ita",
                "jointdegree": "N",
                "academicyear": 2020,
                "departmentname": "math and computer science",
                "departmentcod": 1,
                "courseclassname": "laurea in informatica",
                "courseclasscod": "1",
                "coursetype": "L",
                "lang": "en",
            },
        )

        ## DETAIL
        url = reverse("cds:apiv2:cds-detail", kwargs={"pk": r1.regdid_id})

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)

        res = self.req.get(url, data={"lang": "it"})
        self.assertEqual(res.json()["regDidId"], 1)

        res = self.req.get(url, data={"lang": "en"})
        self.assertEqual(res.json()["regDidId"], 1)

        url = reverse("cds:apiv2:cds-detail", kwargs={"pk": 10})
        res = self.req.get(url, data={"lang": "it"})
        self.assertEqual(len(res.json()), 1)

    def test_apicdsexpiredlist(self):
        dip = ApiCdsUnitTestMethods.create_didatticaDipartimento(dip_id=1)
        cds1 = ApiCdsUnitTestMethods.create_didatticaCds(dip=dip, cds_id=1, cds_cod="CDS001", durata_anni=3)
        cds2 = ApiCdsUnitTestMethods.create_didatticaCds(dip=dip, cds_id=2, cds_cod="CDS002", durata_anni=2, cdsord_id=2)
        
        ApiCdsUnitTestMethods.create_didatticaRegolamento(cds=cds1, regdid_id=1, aa_reg_did=settings.CURRENT_YEAR - 5, stato_regdid_cod="A")
        ApiCdsUnitTestMethods.create_didatticaRegolamento(cds=cds2, regdid_id=2, aa_reg_did=settings.CURRENT_YEAR - 4, stato_regdid_cod="A")
        
        url = reverse("cds:apiv2:cds-expired-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)

        
    def test_apicdsmorphlist(self):
        cds1 = ApiCdsUnitTestMethods.create_didatticaCds(cds_id=1, cds_cod="CDS001")
        cds2 = ApiCdsUnitTestMethods.create_didatticaCds(cds_id=2, cds_cod="CDS002", cdsord_id=2)
        cds3 = ApiCdsUnitTestMethods.create_didatticaCds(cds_id=3, cds_cod="CDS003", cdsord_id=3)
        
        ApiCdsUnitTestMethods.create_didatticaCdsCollegamento(cds=cds2,cds_prec=cds1)
        ApiCdsUnitTestMethods.create_didatticaCdsCollegamento(cds=cds3,cds_prec=cds2)

        url = reverse('cds:apiv2:cds-morph-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

