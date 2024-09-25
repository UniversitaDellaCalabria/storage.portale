import json

import requests
from cds_websites.models import SitoWebCdsOggettiPortale
from cds_websites.settings import UNICMS_OBJECT_API
from generics.serializers import CreateUpdateAbstract
from generics.settings import UNICMS_AUTH_TOKEN
from rest_framework import serializers


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
                    api_url.format(q["id_oggetto_portale"]), headers=head, timeout=5
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
