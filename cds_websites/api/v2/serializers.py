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


