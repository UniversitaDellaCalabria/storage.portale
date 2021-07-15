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
    FunzioniUnitaOrganizzativa,
    UnitaOrganizzativa, UnitaOrganizzativaContatti)


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
        }
        for k, v in kwargs.items():
            data[k] = v

        obj = DidatticaAttivitaFormativa.objects.create(**data)
        return obj


class DidatticaPdsRegolamentoUnitTest(TestCase):
    @classmethod
    def create_didatticaPdsRegolamento(cls, **kwargs):
        data = {
            'aa_ord_id': 1,
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


class PersonaleTipoContattoUnitTest(TestCase):
    @classmethod
    def create_personaleTipoContatto(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = PersonaleUoTipoContatto.objects.create(**data)
        return obj


class FunzioniUnitaOrganizzativaUnitTest(TestCase):
    @classmethod
    def create_funzioniUnitaOrganizzativa(cls, **kwargs):
        data = {}
        for k, v in kwargs.items():
            data[k] = v

        obj = FunzioniUnitaOrganizzativa.objects.create(**data)
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



