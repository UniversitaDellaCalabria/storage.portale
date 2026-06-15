import json

import requests
from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import ReadOnlyModelSerializer
from generics.settings import UNICMS_AUTH_TOKEN
from cds_websites.settings import UNICMS_OBJECT_API
from cds_websites.models import SitoWebCdsTopic, SitoWebCdsTopicArticoliReg
from cds.models import DidatticaPianiStudio


@extend_schema_serializer(examples=examples.TOPIC_SERIALIZER_EXAMPLE)
class TopicListSerialzer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descr_topic_it")

    class Meta:
        model = SitoWebCdsTopic
        fields = [
            "id",
            "description",
            "visibile",
        ]
        language_field_map = {
            "description": {"it": "descr_topic_it", "en": "descr_topic_en"}
        }


@extend_schema_serializer(examples=examples.ARTICLES_TOPIC_SERIALIZER_EXAMPLE)
class ArticlesTopicSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(source="titolo_it")
    topicId = serializers.CharField(source="sito_web_cds_topic_id")
    topicDescription = serializers.CharField(source="sito_web_cds_topic.descr_topic_it")
    order = serializers.CharField(source="ordine")
    type = serializers.CharField(source="tipo")
    content = serializers.SerializerMethodField()
    otherData = serializers.SerializerMethodField()
    subArticles = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_content(self, obj):
        lang = self.get_requestLang()

        if obj.tipo == "Article":
            return {
                "text": obj.testo_it
                if lang == "it" or obj.testo_en is None
                else obj.testo_en
            }
        else:
            if obj.tipo == "Object" and obj.sito_web_cds_oggetti_portale:
                q = {
                    "id": obj.sito_web_cds_oggetti_portale.id,
                    "id_classe_oggetto_portale": obj.sito_web_cds_oggetti_portale.id_classe_oggetto_portale,
                    "id_oggetto_portale": obj.sito_web_cds_oggetti_portale.id_oggetto_portale,
                    "aa_regdid_id": obj.sito_web_cds_oggetti_portale.aa_regdid_id,
                    "testo_it": obj.sito_web_cds_oggetti_portale.testo_it,
                    "testo_en": obj.sito_web_cds_oggetti_portale.testo_en,
                }

                if q and UNICMS_AUTH_TOKEN:
                    head = {"Authorization": "Token {}".format(UNICMS_AUTH_TOKEN)}
                    unicms_obj_api = UNICMS_OBJECT_API
                    api_url = unicms_obj_api.get(q["id_classe_oggetto_portale"], "")
                    unicms_object = (
                        requests.get(
                            f"{api_url}{q['id_oggetto_portale']}/",
                            headers=head,
                            timeout=5,
                        )
                        if api_url
                        else None
                    )

                    return [
                        {
                            "id": q["id"],
                            "yearRegDidID": q["aa_regdid_id"],
                            "objectId": q["id_oggetto_portale"],
                            "object": json.loads(unicms_object._content)
                            if unicms_object
                            else None,
                            "classObjectId": q["id_classe_oggetto_portale"],
                            "objectText": q["testo_it"]
                            if lang == "it" or not q["testo_en"]
                            else q["testo_en"],
                        }
                    ]

    @extend_schema_field(serializers.ListField())
    def get_otherData(self, obj):
        lang = self.get_requestLang()
        return [
            {
                "id": dato.id,
                "ordine": dato.ordine,
                "title": dato.titolo_it
                if lang == "it" or dato.titolo_en is None
                else dato.titolo_en,
                "text": dato.testo_it
                if lang == "it" or dato.testo_en is None
                else dato.testo_en,
                "link": dato.link,
                "typeId": dato.type_id,
                "type": dato.type,
                "visibile": dato.visibile,
            }
            for dato in obj.sitowebcdstopicarticoliregaltridati_set.all()
        ]

    @extend_schema_field(serializers.ListField())
    def get_subArticles(self, obj):
        lang = self.get_requestLang()
        return [
            {
                "id": sotto.id,
                "ordine": sotto.ordine,
                "title": sotto.titolo_it
                if lang == "it" or sotto.titolo_en is None
                else sotto.titolo_en,
                "text": sotto.testo_it
                if lang == "it" or sotto.testo_en is None
                else sotto.testo_en,
                "visibile": sotto.visibile,
            }
            for sotto in obj.sitowebcdssubarticoliregolamento_set.all()
        ]

    class Meta:
        model = SitoWebCdsTopicArticoliReg
        fields = [
            "id",
            "title",
            "topicId",
            "topicDescription",
            "visibile",
            "order",
            "type",
            "content",
            "subArticles",
            "otherData",
        ]
        language_field_map = {
            "title": {"it": "titolo_it", "en": "titolo_en"},
            "topicDescription": {
                "it": "sito_web_cds_topic.descr_topic_it",
                "en": "sito_web_cds_topic.descr_topic_en",
            },
        }


@extend_schema_serializer(examples=examples.STUDY_PLANS_SERIALIZER_EXAMPLE)
class StudyPlansSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(source="piano_studio_id")
    regDidId = serializers.IntegerField(source="regdid_id")
    # ~ relevanceCod = serializers.CharField(source="attinenza_cod")
    yearCoorteId = serializers.IntegerField(source="aa_coorte_id")
    # ~ yearRegPlanId = serializers.IntegerField(source="aa_regpiani_id")
    # ~ regPlanDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ defFlg = serializers.CharField(source="def_flg")
    statusCod = serializers.CharField(source="stato_piano_studio_cod")
    statusDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ regPlansPdrId = serializers.CharField(source="regpiani_pdr_id")
    # ~ regPlansPdrCod = serializers.CharField(source="regpiani_pdr_cod")
    # ~ regPlansPdrDes = serializers.CharField(source="regpiani_pdr_des")
    # ~ regPlansPdrCoorteIdYear = serializers.CharField(source="regpiani_pdr_aa_coorte_id")
    # ~ regPlansPdrYear = serializers.CharField(source="regpiani_pdr_aa_regpiani_id")
    # ~ flgExpSegStu = serializers.CharField(source="flg_exp_seg_stu")
    cdSDuration = serializers.IntegerField(source="regdid.cds.durata_anni")
    planTabs = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_planTabs(self, obj):
        lang = self.get_requestLang()
        result = {}
        
        for q in obj.schemi.all():
            if q.schema_piano_cod not in result:
                result[q.schema_piano_cod] = []
                
            result[q.schema_piano_cod].append(
                {
                    "id": q.schema_piano_id,
                    "des": q.schema_piano_desc_ita,
                    "cod": q.schema_piano_cod,
                    # ~ "pdsCod": q.pds_regdid.pds_cod,
                    # ~ "pdsDes": q.pds_regdid.pds_des_it,
                    "claMiurCod": q.classe_miur_cod,
                    "claMiurDes": q.classe_miur_desc_ita,
                    "commonFlg": q.pds_regdid.comune_flg,
                    "rules": [
                        {
                            "id": q.reg_sce_id,
                            "des": q.reg_sce_desc_ita,
                            # ~ "vinId": q["vin_id"],
                            "year": q.anno_corso_reg_sce,
                            # ~ if q["apt_slot_ord_num"]
                            # ~ else q["anno_corso"],
                            "regSceCodType": q.tipo_reg_sce_cod,
                            # ~ "regSceCodDes": q.reg_sce_desc_ita,
                            # ~ "sceCodType": q["tipo_sce_cod"],
                            # ~ "eceDesType": q["tipo_sce_des"],
                            "umRegSceCodType": q.tipo_um_reg_sce_cod,
                            "minUnt": q.minimo,
                            "maxUnt": q.massimo,
                            "notePre": q.nota_pre_desc_ita,
                            "notePost": q.nota_post_desc_ita,
                            "filters": q.filtri_reg_sce_desc,
                            # ~ "opzFlg": q["opz_flg"],
                            "af": [
                                {
                                    # ~ "scopeId": q["amb_id_af"],
                                    "AfId": af.activities[0].af_pds_id,
                                    "AfCod": af.activities[0].ana_af_cod,
                                    "AfDescription": af.activities[0].ana_af_desc_ita,
                                    "StudyActivitySemester": set([activity.erog_id.tipo_periodo_did_desc_ita for activity in af.activities if getattr(activity, 'erog_id', None)]),
                                    "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                    "SettCod": set([activity.sett_cod for activity in af.activities]),
                                    "AfType": af.activities[0].ambito_desc_ita if len(af.activities) == 1 else None,
                                    "AfScope": af.activities[0].taf_desc_ita if len(af.activities) == 1 else None,
                                    "afSubModules": [
                                        {
                                            "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                            "StudyActivityCod": m.ana_mod_cod,
                                            "StudyActivityName": m.ana_mod_desc_ita ,
                                            "studyActivityPartitionCod": m.erog_id.part_stu_cod if m.erog_id and m.erog_id.part_stu_cod != "-999999999" else None,
                                            "studyActivityPartitionDes": m.erog_id.part_stu_desc_ita if m.erog_id and m.erog_id.part_stu_desc_ita != "#NULL#" else None,
                                            "StudyActivitySemester": m.erog_id.tipo_periodo_did_desc_ita if m.erog_id else None,
                                            "StudyActivitySettCod": m.sett_cod,
                                            "StudyActivityCreditValue": m.cfu,
                                            "StudyActivityScope": m.ambito_desc_ita,
                                            "StudyActivityType": m.taf_desc_ita,
                                        } for m in af.activities
                                    ] if len(af.activities) > 1 else []
                                   
                                } for af in q.af.all() if af.activities
                            ],
                            "blocchi": [
                                [
                                    {
                                        # ~ "scopeId": q["amb_id_af"],
                                        "AfId": af.activities[0].af_pds_id,
                                        "AfCod": af.activities[0].ana_af_cod,
                                        "AfDescription": af.activities[0].ana_af_desc_ita,
                                        "StudyActivitySemester": af.activities[0].erog_id.tipo_periodo_did_desc_ita if len(af.activities) == 1 and getattr(af.activities[0], 'erog_id', None) else None,
                                        "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                        "SettCod": af.activities[0].sett_cod if len(af.activities) == 1 else None,
                                        "AfType": af.activities[0].ambito_desc_ita if len(af.activities) == 1 else None,
                                        "AfScope": af.activities[0].taf_desc_ita if len(af.activities) == 1 else None,
                                        "afSubModules": [
                                            {
                                                "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                                "StudyActivityCod": m.ana_mod_cod,
                                                "StudyActivityName": m.ana_mod_desc_ita,
                                                "StudyActivitySemester": m.erog_id.tipo_periodo_did_desc_ita if m.erog_id else None,
                                                "StudyActivitySettCod": m.sett_cod,
                                                "StudyActivityCreditValue": m.cfu,
                                                "StudyActivityScope": m.ambito_desc_ita,
                                                "StudyActivityType": m.taf_desc_ita,
                                            } for m in af.activities
                                        ] if len(af.activities) > 1 else []
                                       
                                    } for af in b.af_blocco.all() if af.activities
                                ] for b in q.blocchi.all()
                            ]

                        } for q in q.regole.all()
                    ] 
                } 
            )
        return result
        
    class Meta:
        model = DidatticaPianiStudio
        fields = [
            "id",
            "regDidId",
            # ~ "relevanceCod",
            "yearCoorteId",
            # ~ "yearRegPlanId",
            # ~ "regPlanDes",
            # ~ "defFlg",
            "statusCod",
            "statusDes",
            # ~ "regPlansPdrId",
            # ~ "regPlansPdrCod",
            # ~ "regPlansPdrDes",
            # ~ "regPlansPdrCoorteIdYear",
            # ~ "regPlansPdrYear",
            # ~ "flgExpSegStu",
            "cdSDuration",
            "planTabs",
        ]
