from rest_framework import serializers
from generics.utils import encrypt

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from addressbook.models import Personale

class TeachersSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    departmentId = serializers.IntegerField(source="dip_id")
    departmentCod = serializers.CharField(source="dip_cod")
    departmentName = serializers.CharField(source="dip_des_it")
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    SSDCod = serializers.CharField(source="cd_ssd")
    SSDDescription = serializers.CharField(source="ds_ssd")
    CVFull = serializers.CharField(source="cv_full_it")
    CVShort = serializers.CharField(source="cv_short_it")
    profileId = serializers.IntegerField(source="profilo")
    profileDescription = serializers.CharField(source="ds_profilo")
    profileShortDescription = serializers.CharField(source="ds_profilo_breve")
    email = serializers.SerializerMethodField()
    
    def get_email(self, obj):
        return obj["email"] if obj["email"] != "" and obj["email"] is not None else []
    
    def get_id(self, obj):
        return encrypt(obj["matricola"])
    
    def get_name(self, obj):
        return (obj["cognome"] + " " + obj["nome"] + (" " + obj["middle_name"] if obj["middle_name"] else ""))

    class Meta:
        model = Personale
        fields = [
            "id",
            "name",
            "departmentId",
            "departmentCod",
            "departmentName",
            "role",
            "roleDescription",
            "SSDCod",
            "SSDDescription",
            "CVFull",
            "CVShort",
            "profileId",
            "profileDescription",
            "profileShortDescription",
            "email"
        ]
        language_field_map = {
            "CVFull": {"it": "cv_full_it", "en": "cv_full_eng"},
            "CVShort": {"it": "cv_short_it", "en": "cv_short_eng"},
            "departmentName": {"it": "dip_des_it", "en": "dip_des_eng"},
        }
        
        
        