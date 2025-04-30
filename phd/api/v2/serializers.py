from rest_framework import serializers
from generics.utils import encrypt

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from phd.models import (
    DidatticaDottoratoCds,
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaTipologia,
)


@extend_schema_serializer(examples=examples.PHD_DETAIL_SERIALIZER_EXAMPLE)
class PhdSerializer(serializers.Serializer):
    academicYear = serializers.SerializerMethodField()
    departmentID = serializers.IntegerField(source="dip_cod.dip_id")
    departmentCod = serializers.CharField(source="dip_cod.dip_cod")
    departmentName = serializers.SerializerMethodField()
    cdsCOD = serializers.CharField(source="cds_cod")
    cdsName = serializers.CharField(source="cdsord_des")
    regID = serializers.SerializerMethodField()
    regCOD = serializers.SerializerMethodField()
    cdSDuration = serializers.IntegerField(source="durata_anni")
    cdSECTS = serializers.IntegerField(source="valore_min")
    cdSAttendance = serializers.SerializerMethodField()
    courseType = serializers.CharField(source="tipo_corso_cod")
    courseName = serializers.CharField(source="tipo_corso_des")
    cycleNumber = serializers.SerializerMethodField()
    studyPlanCOD = serializers.SerializerMethodField()
    studyPlanDes = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_departmentName(self, obj):
        lang = self.context.get("lang", "it")
        return obj.dip_cod.dip_des_eng if lang == "en" else obj.dip_cod.dip_des_it

    @extend_schema_field(serializers.IntegerField())
    def get_academicYear(self, obj):
        return obj.idesse3_ddr.first().aa_regdid_id

    @extend_schema_field(serializers.IntegerField())
    def get_regID(self, obj):
        return obj.idesse3_ddr.first().regdid_id_esse3

    @extend_schema_field(serializers.CharField())
    def get_regCOD(self, obj):
        return obj.idesse3_ddr.first().regdid_cod

    @extend_schema_field(serializers.BooleanField())
    def get_cdSAttendance(self, obj):
        return bool(obj.idesse3_ddr.first().frequenza_obbligatoria)

    @extend_schema_field(serializers.IntegerField())
    def get_cycleNumber(self, obj):
        return obj.idesse3_ddr.first().num_ciclo

    @extend_schema_field(serializers.CharField())
    def get_studyPlanCOD(self, obj):
        return obj.idesse3_ddpds.first().pds_cod

    @extend_schema_field(serializers.CharField())
    def get_studyPlanDes(self, obj):
        return obj.idesse3_ddpds.first().pds_des

    class Meta:
        model = DidatticaDottoratoCds
        fields = [
            "academicYear",
            "departmentID",
            "departmentCod",
            "departmentName",
            "cdsCOD",
            "cdsName",
            "regID",
            "regCOD",
            "cdSDuration",
            "cdSECTS",
            "cdSAttendance",
            "courseType",
            "courseName",
            "cycleNumber",
            "studyPlanCOD",
            "studyPlanDes",
        ]


@extend_schema_serializer(examples=examples.PHD_ACTIVITY_SERIALIZER_EXAMPLE)
class PhdActivitiesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    activityName = serializers.CharField(source="nome_af")
    hours = serializers.IntegerField(source="numero_ore")
    activityType = serializers.CharField(source="tipo_af")
    activityTypology = serializers.CharField(source="tipologia.nome_it")
    referentPhd = serializers.CharField(source="rif_dottorato")
    cycle = serializers.CharField(source="ciclo")
    referentStructureId = serializers.CharField(source="struttura_proponente")
    referentStructureName = serializers.CharField(source="struttura_proponente_origine")
    activityContents = serializers.CharField(source="contenuti_af")
    prerequisites = serializers.CharField(source="prerequisiti")
    minStudents = serializers.IntegerField(source="num_min_studenti")
    maxStudents = serializers.IntegerField(source="num_max_studenti")
    finalTest = serializers.CharField(source="verifica_finale")
    finalTestMode = serializers.CharField(source="modalita_verifica")
    activityStart = serializers.CharField(source="avvio")
    activityEnd = serializers.CharField(source="fine")
    classroomsTimetable = serializers.CharField(source="orario_aule")
    showTimetable = serializers.CharField(source="visualizza_orario")
    notes = serializers.CharField(source="note")
    mainTeachers = serializers.SerializerMethodField()
    otherTeachers = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField())
    def get_mainTeachers(self, obj):
        return [
            {
                "personId": encrypt(docente.matricola),
                "personName": docente.cognome_nome_origine,
            }
            for docente in obj.docente
        ]

    @extend_schema_field(serializers.ListField())
    def get_otherTeachers(self, obj):
        return [
            {
                "personId": encrypt(docente.matricola),
                "personName": docente.cognome_nome_origine,
            }
            for docente in obj.altri_docenti
        ]

    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = [
            "id",
            "activityName",
            "ssd",
            "hours",
            "cfu",
            "activityType",
            "activityTypology",
            "referentPhd",
            "cycle",
            "referentStructureId",
            "referentStructureName",
            "activityContents",
            "prerequisites",
            "minStudents",
            "maxStudents",
            "finalTest",
            "finalTestMode",
            "activityStart",
            "activityEnd",
            "classroomsTimetable",
            "showTimetable",
            "notes",
            "mainTeachers",
            "otherTeachers",
        ]
        language_field_map = {
            "activityTypology": {"it": "tipologia.nome_it", "en": "tipologia.nome_en"},
        }


@extend_schema_serializer(examples=examples.PHD_ACTIVITY_TYPE_SERIALIZER_EXAMPLE)
class PhdActivitiesTypesSerializer(serializers.ModelSerializer):
    activityType = serializers.CharField(source="tipo_af")

    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = [
            "activityType",
        ]


@extend_schema_serializer(examples=examples.PHD_ACTIVITY_TYPOLOGY_SERIALIZER_EXAMPLE)
class PhdActivitiesTypologiesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source="nome_it")

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaTipologia
        fields = ["id", "name"]
        language_field_map = {
            "name": {"it": "nome_it", "en": "nome_en"},
        }


@extend_schema_serializer(examples=examples.PHD_SSD_SERIALIZER_EXAMPLE)
class PhdSsdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = [
            "ssd",
        ]


@extend_schema_serializer(examples=examples.PHD_REF_SERIALIZER_EXAMPLE)
class RefPhdSerializer(serializers.ModelSerializer):
    referentPhd = serializers.CharField(source="rif_dottorato")

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaTipologia
        fields = ["referentPhd"]


@extend_schema_serializer(examples=examples.PHD_REF_STRUCTURE_SERIALIZER_EXAMPLE)
class RefStructuresSerializer(serializers.ModelSerializer):
    referentStructureName = serializers.CharField(source="struttura_proponente_origine")

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaTipologia
        fields = ["referentStructureName"]
