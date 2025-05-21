from rest_framework import serializers

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from addressbook.models import Personale
from structures.models import UnitaOrganizzativa

class PersonnelCfSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    Cf = serializers.CharField(source="cod_fis")
    ID = serializers.CharField(source="matricola")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    role = serializers.CharField(source="cd_ruolo")
    infrastructureId = serializers.CharField(source="cd_uo_aff_org")
    infrastructureDescription = serializers.CharField(source="ds_aff_org")

    def get_name(self, obj):
        full_name = obj.cognome + " " + obj.nome
        if obj.middle_name:
            full_name += " " + obj.middle_name
        return full_name

    class Meta:
        model = Personale
        fields = [
            "name",
            "Cf",
            "ID",
            "roleDescription",
            "role",
            "infrastructureId",
            "infrastructureDescription",
        ]

class AddressbookStructuresSerializer(serializers.ModelSerializer):
    cod = serializers.CharField(source="uo")
    name = serializers.CharField(source="denominazione")
    typeName = serializers.CharField(source="cd_tipo_nodo")
    typeCOD = serializers.CharField(source="ds_tipo_nodo")
    
    class Meta:
        model = UnitaOrganizzativa
        fields = [
            "cod",
            "name",
            "typeName",
            "typeCOD",
        ]

class RolesSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")

    class Meta:
        model = Personale
        fields = ["role", "roleDescription"]
