import json
import requests

from django.conf import settings

from rest_framework import serializers

from crud.phd.settings import PHD_CYCLES

from . models import DidatticaRegolamento
from . settings import (ALLOWED_PROFILE_ID,
                        CDS_BROCHURE_MEDIA_PATH,
                        CDS_BROCHURE_IS_VISIBLE,
                        # COMPANIES_MEDIA_PATH,
                        # LABORATORIES_MEDIA_PATH,
                        PERSON_CONTACTS_TO_TAKE)
                        # PATENTS_MEDIA_PATH,
                        # TEACHER_CV_EN_MEDIA_PATH,
                        # TEACHER_CV_IT_MEDIA_PATH,
                        # TEACHER_PHOTO_MEDIA_PATH)
from . utils import build_media_path, encrypt, is_path


ALLOWED_PROFILE_ID = getattr(settings, 'ALLOWED_PROFILE_ID', ALLOWED_PROFILE_ID)
CDS_BROCHURE_MEDIA_PATH = getattr(settings, 'CDS_BROCHURE_MEDIA_PATH', CDS_BROCHURE_MEDIA_PATH)
CDS_BROCHURE_IS_VISIBLE = getattr(settings, 'CDS_BROCHURE_IS_VISIBLE', CDS_BROCHURE_IS_VISIBLE)
# COMPANIES_MEDIA_PATH = getattr(settings, 'COMPANIES_MEDIA_PATH', COMPANIES_MEDIA_PATH)
# LABORATORIES_MEDIA_PATH = getattr(settings, 'LABORATORIES_MEDIA_PATH', LABORATORIES_MEDIA_PATH)
# PATENTS_MEDIA_PATH = getattr(settings, 'PATENTS_MEDIA_PATH', PATENTS_MEDIA_PATH)
# TEACHER_CV_EN_MEDIA_PATH = getattr(settings, 'TEACHER_CV_EN_MEDIA_PATH', TEACHER_CV_EN_MEDIA_PATH)
# TEACHER_CV_IT_MEDIA_PATH = getattr(settings, 'TEACHER_CV_IT_MEDIA_PATH', TEACHER_CV_IT_MEDIA_PATH)
# TEACHER_PHOTO_MEDIA_PATH = getattr(settings, 'TEACHER_PHOTO_MEDIA_PATH', TEACHER_PHOTO_MEDIA_PATH)
PERSON_CONTACTS_TO_TAKE = getattr(settings, 'PERSON_CONTACTS_TO_TAKE', PERSON_CONTACTS_TO_TAKE)
PHD_CYCLES = getattr(settings, 'PHD_CYCLES', PHD_CYCLES)


def _get_teacher_obj_publication_date(teacher_dict):
    if not teacher_dict['dt_pubblicazione']: return None
    if not teacher_dict['dt_inizio_validita']: return teacher_dict['dt_pubblicazione']
    if not teacher_dict['dt_pubblicazione']: return teacher_dict['dt_inizio_validita']
    if teacher_dict['dt_pubblicazione'] > teacher_dict['dt_inizio_validita']:
        return teacher_dict['dt_pubblicazione']
    return teacher_dict['dt_inizio_validita']



class CreateUpdateAbstract(serializers.Serializer):
    def create(self, validated_data):
        try:
            super().create(validated_data)
        except BaseException:
            pass

    def update(self, instance, validated_data):
        try:
            super().update(instance, validated_data)
        except BaseException:
            pass


class CdSSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        langs = []
        for q in query['Languages']:
            langs.append(q['lingua_des_it'] if req_lang ==
                         'it' or q['lingua_des_eng'] is None else q['lingua_des_eng'])
        # data = None
        # if query["OtherData"] is not None:
            # data = CdSSerializer.to_dict_data(
                # query["OtherData"])
        erogation_mode = None
        if query['ErogationMode'] is not None:
            erogation_mode = query['ErogationMode'][0]['modalita_erogazione']

        regdid = DidatticaRegolamento.objects.filter(pk=query['didatticaregolamento__regdid_id']).first()
        ordinamento_didattico = regdid.get_ordinamento_didattico()

        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'CdSId': query['cds_id'],
            'CdSCod': query['cds_cod'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'AreaCds': query['area_cds'] if req_lang=='it' or query['area_cds_en'] is None else query['area_cds_en'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_id'],
            'DepartmentCod': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseTypeDescription': query['tipo_corso_des'],
            'CourseClassCod': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CourseInterClassCod': query['intercla_miur_cod'],
            'CourseInterClassDes': query['intercla_miur_des'],
            'ErogationMode': erogation_mode,
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'RegDidState': query['didatticaregolamento__stato_regdid_cod'],
            'JointDegree': query['didatticaregolamento__titolo_congiunto_cod'],
            'StudyManifesto': build_media_path(query["OtherData"][0]['manifesto_studi']) if query["OtherData"] else None,
            'DidacticRegulation': build_media_path(query["OtherData"][0]['regolamento_didattico']) if query["OtherData"] else None,
            'TeachingSystem': build_media_path(ordinamento_didattico[1]) if ordinamento_didattico else None,
            'TeachingSystemYear': ordinamento_didattico[0] if ordinamento_didattico else None,
        }

    # @staticmethod
    # def to_dict_data(query):
        # if query:
            # q = query[0]
            # return {'SeatsNumber': q['num_posti'],
                    # 'RegistrationMode': q['modalita_iscrizione'],
                    # }
        # return {}


class CdsInfoSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        langs = []
        for q in query['Languages']:
            langs.append(q['didatticacdslingua__lingua_des_it'] if req_lang == 'it' or q[
                'didatticacdslingua__lingua_des_eng'] is None else q['didatticacdslingua__lingua_des_eng'])
        video = None
        if query['URL_CDS_VIDEO'] is not None:
            # video = CdsInfoSerializer.get_media_url(
                # query['URL_CDS_VIDEO'])
            video = build_media_path(
                query['URL_CDS_VIDEO'], CDS_BROCHURE_MEDIA_PATH)

        doc = None
        if query['URL_CDS_DOC'] is not None:
            # doc = CdsInfoSerializer.get_media_url(
                # query['URL_CDS_DOC'])
            doc = build_media_path(
                query['URL_CDS_DOC'], CDS_BROCHURE_MEDIA_PATH)

        data = None
        if query["OtherData"] is not None:
            data = CdsInfoSerializer.to_dict_data(
                query["OtherData"])
        offices_data = None
        if query["OfficesData"] is not None:
            offices_data = CdsInfoSerializer.to_dict_offices_data(
                query["OfficesData"])

        erogation_mode = None
        if query['ErogationMode'] is not None:
            erogation_mode = query['ErogationMode'][0]['modalita_erogazione']

        cds_groups_data = None
        if query["CdsGroups"] is not None:
            cds_groups_data = CdsInfoSerializer.to_dict_cds_groups_data(
                query["CdsGroups"], req_lang)

        cds_periods_data = None
        if query["CdsPeriods"] is not None:
            cds_periods_data = CdsInfoSerializer.to_dict_cds_periods_data(
                query["CdsPeriods"], req_lang)

        regdid = DidatticaRegolamento.objects.filter(pk=query['didatticaregolamento__regdid_id']).first()
        ordinamento_didattico = regdid.get_ordinamento_didattico()

        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'RegDidState': query['didatticaregolamento__stato_regdid_cod'],
            'CdSId': query['cds_id'],
            'CdSCod': query['cds_cod'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'AreaCds': query['area_cds'] if req_lang=='it' or query['area_cds_en'] is None else query['area_cds_en'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_id'],
            'DepartmentCod': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseTypeDescription': query['tipo_corso_des'],
            'CourseClassCod': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CourseInterClassCod': query['intercla_miur_cod'],
            'CourseInterClassDes': query['intercla_miur_des'],
            'ErogationMode': erogation_mode,
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'CdSIntro': query['INTRO_CDS_FMT'] if query['INTRO_CDS_FMT'] is not None else query['DESC_COR_BRE'],
            'CdSDoc': doc if CDS_BROCHURE_IS_VISIBLE else None,
            'CdsUrl': query['URL_CDS'],
            'CdSVideo': video,
            'CdSGoals': query['OBB_SPEC'],
            'CdSAccess': query['REQ_ACC'],
            'CdSAdmission': query['REQ_ACC_2'],
            'CdSProfiles': query['PROFILO'],
            'CdSFinalTest': query['PROVA_FINALE'],
            'CdSFinalTestMode': query['PROVA_FINALE_2'],
            'CdSSatisfactionSurvey': query['codicione'],
            'JointDegree': query['didatticaregolamento__titolo_congiunto_cod'],
            'StudyManifesto': build_media_path(query["OtherData"][0]['manifesto_studi']) if query["OtherData"] else None,
            'DidacticRegulation': build_media_path(query["OtherData"][0]['regolamento_didattico']) if query["OtherData"] else None,
            'TeachingSystem': build_media_path(ordinamento_didattico[1]) if ordinamento_didattico else None,
            'TeachingSystemYear': ordinamento_didattico[0] if ordinamento_didattico else None,
            'OtherData': data,
            'OfficesData': offices_data,
            'CdsGroups': cds_groups_data,
            'CdsPeriods': cds_periods_data
        }

    # @staticmethod
    # def get_media_url(query):
        # if 'https' in query or 'http' in query:
            # return query
        # else:
            # query = build_media_path(query, CDS_BROCHURE_MEDIA_PATH),
            # #query = f'{settings.CDS_BROCHURE_MEDIA_PATH}/{query}'
            # return query

    @staticmethod
    def to_dict_data(query):
        if query:
            q = query[0]
            return {'DirectorId': encrypt(q['matricola_coordinatore']),
                    'DirectorName': q['nome_origine_coordinatore'],
                    'DeputyDirectorId': encrypt(q['matricola_vice_coordinatore']),
                    'DeputyDirectorName': q['nome_origine_vice_coordinatore'],
                    # 'SeatsNumber': q['num_posti'],
                    # 'RegistrationMode': q['modalita_iscrizione'],
                    # 'StudyManifesto': build_media_path(q['manifesto_studi']),
                    # 'DidacticRegulation': build_media_path(q['regolamento_didattico']),
                    # 'TeachingSystem': build_media_path(q['ordinamento_didattico'])
                    }
        return {}

    @staticmethod
    def to_dict_offices_data(query):
        data = []
        for q in query:
            data.append({
                'Order': q['ordine'],
                'OfficeName': q['nome_ufficio'],
                'OfficeDirector': encrypt(q['matricola_riferimento']),
                'OfficeDirectorName': q['nome_origine_riferimento'],
                'TelOffice': q['telefono'],
                'Email': q['email'],
                'Building': q['edificio'],
                'Floor': q['piano'],
                'Timetables': q['orari'],
                'OnlineCounter': q['sportello_online']
            })
        return data

    @staticmethod
    def to_dict_cds_groups_data(query, req_lang='en'):
        data = []
        for q in query:
            data.append({
                'Order': q['ordine'],
                'ShortDesc': q['descr_breve_it'] if req_lang == 'it' or q['descr_breve_en'] is None else q['descr_breve_en'],
                'LongDesc': q['descr_lunga_it'] if req_lang == 'it' or q['descr_lunga_en'] is None else q['descr_lunga_en'],
                'Members': CdsInfoSerializer.to_dict_cds_group_members(q['members'], req_lang),
            })
        return data

    @staticmethod
    def to_dict_cds_group_members(query, req_lang='en'):
        data = []
        for q in query:
            data.append({
                'Order': q['ordine'],
                'ID': encrypt(q['matricola']),
                'Surname': q['cognome'],
                'Name': q['nome'],
                'Function': q['funzione_it'] if req_lang == 'it' or q['funzione_en'] is None else q['funzione_en'],
            })
        return data

    @staticmethod
    def to_dict_cds_periods_data(query, req_lang='en'):
        data = []
        for q in query:
            data.append({
                'Description': q['tipo_ciclo_des'] if req_lang == 'it' or q['tipo_ciclo_des_eng'] is None else q['tipo_ciclo_des_eng'],
                'Start': q['data_inizio'],
                'End': q['data_fine'],
            })
        return data


class CdsWebsiteLightSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(self.to_dict(instance,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
                'Id': query['id'],
                # 'CDSId': query['cds__cds_id'],
                'CDSCOD': query['cds__cds_cod'],
                'CDSAcademicYear': query['aa'],
                'CDSName': query['cds__nome_cds_it'] if req_lang=='it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
            }


class CdsWebsiteSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(self.to_dict(instance,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):

        ex_students = []
        if query.get('ExStudents'):
            ex_students = CdsWebsiteSerializer.to_dict_ex_students(
                query['ExStudents'], req_lang)

        cds_link = []
        if query.get('CdsLink'):
            cds_link = CdsWebsiteSerializer.to_dict_links(
                query['CdsLink'], req_lang)

        cds_sliders = []
        if query.get('CdsSliders'):
            cds_sliders = CdsWebsiteSerializer.to_dict_sliders(
                query['CdsSliders'], req_lang)

        course_interclass = None
        if query['cds__intercla_miur_cod'] and query['cds__intercla_miur_des']:
            course_interclass = f"{query['cds__intercla_miur_cod']} {query['cds__intercla_miur_des']}"

        course_class = None
        if query['cds__cla_miur_cod'] and query['cds__cla_miur_des']:
            course_class = f"{query['cds__cla_miur_cod']} {query['cds__cla_miur_des']}"

        return {
            'Id': query['id'],
            # 'CDSId': query['cds_id'],
            'CDSCOD': query['cds__cds_cod'],
            'CDSAcademicYear': query['aa'],
            'CDSName': query['cds__nome_cds_it'] if req_lang=='it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
            'CDSCourseClassName': course_class,
            'CDSCourseInterClassDes': course_interclass,
            'CDSLanguage': query['lingue'], # query['lingua_it'] if req_lang=='it' or query['lingua_en'] is None else query['lingua_en'],
            'CDSDuration': query['cds__durata_anni'],
            'CDSSeatsNumber': query['num_posti'],
            'CDSVideo': query['link_video_cds_it'] if req_lang=='it' or query['link_video_cds_en'] is None else query['link_video_cds_en'],
            'CDSIntro': query['descrizione_corso_it'] if req_lang == 'it' or query['descrizione_corso_en'] is None else query['descrizione_corso_en'],
            'CDSAdmission': query['accesso_corso_it'] if req_lang == 'it' or query['accesso_corso_en'] is None else query['accesso_corso_en'],
            'CDSGoals': query['obiettivi_corso_it'] if req_lang == 'it' or query['obiettivi_corso_en'] is None else query['obiettivi_corso_en'],
            'CDSJobOpportunities': query['sbocchi_professionali_it'] if req_lang == 'it' or query['sbocchi_professionali_en'] is None else query['sbocchi_professionali_en'],
            'CDSTaxes': query['tasse_contributi_esoneri_it'] if req_lang == 'it' or query['tasse_contributi_esoneri_en'] is None else query['tasse_contributi_esoneri_en'],
            'CDSScholarships': query['borse_studio_it'] if req_lang == 'it' or query['borse_studio_en'] is None else query['borse_studio_en'],
            'CDSConcessions': query['agevolazioni_it'] if req_lang == 'it' or query['agevolazioni_en'] is None else query['agevolazioni_en'],
            'CDSShortDescription': query['corso_in_pillole_it'] if req_lang == 'it' or query['corso_in_pillole_en'] is None else query['corso_in_pillole_en'],
            'CDSStudyPlan': query['cosa_si_studia_it'] if req_lang == 'it' or query['cosa_si_studia_en'] is None else query['cosa_si_studia_en'],
            'CDSEnrollmentMode': query['come_iscriversi_it'] if req_lang == 'it' or query['come_iscriversi_en'] is None else query['come_iscriversi_en'],
            'CDSExStudents': ex_students,
            'CDSLinks': cds_link,
            'CDSSliders': cds_sliders,
        }


    @staticmethod
    def to_dict_ex_students(query, req_lang='en'):
        ex_students = []
        for q in query:
            ex_students.append({
                'StudentId': q['id'],
                'StudentName': q['nome'],
                'StudentOrder': q['ordine'],
                'StudentProfile': q['profilo_it'] if req_lang == 'it' or q['profilo_en'] is None else q['profilo_en'],
                'StudentLink': q['link_it'] if req_lang == 'it' or q['link_en'] is None else q['link_en'],
                'StudentPhoto': build_media_path(q['foto']) if q['foto'] else None
            })
        return ex_students


    @staticmethod
    def to_dict_links(query, req_lang='en'):
        links = []
        for q in query:
            links.append({
                'LinkId': q['id'],
                'LinkOrder': q['ordine'],
                'LinkDescription': q['descrizione_link_it'] if req_lang == 'it' or q['descrizione_link_en'] is None else q['descrizione_link_en'],
                'Link': q['link_it'] if req_lang == 'it' or q['link_en'] is None else q['link_en'],
            })
        return links


    @staticmethod
    def to_dict_sliders(query, req_lang='en'):
        sliders = []
        for q in query:
            sliders.append({
                'SliderId': q['id'],
                'SliderOrder': q['ordine'],
                'SliderDescription': q['slider_it'] if req_lang == 'it' or q['slider_en'] is None else q['slider_en'],
            })
        return sliders



    # @staticmethod
    # def to_dict_offices_data(query):
    #     data = []
    #     for q in query:
    #         data.append({
    #             'Order': q['ordine'],
    #             'OfficeName': q['nome_ufficio'],
    #             'OfficeDirector': encrypt(q['matricola_riferimento']),
    #             'OfficeDirectorName': q['nome_origine_riferimento'],
    #             'TelOffice': q['telefono'],
    #             'Email': q['email'],
    #             'Floor': q['piano'],
    #             'Timetables': q['orari'],
    #             'OnlineCounter': q['sportello_online']
    #         })
    #     return data


# class CdsWebsitesDegreeTypesSerializer(CreateUpdateAbstract):
    # def to_representation(self, instance):
        # query = instance
        # data = super().to_representation(instance)
        # data.update(self.to_dict(query,
                                 # str(self.context['language']).lower()))
        # return data

    # @staticmethod
    # def to_dict(query,
                # req_lang='en'):
        # return {
            # 'CDSCourseClassName': query['classe_laurea_it'] if req_lang=='it' or query['classe_laurea_en'] is None else query['classe_laurea_en'],
        # }


class CdsWebsitesTopicSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):


        return {
            'TopicId': query['id'],
            'TopicDescription': query['descr_topic_it'] if req_lang=='it' or query['descr_topic_en'] is None else query['descr_topic_en'],
            'Visible': query['visibile']
        }


class CdsWebsitesTopicArticlesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):

        article = None
        if query['Articles'] is not None:
            article = CdsWebsitesTopicArticlesSerializer.to_dict_articles(
                query['Articles'], req_lang)

        unicms_object = None
        if query['CdsObjects'] is not None:
            unicms_object = CdsWebsitesTopicArticlesSerializer.to_dict_objects(
                query['CdsObjects'], req_lang)

        return {
            'ID': query['id'],
            'Title': query['titolo_it'] if req_lang=='it' or query['titolo_en'] is None else query['titolo_en'],
            'TopicId': query['id_sito_web_cds_topic__id'],
            'TopicDescription': query['id_sito_web_cds_topic__descr_topic_it'] if req_lang=='it' or query['id_sito_web_cds_topic__descr_topic_en'] is None else query['id_sito_web_cds_topic__descr_topic_en'],
            'Visible': query['visibile'],
            'Order': query['ordine'],
            'CdsArticle': article,
            'CdsObject': unicms_object,
            'OtherData': CdsWebsitesTopicArticlesSerializer.to_dict_other_data(query.get('OtherData', []), req_lang),
        }


    @staticmethod
    def to_dict_articles(q, req_lang='en'):
        if q:
            return {
                'ArticleId': q['id'],
                'ArticleTitle': q['titolo_articolo_it'] if req_lang == 'it' or q['titolo_articolo_en'] is None else q['titolo_articolo_en'],
                'ArticleDescription': q['testo_it'] if req_lang == 'it' or q['testo_en'] is None else q['testo_en'],
                'ArticleNumber': q['numero'],
                'Visible': q['visibile'],
                'YearRegDidID': q['aa_regdid_id'],
                'CdSCod': q['cds_id__cds_cod'],
            }


    @staticmethod
    def to_dict_objects(q, req_lang='en'):
        if q and getattr(settings, 'UNICMS_AUTH_TOKEN', ''):
            head = {'Authorization': 'Token {}'.format(getattr(settings, 'UNICMS_AUTH_TOKEN'))}
            unicms_obj_api = getattr(settings, 'UNICMS_OBJECT_API', {})
            api_url = unicms_obj_api.get(q['id_classe_oggetto_portale'], '')
            unicms_object = requests.get(api_url.format(q['id_oggetto_portale']),
                                         headers=head,
                                         timeout=5) if api_url else None
            return {
                'Id': q['id'],
                'CdSCod': q['cds_id__cds_cod'],
                'YearRegDidID': q['aa_regdid_id'],
                'ObjectId': q['id_oggetto_portale'],
                'Object': json.loads(unicms_object._content) if unicms_object else None,
                'ClassObjectId': q['id_classe_oggetto_portale'],
                'ObjectText': q['testo_it'] if req_lang == 'it' or q['testo_en'] is None else q['testo_en'],
            }


    @staticmethod
    def to_dict_other_data(query, req_lang='en'):
        other_data = []
        for q in query:
            other_data.append({
                'Id': q['id'],
                'Order': q['ordine'],
                'Title': q['titolo_it'] if req_lang == 'it' or q['titolo_en'] is None else q['titolo_en'],
                'Text': q['testo_it'] if req_lang == 'it' or q['testo_en'] is None else q['testo_en'],
                'Link': q['link'],
                'TypeID': q['id_sito_web_cds_tipo_dato__pk'],
                'Type': q['id_sito_web_cds_tipo_dato__descr_breve'],
                'Visible': q['visibile']
            })
        return other_data

class CdsWebsitesStudyPlansSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        # study_activities = {}
        # for k in query['StudyActivities']:
        #     study_activities[k] = []
        #     for q in query['StudyActivities'][k]:
        #         study_activities[k].append(
        #             StudyPlansActivitiesSerializer.to_dict(
        #                 q, req_lang))
        plan_tabs = None
        if query['PlanTabs'] is not None:
            plan_tabs = CdsWebsitesStudyPlansSerializer.to_dict_plan(
                query['PlanTabs'], req_lang)

        return {
            'RegPlanId': query['regpiani_id'],
            'RegDidId': query['regdid_id'],
            'RelevanceCod': query['attinenza_cod'],
            'YearCoorteId': query['aa_coorte_id'],
            'YearRegPlanId': query['aa_regpiani_id'],
            'RegPlanDes': query['des'],
            'DefFlg': query['def_flg'],
            'StatusCod': query['stato_cod'],
            'StatusDes': query['stato_des'],
            'RegPlansPdrId': query['regpiani_pdr_id'],
            'RegPlansPdrCod': query['regpiani_pdr_cod'],
            'RegPlansPdrDes': query['regpiani_pdr_des'],
            'RegPlansPdrCoorteIdYear': query['regpiani_pdr_aa_coorte_id'],
            'RegPlansPdrYear': query['regpiani_pdr_aa_regpiani_id'],
            'FlgExpSegStu': query['flg_exp_seg_stu'],
            'CdSDuration': query['regdid__cds__durata_anni'],
            'PlanTabs': plan_tabs,
        }

    @staticmethod
    def to_dict_plan(query, req_lang='en'):
        plan_tabs = []
        for q in query:
            plan_tabs.append({
                'PlanTabId': q['sche_piano_id'],
                'PlanTabDes': q['sche_piano_des'],
                'PlanTabCod': q['sche_piano_cod'],
                'PdsCod': q['pds_cod'],
                'PdsDes': q['pds_des'],
                'ClaMiurCod': q['cla_miur_cod'],
                'ClaMiurDes': q['cla_miur_des'],
                'CommonFlg': q['comune_flg'],
                'Statutario': q['isStatutario'],
                'APT': True if q['apt_id'] else False,
                'AfRequired': CdsWebsitesStudyPlansSerializer.to_dict_af(q.get('AfRequired', []), req_lang),
                'AfChoices': CdsWebsitesStudyPlansSerializer.to_dict_af(q.get('AfChoices', []), req_lang),
            })
        return plan_tabs

    @staticmethod
    def to_dict_af(query, req_lang='en'):
        af = []
        for q in query:
            af.append({
                'SceId': q['sce_id'],
                'SceDes': q['sce_des'],
                'VinId': q['vin_id'],
                'Year': q['apt_slot_ord_num'] if q['apt_slot_ord_num'] else q['anno_corso'],
                'RegSceCodType': q['tipo_regsce_cod'],
                'SceCodType': q['tipo_sce_cod'],
                'SceDesType':q['tipo_sce_des'],
                'RegSceCodDes': q['tipo_regsce_des'],
                'UmRegSceCodType': q['tipo_um_regsce_cod'],
                'MinUnt': q['min_unt'],
                'MaxUnt': q['max_unt'],
                'OpzFlg': q['opz_flg'],
                'Required':  CdsWebsitesStudyPlansSerializer.to_dict_af_required(q.get('Required', []), req_lang),
                'Choices': CdsWebsitesStudyPlansSerializer.to_dict_af_choices(q.get('Choices', []), req_lang),
                'FilAnd': CdsWebsitesStudyPlansSerializer.to_dict_af_fil_and(q.get('FilAnd', []), req_lang),

            })
        return af

    @staticmethod
    def to_dict_af_required(query, req_lang='en'):
        af_required = []
        for q in query:
            af_required.append({
                'ScopeId': q['amb_id_af'],
                'SceId': q['sce_id'],
                'SceDes': q['sce_id__sce_des'],
                'ScopeDes': q['ambito_des_af'],
                'SettCod': q.get('sett_cod', None),
                'CreditValue': q['peso'],
                'CycleDes': q['ciclo_des'],
                'AfDescription': q['af_gen_des'],
                'AfId': q['af_id'],
                'AfCod': q['af_gen_cod'],
                'AfType': q['tipo_af_des_af'],
                'AfScope': q['ambito_des_af'],
                'AfSubModules': CdsWebsitesStudyPlansSerializer.to_dict_af_submodules(q.get('MODULES', []), req_lang),

            })
        return af_required

    @staticmethod
    def to_dict_af_choices(query, req_lang='en'):
        af_choices = []
        for q in query:
            af_choices.append({
                'ScopeId': q['amb_id_af'],
                'SceId': q['sce_id'],
                'SceDes': q['sce_id__sce_des'],
                'ScopeDes': q['ambito_des_af'],
                'SettCod': q.get('sett_cod', None),
                'CreditValue': q['peso'],
                'CycleDes': q['ciclo_des'],
                'AfDescription': q['af_gen_des'],
                'AfId': q['af_id'],
                'AfCod': q['af_gen_cod'],
                'AfType': q['tipo_af_des_af'],
                'AfScope': q['ambito_des_af'],
                'AfSubModules': CdsWebsitesStudyPlansSerializer.to_dict_af_submodules(q.get('MODULES', []), req_lang),
            })
        return af_choices

    @staticmethod
    def to_dict_af_submodules(query, req_lang='en'):
        af_submodules = []
        for q in query:
            af_submodules.append({
                'StudyActivityID': q['af_id'],
                'StudyActivityCod': q['af_gen_cod'],
                'StudyActivityName': q['des'] if req_lang == 'it' or q['af_gen_des_eng'] is None else q['af_gen_des_eng'],
                'StudyActivitySemester': q['ciclo_des'],
                'StudyActivitySettCod': q.get('sett_cod', None),
                'StudyActivityCreditValue': q['peso'],
                'StudyActivityPartitionCod': q['part_stu_cod'],
                'StudyActivityPartitionDescription': q['part_stu_des'],
                'StudyActivityExtendedPartitionCod': q['fat_part_stu_cod'],
                'StudyActivityExtendedPartitionDes': q['fat_part_stu_des'],
            })
        return af_submodules

    @staticmethod
    def to_dict_af_fil_and(query, req_lang='en'):
        fil_and = []
        for q in query:
            fil_and.append({
                'FilAndId': q['sce_fil_and_id'],
                'SceId': q['sce_id'],
                'FilOrId': q['sce_fil_or_id'],
                'FilOrDes': q['sce_fil_or_des'],
                'TipoFiltroCod': q['tipo_filtro_cod'],
                'TipoFiltroDes': q['tipo_filtro_des'],
                'CourseTypeSceFilAndCod': q['tipo_corso_sce_fil_and_cod'],
                'CdsSceFilAndId': q['cds_sce_fil_and_id'],
                'CdsSceFilAndCod': q['cds_sce_fil_and_cod'],
                'CdsSceFilAndNome': q['cds_sce_fil_and_nome'],
                'NotFlg': q['not_flg'],

            })
        return fil_and


    # @staticmethod
    # def to_dict_elective_courses(query, req_lang='en'):
    #     elective_courses = []
    #     for q in query:
    #         elective_courses.append({
    #             'AfId': q['af_gen_id'],
    #             'AfCod': q['af_gen_cod'],
    #             'AfDescription': q['des'] if req_lang == 'it' or q['af_gen_des_eng'] is None else q['af_gen_des_eng'],
    #             'Year': q['apt_slot_ord_num'] if q['apt_slot_ord_num'] is not None else q['anno_corso'],
    #             'SettCod': q.get('sett_cod', None),
    #             'SettDes': q.get('sett_des', None),
    #             'Peso': q['peso'],
    #
    #         })
    #     return elective_courses


class CdSStudyPlansSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        study_activities = {}
        for k in query['StudyActivities']:
            study_activities[k] = []
            for q in query['StudyActivities'][k]:
                study_activities[k].append(
                    StudyPlansActivitiesSerializer.to_dict(
                        q, req_lang))

        return {
            'RegDidId': query['regdid_id'],
            'StudyPlanId': query['pds_regdid_id'],
            'StudyPlanCOD': query['pds_cod'],
            'StudyPlanName': query['pds_regdid_id__pds_des_it'] if req_lang == 'it' or query['pds_regdid_id__pds_des_eng'] is None else query[
                'pds_regdid_id__pds_des_eng'],
            'StudyActivities': study_activities,
        }


class CdSStudyPlanSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        study_activities = {}
        for k in query['StudyActivities']:
            study_activities[k] = []
            for q in query['StudyActivities'][k]:
                study_activities[k].append(
                    StudyPlansActivitiesSerializer.to_dict(
                        q, req_lang))

        return {
            'RegDidId': query['regdid__regdid_id'],
            'StudyPlanId': query['pds_regdid_id'],
            'StudyPlanCOD': query['pds_cod'],
            'StudyPlanName': query['pds_des_it'] if req_lang == 'it' or query['pds_des_eng'] is None else query[
                'pds_des_eng'],
            'StudyActivities': study_activities,
        }


class StudyPlansActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityCod': query['af_gen_cod'],
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityCdSCod': query['cds__cds_cod'],
            'StudyActivityRegDidId': query['regdid__regdid_id'],
            'StudyActivityTeachingUnitTypeCod': query['tipo_af_cod'],
            'StudyActivityTeachingUnitType': query['tipo_af_des'],
            'StudyActivityInterclassTeachingUnitTypeCod': query['tipo_af_intercla_cod'],
            'StudyActivityInterclassTeachingUnitType': query['tipo_af_intercla_des'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
        }



class StudyActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):

        full_name = None

        if query['matricola_resp_did__cognome'] is not None:
            full_name = query['matricola_resp_did__cognome'] + " " + query['matricola_resp_did__nome'] + \
                            (" " + query['matricola_resp_did__middle_name']
                              if query['matricola_resp_did__middle_name'] is not None else "")
        descrizione_gruppo = ''
        if query['part_stu_des']: # pragma: no cover
            descrizione_gruppo = ' (' + query['part_stu_des'] + ')'

        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityCod': query['af_gen_cod'],
            'StudyActivityName': query['des']+descrizione_gruppo if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds_id'],
            'StudyActivityCdSCod': query['cds_id__cds_cod'],
            'StudyActivityLanguage': query['lista_lin_did_af'].replace(' ','').split(',') if query['lista_lin_did_af'] else [],
            'StudyActivityFatherCode': query['af_radice_id'],
            'StudyActivityFatherName': query['Father'],
            'StudyActivityRegDidId': query['regdid_id'],
            'DepartmentName': query['cds_id__dip_id__dip_des_it'] if req_lang == 'it' or query['cds_id__dip_id__dip_des_eng'] is None else query['cds_id__dip_id__dip_des_eng'],
            'DepartmentCod': query['cds_id__dip_id__dip_cod'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivityAcademicYear': query['aa_off_id'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivitySSDCod': query.get('sett_cod', None),
            'StudyActivitySSD': query.get('sett_des', None),
            'StudyActivityPartitionCod': query['part_stu_cod'],
            'StudyActivityPartitionDes': query['part_stu_des'],
            'StudyActivityExtendedPartitionCod': query['fat_part_stu_cod'],
            'StudyActivityExtendedPartitionDes': query['fat_part_stu_des'],
            'StudyActivityCdSName': query['cds_id__nome_cds_it'] if req_lang == 'it' or query['cds_id__nome_cds_eng'] is None else query['cds_id__nome_cds_eng'],
            'StudyActivityTeacherID': encrypt(query['matricola_resp_did']) if query['matricola_resp_did'] else None,
            'StudyActivityTeacherName': full_name,
            'StudyPlanDes': query['pds_des'],
        }

    # @staticmethod
    # def to_dict_teachers(query):
    #     result = []
    #     for q in query:
    #         full_name = q['cognome'] + " " + q['nome'] + \
    #                     (" " + q['middle_name']
    #                      if q['middle_name'] is not None else "")
    #         result.append({
    #             'TeacherName': full_name,
    #         })
    #     return result


class StudyActivityInfoSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        studyactivityroot = None
        if query['ActivityRoot'] is not None:
            studyactivityroot = StudyActivityMinimalInfoSerializer.to_dict(
                query['ActivityRoot'], req_lang)

        studyactivityfather = None
        if query['ActivityFather'] is not None:
            studyactivityfather = StudyActivityMinimalInfoSerializer.to_dict(
                query['ActivityFather'], req_lang)

        studyactivityborrowed = None
        if query['BorrowedFrom'] is not None:
            studyactivityborrowed = StudyActivityMinimalInfoSerializer.to_dict(
                query['BorrowedFrom'], req_lang)

        studyactivitiesborrowedfromthis = []
        if len(query['ActivitiesBorrowedFromThis']) > 0:
            for q in query['ActivitiesBorrowedFromThis']:
                studyactivitiesborrowedfromthis.append(
                    StudyActivityMinimalInfoSerializer.to_dict(q, req_lang))

        ore = None
        if query['Hours'] is not None:
            ore = StudyActivityInfoSerializer.to_dict_hours(
                query['Hours'])

        modalities = None
        if query['Modalities'] is not None:
            modalities = StudyActivityInfoSerializer.to_dict_modalities(
                query['Modalities'])
        descrizione_gruppo = ''
        if query['part_stu_des']: # pragma: no cover
            descrizione_gruppo = '(' +query['part_stu_des'] +')'
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityCod': query['af_gen_cod'],
            'StudyActivityName': query['des']+descrizione_gruppo if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityCdSCod': query['cds__cds_cod'],
            'StudyActivityLanguage': query['lista_lin_did_af'].replace(' ','').split(',') if query['lista_lin_did_af'] else [],
            'StudyActivityRegDidId': query['regdid__regdid_id'],
            'StudyActivityPdsCod': query['pds_cod'],
            'StudyActivityPdsDes': query['pds_des'],
            'StudyActivityErogationYear': query['regdid__aa_reg_did'] + query['anno_corso'] -1 if query['anno_corso'] else studyactivityroot.get('StudyActivityErogationYear', None),
            'StudyActivityYear': query['anno_corso'] or studyactivityroot.get('StudyActivityYear', None),
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityErogationLanguage': query['LANGUAGEIT'] if req_lang == 'it' or query['LANGUAGEEN'] is None else query['LANGUAGEEN'],
            'StudyActivityECTS': query['peso'],
            'StudyActivityHours': ore,
            'StudyActivityModalities': modalities,
            'StudyActivitySSD': query.get('sett_des', None),
            'StudyActivitySSDCod': query.get('sett_cod', None),
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
            'StudyActivityTeachingUnitTypeCod': query['tipo_af_cod'],
            'StudyActivityTeachingUnitType': query['tipo_af_des'],
            'StudyActivityInterclassTeachingUnitTypeCod': query['tipo_af_intercla_cod'],
            'StudyActivityInterclassTeachingUnitType': query['tipo_af_intercla_des'],
            'StudyActivityTeacherID': encrypt(query['StudyActivityTeacherID']),
            'StudyActivityTeacherName': query['StudyActivityTeacherName'],
            'StudyActivityPartitionCod': query['PartitionCod'],
            'StudyActivityPartitionDes': query['PartitionDescription'],
            'StudyActivityExtendedPartitionCod': query['ExtendedPartitionCod'],
            'StudyActivityExtendedPartitionDes': query['ExtendedPartitionDescription'],
            'StudyActivityContent': query['StudyActivityContent'],
            'StudyActivityProgram': query['StudyActivityProgram'],
            'StudyActivityLearningOutcomes': query['StudyActivityLearningOutcomes'],
            'StudyActivityMethodology': query['StudyActivityMethodology'],
            'StudyActivityEvaluation': query['StudyActivityEvaluation'],
            'StudyActivityTextbooks': query['StudyActivityTextbooks'],
            'StudyActivityWorkload': query['StudyActivityWorkload'],
            'StudyActivityElearningLink': query['StudyActivityElearningLink'],
            'StudyActivityElearningInfo': query['StudyActivityElearningInfo'],
            'StudyActivityPrerequisites': query['StudyActivityPrerequisites'],
            'StudyActivityDevelopmentGoal': query['StudyActivityDevelopmentGoal'],
            'StudyActivitiesModules': query['MODULES'],
            'StudyActivityRoot': studyactivityroot,
            'StudyActivityFather': studyactivityfather,
            'StudyActivityBorrowedFrom': studyactivityborrowed,
            'StudyActivitiesBorrowedFromThis': studyactivitiesborrowedfromthis}


    @staticmethod
    def to_dict_hours(query):
        hours = []
        for q in query:
            full_name = None
            if q['coper_id__personale_id__cognome'] and q['coper_id__personale_id__nome']:
                full_name = f"{q['coper_id__personale_id__cognome']} {q['coper_id__personale_id__nome']}"
                if q['coper_id__personale_id__middle_name']:
                    full_name = f"{full_name} {q['coper_id__personale_id__middle_name']}"
            hours.append({
                'ActivityType': q['tipo_att_did_cod'],
                'Hours': q['ore'],
                'StudyActivityTeacherID': encrypt(q['coper_id__personale_id__matricola']) if not q['coper_id__personale_id__flg_cessato'] else None,
                'StudyActivityTeacherName': full_name
            })
        return hours

    @staticmethod
    def to_dict_modalities(query):
        modalities = []
        for q in query:
            modalities.append({
                'ModalityActivityId': q['mod_did_af_id'],
                'ModalityActivityCod': q['mod_did_cod'],
                'ModalityActivityDescription': q['mod_did_des'],
            })
        return modalities


class StudyActivityMinimalInfoSerializer(CreateUpdateAbstract):
    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'StudyActivityID': query.get('af_id'),
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivityErogationYear': query['regdid__aa_reg_did'] + query['anno_corso'] -1 if query.get('anno_corso') else None,
            'StudyActivityRegDidId': query['regdid__regdid_id'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
            'StudyActivityCdSCod': query['cds__cds_cod'],
            'StudyActivityPdsCod': query['pds_cod'],
            'StudyActivityPdsDes': query['pds_des'],

        }


# class CdSMainTeachersSerializer(CreateUpdateAbstract):
#     def to_representation(self, instance):
#         query = instance
#         data = super().to_representation(instance)
#         data.update(self.to_dict(query,
#                                  str(self.context['language']).lower()))
#         return data
#
#     @staticmethod
#     def to_dict(query,
#                 req_lang='en'):
#         name = query['didatticacopertura__personale__cognome'] + " " + query['didatticacopertura__personale__nome'] + \
#             (" " + query['didatticacopertura__personale__middle_name']
#              if query['didatticacopertura__personale__middle_name'] is not None else "")
#         return {
#             'TeacherID': query['didatticacopertura__personale__matricola'],
#             'TeacherName': name,
#             'TeacherRole': query['didatticacopertura__personale__cd_ruolo'],
#             'TeacherSSD': query['didatticacopertura__personale__cd_ssd'],
#         }


# class TeacherResearchGroupsSerializer(CreateUpdateAbstract):
#     def to_representation(self, instance):
#         query = instance
#         data = super().to_representation(instance)
#         data.update(self.to_dict(query,
#                                  str(self.context['language']).lower()))
#         return data
#
#     @staticmethod
#     def to_dict(query,
#                 req_lang='en'):
#         return {
#             'RGroupID': query['ricercadocentegruppo__ricerca_gruppo__id'],
#             'RGroupName': query['ricercadocentegruppo__ricerca_gruppo__nome'],
#             'RGroupDescription': query['ricercadocentegruppo__ricerca_gruppo__descrizione'],
#         }


# class ResearchGroupsSerializer(CreateUpdateAbstract):
#     def to_representation(self, instance):
#         query = instance
#         data = super().to_representation(instance)
#         data.update(self.to_dict(query,
#                                  str(self.context['language']).lower()))
#         return data
#
#     @staticmethod
#     def to_dict(query,
#                 req_lang='en'):
#
#         return {
#             'RGroupID': query['id'],
#             'RGroupName': query['nome'],
#             'RGroupDescription': query['descrizione'],
#         }


class AllResearchGroupsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        teachers = None
        if query['Teachers'] is not None:
            teachers = AllResearchGroupsSerializer.to_dict_teachers(
                query['Teachers'])
        return {
            'RGroupID': query['id'],
            'RGroupName': query['nome'],
            'RGroupDescription': query['descrizione'],
            'IdErc1': query['ricerca_erc1_id__cod_erc1'],
            'RLineDescription': query['ricerca_erc1_id__descrizione'],
            'Teachers': teachers,
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q['personale_id__cognome'] + " " + q['personale_id__nome'] + \
                (" " + q['personale_id__middle_name']
                 if q['personale_id__middle_name'] is not None else "")
            result.append({
                'TeacherID': encrypt(q['personale_id__matricola']),
                'TeacherName': full_name,
                'DepartmentName': q['personale_id__ds_sede'],
                'DepartmentCod': q['personale_id__sede']
            })
        return result


class TeacherResearchLinesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        if query['Tipologia'] == 'base':
            return {
                'RLineID': query['ricercadocentelineabase__ricerca_linea_base__id'],
                'RLineDescription': query['ricercadocentelineabase__ricerca_linea_base__descrizione'],
                'RLineResults': query['ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto'],
                'RLineERC0Id': query['ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod'],
                'RLineERC0Name': query['ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description'],
            }
        else:
            return {
                'RLineID': query['ricercadocentelineaapplicata__ricerca_linea_applicata__id'],
                'RLineDescription': query['ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione'],
                'RLineResults': query['ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto'],
                'RLineERC0Id': query[
                    'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod'],
                'RLineERC0Name': query[
                    'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description'],
            }


class BaseResearchLinesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        teachers = None
        if query['Teachers'] is not None:
            teachers = BaseResearchLinesSerializer.to_dict_teachers(
                query['Teachers'])
        return{
            'RLineID': query['id'],
            'RLineDescription': query['descrizione'],
            'RLineResults': query['descr_pubblicaz_prog_brevetto'],
            'RYear': query['anno'],
            'RLineErc2ID': query['ricerca_erc2_id__cod_erc2'],
            'RLineErc2Name': query['ricerca_erc2_id__descrizione'],
            'Teachers': teachers,
            'RLineVisibile': query['visibile']
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q['personale_id__cognome'] + " " + q['personale_id__nome'] + \
                (" " + q['personale_id__middle_name']
                 if q['personale_id__middle_name'] is not None else "")
            result.append({
                'TeacherID': encrypt(q['personale_id__matricola']),
                'TeacherName': full_name,
                'DepartmentName': q['personale_id__ds_sede'],
                'DepartmentCod': q['personale_id__sede'],
            })
        return result


class AppliedResearchLinesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        teachers = None
        if query['Teachers'] is not None:
            teachers = AppliedResearchLinesSerializer.to_dict_teachers(
                query['Teachers'])
        return{
            'RLineID': query['id'],
            'RLineDescription': query['descrizione'],
            'RLineResults': query['descr_pubblicaz_prog_brevetto'],
            'RYear': query['anno'],
            'RLineAster2Id': query['ricerca_aster2_id__ricerca_aster1_id'],
            'RLineAster2Name': query['ricerca_aster2_id__descrizione'],
            'Teachers': teachers,
            'RLineVisibile': query['visibile']
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q['personale_id__cognome'] + " " + q['personale_id__nome'] + \
                (" " + q['personale_id__middle_name']
                 if q['personale_id__middle_name'] is not None else "")
            result.append({
                'TeacherID': encrypt(q['personale_id__matricola']),
                'TeacherName': full_name,
                'DepartmentName': q['personale_id__ds_sede'],
                'DepartmentCod': q['personale_id__sede'],
            })
        return result


class AllResearchLinesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        teachers = None
        if query['Teachers'] is not None:
            teachers = AllResearchLinesSerializer.to_dict_teachers(
                query['Teachers'])
        if query['Tipologia'] == 'base':
            return{
                'RLineID': query['id'],
                'RLineDescription': query['descrizione'],
                'RLineResults': query['descr_pubblicaz_prog_brevetto'],
                'RYear': query['anno'],
                'RLineERC0Id': query['ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__erc0_cod'],
                'RLineERC0Name': query['ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description'] if req_lang == "it" or query['ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en'] is None else query['ricerca_erc2_id__ricerca_erc1_id__ricerca_erc0_cod__description_en'],
                'RLineERC1Id': query['ricerca_erc2_id__ricerca_erc1_id__cod_erc1'],
                'RLineERC1Name': query['ricerca_erc2_id__ricerca_erc1_id__descrizione'],
                'RLineErc2ID': query['ricerca_erc2_id__cod_erc2'],
                'RLineErc2Name': query['ricerca_erc2_id__descrizione'],
                'Teachers': teachers,
                'RLineVisibile': query['visibile']
            }
        else:
            return {
                'RLineID': query['id'],
                'RLineDescription': query['descrizione'],
                'RLineResults': query['descr_pubblicaz_prog_brevetto'],
                'RYear': query['anno'],
                'RLineAster2Id': query['ricerca_aster2_id__ricerca_aster1_id'],
                'RLineAster2Name': query['ricerca_aster2_id__descrizione'],
                'Teachers': teachers,
                'RLineVisibile': query['visibile']
            }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q['personale_id__cognome'] + " " + q['personale_id__nome'] + \
                        (" " + q['personale_id__middle_name']
                         if q['personale_id__middle_name'] is not None else "")
            result.append({
                'TeacherID': encrypt(q['personale_id__matricola']) if not q['personale_id__flg_cessato'] else None,
                'TeacherName': full_name,
                'DepartmentName': q['personale_id__ds_sede'],
                'DepartmentCod': q['personale_id__sede'],
            })
        return result


class TeachersSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        full_name = query['cognome'] + " " + query['nome'] + \
            (" " + query['middle_name']
             if query['middle_name'] is not None else "")
        return {
            'TeacherID': encrypt(query['matricola']),
            'TeacherName': full_name,
            'TeacherDepartmentID': query['dip_id'],
            'TeacherDepartmentCod': query['dip_cod'],
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or not query['dip_des_eng'] else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherRoleDescription': query['ds_ruolo_locale'],
            'TeacherSSDCod': query['cd_ssd'],
            'TeacherSSDDescription': query['ds_ssd'],
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or not query['cv_full_eng']  else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or not query['cv_short_eng'] else query['cv_short_eng'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'],
            'ProfileShortDescription': query['ds_profilo_breve'],
        }


class TeacherStudyActivitiesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityCod': query['af_gen_cod'],
            'StudyActivityName': query['af_gen_des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds_id'],
            'StudyActivityCdSCod': query['cds_cod'],
            'StudyActivityRegDidId': query['regdid_id'],
            'StudyActivityCdSName': query['cds_des'] if req_lang == 'it' or query[
                'af__cds__nome_cds_eng'] is None else query['af__cds__nome_cds_eng'],
            'StudyActivityAA': query['aa_off_id'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivityLanguage': query['af__lista_lin_did_af'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['af__freq_obblig_flg'],
            'StudyActivityPartitionCod': query['fat_part_stu_cod'],
            'StudyActivityPartitionDescription': query['fat_part_stu_des'],
            'SingleStudyActivityPartitionCod': query['part_stu_cod'],
            'SingleStudyActivityPartitionDescription': query['part_stu_des'],
            'StudyActivityPartitionType': query['tipo_fat_stu_cod'],
            'StudyActivityPartitionStart': query['part_ini'],
            'StudyActivityPartitionEnd': query['part_fine'],
        }


class TeacherInfoSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        functions = None
        if query["Functions"] is not None:
            functions = TeacherInfoSerializer.to_dict_functions(
                query["Functions"])

        return {
            'TeacherID': encrypt(query['matricola']),
            'TeacherFirstName': query['nome'] + (" " + query['middle_name']
                                                 if query['middle_name'] is not None else ""),
            'TeacherLastName': query['cognome'],
            'TeacherDepartmentID': query['dip_id'],
            'TeacherDepartmentCod': query['dip_cod'],
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or not query['dip_des_eng'] else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherRoleDescription': query['ds_ruolo_locale'],
            'TeacherSSDCod': query['cd_ssd'],
            'TeacherSSDDescription': query['ds_ssd'],
            'TeacherOffice': query['ds_aff_org'],
            'ORCID': query['ORCID'],
            'PhotoPath': build_media_path(query['PHOTOPATH']),
            'CVPathIta': build_media_path(query['PATHCVITA']),
            'CVPathEn': build_media_path(query['PATHCVENG']),
            'ShortBio': query['BREVEBIO'] if req_lang == "it" or not query['BREVEBIOENG'] else query['BREVEBIOENG'],
            'ReceptionHours': query['ORARIORICEVIMENTO'] if req_lang == "it" or not query['ORARIORICEVIMENTOEN'] else query['ORARIORICEVIMENTOEN'],
            'TeacherOfficeReference': query['Riferimento Ufficio'] if 'Riferimento Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherEmail': query['Posta Elettronica'] if 'Posta Elettronica' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherPEC': query['POSTA ELETTRONICA CERTIFICATA'] if 'POSTA ELETTRONICA CERTIFICATA' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherTelOffice': query['Telefono Ufficio'] if 'Telefono Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherTelCelOffice': query['Telefono Cellulare Ufficio'] if 'Telefono Cellulare Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherFax': query['Fax'] if 'Fax' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherWebSite': query['URL Sito WEB'] if 'URL Sito WEB' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherCV': query['URL Sito WEB Curriculum Vitae'] if 'URL Sito WEB Curriculum Vitae' in PERSON_CONTACTS_TO_TAKE else [],
            'TeacherFunctions': functions,
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or not query['cv_full_eng'] else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or not query['cv_short_eng'] else query['cv_short_eng'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'],
            'ProfileShortDescription': query['ds_profilo_breve'],
        }

    @staticmethod
    def to_dict_functions(query): # pragma: no cover
        functions = []
        for q in query:
            functions.append({
                'TeacherRole': q['ds_funzione'],
                'StructureCod': q['cd_csa__uo'],
                'StructureName': q['cd_csa__denominazione'],
            })
        return functions

    @staticmethod
    def to_dict_board(query, req_lang='en'): # pragma: no cover
        board = []
        for q in query:
            board.append({
                'Title': q['titolo'] if req_lang == "it" or not q['titolo_en'] else q['titolo_en'],
                'TextType': q['tipo_testo'] if req_lang == "it" or not q['tipo_testo_en'] else q['tipo_testo_en'],
                'Text': q['testo'] if req_lang == "it" or not q['testo_en'] else q['testo_en'],
                'TextUrl': q['url_testo'] if req_lang == "it" or not q['url_testo_en'] else q['url_testo_en'],
                'Order': q['ordine'],
                'Active': q['attivo'],
                'PublicationDate': q['dt_pubblicazione'],
                'ValidityStartDate': q['dt_inizio_validita'],
                'ValidityEndDate': q['dt_fine_validita'],
            })
        return board


class TeacherMaterialsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
                'ID': query['id'],
                'Title': query['titolo'] if req_lang == "it" or not query['titolo_en'] else query['titolo_en'],
                'Text': query['testo'] if req_lang == "it" or not query['testo_en'] else query['testo_en'],
                'TextUrl': query['url_testo'] if req_lang == "it" or not query['url_testo_en'] else query['url_testo_en'],
                'Order': query['ordine'],
                'Active': query['attivo'],
                'PublicationDate': _get_teacher_obj_publication_date(query),
        }


class TeacherNewsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
                'ID': query['id'],
                'Title': query['titolo'] if req_lang == "it" or not query['titolo_en'] else query['titolo_en'],
                'TextType': query['tipo_testo'] if req_lang == "it" or not query['tipo_testo_en'] else query['tipo_testo_en'],
                'Text': query['testo'] if req_lang == "it" or not query['testo_en'] else query['testo_en'],
                'TextUrl': query['url_testo'] if req_lang == "it" or not query['url_testo_en'] else query['url_testo_en'],
                'Order': query['ordine'],
                'Active': query['attivo'],
                'PublicationDate': _get_teacher_obj_publication_date(query),
        }

class PhdSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'AcademicYear': query['idesse3_ddr__aa_regdid_id'],
            'DepartmentID': query['dip_cod__dip_id'],
            'DepartmentCod': query['dip_cod__dip_cod'],
            'DepartmentName': query['dip_cod__dip_des_it'] if req_lang == "it" or not query['dip_cod__dip_des_eng'] else query['dip_cod__dip_des_eng'],
            'PhdCdsCOD': query['cds_cod'],
            'PhdCdsName': query['cdsord_des'],
            'PhdRegID': query['idesse3_ddr__regdid_id_esse3'],
            'PhdRegCOD': query['idesse3_ddr__regdid_cod'],
            'PhdCdSDuration': query['durata_anni'],
            'PhdCdSECTS': query['valore_min'],
            'PhdCdSAttendance': query['idesse3_ddr__frequenza_obbligatoria'],
            'CourseType': query['tipo_corso_cod'],
            'CourseName': query['tipo_corso_des'],
            'CycleNumber': query['idesse3_ddr__num_ciclo'],
            'StudyPlanCOD': query['idesse3_ddpds__pds_cod'],
            'StudyPlanDes': query['idesse3_ddpds__pds_des'],
        }


class DegreeTypesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'CourseType': query['tipo_corso_cod'],
            'CourseTypeDescription': query['tipo_corso_des'],
        }


class DepartmentSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'DepartmentID': query['dip_id'],
            'DepartmentCod': query['dip_cod'],
            'DepartmentName': query['dip_des_it'] if req_lang == "it" or query[
                'dip_des_eng'] is None else query['dip_des_eng'],
            'DepartmentNameShort': query['dip_nome_breve'],
            'DepartmentURL': query['dip_url']
        }


class AddressbookSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en',
                full=False):
        full_name = query['cognome'] + " " + query['nome'] + \
            (" " + query['middle_name']
             if query['middle_name'] is not None else "")

        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(
                query["Roles"], full)

        return {
            'Name': full_name,
            'ID': encrypt(query['matricola']),
            'Roles': roles,
            'OfficeReference': query['Riferimento Ufficio'] if 'Riferimento Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Email': query['Posta Elettronica'] if 'Posta Elettronica' in PERSON_CONTACTS_TO_TAKE else [],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'] if 'POSTA ELETTRONICA CERTIFICATA' in PERSON_CONTACTS_TO_TAKE else [],
            'TelOffice': query['Telefono Ufficio'] if 'Telefono Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TelCelOffice': query['Telefono Cellulare Ufficio'] if 'Telefono Cellulare Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Fax': query['Fax'] if 'Fax' in PERSON_CONTACTS_TO_TAKE else [],
            'WebSite': query['URL Sito WEB'] if 'URL Sito WEB' in PERSON_CONTACTS_TO_TAKE else [],
            'CV': query['URL Sito WEB Curriculum Vitae'] if 'URL Sito WEB Curriculum Vitae' in PERSON_CONTACTS_TO_TAKE else [],
            # 'Teacher': query['fl_docente'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
            'ProfileShortDescription': query['ds_profilo_breve'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
        }

    @staticmethod
    def to_dict_roles(query, full=False):
        roles = []
        for q in query:
            d_data = {
                'Role': q['cd_ruolo'],
                'RoleDescription': q['ds_ruolo'],
                'Priority': q['priorita'],
                'StructureCod': q['cd_uo_aff_org'],
                'Structure': q['ds_aff_org'],
                'StructureTypeCOD': q['cd_tipo_nodo'],
            }
            if full:
                d_data['Start'] = q['dt_rap_ini']
            roles.append(d_data)
        return roles


class AddressbookFullSerializer(AddressbookSerializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower(),
                                 True))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en',
                full=False):
        full_name = query['nome'] + \
            (" " + query['middle_name']
             if query['middle_name'] is not None else "")

        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(
                query["Roles"], full)

        return {
            'Name': full_name,
            'Surname': query['cognome'],
            'ID': query['matricola'],
            'Taxpayer_ID': query['cod_fis'],
            'Roles': roles,
            'OfficeReference': query['Riferimento Ufficio'] if 'Riferimento Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Email': query['Posta Elettronica'] if 'Posta Elettronica' in PERSON_CONTACTS_TO_TAKE else [],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'] if 'POSTA ELETTRONICA CERTIFICATA' in PERSON_CONTACTS_TO_TAKE else [],
            'TelOffice': query['Telefono Ufficio'] if 'Telefono Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TelCelOffice': query['Telefono Cellulare Ufficio'] if 'Telefono Cellulare Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Fax': query['Fax'] if 'Fax' in PERSON_CONTACTS_TO_TAKE else [],
            'WebSite': query['URL Sito WEB'] if 'URL Sito WEB' in PERSON_CONTACTS_TO_TAKE else [],
            'CV': query['URL Sito WEB Curriculum Vitae'] if 'URL Sito WEB Curriculum Vitae' in PERSON_CONTACTS_TO_TAKE else [],
            # 'Teacher': query['fl_docente'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
            'ProfileShortDescription': query['ds_profilo_breve'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
        }


class PersonaleSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en', full=False):
        middle_name = f" {query['middle_name']} " if query['middle_name'] else " "
        full_name = f"{query['nome']}{middle_name}{query['cognome']}"
        functions = None
        if query["Functions"] is not None:
            functions = PersonaleSerializer.to_dict_functions(
                query["Functions"])
        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(
                query["Roles"], full)

        return {
            'Name': full_name,
            'ID': encrypt(query['matricola']),
            'Roles': roles,
            'OfficeReference': query['Riferimento Ufficio'] if 'Riferimento Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Email': query['Posta Elettronica'] if 'Posta Elettronica' in PERSON_CONTACTS_TO_TAKE else [],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'] if 'POSTA ELETTRONICA CERTIFICATA' in PERSON_CONTACTS_TO_TAKE else [],
            'TelOffice': query['Telefono Ufficio'] if 'Telefono Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TelCelOffice': query['Telefono Cellulare Ufficio'] if 'Telefono Cellulare Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Fax': query['Fax'] if 'Faxe' in PERSON_CONTACTS_TO_TAKE else [],
            'WebSite': query['URL Sito WEB'] if 'URL Sito WEB' in PERSON_CONTACTS_TO_TAKE else [],
            'CV': query['URL Sito WEB Curriculum Vitae'] if 'URL Sito WEB Curriculum Vitae' in PERSON_CONTACTS_TO_TAKE else [],
            'Teacher': query['fl_docente'] or query['cop_teacher'],
            'PersonFunctions': functions,
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or not query['cv_full_eng'] else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or not query['cv_short_eng'] else query['cv_short_eng'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
            'ProfileShortDescription':query['ds_profilo_breve'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
        }

    @staticmethod
    def to_dict_functions(query):
        functions = []
        for q in query:
            functions.append({
                'TeacherRole': q['ds_funzione'],
                'FunctionCod': q['funzione'],
                'StructureCod': q['cd_csa__uo'],
                'StructureName': q['cd_csa__denominazione'],
            })
        return functions


class PersonaleFullSerializer(PersonaleSerializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower(),
                                 True))
        return data

    @staticmethod
    def to_dict(query, req_lang='en', full=False):
        middle_name = f" {query['middle_name']} " if query['middle_name'] else " "
        full_name = f"{query['nome']}{middle_name}"
        functions = None
        if query["Functions"] is not None:
            functions = PersonaleSerializer.to_dict_functions(
                query["Functions"])
        roles = None
        if query["Roles"] is not None:
            roles = AddressbookSerializer.to_dict_roles(
                query["Roles"], full)

        return {
            'Name': full_name,
            'Surname': query['cognome'],
            'ID': query['matricola'],
            'Taxpayer_ID': query['cod_fis'],
            'Roles': roles,
            'OfficeReference': query['Riferimento Ufficio'] if 'Riferimento Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Email': query['Posta Elettronica'] if 'Posta Elettronica' in PERSON_CONTACTS_TO_TAKE else [],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'] if 'POSTA ELETTRONICA CERTIFICATA' in PERSON_CONTACTS_TO_TAKE else [],
            'TelOffice': query['Telefono Ufficio'] if 'Telefono Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'TelCelOffice': query['Telefono Cellulare Ufficio'] if 'Telefono Cellulare Ufficio' in PERSON_CONTACTS_TO_TAKE else [],
            'Fax': query['Fax'] if 'Faxe' in PERSON_CONTACTS_TO_TAKE else [],
            'WebSite': query['URL Sito WEB'] if 'URL Sito WEB' in PERSON_CONTACTS_TO_TAKE else [],
            'CV': query['URL Sito WEB Curriculum Vitae'] if 'URL Sito WEB Curriculum Vitae' in PERSON_CONTACTS_TO_TAKE else [],
            'Teacher': query['fl_docente'] or query['cop_teacher'],
            'PersonFunctions': functions,
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or not query['cv_full_eng'] else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or not query['cv_short_eng'] else query['cv_short_eng'],
            'ProfileId': query['profilo'],
            'ProfileDescription': query['ds_profilo'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
            'ProfileShortDescription':query['ds_profilo_breve'] if query['profilo'] in ALLOWED_PROFILE_ID else None,
        }


class StructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        d = {
            'StructureCod': query['uo'],
            'StructureName': query['denominazione'],
            'StructureTypeName': query['ds_tipo_nodo'],
            'StructureTypeCOD': query['cd_tipo_nodo'],
        }
        if 'dip_url' in query:
            d['StructureURL'] = query['dip_url']
        if 'childs' in query:
            d['StructureChilds'] = query.get('childs', [])
        return d


class StructureTypesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'StructureTypeName': query['ds_tipo_nodo'],
            'StructureTypeCOD': query['cd_tipo_nodo'],
        }


class AddressbookStructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance): # pragma: no cover
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'StructureCod': query['uo'],
            'StructureName': query['denominazione'],
            'StructureTypeName': query['cd_tipo_nodo'],
            'StructureTypeCOD': query['ds_tipo_nodo'],
        }


class AcademicYearsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'AcademicYear': query['aa_reg_did']
        }


class RolesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'Role': query['cd_ruolo'],
            'RoleDescription': query['ds_ruolo_locale'],
        }


class StructureDetailSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        personnel_functions = None
        if query['FunzioniPersonale'] is not None:
            personnel_functions = StructureDetailSerializer.to_dict_personnel_functions(
                query['FunzioniPersonale'])
        return {
            'StructureCod': query['uo'],
            'StructureName': query['denominazione'],
            'StructureTypeName': query['ds_tipo_nodo'],
            'StructureTypeCOD': query['cd_tipo_nodo'],
            'StructureFatherId': query['uo_padre'],
            'StructureFatherName': query['denominazione_padre'],
            'StructureEmail': query['EMAIL'],
            'StructurePec': query['PEC'],
            'StructureTfr': query['TFR'],
            'StructurePersonnelFunctions': personnel_functions,
            'StructureMission': query['ds_mission'],
            'StructureURL': query['dip_url']

        }

    @staticmethod
    def to_dict_personnel_functions(query):
        result = []
        for q in query:
            if q['cod_fis__matricola'] is None:
                full_name = None
            else:
                full_name = q['cod_fis__cognome'] + " " + q['cod_fis__nome'] + \
                    (" " + q['cod_fis__middle_name']
                     if q['cod_fis__middle_name'] is not None else "")
            result.append({
                'ID': encrypt(q['cod_fis__matricola']),
                'Name': full_name,
                'Function': q['ds_funzione'],
                'FunctionCod': q['funzione'],
            })
        return result


class LaboratoryDetailSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        erc0 = LaboratoryDetailSerializer.to_dict_erc0(query['LaboratoryErc1'], req_lang)
        research_personnel = LaboratoryDetailSerializer.to_dict_research_personnel(
            query['ResearchPersonnel'])
        tech_personnel = LaboratoryDetailSerializer.to_dict_tech_personnel(
            query['TechPersonnel'])
        offered_services = LaboratoryDetailSerializer.to_dict_offered_services(
            query['OfferedServices'])
        scopes = LaboratoryDetailSerializer.to_dict_scopes(query['Scopes'])
        if query['Location'] is None:
            location = None
        else:
            location = LaboratoryDetailSerializer.to_dict_location(
                query['Location'])
        extra_departments = LaboratoriesSerializer.to_dict_extra_departments(
            query['ExtraDepartments'], req_lang)

        return {
            'LaboratoryId': query['id'],
            'CompletionReferentId': encrypt(query['matricola_referente_compilazione']),
            'CompletionReferentName': query['referente_compilazione'],
            'ScientificDirectorId': encrypt(query['matricola_responsabile_scientifico']),
            'ScientificDirectorName': query['responsabile_scientifico'],
            'LaboratoryName': query['nome_laboratorio'],
            'LaboratoryAcronym': query['acronimo'],
            'LaboratoryLogo': build_media_path(query['nome_file_logo']),
            'LaboratoryEquipment': query['strumentazione_descrizione'],
            'DepartmentReferentId': query['id_dipartimento_riferimento__dip_id'],
            'DepartmentReferentCod': query['id_dipartimento_riferimento__dip_cod'],
            'DepartmentReferentName': query['id_dipartimento_riferimento__dip_des_it'] if req_lang == "it" or query['id_dipartimento_riferimento__dip_des_eng'] is None else query['id_dipartimento_riferimento__dip_des_eng'],
            'InfrastructureId': query['id_infrastruttura_riferimento__id'],
            'InfrastructureName': query['id_infrastruttura_riferimento__descrizione'],
            'Interdepartmental': query['laboratorio_interdipartimentale'],
            'ExtraDepartments': extra_departments,
            'LaboratoryScope': query['ambito'],
            'LaboratoryServicesScope': query['finalita_servizi_it'] if req_lang == "it" or query['finalita_servizi_en'] is None else query['finalita_servizi_en'],
            'LaboratoryResearchScope': query['finalita_ricerca_it'] if req_lang == "it" or query['finalita_ricerca_en'] is None else query['finalita_ricerca_en'],
            'LaboratoryTeachingScope': query['finalita_didattica_it'] if req_lang == "it" or query['finalita_didattica_en'] is None else query['finalita_didattica_en'],
            'LaboratoryScopes': scopes,
            'LaboratoryErc1': erc0,
            'LaboratoryResearchPersonnel': research_personnel,
            'LaboratoryTechPersonnel': tech_personnel,
            'LaboratoryOfferedServices': offered_services,
            'LaboratoryLocation': location,
            'LaboratoryURL': query['sito_web'],
            'Visible': query['visibile'],
        }

    @staticmethod
    def to_dict_scopes(query, lang='en'):
        result = []
        for q in query:
            result.append({'ScopeID': q['id_tipologia_attivita__id'],
                           'ScopeDescription': q["id_tipologia_attivita__descrizione"]})
        return result

    @staticmethod
    def to_dict_erc0(query, req_lang='en'):
        result = []
        for q in query:
            result.append({
                'IdErc0': q['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod'],
                'Description': q['id_ricerca_erc1__ricerca_erc0_cod__description']
                if req_lang == "it" or q['id_ricerca_erc1__ricerca_erc0_cod__description_en'] is None else q[
                    'id_ricerca_erc1__ricerca_erc0_cod__description_en'],
                'Erc1List': LaboratoryDetailSerializer.to_dict_erc1_list(q['Erc1'], req_lang),
            })
        return result

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):

        result = []

        for q in query:
            result.append({
                'IdErc1': q['id_ricerca_erc1__cod_erc1'],
                'Description': q['id_ricerca_erc1__descrizione'],

            })
        return result


    @staticmethod
    def to_dict_research_personnel(query):
        result = []
        for q in query:
            if q['matricola_personale_ricerca__matricola'] is None:
                full_name = None
            else:
                full_name = q['matricola_personale_ricerca__cognome'] + " " + q['matricola_personale_ricerca__nome'] + \
                    (" " + q['matricola_personale_ricerca__middle_name']
                     if q['matricola_personale_ricerca__middle_name'] is not None else "")
            result.append({
                'ResearchPersonnelID': encrypt(q['matricola_personale_ricerca__matricola']),
                'ResearchPersonnelName': full_name,
            })
        return result

    @staticmethod
    def to_dict_tech_personnel(query):
        result = []
        for q in query:
            if q['matricola_personale_tecnico__matricola'] is None:
                full_name = None
            else:
                full_name = q['matricola_personale_tecnico__cognome'] + " " + q['matricola_personale_tecnico__nome'] + \
                    (" " + q['matricola_personale_tecnico__middle_name']
                     if q['matricola_personale_tecnico__middle_name'] is not None else "")
            result.append({
                'TechPersonnelID': encrypt(q['matricola_personale_tecnico__matricola']),
                'TechPersonnelName': full_name,
                'TechPersonnelRole': q['ruolo'],
            })
        return result

    @staticmethod
    def to_dict_offered_services(query):
        result = []
        for q in query:
            result.append({
                'ServiceName': q['nome_servizio'],
                'ServiceDescription': q['descrizione_servizio'],
            })
        return result

    @staticmethod
    def to_dict_location(query):
        result = {
            'LocationBuilding': query['edificio'],
            'LocationFloor': query['piano'],
            'LocationNotes': query['note'],
        }
        return result


class LaboratoriesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        extra_departments = LaboratoriesSerializer.to_dict_extra_departments(
            query['ExtraDepartments'], req_lang)
        research_personnel = LaboratoriesSerializer.to_dict_research_personnel(
            query['ResearchPersonnel'])
        tech_personnel = LaboratoriesSerializer.to_dict_tech_personnel(
            query['TechPersonnel'])
        scopes = LaboratoriesSerializer.to_dict_scopes(
            query['Scopes'])

        return {
            'LaboratoryId': query['id'],
            'LaboratoryName': query['nome_laboratorio'],
            'LaboratoryAcronym': query['acronimo'],
            'LaboratoryLogo': build_media_path(query['nome_file_logo']),
            'Area': query['ambito'],
            'DepartmentName': query['dipartimento_riferimento'],
            'DepartmentReferentId': query['id_dipartimento_riferimento__dip_id'],
            'DepartmentReferentCod': query['id_dipartimento_riferimento__dip_cod'],
            'Interdepartmental': query['laboratorio_interdipartimentale'],
            'ExtraDepartments': extra_departments,
            'InfrastructureId': query['id_infrastruttura_riferimento__id'],
            'InfrastructureName': query['id_infrastruttura_riferimento__descrizione'],
            'Dimension': query['sede_dimensione'],
            'ScientificDirector': query['responsabile_scientifico'],
            'ScientificDirectorId': encrypt(query['matricola_responsabile_scientifico']),
            'LaboratoryResearchPersonnel': research_personnel,
            'LaboratoryScopes': scopes,
            'LaboratoryTechPersonnel': tech_personnel,
            'LaboratoryServicesScope': query['finalita_servizi_it'] if req_lang == "it" or query[
                'finalita_servizi_en'] is None else query['finalita_servizi_en'],
            'LaboratoryResearchScope': query['finalita_ricerca_it'] if req_lang == "it" or query[
                'finalita_ricerca_en'] is None else query['finalita_ricerca_en'],
            'LaboratoryTeachingScope': query['finalita_didattica_it'] if req_lang == "it" or query[
                'finalita_didattica_en'] is None else query['finalita_didattica_en'],
            'Visible': query['visibile'],
        }

    @staticmethod
    def to_dict_extra_departments(query, lang='en'):
        result = []
        for q in query:
            result.append({'DepartmentID': q['id_dip__dip_cod'], 'DepartmentName': q["id_dip__dip_des_it"]
                          if lang == "it" or q['id_dip__dip_des_eng'] is None else q["id_dip__dip_des_eng"], })
        return result

    @staticmethod
    def to_dict_scopes(query, lang='en'):
        result = []
        for q in query:
            result.append({'ScopeID': q['id_tipologia_attivita__id'], 'ScopeDescription': q["id_tipologia_attivita__descrizione"]})
        return result

    @staticmethod
    def to_dict_research_personnel(query):
        result = []
        for q in query:
            if q['matricola_personale_ricerca__matricola'] is None:
                full_name = None
            else:
                full_name = q['matricola_personale_ricerca__cognome'] + " " + q['matricola_personale_ricerca__nome'] + \
                    (" " + q['matricola_personale_ricerca__middle_name']
                     if q['matricola_personale_ricerca__middle_name'] is not None else "")
            result.append({
                'ResearchPersonnelID': encrypt(q['matricola_personale_ricerca__matricola']),
                'ResearchPersonnelName': full_name,
            })
        return result

    @staticmethod
    def to_dict_tech_personnel(query):
        result = []
        for q in query:
            if q['matricola_personale_tecnico__matricola'] is None:
                full_name = None
            else:
                full_name = q['matricola_personale_tecnico__cognome'] + " " + q['matricola_personale_tecnico__nome'] + \
                    (" " + q['matricola_personale_tecnico__middle_name']
                     if q['matricola_personale_tecnico__middle_name'] is not None else "")
            result.append({
                'TechPersonnelID': encrypt(q['matricola_personale_tecnico__matricola']),
                'TechPersonnelName': full_name,
                'TechPersonnelRole': q['ruolo'],
            })
        return result


class LaboratoriesAreasSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'Area': query['ambito'],
        }


class LaboratoriesScopesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'ScopeID': query['id'],
            'ScopeDescription': query['descrizione'],
        }


class Erc1Serializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        erc1 = Erc1Serializer.to_dict_erc1_list(query['Erc1'], req_lang)

        return {
            'IdErc0': query['erc0_cod'],
            'Description': query['description']
            if req_lang == "it" or query['description_en'] is None else query[
                'description_en'],
            'Erc1List': erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):

        result = []

        for q in query:
            result.append({
                'IdErc1': q['cod_erc1'],
                'Description': q['descrizione'],
            })

        return result


class Erc0Serializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {'IdErc0': query['erc0_cod'], 'Description': query['description']
                if req_lang == "it" or query['description_en'] is None else query['description_en']}


class Erc2Serializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        erc1 = Erc2Serializer.to_dict_erc1_list(query['Erc1'], req_lang)

        return {
            'IdErc0': query['erc0_cod'],
            'Description': query['description']
            if req_lang == "it" or query['description_en'] is None else query[
                'description_en'],
            'Erc1List': erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append({
                'IdErc1': q['cod_erc1'],
                'Description': q['descrizione'],
                'Erc2List': Erc2Serializer.to_dict_erc2_list(q['Erc2'], req_lang),
            })
        return result

    @staticmethod
    def to_dict_erc2_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append({
                'CodErc2': q['cod_erc2'],
                'Description': q['descrizione'],
            })
        return result


class PublicationSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        authors = None
        if query.get('Authors') is not None:
            authors = PublicationSerializer.to_dict_authors(
                query['Authors'])
        return {
            'PublicationId': query['item_id'],
            'PublicationTitle': query['title'],
            'PublicationAbstract': query['des_abstract'] if req_lang == "it" or query['des_abstracteng'] is None else query['des_abstracteng'],
            'PublicationCollection': query['collection_id__collection_name'],
            'PublicationCommunity': query['collection_id__community_id__community_name'],
            'Publication': query['pubblicazione'],
            'PublicationLabel': query['label_pubblicazione'],
            'PublicationContributors': query['contributors'],
            'PublicationYear': query['date_issued_year'],
            'PublicationAuthors': authors,
            'PublicationUrl': query['url_pubblicazione'],
        }

    @staticmethod
    def to_dict_authors(query):
        result = []
        for q in query:
            if q['id_ab__matricola'] is None:
                full_name = q['last_name'] + " " + q['first_name']
            else:
                full_name = q['id_ab__cognome'] + " " + q['id_ab__nome'] + \
                    (" " + q['id_ab__middle_name']
                     if q['id_ab__middle_name'] is not None else "")
            result.append({
                'AuthorId': encrypt(q['id_ab__matricola']),
                'AuthorName': full_name,
            })
        return result


class PublicationsSerializer(PublicationSerializer):

    @staticmethod
    def to_dict(query, req_lang='en'):
        response = PublicationSerializer.to_dict(query, req_lang)
        response.pop('PublicationAuthors')
        return response


class PublicationsCommunityTypesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'CommunityId': query['community_id'],
            'CommunityName': query['community_name'],
        }


class InfrastructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'InfrastructureId': query['id'],
            'InfrastructureDescription': query['descrizione'],
        }


class PatentsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        inventors = None
        if query.get('Inventori') is not None:
            inventors = PatentsSerializer.to_dict_inventors(
                query['Inventori'])
        return {
            'PatentId': query['id'],
            'PatentUniqueId': query['id_univoco'],
            'PatentTitle': query['titolo'],
            'PatentImage': build_media_path(query['nome_file_logo']),
            'PatentAbstract': query["breve_descrizione"],
            'PatentUrlKnowledgeShare': query["url_knowledge_share"],
            'PatentInizialTRL': query["trl_iniziale"],
            'PatentUpdatedTRL': query["trl_aggiornato"],
            'PatentEnhancement': query["valorizzazione"],
            'PatentTechAreaId': query["id_area_tecnologica"],
            'PatentAreaDescription': query["id_area_tecnologica__descr_area_ita"] if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None else query['id_area_tecnologica__descr_area_eng'],
            'PatentInventors': inventors,
            'PatentIsActive': query['is_active']
        }

    @staticmethod
    def to_dict_inventors(query):
        result = []
        for q in query:
            full_name = q["cognomenome_origine"]
            result.append({
                'AuthorId': encrypt(q['matricola_inventore']),
                'AuthorName': full_name,
            })
        return result


class CompaniesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'SpinoffId': query['id'],
            'SpinoffPIva': query['piva'],
            'SpinoffAgencyName': query['nome_azienda'],
            'SpinoffAgencyUrl': query['url_sito_web'],
            'SpinoffImage': build_media_path(query['nome_file_logo']),
            'SpinoffDescription': query["descrizione_ita"]if req_lang == "it" or query["descrizione_eng"] is None else query['descrizione_eng'],
            'SpinoffUnicalReferent': query["referente_unical"],
            'SpinoffUnicalReferentId': encrypt(query['matricola_referente_unical']),
            'TechAreaId': query["id_area_tecnologica"],
            'TechAreaDescription': query["id_area_tecnologica__descr_area_ita"] if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None else query['id_area_tecnologica__descr_area_eng'],
            'IsSpinoff': query['is_spinoff'],
            'IsStartup': query['is_startup'],
            'IsActive': query['is_active']
        }


class TechAreasSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {'TechAreaId': query['id'], 'TechAreaDescription': query["descr_area_ita"]
                if req_lang == "it" or query["descr_area_eng"] is None else query['descr_area_eng'], }


class ProjectSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        responsabili = None
        ricercatori = None
        if query.get('Responsabili') is not None:
            responsabili = ProjectSerializer.to_dict_directors(
                query['Responsabili'])
        if query.get('Ricercatori') is not None:
            ricercatori = ProjectSerializer.to_dict_researchers(
                query['Ricercatori'])
        return {
            'ProjectId': query['id'],
            'ProjectYear': query['anno_avvio'],
            'InfrastructureId': query['uo'],
            'InfrastructureDescription': query['uo__denominazione'],
            'TerritorialScopeId': query['id_ambito_territoriale__id'],
            'TerritorialScopeDescription': query['id_ambito_territoriale__ambito_territoriale'],
            'TypeProgramId': query['id_tipologia_programma__id'],
            'TypeProgramDescription': query['id_tipologia_programma__nome_programma'],
            'ProjectTitle': query['titolo'],
            'ProjectDescription': query['descr_breve'],
            'ProjectAbstract': query['abstract_ita'] if req_lang == "it" or query['abstract_eng'] is None else query['abstract_eng'],
            'TechAreaId': query["id_area_tecnologica"],
            'TechAreaDescription': query["id_area_tecnologica__descr_area_ita"] if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None else query['id_area_tecnologica__descr_area_eng'],
            'ProjectImage': query['url_immagine'],
            'ScientificDirectors': responsabili,
            'Researchers': ricercatori,
            'IsActive': query['is_active']
        }

    @staticmethod
    def to_dict_directors(query):
        result = []
        for q in query:
            full_name = q["nome_origine"]
            result.append({
                'ScientificDirectorId': encrypt(q['matricola']),
                'ScientificDirectorName': full_name,
            })
        return result

    @staticmethod
    def to_dict_researchers(query):
        result = []
        for q in query:
            full_name = q["nome_origine"]
            result.append({
                'ResearcherId': encrypt(q['matricola']),
                'ResearcherName': full_name,
            })
        return result


class StructureFunctionsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'StructureTypeCOD': query['cd_tipo_nod'],
            'Function': query['funzione'],
            'FunctionDescription': query['descr_funzione'],
        }


class TerritorialScopesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'TerritorialScopeId': query['id'],
            'TerritorialScopeDescription': query['ambito_territoriale'],
        }


class ProgramTypesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'TypeProgramId': query['id'],
            'TypeProgramDescription': query['nome_programma'],
        }


class CdsAreasSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'AreaCds': query['area_cds'] if req_lang=='it' or query['area_cds_en'] is None else query['area_cds_en'],
        }


class ProjectInfrastructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'InfrastructureId': query['uo'],
            'InfrastructureDescription': query['uo__denominazione'],
        }


class PersonnelCfSerializer(CreateUpdateAbstract):

    def to_representation(self, instance): # pragma: no cover
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        full_name = query['cognome'] + " " + query['nome'] + \
                    (" " + query['middle_name']
                     if query['middle_name'] is not None else "") # pragma: no cover
        return {
            'Name': full_name,
            'CF': query['cod_fis'],
            'ID': query['matricola'],
            'RoleDescription': query['ds_ruolo_locale'],
            'Role': query['cd_ruolo'],
            'InfrastructureId': query['cd_uo_aff_org'],
            'InfrastructureDescription': query['ds_aff_org'],
        }


class SortingContactsSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        full_name = query['personale__cognome'] + " " + query['personale__nome'] + \
                    (" " + query['personale__middle_name']
                     if query['personale__middle_name'] is not None else "")
        return {
            'Name': full_name,
            'ID': encrypt(query['personale__matricola']),
            'TeacherDepartmentID': query['personale__cd_uo_aff_org'],
            'TeacherOffice': query['personale__ds_aff_org'],
            'DepartmentURL': query['DepartmentUrl'],
        }


class HighFormationMastersSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        # full_name = query['personale__cognome'] + " " + query['personale__nome'] + \
        #             (" " + query['personale__middle_name']
        #              if query['personale__middle_name'] is not None else "")

        partners = None
        if query.get('Partners') is not None:
            partners = HighFormationMastersSerializer.to_dict_partners(
                query['Partners'])

        selections = None
        if query.get('Selections') is not None:
            selections = HighFormationMastersSerializer.to_dict_selections(
                query['Selections'])

        internal_council = None
        if query.get('InternalCouncil') is not None:
            internal_council = HighFormationMastersSerializer.to_dict_internal_council(
                query['InternalCouncil'])

        external_council = None
        if query.get('ExternalCouncil') is not None:
            external_council = HighFormationMastersSerializer.to_dict_external_council(
                query['ExternalCouncil'])

        teaching_plans = None
        if query.get('TeachingPlan') is not None:
            teaching_plans = HighFormationMastersSerializer.to_dict_teachings_plan(
                query['TeachingPlan'])

        teaching_assignments = None
        if query.get('TeachingAssignments') is not None:
            teaching_assignments = HighFormationMastersSerializer.to_dict_teaching_assignments(
                query['TeachingAssignments'])
        return {
            'ID': query['id'],
            'MasterTitle': query['titolo_it'] if req_lang=='it' or query['titolo_en'] is None else query['titolo_en'],
            'HighFormationTypeId': query['id_alta_formazione_tipo_corso'],
            'HighFormationTypeDescription': query['id_alta_formazione_tipo_corso__tipo_corso_descr'],
            'HighFormationErogationMode': query['id_alta_formazione_mod_erogazione'],
            'HighFormationErogationModeDescription': query['id_alta_formazione_mod_erogazione__descrizione'],
            'HighFormationHours': query['ore'],
            'HighFormationMonths': query['mesi'],
            'HighFormationLanguage': query['lingua'],
            'HighFormationCourseStructure': query['sede_corso'],
            'HighFormationMinParticipants': query['num_min_partecipanti'],
            'HighFormationMaxParticipants': query['num_max_partecipanti'],
            'HighFormationMasterYear': query['anno_rilevazione'],
            'DepartmentId': query['id_dipartiento_riferimento'],
            'DepartmentCod': query['id_dipartiento_riferimento__dip_cod'],
            'DepartmentName': query['id_dipartiento_riferimento__dip_des_it'] if req_lang=='it' or query['id_dipartiento_riferimento__dip_des_eng'] is None else query['id_dipartiento_riferimento__dip_des_eng'],
            'ListenersAccepted': query['uditori_ammessi'],
            'MaxListeners': query['num_max_uditori'],
            'AdmissionRequirements': query['requisiti_ammissione'],
            'TitleIssued': query['titolo_rilasciato'],
            'DoubleTitle': query['doppio_titolo'],
            'ScientificDirectorId': encrypt(query['matricola_direttore_scientifico']),
            'ScientificDirectorName': query['nome_origine_direttore_scientifico'],
            'SubscriptionFee': query['quota_iscrizione'],
            'ListenersFee': query['quota_uditori'],
            'WorkFunction': query['funzione_lavoro'],
            'FormationObjectivesSummerSchool': query['obiettivi_formativi_summer_school'],
            'Skills': query['competenze'],
            'JobOpportunities': query['sbocchi_occupazionali'],
            'CourseObjectives': query['obiettivi_formativi_corso'],
            'FinalTestMode': query['modalita_svolgimento_prova_finale'],
            'NumModules': query['numero_moduli'],
            'Internship': query['stage_tirocinio'],
            'InternshipHours': query['ore_stage_tirocinio'],
            'InternshipCFU': query['cfu_stage'],
            'InternshipMonths': query['mesi_stage'],
            'TypeCompaniesInternship': query['tipo_aziende_enti_tirocinio'],
            'ContentTimesCriteriaCFU': query['contenuti_tempi_criteri_cfu'],
            'ProjectWork': query['project_work'],
            'HighFormationMasterPartners': partners,
            'HighFormationMasterSelectionModes': selections,
            'HighFormationMasterInternalCouncil': internal_council,
            'HighFormationMasterExternalCouncil': external_council,
            'HighFormationMasterTeachingPlans': teaching_plans,
            'HighFormationMasterTeachingAssignments': teaching_assignments,

        }

    @staticmethod
    def to_dict_partners(query):
        result = []
        for q in query:
            result.append({
                'PartnerId': q['id'],
                'PartnerDenomination': q['denominazione'],
                'PartnerType': q['tipologia'],
                'PartnerURL': q['sito_web']
            })
        return result

    @staticmethod
    def to_dict_selections(query):
        result = []
        for q in query:
            result.append({
                'SelectionId': q['id'],
                'SelectionType': q['tipo_selezione']
            })
        return result

    @staticmethod
    def to_dict_internal_council(query):
        result = []
        for q in query:
            full_name = q["nome_origine_cons"]
            result.append({
                'PersonId': encrypt(q['matricola_cons']),
                'PersonName': full_name,
            })
        return result

    @staticmethod
    def to_dict_external_council(query):
        result = []
        for q in query:
            full_name = q["nome_cons"]
            result.append({
                'PersonName': full_name,
                'Role': q['ruolo_cons'],
                'Institution': q['ente_cons']
            })
        return result

    @staticmethod
    def to_dict_teachings_plan(query):
        result = []
        for q in query:
            result.append({
                'TeachingPlanModule': q['modulo'],
                'TeachingPlanSSD': q['ssd'],
                'TeachingPlanHours': q['num_ore'],
                'TeachingPlanCFU': q['cfu'],
                'TeachingPlanFinalTest': q['verifica_finale']
            })
        return result

    @staticmethod
    def to_dict_teaching_assignments(query):
        result = []
        for q in query:
            result.append({
                'TeachingAssignmentsModule': q['modulo'],
                'TeachingAssignmentsHours': q['num_ore'],
                'TeachingAssignmentsTeachers': q['docente'],
                'TeachingAssignmentsQualification': q['qualifica'],
                'TeachingAssignmentsInstitution': q['ente'],
                'TeachingAssignmentsType': q['tipologia'],
            })
        return result



class ErogationModesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'ID': query['id'],
            'Description': query['descrizione']
        }


class HighFormationCourseTypesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'ID': query['id'],
            'Description': query['tipo_corso_descr']
        }


class Asters1Serializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        aster1 = Asters1Serializer.to_dict_aster1_list(query['Aster1'], req_lang)

        return {
            'IdErc0': query['erc0_cod'],
            'Description': query['description'] if req_lang == "it" or query['description_en'] is None else query['description_en'],
            'Aster1List': aster1,
        }

    @staticmethod
    def to_dict_aster1_list(query, req_lang="en"):
        result = []

        for q in query:
            result.append({
                'IdAster1': q['id'],
                'Description': q['descrizione'],
            })

        return result


class Asters2Serializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        aster1 = Asters2Serializer.to_dict_aster1_list(query['Aster1'], req_lang)

        return {
            'IdErc0': query['erc0_cod'],
            'Description': query['description'] if req_lang == "it" or query['description_en'] is None else query['description_en'],
            'Aster1List': aster1,
        }

    @staticmethod
    def to_dict_aster1_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append({
                'IdAster1': q['id'],
                'Description': q['descrizione'],
                'Aster2List': Asters2Serializer.to_dict_aster2_list(q['Aster2'], req_lang),
            })
        return result

    @staticmethod
    def to_dict_aster2_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append({
                'IdAster2': q['id'],
                'Description': q['descrizione'],
            })
        return result


class PhdActivitiesSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        cycle_des = ''
        for cycle in PHD_CYCLES:
            if cycle[0] == query['ciclo']:
                cycle_des = cycle[1]
                break

        main_teachers = None
        if query.get('MainTeachers') is not None:
            main_teachers = PhdActivitiesSerializer.to_dict_teachers(
                query['MainTeachers'])
        other_teachers = None
        if query.get('OtherTeachers') is not None:
            other_teachers = PhdActivitiesSerializer.to_dict_teachers(
                query['OtherTeachers'])

        tipologia = None
        if query['tipologia_obj']:
            tipologia = query['tipologia_obj'].nome_it if req_lang == 'it' or query['tipologia_obj'].nome_en is None else query['tipologia_obj'].nome_en

        return {
            'ID': query['id'],
            'ActivityName': query['nome_af'],
            'SSD': query['ssd'],
            'Hours': query['numero_ore'],
            'CFU': query['cfu'],
            'ActivityType': query['tipo_af'],
            'ActivityTypology': tipologia,
            'ReferentPhd': query['rif_dottorato'],
            'Cycle': cycle_des,
            'ReferentStructureId': query['id_struttura_proponente'],
            'ReferentStructureName': query['struttura_proponente_origine'],
            'ActivityContents': query['contenuti_af'],
            'Prerequisities': query['prerequisiti'],
            'MinStudents': query['num_min_studenti'],
            'MaxStudents': query['num_max_studenti'],
            'FinalTest': query['verifica_finale'],
            'FinalTestMode': query['modalita_verifica'],
            'ActivityStart': query['avvio'],
            'ActivityEnd': query['fine'],
            'ClassroomsTimetable': query['orario_aule'],
            'ShowTimetable': query['visualizza_orario'],
            'Notes': query['note'],
            'MainTeachers': main_teachers,
            'OtherTeachers': other_teachers,
        }

    @staticmethod
    def to_dict_teachers(query):
        result = []
        for q in query:
            full_name = q["cognome_nome_origine"]
            result.append({
                'PersonId': encrypt(q['matricola']),
                'PersonName': full_name,
            })
        return result


class RefPhdSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'ReferentPhd': query['rif_dottorato'],
        }


class RefStructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'ReferentStructureName': query['struttura_proponente_origine'],
        }


class PhdSsdListSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'SSD': query['ssd'],
        }



class PhdActivityTypeSerializer(CreateUpdateAbstract): # pragma: no cover

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):

        return {
            'ActivityType': query['tipo_af'],
        }
