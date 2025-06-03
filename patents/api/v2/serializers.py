from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.utils import build_media_path, encrypt
from generics.api.serializers import ReadOnlyModelSerializer
from patents.models import BrevettoDatiBase


@extend_schema_serializer(examples=examples.PATENTS_SERIALIZER_EXAMPLE)
class PatentsSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    uniqueId = serializers.IntegerField(source="id_univoco")
    title = serializers.CharField(source="titolo")
    image = serializers.SerializerMethodField()
    abstract = serializers.CharField(source="breve_descrizione")
    urlKnowledgeShare = serializers.CharField(source="url_knowledge_share")
    inizialTRL = serializers.CharField(source="trl_iniziale")
    updatedTRL = serializers.CharField(source="trl_aggiornato")
    enhancement = serializers.CharField(source="valorizzazione")
    techAreaId = serializers.CharField(source="area_tecnologica")
    areaDescription = serializers.CharField(source="area_tecnologica.descr_area_ita")
    inventors = serializers.SerializerMethodField()
    isActive = serializers.CharField(source="is_active")

    @extend_schema_field(serializers.CharField())
    def get_image(self, obj):
        return build_media_path(obj.nome_file_logo)

    @extend_schema_field(serializers.ListField())
    def get_inventors(self, obj):
        return [
            {
                "authorId": encrypt(inv.matricola_inventore),
                "authorName": inv.cognomenome_origine,
            }
            for inv in obj.inventori
        ]

    class Meta:
        model = BrevettoDatiBase
        fields = [
            "id",
            "uniqueId",
            "title",
            "image",
            "abstract",
            "urlKnowledgeShare",
            "inizialTRL",
            "updatedTRL",
            "enhancement",
            "techAreaId",
            "areaDescription",
            "inventors",
            "isActive",
        ]
        language_field_map = {
            "areaDescription": {
                "it": "area_tecnologica.descr_area_ita",
                "en": "area_tecnologica.descr_area_eng",
            }
        }
