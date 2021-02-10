from functools import reduce
import operator

from django.db.models import Q
from .models import DidatticaCds, DidatticaAttivitaFormativa


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
            'cdslanguage': f'didatticacdslingua__lingua_des_{language == "it" and "it" or "eng"}__iexact',
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
                    'didatticacdslingua__lingua_des_it',
                    'didatticacdslingua__lingua_des_eng',
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


class ServiceDidatticaAttivitaFormativa:

    # filtrare quelli che hanno af_id = af_radice_id
    @staticmethod
    def getListAttivitaFormativa(regdid_id, only_main_course=True):
        query = DidatticaAttivitaFormativa.objects.filter(
            regdid=regdid_id, af_id__isnull=False)
        if only_main_course:
            # QuerySet(model=DidatticaAttivitaFormativa)
            new_query = DidatticaAttivitaFormativa.objects.none()
            for q in query:
                if q.checkIfMainCourse():
                    new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                        af_id=q.af_id)
            query = new_query

        return query.order_by('pds_regdid__pds_regdid_id', 'anno_corso', 'ciclo_des') \
            .values('pds_regdid__pds_regdid_id', 'pds_regdid__pds_des_it', 'pds_regdid__pds_des_eng',
                    'regdid__regdid_id',
                    'af_id', 'des', 'af_gen_des_eng', 'cds__cds_id', 'anno_corso',
                    'ciclo_des', 'peso', 'sett_des', 'freq_obblig_flg',
                    'cds__nome_cds_it', 'cds__nome_cds_eng')

    @staticmethod
    def getAttivitaFormativaByStudyPlan(studyplanid):
        query = DidatticaAttivitaFormativa.objects.filter(
            pds_regdid__pds_regdid_id=studyplanid, af_id__isnull=False)
        new_query = DidatticaAttivitaFormativa.objects.none()
        for q in query:
            if q.checkIfMainCourse():
                new_query = new_query | DidatticaAttivitaFormativa.objects.filter(
                    af_id=q.af_id)

        return new_query.order_by('anno_corso', 'ciclo_des') \
            .values('af_id', 'des', 'af_gen_des_eng', 'cds__cds_id', 'anno_corso',
                    'ciclo_des', 'peso', 'sett_des', 'freq_obblig_flg',
                    'cds__nome_cds_it', 'cds__nome_cds_eng')

    # @staticmethod
    # def getAttivitaFormativaWithSubModules(af_id):
    #     list_submodules = DidatticaAttivitaFormativa.objects.filter(af_radice_id=af_id) \
    #         .exclude(af_id=af_id) \
    #         .values('af_id', 'des', 'af_gen_des_eng', 'ciclo_des')
    #     query = DidatticaAttivitaFormativa.objects.filter(af_id=af_id).order_by('anno_corso', 'ciclo_des') \
    #             .values('af_id', 'des', 'af_gen_des_eng', 'cds__cds_id', 'anno_corso',
    #                     'ciclo_des', 'peso', 'sett_des', 'freq_obblig_flg',
    #                     'cds__nome_cds_it', 'cds__nome_cds_eng')
    #     query[0]['MODULES'] = list_submodules
    #
    #     return query
