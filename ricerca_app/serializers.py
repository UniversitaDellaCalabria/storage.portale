from rest_framework import serializers
from django.conf import settings
from .utils import encrypt


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
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'RegDidState': query['didatticaregolamento__stato_regdid_cod'],
            'JointDegree': query['didatticaregolamento__titolo_congiunto_cod'],
        }


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
            video = CdsInfoSerializer.to_dict_video(
                query['URL_CDS_VIDEO'])

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
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'CdSIntro': query['INTRO_CDS_FMT'] if query['INTRO_CDS_FMT'] is not None else query['DESC_COR_BRE'],
            'CdSDoc': f'{settings.CDS_BROCHURE_MEDIA_PATH}/{query["URL_CDS_DOC"]}',
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
        }


    @staticmethod
    def to_dict_video(query):
        if 'https' in query or 'http' in query:
            return query
        else:
            query = f'{settings.CDS_BROCHURE_MEDIA_PATH}/{query}'
            return query


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
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
        }


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

        studyactivityborrowed = None
        if query['BorrowedFrom'] is not None:
            studyactivityborrowed = StudyActivityMinimalInfoSerializer.to_dict(
                query['BorrowedFrom'], req_lang)

        studyactivitiesborrowedfromthis = []
        if len(query['ActivitiesBorrowedFromThis']) > 0:
            for q in query['ActivitiesBorrowedFromThis']:
                studyactivitiesborrowedfromthis.append(
                    StudyActivityMinimalInfoSerializer.to_dict(q, req_lang))
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityCod': query['af_gen_cod'],
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_id'],
            'StudyActivityCdSCod': query['cds__cds_cod'],
            'StudyActivityRegDidId': query['regdid__regdid_id'],
            'StudyActivityYear': query['anno_corso'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityECTS': query['peso'],
            'StudyActivitySSD': query['sett_des'],
            'StudyActivityCompulsory': query['freq_obblig_flg'],
            'StudyActivityCdSName': query['cds__nome_cds_it'] if req_lang == 'it' or query['cds__nome_cds_eng'] is None else query['cds__nome_cds_eng'],
            'StudyActivityTeachingUnitType': query['tipo_af_des'],
            'StudyActivityTeacherID': query['StudyActivityTeacherID'],
            'StudyActivityTeacherName': query['StudyActivityTeacherName'],
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
            'StudyActivitiesModules': query['MODULES'],
            'StudyActivityRoot': studyactivityroot,
            'StudyActivityBorrowedFrom': studyactivityborrowed,
            'StudyActivitiesBorrowedFromThis': studyactivitiesborrowedfromthis}


class StudyActivityMinimalInfoSerializer(CreateUpdateAbstract):
    @staticmethod
    def to_dict(query,
                req_lang='en'):
        return {
            'StudyActivityID': query['af_id'],
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivitySemester': query['ciclo_des'],
            'StudyActivityRegDidId': query['regdid__regdid_id'],
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
            'Teachers': teachers
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
            'Teachers': teachers
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
                'Teachers': teachers
            }
        else:
            return {
                'RLineID': query['id'],
                'RLineDescription': query['descrizione'],
                'RLineResults': query['descr_pubblicaz_prog_brevetto'],
                'RYear': query['anno'],
                'RLineAster2Id': query['ricerca_aster2_id__ricerca_aster1_id'],
                'RLineAster2Name': query['ricerca_aster2_id__descrizione'],
                'Teachers': teachers
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
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or query['dip_des_eng'] is None else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherRoleDescription': query['ds_ruolo_locale'],
            'TeacherSSDCod': query['cd_ssd'],
            'TeacherSSDDescription': query['ds_ssd'],
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or query['cv_full_eng'] is None else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or query['cv_short_eng'] is None else query['cv_short_eng'],
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
            'StudyActivityID': query['didatticacopertura__af_id'],
            'StudyActivityCod': query['didatticacopertura__af_gen_cod'],
            'StudyActivityName': query['didatticacopertura__af_gen_des'] if req_lang == 'it' or query['didatticacopertura__af_gen_des_eng'] is None else query['didatticacopertura__af_gen_des_eng'],
            'StudyActivityCdSID': query['didatticacopertura__cds_id'],
            'StudyActivityCdSCod': query['didatticacopertura__cds_cod'],
            'StudyActivityRegDidId': query['didatticacopertura__regdid_id'],
            'StudyActivityCdSName': query['didatticacopertura__cds_des'] if req_lang == 'it' or query[
                'didatticacopertura__af__cds__nome_cds_eng'] is None else query['didatticacopertura__af__cds__nome_cds_eng'],
            'StudyActivityAA': query['didatticacopertura__aa_off_id'],
            'StudyActivityYear': query['didatticacopertura__anno_corso'],
            'StudyActivitySemester': query['didatticacopertura__ciclo_des'],
            'StudyActivityECTS': query['didatticacopertura__peso'],
            'StudyActivityLanguage': query['didatticacopertura__af__lista_lin_did_af'],
            'StudyActivitySSD': query['didatticacopertura__sett_des'],
            'StudyActivityCompulsory': query['didatticacopertura__af__freq_obblig_flg'],
            'StudyActivityPartitionCod': query['didatticacopertura__fat_part_stu_cod'],
            'StudyActivityPartitionDescription': query['didatticacopertura__fat_part_stu_des'],
            'SingleStudyActivityPartitionCod': query['didatticacopertura__part_stu_cod'],
            'SingleStudyActivityPartitionDescription': query['didatticacopertura__part_stu_des'],
            'StudyActivityPartitionType': query['didatticacopertura__tipo_fat_stu_cod'],
            'StudyActivityPartitionStart': query['didatticacopertura__part_ini'],
            'StudyActivityPartitionEnd': query['didatticacopertura__part_fine'],
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
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or query['dip_des_eng'] is None else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherRoleDescription': query['ds_ruolo_locale'],
            'TeacherSSDCod': query['cd_ssd'],
            'TeacherSSDDescription': query['ds_ssd'],
            'TeacherOffice': query['ds_aff_org'],
            'TeacherOfficeReference': query['Riferimento Ufficio'],
            'TeacherEmail': query['Posta Elettronica'],
            'TeacherPEC': query['POSTA ELETTRONICA CERTIFICATA'],
            'TeacherTelOffice': query['Telefono Ufficio'],
            'TeacherTelCelOffice': query['Telefono Cellulare Ufficio'],
            'TeacherFax': query['Fax'],
            'TeacherWebSite': query['URL Sito WEB'],
            'TeacherCV': query['URL Sito WEB Curriculum Vitae'],
            'TeacherFunctions': functions,
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or query['cv_full_eng'] is None else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or query['cv_short_eng'] is None else query['cv_short_eng'],
        }

    @staticmethod
    def to_dict_functions(query):
        functions = []
        for q in query:
            functions.append({
                'TeacherRole': q['ds_funzione'],
                'StructureCod': q['cd_csa__uo'],
                'StructureName': q['cd_csa__denominazione'],
            })
        return functions


class DoctoratesSerializer(CreateUpdateAbstract):

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
            'DepartmentName': query['dip_cod__dip_des_it'] if req_lang == "it" or query['dip_cod__dip_des_eng'] is None else query['dip_cod__dip_des_eng'],
            'DoctorateCdsCOD': query['cds_cod'],
            'DoctorateCdsName': query['cdsord_des'],
            'DoctorateRegID': query['idesse3_ddr__regdid_id_esse3'],
            'DoctorateRegCOD': query['idesse3_ddr__regdid_cod'],
            'DoctorateCdSDuration': query['durata_anni'],
            'DoctorateCdSECTS': query['valore_min'],
            'DoctorateCdSAttendance': query['idesse3_ddr__frequenza_obbligatoria'],
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
                req_lang='en'):
        full_name = query['cognome'] + " " + query['nome'] + \
            (" " + query['middle_name']
             if query['middle_name'] is not None else "")

        return {
            'Name': full_name,
            'ID': encrypt(query['matricola']),
            'RoleDescription': query['ds_ruolo_locale'],
            'Role': query['cd_ruolo'],
            'Structure': query['Struttura'],
            'StructureTypeName': query['TipologiaStrutturaNome'],
            'StructureTypeCOD': query['TipologiaStrutturaCod'],
            'OfficeReference': query['Riferimento Ufficio'],
            'Email': query['Posta Elettronica'],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'],
            'TelOffice': query['Telefono Ufficio'],
            'TelCelOffice': query['Telefono Cellulare Ufficio'],
            'Fax': query['Fax'],
            'WebSite': query['URL Sito WEB'],
            'CV': query['URL Sito WEB Curriculum Vitae'],
            'Teacher': query['fl_docente']
        }


class PersonaleSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        full_name = query['cognome'] + " " + query['nome'] + \
            (" " + query['middle_name']
             if query['middle_name'] is not None else "")
        functions = None
        if query["Functions"] is not None:
            functions = PersonaleSerializer.to_dict_functions(
                query["Functions"])
        return {
            'Name': full_name,
            'ID': encrypt(query['matricola']),
            'RoleDescription': query['ds_ruolo_locale'],
            'Role': query['cd_ruolo'],
            'Structure': query['Struttura'],
            'StructureCod': query['CodStruttura'],
            'StructureTypeName': query['TipologiaStrutturaNome'],
            'StructureTypeCOD': query['TipologiaStrutturaCod'],
            'OfficeReference': query['Riferimento Ufficio'],
            'Email': query['Posta Elettronica'],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'],
            'TelOffice': query['Telefono Ufficio'],
            'TelCelOffice': query['Telefono Cellulare Ufficio'],
            'Fax': query['Fax'],
            'WebSite': query['URL Sito WEB'],
            'CV': query['URL Sito WEB Curriculum Vitae'],
            'Teacher': query['fl_docente'],
            'PersonFunctions': functions,
            'TeacherCVFull': query['cv_full_it'] if req_lang == "it" or query['cv_full_eng'] is None else query['cv_full_eng'],
            'TeacherCVShort': query['cv_short_it'] if req_lang == "it" or query['cv_short_eng'] is None else query['cv_short_eng'],
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


class StructuresSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'StructureCod': query['uo'],
            'StructureName': query['denominazione'],
            'StructureTypeName': query['ds_tipo_nodo'],
            'StructureTypeCOD': query['cd_tipo_nodo'],
            'StructureURL': query['dip_url']
        }


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

    def to_representation(self, instance):
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
        erc1 = Erc1Serializer.to_dict(query['Erc1'][0], req_lang)
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
            'LaboratoryLogo': f'{settings.LABORATORIES_MEDIA_PATH}/{query["nome_file_logo"]}' if query['nome_file_logo'] else '',
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
            'LaboratoryErc1': erc1,
            'LaboratoryResearchPersonnel': research_personnel,
            'LaboratoryTechPersonnel': tech_personnel,
            'LaboratoryOfferedServices': offered_services,
            'LaboratoryLocation': location,
            'LaboratoryURL': query['sito_web'],
        }

    @staticmethod
    def to_dict_scopes(query, lang='en'):
        result = []
        for q in query:
            result.append({'ScopeID': q['id_tipologia_attivita__id'],
                           'ScopeDescription': q["id_tipologia_attivita__descrizione"]})
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
            'LaboratoryLogo': f'{settings.LABORATORIES_MEDIA_PATH}/{query["nome_file_logo"]}' if query['nome_file_logo'] else '',
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
            'IdErc0': query['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod'],
            'Description': query['id_ricerca_erc1__ricerca_erc0_cod__description']
            if req_lang == "it" or query['id_ricerca_erc1__ricerca_erc0_cod__description_en'] is None else query[
                'id_ricerca_erc1__ricerca_erc0_cod__description_en'],
            'Erc1List': erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):

        result = []

        for q in query:
            result.append({
                'IdErc1': q['id_ricerca_erc1__cod_erc1'],
                'Description': q['id_ricerca_erc1__descrizione'],
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
        return {'IdErc0': query['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod'], 'Description': query['id_ricerca_erc1__ricerca_erc0_cod__description']
                if req_lang == "it" or query['id_ricerca_erc1__ricerca_erc0_cod__description_en'] is None else query['id_ricerca_erc1__ricerca_erc0_cod__description_en']}


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
            'IdErc0': query['id_ricerca_erc1__ricerca_erc0_cod__erc0_cod'],
            'Description': query['id_ricerca_erc1__ricerca_erc0_cod__description']
            if req_lang == "it" or query['id_ricerca_erc1__ricerca_erc0_cod__description_en'] is None else query[
                'id_ricerca_erc1__ricerca_erc0_cod__description_en'],
            'Erc1List': erc1,
        }

    @staticmethod
    def to_dict_erc1_list(query, req_lang="en"):
        result = []
        for q in query:
            result.append({
                'IdErc1': q['id_ricerca_erc1__cod_erc1'],
                'Description': q['id_ricerca_erc1__descrizione'],
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
            'PatentImage': f'{settings.PATENTS_MEDIA_PATH}/{query["nome_file_logo"]}' if query['nome_file_logo'] else '',
            'PatentAbstract': query["breve_descrizione"],
            'PatentUrlKnowledgeShare': query["url_knowledge_share"],
            'PatentTechAreaId': query["id_area_tecnologica"],
            'PatentAreaDescription': query["id_area_tecnologica__descr_area_ita"] if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None else query['id_area_tecnologica__descr_area_eng'],
            'PatentInventors': inventors,
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
            'SpinoffImage': f'{settings.COMPANIES_MEDIA_PATH}/{query["nome_file_logo"]}' if query['nome_file_logo'] else '',
            'SpinoffDescription': query["descrizione_ita"]if req_lang == "it" or query["descrizione_eng"] is None else query['descrizione_eng'],
            'SpinoffUnicalReferent': query["referente_unical"],
            'SpinoffUnicalReferentId': encrypt(query['matricola_referente_unical']),
            'TechAreaId': query["id_area_tecnologica"],
            'TechAreaDescription': query["id_area_tecnologica__descr_area_ita"] if req_lang == "it" or query["id_area_tecnologica__descr_area_eng"] is None else query['id_area_tecnologica__descr_area_eng'],
            'IsSpinoff': query['is_spinoff'],
            'IsStartup': query['is_startup'],
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
            'HighFormationErogationMode': query['id_alta_formazione_mod_erogazione'],
            'HighFormationHours': query['ore'],
            'HighFormationMonths': query['mesi'],
            'HighFormationCourseStructure': query['sede_corso'],
            'HighFormationMinParticipants': query['num_min_partecipanti'],
            'HighFormationMaxParticipants': query['num_max_partecipanti'],
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


class CourseTypesSerializer(CreateUpdateAbstract):

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