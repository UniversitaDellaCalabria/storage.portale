from functools import reduce
import operator

from django.db.models import Q
from .models import DidatticaCds


class ServiceQueryBuilder:
    @staticmethod
    def build_filter_chain(params_dict, query_params, *args):
        return reduce(operator.and_,
                      [Q(**{v: query_params.get(k)})
                       for (k, v) in params_dict.items() if query_params.get(k)] + list(args),
                      Q())


class ServiceDidatticaCds:
    @staticmethod
    def cdslist(language, query_params):
        didatticacds_params_to_query_field = {
            'coursetype': 'tipo_corso_cod',
            'courseclassid': 'cla_miur_cod',
            'courseclassname': 'cla_miur_des__iexact',
            # 'courseclassgroup': ... unspecified atm
            'departmentid': 'dip__dip_cod',
            'departmentname': f'dip__dip_des_{language == "it" and "it" or "eng"}__iexact',
        }

        didatticaregolamento_params_to_query_field = {
            'academicyear': 'didatticaregolamento__aa_reg_did',
            'jointdegree': 'didatticaregolamento__titolo_congiunto_cod',
            'regdid_id': 'didatticaregolamento__regdid_id',
        }

        didatticacdslingua_params_to_query_field = {
            'cdslanguage': 'didatticacdslingua__iso6392_cod__iexact',
        }

        keywords = set(
            query_params.get(
                'keywords', '').split(','))

        items = DidatticaCds.objects \
            .filter(reduce(operator.and_,
                           [Q(**{f'nome_cds_{language == "it" and "it" or "eng"}__icontains': e})
                            for e in keywords],
                           Q())) \
            .filter(ServiceQueryBuilder.build_filter_chain(didatticacds_params_to_query_field,
                                                           query_params)) \
            .filter(ServiceQueryBuilder.build_filter_chain(didatticaregolamento_params_to_query_field,
                                                           query_params,
                                                           Q(didatticaregolamento__stato_regdid_cod='A'))) \
            .filter(ServiceQueryBuilder.build_filter_chain(didatticacdslingua_params_to_query_field,
                                                           query_params,
                                                           Q(didatticacdslingua__lin_did_ord_id__isnull=False))) \
            .values('didatticaregolamento__regdid_id',
                    'didatticaregolamento__aa_reg_did',
                    'didatticaregolamento__frequenza_obbligatoria',
                    'dip__dip_cod',
                    'dip__dip_des_it',
                    'dip__dip_des_eng',
                    'didatticacdslingua__iso6392_cod',
                    'cds_id',
                    'nome_cds_it',
                    'nome_cds_eng',
                    'tipo_corso_cod',
                    'cla_miur_cod',
                    'cla_miur_des',
                    'durata_anni',
                    'valore_min',
                    'codicione').distinct()

        return items
