from generics.utils import encrypt
from rest_framework import serializers

from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsTipoCorso,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
)

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class CdsSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCds
        fields = "__all__"


class CdsAreasSerializer(ReadOnlyModelSerializer):
    area_cds = serializers.SerializerMethodField()

    def get_area_cds(self, obj):
        language = self.context.get("request").LANGUAGE_CODE.lower()
        if language == "en" and obj.get("area_cds_en"):
            return obj.get("area_cds_en")
        return obj.get("area_cds")

    class Meta:
        model = DidatticaCds
        fields = [
            "area_cds",
        ]


class CdsExpiredSerializer(ReadOnlyModelSerializer):
    cds_cod = serializers.CharField(source="cds.cds_cod", default=None)
    cds_duration = serializers.CharField(source="cds.durata_anni", default=None)

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "cds_cod",
            "aa_reg_did",
            "cds_duration",
        ]


class DegreeTypeSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = ["tipo_corso_cod", "tipo_corso_des"]


class DidatticaAttivitaFormativaSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = "__all__"


class AcademicYearsSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaRegolamento
        fields = [
            "aa_reg_did",
        ]


class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = "__all__"


class StudyActivitiesListSerializer(ReadOnlyModelSerializer):
    cds_cod = serializers.CharField(source="cds.cds_cod")
    dip_des_it = serializers.CharField(source="cds.dip.dip_des_it")
    dip_des_eng = serializers.CharField(source="cds.dip.dip_des_eng")
    dip_cod = serializers.CharField(source="cds.dip.dip_cod")

    nome_cds_it = serializers.CharField(source="cds.nome_cds_it")
    nome_cds_eng = serializers.CharField(source="cds.nome_cds_eng")

    full_name = serializers.CharField()
    group_description = serializers.CharField()

    lista_lin_did_af = serializers.SerializerMethodField()
    matricola_resp_did = serializers.SerializerMethodField()

    father = serializers.SerializerMethodField()

    def get_lista_lin_did_af(self, obj):
        lista_lin_did_af = getattr(obj, "lista_lin_did_af", None)
        if lista_lin_did_af:
            return lista_lin_did_af.replace(" ", "").split(",")
        return []

    def get_matricola_resp_did(self, obj):
        matricola = getattr(obj, "matricola_resp_did", None)
        return encrypt(matricola)

    def get_father(self, obj):
        return getattr(obj, "father", None)

    """
    dip_des = serializers.SerializerMethodField()
    
    def get_group_description(self, obj):
        for i in self.get_lista_lin_did_af(obj):
            if "IT" not in i or obj.af_gen_des_eng:
                return obj.af_gen_des_eng

    def get_dip_des(self, obj):
        for i in self.get_lista_lin_did_af(obj):
            if "IT" not in i or obj.dip_des_eng:
                return obj.dip_des_it
        return obj.dip_des_eng
    """

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = [
            "af_id",
            "af_gen_cod",
            "group_description",
            "af_gen_des_eng",
            "cds_id",
            "cds_cod",
            "lista_lin_did_af",
            "af_radice_id",
            "father",
            "regdid_id",
            "dip_des_it",
            "dip_des_eng",
            "dip_cod",
            "anno_corso",
            "aa_off_id",
            "ciclo_des",
            "sett_cod",
            "sett_des",
            "part_stu_cod",
            "part_stu_des",
            "fat_part_stu_cod",
            "fat_part_stu_des",
            "nome_cds_it",
            "nome_cds_eng",
            "matricola_resp_did",
            "full_name",
            "pds_des",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Single",
            value=[
                {
                    "id": 1,
                    "cod": "123",
                    "name": "GENERIC",
                    "duration": 2,
                }
            ],
            description="Single academic pathway",
        ),
        OpenApiExample(
            "Multiple",
            value=[
                {
                    "id": 1,
                    "cod": "123",
                    "name": "GENERIC",
                    "duration": 2,
                },
                {
                    "id": 2,
                    "cod": "321",
                    "name": "OTHER",
                    "duration": 3,
                },
            ],
            description="Multiple academic pathways",
        ),
    ]
)
class AcademicPathwaysListSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(
        source="pds_regdid_id", help_text="The ID of the academic pathway."
    )
    cod = serializers.CharField(
        source="pds_cod", help_text="The code of the academic pathway."
    )
    name = serializers.CharField(
        source="pds_des_it", help_text="The name of the academic pathway."
    )
    duration = serializers.IntegerField(
        help_text="The duration in years of the academic pathway."
    )

    class Meta:
        model = DidatticaPdsRegolamento
        fields = ["id", "cod", "name", "duration"]
