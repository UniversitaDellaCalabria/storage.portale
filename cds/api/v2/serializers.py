from collections import defaultdict

from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)
from generics.serializers import ReadOnlyModelSerializer
from generics.utils import encrypt
from rest_framework import serializers


from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsTipoCorso,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaCdsCollegamento
)


class CdsSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaCds
        fields = "__all__"


class CdsAreasSerializer(ReadOnlyModelSerializer):
    areaCds = serializers.CharField(source="area_cds")

    class Meta:
        model = DidatticaCds
        fields = [
            "areaCds",
        ]
        language_field_map = {
            "areaCds": {"it": "area_cds", "en": "area_cds_en"},
        }

class CdsExpiredSerializer(ReadOnlyModelSerializer):
    cdsCod = serializers.CharField(source="cds.cds_cod")
    aaRegDid = serializers.CharField(source="aa_reg_did")
    cdsDuration = serializers.CharField(source="cds.durata_anni")

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "cdsCod",
            "aaRegDid",
            "cdsDuration",
        ]


class DegreeTypeSerializer(ReadOnlyModelSerializer):
    courseType = serializers.CharField(source="tipo_corso_cod")
    courseTypeDescription = serializers.CharField(source="tipo_corso_des")
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = [
            "courseType",
            "courseTypeDescription",
        ]

class AcademicYearsSerializer(ReadOnlyModelSerializer):
    aaRegDid = serializers.CharField(source="aa_reg_did")
    class Meta:
        model = DidatticaRegolamento
        fields = [
            "aaRegDid",
        ]


class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = "__all__"


class StudyActivitiesListSerializer(ReadOnlyModelSerializer):
    id = serializers.CharField(source="af_id")
    genCod = serializers.CharField(source="af_gen_cod")
    des = serializers.CharField(source="group_description")
    cdsId = serializers.CharField(source="cds_id")
    cdsCod = serializers.CharField(source="cds.cds_cod")
    language = serializers.SerializerMethodField()
    fatherCode = serializers.CharField(source="af_radice_id")
    fatherName = serializers.CharField()
    regDidId = serializers.CharField(source="regdid_id")
    dipDes = serializers.CharField(source="cds.dip.dip_des_it")
    dipCod = serializers.CharField(source="cds.dip.dip_cod")
    courseYear = serializers.CharField(source="anno_corso")
    academicYear = serializers.CharField(source="aa_off_id")
    semester = serializers.CharField(source="ciclo_des")
    SSDCod = serializers.CharField(source="sett_cod")
    SSD = serializers.CharField(source="sett_des")
    partitionCod = serializers.CharField(source="part_stu_cod")
    partitionDes = serializers.CharField(source="part_stu_des")
    extendedPartitionCod = serializers.CharField(source="fat_part_stu_cod")
    extendedPartitionDes = serializers.CharField(source="fat_part_stu_des")
    cdsName = serializers.CharField(source="cds.nome_cds_it")
    teacherId = serializers.SerializerMethodField()
    teacherName = serializers.CharField(source="full_name")
    studyPlanDes = serializers.CharField(source="pds_des")

    def get_language(self, obj):
        list_language = getattr(obj, "lista_lin_did_af", None)
        if list_language:
            return list_language.replace(" ", "").split(",")
        return []

    def get_teacherId(self, obj):
        matricola = getattr(obj, "matricola_resp_did", None)
        return encrypt(matricola)

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = [
            "id",
            "genCod",
            "des",
            "cdsId",
            "cdsCod",
            "language",
            "fatherCode",
            "fatherName",
            "regDidId",
            "dipDes",
            "dipCod",
            "courseYear",
            "academicYear",
            "semester",
            "SSDCod",
            "SSD",
            "partitionCod",
            "partitionDes",
            "extendedPartitionCod",
            "extendedPartitionDes",
            "cdsName",
            "teacherId",
            "teacherName",
            "studyPlanDes"
        ]
        language_field_map = {
            "des": {"it": "group_description", "en": "af_gen_des_eng"},
            "dipDes": {"it": "cds.dip.dip_des_it", "en": "cds.dip.dip_des_eng"},
            "cdsName": {"it": "cds.nome_cds_it", "en": "cds.nome_cds_eng"},
        }
        
class CdsMorphSerializer(ReadOnlyModelSerializer):
    
    class Meta:
        model = DidatticaCdsCollegamento
        fields = "__all__"

class StudyActivitiesLiteSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(source="af_id")
    name = serializers.CharField(source="des")
    year = serializers.IntegerField(source="anno_corso")
    cycle = serializers.CharField(source="ciclo_des")
    etcs = serializers.IntegerField(source="peso")
    type = serializers.CharField(source="tipo_af_des")

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = ["id", "name", "year", "cycle", "etcs", "type"]


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


class AcademicPathwaysDetailSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(
        source="pds_regdid_id", help_text="The ID of the academic pathway."
    )
    cod = serializers.CharField(
        source="pds_cod", help_text="The code of the academic pathway."
    )
    name = serializers.CharField(
        source="pds_des_it", help_text="The name of the academic pathway."
    )
    activities = serializers.SerializerMethodField(method_name="get_activities_by_year")

    @extend_schema_field(StudyActivitiesLiteSerializer(many=True))
    def get_activities_by_year(self, obj):
        activities = obj.didatticaattivitaformativa_set.all()
        grouped_data = defaultdict(list)
        for activity in activities:
            grouped_data[activity.anno_corso].append(
                StudyActivitiesLiteSerializer(activity).data
            )
        return grouped_data

    class Meta:
        model = DidatticaPdsRegolamento
        fields = ["id", "cod", "name", "activities"]
