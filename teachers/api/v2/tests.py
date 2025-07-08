from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiTeachersUnitTestMethods
from generics.utils import decrypt, encrypt


class TeachersUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)

    def test_apiteachersunittest(self):
        u1 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            uo_padre="1",
        )
        u2 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            uo_padre="1",
        )

        doc1 = ApiTeachersUnitTestMethods.create_personale(
            id=1,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            id_ab=1,
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
        )
        doc2 = ApiTeachersUnitTestMethods.create_personale(
            id=2,
            nome="Franco",
            middle_name="Luigi",
            cognome="Garofalo",
            cd_ruolo="PO",
            id_ab=2,
            matricola="111111",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u2,
            cv_full_it="AAA",
            cv_short_it="A",
            cv_full_eng="BBB",
            cv_short_eng="B",
        )
        ApiTeachersUnitTestMethods.create_personale(
            id=3,
            nome="Pippo",
            cognome="Inzaghi",
            cd_ruolo="PO",
            id_ab=3,
            matricola="111113",
            fl_docente=1,
            flg_cessato=1,
            cd_uo_aff_org=u1,
        )
        ApiTeachersUnitTestMethods.create_personale(
            id=4,
            nome="Zlatan",
            cognome="Ibrahimovic",
            cd_ruolo="PO",
            id_ab=4,
            matricola="111114",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
        )
        ApiTeachersUnitTestMethods.create_didatticaDipartimento(
            dip_id=1,
            dip_cod=1,
            dip_des_it="Matematica e Informatica",
            dip_des_eng="Math and Computer Science",
        )
        regdid = ApiTeachersUnitTestMethods.create_didatticaRegolamento(
            regdid_id=1,
        )
        regdid2 = ApiTeachersUnitTestMethods.create_didatticaRegolamento(
            regdid_id=2,
        )
        course1 = ApiTeachersUnitTestMethods.create_didatticaAttivitaFormativa(
            af_id=1,
            des="matematica",
            af_gen_des_eng="math",
            ciclo_des="Primo semestre",
            regdid=regdid,
            af_radice_id=1,
            anno_corso=1,
        )
        course2 = ApiTeachersUnitTestMethods.create_didatticaAttivitaFormativa(
            af_id=2,
            des="informatica",
            af_gen_des_eng="computer science",
            ciclo_des="Secondo semestre",
            regdid=regdid2,
            af_radice_id=2,
            anno_corso=2,
        )
        ApiTeachersUnitTestMethods.create_didatticaCopertura(
            af=course1,
            personale=doc1,
            aa_off_id=2019,
            fat_part_stu_des="111",
            fat_part_stu_cod="AA",
            part_stu_des="11",
            part_stu_cod="A",
            tipo_fat_stu_cod="ALF",
            part_ini="A",
            part_fine="Z",
        )
        ApiTeachersUnitTestMethods.create_didatticaCopertura(
            af=course2, personale=doc2, aa_off_id=2020
        )

        url = reverse("teachers:apiv2:teachers-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 4)

        data = {"search": "gar"}
        res = self.req.get(url, data=data)
        self.assertEqual(decrypt(res.json()["results"][0]["id"]), "111111")

        data = {"role": "PA", "lang": "it"}
        res = self.req.get(url, data=data)
        self.assertIsNone(res.json()["results"][0]["CVFull"])

        data = {"department": 1}
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 4)

        data = {"department": 1, "role": "PO"}
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 3)

        data = {"department": 1, "role": "PA", "lang": "en", "year": "2015"}
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 0)

        data = {"cds": 1}
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 0)

        url2 = reverse("teachers:apiv2:teachers-detail", kwargs={"matricola": "111112"})

        res = self.req.get(url2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["id"], 2)
        self.assertEqual(len(res.json()["results"]), 2)

        self.assert_data_len(url2, {"yearFrom": 2020}, 1)
        self.assert_data_len(url2, {"year": 2020}, 1)
        self.assert_data_len(url2, {"yearTo": 2020}, 1)
        self.assert_data_len(url2, {"yearFrom": 2019, "yearTo": 2020}, 1)

    def test_apiteachernewslist(self):
        p1 = ApiTeachersUnitTestMethods.create_personale(id=1)
        ApiTeachersUnitTestMethods.create_docentePtaBacheca(matricola=p1)

        url = reverse(
            "teachers:apiv2:teachers-news-list", kwargs={"id": encrypt("111112")}
        )
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiteachermaterialslist(self):
        p1 = ApiTeachersUnitTestMethods.create_personale(id=1)
        ApiTeachersUnitTestMethods.create_docenteMaterialeDidattico(matricola=p1)

        url = reverse(
            "teachers:apiv2:teachers-materials-list", kwargs={"id": encrypt("111112")}
        )
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiPublicationsList(self):
        u1 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa()
        u2 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
            id_ab=2,
            denominazione="bbb",
            denominazione_padre="d",
            uo_padre="22",
        )
        p1 = ApiTeachersUnitTestMethods.create_personale(id=1, cd_uo_aff_org=u1)
        p2 = ApiTeachersUnitTestMethods.create_personale(
            id=2,
            id_ab=2,
            matricola="111113",
            cd_uo_aff_org=u2,
            cod_fis="SMN2",
        )
        p3 = ApiTeachersUnitTestMethods.create_personale(
            id=3,
            cognome="Pino",
            id_ab=3,
            matricola="111119",
            cd_uo_aff_org=u2,
            cod_fis="SMN3",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity()
        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity(
            community_id=2,
            community_name="Community 2",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneCollection()
        ApiTeachersUnitTestMethods.create_pubblicazioneCollection(
            collection_id=2,
            community_id=2,
            collection_name="Collection 2",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(item_id=1)
        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(
            item_id=2,
            title="pub2",
            des_abstract="abstract italiano2",
            des_abstracteng="abstract inglese2",
            date_issued_year=2019,
            pubblicazione="Convegno Cosenza",
            label_pubblicazione="Convegno",
            collection_id=2,
            url_pubblicazione="aba",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(
            item_id=3,
            title="pub3",
            des_abstract="abstract italiano3",
            des_abstracteng="abstract inglese3",
            date_issued_year=9999,
            pubblicazione="Convegno Cosenza",
            label_pubblicazione="Convegno",
            collection_id=2,
            url_pubblicazione="ccc",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneAutori(item_id=1, ab=p1)
        ApiTeachersUnitTestMethods.create_pubblicazioneAutori(item_id=2, ab=p2)
        ApiTeachersUnitTestMethods.create_pubblicazioneAutori(item_id=3, ab=p3)

        url = (
            reverse("teachers:apiv2:publications-list")
            + f"?teacherid={encrypt('111112')}"
        )

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "year": 2020,
            "search": "pub",
            "type": 1,
            "contributor": "111119",
        }

        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiAllPublicationsList(self):
        u1 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa()
        u2 = ApiTeachersUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
            id_ab=2,
            denominazione="bbb",
            denominazione_padre="d",
        )
        p1 = ApiTeachersUnitTestMethods.create_personale(
            id=1,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            ds_ruolo_locale="Professore Associato",
            id_ab=1,
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            cod_fis="SMN1",
        )
        p2 = ApiTeachersUnitTestMethods.create_personale(
            id=2,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            ds_ruolo_locale="Professore Associato",
            id_ab=2,
            matricola="111113",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u2,
            cod_fis="SMN2",
        )

        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity(
            community_id=1,
            community_name="Community 1",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity(
            community_id=2,
            community_name="Community 2",
        )

        ApiTeachersUnitTestMethods.create_pubblicazioneCollection(
            collection_id=1,
            community_id=1,
            collection_name="Collection 1",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneCollection(
            collection_id=2,
            community_id=2,
            collection_name="Collection 2",
        )

        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(
            item_id=1,
            title="pub1",
            des_abstract="abstract italiano",
            des_abstracteng="abstract inglese",
            date_issued_year=2020,
            pubblicazione="Giornale 1",
            contributors="Pinnola",
            label_pubblicazione="Rivista",
            collection_id=1,
            url_pubblicazione="aaa",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(
            item_id=2,
            title="pub2",
            des_abstract="abstract italiano2",
            des_abstracteng="abstract inglese2",
            date_issued_year=2019,
            pubblicazione="Convegno Cosenza",
            label_pubblicazione="Convegno",
            collection_id=2,
            url_pubblicazione="aba",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneDatiBase(
            item_id=3,
            title="pub3",
            des_abstract="abstract italiano3",
            des_abstracteng="abstract inglese3",
            date_issued_year=9999,
            pubblicazione="Convegno Cosenza",
            label_pubblicazione="Convegno",
            collection_id=2,
            url_pubblicazione="ccc",
        )

        ApiTeachersUnitTestMethods.create_pubblicazioneAutori(
            item_id=1,
            ab=p1,
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneAutori(
            item_id=3,
            ab=p2,
        )

        url = reverse("teachers:apiv2:publications-list")

        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][1]["abstract"], "abstract italiano")

        data = {"year": 2020, "search": "pub", "type": 1, "contributors": "Pinnola"}
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), 1)

    def test_apiPublicationsCommunityTypesList(self):
        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity(
            community_id=1,
            community_name="Community 1",
        )
        ApiTeachersUnitTestMethods.create_pubblicazioneCommunity(
            community_id=2,
            community_name="Community 2",
        )
        
        url = reverse("teachers:apiv2:publicationscommunitytypes-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["results"][0]["name"], "Community 1")

        
