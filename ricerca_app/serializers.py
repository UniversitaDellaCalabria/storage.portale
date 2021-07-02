from rest_framework import serializers


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


class CdSListSerializer(CreateUpdateAbstract):
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
            langs.append(q['didatticacdslingua__lingua_des_it'] if req_lang ==
                         'it' or q['didatticacdslingua__lingua_des_eng'] is None else q['didatticacdslingua__lingua_des_eng'])
        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'CdSId': query['cds_cod'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseClassId': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'RegDidState': query['didatticaregolamento__stato_regdid_cod'],
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

        return {
            'RegDidId': query['didatticaregolamento__regdid_id'],
            'RegDidState': query['didatticaregolamento__stato_regdid_cod'],
            'CdSId': query['cds_cod'],
            'AcademicYear': query['didatticaregolamento__aa_reg_did'],
            'CdSName': query['nome_cds_it'] if req_lang == 'it' or query['nome_cds_eng'] is None else query['nome_cds_eng'],
            'DepartmentId': query['dip__dip_cod'],
            'DepartmentName': query['dip__dip_des_it'] if req_lang == 'it' or query['dip__dip_des_eng'] is None else query['dip__dip_des_eng'],
            'CourseType': query['tipo_corso_cod'],
            'CourseClassId': query['cla_miur_cod'],
            'CourseClassName': query['cla_miur_des'],
            'CdSLanguage': langs,
            'CdSDuration': query['durata_anni'],
            'CdSECTS': query['valore_min'],
            'CdSAttendance': query['didatticaregolamento__frequenza_obbligatoria'],
            'CdSIntro': query['DESC_COR_BRE'],
            'CdSGoals': query['OBB_SPEC'],
            'CdSAccess': query['REQ_ACC'],
            'CdSAdmission': query['REQ_ACC_2'],
            'CdSProfiles': query['PROFILO'],
            'CdSFinalTest': query['PROVA_FINALE'],
            'CdSFinalTestMode': query['PROVA_FINALE_2'],
            'CdSSatisfactionSurvey': query['codicione'],
        }


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
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_cod'],
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
            'StudyActivityName': query['des'] if req_lang == 'it' or query['af_gen_des_eng'] is None else query['af_gen_des_eng'],
            'StudyActivityCdSID': query['cds__cds_cod'],
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
            'StudyActivitiesBorrowedFromThis': studyactivitiesborrowedfromthis,

        }


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


class CdSMainTeachersSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query,
                                 str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query,
                req_lang='en'):
        name = query['didatticacopertura__personale__cognome'] + " " + query['didatticacopertura__personale__nome'] + \
            (" " + query['didatticacopertura__personale__middle_name']
             if query['didatticacopertura__personale__middle_name'] is not None else "")
        return {
            'TeacherID': query['didatticacopertura__personale__matricola'],
            'TeacherName': name,
            'TeacherRole': query['didatticacopertura__personale__cd_ruolo'],
            'TeacherSSD': query['didatticacopertura__personale__cd_ssd'],
        }


class TeacherResearchGroupsSerializer(CreateUpdateAbstract):
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
            'RGroupID': query['ricercadocentegruppo__ricerca_gruppo__id'],
            'RGroupName': query['ricercadocentegruppo__ricerca_gruppo__nome'],
            'RGroupDescription': query['ricercadocentegruppo__ricerca_gruppo__descrizione'],
        }


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
                'R&SLineID': query['ricercadocentelineabase__ricerca_linea_base__id'],
                'R&SLineDescription': query['ricercadocentelineabase__ricerca_linea_base__descrizione'],
                'R&SLineResults': query['ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto'],
                'R&SLineERC0Id': query['ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod'],
                'R&SLineERC0Name': query['ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description'],
            }
        else:
            return {
                'R&SLineID': query['ricercadocentelineaapplicata__ricerca_linea_applicata__id'],
                'R&SLineDescription': query['ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione'],
                'R&SLineResults': query['ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto'],
                'R&SLineERC0Id': query[
                    'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod'],
                'R&SLineERC0Name': query[
                    'ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description'],
            }


class TeachersListSerializer(CreateUpdateAbstract):

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
            'TeacherID': query['matricola'],
            'TeacherName': full_name,
            'TeacherDepartmentID': query['dip_cod'],
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or query['dip_des_eng'] is None else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherSSDCod': query['cd_ssd'],
            'TeacherSSDDescription': query['ds_ssd'],
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
            'StudyActivityID': query['didatticacopertura__af__af_id'],
            'StudyActivityName': query['didatticacopertura__af__des'] if req_lang == 'it' or query['didatticacopertura__af__af_gen_des_eng'] is None else query['didatticacopertura__af__af_gen_des_eng'],
            'StudyActivityCdSID': query['didatticacopertura__af__cds_id'],
            'StudyActivityRegDidId': query['didatticacopertura__af__regdid__regdid_id'],
            'StudyActivityCdSName': query['didatticacopertura__af__cds__nome_cds_it'] if req_lang == 'it' or query[
                'didatticacopertura__af__cds__nome_cds_eng'] is None else query['didatticacopertura__af__cds__nome_cds_eng'],
            'StudyActivityAA': query['didatticacopertura__aa_id'],
            'StudyActivityYear': query['didatticacopertura__af__anno_corso'],
            'StudyActivitySemester': query['didatticacopertura__af__ciclo_des'],
            'StudyActivityECTS': query['didatticacopertura__af__peso'],
            'StudyActivityLanguage': query['didatticacopertura__af__lista_lin_did_af'],
            'StudyActivitySSD': query['didatticacopertura__af__sett_des'],
            'StudyActivityCompulsory': query['didatticacopertura__af__freq_obblig_flg'],
        }


class TeacherInfoSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'TeacherID': query['matricola'],
            'TeacherFirstName': query['nome'] + (" " + query['middle_name']
                                                 if query['middle_name'] is not None else ""),
            'TeacherLastName': query['cognome'],
            'TeacherDepartmentID': query['dip_cod'],
            'TeacherDepartmentName': query['dip_des_it'] if req_lang == "it" or query['dip_des_eng'] is None else query['dip_des_eng'],
            'TeacherRole': query['cd_ruolo'],
            'TeacherRoleDescription': query['ds_ruolo'],
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
            'TeacherCV': query['URL Sito WEB Curriculum Vitae']

        }


class DoctoratesListSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'AcademicYear': query['idesse3_ddr__aa_regdid_id'],
            'DepartmentID': query['dip_cod__dip_cod'],
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


class DegreeTypesListSerializer(CreateUpdateAbstract):

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


class DepartmentsListSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'DepartmentID': query['dip_cod'],
            'DepartmentName': query['dip_des_it'] if req_lang == "it" or query[
                'dip_des_eng'] is None else query['dip_des_eng'],
            'DepartmentNameShort': query['dip_nome_breve'],
        }


class AddressbookListSerializer(CreateUpdateAbstract):
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
            'ID': query['matricola'],
            'Role': query['ds_ruolo'],
            'Structure': query['Struttura'],
            'Function': query['Funzione'],
            'OfficeReference': query['Riferimento Ufficio'],
            'Email': query['Posta Elettronica'],
            'PEC': query['POSTA ELETTRONICA CERTIFICATA'],
            'TelOffice': query['Telefono Ufficio'],
            'TelCelOffice': query['Telefono Cellulare Ufficio'],
            'Fax': query['Fax'],
            'WebSite': query['URL Sito WEB'],
            'CV': query['URL Sito WEB Curriculum Vitae']
        }


class StructuresListSerializer(CreateUpdateAbstract):

    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context['language']).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang='en'):
        return {
            'StructureId': query['uo'],
            'StructureName': query['denominazione'],
            'StructureTypeName': query['ds_tipo_nodo'],
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
