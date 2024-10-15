from generics.serializers import CreateUpdateAbstract
from generics.utils import build_media_path, encrypt

from cds.models import DidatticaRegolamento
from cds.settings import CDS_BROCHURE_IS_VISIBLE, CDS_BROCHURE_MEDIA_PATH


class CdSSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        langs = []
        for q in query["Languages"]:
            langs.append(
                q["lingua_des_it"]
                if req_lang == "it" or q["lingua_des_eng"] is None
                else q["lingua_des_eng"]
            )
        # data = None
        # if query["OtherData"] is not None:
        # data = CdSSerializer.to_dict_data(
        # query["OtherData"])
        erogation_mode = None
        if query["ErogationMode"] is not None:
            erogation_mode = query["ErogationMode"][0]["modalita_erogazione"]

        regdid = DidatticaRegolamento.objects.filter(
            pk=query["didatticaregolamento__regdid_id"]
        ).first()
        ordinamento_didattico = regdid.get_ordinamento_didattico()

        return {
            "RegDidId": query["didatticaregolamento__regdid_id"],
            "CdSId": query["cds_id"],
            "CdSCod": query["cds_cod"],
            "AcademicYear": query["didatticaregolamento__aa_reg_did"],
            "AreaCds": query["area_cds"]
            if req_lang == "it" or query["area_cds_en"] is None
            else query["area_cds_en"],
            "CdSName": query["nome_cds_it"]
            if req_lang == "it" or query["nome_cds_eng"] is None
            else query["nome_cds_eng"],
            "DepartmentId": query["dip__dip_id"],
            "DepartmentCod": query["dip__dip_cod"],
            "DepartmentName": query["dip__dip_des_it"]
            if req_lang == "it" or query["dip__dip_des_eng"] is None
            else query["dip__dip_des_eng"],
            "CourseType": query["tipo_corso_cod"],
            "CourseTypeDescription": query["tipo_corso_des"],
            "CourseClassCod": query["cla_miur_cod"],
            "CourseClassName": query["cla_miur_des"],
            "CourseInterClassCod": query["intercla_miur_cod"],
            "CourseInterClassDes": query["intercla_miur_des"],
            "ErogationMode": erogation_mode,
            "CdSLanguage": langs,
            "CdSDuration": query["durata_anni"],
            "CdSECTS": query["valore_min"],
            "CdSAttendance": query["didatticaregolamento__frequenza_obbligatoria"],
            "RegDidState": query["didatticaregolamento__stato_regdid_cod"],
            "JointDegree": query["didatticaregolamento__titolo_congiunto_cod"],
            "StudyManifesto": build_media_path(query["OtherData"][0]["manifesto_studi"])
            if query["OtherData"]
            else None,
            "DidacticRegulation": build_media_path(
                query["OtherData"][0]["regolamento_didattico"]
            )
            if query["OtherData"]
            else None,
            "TeachingSystem": build_media_path(ordinamento_didattico[1])
            if ordinamento_didattico
            else None,
            "TeachingSystemYear": ordinamento_didattico[0]
            if ordinamento_didattico
            else None,
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
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        langs = []
        for q in query["Languages"]:
            langs.append(
                q["didatticacdslingua__lingua_des_it"]
                if req_lang == "it" or q["didatticacdslingua__lingua_des_eng"] is None
                else q["didatticacdslingua__lingua_des_eng"]
            )
        video = None
        if query["URL_CDS_VIDEO"] is not None:
            # video = CdsInfoSerializer.get_media_url(
            # query['URL_CDS_VIDEO'])
            video = build_media_path(query["URL_CDS_VIDEO"], CDS_BROCHURE_MEDIA_PATH)

        doc = None
        if query["URL_CDS_DOC"] is not None:
            # doc = CdsInfoSerializer.get_media_url(
            # query['URL_CDS_DOC'])
            doc = build_media_path(query["URL_CDS_DOC"], CDS_BROCHURE_MEDIA_PATH)

        data = None
        if query["OtherData"] is not None:
            data = CdsInfoSerializer.to_dict_data(query["OtherData"])
        offices_data = None
        if query["OfficesData"] is not None:
            offices_data = CdsInfoSerializer.to_dict_offices_data(query["OfficesData"])

        erogation_mode = None
        if query["ErogationMode"] is not None:
            erogation_mode = query["ErogationMode"][0]["modalita_erogazione"]

        cds_groups_data = None
        if query["CdsGroups"] is not None:
            cds_groups_data = CdsInfoSerializer.to_dict_cds_groups_data(
                query["CdsGroups"], req_lang
            )

        cds_periods_data = None
        if query["CdsPeriods"] is not None:
            cds_periods_data = CdsInfoSerializer.to_dict_cds_periods_data(
                query["CdsPeriods"], req_lang
            )

        regdid = DidatticaRegolamento.objects.filter(
            pk=query["didatticaregolamento__regdid_id"]
        ).first()
        ordinamento_didattico = regdid.get_ordinamento_didattico()

        return {
            "RegDidId": query["didatticaregolamento__regdid_id"],
            "RegDidState": query["didatticaregolamento__stato_regdid_cod"],
            "CdSId": query["cds_id"],
            "CdSCod": query["cds_cod"],
            "AcademicYear": query["didatticaregolamento__aa_reg_did"],
            "AreaCds": query["area_cds"]
            if req_lang == "it" or query["area_cds_en"] is None
            else query["area_cds_en"],
            "CdSName": query["nome_cds_it"]
            if req_lang == "it" or query["nome_cds_eng"] is None
            else query["nome_cds_eng"],
            "DepartmentId": query["dip__dip_id"],
            "DepartmentCod": query["dip__dip_cod"],
            "DepartmentName": query["dip__dip_des_it"]
            if req_lang == "it" or query["dip__dip_des_eng"] is None
            else query["dip__dip_des_eng"],
            "CourseType": query["tipo_corso_cod"],
            "CourseTypeDescription": query["tipo_corso_des"],
            "CourseClassCod": query["cla_miur_cod"],
            "CourseClassName": query["cla_miur_des"],
            "CourseInterClassCod": query["intercla_miur_cod"],
            "CourseInterClassDes": query["intercla_miur_des"],
            "ErogationMode": erogation_mode,
            "CdSLanguage": langs,
            "CdSDuration": query["durata_anni"],
            "CdSECTS": query["valore_min"],
            "CdSAttendance": query["didatticaregolamento__frequenza_obbligatoria"],
            "CdSIntro": query["INTRO_CDS_FMT"]
            if query["INTRO_CDS_FMT"] is not None
            else query["DESC_COR_BRE"],
            "CdSDoc": doc if CDS_BROCHURE_IS_VISIBLE else None,
            "CdsUrl": query["URL_CDS"],
            "CdSVideo": video,
            "CdSGoals": query["OBB_SPEC"],
            "CdSAccess": query["REQ_ACC"],
            "CdSAdmission": query["REQ_ACC_2"],
            "CdSProfiles": query["PROFILO"],
            "CdSFinalTest": query["PROVA_FINALE"],
            "CdSFinalTestMode": query["PROVA_FINALE_2"],
            "CdSSatisfactionSurvey": query["codicione"],
            "JointDegree": query["didatticaregolamento__titolo_congiunto_cod"],
            "StudyManifesto": build_media_path(query["OtherData"][0]["manifesto_studi"])
            if query["OtherData"]
            else None,
            "DidacticRegulation": build_media_path(
                query["OtherData"][0]["regolamento_didattico"]
            )
            if query["OtherData"]
            else None,
            "TeachingSystem": build_media_path(ordinamento_didattico[1])
            if ordinamento_didattico
            else None,
            "TeachingSystemYear": ordinamento_didattico[0]
            if ordinamento_didattico
            else None,
            "OtherData": data,
            "OfficesData": offices_data,
            "CdsGroups": cds_groups_data,
            "CdsPeriods": cds_periods_data,
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
            return {
                "DirectorId": encrypt(q["matricola_coordinatore"]),
                "DirectorName": q["nome_origine_coordinatore"],
                "DeputyDirectorId": encrypt(q["matricola_vice_coordinatore"]),
                "DeputyDirectorName": q["nome_origine_vice_coordinatore"],
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
            data.append(
                {
                    "Order": q["ordine"],
                    "OfficeName": q["nome_ufficio"],
                    "OfficeDirector": encrypt(q["matricola_riferimento"]),
                    "OfficeDirectorName": q["nome_origine_riferimento"],
                    "TelOffice": q["telefono"],
                    "Email": q["email"],
                    "Building": q["edificio"],
                    "Floor": q["piano"],
                    "Timetables": q["orari"],
                    "OnlineCounter": q["sportello_online"],
                }
            )
        return data

    @staticmethod
    def to_dict_cds_groups_data(query, req_lang="en"):
        data = []
        for q in query:
            data.append(
                {
                    "Order": q["ordine"],
                    "ShortDesc": q["descr_breve_it"]
                    if req_lang == "it" or q["descr_breve_en"] is None
                    else q["descr_breve_en"],
                    "LongDesc": q["descr_lunga_it"]
                    if req_lang == "it" or q["descr_lunga_en"] is None
                    else q["descr_lunga_en"],
                    "Members": CdsInfoSerializer.to_dict_cds_group_members(
                        q["members"], req_lang
                    ),
                }
            )
        return data

    @staticmethod
    def to_dict_cds_group_members(query, req_lang="en"):
        data = []
        for q in query:
            data.append(
                {
                    "Order": q["ordine"],
                    "ID": encrypt(q["matricola"]),
                    "Surname": q["cognome"],
                    "Name": q["nome"],
                    "Function": q["funzione_it"]
                    if req_lang == "it" or q["funzione_en"] is None
                    else q["funzione_en"],
                }
            )
        return data

    @staticmethod
    def to_dict_cds_periods_data(query, req_lang="en"):
        data = []
        for q in query:
            data.append(
                {
                    "Description": q["tipo_ciclo_des"]
                    if req_lang == "it" or q["tipo_ciclo_des_eng"] is None
                    else q["tipo_ciclo_des_eng"],
                    "Start": q["data_inizio"],
                    "End": q["data_fine"],
                }
            )
        return data


class CdSStudyPlansSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        study_activities = {}
        for k in query["StudyActivities"]:
            study_activities[k] = []
            for q in query["StudyActivities"][k]:
                study_activities[k].append(
                    CdsStudyPlansActivitiesSerializer.to_dict(q, req_lang)
                )

        return {
            "RegDidId": query["regdid_id"],
            "StudyPlanId": query["pds_regdid_id"],
            "StudyPlanCOD": query["pds_cod"],
            "StudyPlanName": query["pds_regdid_id__pds_des_it"]
            if req_lang == "it" or query["pds_regdid_id__pds_des_eng"] is None
            else query["pds_regdid_id__pds_des_eng"],
            "StudyActivities": study_activities,
        }


class CdSStudyPlanSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        study_activities = {}
        for k in query["StudyActivities"]:
            study_activities[k] = []
            for q in query["StudyActivities"][k]:
                study_activities[k].append(
                    CdsStudyPlansActivitiesSerializer.to_dict(q, req_lang)
                )

        return {
            "RegDidId": query["regdid__regdid_id"],
            "StudyPlanId": query["pds_regdid_id"],
            "StudyPlanCOD": query["pds_cod"],
            "StudyPlanName": query["pds_des_it"]
            if req_lang == "it" or query["pds_des_eng"] is None
            else query["pds_des_eng"],
            "StudyActivities": study_activities,
        }


class CdsStudyPlansActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StudyActivityID": query["af_id"],
            "StudyActivityCod": query["af_gen_cod"],
            "StudyActivityName": query["des"]
            if req_lang == "it" or query["af_gen_des_eng"] is None
            else query["af_gen_des_eng"],
            "StudyActivityCdSID": query["cds__cds_id"],
            "StudyActivityCdSCod": query["cds__cds_cod"],
            "StudyActivityRegDidId": query["regdid__regdid_id"],
            "StudyActivityTeachingUnitTypeCod": query["tipo_af_cod"],
            "StudyActivityTeachingUnitType": query["tipo_af_des"],
            "StudyActivityInterclassTeachingUnitTypeCod": query["tipo_af_intercla_cod"],
            "StudyActivityInterclassTeachingUnitType": query["tipo_af_intercla_des"],
            "StudyActivityYear": query["anno_corso"],
            "StudyActivitySemester": query["ciclo_des"],
            "StudyActivityECTS": query["peso"],
            "StudyActivitySSD": query["sett_des"],
            "StudyActivityCompulsory": query["freq_obblig_flg"],
            "StudyActivityCdSName": query["cds__nome_cds_it"]
            if req_lang == "it" or query["cds__nome_cds_eng"] is None
            else query["cds__nome_cds_eng"],
        }


class StudyActivitiesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        full_name = None

        if query["matricola_resp_did__cognome"] is not None:
            full_name = (
                query["matricola_resp_did__cognome"]
                + " "
                + query["matricola_resp_did__nome"]
                + (
                    " " + query["matricola_resp_did__middle_name"]
                    if query["matricola_resp_did__middle_name"] is not None
                    else ""
                )
            )
        descrizione_gruppo = ""
        if query["part_stu_des"]:  # pragma: no cover
            descrizione_gruppo = " (" + query["part_stu_des"] + ")"

        return {
            "StudyActivityID": query["af_id"],
            "StudyActivityCod": query["af_gen_cod"],
            "StudyActivityName": query["des"] + descrizione_gruppo
            if req_lang == "it" or query["af_gen_des_eng"] is None
            else query["af_gen_des_eng"],
            "StudyActivityCdSID": query["cds_id"],
            "StudyActivityCdSCod": query["cds_id__cds_cod"],
            "StudyActivityLanguage": query["lista_lin_did_af"]
            .replace(" ", "")
            .split(",")
            if query["lista_lin_did_af"]
            else [],
            "StudyActivityFatherCode": query["af_radice_id"],
            "StudyActivityFatherName": query["Father"],
            "StudyActivityRegDidId": query["regdid_id"],
            "DepartmentName": query["cds_id__dip_id__dip_des_it"]
            if req_lang == "it" or query["cds_id__dip_id__dip_des_eng"] is None
            else query["cds_id__dip_id__dip_des_eng"],
            "DepartmentCod": query["cds_id__dip_id__dip_cod"],
            "StudyActivityYear": query["anno_corso"],
            "StudyActivityAcademicYear": query["aa_off_id"],
            "StudyActivitySemester": query["ciclo_des"],
            "StudyActivitySSDCod": query.get("sett_cod", None),
            "StudyActivitySSD": query.get("sett_des", None),
            "StudyActivityPartitionCod": query["part_stu_cod"],
            "StudyActivityPartitionDes": query["part_stu_des"],
            "StudyActivityExtendedPartitionCod": query["fat_part_stu_cod"],
            "StudyActivityExtendedPartitionDes": query["fat_part_stu_des"],
            "StudyActivityCdSName": query["cds_id__nome_cds_it"]
            if req_lang == "it" or query["cds_id__nome_cds_eng"] is None
            else query["cds_id__nome_cds_eng"],
            "StudyActivityTeacherID": encrypt(query["matricola_resp_did"])
            if query["matricola_resp_did"]
            else None,
            "StudyActivityTeacherName": full_name,
            "StudyPlanDes": query["pds_des"],
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
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        studyactivityroot = None
        if query["ActivityRoot"] is not None:
            studyactivityroot = StudyActivityMinimalInfoSerializer.to_dict(
                query["ActivityRoot"], req_lang
            )

        studyactivityfather = None
        if query["ActivityFather"] is not None:
            studyactivityfather = StudyActivityMinimalInfoSerializer.to_dict(
                query["ActivityFather"], req_lang
            )

        studyactivityborrowed = None
        if query["BorrowedFrom"] is not None:
            studyactivityborrowed = StudyActivityMinimalInfoSerializer.to_dict(
                query["BorrowedFrom"], req_lang
            )

        studyactivitiesborrowedfromthis = []
        if len(query["ActivitiesBorrowedFromThis"]) > 0:
            for q in query["ActivitiesBorrowedFromThis"]:
                studyactivitiesborrowedfromthis.append(
                    StudyActivityMinimalInfoSerializer.to_dict(q, req_lang)
                )

        ore = None
        if query["Hours"] is not None:
            ore = StudyActivityInfoSerializer.to_dict_hours(query["Hours"])

        modalities = None
        if query["Modalities"] is not None:
            modalities = StudyActivityInfoSerializer.to_dict_modalities(
                query["Modalities"]
            )
        descrizione_gruppo = ""
        if query["part_stu_des"]:  # pragma: no cover
            descrizione_gruppo = "(" + query["part_stu_des"] + ")"
        return {
            "StudyActivityID": query["af_id"],
            "StudyActivityCod": query["af_gen_cod"],
            "StudyActivityName": query["des"] + descrizione_gruppo
            if req_lang == "it" or query["af_gen_des_eng"] is None
            else query["af_gen_des_eng"],
            "StudyActivityCdSID": query["cds__cds_id"],
            "StudyActivityCdSCod": query["cds__cds_cod"],
            "StudyActivityLanguage": query["lista_lin_did_af"]
            .replace(" ", "")
            .split(",")
            if query["lista_lin_did_af"]
            else [],
            "StudyActivityRegDidId": query["regdid__regdid_id"],
            "StudyActivityPdsCod": query["pds_cod"],
            "StudyActivityPdsDes": query["pds_des"],
            "StudyActivityErogationYear": query["regdid__aa_reg_did"]
            + query["anno_corso"]
            - 1
            if query["anno_corso"]
            else studyactivityroot.get("StudyActivityErogationYear", None),
            "StudyActivityYear": query["anno_corso"]
            or studyactivityroot.get("StudyActivityYear", None),
            "StudyActivitySemester": query["ciclo_des"],
            "StudyActivityErogationLanguage": query["LANGUAGEIT"]
            if req_lang == "it" or query["LANGUAGEEN"] is None
            else query["LANGUAGEEN"],
            "StudyActivityECTS": query["peso"],
            "StudyActivityHours": ore,
            "StudyActivityModalities": modalities,
            "StudyActivitySSD": query.get("sett_des", None),
            "StudyActivitySSDCod": query.get("sett_cod", None),
            "StudyActivityCompulsory": query["freq_obblig_flg"],
            "StudyActivityCdSName": query["cds__nome_cds_it"]
            if req_lang == "it" or query["cds__nome_cds_eng"] is None
            else query["cds__nome_cds_eng"],
            "StudyActivityTeachingUnitTypeCod": query["tipo_af_cod"],
            "StudyActivityTeachingUnitType": query["tipo_af_des"],
            "StudyActivityInterclassTeachingUnitTypeCod": query["tipo_af_intercla_cod"],
            "StudyActivityInterclassTeachingUnitType": query["tipo_af_intercla_des"],
            "StudyActivityTeacherID": encrypt(query["StudyActivityTeacherID"]),
            "StudyActivityTeacherName": query["StudyActivityTeacherName"],
            "StudyActivityPartitionCod": query["PartitionCod"],
            "StudyActivityPartitionDes": query["PartitionDescription"],
            "StudyActivityExtendedPartitionCod": query["ExtendedPartitionCod"],
            "StudyActivityExtendedPartitionDes": query["ExtendedPartitionDescription"],
            "StudyActivityContent": query["StudyActivityContent"],
            "StudyActivityProgram": query["StudyActivityProgram"],
            "StudyActivityLearningOutcomes": query["StudyActivityLearningOutcomes"],
            "StudyActivityMethodology": query["StudyActivityMethodology"],
            "StudyActivityEvaluation": query["StudyActivityEvaluation"],
            "StudyActivityTextbooks": query["StudyActivityTextbooks"],
            "StudyActivityWorkload": query["StudyActivityWorkload"],
            "StudyActivityElearningLink": query["StudyActivityElearningLink"],
            "StudyActivityElearningInfo": query["StudyActivityElearningInfo"],
            "StudyActivityPrerequisites": query["StudyActivityPrerequisites"],
            "StudyActivityDevelopmentGoal": query["StudyActivityDevelopmentGoal"],
            "StudyActivitiesModules": query["MODULES"],
            "StudyActivityRoot": studyactivityroot,
            "StudyActivityFather": studyactivityfather,
            "StudyActivityBorrowedFrom": studyactivityborrowed,
            "StudyActivitiesBorrowedFromThis": studyactivitiesborrowedfromthis,
        }

    @staticmethod
    def to_dict_hours(query):
        hours = []
        for q in query:
            full_name = None
            if (
                q["coper_id__personale_id__cognome"]
                and q["coper_id__personale_id__nome"]
            ):
                full_name = f"{q['coper_id__personale_id__cognome']} {q['coper_id__personale_id__nome']}"
                if q["coper_id__personale_id__middle_name"]:
                    full_name = (
                        f"{full_name} {q['coper_id__personale_id__middle_name']}"
                    )
            hours.append(
                {
                    "ActivityType": q["tipo_att_did_cod"],
                    "Hours": q["ore"],
                    "StudyActivityTeacherID": encrypt(
                        q["coper_id__personale_id__matricola"]
                    )
                    if not q["coper_id__personale_id__flg_cessato"]
                    else None,
                    "StudyActivityTeacherName": full_name,
                    "TeacherEmail": q["email"],
                }
            )
        return hours

    @staticmethod
    def to_dict_modalities(query):
        modalities = []
        for q in query:
            modalities.append(
                {
                    "ModalityActivityId": q["mod_did_af_id"],
                    "ModalityActivityCod": q["mod_did_cod"],
                    "ModalityActivityDescription": q["mod_did_des"],
                }
            )
        return modalities


class StudyActivityMinimalInfoSerializer(CreateUpdateAbstract):
    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "StudyActivityID": query.get("af_id"),
            "StudyActivityName": query["des"]
            if req_lang == "it" or query["af_gen_des_eng"] is None
            else query["af_gen_des_eng"],
            "StudyActivitySemester": query["ciclo_des"],
            "StudyActivityYear": query["anno_corso"],
            "StudyActivityErogationYear": query["regdid__aa_reg_did"]
            + query["anno_corso"]
            - 1
            if query.get("anno_corso")
            else None,
            "StudyActivityRegDidId": query["regdid__regdid_id"],
            "StudyActivityCdSID": query["cds__cds_id"],
            "StudyActivityCdSName": query["cds__nome_cds_it"]
            if req_lang == "it" or query["cds__nome_cds_eng"] is None
            else query["cds__nome_cds_eng"],
            "StudyActivityCdSCod": query["cds__cds_cod"],
            "StudyActivityPdsCod": query["pds_cod"],
            "StudyActivityPdsDes": query["pds_des"],
        }


class DegreeTypesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "CourseType": query["tipo_corso_cod"],
            "CourseTypeDescription": query["tipo_corso_des"],
        }


class AcademicYearsSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {"AcademicYear": query["aa_reg_did"]}


class ProgramTypesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "TypeProgramId": query["id"],
            "TypeProgramDescription": query["nome_programma"],
        }


class CdsAreasSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "AreaCds": query["area_cds"]
            if req_lang == "it" or query["area_cds_en"] is None
            else query["area_cds_en"],
        }
