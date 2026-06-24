from collections import defaultdict
from .docs import examples
from django.conf import settings
from addressbook.utils import append_email_addresses, get_contacts
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import LanguageAwareMixin, ReadOnlyModelSerializer
from generics.utils import encrypt, build_media_path, is_nullable
from rest_framework import serializers
from django.db.models import Q
from django.db.models import Prefetch
from addressbook.models import Personale
from addressbook.settings import ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN
from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaAttivitaFormativaErogata,
    DidatticaAttivitaFormativaPds,
    DidatticaCds,
    DidatticaCdsTipoCorso,
    DidatticaPdsRegolamento,
    DidatticaPianiStudio,
    DidatticaRegolamento,
    DidatticaCdsCollegamento,
    DidatticaCopertura,
    DidatticaCdsPeriodi,
    DidatticaTestiAfErogata,
    DidatticaCoperturaDettaglioOre,
)


@extend_schema_serializer(examples=examples.CDS_SERIALIZER_EXAMPLE)
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

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_languages(self, obj):
        lang = self.get_requestLang()

        lang_list = []

        if hasattr(obj.cds, "lingue"):
            for lingua in obj.cds.lingue:
                lang_list.append(
                    lingua.lingua_des_it
                    if lang == "it" or not lingua.lingua_des_eng
                    else lingua.lingua_des_eng
                )

        return lang_list

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
        language_field_map = {
            "area": {"it": "cds.area_cds", "en": "cds.area_cds_en"},
            "name": {"it": "cds.nome_cds_it", "en": "cds.nome_cds_eng"},
            "departmentName": {"it": "cds.dip.dip_des_it", "en": "cds.dip.dip_des_eng"},
        }


@extend_schema_serializer(examples=examples.CDS_DETAIL_SERIALIZER_EXAMPLE)
class CdsDetailSerializer(ReadOnlyModelSerializer):
    regDidId = serializers.IntegerField(source="regdid_id")
    status = serializers.CharField(source="stato_regdid_cod")
    cdsId = serializers.IntegerField(source="cds.cds_id")
    cdsCod = serializers.CharField(source="cds.cds_cod")
    academicYear = serializers.IntegerField(source="aa_reg_did")
    area = serializers.CharField(source="cds.area_cds")
    name = serializers.CharField(source="cds.nome_cds_it")
    departmentId = serializers.IntegerField(source="cds.dip.dip_id")
    departmentCod = serializers.CharField(source="cds.dip.dip_cod")
    departmentName = serializers.CharField(source="cds.dip.dip_des_it")
    type = serializers.CharField(source="cds.tipo_corso_cod")
    typeDescription = serializers.CharField(source="cds.tipo_corso_des")
    courseClassCod = serializers.CharField(source="cds.cla_miur_cod")
    courseClassName = serializers.CharField(source="cds.cla_miur_des")
    courseInterClassCod = serializers.CharField(source="cds.intercla_miur_cod")
    courseInterClassDes = serializers.CharField(source="cds.intercla_miur_des")
    erogationMode = serializers.CharField()
    languages = serializers.SerializerMethodField()
    duration = serializers.IntegerField(source="cds.durata_anni")
    ECTS = serializers.IntegerField(source="cds.valore_min")
    mandatoryAttendance = serializers.SerializerMethodField()
    profiles = serializers.SerializerMethodField()
    satisfactionSurvey = serializers.IntegerField(source="cds.codicione")
    jointDegree = serializers.CharField(source="titolo_congiunto_cod")
    studyManifesto = serializers.CharField(
        source="didatticacdsaltridati.manifesto_studi"
    )
    didacticRegulation = serializers.SerializerMethodField(
        method_name="get_didactic_regulation"
    )
    teachingSystem = serializers.SerializerMethodField()
    teachingSystemYear = serializers.SerializerMethodField()
    officesData = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()
    currentPeriods = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    def serializer_periods(self, obj, year):
        periods = DidatticaCdsPeriodi.objects.filter(
            cds_cod=obj.cds.cds_cod, aa_id=year
        ).only(
            "tipo_ciclo_des",
            "data_inizio",
            "data_fine",
        )

        return [
            {
                "description": item.tipo_ciclo_des,
                "start": item.data_inizio,
                "end": item.data_fine,
            }
            for item in periods
        ]

    @extend_schema_field(serializers.CharField())
    def get_teachingSystem(self, obj):
        return (
            build_media_path(obj.ordinamento_didattico[1])
            if obj.ordinamento_didattico
            else None
        )

    @extend_schema_field(serializers.CharField())
    def get_teachingSystemYear(self, obj):
        return (
            build_media_path(obj.ordinamento_didattico[0])
            if obj.ordinamento_didattico
            else None
        )

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

    @extend_schema_field(serializers.ListField())
    def get_currentPeriods(self, obj):
        return self.serializer_periods(obj, settings.CURRENT_YEAR)

    @extend_schema_field(serializers.ListField())
    def get_periods(self, obj):
        return self.serializer_periods(obj, obj.aa_reg_did)

    @extend_schema_field(serializers.ListField())
    def get_profiles(self, obj):
        language = self.get_requestLang()

        texts = getattr(obj, "testi_regolamento", []) or []
        list = []
        last_profile = ""

        for text in texts:
            text_it = text.clob_txt_ita
            text_eng = text.clob_txt_eng

            if text.tipo_testo_regdid_cod not in ["FUNZIONI", "COMPETENZE", "SBOCCHI"]:
                list.append(
                    text_eng
                    if (text_eng is None and language != "it") or language == "it"
                    else text_it
                )
            else:
                selected_profile = (
                    text.profilo
                    if (language != "it" and text.profilo_eng is None)
                    or language == "it"
                    else text.profilo_eng
                )
                if selected_profile != last_profile:
                    last_profile = selected_profile
                    list[last_profile] = {}

                list[last_profile][text.tipo_testo_regdid_cod] = (
                    text_it
                    if (text_eng is None and language != "it") or language == "it"
                    else text_eng
                )

        return list

    @extend_schema_field(serializers.ListField())
    def get_otherData(self, obj):
        email_id_coordinatore = (
            obj.matricola_coordinatore.email.split("@")[0]
            if obj.matricola_coordinatore.email
            and obj.matricola_coordinatore.email.endswith(
                f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"
            )
            else None
        )
        email_id_vice = (
            obj.matricola_vice_coordinatore.email.split("@")[0]
            if obj.matricola_vice_coordinatore.email
            and obj.matricola_vice_coordinatore.email.endswith(
                f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"
            )
            else None
        )

        altri_dati = getattr(obj, "otherData", [])
        return [
            {
                "coordinatorId": email_id_coordinatore
                or encrypt(obj.matricola_coordinatore),
                "coordinatorName": ad.nome_origine_coordinatore,
                # "viceCoordinatorId": ad.matricola_vice_coordinatore,
                "viceCoordinatorId": email_id_vice
                or encrypt(ad.matricola_vice_coordinatore),
                "viceCoordinatorName": ad.nome_origine_vice_coordinatore,
                "studyManifesto": ad.manifesto_studi,
                "educationalRules": ad.regolamento_didattico,
                "educationalSystem": ad.ordinamento_didattico,
            }
            for ad in altri_dati
        ]

    @extend_schema_field(serializers.ListField())
    def get_officesData(self, obj):
        return []

        # toDO GDA REFACTOR
        officeData = getattr(obj, "officesData", [])
        email_id = (
            obj.email.split("@")[0]
            if obj.email
            and obj.email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
            else None
        )
        return [
            {
                "ordine": item.ordine,
                "nome_ufficio": item.nome_ufficio,
                # "matricola_riferimento": item.matricola_riferimento,
                "matricola_riferimento": email_id
                or encrypt(item.matricola_riferimento),
                "nome_origine_riferimento": item.nome_origine_riferimento,
                "telefono": item.telefono,
                "email": item.email,
                "edificio": item.edificio,
                "piano": item.piano,
                "orari": item.orari,
                "sportello_online": item.sportello_online,
            }
            for item in officeData
        ]

    @extend_schema_field(serializers.ListField())
    def get_groups(self, obj):
        cdsGroups = getattr(obj, "cdsGroups", []) or []

        return [
            {
                "ordine": item.ordine,
                "id": item.id,
                "descr_breve_it": item.descr_breve_it,
                "descr_breve_en": item.descr_breve_en,
                "descr_lunga_it": item.descr_lunga_it,
                "descr_lunga_en": item.descr_lunga_en,
                "members": [
                    {
                        "ordine": component.ordine,
                        "id": component.id,
                        "matricola": component.matricola,
                        "cognome": component.cognome,
                        "nome": component.nome,
                        "funzione_it": component.funzione_it,
                        "funzione_en": component.funzione_en,
                    }
                    for component in getattr(item, "components", [])
                ],
            }
            for item in cdsGroups
        ]

    @extend_schema_field(serializers.ListField())
    def get_languages(self, obj):
        lang = self.get_requestLang()

        lang_list = []

        if hasattr(obj.cds, "lingue"):
            for lingua in obj.cds.lingue:
                lang_list.append(
                    lingua.lingua_des_it
                    if lang == "it" or not lingua.lingua_des_eng
                    else lingua.lingua_des_eng
                )

        return lang_list

    @extend_schema_field(serializers.BooleanField())
    def get_mandatoryAttendance(self, obj):
        return bool(obj.frequenza_obbligatoria)

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "regDidId",
            "status",
            "cdsId",
            "cdsCod",
            "academicYear",
            "area",
            "name",
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
            # "intro",
            # "doc",
            # "url",
            # "video",
            # "goals",
            # "access",
            # "admission",
            "profiles",
            # "finalTest",
            # "finalTestMode",
            "satisfactionSurvey",
            "jointDegree",
            "studyManifesto",
            "didacticRegulation",
            "teachingSystem",
            "teachingSystemYear",
            # "otherData",
            "officesData",
            "groups",
            "periods",
            "currentPeriods",
        ]
        language_field_map = {
            "area": {"it": "cds.area_cds", "en": "cds.area_cds_en"},
            "name": {"it": "cds.nome_cds_it", "en": "cds.nome_cds_eng"},
            "departmentName": {"it": "cds.dip.dip_des_it", "en": "cds.dip.dip_des_eng"},
        }


@extend_schema_serializer(examples=examples.CDS_AREA_SERIALIZER_EXAMPLE)
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


@extend_schema_serializer(examples=examples.CDS_EXPIRED_SERIALIZER_EXAMPLE)
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


@extend_schema_serializer(examples=examples.DEGREE_TYPE_SERIALIZER_EXAMPLE)
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


@extend_schema_serializer(examples=examples.ACADEMIC_YEARS_SERIALIZER_EXAMPLE)
class AcademicYearsSerializer(ReadOnlyModelSerializer):
    aaRegDid = serializers.CharField(
        source="aa_reg_did", help_text="Academic year identifier"
    )

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "aaRegDid",
        ]

class StudyActivityModalitySerializer(serializers.Serializer):
    ModalityActivityCod = serializers.CharField(source="mod_did_cod")
    ModalityActivityDescription = serializers.CharField(source="mod_did_desc_ita")

    class Meta:
        fields = [
            "ModalityActivityCod",
            "ModalityActivityDescription",
        ]
        language_field_map = {
            "ModalityActivityDescription": {"it": "mod_did_desc_ita", "en": "mod_did_desc_eng"},
        }


class StudyActivityModulePartitionSerializer(serializers.Serializer):
    StudyActivityID = serializers.IntegerField(source="erog_id")
    StudyActivityPartitionCod = serializers.CharField(source="erog_id__part_stu_cod")
    StudyActivityPartitionDes = serializers.CharField(source="erog_id__part_stu_desc_ita")
    StudyActivityExtendedPartitionCod = serializers.CharField(source="erog_id__fatt_part_stu_cod")
    # ~ StudyActivityExtendedPartitionDes = serializers.CharField(source="erog_id__fatt_part_stu_desc_ita")

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'ita')
        super().__init__(*args, **kwargs)
        
    class Meta:
        fields = [
            "StudyActivityID",
            "StudyActivityPartitionCod",
            "StudyActivityPartitionDes",
            "StudyActivityExtendedPartitionCod",
            "StudyActivityExtendedPartitionDes",
        ]
        language_field_map = {
            "StudyActivityPartitionDes": {
                "it": "erog_id__part_stu_desc_ita",
                "en": "erog_id__part_stu_desc_eng"
            },
            "StudyActivityExtendedPartitionDes": {
                "it": "erog_id__fatt_part_stu_desc_ita",
                "en": "erog_id__fatt_part_stu_desc_eng"
            },
        }


class StudyActivityModuleSerializer(serializers.Serializer, LanguageAwareMixin):
    StudyActivityID = serializers.IntegerField()
    StudyActivityCod = serializers.CharField(source="ana_mod_cod")
    StudyActivityName = serializers.CharField(source="ana_mod_desc_ita")
    StudyActivitySemester = serializers.CharField(source="erog_id__tipo_periodo_did_desc_ita")
    StudyActivityPartitions = serializers.SerializerMethodField()

    def get_StudyActivityPartitions(self, obj):
        if not self.moduli_queryset:
            return []
        
        erogazioni = self.moduli_queryset.filter(ana_mod_id=obj["ana_mod_id"]).values(
            "erog_id",
            "erog_id__part_stu_cod",
            "erog_id__part_stu_desc_ita" if self._get_lang() == "it" else is_nullable("erog_id__part_stu_desc_eng") or "erog_id__part_stu_desc_ita",
            "erog_id__fatt_part_stu_cod",
            "erog_id__fatt_part_stu_desc_ita" if self._get_lang() == "it" else is_nullable("erog_id__fatt_part_stu_desc_eng") or "erog_id__fatt_part_stu_desc_ita",
        ).distinct().order_by("erog_id")
        
        if erogazioni.count() > 1:
            return StudyActivityModulePartitionSerializer(erogazioni, many=True, context=self.context).data
        return []

    class Meta:
        fields = [
            "StudyActivityID",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivitySemester",
            "StudyActivityPartitions",
        ]
        language_field_map = {
            "StudyActivitySemester": {"it": "erog_id__tipo_periodo_did_desc_ita", "en": "erog_id__tipo_periodo_did_desc_eng"},
            "StudyActivityName": {"it": "ana_mod_desc_ita", "en": "ana_mod_desc_eng"},
        }


class StudyActivityHourSerializer(serializers.Serializer):
    ActivityType = serializers.CharField(source="tipo_att_did_cod")
    Hours = serializers.IntegerField(source="ore")
    StudyActivityTeacherID = serializers.SerializerMethodField()
    StudyActivityTeacherName = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.teacher_id = kwargs.pop('teacher_id', None)
        self.teacher_name = kwargs.pop('teacher_name', None)
        super().__init__(*args, **kwargs)

    def get_StudyActivityTeacherID(self, obj):
        return self.teacher_id

    def get_StudyActivityTeacherName(self, obj):
        return self.teacher_name


class StudyActivityBorrowSerializer(serializers.Serializer):
    StudyActivityID = serializers.IntegerField(source="erog_id")
    StudyActivityName = serializers.CharField(source="ana_mod_desc_ita")
    StudyActivityPartitionCod = serializers.CharField(source="part_stu_cod")
    StudyActivityPartition = serializers.CharField(source="part_stu_desc_ita")
    StudyActivityCdSCod = serializers.CharField(source="cds_cod")
    StudyActivityCdSName = serializers.CharField(source="nome_cds_it")

    class Meta:
        fields = [
            "StudyActivityID",
            "StudyActivityName",
            "StudyActivityPartitionCod",
            "StudyActivityPartition",
            "StudyActivityCdSCod",
            "StudyActivityCdSName",
        ]
        language_field_map = {
            "StudyActivityName": {"it": "ana_mod_desc_ita", "en": "ana_mod_desc_eng"},
            "StudyActivityPartition": {"it": "part_stu_desc_ita", "en": "part_stu_desc_eng"},
            "StudyActivityCdSName": {"it": "nome_cds_it", "en": "nome_cds_en"},
        }

class StudyActivityContentSerializer(serializers.Serializer):
    StudyActivityContentCod = serializers.CharField(source="campo_cod")
    StudyActivityContentTitle = serializers.CharField(source="campo_desc_ita")
    StudyActivityContentDes = serializers.CharField(source="testo_fmt_ita")

    class Meta:
        fields = [
            "StudyActivityContentCod",
            "StudyActivityContentTitle",
            "StudyActivityContentDes",
        ]
        language_field_map = {
            "StudyActivityContentTitle": {"it": "campo_desc_ita", "en": "campo_desc_eng"},
            "StudyActivityContentDes": {"it": "testo_fmt_ita", "en": "testo_fmt_eng"},
        }


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE)
class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer, LanguageAwareMixin):
    StudyActivityID = serializers.IntegerField(source="af_pds_id")
    StudyActivityCod = serializers.CharField(source="ana_mod_cod", default=None)
    StudyActivityCdSID = serializers.IntegerField(source="id_cds.cds_id", default=None)
    StudyActivityCdSCod = serializers.CharField(source="cds_cod", default=None)
    StudyActivityRegDidId = serializers.IntegerField(source="regdid_id", default=None)
    StudyActivityErogationYear = serializers.IntegerField(source="aa_off_id", default=None)
    StudyActivityECTS = serializers.IntegerField(source="cfu", default=None)
    StudyActivityYear = serializers.IntegerField(source="anno_corso", default=None)
    StudyActivityTeachingUnitTypeCod = serializers.CharField(source="taf_cod", default=None)
    StudyActivityCompulsory = serializers.CharField(source="flag_obbl", default=None)
    StudyActivitySSDCod = serializers.CharField(source="sett_cod", default=None)

    StudyActivityTeachingUnitType = serializers.CharField(source="taf_desc_ita", default=None)
    StudyActivityCdSName = serializers.CharField(source="id_cds.nome_cds_it", default=None)
    StudyActivitySSD = serializers.CharField(source="sett_desc_ita", default=None)
    StudyActivitySemester = serializers.CharField(source="erog_id.tipo_periodo_did_desc_ita", default=None)

    StudyActivityPartitionDes = serializers.SerializerMethodField()
    StudyActivityName = serializers.SerializerMethodField()
    StudyActivityStudyPlans = serializers.SerializerMethodField()
    StudyActivityLanguage = serializers.SerializerMethodField()
    StudyActivityTeacherID = serializers.SerializerMethodField()
    StudyActivityTeacherName = serializers.SerializerMethodField()
    StudyActivityModalities = serializers.SerializerMethodField()
    StudyActivitiesModules = serializers.SerializerMethodField()
    StudyActivityPartitions = serializers.SerializerMethodField()
    StudyActivityRoot = serializers.SerializerMethodField()
    StudyActivityHours = serializers.SerializerMethodField()
    StudyActivityBorrows = serializers.SerializerMethodField()
    StudyActivityBorrowedFrom = serializers.SerializerMethodField()
    StudyActivityContents = serializers.SerializerMethodField()

    def get_StudyActivityName(self, obj):
        if isinstance(obj, str):
            return obj
        lang = self._get_lang()
        return obj.ana_mod_desc_ita if lang == 'it' else (is_nullable(obj.ana_mod_desc_eng) or obj.ana_mod_desc_ita)

    def get_StudyActivityPartitionDes(self, obj):
        if not obj.erog_found: return None
        lang = self._get_lang()
        return obj.erog_id.part_stu_desc_ita if lang == 'it' else (is_nullable(obj.erog_id.part_stu_desc_eng) or obj.erog_id.part_stu_desc_ita)

    def get_StudyActivityStudyPlans(self, obj):
        lang = self._get_lang()
        if obj.erog_found:
            pds_list = getattr(obj, "pds", [])
            attr = "pds_desc_ita" if lang == 'it' else is_nullable("pds_desc_eng") or "pds_desc_ita"
            return [
                getattr(pds, attr, None) or getattr(pds, "pds_desc_ita", None)
                if not isinstance(pds, str) else pds
                for pds in pds_list
            ]
        pds = obj.pds_desc_ita if lang == 'it' else (is_nullable(obj.pds_desc_eng) or obj.pds_desc_ita)
        return [pds]

    def get_StudyActivityLanguage(self, obj):
        lang = self._get_lang()
        if obj.erog_found:
            val = obj.erog_id.lingua_did_desc_ita if lang == 'it' else (is_nullable(obj.erog_id.lingua_did_desc_eng) or obj.erog_id.lingua_did_desc_ita)
            return [val] if val else []
        return []
        # ~ return {
            # ~ (modulo.erog_id.lingua_did_desc_ita if lang == 'it' else (modulo.erog_id.lingua_did_desc_eng or modulo.erog_id.lingua_did_desc_ita))
            # ~ for modulo in obj.moduli
        # ~ }
    
    def get_StudyActivityTeacherID(self, obj):
        try:
            af_off = obj.erog_id.mod_off_id.af_off
            if af_off.doc_tit_matricola == "-999999999":
                return None
            email = af_off.doc_tit_id_ab.email
            if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                return email.split("@")[0]
            return encrypt(af_off.doc_tit_matricola)
        except Exception:
            return None

    def get_StudyActivityTeacherName(self, obj):
        try:
            doc = Personale.objects.filter(id_ab=obj.erog_id.mod_off_id.af_off.doc_tit_id_ab.id_ab).first()
            if doc:
                return f"{doc.cognome} {doc.nome}"
        except Exception:
            pass
        return None

    def get_StudyActivityModalities(self, obj):
        if obj.erog_found:
            return StudyActivityModalitySerializer([obj], many=True, context=self.context).data
        
        seen = set()
        unique_moduli = []
        for modulo in obj.moduli:
            if modulo.mod_did_cod not in seen:
                seen.add(modulo.mod_did_cod)
                unique_moduli.append(modulo)
        return StudyActivityModalitySerializer(unique_moduli, many=True, context=self.context).data

    def get_StudyActivitiesModules(self, obj):
        # obj.moduli ora è una normale lista Python (es. [mod1, mod2, mod3])
        if not obj.moduli:
            return []

        # 1. Raggruppiamo i moduli per 'ana_mod_id' usando un dizionario Python
        # Invece di chiedere al DB di fare la DISTINCT, la facciamo noi in RAM.
        moduli_raggruppati = {}
        for modulo in obj.moduli:
            m_id = modulo.ana_mod_id
            if m_id not in moduli_raggruppati:
                moduli_raggruppati[m_id] = []
            moduli_raggruppati[m_id].append(modulo)

        # L'equivalente in RAM di moduli.count() == 1
        if len(moduli_raggruppati) <= 1:
            return []

        result = []
        
        # 2. Cicliamo sui gruppi che abbiamo creato in memoria
        for ana_mod_id, lista_moduli_stesso_id in moduli_raggruppati.items():
            # Prendiamo il primo elemento per leggere i campi anagrafici (es. ana_mod_cod)
            primo_mod = lista_moduli_stesso_id[0]
            
            # 3. Raggruppiamo le erogazioni distinte per questo modulo
            # L'equivalente in RAM del tuo secondo .values(...).distinct()
            erogazioni_uniche = {}
            for m in lista_moduli_stesso_id:
                # Usiamo erog_id come chiave del dizionario per scartare i duplicati
                if m.erog_id_id not in erogazioni_uniche:
                    # Navighiamo l'oggetto relazionato (pre-caricato con select_related)
                    erogazioni_uniche[m.erog_id_id] = {
                        "erog_id": m.erog_id_id,
                        "erog_id__part_stu_cod": getattr(m.erog_id, 'part_stu_cod', None),
                        "erog_id__part_stu_desc" : getattr(m.erog_id, "part_stu_desc_ita" if self._get_lang() == "it" else (is_nullable("part_stu_desc_eng") or "part_stu_desc_ita"), None),
                        "erog_id__fatt_part_stu_cod": getattr(m.erog_id, 'erog_id__fatt_part_stu_cod', None),
                        "erog_id__fatt_part_stu_desc": getattr(m.erog_id, "fatt_part_stu_desc_ita" if self._get_lang() == "it" else (is_nullable("fatt_part_stu_desc_eng") or "fatt_part_stu_desc_ita"), None),
                        "erog_id__tipo_periodo_did_desc": getattr(m.erog_id, "tipo_periodo_did_desc_ita" if self._get_lang() == "it" else (is_nullable("tipo_periodo_did_desc_eng") or "tipo_periodo_did_desc_ita"), None),
                    }
            
            # Trasformiamo il dizionario delle erogazioni in una lista
            lista_erogazioni = list(erogazioni_uniche.values())
            
            if len(lista_erogazioni) > 1:
                m_id_val = None
                # Assicurati che il tuo serializer accetti dizionari (come abbiamo risolto per Borrows)
                erog_list = StudyActivityModulePartitionSerializer(lista_erogazioni, many=True, context=self.context).data
            else:
                first_erog = lista_erogazioni[0] if lista_erogazioni else None
                m_id_val = first_erog["erog_id"] if first_erog else None
                erog_list = []

            first_elem = lista_erogazioni[0] if lista_erogazioni else None
            ana_mod_desc = "ana_mod_desc_ita" if self._get_lang() == "it" else (is_nullable("ana_mod_desc_eng") or "ana_mod_desc_ita")
            tipo_periodo_did_desc = "tipo_periodo_did_desc_ita" if self._get_lang() == "it" else (is_nullable("tipo_periodo_did_desc_eng") or "tipo_periodo_did_desc_ita")
            result.append({
                "StudyActivityID": m_id_val,
                "StudyActivityCod": getattr(primo_mod, "ana_mod_cod", None),
                "StudyActivityName": getattr(primo_mod, ana_mod_desc, None),
                "StudyActivitySemester": first_elem.get(tipo_periodo_did_desc) if first_elem else None,
                "StudyActivityPartitions": erog_list,
            })

        return result
    
    def get_StudyActivitiesModulesBKP(self, obj):
        if not obj.moduli:
            return []
        ana_mod_desc = "ana_mod_desc_ita" if self._get_lang() == "it" else is_nullable("ana_mod_desc_eng") or "ana_mod_desc_ita"
        fields_to_value = ["ana_mod_id", "ana_mod_cod", ana_mod_desc]
        moduli = obj.moduli.values(*fields_to_value).distinct()
        if moduli.count() == 1:
            return []

        result = []
        erog_id__part_stu_desc = "erog_id__part_stu_desc_ita" if self._get_lang() == "it" else is_nullable("erog_id__part_stu_desc_eng") or "erog_id__part_stu_desc_ita"
        erog_id__fatt_part_stu_desc_ = "erog_id__fatt_part_stu_desc_ita" if self._get_lang() == "it" else is_nullable("erog_id__fatt_part_stu_desc_eng") or "erog_id__fatt_part_stu_desc_ita"
        erog_id__tipo_periodo_did_desc_ = f"erog_id__tipo_periodo_did_desc_{self._get_lang()}"
        for m in moduli:
            erogazioni = obj.moduli.filter(ana_mod_id=m["ana_mod_id"]).values(
                "erog_id",
                "erog_id__part_stu_cod",
                erog_id__part_stu_desc,
                "erog_id__fatt_part_stu_cod",
                erog_id__fatt_part_stu_desc_,
                erog_id__tipo_periodo_did_desc_,
            ).distinct().order_by("erog_id")

            if erogazioni.count() > 1:
                m_id = None
                erog_list = StudyActivityModulePartitionSerializer(erogazioni, many=True, context=self.context).data
            else:
                first_erog = erogazioni.first()
                m_id = first_erog["erog_id"] if first_erog else None
                erog_list = []

            first_elem = erogazioni.first()
            result.append({
                "StudyActivityID": m_id,
                "StudyActivityCod": m["ana_mod_cod"],
                "StudyActivityName": m.ana_mod_desc_ita if self._get_lang() == "it" else (is_nullable(m.ana_mod_desc_eng) or m.ana_mod_desc_ita),
                "StudyActivitySemester": first_elem[erog_id__tipo_periodo_did_desc_] if first_elem else None,
                "StudyActivityPartitions": erog_list,
            })
        return result

    def get_StudyActivityPartitions(self, obj):
        moduli = obj.moduli 
        ids_moduli = {m.ana_mod_id for m in moduli}
        if len(ids_moduli) > 1:
            return []
        
        erogazioni = {}
        for m in moduli:
            if m.erog_id_id not in erogazioni:
                erogazioni[m.erog_id_id] = { ... }
        if len(erogazioni) > 1:
            return StudyActivityModulePartitionSerializer(
                list(erogazioni.values()), many=True, context=self.context
            ).data
        return []

    def get_StudyActivityRoot(self, obj):
        lang = self._get_lang()
        if not obj.erog_found:
            return None
        # ~ if DidatticaAttivitaFormativaPds.objects.filter(af_pds_id=obj.erog_id.erog_id).exists():
        if obj.af_pds_id==obj.erog_id.erog_id:
            return None
        
        return {
            "StudyActivityID": obj.af_pds_id,
            "StudyActivityName": obj.ana_af_desc_ita if lang == 'it' else (is_nullable(obj.ana_af_desc_eng) or obj.ana_af_desc_ita),
            "StudyActivityCod": obj.ana_af_cod
        }
    def get_StudyActivityHours(self, obj):
        if not obj.erog_found:
            return []

        coperture = getattr(obj.erog_id, 'coperture_attive', [])
        
        ids_ab = [
            cop.doc_id_ab_id
            for cop in coperture
            if cop.doc_matricola != "-999999999" and cop.doc_id_ab_id
        ]
        personale_map = {
            p.id_ab: p
            for p in Personale.objects.filter(id_ab__in=ids_ab).only('id_ab', 'cognome', 'nome')
        }

        result = []
        for cop in coperture:
            teacher_id, teacher_name = None, None
            if cop.doc_matricola != "-999999999":
                doc = personale_map.get(cop.doc_id_ab_id)
                teacher_name = f"{doc.cognome} {doc.nome}" if doc else None
                email = getattr(cop.doc_id_ab, "email", None)
                if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                    teacher_id = email.split("@")[0]
                else:
                    teacher_id = encrypt(cop.doc_matricola)
            
            serializer = StudyActivityHourSerializer(
                cop.dettaglio_ore.all(),
                many=True,
                teacher_id=teacher_id,
                teacher_name=teacher_name,
            )
            result.extend(serializer.data)
        return result

    def get_StudyActivityBorrows(self, obj):
        mapped_mutuazioni = []

        ana_mod_desc = "ana_mod_desc_ita" if self._get_lang() == "it" else (is_nullable("ana_mod_desc_eng") or "ana_mod_desc_ita")
        part_stu_desc = "part_stu_desc_ita" if self._get_lang() == "it" else (is_nullable("part_stu_desc_eng") or "part_stu_desc_ita")
        nome_cds = "nome_cds_it" if self._get_lang() == "it" else (is_nullable("nome_cds_eng") or "nome_cds_it")
        for m in obj.mutuazioni:
            for pds in m.pds.all():
                mapped_mutuazioni.append({
                    "erog_id": m.erog_id,
                    ana_mod_desc : getattr(pds, ana_mod_desc, None),
                    "part_stu_cod": m.part_stu_cod,
                    part_stu_desc: getattr(m, part_stu_desc, None),
                    "cds_cod": pds.cds_cod,
                    nome_cds: getattr(pds.id_cds, nome_cds, None),
                })
        return StudyActivityBorrowSerializer(mapped_mutuazioni, many=True, context=self.context).data

    def get_StudyActivityBorrowedFrom(self, obj):
        if not obj.mutuato_da:
            return None
        
        m = obj.mutuato_da[0]

        ana_mod_desc = "ana_mod_desc_ita" if self._get_lang() == "it" else (is_nullable("ana_mod_desc_eng") or "ana_mod_desc_ita")
        part_stu_desc = "part_stu_desc_ita" if self._get_lang() == "it" else (is_nullable("part_stu_desc_eng") or "part_stu_desc_ita")
        nome_cds = "nome_cds_it" if self._get_lang() == "it" else (is_nullable("nome_cds_eng") or "nome_cds_it")
        result = {
            "StudyActivityID": m.erog_id.erog_master_id,
            "StudyActivityName": getattr(m, ana_mod_desc, None),
            "StudyActivityPartition": getattr(m.erog_id, part_stu_desc, None),
            "StudyActivityCdSCod": m.cds_cod,
            "StudyActivityCdSName": getattr(m.id_cds, nome_cds, None),
            "StudyActivityStudyPlans": [],
        }
        pds_desc = "pds_desc_ita" if self._get_lang() == "it" else (is_nullable("pds_desc_eng") or "pds_desc_ita")
        for item in obj.mutuato_da:
            result["StudyActivityStudyPlans"].append(getattr(item, pds_desc, None))
            
        result["StudyActivityStudyPlans"] = list(set(result["StudyActivityStudyPlans"]))
        return result

    def get_StudyActivityContents(self, obj):
        if getattr(obj, "num_erogazioni", 1) > 1 or not obj.erog_found:
            return []
        
        # Recupera i testi direttamente dalla cache in memoria del prefetch
        testi_precaricati = obj.erog_id.testi.all()
        return StudyActivityContentSerializer(testi_precaricati, many=True, context=self.context).data



        
        # ~ if getattr(obj, "num_erogazioni", 1) > 1:
            # ~ return []
        
        # ~ testi_queryset = DidatticaTestiAfErogata.objects.filter(erog_id=obj.erog_id.erog_master_id)
        # ~ return StudyActivityContentSerializer(testi_queryset, many=True, lang=self._get_lang()).data

    class Meta:
        model = DidatticaAttivitaFormativaPds
        fields = [
            "StudyActivityID", "StudyActivityCod", "StudyActivityName", "StudyActivityPartitionDes",
            "StudyActivityRoot", "StudyActivityCdSID", "StudyActivityCdSCod", "StudyActivityRegDidId",
            "StudyActivityStudyPlans", "StudyActivityErogationYear", "StudyActivityECTS",
            "StudyActivityLanguage", "StudyActivityModalities", "StudyActivitySSDCod", "StudyActivitySSD",
            "StudyActivityCompulsory", "StudyActivityCdSName", "StudyActivityYear", "StudyActivitySemester",
            "StudyActivityTeacherID", "StudyActivityTeacherName", "StudyActivityTeachingUnitTypeCod",
            "StudyActivityTeachingUnitType", "StudyActivitiesModules", "StudyActivityPartitions",
            "StudyActivityHours", "StudyActivityBorrows", "StudyActivityBorrowedFrom", "StudyActivityContents",
        ]
        language_field_map = {
            "StudyActivityName": {"it": "ana_mod_desc_ita", "en": "ana_mod_desc_eng"},
            "StudyActivitySemester": {"it": "erog_id.tipo_periodo_did_desc_ita", "en": "erog_id.tipo_periodo_did_desc_eng"},
            "StudyActivityTeachingUnitType": {"it": "taf_desc_ita", "en": "taf_desc_eng"},
            "StudyActivityCdSName": {"it": "id_cds.nome_cds_it", "en": "id_cds.nome_cds_eng"},
            "StudyActivitySSD": {"it": "sett_desc_ita", "en": "sett_desc_eng"},

        }

class PdsListMixin:
    """Mixin con helper per accedere a _pds_list in modo sicuro."""

    def _first_pds(self, obj):
        pds_list = getattr(obj, '_pds_list', None)
        return pds_list[0] if pds_list else None


class StudyActivityTeacherSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        if obj.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            email = getattr(obj.doc_tit_id_ab, "email", None)
            if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                return email.split("@")[0]
            return encrypt(obj.af_off.doc_tit_matricola)
        except Exception:
            pass
        return None

    def get_name(self, obj):
        if obj.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            nome = obj.doc_tit_id_ab.nome
            cognome = obj.doc_tit_id_ab.cognome
            if nome and cognome:
                return f"{cognome} {nome}"
        except Exception:
            pass
        return None


class StudyActivityFatherSerializer(LanguageAwareMixin,serializers.Serializer):
    id = serializers.IntegerField(source="af_pds_id")
    cod = serializers.CharField(source="ana_af_cod")
    name = serializers.CharField(source="ana_af_desc_ita")
    pds = serializers.CharField(source="pds_desc_ita")

    class Meta:
        model = DidatticaAttivitaFormativaPds
        fields = [
            "id",
            "cod",
            "name",
            "pds"
        ]
        language_field_map = {
            "name": {"it": "ana_af_desc_ita", "en": "ana_af_desc_eng"},
            "pds": {"it": "pds_desc_ita", "en": "pds_desc_eng"}
        }


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
class StudyActivitiesListSerializer(PdsListMixin, ReadOnlyModelSerializer, LanguageAwareMixin):
    StudyActivityID = serializers.IntegerField(source="erog_id", default=None)
    StudyActivityCod = serializers.CharField(source="mod_off_id.ana_mod_cod", default=None)
    StudyActivityCdSID = serializers.IntegerField(source="mod_off_id.af_off.id_cds.cds_id", default=None)
    StudyActivityCdSCod = serializers.CharField(source="mod_off_id.af_off.cds_cod", default=None)

    DepartmentName = serializers.CharField(source="mod_off_id.af_off.id_cds.dip.dip_des_it", default=None) 
    DepartmentCod = serializers.CharField(source="mod_off_id.af_off.id_cds.dip.dip_cod", default=None)
    StudyActivityCdSName = serializers.CharField(source="mod_off_id.af_off.id_cds.nome_cds_it", default=None)

    StudyActivityName = serializers.CharField(default=None)
    StudyActivityLanguage = serializers.CharField(default=None)
    StudyActivitySemester = serializers.CharField(default=None)
    StudyActivityPartitionCod = serializers.CharField(source="part_stu_cod", default=None)
    StudyActivityPartitionDes = serializers.CharField(source="part_stu_desc_ita", default=None)
    StudyActivityExtendedPartitionCod = serializers.CharField(source="fatt_part_stu_cod", default=None)
    StudyActivityExtendedPartitionDes = serializers.CharField(default=None)

    StudyActivityTeacherID = serializers.SerializerMethodField()
    StudyActivityTeacherName = serializers.SerializerMethodField()
    
    StudyActivityStudyPlans = serializers.SerializerMethodField()
    StudyActivityFathers = serializers.SerializerMethodField()
    StudyActivityYear = serializers.SerializerMethodField()
    StudyActivityAcademicYear = serializers.SerializerMethodField()
    StudyActivityRegDidId = serializers.SerializerMethodField()
    StudyActivitySSDCod = serializers.SerializerMethodField()
    StudyActivitySSD = serializers.SerializerMethodField()


    def to_representation(self, instance):
        if hasattr(instance, 'pds_filtrati'):
            instance._pds_list = list(instance.pds_filtrati)
        else:
            instance._pds_list = list(instance.pds.all())
        return super().to_representation(instance)
    
    # --- 1. FUNZIONE DI CACHE PER LA LOGICA DEI DOCENTI (Sostituisce il vecchio sub-serializer) ---
    def _get_teacher_data(self, obj):
        if hasattr(obj, '_cached_teacher_data'):
            return obj._cached_teacher_data

        mod_off = obj.mod_off_id
        teacher_info = {"id": None, "name": None}

        if not mod_off or getattr(mod_off.af_off, "doc_tit_matricola", None) == "-999999999":
            obj._cached_teacher_data = teacher_info
            return teacher_info

        try:
            email = getattr(mod_off.doc_tit_id_ab, "email", None)
            if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                teacher_info["id"] = email.split("@")[0]
            else:
                teacher_info["id"] = encrypt(mod_off.af_off.doc_tit_matricola)
        except Exception:
            pass

        try:
            nome = mod_off.doc_tit_id_ab.nome
            cognome = mod_off.doc_tit_id_ab.cognome
            if nome and cognome:
                teacher_info["name"] = f"{cognome} {nome}"
        except Exception:
            pass

        obj._cached_teacher_data = teacher_info
        return teacher_info

    def get_StudyActivityTeacherID(self, obj):
        return self._get_teacher_data(obj)["id"]

    def get_StudyActivityTeacherName(self, obj):
        return self._get_teacher_data(obj)["name"]

    def get_StudyActivityFathers(self, obj):
        pds_list = getattr(obj, '_pds_list', None)
        if not pds_list:
            return []
            
        if any(pds.af_pds_id == obj.erog_id for pds in pds_list):
            return []
        
        unique_fathers = {}
        for pds in pds_list:
            father_id = getattr(pds, 'af_pds_id', None)
            regdid_id = getattr(pds, 'regdid_id', None)
            if father_id and father_id not in unique_fathers:
                pds_desc = "pds_desc_ita" if self._get_lang() == "it" else (is_nullable("pds_desc_eng") or "pds_desc_ita")
                name = "ana_af_desc_ita" if self._get_lang() == "it" else (is_nullable("ana_af_desc_eng") or "ana_af_desc_ita")

                father_name = getattr(pds, name, None)
                father_pds = getattr(pds, pds_desc, None)

                unique_fathers[father_id] = {
                    "FatherID": father_id,
                    "FatherName": f"{father_name} ({father_pds})",
                    "RegdidId": regdid_id
                }
        return list(unique_fathers.values())

    def get_StudyActivityStudyPlans(self, obj):
        study_plans = set()
        
        pds_list = getattr(obj, '_pds_list', None)
        if not pds_list:
            return []
        
        for pds in pds_list:
            pds_ita = getattr(pds, 'pds_desc_ita', None)
            pds_eng = getattr(pds, 'pds_desc_eng', None)

            valore = pds_ita if self._get_lang() == 'it' else (is_nullable(pds_eng) or pds_ita)
            if valore: 
                study_plans.add(valore)
                    
        return list(study_plans)

    def _get_cached_pds(self, obj):
        if not hasattr(obj, '_cached_first_pds'):
            obj._cached_first_pds = self._first_pds(obj)
        return obj._cached_first_pds

    def get_StudyActivityYear(self, obj):
        pds = self._get_cached_pds(obj)
        return pds.anno_corso if pds else None

    def get_StudyActivityAcademicYear(self, obj):
        pds = self._get_cached_pds(obj)
        return pds.aa_off_id if pds else None

    def get_StudyActivitySSDCod(self, obj):
        pds = self._get_cached_pds(obj)
        return pds.sett_cod if pds else None

    def get_StudyActivitySSD(self, obj):
        # Fix: Qui c'era un bug, chiamava self._first_pds invece del metodo cached!
        pds = self._get_cached_pds(obj)
        if pds:
            set_desc_ita = getattr(pds, "sett_desc_ita", None)
            set_desc_eng = getattr(pds, "sett_desc_eng", None)
            
            # Se la lingua è esplicitamente italiano, usa l'italiano. Altrimenti prova inglese, poi italiano.
            return set_desc_ita if self._get_lang() == 'it' else (is_nullable(set_desc_eng) or set_desc_ita)
        return None
    
    def get_StudyActivityRegDidId(self, obj):
        pds = self._get_cached_pds(obj)
        return pds.regdid_id if pds else None

    class Meta:
        model = DidatticaAttivitaFormativaErogata
        fields = [
            "StudyActivityID",
            "StudyActivityCdSID",
            "StudyActivityCdSCod",
            "StudyActivityCdSName",
            "DepartmentName",
            "DepartmentCod",
            "StudyActivityFathers",
            "StudyActivityRegDidId",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivityYear",
            "StudyActivityAcademicYear",
            "StudyActivityLanguage",
            "StudyActivitySemester",
            "StudyActivitySSDCod",
            "StudyActivitySSD",
            "StudyActivityTeacherName",
            "StudyActivityTeacherID",
            "StudyActivityStudyPlans",
            "StudyActivityPartitionCod",
            "StudyActivityPartitionDes",
            "StudyActivityExtendedPartitionCod",
            "StudyActivityExtendedPartitionDes",
        ]
        language_field_map = {
            "StudyActivityName": {"en": "mod_off_id.ana_mod_desc_eng", "it": "mod_off_id.ana_mod_desc_ita"},
            "StudyActivityLanguage": {"en": "lingua_did_desc_eng", "it": "lingua_did_desc_ita"},
            "StudyActivitySemester": {"en": "tipo_periodo_did_desc_eng", "it": "tipo_periodo_did_desc_ita"},
            "StudyActivityPartitionDes": {"en": "part_stu_desc_eng", "it": "part_stu_desc_ita"},
            "StudyActivityExtendedPartitionDes": {"en": "fatt_part_stu_desc_eng", "it": "fatt_part_stu_desc_ita"},
        }           

@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
class StudyActivitiesListSerializerBKP(PdsListMixin, ReadOnlyModelSerializer):
    StudyActivityID = serializers.IntegerField(source="erog_id", default=None)
    StudyActivityCod = serializers.CharField(source="mod_off_id.ana_mod_cod", default=None)
    StudyActivityCdSID = serializers.IntegerField(source="mod_off_id.af_off.id_cds.cds_id", default=None)
    StudyActivityCdSCod = serializers.CharField(source="mod_off_id.af_off.cds_cod", default=None)

    DepartmentName = serializers.CharField(source="mod_off_id.af_off.id_cds.dip.dip_des_it", default=None) 
    DepartmentCod = serializers.CharField(source="mod_off_id.af_off.id_cds.dip.dip_cod", default=None)
    StudyActivityCdSName = serializers.CharField(source="mod_off_id.af_off.id_cds.nome_cds_it", default=None)

    StudyActivityName = serializers.CharField(default=None)
    StudyActivityLanguage = serializers.CharField(default=None)
    StudyActivitySemester = serializers.CharField(default=None)
    StudyActivityPartitionCod = serializers.CharField(source="part_stu_cod", default=None)
    StudyActivityPartitionDes = serializers.CharField(default=None)
    StudyActivityExtendedPartitionCod = serializers.CharField(source="fatt_part_stu_cod", default=None)
    StudyActivityExtendedPartitionDes = serializers.CharField(default=None)

    StudyActivityTeacherID = serializers.SerializerMethodField()
    StudyActivityTeacherName = serializers.SerializerMethodField()
    StudyActivityStudyPlans = serializers.SerializerMethodField()
    StudyActivityFathers = serializers.SerializerMethodField()
    StudyActivityYear = serializers.SerializerMethodField()
    StudyActivityAcademicYear = serializers.SerializerMethodField()
    StudyActivityRegDidId = serializers.SerializerMethodField()
    StudyActivitySSDCod = serializers.SerializerMethodField()
    StudyActivitySSD = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request', None)
        
        self.lang = 'ita'
        if request:
            url_lang = request.query_params.get('lang')
            if url_lang in ['ita', 'eng']:
                self.lang = url_lang
            else:
                browser_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
                if browser_lang.strip().startswith('en'):
                    self.lang = 'eng'

        super().__init__(*args, **kwargs)

        self.fields['StudyActivityName'].source = f"mod_off_id.ana_mod_desc_{self.lang}"
        self.fields['StudyActivityLanguage'].source = f"lingua_did_desc_{self.lang}"
        self.fields['StudyActivitySemester'].source = f"tipo_periodo_did_desc_{self.lang}"
        self.fields['StudyActivityPartitionDes'].source = f"part_stu_desc_{self.lang}"
        self.fields['StudyActivityExtendedPartitionDes'].source = f"fatt_part_stu_desc_{self.lang}"

    def to_representation(self, instance):
        instance._pds_list = list(instance.pds.all())
        return super().to_representation(instance)

    def get_StudyActivityTeacherName(self, obj):
        return StudyActivityTeacherSerializer(obj.mod_off_id).data.get("name")

    def get_StudyActivityTeacherID(self, obj):
        return StudyActivityTeacherSerializer(obj.mod_off_id).data.get("id")

    def get_StudyActivityStudyPlans(self, obj):
        attr_name = f"pds_desc_{self.lang}"
        return {getattr(pds, attr_name, None) for pds in obj._pds_list if getattr(pds, attr_name, None)}

    def get_StudyActivityFathers(self, obj):
        if any(pds.af_pds_id == obj.erog_id for pds in obj._pds_list):
            return []
        
        serializer_data = StudyActivityFatherSerializer(obj._pds_list, many=True, context=self.context).data
        unique = {tuple(d.items()) for d in serializer_data}
        return [dict(t) for t in unique]

    def get_StudyActivityYear(self, obj):
        pds = self._first_pds(obj)
        return pds.anno_corso if pds else None

    def get_StudyActivityAcademicYear(self, obj):
        pds = self._first_pds(obj)
        return pds.aa_off_id if pds else None

    def get_StudyActivitySSDCod(self, obj):
        pds = self._first_pds(obj)
        return pds.sett_cod if pds else None

    def get_StudyActivitySSD(self, obj):
        pds = self._first_pds(obj)
        if pds:
            return getattr(pds, f"sett_desc_{self.lang}", None)
        return None

    def get_StudyActivityRegDidId(self, obj):
        pds = self._first_pds(obj)
        return pds.regdid_id if pds else None

    class Meta:
        model = DidatticaAttivitaFormativaErogata
        fields = [
            "StudyActivityID",
            "StudyActivityCdSID",
            "StudyActivityCdSCod",
            "StudyActivityCdSName",
            "DepartmentName",
            "DepartmentCod",
            "StudyActivityFathers",
            "StudyActivityRegDidId",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivityYear",
            "StudyActivityAcademicYear",
            "StudyActivityLanguage",
            "StudyActivitySemester",
            "StudyActivitySSDCod",
            "StudyActivitySSD",
            "StudyActivityTeacherName",
            "StudyActivityTeacherID",
            "StudyActivityStudyPlans",
            "StudyActivityPartitionCod",
            "StudyActivityPartitionDes",
            "StudyActivityExtendedPartitionCod",
            "StudyActivityExtendedPartitionDes",
        ]

@extend_schema_serializer(examples=examples.CDS_MORPH_SERIALIZER_EXAMPLE)
class CdsMorphSerializer(ReadOnlyModelSerializer):
    idCds = serializers.IntegerField(source="cds", help_text="The ID of the cds.")
    idCdsPrec = serializers.IntegerField(
        source="cds_prec", help_text="The id of the previous cds."
    )

    class Meta:
        model = DidatticaCdsCollegamento
        fields = ["idCds", "idCdsPrec"]


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LITE_SERIALIZER_EXAMPLE)
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
        language_field_map = {
            "name": {"it": "des", "en": "af_gen_des_eng"},
        }


@extend_schema_serializer(examples=examples.ACADEMIC_PATHWAYS_LIST_SERIALIZER_EXAMPLE)
class AcademicPathwaysListSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(
        source="pds_regdid_id", help_text="The ID of the academic pathway."
    )
    cod = serializers.CharField(
        source="pds_cod", help_text="The code of the academic pathway."
    )
    name = serializers.SerializerMethodField()
    duration = serializers.IntegerField(
        help_text="The duration in years of the academic pathway."
    )

    def get_name(self, obj):
        request = self.context.get("request", None)
        if request and request.GET.get("lang") == "en":
            return obj.pds_des_eng
        return obj.pds_des_it

    class Meta:
        model = DidatticaPdsRegolamento
        fields = ["id", "cod", "name", "duration"]


@extend_schema_serializer(examples=examples.ACADEMIC_PATHWAYS_DETAIL_SERIALIZER_EXAMPLE)
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
                StudyActivitiesLiteSerializer(activity, context=self.context).data
            )
        return grouped_data

    class Meta:
        model = DidatticaPdsRegolamento
        fields = ["id", "cod", "name", "activities"]
        # language_field_map = {
        #     "name": {"en": "pds_des_eng"},
        # }


class SortingContactsSerializer(ReadOnlyModelSerializer):
    fullName = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    teacherDepartmentID = serializers.CharField(source="personale__cd_uo_aff_org")
    teacherOffice = serializers.CharField(source="personale__ds_aff_org")
    departmentURL = serializers.CharField(source="dip_urls")

    @extend_schema_field(serializers.CharField())
    def get_fullName(self, obj):
        full_name = obj.personale.cognome + ", " + obj.personale.nome
        if obj.personale.middle_name:
            full_name += " " + obj.personale.middle_name
        return full_name

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        official = get_contacts(obj, "Posta Elettronica")
        if not official:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in official
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )
        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    class Meta:
        model = DidatticaCopertura
        fields = [
            "fullName",
            "id",
            "teacherDepartmentID",
            "teacherOffice",
            "departmentURL",
        ]


# ~ @extend_schema_serializer(examples=examples.STUDY_PLANS_SERIALIZER_EXAMPLE)
class StudyPlansActivitiesSerializer(ReadOnlyModelSerializer, LanguageAwareMixin):
    RegPlanId = serializers.IntegerField(source="piano_studio_id")
    RegDidId = serializers.IntegerField(source="regdid_id")
    # ~ relevanceCod = serializers.CharField(source="attinenza_cod")
    YearCoorteId = serializers.IntegerField(source="aa_coorte_id")
    # ~ yearRegPlanId = serializers.IntegerField(source="aa_regpiani_id")
    # ~ regPlanDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ defFlg = serializers.CharField(source="def_flg")
    # ~ statusCod = serializers.CharField(source="stato_piano_studio_cod")
    # ~ statusDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ regPlansPdrId = serializers.CharField(source="regpiani_pdr_id")
    # ~ regPlansPdrCod = serializers.CharField(source="regpiani_pdr_cod")
    # ~ regPlansPdrDes = serializers.CharField(source="regpiani_pdr_des")
    # ~ regPlansPdrCoorteIdYear = serializers.CharField(source="regpiani_pdr_aa_coorte_id")
    # ~ regPlansPdrYear = serializers.CharField(source="regpiani_pdr_aa_regpiani_id")
    # ~ flgExpSegStu = serializers.CharField(source="flg_exp_seg_stu")
    CdSDuration = serializers.IntegerField(source="regdid.cds.durata_anni")
    PlanTabs = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField())
    def get_PlanTabs(self, obj):
        lang = self._get_lang()
        result = []
        for q in obj.schemi.all():
            
            # evitiamo di prendere i percorsi part-time
            regole_standard = []
            for r in q.regole_filtrate:
                if len(q.regole_filtrate) == obj.regdid.cds.durata_anni:
                    regole_standard.append(r)

            if not regole_standard: continue

            activities = {}

            for r in regole_standard:
                activities[r.anno_corso_reg_sce] = [
                    {
                        "StudyActivityID": af.activities[0].af_pds_id,
                        "StudyActivityCod": af.activities[0].ana_af_cod,
                        "StudyActivityName": af.activities[0].ana_af_desc_ita if lang == 'it' else (is_nullable(af.activities[0].ana_af_desc_eng) or af.activities[0].ana_af_desc_ita),
                        "StudyActivityECTS": af.activities[0].cfu,
                        "StudyActivityCompulsory": True if af.activities[0].flag_obbl == 'Si' else False,
                        "StudyActivitySSD": set(activity.sett_cod for activity in af.activities),
                        "StudyActivitySemester": set(activity.erog_id.tipo_periodo_did_desc_ita for activity in af.activities if activity.erog_id) if lang == 'it' else set(is_nullable(activity.erog_id.tipo_periodo_did_desc_eng) or activity.erog_id.tipo_periodo_did_desc_ita for activity in af.activities if activity.erog_id),
                        # ~ "AfType": af.activities[0].ambito_desc_ita if len(af.activities) == 1 else None,
                        "StudyActivityTeachingUnitType": af.activities[0].taf_desc_ita if lang == 'it' else (is_nullable(af.activities[0].taf_desc_eng) or af.activities[0].taf_desc_ita) if len(af.activities) == 1 else None,
                    } for af in r.af.all() if af.activities
                ]
            
            result.append({
                "StudyPlanID": q.schema_piano_id,
                "StudyPlanCOD": q.schema_piano_cod,
                "StudyPlanName": q.schema_piano_desc_ita if lang == 'it' else (is_nullable(q.schema_piano_desc_eng) or q.schema_piano_desc_ita),
                "StudyActivities": activities
            })
        return result
        
    class Meta:
        model = DidatticaPianiStudio
        fields = [
            "RegPlanId",
            "RegDidId",
            # ~ "relevanceCod",
            "YearCoorteId",
            # ~ "yearRegPlanId",
            # ~ "regPlanDes",
            # ~ "defFlg",
            # ~ "statusCod",
            # ~ "statusDes",
            # ~ "regPlansPdrId",
            # ~ "regPlansPdrCod",
            # ~ "regPlansPdrDes",
            # ~ "regPlansPdrCoorteIdYear",
            # ~ "regPlansPdrYear",
            # ~ "flgExpSegStu",
            "CdSDuration",
            "PlanTabs",
        ]


@extend_schema_serializer(examples=examples.STUDY_PLANS_SERIALIZER_FULL_EXAMPLE)
class StudyPlansSerializer(ReadOnlyModelSerializer, LanguageAwareMixin):
    RegPlanId = serializers.IntegerField(source="piano_studio_id")
    RegDidId = serializers.IntegerField(source="regdid_id")
    # ~ relevanceCod = serializers.CharField(source="attinenza_cod")
    YearCoorteId = serializers.IntegerField(source="aa_coorte_id")
    # ~ yearRegPlanId = serializers.IntegerField(source="aa_regpiani_id")
    # ~ regPlanDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ defFlg = serializers.CharField(source="def_flg")
    StatusCod = serializers.CharField(source="stato_piano_studio_cod")
    StatusDes = serializers.CharField(source="stato_piano_studio_desc_ita")
    # ~ regPlansPdrId = serializers.CharField(source="regpiani_pdr_id")
    # ~ regPlansPdrCod = serializers.CharField(source="regpiani_pdr_cod")
    # ~ regPlansPdrDes = serializers.CharField(source="regpiani_pdr_des")
    # ~ regPlansPdrCoorteIdYear = serializers.CharField(source="regpiani_pdr_aa_coorte_id")
    # ~ regPlansPdrYear = serializers.CharField(source="regpiani_pdr_aa_regpiani_id")
    # ~ flgExpSegStu = serializers.CharField(source="flg_exp_seg_stu")
    CdSDuration = serializers.IntegerField(source="regdid.cds.durata_anni") 
    PlanTabs = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField())
    def get_PlanTabs(self, obj):
        lang = self._get_lang()
        result = []
        
        for q in obj.schemi.all():
            # ~ if q.schema_piano_cod not in result:
                # ~ result[q.schema_piano_cod] = []
                
            # ~ result[q.schema_piano_cod].append(
            result.append(
                {
                    "PlanTabId": q.schema_piano_id,
                    "PlanTabDes": q.schema_piano_desc_ita if lang == 'it' else (is_nullable(q.schema_piano_desc_eng) or q.schema_piano_desc_ita),
                    "PlanTabCod": q.schema_piano_cod,
                    "PdsDes": q.pds_regdid.pds_des_it if lang == 'it' else (is_nullable(q.pds_regdid.pds_des_eng) or q.pds_regdid.pds_des_it),
                    "ClaMiurCod": q.classe_miur_cod,
                    "ClaMiurDes": q.classe_miur_desc_ita if lang == 'it' else (is_nullable(q.classe_miur_desc_eng) or q.classe_miur_desc_ita),
                    "CommonFlg": q.pds_regdid.comune_flg,
                    "Rules": [
                        {
                            "SceId": rule.reg_sce_id,
                            "SceDes": rule.reg_sce_desc_ita if lang == 'it' else (is_nullable(rule.reg_sce_desc_eng) or rule.reg_sce_desc_ita),
                            # ~ "vinId": q["vin_id"],
                            "Year": rule.anno_corso_reg_sce,
                            # ~ if q["apt_slot_ord_num"]
                            # ~ else q["anno_corso"],
                            "RegSceCodType": rule.tipo_reg_sce_cod,
                            # ~ "regSceCodDes": q.reg_sce_desc_ita,
                            # ~ "sceCodType": q["tipo_sce_cod"],
                            # ~ "eceDesType": q["tipo_sce_des"],
                            "UmRegSceCodType": rule.tipo_um_reg_sce_cod,
                            "MinUnt": rule.minimo,
                            "MaxUnt": rule.massimo,
                            "NotePre": rule.nota_pre_desc_ita if lang == 'it' else (is_nullable(rule.nota_pre_desc_eng) or rule.nota_pre_desc_ita),
                            "NotePost": rule.nota_post_desc_ita if lang == 'it' else (is_nullable(rule.nota_post_desc_eng) or rule.nota_post_desc_ita),
                            "Filters": rule.filtri_reg_sce_desc,
                            # ~ "opzFlg": q["opz_flg"],
                            "Required": [
                                {
                                    # ~ "scopeId": q["amb_id_af"],
                                    "AfId": af.activities[0].af_pds_id,
                                    "AfCod": af.activities[0].ana_af_cod,
                                    "AfDescription": af.activities[0].ana_af_desc_ita if lang == 'it' else (is_nullable(af.activities[0].ana_af_desc_eng) or af.activities[0].ana_af_desc_ita),
                                    "CycleDes": set(
                                        activity.erog_id.tipo_periodo_did_desc_ita if lang == 'it' else (is_nullable(activity.erog_id.tipo_periodo_did_desc_eng) or activity.erog_id.tipo_periodo_did_desc_ita)
                                        for activity in af.activities
                                        if getattr(activity, 'erog_id', None)
                                    ),
                                    "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                    "SettCod": set(activity.sett_cod for activity in af.activities),
                                    "AfType": af.activities[0].ambito_desc_ita if lang == 'it' else (is_nullable(af.activities[0].ambito_desc_eng) or af.activities[0].ambito_desc_ita) if len(af.activities) == 1 else None,
                                    "AfScope": af.activities[0].taf_desc_ita if lang == 'it' else (is_nullable(af.activities[0].taf_desc_eng) or af.activities[0].taf_desc_ita) if len(af.activities) == 1 else None,
                                    "AfSubModules": [
                                        {
                                            "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                            "StudyActivityCod": m.ana_mod_cod,
                                            "StudyActivityName": m.ana_mod_desc_ita if lang == 'it' else (is_nullable(m.ana_mod_desc_eng) or m.ana_mod_desc_ita),
                                            "studyActivityPartitionCod": m.erog_id.part_stu_cod if m.erog_id and m.erog_id.part_stu_cod != "-999999999" else None,
                                            "studyActivityPartitionDes": (
                                                (m.erog_id.part_stu_desc_ita if lang == 'it' else (is_nullable(m.erog_id.part_stu_desc_eng) or m.erog_id.part_stu_desc_ita))
                                                if m.erog_id else None
                                            ),
                                            "StudyActivitySemester": (m.erog_id.tipo_periodo_did_desc_ita if lang == 'it' else (is_nullable(m.erog_id.tipo_periodo_did_desc_eng) or m.erog_id.tipo_periodo_did_desc_ita)) if m.erog_id else None,
                                            "StudyActivitySettCod": m.sett_cod,
                                            "StudyActivityCreditValue": m.cfu,
                                            "StudyActivityScope": m.ambito_desc_ita if lang == 'it' else (is_nullable(m.ambito_desc_eng) or m.ambito_desc_ita),
                                            "StudyActivityType": m.taf_desc_ita if lang == 'it' else (is_nullable(m.taf_desc_eng) or m.taf_desc_ita),
                                        } for m in af.activities
                                    ] if len(af.activities) > 1 else []
                                    
                                } for af in rule.af.all() if af.activities
                            ],
                            "AfChoices": [
                                [
                                    {
                                        # ~ "scopeId": q["amb_id_af"],
                                        "AfId": af.activities[0].af_pds_id,
                                        "AfCod": af.activities[0].ana_af_cod,
                                        "AfDescription": af.activities[0].ana_af_desc_ita if lang == 'it' else (is_nullable(af.activities[0].ana_af_desc_eng) or af.activities[0].ana_af_desc_ita),
                                        "StudyActivitySemester": (
                                            (af.activities[0].erog_id.tipo_periodo_did_desc_ita if lang == 'it' else (is_nullable(af.activities[0].erog_id.tipo_periodo_did_desc_eng) or af.activities[0].erog_id.tipo_periodo_did_desc_ita))
                                            if len(af.activities) == 1 and getattr(af.activities[0], 'erog_id', None)
                                            else None
                                        ),
                                        "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                        "SettCod": af.activities[0].sett_cod if len(af.activities) == 1 else [],
                                        "CycleDes": set(
                                            activity.erog_id.tipo_periodo_did_desc_ita if lang == 'it' else (is_nullable(activity.erog_id.tipo_periodo_did_desc_eng) or activity.erog_id.tipo_periodo_did_desc_ita)
                                            for activity in af.activities
                                            if getattr(activity, 'erog_id', None)
                                        ),
                                        "AfType": af.activities[0].ambito_desc_ita if lang == 'it' else (is_nullable(af.activities[0].ambito_desc_eng) or af.activities[0].ambito_desc_ita) if len(af.activities) == 1 else None,
                                        "AfScope": af.activities[0].taf_desc_ita if lang == 'it' else (is_nullable(af.activities[0].taf_desc_eng) or af.activities[0].taf_desc_ita) if len(af.activities) == 1 else None,
                                        "AfSubModules": [
                                            {
                                                "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                                "StudyActivityCod": m.ana_mod_cod,
                                                "StudyActivityName": m.ana_mod_desc_ita if lang == 'it' else (is_nullable(m.ana_mod_desc_eng) or m.ana_mod_desc_ita),
                                                "StudyActivitySemester": (m.erog_id.tipo_periodo_did_desc_ita if lang == 'it' else (is_nullable(m.erog_id.tipo_periodo_did_desc_eng) or m.erog_id.tipo_periodo_did_desc_ita)) if m.erog_id else None,
                                                "StudyActivitySettCod": m.sett_cod,
                                                "StudyActivityCreditValue": m.cfu,
                                                "StudyActivityScope": m.ambito_desc_ita if lang == 'it' else (is_nullable(m.ambito_desc_eng) or m.ambito_desc_ita),
                                                "StudyActivityType": m.taf_desc_ita if lang == 'it' else (is_nullable(m.taf_desc_eng) or m.taf_desc_ita),
                                            } for m in af.activities
                                        ] if len(af.activities) > 1 else []
                                        
                                    } for af in b.af_blocco.all() if af.activities
                                ] for b in rule.blocchi.all()
                            ]

                        } for rule in q.regole.all()
                    ] 
                } 
            )
        return result
        
    class Meta:
        model = DidatticaPianiStudio
        fields = [
            "RegPlanId",
            "RegDidId",
            "YearCoorteId",
            "StatusCod",
            "StatusDes",
            "CdSDuration",
            "PlanTabs",
        ]
        language_field_map = {
            "StatusDes": {"en": "stato_piano_studio_desc_eng", "it": "stato_piano_studio_desc_ita"},
        }
