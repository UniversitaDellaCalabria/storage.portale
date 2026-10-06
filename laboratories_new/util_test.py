from addressbook.models import Personale
from structures.models import DidatticaDipartimento, UnitaOrganizzativa
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from laboratories_new.models import (
    AmbitiS3,
    LaboratorioAffiliati,
    LaboratorioAnagraficaServizi,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioDipartimenti,
    LaboratorioInfrastruttura,
    LaboratorioResponsabile,
    LaboratorioRuolo,
    LaboratorioServizi,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)


def _create(model, defaults, kwargs):
    data = dict(defaults)
    data.update(kwargs)
    return model.objects.create(**data)


class ApiLaboratoriesUnitTestMethods:
    """Factory di dati di test (solo classmethod, nessun TestCase)."""

    # ---------- anagrafiche esterne (invariate) ----------
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        return _create(
            DidatticaDipartimento,
            {
                "dip_id": 1,
                "dip_cod": "1",
                "dip_des_it": "matematica e informatica",
                "dip_des_eng": "math and computer science",
            },
            kwargs,
        )

    @classmethod
    def create_personale(cls, **kwargs):
        return _create(
            Personale,
            {
                "id": 1,
                "nome": "Simone",
                "cognome": "Mungari",
                "cd_ruolo": "responsabile",
                "id_ab": 1,
                "matricola": "111111",
                "cod_fis": "CF1",
            },
            kwargs,
        )

    @classmethod
    def create_unitaOrganizzativa(cls, **kwargs):
        return _create(
            UnitaOrganizzativa,
            {
                "uo": "1",
                "ds_tipo_nodo": "facolta",
                "cd_tipo_nodo": "000",
                "id_ab": 1,
                "denominazione": "aaa",
                "denominazione_padre": "c",
                "uo_padre": "11",
            },
            kwargs,
        )

    # ---------- ERC / ASTER (invariati) ----------
    @classmethod
    def create_ricercaErc0(cls, **kwargs):
        return _create(
            RicercaErc0,
            {"erc0_cod": "111", "description": "IT", "description_en": "IT"},
            kwargs,
        )

    @classmethod
    def create_ricercaErc1(cls, **kwargs):
        return _create(
            RicercaErc1,
            {
                "cod_erc1": "cod1_erc1",
                "descrizione": "Computer Science and Informatics",
            },
            kwargs,
        )

    @classmethod
    def create_ricercaErc2(cls, **kwargs):
        return _create(
            RicercaErc2,
            {"cod_erc2": "cod_erc2", "descrizione": "Sicurezza Informatica"},
            kwargs,
        )

    @classmethod
    def create_ricercaAster1(cls, **kwargs):
        return _create(RicercaAster1, {"descrizione": "Aster1"}, kwargs)

    @classmethod
    def create_ricercaAster2(cls, **kwargs):
        return _create(RicercaAster2, {"descrizione": "Aster2"}, kwargs)

    # ---------- laboratories_new ----------
    @classmethod
    def create_ambitoS3(cls, **kwargs):
        return _create(
            AmbitiS3,
            {
                "codice": "T",
                "denominazione_it": "Tecnologico",
                "denominazione_en": "Technological",
            },
            kwargs,
        )

    @classmethod
    def create_laboratorioInfrastruttura(cls, **kwargs):
        return _create(
            LaboratorioInfrastruttura,
            {
                "nome": "SILA",
                "descrizione_it": "SILA",
                "descrizione_en": "SILA en",
            },
            kwargs,
        )

    @classmethod
    def create_laboratorioTipologiaAttivita(cls, **kwargs):
        return _create(
            LaboratorioTipologiaAttivita,
            {"descrizione_it": "aaa", "descrizione_en": "aaa en"},
            kwargs,
        )

    @classmethod
    def create_laboratorioDatiBase(cls, **kwargs):
        return _create(
            LaboratorioDatiBase,
            {"nome_laboratorio": "Informatica", "acronimo": "INF", "visibile": True},
            kwargs,
        )

    @classmethod
    def create_laboratorioRuolo(cls, **kwargs):
        return _create(
            LaboratorioRuolo,
            {"descr_ruolo_it": "Ricercatore", "descr_ruolo_en": "Researcher"},
            kwargs,
        )

    @classmethod
    def create_laboratorioRuoloTecnico(cls, **kwargs):
        data = {"descr_ruolo_it": "Tecnico", "descr_ruolo_en": "Technician"}
        data.update(kwargs)
        return LaboratorioRuolo.objects.create(**data)

    @classmethod
    def create_laboratorioResponsabile(cls, **kwargs):
        # obbligatori: laboratorio_dati_base, matricola_personale
        return _create(LaboratorioResponsabile, {}, kwargs)

    @classmethod
    def create_laboratorioAffiliati(cls, **kwargs):
        # obbligatori: laboratorio_dati_base, matricola_personale, laboratorio_ruolo
        return _create(LaboratorioAffiliati, {}, kwargs)

    @classmethod
    def create_laboratorioDipartimenti(cls, **kwargs):
        # obbligatori: laboratorio_dati_base, didattica_dipartimento
        return _create(LaboratorioDipartimenti, {"principale": True}, kwargs)

    @classmethod
    def create_laboratorioAnagraficaServizi(cls, **kwargs):
        return _create(
            LaboratorioAnagraficaServizi,
            {
                "nome_servizio_it": "S1",
                "nome_servizio_en": "S1 en",
                "descrizione_servizio_it": "Descrizione anagrafica",
            },
            kwargs,
        )

    @classmethod
    def create_laboratorioServizi(cls, **kwargs):
        # obbligatori: laboratorio_dati_base, laboratorio_anagrafica_servizi
        return _create(LaboratorioServizi, {}, kwargs)

    @classmethod
    def create_laboratorioUbicazione(cls, **kwargs):
        return _create(
            LaboratorioUbicazione,
            {"edificio": "31B", "piano": "1", "superficie_mq": 100},
            kwargs,
        )

    @classmethod
    def create_laboratorioDatiErc1(cls, **kwargs):
        # obbligatori: laboratorio_dati_base, ricerca_erc1
        return _create(LaboratorioDatiErc1, {}, kwargs)
