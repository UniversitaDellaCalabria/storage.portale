from django.test import TestCase
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
from structures.models import DidatticaDipartimento


class ApiAdvancedTrainingUnitTestMethods(TestCase):
    @classmethod
    def create_altaFormazioneModalitaErogazione(cls, **kwargs):
        data = {"id": 1, "descrizione": "AAAA"}
        data.update(kwargs)
        return AltaFormazioneModalitaErogazione.objects.create(**data)

    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": "1",
            "dip_des_it": "matematica e informatica",
            "dip_des_eng": "math and computer science",
        }
        data.update(kwargs)
        return DidatticaDipartimento.objects.create(**data)

    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Franco",
            "cognome": "Garofalo",
            "cd_ruolo": "PO",
            "id_ab": 1,
            "matricola": "111111",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_altaFormazioneTipoCorso(cls, **kwargs):
        data = {"id": 3, "tipo_corso_descr": "AAAA"}
        data.update(kwargs)
        return AltaFormazioneTipoCorso.objects.create(**data)

    @classmethod
    def create_altaFormazioneDatiBase(cls, **kwargs):
        data = {
            "id": 1,
            "titolo_it": "AAAA",
            "titolo_en": "AAAA",
            "lingua": "ita",
            "anno_rilevazione": 2021,
        }
        data.update(kwargs)
        return AltaFormazioneDatiBase.objects.create(**data)

    @classmethod
    def create_altaFormazioneConsiglioScientificoEsterno(cls, **kwargs):
        data = {
            "nome_cons": "Simone",
            "ruolo_cons": "docente",
            "ente_cons": "università",
        }
        data.update(kwargs)
        return AltaFormazioneConsiglioScientificoEsterno.objects.create(**data)

    @classmethod
    def create_altaFormazioneConsiglioScientificoInterno(cls, **kwargs):
        data = {
            "nome_origine_cons": "Simone",
        }
        data.update(kwargs)
        return AltaFormazioneConsiglioScientificoInterno.objects.create(**data)

    @classmethod
    def create_altaFormazionePartner(cls, **kwargs):
        data = {
            "denominazione": "aaaa",
            "tipologia": "bbbb",
            "sito_web": "aaaa",
        }
        data.update(kwargs)
        return AltaFormazionePartner.objects.create(**data)

    @classmethod
    def create_altaFormazioneModalitaSelezione(cls, **kwargs):
        data = {
            "tipo_selezione": "chiusa",
        }
        data.update(kwargs)
        return AltaFormazioneModalitaSelezione.objects.create(**data)

    @classmethod
    def create_altaFormazioneIncaricoDidattico(cls, **kwargs):
        data = {
            "id": 1,
            "modulo": "AAA",
            "qualifica": "SSF",
            "num_ore": 13,
            "ente": "Università",
            "tipologia": "Prova",
            "docente": "Mungari",
        }
        data.update(kwargs)
        return AltaFormazioneIncaricoDidattico.objects.create(**data)

    @classmethod
    def create_altaFormazionePianoDidattico(cls, **kwargs):
        data = {
            "id": 1,
            "modulo": "AAA",
            "ssd": "SSF",
            "num_ore": 13,
            "cfu": 2,
            "verifica_finale": 1,
        }
        data.update(kwargs)
        return AltaFormazionePianoDidattico.objects.create(**data)
