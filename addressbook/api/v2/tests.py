from django.test import TestCase, Client
from django.urls import reverse
from .util_test import ApiAddressBookUnitTestMethods
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from generics.utils import decrypt, encrypt
import datetime
class AddressBookUnitTest(TestCase):
    def setUp(self):
        self.req = Client()

    def assert_data_len(self, url, data, result):
        res = self.req.get(url, data=data)
        self.assertEqual(len(res.json()["results"]), result)
        
    def test_apiaddressbookstructureslist(self):
        u1 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa()
        u2 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="3", uo_padre="2"
        )
        p1 = ApiAddressBookUnitTestMethods.create_personale(cd_uo_aff_org=u1)
        ApiAddressBookUnitTestMethods.create_personaleAttivoTuttiRuoli(
            matricola=p1,
            cd_uo_aff_org=u1,
            cd_ruolo="PO",
            cod_fis="ZLT"
        )
        ApiAddressBookUnitTestMethods.create_personalePrioritaRuolo(
            cd_ruolo="PO",
            priorita=1,
        )

        p2 = ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            nome="Lionel",
            cognome="Messi",
            cd_ruolo="AM",
            ds_ruolo_locale="Amministrazione",
            id_ab=2,
            matricola="111113",
            fl_docente=0,
            cd_uo_aff_org=u2,
            cod_fis="LNL1",
            cv_full_it="BBB",
            cv_short_it="B",
            cv_full_eng="AA",
            cv_short_eng="A",
        )
        ApiAddressBookUnitTestMethods.create_personale(
            id=10,
            id_ab=10,
            matricola="111119",
            cd_uo_aff_org=u1,
            cod_fis="SMN10",
        )
        ApiAddressBookUnitTestMethods.create_personale(
            id=55,
            nome="Simone2",
            id_ab=55,
            matricola="111166",
            cd_uo_aff_org=u2,
            cod_fis="SMN25",
        )
        ApiAddressBookUnitTestMethods.create_personale(
            id=13,
            nome="Simone13",
            cognome="Mungari",
            id_ab=13,
            matricola=p2,
            fl_docente=0,
            flg_cessato=1,
            cd_uo_aff_org=u1,
            cod_fis="SMN13",
        )
        ApiAddressBookUnitTestMethods.create_personale(
            id=4,
            nome="Simone4",
            id_ab=4,
            matricola="111115",
            fl_docente=0,
            cd_uo_aff_org=u2,
            cod_fis="SMN4",
        )
        p3 = ApiAddressBookUnitTestMethods.create_personale(
            id=3,
            nome="Zlatan",
            cognome="Ibra",
            id_ab=3,
            matricola=p1,
            fl_docente=1,
            flg_cessato=0,
            cod_fis="ZLT",
            cd_uo_aff_org=u2,
            dt_rap_fin="2222-02-02",
        )
        tipo_contatto = ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="EMAIL",
            descr_contatto="Posta Elettronica",
        )
        tipo_contatto2 = ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="tipo_contatto2",
            descr_contatto="tipo_contatto2",
        )
        tipo_contatto_phone = (
            ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
                cod_contatto="Telefono Cellulare Ufficio",
                descr_contatto="Telefono Cellulare Ufficio",
            )
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Riferimento Ufficio",
            descr_contatto="Riferimento Ufficio",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="POSTA ELETTRONICA CERTIFICATA",
            descr_contatto="POSTA ELETTRONICA CERTIFICATA",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Posta Elettronica Privata",
            descr_contatto="Posta Elettronica Privata",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Fax",
            descr_contatto="Fax",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Telefono Residenza",
            descr_contatto="Telefono Residenza",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Telefono Domicilio",
            descr_contatto="Telefono Domicilio",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Telefono Cellulare",
            descr_contatto="Telefono Cellulare",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="URL Sito WEB Curriculum Vitae",
            descr_contatto="URL Sito WEB Curriculum Vitae",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="URL Sito WEB",
            descr_contatto="URL Sito WEB",
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="Skype",
            descr_contatto="Skype",
        )
        ApiAddressBookUnitTestMethods.create_personaleContatti(
            cd_tipo_cont=tipo_contatto,
            cod_fis=p1,
        )
        ApiAddressBookUnitTestMethods.create_personaleContatti(
            cd_tipo_cont=tipo_contatto2,
            id_ab=2,
            cod_fis=p2,
            contatto="email2@email",
            prg_priorita=1,
        )
        ApiAddressBookUnitTestMethods.create_personaleContatti(
            cd_tipo_cont=tipo_contatto_phone,
            id_ab=3,
            cod_fis=p3,
            contatto="999",
            prg_priorita=1000,
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(cod_fis=p2)
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            cod_fis=p3,
            termine="2222-03-26",
            decorrenza="1900-01-01",
            ds_funzione="Direttore",
            matricola=p1,
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            denominazione="Dipartimento di Matematica e Informatica",
            dt_fine_val="2222-01-01",
        )

        url = reverse("addressbook:apiv2:addressbook-list")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assert_data_len(url, {"structureid": "88", "lang": "it"}, 0)
        self.assert_data_len(url, {"search": "Ibra", "function": "Direttore"}, 1)
        self.assert_data_len(url, {"search": "Mungar", "structureid": "99"}, 0)
        self.assert_data_len(url, {"phone": "999"}, 1)
        self.assert_data_len(url, {"phone": "999", "role": "PO", "structuretypes": "DRZ"}, 1)
        self.assert_data_len(url, {"role": "PO", "structuretypes": "DRZ"}, 1)
        self.assert_data_len(url, {"phone": "999", "structuretypes": "DRZ"}, 1)
        self.assert_data_len(url, {"phone": "999", "role": "PO"}, 1)
        self.assert_data_len(url, {"structuretypes": "DRZ"}, 1)
        # self.assert_data_len(url, {"structuretree": "1"}, 1)
        # self.assert_data_len(url, {"structuretree": "2"}, 1)
        self.assert_data_len(url, {"phone": "999", "role": "PO", "structuretypes": "DRZ", "structureid": 3}, 0)
        
        res = self.req.get(url, {"role": "PO"})
        self.assertEqual(res.json()["results"][0]["name"], "Ibra Zlatan")
        
        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse("addressbook:apiv2:addressbook-full-list")
        res = self.req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 200

    def test_apiroleslist(self):
        ApiAddressBookUnitTestMethods.create_personale(
            id=1,
            id_ab=1,
            cod_fis="SMN1",
            matricola="111112",
            cd_ruolo="f",
            ds_ruolo_locale="g",
        )
        
        ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            id_ab=2,
            cod_fis="LNL1",
            matricola="111113",
            cd_ruolo="g",
            ds_ruolo_locale="h",
        )
        
        ApiAddressBookUnitTestMethods.create_personale(
            id=3,
            id_ab=3,
            cod_fis="AB",
            matricola="111115",
            cd_ruolo="1",
            ds_ruolo_locale="o",
        )
        
        url = reverse("addressbook:apiv2:roles-list")
        res = self.req.get(url)
        self.assertEqual(res.json()["results"][0]["role"], "f")
        self.assertEqual(res.json()["results"][1]["roleDescription"], "h")
        self.assertEqual(len(res.json()["results"]), 3)
        
    def test_apipersonaledetail(self):
        u1 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(uo="2", uo_padre="1")
        p1 = ApiAddressBookUnitTestMethods.create_personale(
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
            cv_full_it="AAA",
            cv_short_it="A",
            cv_full_eng="BBB",
            cv_short_eng="B",
        )
        p2 = ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            nome="Lionel",
            cognome="Messi",
            cd_ruolo="AM",
            ds_ruolo_locale="Amministrazione",
            id_ab=2,
            matricola="111113",
            fl_docente=0,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            cod_fis="LNL1",
        )
        p3 = ApiAddressBookUnitTestMethods.create_personale(
            id=3,
            nome="A",
            cognome="B",
            cd_ruolo="AB",
            ds_ruolo_locale="Amministrazione",
            id_ab=3,
            matricola="111114",
            fl_docente=0,
            flg_cessato=0,
            cod_fis="AB",
        )
        tipo_contatto = ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="EMAIL",
            descr_contatto="Posta Elettronica",
        )
        ApiAddressBookUnitTestMethods.create_personaleContatti(
            cd_tipo_cont=tipo_contatto,
            id_ab=1,
            cod_fis=p1,
            prg_priorita=1,
        )
        ApiAddressBookUnitTestMethods.create_personaleContatti(
            cd_tipo_cont=tipo_contatto,
            id_ab=2,
            cod_fis=p2,
            prg_priorita=2,
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=1,
            ds_funzione="Amministrazione",
            termine="2999-12-1",
            cod_fis=p1,
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=2,
            ds_funzione="Delega",
            termine=None,
            cod_fis=p2,
        )
        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="URL Sito WEB Curriculum Vitae",
            descr_contatto="URL Sito WEB Curriculum Vitae",
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            denominazione="Dipartimento di Matematica e Informatica",
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="99",
            denominazione="Dipartimento di Matematica e Informatica",
        )
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            cod_fis=p1,
            termine="2222-03-26",
            decorrenza="1900-01-01",
            ds_funzione="Direttore",
            matricola="111112",
        )
        ApiAddressBookUnitTestMethods.create_personaleAttivoTuttiRuoli(
            matricola=p3, 
            ds_ruolo="test"
        )
        
        url1 = reverse("addressbook:apiv2:addressbook-detail", kwargs={"matricola": encrypt("111112")})
        res1 = self.req.get(url1)
        self.assertEqual(res1.status_code, 200)
        
        url2 = reverse("addressbook:apiv2:addressbook-detail", kwargs={"matricola": encrypt("111113")})
        res2 = self.req.get(url2)
        self.assertEqual(res2.status_code, 200)
        
        url3 = reverse("addressbook:apiv2:addressbook-detail", kwargs={"matricola": encrypt("111114")})
        res3 = self.req.get(url3)
        self.assertEqual(res3.status_code, 200)
        
        self.assertEqual(decrypt(res1.json()["id"]), "111112")
        self.assertEqual(decrypt(res2.json()["id"]), "111113")
        
        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)

        url = reverse(
            "addressbook:apiv1:personale-detail", kwargs={"personaleid": encrypt("111112")}
        )
        res = self.req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        self.assertEqual(res.status_code, 200)
        
    def test_apipersonalefulldetail(self):
        u1  = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            ds_tipo_nodo="facolta",
            cd_tipo_nodo="000",
            id_ab=1,
            denominazione="aaa",
            denominazione_padre="c",
            uo_padre="11",
            cd_csa=1,
            dt_fine_val="2222-01-01",
        )
        
        u2  = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            ds_tipo_nodo="direzione",
            cd_tipo_nodo="CDS",
            id_ab=2,
            denominazione="bbb",
            denominazione_padre="d",
            uo_padre="22",
            cd_csa=2,
            dt_fine_val="2222-01-01",
        )
        
        p1 = ApiAddressBookUnitTestMethods.create_personale(
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
        
        p2 = ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            nome="Lionel",
            cognome="Messi",
            cd_ruolo="AM",
            ds_ruolo_locale="Amministrazione",
            id_ab=2,
            matricola="111113",
            fl_docente=0,
            flg_cessato=0,
            cd_uo_aff_org=u2,
            cod_fis="LNL1",
        )
        
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            ds_tipo_nodo="rettorato",
            cd_tipo_nodo="RET",
            id_ab=3,
            denominazione="ccc",
            denominazione_padre="d",
            uo_padre="33",
            cd_csa=3,
            dt_fine_val="2222-01-01",
        )
        
        tipo_contatto = ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="PEC",
            descr_contatto="Posta Elettronica Certificata",
        )

        ApiAddressBookUnitTestMethods.create_personaleUoTipoContatto(
            cod_contatto="URL Sito WEB Curriculum Vitae",
            descr_contatto="URL Sito WEB Curriculum Vitae",
        )
        
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaContatti(
            cd_tipo_cont=tipo_contatto,
            ab=u1,
            prg_priorita=1,
        )
        
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaContatti(
            cd_tipo_cont=tipo_contatto,
            ab=u2,
            prg_priorita=2,
        )
        
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=1,
            ds_funzione="Amministrazione",
            termine="2999-12-1",
            cod_fis=p1,
            cd_csa=u1,
        )
        
        ApiAddressBookUnitTestMethods.create_unitaOrganizzativaFunzioni(
            id_ab=2,
            ds_funzione="Delega",
            termine=None,
            cod_fis=p2,
            cd_csa=u2,
        )
        
        
        url = reverse("addressbook:apiv2:addressbookstructures-detail", kwargs={"pk": 1})
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["cod"], '1')
        
        url1 = reverse("addressbook:apiv2:addressbookstructures-detail", kwargs={"pk": 2})
        res1 = self.req.get(url1)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.json()["cod"], '2')
        
    def test_apipersonid(self):
        ApiAddressBookUnitTestMethods.create_personale(
            id=1,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            id_ab=1,
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            ds_aff_org="aaaa",
        )
        
        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)
        
        url = reverse("addressbook:apiv2:get-person-id")
        
        # GET
        res = self.req.get(url, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 405

        # POST
        res = self.req.post(url, {"test": "test"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = self.req.post(url, {"id": "99999"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = self.req.post(url, {"id": "111112"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 200

        url = reverse("addressbook:apiv1:get-decrypted-person-id")

        # GET
        res = self.req.get(url, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 405

        # POST
        res = self.req.post(url, {"test": "test"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        res = self.req.post(url, {"id": "99999"}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert res.status_code == 404

        # POST
        m_test_encrypted = encrypt("111111")
        res = self.req.post(
            url, {"id": m_test_encrypted}, HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        assert res.status_code == 200
        
    def test_apipersonnelcfslist(self):
        u1 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="2",
            uo_padre="1",
        )    
        u2 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="3",
            uo_padre="2",
        )    
        
        ApiAddressBookUnitTestMethods.create_personale(
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
            dt_rap_fin="2023-01-03",
            ds_aff_org="aaa",
            cod_fis="SMN1",
        )
        
        ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            nome="Lionel",
            cognome="Messi",
            cd_ruolo="AM",
            ds_ruolo_locale="Amministrazione",
            id_ab=2,
            matricola="111113",
            fl_docente=0,
            flg_cessato=0,
            cd_uo_aff_org=u2,
            dt_rap_fin="2023-01-03",
            ds_aff_org="bbb",
            cod_fis="LNL1",
        )
        
        usr = get_user_model().objects.create(
            **{
                "username": "test",
                "password": "password",
            }
        )
        token = Token.objects.create(user=usr)
        
        url = reverse("addressbook:apiv2:personnel-cfs")
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["cod"], '1')
        
        
        # GET
        res = self.req.get(url, {}, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert len(res.json()["results"]) == 0

        data = {"roles": "PA"}
        res = self.req.get(url, data=data, HTTP_AUTHORIZATION=f"Token {token.key}")
        assert len(res.json()["results"]) == 0
        
    def test_apisortingcontactslist(self):
        u1 = ApiAddressBookUnitTestMethods.create_unitaOrganizzativa(
            uo="1",
            uo_padre="1",
        )
        ApiAddressBookUnitTestMethods.create_personale(
            id=1,
            nome="Simone",
            cognome="Mungari",
            cd_ruolo="PA",
            id_ab=1,
            matricola="111112",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            ds_aff_org="aaaa",
        )
        
        ApiAddressBookUnitTestMethods.create_personale(
            id=2,
            nome="Franco",
            middle_name="Luigi",
            cognome="Garofalo",
            cd_ruolo="PO",
            id_ab=2,
            matricola="111111",
            fl_docente=1,
            flg_cessato=0,
            cd_uo_aff_org=u1,
            ds_aff_org="bbbb",
        )
        
        ApiAddressBookUnitTestMethods.create_didatticaCopertura()
        
        ApiAddressBookUnitTestMethods.create_didatticaCopertura(
            personale_id=2,
            cds_cod="1",
            aa_off_id=datetime.datetime.now().year - 1,
        )
        
        url = reverse("cds:apiv2:sorting-contacts", kwargs={"pk": "1"})
        res = self.req.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["results"]), 1)