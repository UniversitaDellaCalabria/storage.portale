from rest_framework import serializers

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from addressbook.models import Personale


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
        
class RolesSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    
    class Meta:
        model = Personale
        fields = ["role", "roleDescription"]