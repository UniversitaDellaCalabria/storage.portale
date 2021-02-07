from django.test import TestCase

from .models import (DidatticaCds, DidatticaCdsLingua, DidatticaRegolamento, DidatticaDipartimento, ComuniAll,
                     TerritorioIt, DidatticaTestiRegolamento)


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
            'iso6392_cod': 'ita',
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
            'cds_id': 1,
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
