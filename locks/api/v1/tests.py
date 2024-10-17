from cds.api.v1.util_tests import DidatticaCdsUnitTest
from cds.models import DidatticaCdsTipoCorso
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse
from locks.concurrency import acquire_lock
from regdid.models import (
    DidatticaArticoliRegolamentoStatus,
    DidatticaArticoliRegolamentoStruttura,
    DidatticaArticoliRegolamentoTitolo,
    DidatticaCdsArticoliRegolamento,
    DidatticaCdsArticoliRegolamentoTestata,
    DidatticaCdsTestataStatus,
)
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest


class ApiLockUnitTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_superuser(
            **{
                "username": "test1",
                "password": "password",
            }
        )
        self.user2 = get_user_model().objects.create_superuser(
            **{
                "username": "test2",
                "password": "password",
            }
        )
        self.dipartimento = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        self.cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": self.dipartimento,
                "tipo_corso_cod": "L",
                "area_cds": "scienze",
                "cds_id": 1,
            }
        )
        self.tipo_corso = DidatticaCdsTipoCorso.objects.create(
            **{
                "tipo_corso_cod": "L",
                "tipo_corso_des": "Laurea",
                "note": "",
                "dt_mod": "2024-01-01",
                "user_mod": self.user1,
            }
        )
        self.titolo = DidatticaArticoliRegolamentoTitolo.objects.create(
            **{
                "descr_titolo_it": "Titolo I",
                "ordine": 0,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.struttura_articolo = DidatticaArticoliRegolamentoStruttura.objects.create(
            **{
                "aa": "2024",
                "titolo_it": "Test titolo articolo",
                "numero": 1,
                "visibile": 1,
                "id_didattica_cds_tipo_corso": self.tipo_corso,
                "id_didattica_articoli_regolamento_titolo": self.titolo,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.regolamento_status = DidatticaArticoliRegolamentoStatus.objects.create(
            **{
                "status_cod": "0",
                "status_desc": "In bozza",
            }
        )
        self.testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            **{
                "cds_id": self.cds.pk,
                "aa": "2024",
                "note": "",
                "visibile": 1,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.testata_status = DidatticaCdsTestataStatus.objects.create(
            **{
                "id_didattica_articoli_regolamento_status": self.regolamento_status,
                "id_didattica_cds_articoli_regolamento_testata": self.testata,
                "data_status": "2024-01-01",
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.articolo = DidatticaCdsArticoliRegolamento.objects.create(
            **{
                "id_didattica_cds_articoli_regolamento_testata": self.testata,
                "id_didattica_articoli_regolamento_struttura": self.struttura_articolo,
                "testo_it": "Test testo articolo",
                "visibile": 1,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )

    def test_apilock(self):
        req = Client()
        # user1 login
        req.login(
            **{
                "username": "test1",
                "password": "password",
            }
        )
        content_type_id = ContentType.objects.get_for_model(self.articolo.__class__).pk
        url = reverse(
            "locks:apiv1:check-lock",
            kwargs={"content_type_id": content_type_id, "object_id": self.articolo.pk},
        )
        # user1 calls api
        res = req.get(url)
        assert not res.data
        # acquire lock for user1
        acquire_lock(self.user1.pk, content_type_id, self.articolo.pk)
        res = req.get(url)
        assert not res.data
        # user1 logout
        req.logout()
        # user2 login
        req.login(
            **{
                "username": "test2",
                "password": "password",
            }
        )
        # user2 calls api
        res = req.get(url)
        assert res.data.get("lock")


class ApiSetLockUnitTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_superuser(
            **{
                "username": "test1",
                "password": "password",
            }
        )
        self.user2 = get_user_model().objects.create_superuser(
            **{
                "username": "test2",
                "password": "password",
            }
        )
        self.dipartimento = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{
                "dip_id": 1,
            }
        )
        self.cds = DidatticaCdsUnitTest.create_didatticaCds(
            **{
                "dip": self.dipartimento,
                "tipo_corso_cod": "L",
                "area_cds": "scienze",
                "cds_id": 1,
            }
        )
        self.tipo_corso = DidatticaCdsTipoCorso.objects.create(
            **{
                "tipo_corso_cod": "L",
                "tipo_corso_des": "Laurea",
                "note": "",
                "dt_mod": "2024-01-01",
                "user_mod": self.user1,
            }
        )
        self.titolo = DidatticaArticoliRegolamentoTitolo.objects.create(
            **{
                "descr_titolo_it": "Titolo I",
                "ordine": 0,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.struttura_articolo = DidatticaArticoliRegolamentoStruttura.objects.create(
            **{
                "aa": "2024",
                "titolo_it": "Test titolo articolo",
                "numero": 1,
                "visibile": 1,
                "id_didattica_cds_tipo_corso": self.tipo_corso,
                "id_didattica_articoli_regolamento_titolo": self.titolo,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.regolamento_status = DidatticaArticoliRegolamentoStatus.objects.create(
            **{
                "status_cod": "0",
                "status_desc": "In bozza",
            }
        )
        self.testata = DidatticaCdsArticoliRegolamentoTestata.objects.create(
            **{
                "cds_id": self.cds.pk,
                "aa": "2024",
                "note": "",
                "visibile": 1,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.testata_status = DidatticaCdsTestataStatus.objects.create(
            **{
                "id_didattica_articoli_regolamento_status": self.regolamento_status,
                "id_didattica_cds_articoli_regolamento_testata": self.testata,
                "data_status": "2024-01-01",
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )
        self.articolo = DidatticaCdsArticoliRegolamento.objects.create(
            **{
                "id_didattica_cds_articoli_regolamento_testata": self.testata,
                "id_didattica_articoli_regolamento_struttura": self.struttura_articolo,
                "testo_it": "Test testo articolo",
                "visibile": 1,
                "dt_mod": "2024-01-01",
                "id_user_mod": self.user1,
            }
        )

    def test_apisetlock(self):
        req = Client()
        content_type_id = ContentType.objects.get_for_model(self.articolo.__class__).pk
        url = reverse("locks:apiv1:set-lock")
        # user1 login
        req.login(
            **{
                "username": "test1",
                "password": "password",
            }
        )
        # user1 calls api
        data = {"content_type_id": content_type_id, "object_id": self.articolo.pk}
        res = req.post(url, data)
        assert res.status_code == 200
        # user1 logout
        req.logout()
        # user2 login
        req.login(
            **{
                "username": "test2",
                "password": "password",
            }
        )
        # user2 calls api
        res = req.post(url, data)
        assert res.data.get("lock")
