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
from cds.models import DidatticaPianoRegolamento


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
    id = serializers.IntegerField(source="regpiani_id")
    regDidId = serializers.IntegerField(source="regdid_id")
    relevanceCod = serializers.CharField(source="attinenza_cod")
    yearCoorteId = serializers.CharField(source="aa_coorte_id")
    yearRegPlanId = serializers.IntegerField(source="aa_regpiani_id")
    regPlanDes = serializers.CharField(source="des")
    defFlg = serializers.CharField(source="def_flg")
    statusCod = serializers.CharField(source="stato_cod")
    statusDes = serializers.CharField(source="stato_des")
    regPlansPdrId = serializers.CharField(source="regpiani_pdr_id")
    regPlansPdrCod = serializers.CharField(source="regpiani_pdr_cod")
    regPlansPdrDes = serializers.CharField(source="regpiani_pdr_des")
    regPlansPdrCoorteIdYear = serializers.CharField(source="regpiani_pdr_aa_coorte_id")
    regPlansPdrYear = serializers.CharField(source="regpiani_pdr_aa_regpiani_id")
    flgExpSegStu = serializers.CharField(source="flg_exp_seg_stu")
    cdSDuration = serializers.CharField(source="regdid__cds__durata_anni")
    planTabs = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_planTabs(self, obj):
        lang = self.get_requestLang()
        if obj["PlanTabs"] is not None:
            return [
                {
                    "id": q["sche_piano_id"],
                    "des": q["sche_piano_des"],
                    "cod": q["sche_piano_cod"],
                    "pdsCod": q["pds_cod"],
                    "pdsDes": q["pds_des"],
                    "claMiurCod": q["cla_miur_cod"],
                    "claMiurDes": q["cla_miur_des"],
                    "commonFlg": q["comune_flg"],
                    "statutario": q["isStatutario"],
                    "APT": True if q["apt_id"] else False,
                    "afRequired": [
                        {
                            "id": q["sce_id"],
                            "des": q["sce_des"],
                            "vinId": q["vin_id"],
                            "year": q["apt_slot_ord_num"]
                            if q["apt_slot_ord_num"]
                            else q["anno_corso"],
                            "regSceCodType": q["tipo_regsce_cod"],
                            "sceCodType": q["tipo_sce_cod"],
                            "eceDesType": q["tipo_sce_des"],
                            "regSceCodDes": q["tipo_regsce_des"],
                            "umRegSceCodType": q["tipo_um_regsce_cod"],
                            "minUnt": q["min_unt"],
                            "maxUnt": q["max_unt"],
                            "opzFlg": q["opz_flg"],
                            "required": [
                                {
                                    "scopeId": q["amb_id_af"],
                                    "sceId": q["sce_id"],
                                    "sceDes": q["sce_id__sce_des"],
                                    "scopeDes": q["ambito_des_af"],
                                    "settCod": q.get("sett_cod", None),
                                    "creditValue": q["peso"],
                                    "cycleDes": q["ciclo_des"],
                                    "afDescription": q["af_gen_des"],
                                    "afId": q["af_id"],
                                    "afCod": q["af_gen_cod"],
                                    "afType": q["tipo_af_des_af"],
                                    "afScope": q["ambito_des_af"],
                                    "afSubModules": [
                                        {
                                            "id": q["af_id"],
                                            "cod": q["af_gen_cod"],
                                            "name": q["des"]
                                            if lang == "it" or q["af_gen_des_eng"] is None
                                            else q["af_gen_des_eng"],
                                            "semester": q["ciclo_des"],
                                            "sttCod": q.get("sett_cod", None),
                                            "creditValue": q["peso"],
                                            "partitionCod": q["part_stu_cod"],
                                            "partitionDescription": q["part_stu_des"],
                                            "extendedPartitionCod": q["fat_part_stu_cod"],
                                            "extendedPartitionDes": q["fat_part_stu_des"],
                                        }
                                        for q in q.get("MODULES", [])
                                    ],
                                }
                                for q in q.get("Required", [])
                            ],
                            "choices": [
                                {
                                    "scopeId": q["amb_id_af"],
                                    "sceId": q["sce_id"],
                                    "sceDes": q["sce_id__sce_des"],
                                    "scopeDes": q["ambito_des_af"],
                                    "settCod": q.get("sett_cod", None),
                                    "creditValue": q["peso"],
                                    "cycleDes": q["ciclo_des"],
                                    "afDescription": q["af_gen_des"],
                                    "afId": q["af_id"],
                                    "afCod": q["af_gen_cod"],
                                    "afType": q["tipo_af_des_af"],
                                    "afScope": q["ambito_des_af"],
                                    "afSubModules": [
                                        {
                                            "id": q["af_id"],
                                            "cod": q["af_gen_cod"],
                                            "name": q["des"]
                                            if lang == "it" or q["af_gen_des_eng"] is None
                                            else q["af_gen_des_eng"],
                                            "semester": q["ciclo_des"],
                                            "sttCod": q.get("sett_cod", None),
                                            "creditValue": q["peso"],
                                            "partitionCod": q["part_stu_cod"],
                                            "partitionDescription": q["part_stu_des"],
                                            "extendedPartitionCod": q["fat_part_stu_cod"],
                                            "extendedPartitionDes": q["fat_part_stu_des"],
                                        }
                                        for q in q.get("MODULES", [])
                                    ],
                                }
                                for q in q.get("Required", [])
                            ],
                            "filAnd": [
                                {
                                    "filAndId": q["sce_fil_and_id"],
                                    "sceId": q["sce_id"],
                                    "filOrId": q["sce_fil_or_id"],
                                    "filOrDes": q["sce_fil_or_des"],
                                    "tipoFiltroCod": q["tipo_filtro_cod"],
                                    "tipoFiltroDes": q["tipo_filtro_des"],
                                    "courseTypeSceFilAndCod": q["tipo_corso_sce_fil_and_cod"],
                                    "cdsSceFilAndId": q["cds_sce_fil_and_id"],
                                    "cdsSceFilAndCod": q["cds_sce_fil_and_cod"],
                                    "cdsSceFilAndNome": q["cds_sce_fil_and_nome"],
                                    "notFlg": q["not_flg"],
                                }
                                for q in q.get("FilAnd", [])
                            ],
                        }
                        for q in q.get("AfRequired", []) 
                    ],                       
                }
                for q in obj["PlanTabs"]
            ]
                

    class Meta:
        model = DidatticaPianoRegolamento
        fields = [
            "id",
            "regDidId",
            "relevanceCod",
            "yearCoorteId",
            "yearRegPlanId",
            "regPlanDes",
            "defFlg",
            "statusCod",
            "statusDes",
            "regPlansPdrId",
            "regPlansPdrCod",
            "regPlansPdrDes",
            "regPlansPdrCoorteIdYear",
            "regPlansPdrYear",
            "flgExpSegStu",
            "cdSDuration",
            "planTabs",
        ]
