from rest_framework import serializers
from generics.utils import build_media_path, encrypt


class PatentsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        query = instance
        data = super().to_representation(instance)
        data.update(self.to_dict(query, str(self.context["language"]).lower()))
        return data

    @staticmethod
    def to_dict(query, req_lang="en"):
        inventors = None
        if query.get("Inventori") is not None:
            inventors = PatentsSerializer.to_dict_inventors(query["Inventori"])
        return {
            "PatentId": query["id"],
            "PatentUniqueId": query["id_univoco"],
            "PatentTitle": query["titolo"],
            "PatentImage": build_media_path(query["nome_file_logo"]),
            "PatentAbstract": query["breve_descrizione"],
            "PatentUrlKnowledgeShare": query["url_knowledge_share"],
            "PatentInizialTRL": query["trl_iniziale"],
            "PatentUpdatedTRL": query["trl_aggiornato"],
            "PatentEnhancement": query["valorizzazione"],
            "PatentTechAreaId": query["area_tecnologica"],
            "PatentAreaDescription": query["area_tecnologica__descr_area_ita"]
            if req_lang == "it" or query["area_tecnologica__descr_area_eng"] is None
            else query["area_tecnologica__descr_area_eng"],
            "PatentInventors": inventors,
            "PatentIsActive": query["is_active"],
        }

    @staticmethod
    def to_dict_inventors(query):
        result = []
        for q in query:
            full_name = q["cognomenome_origine"]
            result.append(
                {
                    "AuthorId": encrypt(q["matricola_inventore"]),
                    "AuthorName": full_name,
                }
            )
        return result
