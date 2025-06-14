from django.test import TestCase, Client
from addressbook.models import Personale
from structures.models import DidatticaDipartimento
from structures.models import UnitaOrganizzativa
from research_lines.models import RicercaErc0, RicercaErc1, RicercaErc2
from laboratories.models import (
    LaboratorioAltriDipartimenti,
    LaboratorioAttivita,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioInfrastruttura,
    LaboratorioPersonaleRicerca,
    LaboratorioPersonaleTecnico,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)


class ApiLaboratoriesUnitTestMethods(TestCase):
    def setUp(self):
        self.client = Client()
        self.personale = self.create_personale()
        self.dipartimento = self.create_didatticaDipartimento()

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
            "nome": "Simone",
            "cognome": "Mungari",
            "cd_ruolo": "responsabile",
            "id_ab": 1,
            "matricola": "111111",
        }
        data.update(kwargs)
        return Personale.objects.create(**data)

    @classmethod
    def create_laboratorioDatiBase(cls, **kwargs):
        data = {
            "id": 1,
            "nome_laboratorio": "Informatica",
            "ambito": "Tecnico",
            "dipartimento_riferimento_nome": "Informatica, demacs",
            "sede_dimensione": "290",
            "responsabile_scientifico": "Mungari Simone",
            "laboratorio_interdipartimentale": "SI",
            "visibile": True,
        }
        data.update(kwargs)
        return LaboratorioDatiBase.objects.create(**data)

    @classmethod
    def create_laboratorioTipologiaAttivita(cls, **kwargs):
        data = {"id": 1, "descrizione": "aaa"}
        data.update(kwargs)
        return LaboratorioTipologiaAttivita.objects.create(**data)

    @classmethod
    def create_laboratorioAttivita(cls, **kwargs):
        data = {
            "id": 1,
        }
        data.update(kwargs)
        return LaboratorioAttivita.objects.create(**data)

    @classmethod
    def create_ricercaErc0(cls, **kwargs):
        data = {
            "erc0_cod": "111",
            "description": "IT",
            "description_en": "IT",
        }
        data.update(kwargs)
        return RicercaErc0.objects.create(**data)

    @classmethod
    def create_ricercaErc1(cls, **kwargs):
        data = {
            "cod_erc1": "cod1_erc1",
            "descrizione": "Computer Science and Informatics",
        }
        data.update(kwargs)
        return RicercaErc1.objects.create(**data)

    @classmethod
    def create_ricercaErc2(cls, **kwargs):
        data = {
            "cod_erc2": "cod_erc2",
            "descrizione": "Sicurezza Informatica",
        }
        data.update(kwargs)
        return RicercaErc2.objects.create(**data)

    @classmethod
    def create_laboratorioInfrastruttura(cls, **kwargs):
        data = {"id": 1, "descrizione": "SILA"}
        data.update(kwargs)
        return LaboratorioInfrastruttura.objects.create(**data)

    @classmethod
    def create_laboratorioPersonaleRicerca(cls, **kwargs):
        data = {
            "id": 1,
        }
        data.update(kwargs)
        return LaboratorioPersonaleRicerca.objects.create(**data)

    @classmethod
    def create_laboratorioPersonaleTecnico(cls, **kwargs):
        data = {
            "id": 1,
            "ruolo": "R1",
        }
        data.update(kwargs)
        return LaboratorioPersonaleTecnico.objects.create(**data)

    @classmethod
    def create_laboratorioDatiErc1(cls, **kwargs):
        data = {
            "id": 3,
        }
        data.update(kwargs)
        return LaboratorioDatiErc1.objects.create(**data)

    @classmethod
    def create_laboratorioAltriDipartimenti(cls, **kwargs):
        data = {
            "id": 1,
        }
        data.update(kwargs)
        return LaboratorioAltriDipartimenti.objects.create(**data)

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
    def create_laboratorioServiziOfferti(cls, **kwargs):
        data = {"id": 1, "nome_servizio": "S1"}
        data.update(kwargs)
        return LaboratorioServiziOfferti.objects.create(**data)

    @classmethod
    def create_laboratorioUbicazione(cls, **kwargs):
        data = {
            "id": 1,
            "edificio": "31B",
            "piano": "1",
        }
        data.update(kwargs)
        return LaboratorioUbicazione.objects.create(**data)
