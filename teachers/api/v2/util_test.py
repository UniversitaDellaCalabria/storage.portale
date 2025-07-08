from django.test import TestCase
from addressbook.models import Personale, PersonaleContatti, PersonaleUoTipoContatto
from structures.models import UnitaOrganizzativa, UnitaOrganizzativaFunzioni
from structures.models import (
    DidatticaDipartimento,
)
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaRegolamento,
    DidatticaCopertura,
)
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
from teachers.models import (
    DocenteMaterialeDidattico,
    DocentePtaAltriDati,
    DocentePtaBacheca,
    PubblicazioneAutori,
    PubblicazioneCollection,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)


class ApiTeachersUnitTestMethods(TestCase):
    @classmethod
    def create_unitaOrganizzativa(cls, **kwargs):
        data = {
            "uo": "1",
            "ds_tipo_nodo": "facolta",
            "cd_tipo_nodo": "000",
            "id_ab": 1,
            "denominazione": "aaa",
            "denominazione_padre": "c",
            "uo_padre": "11",
        }
        data.update(kwargs)
        return UnitaOrganizzativa.objects.create(**data)

    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "nome": "Simone",
            "cognome": "Mungari",
            "cd_ruolo": "PA",
            "ds_ruolo_locale": "Professore Associato",
            "id_ab": 1,
            "fl_docente": 1,
            "flg_cessato": 0,
            "ds_aff_org": "aaaa",
            "cod_fis": "SMN1",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_docentePtaBacheca(cls, **kwargs):
        data = {
            "id": 1,
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
        data.update(kwargs)
        return DocentePtaBacheca.objects.create(**data)

    @classmethod
    def create_docenteMaterialeDidattico(cls, **kwargs):
        data = {
            "id": 1,
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
        data.update(kwargs)
        return DocenteMaterialeDidattico.objects.create(**data)

    @classmethod
    def create_pubblicazioneCommunity(cls, **kwargs):
        data = {
            "community_id": 1,
            "community_name": "Community 1",
        }
        data.update(kwargs)
        return PubblicazioneCommunity.objects.create(**data)

    @classmethod
    def create_pubblicazioneCollection(cls, **kwargs):
        data = {
            "collection_id": 1,
            "community_id": 1,
            "collection_name": "Collection 1",
        }
        data.update(kwargs)
        return PubblicazioneCollection.objects.create(**data)

    @classmethod
    def create_pubblicazioneDatiBase(cls, **kwargs):
        data = {
            "title": "pub1",
            "des_abstract": "abstract italiano",
            "des_abstracteng": "abstract inglese",
            "date_issued_year": 2020,
            "pubblicazione": "Giornale 1",
            "label_pubblicazione": "Rivista",
            "collection_id": 1,
            "url_pubblicazione": "aaa",
        }
        data.update(kwargs)
        return PubblicazioneDatiBase.objects.create(**data)

    @classmethod
    def create_pubblicazioneAutori(cls, **kwargs):
        data = {
        }
        data.update(kwargs)
        return PubblicazioneAutori.objects.create(**data)

    # @classmethod
    # def create_didatticaDipartimento(cls, **kwargs):
    #     data = {
    #         "dip_id": 1,
    #         "dip_cod": 1,
    #         "dip_des_it": "Matematica e Informatica",
    #         "dip_des_eng": "Math and Computer Science",
    #     }
    #     data.update(kwargs)
    #     return DidatticaDipartimento.objects.create(**data)

    # @classmethod
    # def create_didatticaRegolamento(cls, **kwargs):
    #     data = {
    #         "regdid_id": 1,
    #         "aa_reg_did": 2020,
    #         "frequenza_obbligatoria": 0,
    #         "titolo_congiunto_cod": "N",
    #     }
    #     data.update(kwargs)
    #     return DidatticaRegolamento.objects.create(**data)

    # @classmethod
    # def create_didatticaAttivitaFormativa(cls, **kwargs):
    #     data = {
    #         "af_id": "1", "anno_corso": 1
    #     }
    #     data.update(kwargs)
    #     return DidatticaAttivitaFormativa.objects.create(**data)

    # @classmethod
    # def create_didatticaCopertura(cls, **kwargs):
    #     data = {}
    #     data.update(kwargs)
    #     return DidatticaCopertura.objects.create(**data)

    # @classmethod
    # def create_ricercaErc0(cls, **kwargs):
    #     data = {
    #         "erc0_cod": "111",
    #         "description": "IT",
    #     }
    #     data.update(kwargs)
    #     return RicercaErc0.objects.create(**data)

    # @classmethod
    # def create_ricercaErc1(cls, **kwargs):
    #     data = {
    #         "cod_erc1": "cod1_erc1",
    #         "descrizione": "Computer Science and Informatics",
    #     }
    #     data.update(kwargs)
    #     return RicercaErc1.objects.create(**data)

    # @classmethod
    # def create_ricercaErc2(cls, **kwargs):
    #     data = {
    #         "cod_erc2": "cod1_erc2",
    #         "descrizione": "Machine learning",
    #     }
    #     data.update(kwargs)
    #     return RicercaErc2.objects.create(**data)

    # @classmethod
    # def create_ricercaLineaBase(cls, **kwargs):
    #     data = {
    #         "id": 1,
    #         "descrizione": "regressione lineare",
    #         "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
    #         "visibile": 1,
    #     }
    #     data.update(kwargs)
    #     return RicercaLineaBase.objects.create(**data)

    # @classmethod
    # def create_ricercaDocenteLineaBase(cls, **kwargs):
    #     data = {
    #         "dt_fine": "2021-01-03",
    #     }
    #     data.update(kwargs)
    #     return RicercaDocenteLineaBase.objects.create(**data)

    # @classmethod
    # def create_ricercaAster1(cls, **kwargs):
    #     data = {
    #         "id": 1,
    #         "descrizione": "ICT & Design",
    #     }
    #     data.update(kwargs)
    #     return RicercaAster1.objects.create(**data)

    # @classmethod
    # def create_ricercaAster2(cls, **kwargs):
    #     data = {
    #         "id": 2,
    #         "descrizione": "Algorithms. Data and signal processing",
    #     }
    #     data.update(kwargs)
    #     return RicercaAster2.objects.create(**data)

    # @classmethod
    # def create_ricercaLineaApplicata(cls, **kwargs):
    #     data = {
    #         "id": 1,
    #         "descrizione": "regressione lineare",
    #         "descr_pubblicaz_prog_brevetto": "pubblicazione 2020",
    #         "visibile": 1,
    #     }
    #     data.update(kwargs)
    #     return RicercaLineaApplicata.objects.create(**data)

    # @classmethod
    # def create_ricercaDocenteLineaApplicata(cls, **kwargs):
    #     data = {
    #         "dt_ins": "2021-01-03 15:47:21",
    #     }
    #     data.update(kwargs)
    #     return RicercaDocenteLineaApplicata.objects.create(**data)
