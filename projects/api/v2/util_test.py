from django.test import TestCase
from addressbook.models import Personale
from structures.models import UnitaOrganizzativa
from companies.models import TipologiaAreaTecnologica
from projects.models import (
    ProgettoAmbitoTerritoriale,
    ProgettoDatiBase,
    ProgettoResponsabileScientifico,
    ProgettoRicercatore,
    ProgettoTipologiaProgramma,
)

class ApiProjectsUnitTestMethods(TestCase):
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
    def create_unitaOrganizzativa(cls, **kwargs):
        data = {
                "uo": "1",
                "ds_tipo_nodo": "facolta",
                "cd_tipo_nodo": "000",
                "id_ab": 1,
                "denominazione": "aaa",
                "denominazione_padre": "c",
                "uo_padre": "11",
                "cd_csa": 1,
            }
        data.update(kwargs)
        return UnitaOrganizzativa.objects.create(**data)
    
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
    def create_progettoAmbitoTerritoriale(cls, **kwargs):
        data = {
                "id": 1,
                "ambito_territoriale": "europeo",
            }
        data.update(kwargs)
        return ProgettoAmbitoTerritoriale.objects.create(**data)
    
    @classmethod
    def create_progettoTipologiaProgramma(cls, **kwargs):
        data = {
                "id": 1, 
                "nome_programma": "AAA"
            }
        data.update(kwargs)
        return ProgettoTipologiaProgramma.objects.create(**data)
    
    @classmethod
    def create_progettoDatiBase(cls, **kwargs):
        data = {
                "id": 1,
                "titolo": "Motore",
                "descr_breve": "Mot",
                "abstract_ita": "Motore",
                "abstract_eng": "Engine",
                "anno_avvio": 2021,
            }
        data.update(kwargs)
        return ProgettoDatiBase.objects.create(**data)
    
    @classmethod
    def create_progettoResponsabileScientifico(cls, **kwargs):
        data = {
                "nome_origine": "Simone",
            }
        data.update(kwargs)
        return ProgettoResponsabileScientifico.objects.create(**data)
    
    @classmethod
    def create_progettoRicercatore(cls, **kwargs):
        data = {
                "nome_origine": "Simone",
            }
        data.update(kwargs)
        return ProgettoRicercatore.objects.create(**data)
    