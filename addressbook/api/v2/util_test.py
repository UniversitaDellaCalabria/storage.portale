from django.test import TestCase
from addressbook.models import (
    Personale,
    PersonaleAttivoTuttiRuoli,
    PersonaleContatti,
    PersonalePrioritaRuolo,
    PersonaleUoTipoContatto,
)
from structures.models import DidatticaDipartimento
from structures.models import (
    UnitaOrganizzativa,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaContatti
)

class ApiAddressBookUnitTestMethods(TestCase):
    @classmethod
    def create_personale(cls, **kwargs):
        data = {
            "id": 1,
            "nome": "Simone",
            "cognome": "Mungari",
            "cd_ruolo": "PA",
            "ds_ruolo_locale": "Professore Associato",
            "id_ab": 1,
            "matricola": "111112",
            "fl_docente": 1,
            "flg_cessato": 0,
            "cod_fis": "SMN1",
            "cv_full_it": "AAA",
            "cv_short_it": "A",
            "cv_full_eng": "BBB",
            "cv_short_eng": "B",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_unitaOrganizzativa(cls, **kwargs):
        data = {
            "uo": "2",
            "uo_padre": "1",
            "cd_tipo_nodo": "DRZ",
            "ds_tipo_nodo": "Direzione",
            "dt_fine_val": "2222-01-01",
        }
        data.update(kwargs)
        return UnitaOrganizzativa.objects.create(**data)

    @classmethod
    def create_personaleAttivoTuttiRuoli(cls, **kwargs):
        data = {
            "cd_ruolo": "PO",
            "ds_ruolo": "Professore Ordinario",
            "ds_aff_org": "Direzione",
        }
        data.update(kwargs)
        return PersonaleAttivoTuttiRuoli.objects.create(**data)

    @classmethod
    def create_personalePrioritaRuolo(cls, **kwargs):
        data = {
            "cd_ruolo": "PO",
            "priorita": 1,
        }
        data.update(kwargs)
        return PersonalePrioritaRuolo.objects.create(**data)

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
    def create_personaleUoTipoContatto(cls, **kwargs):
        data = {
            "descr_contatto": "Posta Elettronica",
        }
        data.update(kwargs)
        return PersonaleUoTipoContatto.objects.create(**data)
    
    @classmethod
    def create_personaleContatti(cls, **kwargs):
        data = {
            "id_ab": 1,
            "contatto": "email@email",
            "prg_priorita": 1,
        }
        data.update(kwargs)
        return PersonaleContatti.objects.create(**data)
    
    @classmethod
    def create_unitaOrganizzativaFunzioni(cls, **kwargs):
        data = {
            "id_ab": 2,
            "ds_funzione": "Amministrazione Rettorato",
        }
        data.update(kwargs)
        return UnitaOrganizzativaFunzioni.objects.create(**data)
    
    @classmethod
    def create_unitaOrganizzativaContatti(cls, **kwargs):
        data = {
            "prg_priorita": 2,
        }
        data.update(kwargs)
        return UnitaOrganizzativaContatti.objects.create(**data)
    
    classmethod
    def create_didatticaCopertura(cls, **kwargs):
        data = {
            "personale_id": 1, 
            "cds_cod": "1", 
            "aa_off_id": 2021
        }
        data.update(kwargs)
        return UnitaOrganizzativaContatti.objects.create(**data)
    