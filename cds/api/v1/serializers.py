from addressbook.settings import ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN

from rest_framework import serializers

from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)

from ..v2.docs import examples

from generics.api.serializers import ReadOnlyModelSerializer
from generics.utils import build_media_path, encrypt

from cds.models import *
from cds.settings import CDS_BROCHURE_IS_VISIBLE, CDS_BROCHURE_MEDIA_PATH


class CdSSerializer(serializers.Serializer):
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


class CdsInfoSerializer(serializers.Serializer):
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

        cds_current_periods_data = None
        if query["CdsCurrentPeriods"] is not None:
            cds_current_periods_data = CdsInfoSerializer.to_dict_cds_periods_data(
                query["CdsCurrentPeriods"], req_lang
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
            "CdsCurrentPeriods": cds_current_periods_data,
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
            email_id_coordinatore = q["matricola_coordinatore__email"].split("@")[0] if q["matricola_coordinatore__email"] and q["matricola_coordinatore__email"].endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}") else None
            email_id_vice = q["matricola_vice_coordinatore__email"].split("@")[0] if q["matricola_vice_coordinatore__email"] and q["matricola_vice_coordinatore__email"].endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}") else None
            return {
                "DirectorId": email_id_coordinatore or encrypt(q["matricola_coordinatore"]),
                "DirectorName": q["nome_origine_coordinatore"],
                "DeputyDirectorId": email_id_vice or encrypt(q["matricola_vice_coordinatore"]),
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
            email_id = q["email"].split("@")[0] if q["email"] and q["email"].endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}") else None
            data.append(
                {
                    "Order": q["ordine"],
                    "OfficeName": q["nome_ufficio"],
                    "OfficeDirector": email_id or encrypt(q["matricola_riferimento"]),
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


class CdSStudyPlansSerializer(serializers.Serializer):
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


class CdSStudyPlanSerializer(serializers.Serializer):
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


class CdsStudyPlansActivitiesSerializer(serializers.Serializer):
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


class StudyActivitiesSerializer(serializers.Serializer):
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
            "StudyActivityFatherName": query["Father"].des if req_lang == "it" else query["Father"].af_gen_des_eng,
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
        

class StudyActivityInfoSerializer(serializers.Serializer):
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
            if not q["email"]: official_email = None
            else: official_email = next((e for e in q["email"] if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")), None)

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
                    "StudyActivityTeacherID": official_email.split("@")[0] if official_email else encrypt(q["coper_id__personale_id__matricola"]),
                    # if not q["coper_id__personale_id__flg_cessato"]
                    # else None,
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


class StudyActivityMinimalInfoSerializer(serializers.Serializer):
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


class DegreeTypesSerializer(serializers.Serializer):
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


class AcademicYearsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {"AcademicYear": query["aa_reg_did"]}


class ProgramTypesSerializer(serializers.Serializer):
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


class CdsAreasSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "AreaCds": list(instance.values())[0]
        }


class CdsExpiredSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "CdsCod": query["cds__cds_cod"],
            "LastErogationYear": query["aa_reg_did"],
            "CdSDuration" : query["cds__durata_anni"]
        }




# v2 serializers

class StudyActivitiesDetailSerializerV1(ReadOnlyModelSerializer):
    StudyActivityID = serializers.IntegerField(source="af_pds_id")
    StudyActivityCod = serializers.CharField(
        source="ana_mod_cod",
        help_text="",
        default=None,
    )
    StudyActivityCdSID = serializers.IntegerField(
        source="id_cds.cds_id",
        help_text="",
        default=None,
    )
    StudyActivityCdSCod = serializers.CharField(
        source="cds_cod",
        help_text="",
        default=None,
    )
    StudyActivityRegDidId = serializers.IntegerField(
        source="regdid_id",
        help_text="",
        default=None,
    )
    StudyActivityErogationYear = serializers.IntegerField(
        source="aa_off_id",
        help_text="",
        default=None,
    )
    StudyActivityECTS = serializers.IntegerField(
        source="cfu",
        help_text="",
        default=None,
    )
    StudyActivityYear = serializers.IntegerField(
        source="anno_corso",
        help_text="",
        default=None,
    )
    StudyActivityTeachingUnitTypeCod = serializers.CharField(
        source="taf_cod",
        help_text="",
        default=None,
    )
    StudyActivityTeachingUnitType = serializers.CharField(
        source="taf_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityName  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityLanguage  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityModalities  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherID  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherName  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiesModules  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityPartitions  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityRoot  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityHours  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyBorrows = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyBorrowedFrom  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyContents  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityStudyPlans = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityCdSName = serializers.CharField(
        source="id_cds.nome_cds_it",
        help_text="",
        default=None,
    )
    StudyActivityCompulsory = serializers.CharField(
        source="flag_obbl",
        help_text="",
        default=None,
    )
    StudyActivitySSDCod = serializers.CharField(
        source="sett_cod",
        help_text="",
        default=None,
    )
    StudyActivitySSD = serializers.CharField(
        source="sett_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityPartitionDes = serializers.CharField(
        source="erog_id.part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivitySemester = serializers.CharField(
        source="erog_id.tipo_periodo_did_desc_ita",
        help_text="",
        default=None,
    )
    
    def get_StudyActivityName(self, obj):
        if not obj.erog_found: return obj.ana_af_desc_ita
        return obj.ana_mod_desc_ita
        
    def get_StudyActivityStudyPlans(self, obj):
        if obj.erog_found: return getattr(obj, "pds", [])
        return [obj.pds_desc_ita]
        
    def get_StudyActivityLanguage(self, obj):
        if obj.erog_found: return [obj.erog_id.lingua_did_desc_ita]
        result = []
        for erog in obj.moduli:
            result.append(erog.erog_id.lingua_did_desc_ita)
        return set(result)

    def get_StudyActivityTeacherID(self, obj):
        if obj.erog_id.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        email = obj.erog_id.mod_off_id.af_off.doc_tit_id_ab.email
        if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
            return email.split("@")[0]
        return encrypt(obj.erog_id.mod_off_id.af_off.doc_tit_matricola)

    def get_StudyActivityTeacherName(self, obj):
        try:
            doc = Personale.objects.filter(id_ab=obj.erog_id.mod_off_id.af_off.doc_tit_id_ab.id_ab).first()
            if doc: return f"{doc.cognome} {doc.nome}"
        except:
            pass
        return None

    def get_StudyActivityModalities(self, obj):
        if obj.erog_found:
            return [{
                "ModalityActivityCod": obj.mod_did_cod,
                "ModalityActivityDescription": obj.mod_did_desc_ita
            }]
        modalities = []
        for mod in obj.moduli:
            m = {
                    "ModalityActivityCod": mod.mod_did_cod,
                    "ModalityActivityDescription": mod.mod_did_desc_ita
                }
            if not m in modalities:
                modalities.append(m)
        return modalities

    def get_StudyActivitiesModules(self, obj):
        if not obj.moduli: return []
        moduli = obj.moduli.values("ana_mod_id", "ana_mod_cod", "ana_mod_desc_ita").distinct()
        if moduli.count() == 1: return []
        result = []
        for m in moduli:
            erog_list = []
            erogazioni = obj.moduli.filter(ana_mod_id=m["ana_mod_id"]).values(
                "erog_id",
                "erog_id__part_stu_cod",
                "erog_id__part_stu_desc_ita",
                "erog_id__fatt_part_stu_cod",
                "erog_id__fatt_part_stu_desc_ita",
                "erog_id__tipo_periodo_did_desc_ita",
            ).distinct().order_by("erog_id")
            if erogazioni.count() > 1:
                m_id = None
                for e in erogazioni:
                    erog_list.append(
                        {
                            "StudyActivityID": e["erog_id"],
                            "StudyActivityPartitionCod": e["erog_id__part_stu_cod"],
                            "StudyActivityPartitionDes": e["erog_id__part_stu_desc_ita"],
                            "StudyActivityExtendedPartitionCod": e["erog_id__fatt_part_stu_cod"],
                            "StudyActivityExtendedPartitionDes": e["erog_id__fatt_part_stu_desc_ita"],
                        }
                    )
            else:
                m_id = erogazioni.first()["erog_id"]
            
            result.append(
                {
                    "StudyActivityID": m_id,
                    "StudyActivityCod": m["ana_mod_cod"],
                    "StudyActivityName": m["ana_mod_desc_ita"],
                    "StudyActivitySemester": erogazioni.first()["erog_id__tipo_periodo_did_desc_ita"],
                    "StudyActivityPartitions": erog_list,
                }
            ) 
        return result
        
    def get_StudyActivityPartitions(self, obj):
        moduli = obj.moduli.values("ana_mod_id").distinct()
        if moduli.count() > 1:
            return []
        erog_list = []
        erogazioni = obj.moduli.values(
            "erog_id",
            "erog_id__part_stu_cod",
            "erog_id__part_stu_desc_ita",
            "erog_id__fatt_part_stu_cod",
            "erog_id__fatt_part_stu_desc_ita",
            "erog_id__tipo_periodo_did_desc_ita",
        ).distinct().order_by("erog_id")
        if erogazioni.count() > 1:
            for e in erogazioni:
                erog_list.append(
                    {
                        "StudyActivityID": e["erog_id"],
                        "StudyActivityPartitionCod": e["erog_id__part_stu_cod"],
                        "StudyActivityPartitionDes": e["erog_id__part_stu_desc_ita"],
                        "StudyActivityExtendedPartitionCod": e["erog_id__fatt_part_stu_cod"],
                        "StudyActivityExtendedPartitionDes": e["erog_id__fatt_part_stu_desc_ita"],
                    }
                )
        return erog_list

    def get_StudyActivityRoot(self, obj):
        if not obj.erog_found: return None
        if DidatticaAttivitaFormativaPds.objects.filter(af_pds_id=obj.erog_id.erog_id).exists():
            return None
        return {
            "StudyActivityID": obj.af_pds_id,
            "StudyActivityName": obj.ana_af_desc_ita,
            "StudyActivityCod": obj.ana_af_cod
        }

    def get_StudyActivityHours(self, obj):
        if not obj.erog_found: return []
        coperture = getattr(obj.erog_id, 'coperture_attive', [])
        result = []
        for cop in coperture:
            teacher_id = None
            if cop.doc_matricola != "-999999999":
                email = getattr(cop.doc_id_ab, "email", None)
                if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                    teacher_id = email.split("@")[0]
                else:
                    teacher_id = encrypt(cop.doc_matricola)
            ore = cop.dettaglio_ore.all()
            for ora in ore:
                d = {
                    "ActivityType": ora.tipo_att_did_cod,
                    "Hours": ora.ore,
                    "StudyActivityTeacherID": teacher_id,
                    "StudyActivityTeacherName": f"{cop.doc_cognome} {cop.doc_nome}",
                }
                result.append(d)
        return result

    def get_StudyActivitiyBorrows(self, obj):
        result = []
        for m in obj.mutuazioni:
            for pds in m.pds:
                result.append({
                    "StudyActivityID": m.erog_id,
                    "StudyActivityName": pds.ana_mod_desc_ita,
                    "StudyActivityPartitionCod": m.part_stu_cod,
                    "StudyActivityPartition": m.part_stu_desc_ita,
                    "StudyActivityCdSCod": pds.cds_cod,
                    "StudyActivityCdSName": pds.id_cds.nome_cds_it,
                })
        return result
        
    def get_StudyActivitiyBorrowedFrom(self, obj):
        # ho trovato l'erog_id e corrisponde all'erogazione master
        # sono io l'attività master
        if not obj.mutuato_da: return None
        m = obj.mutuato_da.first()
        result = {
            "StudyActivityID": m.erog_id.erog_master_id,
            "StudyActivityName": m.ana_mod_desc_ita,
            "StudyActivityPartition": m.erog_id.part_stu_desc_ita,
            "StudyActivityCdSCod": m.cds_cod,
            "StudyActivityCdSName": m.id_cds.nome_cds_it,
            "StudyActivityStudyPlans": [],
        }
        for m in obj.mutuato_da:
            result["StudyActivityStudyPlans"].append(m.pds_desc_ita)
        result["StudyActivityStudyPlans"] = set(result["StudyActivityStudyPlans"])
        return result
    
    def get_StudyActivitiyContents(self, obj):
        if getattr(obj, "num_erogazioni", 1) > 1: return []
        result = []
        for testo in DidatticaTestiAfErogata.objects.filter(erog_id=obj.erog_id.erog_master_id).all():
            result.append({
                "StudyActivitiyContentCod": testo.campo_cod,
                "StudyActivitiyContentTitle": testo.campo_desc_ita,
                "StudyActivitiyContentDes": testo.testo_fmt_ita
            })
        return result
    
    class Meta:
        model = DidatticaAttivitaFormativaPds
        fields = [
            "StudyActivityID",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivityPartitionDes",
            "StudyActivityRoot",
            "StudyActivityCdSID",
            "StudyActivityCdSCod",
            "StudyActivityRegDidId",
            "StudyActivityStudyPlans",
            "StudyActivityErogationYear",
            "StudyActivityECTS",
            "StudyActivityLanguage",
            "StudyActivityModalities",
            "StudyActivitySSDCod",
            "StudyActivitySSD",
            "StudyActivityCompulsory",
            "StudyActivityCdSName",
            "StudyActivityYear",
            "StudyActivitySemester",
            "StudyActivityTeacherID",
            "StudyActivityTeacherName",
            "StudyActivityTeachingUnitTypeCod",
            "StudyActivityTeachingUnitType",
            "StudyActivitiesModules",
            "StudyActivityPartitions",
            "StudyActivityHours",
            "StudyActivitiyBorrows",
            "StudyActivitiyBorrowedFrom",
            "StudyActivitiyContents",
        ]

        language_field_map = {
            "cds_name": {"it": "id_cds.nome_cds_it", "en": "id_cds.nome_cds_eng"},
            "sett_desc": {"it": "sett_desc_ita", "en": "sett_desc_eng"},
            "part": {"it": "erog_id.part_stu_desc_ita", "en": "erog_id.part_stu_desc_eng"},
        }

    
@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
class StudyActivitiesListSerializerV1(ReadOnlyModelSerializer):
    StudyActivityID = serializers.IntegerField(
        source="erog_id",
        help_text="",
        default=None,
    )
    StudyActivityCod = serializers.CharField(
        source="mod_off_id.ana_mod_cod",
        help_text="",
        default=None,
    )
    StudyActivityName = serializers.CharField(
        source="mod_off_id.ana_mod_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityCdSID = serializers.IntegerField(
        source="mod_off_id.af_off.id_cds.cds_id",
        help_text="",
        default=None,
    )
    StudyActivityCdSCod = serializers.CharField(
        source="mod_off_id.af_off.cds_cod",
        help_text="",
        default=None,
    )
    StudyActivityCdSName = serializers.CharField(
        source="mod_off_id.af_off.id_cds.nome_cds_it",
        help_text="",
        default=None,
    )
    DepartmentName = serializers.CharField(
        source="mod_off_id.af_off.id_cds.dip.dip_desc_ita",
        help_text="",
        default=None,
    )
    DepartmentCod = serializers.CharField(
        source="mod_off_id.af_off.id_cds.dip.dip_cod",
        help_text="",
        default=None,
    )
    StudyActivityLanguage = serializers.CharField(
        source="lingua_did_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivitySemester = serializers.CharField(
        source="tipo_periodo_did_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityTeacherID = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityPartitionCod = serializers.CharField(
        source="part_stu_cod",
        help_text="",
        default=None,
    )
    StudyActivityPartitionDes = serializers.CharField(
        source="part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityExtendedPartitionCod = serializers.CharField(
        source="fatt_part_stu_cod",
        help_text="",
        default=None,
    )
    StudyActivityExtendedPartitionDes = serializers.CharField(
        source="fatt_part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityStudyPlans = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityFathers = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityAcademicYear = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityYear = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitySSDCod = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitySSD = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityRegDidId = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherName = serializers.SerializerMethodField(
        help_text="",
    )

    def to_representation(self, instance):
        # Usiamo il prefetch in modo sicuro. 
        # Se non ci sono pds, first_pds sarà None (senza crashare!)
        instance._pds_list= list(instance.pds.all())
        return super().to_representation(instance)

    def get_StudyActivityTeacherName(self, obj):
        if obj.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            nome = obj.mod_off_id.doc_tit_id_ab.nome
            cognome = obj.mod_off_id.doc_tit_id_ab.cognome
            if nome and cognome:
                return f"{cognome} {nome}"
        except:
            pass
        return None
        
    def get_StudyActivityTeacherID(self, obj):
        if obj.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            email = getattr(obj.mod_off_id.doc_tit_id_ab, "email", None)
            if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                return email.split("@")[0]
            return encrypt(obj.mod_off_id.af_off.doc_tit_matricola)
        except:
            pass
        return None
        
    def get_StudyActivityStudyPlans(self, obj):
        result = []
        for pds in obj._pds_list:
            result.append(pds.pds_desc_ita)
        return set(result)

    def get_StudyActivityFathers(self, obj):
        # Check in Python invece di .filter().exists()
        if any(pds.af_pds_id == obj.erog_id for pds in obj._pds_list):
            return []
        
        result = []
        for pds in obj._pds_list:
            result.append({
                "id": pds.af_pds_id,
                "cod": pds.ana_af_cod,
                "name": pds.ana_af_desc_ita,
                "pds": pds.pds_desc_ita,
            })
        return [dict(t) for t in {tuple(d.items()) for d in result}]

    def get_StudyActivityYear(self, obj):
        return obj._pds_list[0].anno_corso if obj._pds_list else None

    def get_StudyActivityAcademicYear(self, obj):
        return obj._pds_list[0].aa_off_id if obj._pds_list else None
        
    def get_StudyActivitySSDCod(self, obj):
        return obj._pds_list[0].sett_cod if obj._pds_list else None
        
    def get_StudyActivitySSD(self, obj):
        return obj._pds_list[0].sett_desc_ita if obj._pds_list else None
    
    def get_StudyActivityRegDidId(self, obj):
        return obj._pds_list[0].regdid_id if obj._pds_list else None
    
    class Meta:
        model = DidatticaAttivitaFormativaErogata
        fields = [
            "StudyActivityID",
            "StudyActivityCdSID",
            "StudyActivityCdSCod",
            "StudyActivityCdSName",
            "DepartmentName",
            "DepartmentCod",
            "StudyActivityFathers",
            "StudyActivityRegDidId",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivityYear",
            "StudyActivityAcademicYear",
            "StudyActivityLanguage",
            "StudyActivitySemester",
            "StudyActivitySSDCod",
            "StudyActivitySSD",
            "StudyActivityTeacherName",
            "StudyActivityTeacherID",
            "StudyActivityStudyPlans",
            "StudyActivityPartitionCod",
            "StudyActivityPartitionDes",
            "StudyActivityExtendedPartitionCod",
            "StudyActivityExtendedPartitionDes",
        ]

