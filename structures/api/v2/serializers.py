from rest_framework import serializers

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from structures.models import (
    UnitaOrganizzativa,
    UnitaOrganizzativaFunzioni,
    DidatticaDipartimento,
)
from generics.utils import encrypt


class ChildStructureSerializer(serializers.Serializer):
    cod = serializers.CharField(source="uo")
    name = serializers.CharField(source="denominazione")
    typeName = serializers.CharField(source="ds_tipo_nodo")
    typeCOD = serializers.CharField(source="cd_tipo_nodo")


@extend_schema_serializer(examples=examples.STRUCTURES_LIST_EXAMPLES)
class StructuresSerializer(serializers.ModelSerializer):
    cod = serializers.CharField(source="uo")
    name = serializers.CharField(source="denominazione")
    typeName = serializers.CharField(source="ds_tipo_nodo")
    typeCOD = serializers.CharField(source="cd_tipo_nodo")
    URL = serializers.SerializerMethodField()
    childs = ChildStructureSerializer(many=True, required=False)

    @extend_schema_field(serializers.CharField())
    def get_URL(self, obj):
        return obj["urls"]["dip_url"] if obj["urls"] else ""

    class Meta:
        model = UnitaOrganizzativa
        fields = ["cod", "name", "typeName", "typeCOD", "URL", "childs"]


@extend_schema_serializer(examples=examples.STRUCTURE_DETAIL_EXAMPLES)
class StructureSerializer(serializers.ModelSerializer):
    cod = serializers.CharField(source="uo")
    name = serializers.CharField(source="denominazione")
    typeName = serializers.CharField(source="ds_tipo_nodo")
    typeCOD = serializers.CharField(source="cd_tipo_nodo")
    fatherId = serializers.CharField(source="uo_padre")
    fatherName = serializers.CharField(source="denominazione_padre")
    email = serializers.SerializerMethodField()
    pec = serializers.SerializerMethodField()
    tfr = serializers.SerializerMethodField()
    personnelFunctions = serializers.SerializerMethodField()
    mission = serializers.CharField(source="ds_mission")
    URL = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_personnelFunctions(self, obj):
        for f in obj.funzioni:
            full_name = f.cod_fis.cognome + " " + f.cod_fis.nome
            if f.cod_fis.middle_name is not None:
                full_name = full_name + " " + f.cod_fis.middle_name
            return [
                {
                    "id": encrypt(f.cod_fis.matricola),
                    "name": full_name,
                    "function": f.ds_funzione,
                    "functionCod": f.funzione,
                }
            ]

    @extend_schema_field(serializers.CharField())
    def get_URL(self, obj):
        return getattr(obj, "urls", None)

    def contacts(self, obj, contact_type):
        contatto_obj = getattr(obj, "unitaorganizzativacontatti", None)
        if (
            contatto_obj
            and getattr(contatto_obj.cd_tipo_cont, "pk", None) == contact_type
        ):
            return [contatto_obj.contatto]
        return []

    @extend_schema_field(serializers.CharField())
    def get_email(self, obj):
        return self.contacts(obj, "EMAIL")

    @extend_schema_field(serializers.CharField())
    def get_pec(self, obj):
        return self.contacts(obj, "PEC")

    @extend_schema_field(serializers.CharField())
    def get_tfr(self, obj):
        return self.contacts(obj, "TFR")

    class Meta:
        model = UnitaOrganizzativa
        fields = [
            "cod",
            "name",
            "typeName",
            "typeCOD",
            "fatherId",
            "fatherName",
            "email",
            "pec",
            "tfr",
            "personnelFunctions",
            "mission",
            "URL",
        ]


@extend_schema_serializer(examples=examples.STRUCTURE_TYPES_EXAMPLES)
class TypesSerializer(serializers.ModelSerializer):
    typeName = serializers.CharField(source="ds_tipo_nodo")
    typeCOD = serializers.CharField(source="cd_tipo_nodo")

    class Meta:
        model = UnitaOrganizzativa
        fields = [
            "typeName",
            "typeCOD",
        ]


@extend_schema_serializer(examples=examples.STRUCTURE_FUNCTIONS_EXAMPLES)
class FunctionSerializer(serializers.ModelSerializer):
    typeCOD = serializers.CharField(source="cd_tipo_nod")
    function = serializers.CharField(source="funzione")
    functionDescription = serializers.CharField(source="descr_funzione")

    class Meta:
        model = UnitaOrganizzativaFunzioni
        fields = [
            "typeCOD",
            "function",
            "functionDescription",
        ]


@extend_schema_serializer(examples=examples.DEPARTMENTS_EXAMPLES)
class DepartmentsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="dip_id")
    cod = serializers.CharField(source="dip_cod")
    name = serializers.CharField(source="dip_des_it")
    nameShort = serializers.CharField(source="dip_nome_breve")
    URL = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_URL(self, obj):
        return getattr(obj, "urls", None)

    class Meta:
        model = DidatticaDipartimento
        fields = ["id", "cod", "name", "nameShort", "URL"]
        language_field_map = {
            "name": {"it": "dip_des_it", "en": "dip_des_eng"},
        }
