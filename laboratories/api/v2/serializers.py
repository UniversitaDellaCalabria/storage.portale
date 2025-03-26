from rest_framework import serializers

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from generics.api.serializers import ReadOnlyModelSerializer
from laboratories.models import (
    LaboratorioDatiBase,
    LaboratorioTipologiaAttivita,
    LaboratorioInfrastruttura
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from generics.utils import encrypt


class LaboratoriesAreaSerializer(ReadOnlyModelSerializer):
    area = serializers.CharField(source="ambito")
    class Meta:
        model = LaboratorioDatiBase
        fields = ["area"]
        
class LaboratoriesScopesSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descrizione")
    class Meta:
        model = LaboratorioTipologiaAttivita
        fields = ["id", "description"]
        
class InfrastructuresSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField(source="descrizione")
    class Meta:
        model = LaboratorioInfrastruttura
        fields = ["id", "description"]

class Erc0ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }
class Erc1ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    erc1List = serializers.SerializerMethodField()
    
    def get_erc1List(self, obj):
        return [
            {
                "codErc1": erc1["cod_erc1"],
                "description": erc1["descrizione"],
            }
            for erc1 in obj["erc1_list"]
        ]
    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "erc1List"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }
        
class Erc2ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    erc1List = serializers.SerializerMethodField()
    
    def get_erc1List(self, obj):
        return [
            {
                "codErc1": erc1["cod_erc1"],
                "description": erc1["descrizione"],
                "erc2List": [
                    {
                        "codErc2": erc2["cod_erc2"],
                        "description": erc2["descrizione"],
                    }
                    for erc2 in erc1.get("erc2_list") 
                ],
            }
            for erc1 in obj.get("erc1_list")
        ]


    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "erc1List"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }
class Aster1ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    aster1_list = serializers.SerializerMethodField()
    
    def get_aster1_list(self, obj):
        return [
            {
                "idAster1": a["id"],
                "description": a["descrizione"],
            }
            for a in obj.get("aster1_list")
        ]


    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "aster1_list"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }
        
class Aster2ListSerializer(serializers.ModelSerializer):
    idErc0 = serializers.CharField(source="erc0_cod")
    description = serializers.CharField()
    aster1_list = serializers.SerializerMethodField()
    
    def get_aster1_list(self, obj):
        return [
            {
                "idAster1": a["id"],
                "description": a["descrizione"],
                "aster2_list": [
                    {
                        "idAster2": a2["id"],
                        "description": a2["descrizione"],
                    }
                    for a2 in a.get("aster2_list")
                ],                
            }
            for a in obj.get("aster1_list")
        ]


    class Meta:
        model = RicercaErc0
        fields = ["idErc0", "description", "aster1_list"]
        language_field_map = {
            "description": {"it": "descrizione", "en": "descrizione_en"},
        }