from django.test import TestCase

from .models import (
    DidatticaCds,
    DidatticaCdsLingua,
    DidatticaRegolamento,
    DidatticaDipartimento,
    ComuniAll,
    TerritorioIt,
    DidatticaTestiRegolamento,
    DidatticaAttivitaFormativa,
    DidatticaPdsRegolamento,
    DidatticaTestiAf,
    Personale,
    DidatticaCopertura,
    RicercaDocenteGruppo,
    RicercaGruppo,
    RicercaDocenteLineaApplicata,
    RicercaLineaApplicata,
    RicercaAster2,
    RicercaAster1,
    RicercaDocenteLineaBase,
    RicercaLineaBase,
    RicercaErc2,
    RicercaErc1,
    RicercaErc0,
    DidatticaDottoratoCds,
    DidatticaDottoratoPds,
    DidatticaDottoratoRegolamento,
    PersonaleContatti,
    PersonaleUoTipoContatto,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativa,
    UnitaOrganizzativaContatti,
    LaboratorioAttivita,
    LaboratorioUbicazione,
    LaboratorioServiziOfferti,
    LaboratorioPersonaleTecnico,
    LaboratorioPersonaleRicerca,
    LaboratorioDatiErc1,
    LaboratorioDatiBase,
    LaboratorioAltriDipartimenti,
    PubblicazioneAutori,
    PubblicazioneDatiBase,
    PubblicazioneCommunity,
    PubblicazioneCollection,
    LaboratorioInfrastruttura,
    LaboratorioTipologiaAttivita,
    BrevettoDatiBase,
    BrevettoInventori,
    TipologiaAreaTecnologica,
    SpinoffStartupDatiBase,
    ProgettoDatiBase,
    ProgettoTipologiaProgramma,
    ProgettoAmbitoTerritoriale,
    ProgettoResponsabileScientifico,
    UnitaOrganizzativaTipoFunzioni,
    ProgettoRicercatore,
    AltaFormazioneDatiBase,
    AltaFormazioneModalitaErogazione,
    AltaFormazioneModalitaSelezione,
    AltaFormazioneConsiglioScientificoEsterno,
    AltaFormazioneConsiglioScientificoInterno,
    AltaFormazionePartner,
    AltaFormazioneIncaricoDidattico,
    AltaFormazionePianoDidattico,
    AltaFormazioneTipoCorso,
    DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio,
    DidatticaAttivitaFormativaModalita,
    DidatticaCoperturaDettaglioOre,
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaDocente,
    DidatticaDottoratoAttivitaFormativaAltriDocenti,
    SpinoffStartupDipartimento,
    PersonaleAttivoTuttiRuoli,
    PersonalePrioritaRuolo,
    DocentePtaBacheca,
    DocentePtaAltriDati,
    DocenteMaterialeDidattico,
    SitoWebCdsDatiBase,
    SitoWebCdsSlider,
    SitoWebCdsLink,
    SitoWebCdsExStudenti,
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliReg,
    SitoWebCdsArticoliRegolamento,
    # SitoWebCdsArticoliRegAltriDati,
    # SitoWebCdsOggettiPortaleAltriDati,
    SitoWebCdsTopicArticoliRegAltriDati,
    SitoWebCdsOggettiPortale,
    DidatticaPianoRegolamento,
    DidatticaPianoSche,
    DidatticaPianoSceltaSchePiano,
    DidatticaPianoSceltaVincoli,
    DidatticaAmbiti,
    DidatticaPianoSceltaAf,
    DidatticaArticoliRegolamentoStatus,
    DidatticaCdsTipoCorso,
    DidatticaArticoliRegolamentoStruttura,
    DidatticaCdsArticoliRegolamentoTestata,
    DidatticaArticoliRegolamentoStrutturaTopic,
    DidatticaCdsArticoliRegolamento,
    DidatticaArticoliRegolamentoTitolo,
    DidatticaCdsSubArticoliRegolamento
)


# class ContextUnitTest(TestCase):
#     @classmethod
#     def create_user(cls, **kwargs):
#         data = {'username': 'foo',
#                 'first_name': 'foo',
#                 'last_name': 'bar',
#                 'email': 'that@mail.org'}
#         for k, v in kwargs.items():
#             data[k] = v
#         user = get_user_model().objects.create(**data)
#         return user


class DidatticaCdsUnitTest(TestCase):
    @classmethod
    def create_didatticaCds(cls, **kwargs):
        data = {
            'cds_id': 1,
            'nome_cds_it': 'informatica',
            'nome_cds_eng': 'computer science',
            'tipo_corso_cod': '1',
            'cla_miur_cod': '1',
            'cla_miur_des': 'laurea in informatica',
            'durata_anni': 3,
            'valore_min': 180,
            'cdsord_id': 1,
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCds.objects.create(**data)
        return obj


class DidatticaCdsLinguaUnitTest(TestCase):
    @classmethod
    def create_didatticaCdsLingua(cls, **kwargs):
        data = {
            'lin_did_ord_id': 1,
            'lingua_des_it': 'ITALIANO',
            'lingua_des_eng': 'ITALIAN',
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsLingua.objects.create(**data)
        return obj


class DidatticaRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaRegolamento(cls, **kwargs):
        data = {
            'regdid_id': 1,
            'aa_reg_did': 2020,
            'frequenza_obbligatoria': 0,
            'titolo_congiunto_cod': 'N',
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaRegolamento.objects.create(**data)
        return obj


class DidatticaTestiRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaTestiRegolamento(cls, **kwargs):
        data = {
            'txt_id': 1,
            'tipo_testo_regdid_cod': 'testo regolamento',
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaTestiRegolamento.objects.create(**data)
        return obj


class DidatticaDipartimentoUnitTest(TestCase):
    @classmethod
    def create_didatticaDipartimento(cls, **kwargs):
        data = {
            'dip_id': 1,
            'dip_cod': '1',
            'dip_des_it': 'matematica e informatica',
            'dip_des_eng': 'math and computer science'
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDipartimento.objects.create(**data)
        return obj


class ComuniAllUnitTest(TestCase):
    @classmethod
    def create_comuniAll(cls, **kwargs):
        data = {
            'id_comune': 1,
            'ds_comune': 'comune 1',
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = ComuniAll.objects.create(**data)
        return obj


class TerritorioItUnitTest(TestCase):
    @classmethod
    def create_territorioIt(cls, **kwargs):
        data = {
            'cd_istat': '1',
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = TerritorioIt.objects.create(**data)
        return obj


class DidatticaAttivitaFormativaUnitTest(TestCase):
    @classmethod
    def create_didatticaAttivitaFormativa(cls, **kwargs):
        data = {
            'af_id': '1',
            'anno_corso': 1
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaAttivitaFormativa.objects.create(**data)
        return obj


class DidatticaPdsRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaPdsRegolamento(cls, **kwargs):
        data = {
            # 'aa_ord_id': 1,
            'pds_regdid_id': 1,
        }

        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPdsRegolamento.objects.create(**data)
        return obj


class DidatticaTestiAfUnitTest(TestCase):
    @classmethod
    def create_didatticaTestiAf(cls, **kwargs):
        data = {
            # 'testi_af_id': 1,
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaTestiAf.objects.create(**data)
        return obj


class PersonaleUnitTest(TestCase):
    @classmethod
    def create_personale(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = Personale.objects.create(**data)
        return obj


class DidatticaCoperturaUnitTest(TestCase):
    @classmethod
    def create_didatticaCopertura(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCopertura.objects.create(**data)
        return obj


class RicercaDocenteGruppoUnitTest(TestCase):
    @classmethod
    def create_ricercaDocenteGruppo(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaDocenteGruppo.objects.create(**data)
        return obj


class RicercaGruppoUnitTest(TestCase):
    @classmethod
    def create_ricercaGruppo(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaGruppo.objects.create(**data)
        return obj


class RicercaDocenteLineaApplicataUnitTest(TestCase):
    @classmethod
    def create_ricercaDocenteLineaApplicata(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaDocenteLineaApplicata.objects.create(**data)
        return obj


class RicercaLineaApplicataUnitTest(TestCase):
    @classmethod
    def create_ricercaLineaApplicata(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaLineaApplicata.objects.create(**data)
        return obj


class RicercaAster2UnitTest(TestCase):
    @classmethod
    def create_ricercaAster2(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaAster2.objects.create(**data)
        return obj


class RicercaAster1UnitTest(TestCase):
    @classmethod
    def create_ricercaAster1(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaAster1.objects.create(**data)
        return obj


class RicercaDocenteLineaBaseUnitTest(TestCase):
    @classmethod
    def create_ricercaDocenteLineaBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaDocenteLineaBase.objects.create(**data)
        return obj


class RicercaLineaBaseUnitTest(TestCase):
    @classmethod
    def create_ricercaLineaBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaLineaBase.objects.create(**data)
        return obj


class RicercaErc2UnitTest(TestCase):
    @classmethod
    def create_ricercaErc2(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaErc2.objects.create(**data)
        return obj


class RicercaErc1UnitTest(TestCase):
    @classmethod
    def create_ricercaErc1(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaErc1.objects.create(**data)
        return obj


class RicercaErc0UnitTest(TestCase):
    @classmethod
    def create_ricercaErc0(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = RicercaErc0.objects.create(**data)
        return obj


class DidatticaDottoratoCdsUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoCds(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoCds.objects.create(**data)
        return obj


class DidatticaDottoratoPdsUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoPds(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoPds.objects.create(**data)
        return obj


class DidatticaDottoratoRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoRegolamento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoRegolamento.objects.create(**data)
        return obj


class PersonaleContattiUnitTest(TestCase):
    @classmethod
    def create_personaleContatti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PersonaleContatti.objects.create(**data)
        return obj


class PersonaleUoTipoContattoUnitTest(TestCase):
    @classmethod
    def create_personaleUoTipoContatto(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PersonaleUoTipoContatto.objects.create(**data)
        return obj


class UnitaOrganizzativaFunzioniUnitTest(TestCase):
    @classmethod
    def create_unitaOrganizzativaFunzioni(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = UnitaOrganizzativaFunzioni.objects.create(**data)
        return obj


class UnitaOrganizzativaUnitTest(TestCase):
    @classmethod
    def create_unitaOrganizzativa(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = UnitaOrganizzativa.objects.create(**data)
        return obj


class UnitaOrganizzativaContattiUnitTest(TestCase):
    @classmethod
    def create_unitaOrganizzativaContatti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = UnitaOrganizzativaContatti.objects.create(**data)
        return obj


class LaboratorioAttivitaUnitTest(TestCase):
    @classmethod
    def create_laboratorioAttivita(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioAttivita.objects.create(**data)
        return obj


class LaboratorioDatiBaseUnitTest(TestCase):
    @classmethod
    def create_laboratorioDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioDatiBase.objects.create(**data)
        return obj


class LaboratorioDatiErc1UnitTest(TestCase):
    @classmethod
    def create_laboratorioDatiErc1(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioDatiErc1.objects.create(**data)
        return obj


class LaboratorioPersonaleRicercaUnitTest(TestCase):
    @classmethod
    def create_laboratorioPersonaleRicerca(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioPersonaleRicerca.objects.create(**data)
        return obj


class LaboratorioPersonaleTecnicoUnitTest(TestCase):
    @classmethod
    def create_laboratorioPersonaleTecnico(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioPersonaleTecnico.objects.create(**data)
        return obj


class LaboratorioServiziOffertiUnitTest(TestCase):
    @classmethod
    def create_laboratorioServiziOfferti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioServiziOfferti.objects.create(**data)
        return obj


class LaboratorioUbicazioneUnitTest(TestCase):
    @classmethod
    def create_laboratorioUbicazione(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioUbicazione.objects.create(**data)
        return obj


class LaboratorioAltriDipartimentiUnitTest(TestCase):
    @classmethod
    def create_laboratorioAltriDipartimenti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioAltriDipartimenti.objects.create(**data)
        return obj


class PubblicazioneAutoriUnitTest(TestCase):
    @classmethod
    def create_pubblicazioneAutori(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PubblicazioneAutori.objects.create(**data)
        return obj


class PubblicazioneCollectionUnitTest(TestCase):
    @classmethod
    def create_pubblicazioneCollection(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PubblicazioneCollection.objects.create(**data)
        return obj


class PubblicazioneCommunityUnitTest(TestCase):
    @classmethod
    def create_pubblicazioneCommunity(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PubblicazioneCommunity.objects.create(**data)
        return obj


class PubblicazioneDatiBaseUnitTest(TestCase):
    @classmethod
    def create_pubblicazioneDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PubblicazioneDatiBase.objects.create(**data)
        return obj


class LaboratorioInfrastrutturaUnitTest(TestCase):
    @classmethod
    def create_laboratorioInfrastruttura(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioInfrastruttura.objects.create(**data)
        return obj


class LaboratorioTipologiaAttivitaUnitTest(TestCase):
    @classmethod
    def create_laboratorioTipologiaAttivita(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = LaboratorioTipologiaAttivita.objects.create(**data)
        return obj


class BrevettoDatiBaseUnitTest(TestCase):
    @classmethod
    def create_brevettoDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = BrevettoDatiBase.objects.create(**data)
        return obj


class BrevettoInventoriUnitTest(TestCase):
    @classmethod
    def create_brevettoInventori(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = BrevettoInventori.objects.create(**data)
        return obj


class TipologiaAreaTecnologicaUnitTest(TestCase):
    @classmethod
    def create_tipologiaAreaTecnologica(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = TipologiaAreaTecnologica.objects.create(**data)
        return obj


class SpinoffStartupDatiBaseUnitTest(TestCase):
    @classmethod
    def create_spinoffStartupDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SpinoffStartupDatiBase.objects.create(**data)
        return obj


class ProgettoDatiBaseUnitTest(TestCase):
    @classmethod
    def create_progettoDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = ProgettoDatiBase.objects.create(**data)
        return obj


class ProgettoAmbitoTerritorialeUnitTest(TestCase):
    @classmethod
    def create_progettoAmbitoTerritoriale(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = ProgettoAmbitoTerritoriale.objects.create(**data)
        return obj


class ProgettoTipologiaProgrammaUnitTest(TestCase):
    @classmethod
    def create_progettoTipologiaProgramma(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = ProgettoTipologiaProgramma.objects.create(**data)
        return obj


class ProgettoResponsabileScientificoUnitTest(TestCase):
    @classmethod
    def create_progettoResponsabileScientifico(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = ProgettoResponsabileScientifico.objects.create(**data)
        return obj


class ProgettoRicercatoreUnitTest(TestCase):
    @classmethod
    def create_progettoRicercatore(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = ProgettoRicercatore.objects.create(**data)
        return obj


class UnitaOrganizzativaTipoFunzioniUnitTest(TestCase):
    @classmethod
    def create_unitaOrganizzativaTipoFunzioni(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = UnitaOrganizzativaTipoFunzioni.objects.create(**data)
        return obj


class AltaFormazioneDatiBaseUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneDatiBase.objects.create(**data)
        return obj

class AltaFormazioneTipoCorsoUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneTipoCorso(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneTipoCorso.objects.create(**data)
        return obj


class AltaFormazioneModalitaErogazioneUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneModalitaErogazione(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneModalitaErogazione.objects.create(**data)
        return obj


class AltaFormazioneModalitaSelezioneUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneModalitaSelezione(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneModalitaSelezione.objects.create(**data)
        return obj


class AltaFormazioneConsiglioScientificoEsternoUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneConsiglioScientificoEsterno(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneConsiglioScientificoEsterno.objects.create(**data)
        return obj


class AltaFormazioneConsiglioScientificoInternoUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneConsiglioScientificoInterno(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneConsiglioScientificoInterno.objects.create(**data)
        return obj


class AltaFormazionePartnerUnitTest(TestCase):
    @classmethod
    def create_altaFormazionePartner(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazionePartner.objects.create(**data)
        return obj


class AltaFormazioneIncaricoDidatticoUnitTest(TestCase):
    @classmethod
    def create_altaFormazioneIncaricoDidattico(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazioneIncaricoDidattico.objects.create(**data)
        return obj


class AltaFormazionePianoDidatticoUnitTest(TestCase):
    @classmethod
    def create_altaFormazionePianoDidattico(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = AltaFormazionePianoDidattico.objects.create(**data)
        return obj


class DidatticaCdsAltriDatiUnitTest(TestCase):
    @classmethod
    def create_didatticaCdsAltriDati(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsAltriDati.objects.create(**data)
        return obj


class DidatticaCdsAltriDatiUfficioUnitTest(TestCase):
    @classmethod
    def create_didatticaCdsAltriDatiUfficio(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsAltriDatiUfficio.objects.create(**data)
        return obj


class DidatticaAttivitaFormativaModalitaUnitTest(TestCase):
    @classmethod
    def create_didatticaAttivitaFormativaModalita(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaAttivitaFormativaModalita.objects.create(**data)
        return obj

class DidatticaCoperturaDettaglioOreUnitTest(TestCase):
    @classmethod
    def create_didatticaCoperturaDettaglioOre(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCoperturaDettaglioOre.objects.create(**data)
        return obj


class DidatticaDottoratoAttivitaFormativaUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoAttivitaFormativa(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoAttivitaFormativa.objects.create(**data)
        return obj


class DidatticaDottoratoAttivitaFormativaDocenteUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoAttivitaFormativaDocente(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoAttivitaFormativaDocente.objects.create(**data)
        return obj


class DidatticaDottoratoAttivitaFormativaAltriDocentiUnitTest(TestCase):
    @classmethod
    def create_didatticaDottoratoAttivitaFormativaAltriDocenti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.create(**data)
        return obj


class SpinoffStartupDipartimentoUnitTest(TestCase):
    @classmethod
    def create_spinoffStartupDipartimento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SpinoffStartupDipartimento.objects.create(**data)
        return obj


class PersonaleAttivoTuttiRuoliUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_personaleAttivoTuttiRuoli(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PersonaleAttivoTuttiRuoli.objects.create(**data)
        return obj


class PersonalePrioritaRuoloUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_personalePrioritaRuolo(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PersonalePrioritaRuolo.objects.create(**data)
        return obj


class DocentePtaBachecaUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_docentePtaBacheca(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DocentePtaBacheca.objects.create(**data)
        return obj


class DocentePtaMaterialeDidatticoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_docentePtaMaterialeDidattico(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DocenteMaterialeDidattico.objects.create(**data)
        return obj


class DocentePtaAltriDatiUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_docentePtaAltriDati(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DocentePtaAltriDati.objects.create(**data)
        return obj


class SitoWebCdsDatiBaseUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsDatiBase(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsDatiBase.objects.create(**data)
        return obj


class SitoWebCdsExStudentiUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsExStudenti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsExStudenti.objects.create(**data)
        return obj


class SitoWebCdsSliderUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsSlider(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsSlider.objects.create(**data)
        return obj


class SitoWebCdsLinkUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsLink(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsLink.objects.create(**data)
        return obj


class SitoWebCdsTopicListUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsTopicList(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsTopic.objects.create(**data)
        return obj


class SitoWebCdsTopicArticoliRegUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsTopicArticoliReg(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsTopicArticoliReg.objects.create(**data)
        return obj

class SitoWebCdsOggettiPortaleUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsOggettiPortale(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsOggettiPortale.objects.create(**data)
        return obj


# class SitoWebCdsOggettiPortaleAltriDatiUnitTest(TestCase): # pragma: no cover
    # @classmethod
    # def create_sitoWebCdsOggettiPortaleAltriDati(cls, **kwargs):
        # data = {}
        # for k, v in kwargs.items():
            # data[k] = v

        # obj = SitoWebCdsOggettiPortaleAltriDati.objects.create(**data)
        # return obj


class SitoWebCdsArticoliRegolamentoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsArticoliRegolamento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsArticoliRegolamento.objects.create(**data)
        return obj


# class SitoWebCdsArticoliRegAltriDatiUnitTest(TestCase): # pragma: no cover
    # @classmethod
    # def create_sitoWebCdsArticoliRegAltriDati(cls, **kwargs):
        # data = {}
        # for k, v in kwargs.items():
            # data[k] = v

        # obj = SitoWebCdsArticoliRegAltriDati.objects.create(**data)
        # return obj


class SitoWebCdsTopicArticoliRegAltriDatiUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_sitoWebCdsTopicArticoliRegAltriDati(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = SitoWebCdsTopicArticoliRegAltriDati.objects.create(**data)
        return obj


class DidatticaPianoRegolamentoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaPianoRegolamento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPianoRegolamento.objects.create(**data)
        return obj



class DidatticaPianoScheUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaPianoSche(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPianoSche.objects.create(**data)
        return obj



class DidatticaPianoSceltaSchePianoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaPianoSceltaSchePiano(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPianoSceltaSchePiano.objects.create(**data)
        return obj


class DidatticaPianoSceltaVincoliUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaPianoSceltaVincoli(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPianoSceltaVincoli.objects.create(**data)
        return obj


class DidatticaAmbitiUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaAmbiti(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaAmbiti.objects.create(**data)
        return obj


class DidatticaPianoSceltaAfUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaPianoSceltaAf(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaPianoSceltaAf.objects.create(**data)
        return obj

class DidatticaArticoliRegolamentoStatusUnitTest(TestCase):
    @classmethod
    def create_didatticaArticoliRegolamentoStatus(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaArticoliRegolamentoStatus.objects.create(**data)
        return obj

class DidatticaCdsTipoCorsoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaCdsTipoCorso(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsTipoCorso.objects.create(**data)
        return obj
    
    
class DidatticaArticoliRegolamentoStrutturaUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaArticoliRegolamentoStruttura(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaArticoliRegolamentoStruttura.objects.create(**data)
        return obj
    
    
class DidatticaCdsArticoliRegolamentoTestataUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaCdsArticoliRegolamentoTestata(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsArticoliRegolamentoTestata.objects.create(**data)
        return obj
    
class DidatticaArticoliRegolamentoStrutturaTopicUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaArticoliRegolamentoStrutturaTopic(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaArticoliRegolamentoStrutturaTopic.objects.create(**data)
        return obj
    
    
class DidatticaCdsArticoliRegolamentoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaCdsArticoliRegolamento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsArticoliRegolamento.objects.create(**data)
        return obj
    
    
class DidatticaArticoliRegolamentoTitoloUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaArticoliRegolamentoTitolo(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaArticoliRegolamentoTitolo.objects.create(**data)
        return obj


class DidatticaCdsSubArticoliRegolamentoUnitTest(TestCase): # pragma: no cover
    @classmethod
    def create_didatticaCdsSubArticoliRegolamento(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaCdsSubArticoliRegolamento.objects.create(**data)
        return obj
