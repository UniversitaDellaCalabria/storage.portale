from addressbook.models import Personale
from advanced_training.models import (
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazioneDatiBase,
    AltaFormazioneIncaricoDidattico,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneModalitaSelezione,
    AltaFormazionePartner,
    AltaFormazionePianoDidattico,
    AltaFormazioneTipoCorso,
)
from django.test import Client, TestCase
from django.urls import reverse
from structures.api.v1.util_tests import DidatticaDipartimentoUnitTest


class ApiErogationModesListUnitTest(TestCase):
    def test_apierogationmodeslist(self):
        req = Client()

        AltaFormazioneModalitaErogazione.objects.create(
            **{"id": 1, "descrizione": "AAAA"}
        )

        url = reverse("advanced-training:apiv1:erogation-modes")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1


class ApiHighFormationMastersListUnitTest(TestCase):
    def test_apihighformationmasterslist(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{"dip_id": 1, "dip_cod": "1111", "dip_des_it": "Informatica"}
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
                "ds_aff_org": "aaaa",
            }
        )

        aftc = AltaFormazioneTipoCorso.objects.create(
            **{"id": 3, "tipo_corso_descr": "AAAA"}
        )

        afme = AltaFormazioneModalitaErogazione.objects.create(
            **{"id": 3, "descrizione": "AAAA"}
        )

        a1 = AltaFormazioneDatiBase.objects.create(
            **{
                "id": 1,
                "titolo_it": "AAAA",
                "titolo_en": "AAAA",
                "lingua": "ita",
                "matricola_direttore_scientifico": doc1,
                "id_alta_formazione_tipo_corso": aftc,
                "id_alta_formazione_mod_erogazione": afme,
                "id_dipartimento_riferimento": dip,
                "anno_rilevazione": 2021,
            }
        )

        AltaFormazioneDatiBase.objects.create(
            **{
                "id": 2,
                "titolo_it": "AAAA",
                "titolo_en": "AAAA",
                "matricola_direttore_scientifico": doc1,
                "id_alta_formazione_tipo_corso": aftc,
                "id_alta_formazione_mod_erogazione": afme,
            }
        )

        AltaFormazioneConsiglioScientificoEsterno.objects.create(
            **{
                "nome_cons": "Simone",
                "ruolo_cons": "docente",
                "ente_cons": "università",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazioneConsiglioScientificoInterno.objects.create(
            **{
                "nome_origine_cons": "Simone",
                "matricola_cons": doc1,
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazionePartner.objects.create(
            **{
                "denominazione": "aaaa",
                "tipologia": "bbbb",
                "sito_web": "aaaa",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazioneModalitaSelezione.objects.create(
            **{"tipo_selezione": "chiusa", "id_alta_formazione_dati_base": a1}
        )

        AltaFormazioneIncaricoDidattico.objects.create(
            **{
                "id": 1,
                "modulo": "AAA",
                "qualifica": "SSF",
                "num_ore": 13,
                "ente": "Università",
                "tipologia": "Prova",
                "docente": "Mungari",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazionePianoDidattico.objects.create(
            **{
                "id": 1,
                "modulo": "AAA",
                "ssd": "SSF",
                "num_ore": 13,
                "cfu": 2,
                "verifica_finale": 1,
                "id_alta_formazione_dati_base": a1,
            }
        )

        url = reverse("advanced-training:apiv1:high-formation-masters")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 2

        data = {"search": "AAA"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"language": "ita"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"coursetype": "3"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"erogation": "3"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"department": "1111"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1

        data = {"director": "111112"}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 2

        data = {"year": 2021}
        res = req.get(url, data=data)
        assert len(res.json()["results"]) == 1


class ApiHighFormationMasterDetailUnitTest(TestCase):
    def test_apihighformationmasterdetail(self):
        req = Client()

        dip = DidatticaDipartimentoUnitTest.create_didatticaDipartimento(
            **{"dip_id": 1, "dip_cod": "1111", "dip_des_it": "Informatica"}
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
                "ds_aff_org": "aaaa",
            }
        )

        aftc = AltaFormazioneTipoCorso.objects.create(
            **{"id": 3, "tipo_corso_descr": "AAAA"}
        )

        afme = AltaFormazioneModalitaErogazione.objects.create(
            **{"id": 3, "descrizione": "AAAA"}
        )

        a1 = AltaFormazioneDatiBase.objects.create(
            **{
                "id": 1,
                "titolo_it": "AAAA",
                "titolo_en": "AAAA",
                "matricola_direttore_scientifico": doc1,
                "id_alta_formazione_tipo_corso": aftc,
                "id_alta_formazione_mod_erogazione": afme,
                "id_dipartimento_riferimento": dip,
            }
        )

        AltaFormazioneConsiglioScientificoEsterno.objects.create(
            **{
                "nome_cons": "Simone",
                "ruolo_cons": "docente",
                "ente_cons": "università",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazioneConsiglioScientificoInterno.objects.create(
            **{
                "nome_origine_cons": "Simone",
                "matricola_cons": doc1,
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazionePartner.objects.create(
            **{
                "denominazione": "aaaa",
                "tipologia": "bbbb",
                "sito_web": "aaaa",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazioneModalitaSelezione.objects.create(
            **{"tipo_selezione": "chiusa", "id_alta_formazione_dati_base": a1}
        )

        AltaFormazioneIncaricoDidattico.objects.create(
            **{
                "id": 1,
                "modulo": "AAA",
                "qualifica": "SSF",
                "num_ore": 13,
                "ente": "Università",
                "tipologia": "Prova",
                "docente": "Mungari",
                "id_alta_formazione_dati_base": a1,
            }
        )

        AltaFormazionePianoDidattico.objects.create(
            **{
                "id": 1,
                "modulo": "AAA",
                "ssd": "SSF",
                "num_ore": 13,
                "cfu": 2,
                "verifica_finale": 1,
                "id_alta_formazione_dati_base": a1,
            }
        )

        url = reverse("advanced-training:apiv1:high-formation-master-detail", kwargs={"id": 1})

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert res.json()["results"]["ID"] == 1


class ApiHighFormationCourseTypesListUnitTest(TestCase):
    def test_apicoursetypeslist(self):
        req = Client()

        AltaFormazioneTipoCorso.objects.create(**{"id": 1, "tipo_corso_descr": "AAAA"})

        url = reverse("advanced-training:apiv1:high-formation-course-types")

        # check url
        res = req.get(url)

        assert res.status_code == 200

        # GET

        res = req.get(url)
        assert len(res.json()["results"]) == 1
