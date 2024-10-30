import json

import requests
from generics.serializers import CreateUpdateAbstract
from generics.settings import UNICMS_AUTH_TOKEN
from rest_framework import serializers

from cds_websites.models import SitoWebCdsOggettiPortale
from cds_websites.settings import UNICMS_OBJECT_API


class SitoWebCdsOggettiPortaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitoWebCdsOggettiPortale
        fields = ("id", "aa_regdid_id", "titolo_it", "titolo_en")


class CdsWebsitesTopicSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        return {
            "TopicId": query["id"],
            "TopicDescription": query["descr_topic_it"]
            if req_lang == "it" or query["descr_topic_en"] is None
            else query["descr_topic_en"],
            "Visible": query["visibile"],
        }


class CdsWebsitesTopicArticlesSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        if query["tipo"] == "Article":
            content = {
                "Text": query["testo_it"]
                if req_lang == "it" or not query["testo_en"]
                else query["testo_en"]
            }
        else:
            content = CdsWebsitesTopicArticlesSerializer.to_dict_objects(
                query.get("oggetto", None), req_lang
            )

        return {
            "ID": query["id"],
            "Title": query["titolo_it"]
            if req_lang == "it" or not query["titolo_en"]
            else query["titolo_en"],
            "TopicId": query["topic_id"],
            "TopicDescription": query["descr_topic_it"]
            if req_lang == "it" or not query["descr_topic_en"]
            else query["descr_topic_en"],
            "Visible": query["visibile"],
            "Order": query["ordine"],
            "Type": query["tipo"],
            "Content": content,
            "SubArticles": CdsWebsitesTopicArticlesSerializer.to_dict_sub_articles(
                query.get("sotto_articoli", []), req_lang
            ),
            "OtherData": CdsWebsitesTopicArticlesSerializer.to_dict_other_data(
                query.get("altri_dati", []), req_lang
            ),
        }

    @staticmethod
    def to_dict_objects(q, req_lang="en"):
        if q and UNICMS_AUTH_TOKEN:
            head = {"Authorization": "Token {}".format(UNICMS_AUTH_TOKEN)}
            unicms_obj_api = UNICMS_OBJECT_API
            api_url = unicms_obj_api.get(q["id_classe_oggetto_portale"], "")
            unicms_object = (
                requests.get(
                    f"{api_url}{q['id_oggetto_portale']}/", headers=head, timeout=5
                )
                if api_url
                else None
            )
            return {
                "Id": q["id"],
                "YearRegDidID": q["aa_regdid_id"],
                "ObjectId": q["id_oggetto_portale"],
                "Object": json.loads(unicms_object._content) if unicms_object else None,
                "ClassObjectId": q["id_classe_oggetto_portale"],
                "ObjectText": q["testo_it"]
                if req_lang == "it" or not q["testo_en"]
                else q["testo_en"],
            }

    @staticmethod
    def to_dict_other_data(query, req_lang="en"):
        other_data = []
        for q in query:
            other_data.append(
                {
                    "Id": q["id"],
                    "Order": q["ordine"],
                    "Title": q["titolo_it"]
                    if req_lang == "it" or not q["titolo_en"]
                    else q["titolo_en"],
                    "Text": q["testo_it"]
                    if req_lang == "it" or not q["testo_en"]
                    else q["testo_en"],
                    "Link": q["link"],
                    "TypeID": q["type_id"],
                    "Type": q["type"],
                    "Visible": q["visibile"],
                }
            )
        return other_data

    @staticmethod
    def to_dict_sub_articles(query, req_lang="en"):
        sub_articles = []
        for q in query:
            sub_articles.append(
                {
                    "Id": q["id"],
                    "Order": q["ordine"],
                    "Title": q["titolo_it"]
                    if req_lang == "it" or not q["titolo_en"]
                    else q["titolo_en"],
                    "Text": q["testo_it"]
                    if req_lang == "it" or not q["testo_en"]
                    else q["testo_en"],
                    "Visible": q["visibile"],
                }
            )
        return sub_articles


class CdsWebsitesStudyPlansSerializer(CreateUpdateAbstract):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        # study_activities = {}
        # for k in query['StudyActivities']:
        #     study_activities[k] = []
        #     for q in query['StudyActivities'][k]:
        #         study_activities[k].append(
        #             CdsStudyPlansActivitiesSerializer.to_dict(
        #                 q, req_lang))
        plan_tabs = None
        if query["PlanTabs"] is not None:
            plan_tabs = CdsWebsitesStudyPlansSerializer.to_dict_plan(
                query["PlanTabs"], req_lang
            )

        return {
            "RegPlanId": query["regpiani_id"],
            "RegDidId": query["regdid_id"],
            "RelevanceCod": query["attinenza_cod"],
            "YearCoorteId": query["aa_coorte_id"],
            "YearRegPlanId": query["aa_regpiani_id"],
            "RegPlanDes": query["des"],
            "DefFlg": query["def_flg"],
            "StatusCod": query["stato_cod"],
            "StatusDes": query["stato_des"],
            "RegPlansPdrId": query["regpiani_pdr_id"],
            "RegPlansPdrCod": query["regpiani_pdr_cod"],
            "RegPlansPdrDes": query["regpiani_pdr_des"],
            "RegPlansPdrCoorteIdYear": query["regpiani_pdr_aa_coorte_id"],
            "RegPlansPdrYear": query["regpiani_pdr_aa_regpiani_id"],
            "FlgExpSegStu": query["flg_exp_seg_stu"],
            "CdSDuration": query["regdid__cds__durata_anni"],
            "PlanTabs": plan_tabs,
        }

    @staticmethod
    def to_dict_plan(query, req_lang="en"):
        plan_tabs = []
        for q in query:
            plan_tabs.append(
                {
                    "PlanTabId": q["sche_piano_id"],
                    "PlanTabDes": q["sche_piano_des"],
                    "PlanTabCod": q["sche_piano_cod"],
                    "PdsCod": q["pds_cod"],
                    "PdsDes": q["pds_des"],
                    "ClaMiurCod": q["cla_miur_cod"],
                    "ClaMiurDes": q["cla_miur_des"],
                    "CommonFlg": q["comune_flg"],
                    "Statutario": q["isStatutario"],
                    "APT": True if q["apt_id"] else False,
                    "AfRequired": CdsWebsitesStudyPlansSerializer.to_dict_af(
                        q.get("AfRequired", []), req_lang
                    ),
                    "AfChoices": CdsWebsitesStudyPlansSerializer.to_dict_af(
                        q.get("AfChoices", []), req_lang
                    ),
                }
            )
        return plan_tabs

    @staticmethod
    def to_dict_af(query, req_lang="en"):
        af = []
        for q in query:
            af.append(
                {
                    "SceId": q["sce_id"],
                    "SceDes": q["sce_des"],
                    "VinId": q["vin_id"],
                    "Year": q["apt_slot_ord_num"]
                    if q["apt_slot_ord_num"]
                    else q["anno_corso"],
                    "RegSceCodType": q["tipo_regsce_cod"],
                    "SceCodType": q["tipo_sce_cod"],
                    "SceDesType": q["tipo_sce_des"],
                    "RegSceCodDes": q["tipo_regsce_des"],
                    "UmRegSceCodType": q["tipo_um_regsce_cod"],
                    "MinUnt": q["min_unt"],
                    "MaxUnt": q["max_unt"],
                    "OpzFlg": q["opz_flg"],
                    "Required": CdsWebsitesStudyPlansSerializer.to_dict_af_required(
                        q.get("Required", []), req_lang
                    ),
                    "Choices": CdsWebsitesStudyPlansSerializer.to_dict_af_choices(
                        q.get("Choices", []), req_lang
                    ),
                    "FilAnd": CdsWebsitesStudyPlansSerializer.to_dict_af_fil_and(
                        q.get("FilAnd", []), req_lang
                    ),
                }
            )
        return af

    @staticmethod
    def to_dict_af_required(query, req_lang="en"):
        af_required = []
        for q in query:
            af_required.append(
                {
                    "ScopeId": q["amb_id_af"],
                    "SceId": q["sce_id"],
                    "SceDes": q["sce_id__sce_des"],
                    "ScopeDes": q["ambito_des_af"],
                    "SettCod": q.get("sett_cod", None),
                    "CreditValue": q["peso"],
                    "CycleDes": q["ciclo_des"],
                    "AfDescription": q["af_gen_des"],
                    "AfId": q["af_id"],
                    "AfCod": q["af_gen_cod"],
                    "AfType": q["tipo_af_des_af"],
                    "AfScope": q["ambito_des_af"],
                    "AfSubModules": CdsWebsitesStudyPlansSerializer.to_dict_af_submodules(
                        q.get("MODULES", []), req_lang
                    ),
                }
            )
        return af_required

    @staticmethod
    def to_dict_af_choices(query, req_lang="en"):
        af_choices = []
        for q in query:
            af_choices.append(
                {
                    "ScopeId": q["amb_id_af"],
                    "SceId": q["sce_id"],
                    "SceDes": q["sce_id__sce_des"],
                    "ScopeDes": q["ambito_des_af"],
                    "SettCod": q.get("sett_cod", None),
                    "CreditValue": q["peso"],
                    "CycleDes": q["ciclo_des"],
                    "AfDescription": q["af_gen_des"],
                    "AfId": q["af_id"],
                    "AfCod": q["af_gen_cod"],
                    "AfType": q["tipo_af_des_af"],
                    "AfScope": q["ambito_des_af"],
                    "AfSubModules": CdsWebsitesStudyPlansSerializer.to_dict_af_submodules(
                        q.get("MODULES", []), req_lang
                    ),
                }
            )
        return af_choices

    @staticmethod
    def to_dict_af_submodules(query, req_lang="en"):
        af_submodules = []
        for q in query:
            af_submodules.append(
                {
                    "StudyActivityID": q["af_id"],
                    "StudyActivityCod": q["af_gen_cod"],
                    "StudyActivityName": q["des"]
                    if req_lang == "it" or q["af_gen_des_eng"] is None
                    else q["af_gen_des_eng"],
                    "StudyActivitySemester": q["ciclo_des"],
                    "StudyActivitySettCod": q.get("sett_cod", None),
                    "StudyActivityCreditValue": q["peso"],
                    "StudyActivityPartitionCod": q["part_stu_cod"],
                    "StudyActivityPartitionDescription": q["part_stu_des"],
                    "StudyActivityExtendedPartitionCod": q["fat_part_stu_cod"],
                    "StudyActivityExtendedPartitionDes": q["fat_part_stu_des"],
                }
            )
        return af_submodules

    @staticmethod
    def to_dict_af_fil_and(query, req_lang="en"):
        fil_and = []
        for q in query:
            fil_and.append(
                {
                    "FilAndId": q["sce_fil_and_id"],
                    "SceId": q["sce_id"],
                    "FilOrId": q["sce_fil_or_id"],
                    "FilOrDes": q["sce_fil_or_des"],
                    "TipoFiltroCod": q["tipo_filtro_cod"],
                    "TipoFiltroDes": q["tipo_filtro_des"],
                    "CourseTypeSceFilAndCod": q["tipo_corso_sce_fil_and_cod"],
                    "CdsSceFilAndId": q["cds_sce_fil_and_id"],
                    "CdsSceFilAndCod": q["cds_sce_fil_and_cod"],
                    "CdsSceFilAndNome": q["cds_sce_fil_and_nome"],
                    "NotFlg": q["not_flg"],
                }
            )
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
