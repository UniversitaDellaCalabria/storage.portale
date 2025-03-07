from django.test import TestCase
from cds.models import (
    DidatticaCds,
)
from cds_brochure.models import (
    CdsBrochure,
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider
)


class ApiCdsBrochureUnitTestMethods(TestCase):
    @classmethod
    def create_didatticaCds(cls, **kwargs):
        data = {
            "cds_id": 1,
            "cds_cod": "aaa",
            "nome_cds_it": "Matematica",
            "nome_cds_eng": "Math",
        }
        data.update(kwargs)
        return DidatticaCds.objects.create(**data)


    @classmethod
    def create_cdsBrochure(cls, **kwargs):
        data = {
            "id": 1,
            "aa": "2022",
            # 'nome_corso_it': 'Informatica',
            # 'nome_corso_en': 'Computer Science',
            # 'lingua_it': 'italiano',
            # 'lingua_en': "italian",
            # 'classe_laurea_it': 'aaa',
            # 'durata': 50,
            "num_posti": 50,
        }
        data.update(kwargs)
        return CdsBrochure.objects.create(**data)
    
    
    @classmethod
    def create_cdsBrochureExStudenti(cls, **kwargs):
        data = {
            "id": 111,
            "ordine": 1,
            "profilo_it": "aaa",
            "profilo_en": "aaa",
            "link_it": "aaa",
            "link_en": "aaa",
        }
        data.update(kwargs)
        return CdsBrochureExStudenti.objects.create(**data)
    
    @classmethod
    def create_cdsBrochureLink(cls, **kwargs):
        data = {
            "id": 111111,
            "ordine": 1,
            "descrizione_link_it": "aaa",
            "descrizione_link_en": "aaa",
            "link_it": "aaa",
            "link_en": "aaa",
        }
        data.update(kwargs)
        return CdsBrochureLink.objects.create(**data)
    
    
    @classmethod
    def create_cdsBrochureSlider(cls, **kwargs):
        data = {
            "id": 123,
            "ordine": 1,
            "slider_it": "aaa",
            "slider_en": "aaa",
        }
        data.update(kwargs)
        return CdsBrochureSlider.objects.create(**data)