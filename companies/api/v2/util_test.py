from django.test import TestCase
from addressbook.models import Personale
from companies.models import (
    SpinoffStartupDatiBase,
    SpinoffStartupDipartimento,
    TipologiaAreaTecnologica,
)
from structures.models import DidatticaDipartimento 

class ApiCompaniesUnitTestMethods(TestCase):
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
    def create_tipologiaAreaTecnologica(cls, **kwargs):
        data = {
                "id": 1,
                "descr_area_ita": "aaa",
                "descr_area_eng": "aaa",
            }
        data.update(kwargs)
        return TipologiaAreaTecnologica.objects.create(**data)
    
    
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            "dip_id": 1,
            "dip_cod": 111,
            "dip_des_it": "Informatica",
            "dip_des_eng": "math and computer science",
        }
        data.update(kwargs)
        return DidatticaDipartimento.objects.create(**data)
    
    
    @classmethod
    def create_spinoffStartupDatiBase(cls, **kwargs):
        data = {
                "id": 1,
                "piva": "1111sc",
                "nome_azienda": "Revelis",
                "nome_file_logo": "aaaa",
                "url_sito_web": "bbbb",
                "descrizione_ita": "applicazione",
                "descrizione_eng": "description",
                "referente_unical": "Garofalo",
                "is_spinoff": 1,
                "is_startup": 0,
            }
        data.update(kwargs)
        return SpinoffStartupDatiBase.objects.create(**data)
    
    @classmethod
    def create_spinoffStartupDipartimento(cls, **kwargs):
        data = {
                
            }
        data.update(kwargs)
        return SpinoffStartupDipartimento.objects.create(**data)