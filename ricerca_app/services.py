from functools import reduce
import operator

from django.db.models import Q
from .models import DidatticaCds, DidatticaAttivitaFormativa, DidatticaTestiAf


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

    @staticmethod
    def getAttivitaFormativaWithSubModules(af_id, language):
        list_submodules = DidatticaAttivitaFormativa.objects.filter(af_radice_id=af_id) \
            .exclude(af_id=af_id) \
            .values('af_id', 'des', 'af_gen_des_eng', 'ciclo_des')

        # TODO: StudyActivityTeacherID e StudyActivityTeacherName, problema
        # join con Personale
        query = DidatticaAttivitaFormativa.objects.filter(af_id=af_id).order_by('anno_corso', 'ciclo_des') \
            .values('af_id', 'des', 'af_gen_des_eng', 'cds__cds_id', 'anno_corso',
                    'ciclo_des', 'peso', 'sett_des', 'freq_obblig_flg',
                    'cds__nome_cds_it', 'cds__nome_cds_eng', 'tipo_af_des',
                    )
        texts_af = DidatticaTestiAf.objects.filter(
            af_id=af_id).values(
            'tipo_testo_af_cod',
            'testo_af_ita',
            'testo_af_eng')

        query = list(query)
        query[0]['MODULES'] = list()
        for i in range(len(list_submodules)):
            query[0]['MODULES'].append({
                'StudyActivityID': list_submodules[i]['af_id'],
                'StudyActivityName': list_submodules[i]['des'] if language == 'it' or list_submodules[i]['af_gen_des_eng'] is None else list_submodules[i]['af_gen_des_eng'],
                'StudyActivitySemester': list_submodules[i]['ciclo_des'],
            })

        query[0]['StudyActivityContent'] = None
        query[0]['StudyActivityProgram'] = None
        query[0]['StudyActivityLearningOutcomes'] = None
        query[0]['StudyActivityMethodology'] = None
        query[0]['StudyActivityEvaluation'] = None
        query[0]['StudyActivityTextbooks'] = None
        query[0]['StudyActivityWorkload'] = None
        query[0]['StudyActivityElearningLink'] = None
        query[0]['StudyActivityElearningInfo'] = None
        query[0]['StudyActivityPrerequisites'] = None

        dict_activity = {
            'CONTENUTI': 'StudyActivityContent',
            'PROGR_EST': 'StudyActivityProgram',
            'OBIETT_FORM': 'StudyActivityLearningOutcomes',
            'METODI_DID': 'StudyActivityMethodology',
            'MOD_VER_APPR': 'StudyActivityEvaluation',
            'TESTI_RIF': 'StudyActivityTextbooks',
            'STIMA_CAR_LAV': 'StudyActivityWorkload',
            'PREREQ': 'StudyActivityPrerequisites',
            'LINK_TEAMS': 'StudyActivityElearningLink',
            'CODICE_TEAMS': 'StudyActivityElearningInfo',
            'PROPEDE': None,
            'LINGUA_INS': None,
            'PAG_WEB_DOC': None,
            'ALTRO': None,
        }

        for text in texts_af:
            query[0][dict_activity[text['tipo_testo_af_cod']]
                     ] = text['testo_af_ita'] if language == 'it' or text['testo_af_eng'] is None else text['testo_af_eng']

        return query
