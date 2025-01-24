from collections import defaultdict
from .docs import examples

from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.serializers import ReadOnlyModelSerializer
from generics.utils import encrypt, build_media_path
from rest_framework import serializers


from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsTipoCorso,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaCdsCollegamento,
)

@extend_schema_serializer(
    examples=examples.CDS_SERIALIZER_EXAMPLE
)
class CdsSerializer(ReadOnlyModelSerializer):
    regDidId = serializers.IntegerField(source="regdid_id")
    cdSId = serializers.IntegerField(source="cds.cds_id")
    cdSCod = serializers.CharField(source="cds.cds_cod")
    academicYear = serializers.IntegerField(source="aa_reg_did")
    name = serializers.CharField(source="cds.nome_cds_it")
    area = serializers.CharField(source="cds.area_cds")
    departmentId = serializers.IntegerField(source="cds.dip.dip_id")
    departmentCod = serializers.CharField(source="cds.dip.dip_cod")
    departmentName = serializers.CharField(source="cds.dip.dip_des_it")
    type = serializers.CharField(source="cds.tipo_corso_cod")
    typeDescription = serializers.CharField(source="cds.tipo_corso_des")
    courseClassCod = serializers.CharField(source="cds.cla_miur_cod")
    courseClassName = serializers.CharField(source="cds.cla_miur_des")
    courseInterClassCod = serializers.CharField(source="cds.intercla_miur_cod")
    courseInterClassDes = serializers.CharField(source="cds.intercla_miur_des")
    erogationMode = serializers.CharField(source="modalita_erogazione")
    languages = serializers.SerializerMethodField(method_name="get_languages")
    duration = serializers.IntegerField(source="cds.durata_anni")
    ECTS = serializers.IntegerField(source="cds.valore_min")
    mandatoryAttendance = serializers.SerializerMethodField(
        method_name="get_mandatory_attendance"
    )
    status = serializers.CharField(source="stato_regdid_cod")
    jointDegree = serializers.CharField(source="titolo_congiunto_cod")
    studyManifesto = serializers.SerializerMethodField(
        method_name="get_study_manifesto"
    )
    didacticRegulation = serializers.SerializerMethodField(
        method_name="get_didactic_regulation"
    )
    ordinamentoDidattico = serializers.SerializerMethodField(
        method_name="get_ordinamento_didattico"
    )
    yearOrdinamentoDidattico = serializers.IntegerField(source="cds.aa_ord_id")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_languages(self, obj):
        return [lang.iso6392_cod for lang in obj.cds.lingue]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_study_manifesto(self, obj):
        if not hasattr(obj, "didatticacdsaltridati") or not hasattr(
            obj.didatticacdsaltridati, "manifesto_studi"
        ):
            return None
        return build_media_path(
            getattr(obj.didatticacdsaltridati.manifesto_studi, "name")
        )

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_didactic_regulation(self, obj):
        if not hasattr(obj, "didatticacdsaltridati") or not hasattr(
            obj.didatticacdsaltridati, "regolamento_didattico"
        ):
            return None
        return build_media_path(
            getattr(obj.didatticacdsaltridati.regolamento_didattico, "name")
        )

    @extend_schema_field(serializers.CharField())
    def get_ordinamento_didattico(self, obj):
        return build_media_path(obj.ordinamento_didattico)

    @extend_schema_field(serializers.BooleanField())
    def get_mandatory_attendance(self, obj):
        return bool(obj.frequenza_obbligatoria)

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "regDidId",
            "cdSId",
            "cdSCod",
            "academicYear",
            "name",
            "area",
            "departmentId",
            "departmentCod",
            "departmentName",
            "type",
            "typeDescription",
            "courseClassCod",
            "courseClassName",
            "courseInterClassCod",
            "courseInterClassDes",
            "erogationMode",
            "languages",
            "duration",
            "ECTS",
            "mandatoryAttendance",
            "status",
            "jointDegree",
            "studyManifesto",
            "didacticRegulation",
            "ordinamentoDidattico",
            "yearOrdinamentoDidattico",
        ]


@extend_schema_serializer(
    examples=examples.CDS_AREA_SERIALIZER_EXAMPLE
)
class CdsAreasSerializer(ReadOnlyModelSerializer):
    areaCds = serializers.CharField(
        source="area_cds", help_text="The area/field of study for the CDS"
    )

    class Meta:
        model = DidatticaCds
        fields = [
            "areaCds",
        ]
        language_field_map = {
            "areaCds": {"it": "area_cds", "en": "area_cds_en"},
        }


@extend_schema_serializer(
    examples=examples.CDS_EXPIRED_SERIALIZER_EXAMPLE
)
class CdsExpiredSerializer(ReadOnlyModelSerializer):
    cdsCod = serializers.CharField(
        source="cds.cds_cod", help_text="The unique code of the CDS"
    )
    aaRegDid = serializers.CharField(
        source="aa_reg_did", help_text="Academic year of the didactic regulation"
    )
    cdsDuration = serializers.CharField(
        source="cds.durata_anni", help_text="Duration of the course in years"
    )

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "cdsCod",
            "aaRegDid",
            "cdsDuration",
        ]

@extend_schema_serializer(
    examples=examples.DEGREE_TYPE_SERIALIZER_EXAMPLE
)
class DegreeTypeSerializer(ReadOnlyModelSerializer):
    courseType = serializers.CharField(
        source="tipo_corso_cod", help_text="Code representing the type of course"
    )
    courseTypeDescription = serializers.CharField(
        source="tipo_corso_des", help_text="Description of the course type"
    )

    class Meta:
        model = DidatticaCdsTipoCorso
        fields = [
            "courseType",
            "courseTypeDescription",
        ]


@extend_schema_serializer(
    examples=examples.ACADEMIC_YEARS_SERIALIZER_EXAMPLE
)
class AcademicYearsSerializer(ReadOnlyModelSerializer):
    aaRegDid = serializers.CharField(
        source="aa_reg_did", help_text="Academic year identifier"
    )

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "aaRegDid",
        ]

@extend_schema_serializer(
    examples=examples.STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE
)
class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = "__all__"


@extend_schema_serializer(
    examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE
)
class StudyActivitiesListSerializer(ReadOnlyModelSerializer):
    id = serializers.CharField(
        source="af_id", help_text="The ID of the study activity."
    )
    genCod = serializers.CharField(
        source="af_gen_cod", help_text="Code of the study activity."
    )
    des = serializers.CharField(
        source="group_description", help_text="Description of the study activity group."
    )
    cdsId = serializers.CharField(
        source="cds_id", help_text="The ID of the degree program."
    )
    cdsCod = serializers.CharField(
        source="cds.cds_cod", help_text="Code of the degree program."
    )
    language = serializers.SerializerMethodField(
        help_text="List of languages available for the study activity."
    )
    fatherCode = serializers.CharField(
        source="af_radice_id", help_text="Parent activity's ID."
    )
    fatherName = serializers.CharField(help_text="Name of the parent activity.")
    regDidId = serializers.CharField(
        source="regdid_id",
        help_text="Regulation identifier associated with the activity.",
    )
    dipDes = serializers.CharField(
        source="cds.dip.dip_des_it",
        help_text="Description of the department in Italian.",
    )
    dipCod = serializers.CharField(
        source="cds.dip.dip_cod", help_text="Code of the department."
    )
    courseYear = serializers.CharField(
        source="anno_corso", help_text="The year of the course in the degree program."
    )
    academicYear = serializers.CharField(
        source="aa_off_id", help_text="Academic year of the activity."
    )
    semester = serializers.CharField(
        source="ciclo_des", help_text="Semester in which the activity is offered."
    )
    SSDCod = serializers.CharField(
        source="sett_cod", help_text="Code of the scientific-disciplinary sector (SSD)."
    )
    SSD = serializers.CharField(
        source="sett_des",
        help_text="Description of the scientific-disciplinary sector (SSD).",
    )
    partitionCod = serializers.CharField(
        source="part_stu_cod", help_text="Partition code for the study activity."
    )
    partitionDes = serializers.CharField(
        source="part_stu_des", help_text="Partition description for the study activity."
    )
    extendedPartitionCod = serializers.CharField(
        source="fat_part_stu_cod",
        help_text="Extended partition code for detailed activities.",
    )
    extendedPartitionDes = serializers.CharField(
        source="fat_part_stu_des",
        help_text="Extended partition description for detailed activities.",
    )
    cdsName = serializers.CharField(
        source="cds.nome_cds_it", help_text="Name of the degree program in Italian."
    )
    teacherId = serializers.SerializerMethodField(
        help_text="Encrypted identifier of the teacher responsible for the activity."
    )
    teacherName = serializers.CharField(
        source="full_name",
        help_text="Full name of the teacher responsible for the activity.",
    )
    studyPlanDes = serializers.CharField(
        source="pds_des",
        help_text="Description of the study plan associated with the activity.",
    )
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_language(self, obj):
        list_language = getattr(obj, "lista_lin_did_af", None)
        if list_language:
            return list_language.replace(" ", "").split(",")
        return []

    @extend_schema_field(serializers.CharField())
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
            "studyPlanDes",
        ]


@extend_schema_serializer(
    examples=examples.CDS_MORPH_SERIALIZER_EXAMPLE
)
class CdsMorphSerializer(ReadOnlyModelSerializer):
    idCds = serializers.IntegerField(source="cds", help_text="The ID of the cds.")
    idCdsPrec = serializers.IntegerField(
        source="cds_prec", help_text="The id of the previous cds."
    )

    class Meta:
        model = DidatticaCdsCollegamento
        fields = ["idCds", "idCdsPrec"]


@extend_schema_serializer(
    examples=examples.STUDY_ACTIVITY_LITE_SERIALIZER_EXAMPLE
)
class StudyActivitiesLiteSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(
        source="af_id", help_text="The ID of the study activity"
    )
    name = serializers.CharField(source="des", help_text="Name of the study activity")
    year = serializers.IntegerField(source="anno_corso", help_text="Year of the course")
    cycle = serializers.CharField(
        source="ciclo_des", help_text="Cycle/semester of the activity"
    )
    etcs = serializers.IntegerField(
        source="peso", help_text="ECTS credits for the activity"
    )
    type = serializers.CharField(
        source="tipo_af_des", help_text="Type of educational activity"
    )

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = ["id", "name", "year", "cycle", "etcs", "type"]


@extend_schema_serializer(
    examples=examples.ACADEMIC_PATHWAYS_LIST_SERIALIZER_EXAMPLE
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

@extend_schema_serializer(
    examples=examples.ACADEMIC_PATHWAYS_DETAIL_SERIALIZER_EXAMPLE
)
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
