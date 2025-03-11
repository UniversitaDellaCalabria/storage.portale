from rest_framework import serializers

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from generics.api.serializers import ReadOnlyModelSerializer
from companies.models import (
    SpinoffStartupDatiBase,
    SpinoffStartupDipartimento,
    TipologiaAreaTecnologica,
)
from generics.utils import build_media_path, encrypt


class CompaniesSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    PIva = serializers.CharField(source="piva")
    agencyName = serializers.CharField(source="nome_azienda")
    agencyUrl = serializers.CharField(source="url_sito_web")
    image = serializers.SerializerMethodField()
    description = serializers.CharField(source="descrizione_ita")
    unicalReferent = serializers.CharField(source="referente_unical")
    unicalReferentId = serializers.SerializerMethodField()
    techAreaId = serializers.IntegerField(source="area_tecnologica")
    techAreaDescription = serializers.CharField(source="area_tecnologica__descr_area_ita")
    isSpinoff = serializers.BooleanField(source="is_spinoff")
    isStartup = serializers.BooleanField(source="is_startup")
    isActive = serializers.BooleanField(source="is_active")

    def get_image(self, obj):
        return build_media_path(obj["nome_file_logo"])
    
    def get_unicalReferentId(self, obj):
        return encrypt(obj["matricola_referente_unical"])
    
    class Meta:
        model = SpinoffStartupDatiBase
        fields = [
            "id",
            "PIva",
            "agencyName", 
            "agencyUrl",
            "image", 
            "description",
            "unicalReferent",
            "unicalReferentId", 
            "techAreaId",
            "techAreaDescription",
            "isSpinoff",
            "isStartup",
            "isActive",
        ]
        language_field_map = {
            "description": {"it": "descrizione_ita", "en": "descrizione_eng"},
            "techAreaDescription": {"it": "area_tecnologica__descr_area_ita", "en": "area_tecnologica__descr_area_eng"}
        }
        
class TechAreaSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descr_area_ita")

    class Meta:
        model = SpinoffStartupDatiBase
        fields = [
            "id",
            "description",
        ]
        language_field_map = {
            "description": {"it": "descr_area_ita", "en": "descr_area_eng"}
        }