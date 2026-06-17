from collections import defaultdict
from .docs import examples
from django.conf import settings
from addressbook.utils import append_email_addresses, get_contacts
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import ReadOnlyModelSerializer
from generics.utils import encrypt, build_media_path
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

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'ita')
        super().__init__(*args, **kwargs)
        self.fields['ModalityActivityDescription'].source = f"mod_did_desc_{lang}"


class StudyActivityModulePartitionSerializer(serializers.Serializer):
    StudyActivityID = serializers.IntegerField(source="erog_id")
    StudyActivityPartitionCod = serializers.CharField(source="erog_id__part_stu_cod")
    StudyActivityPartitionDes = serializers.CharField(source="erog_id__part_stu_desc_ita")
    StudyActivityExtendedPartitionCod = serializers.CharField(source="erog_id__fatt_part_stu_cod")
    StudyActivityExtendedPartitionDes = serializers.CharField(source="erog_id__fatt_part_stu_desc_ita")

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'ita')
        super().__init__(*args, **kwargs)
        self.fields['StudyActivityPartitionDes'].source = f"erog_id__part_stu_desc_{lang}"
        self.fields['StudyActivityExtendedPartitionDes'].source = f"erog_id__fatt_part_stu_desc_{lang}"


class StudyActivityModuleSerializer(serializers.Serializer):
    StudyActivityID = serializers.IntegerField()
    StudyActivityCod = serializers.CharField(source="ana_mod_cod")
    StudyActivityName = serializers.CharField(source="ana_mod_desc_ita")
    StudyActivitySemester = serializers.CharField(source="erog_id__tipo_periodo_did_desc_ita")
    StudyActivityPartitions = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang', 'ita')
        self.moduli_queryset = kwargs.pop('moduli_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['StudyActivityName'].source = f"ana_mod_desc_{self.lang}"
        self.fields['StudyActivitySemester'].source = f"erog_id__tipo_periodo_did_desc_{self.lang}"

    def get_StudyActivityPartitions(self, obj):
        if not self.moduli_queryset:
            return []
        
        erogazioni = self.moduli_queryset.filter(ana_mod_id=obj["ana_mod_id"]).values(
            "erog_id",
            "erog_id__part_stu_cod",
            f"erog_id__part_stu_desc_{self.lang}",
            "erog_id__fatt_part_stu_cod",
            f"erog_id__fatt_part_stu_desc_{self.lang}",
        ).distinct().order_by("erog_id")
        
        if erogazioni.count() > 1:
            return StudyActivityModulePartitionSerializer(erogazioni, many=True, lang=self.lang).data
        return []


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

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'ita')
        super().__init__(*args, **kwargs)
        
        self.fields['StudyActivityName'].source = f"ana_mod_desc_{lang}"
        self.fields['StudyActivityPartition'].source = f"part_stu_desc_{lang}"
        self.fields['StudyActivityCdSCod'].source = "cds_cod"
        self.fields['StudyActivityCdSName'].source = f"nome_cds_{'it' if lang == 'ita' else 'eng'}"

class StudyActivityContentSerializer(serializers.Serializer):
    StudyActivitiyContentCod = serializers.CharField(source="campo_cod")
    StudyActivitiyContentTitle = serializers.CharField(source="campo_desc_ita")
    StudyActivitiyContentDes = serializers.CharField(source="testo_fmt_ita")

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'ita')
        super().__init__(*args, **kwargs)
        self.fields['StudyActivitiyContentTitle'].source = f"campo_desc_{lang}"
        self.fields['StudyActivitiyContentDes'].source = f"testo_fmt_{lang}"


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE)
class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
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
    StudyActivityPartitionDes = serializers.CharField(source="erog_id.part_stu_desc_ita", default=None)
    StudyActivitySemester = serializers.CharField(source="erog_id.tipo_periodo_did_desc_ita", default=None)

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
    StudyActivitiyBorrows = serializers.SerializerMethodField()
    StudyActivitiyBorrowedFrom = serializers.SerializerMethodField()
    StudyActivitiyContents = serializers.SerializerMethodField()

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
            
        cds_suffix = 'it' if self.lang == 'ita' else 'eng'

        super().__init__(*args, **kwargs)

        self.fields['StudyActivityTeachingUnitType'].source = f"taf_desc_{self.lang}"
        self.fields['StudyActivityCdSName'].source = f"id_cds.nome_cds_{cds_suffix}"
        self.fields['StudyActivitySSD'].source = f"sett_desc_{self.lang}"
        self.fields['StudyActivityPartitionDes'].source = f"erog_id.part_stu_desc_{self.lang}"
        self.fields['StudyActivitySemester'].source = f"erog_id.tipo_periodo_did_desc_{self.lang}"

    def get_StudyActivityName(self, obj):
        attr = f"ana_mod_desc_{self.lang}" if obj.erog_found else f"ana_af_desc_{self.lang}"
        return getattr(obj, attr, None)

    def get_StudyActivityStudyPlans(self, obj):
        if obj.erog_found:
            return getattr(obj, "pds", [])
        attr_pds = f"pds_desc_{self.lang}"
        return [getattr(obj, attr_pds, None)]

    def get_StudyActivityLanguage(self, obj):
        attr_lang = f"lingua_did_desc_{self.lang}"
        if obj.erog_found:
            val = getattr(obj.erog_id, attr_lang, None)
            return [val] if val else []
        
        return {getattr(modulo.erog_id, attr_lang) for modulo in obj.moduli if hasattr(modulo.erog_id, attr_lang)}

    def get_StudyActivityTeacherID(self, obj):
        try:
            af_off = obj.erog_id.mod_off_id.af_off
            if af_off.doc_tit_matricola == "-999999999":
                return None
            email = af_off.doc_tit_id_ab.email
            if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                return email.split("@")[0]
            return encrypt(af_off.doc_tit_matricola)
        except AttributeError:
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
            return StudyActivityModalitySerializer([obj], many=True, lang=self.lang).data
        
        seen = set()
        unique_moduli = []
        for modulo in obj.moduli:
            if modulo.mod_did_cod not in seen:
                seen.add(modulo.mod_did_cod)
                unique_moduli.append(modulo)
        return StudyActivityModalitySerializer(unique_moduli, many=True, lang=self.lang).data

    def get_StudyActivitiesModules(self, obj):
        if not obj.moduli:
            return []
        
        fields_to_value = ["ana_mod_id", "ana_mod_cod", f"ana_mod_desc_{self.lang}"]
        moduli = obj.moduli.values(*fields_to_value).distinct()
        if moduli.count() == 1:
            return []

        result = []
        for m in moduli:
            erogazioni = obj.moduli.filter(ana_mod_id=m["ana_mod_id"]).values(
                "erog_id",
                "erog_id__part_stu_cod",
                f"erog_id__part_stu_desc_{self.lang}",
                "erog_id__fatt_part_stu_cod",
                f"erog_id__fatt_part_stu_desc_{self.lang}",
                f"erog_id__tipo_periodo_did_desc_{self.lang}",
            ).distinct().order_by("erog_id")

            if erogazioni.count() > 1:
                m_id = None
                erog_list = StudyActivityModulePartitionSerializer(erogazioni, many=True, lang=self.lang).data
            else:
                first_erog = erogazioni.first()
                m_id = first_erog["erog_id"] if first_erog else None
                erog_list = []

            first_elem = erogazioni.first()
            result.append({
                "StudyActivityID": m_id,
                "StudyActivityCod": m["ana_mod_cod"],
                "StudyActivityName": m[f"ana_mod_desc_{self.lang}"],
                "StudyActivitySemester": first_elem[f"erog_id__tipo_periodo_did_desc_{self.lang}"] if first_elem else None,
                "StudyActivityPartitions": erog_list,
            })
        return result

    def get_StudyActivityPartitions(self, obj):
        moduli = obj.moduli.values("ana_mod_id").distinct()
        if moduli.count() > 1:
            return []
        
        erogazioni = obj.moduli.values(
            "erog_id",
            "erog_id__part_stu_cod",
            f"erog_id__part_stu_desc_{self.lang}",
            "erog_id__fatt_part_stu_cod",
            f"erog_id__fatt_part_stu_desc_{self.lang}",
        ).distinct().order_by("erog_id")
        
        if erogazioni.count() > 1:
            return StudyActivityModulePartitionSerializer(erogazioni, many=True, lang=self.lang).data
        return []

    def get_StudyActivityRoot(self, obj):
        if not obj.erog_found:
            return None
            
        # ~ if DidatticaAttivitaFormativaPds.objects.filter(af_pds_id=obj.erog_id.erog_id).exists():
        if obj.af_pds_id==obj.erog_id.erog_id:
            return None
        
        return {
            "StudyActivityID": obj.af_pds_id,
            "StudyActivityName": getattr(obj, f"ana_af_desc_{self.lang}", None),
            "StudyActivityCod": obj.ana_af_cod
        }

    def get_StudyActivityHours(self, obj):
        if not obj.erog_found:
            return []
        
        coperture = getattr(obj.erog_id, 'coperture_attive', [])
        result = []
        for cop in coperture:
            teacher_id = None
            if cop.doc_matricola != "-999999999":
                email = getattr(cop.doc_id_ab, "email", None)
                if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                    teacher_id = email.split("@")[0]
                else:
                    teacher_id = encrypt(cop.doc_matricola)
            
            serializer = StudyActivityHourSerializer(
                cop.dettaglio_ore.all(), 
                many=True, 
                teacher_id=teacher_id, 
                teacher_name=f"{cop.doc_cognome} {cop.doc_nome}"
            )
            result.extend(serializer.data)
        return result

    def get_StudyActivitiyBorrows(self, obj):
        mapped_mutuazioni = []
        cds_suffix = 'it' if self.lang == 'ita' else 'eng'
        
        for m in obj.mutuazioni:
            for pds in m.pds.all():
                mapped_mutuazioni.append({
                    "erog_id": m.erog_id,
                    f"ana_mod_desc_{self.lang}": getattr(pds, f"ana_mod_desc_{self.lang}", None),
                    "part_stu_cod": m.part_stu_cod,
                    f"part_stu_desc_{self.lang}": getattr(m, f"part_stu_desc_{self.lang}", None),
                    "cds_cod": pds.cds_cod,
                    f"nome_cds_{cds_suffix}": getattr(pds.id_cds, f"nome_cds_{cds_suffix}", None),
                })
        return StudyActivityBorrowSerializer(mapped_mutuazioni, many=True, lang=self.lang).data

    def get_StudyActivitiyBorrowedFrom(self, obj):
        if not obj.mutuato_da:
            return None
        
        m = obj.mutuato_da[0]
        cds_suffix = 'it' if self.lang == 'ita' else 'eng'
        
        result = {
            "StudyActivityID": m.erog_id.erog_master_id,
            "StudyActivityName": getattr(m, f"ana_mod_desc_{self.lang}", None),
            "StudyActivityPartition": getattr(m.erog_id, f"part_stu_desc_{self.lang}", None),
            "StudyActivityCdSCod": m.cds_cod,
            "StudyActivityCdSName": getattr(m.id_cds, f"nome_cds_{cds_suffix}", None),
            "StudyActivityStudyPlans": [],
        }
        
        attr_pds = f"pds_desc_{self.lang}"
        for item in obj.mutuato_da:
            result["StudyActivityStudyPlans"].append(getattr(item, attr_pds, None))
            
        result["StudyActivityStudyPlans"] = set(result["StudyActivityStudyPlans"])
        return result

    def get_StudyActivitiyContents(self, obj):
        if getattr(obj, "num_erogazioni", 1) > 1 or not obj.erog_found:
            return []
        
        # Recupera i testi direttamente dalla cache in memoria del prefetch
        testi_precaricati = obj.erog_id.testi.all()
        return StudyActivityContentSerializer(testi_precaricati, many=True, lang=self.lang).data



        
        # ~ if getattr(obj, "num_erogazioni", 1) > 1:
            # ~ return []
        
        # ~ testi_queryset = DidatticaTestiAfErogata.objects.filter(erog_id=obj.erog_id.erog_master_id)
        # ~ return StudyActivityContentSerializer(testi_queryset, many=True, lang=self.lang).data

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
            "StudyActivityHours", "StudyActivitiyBorrows", "StudyActivitiyBorrowedFrom", "StudyActivitiyContents",
        ]

class PdsListMixin:
    """Mixin con helper per accedere a _pds_list in modo sicuro."""

    def _first_pds(self, obj):
        return obj._pds_list[0] if obj._pds_list else None


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


class StudyActivityFatherSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="af_pds_id")
    cod = serializers.CharField(source="ana_af_cod")
    name = serializers.CharField(source="ana_af_desc_ita")
    pds = serializers.CharField(source="pds_desc_ita")

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request', None)
        
        lang = 'ita'
        if request:
            url_lang = request.query_params.get('lang')
            if url_lang in ['ita', 'eng']:
                lang = url_lang
            else:
                browser_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
                if browser_lang.strip().startswith('en'):
                    lang = 'eng'

        super().__init__(*args, **kwargs)

        self.fields['name'].source = f"ana_af_cod_desc_{lang}"
        self.fields['pds'].source = f"pds_desc_{lang}"


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
class StudyActivitiesListSerializer(PdsListMixin, ReadOnlyModelSerializer):
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

    # Convertiti in MethodField ottimizzati
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
        # Mettiamo in cache la lista dei pds per evitare query N+1 successive
        if hasattr(instance, 'pds_filtrati'):
            instance._pds_list = list(instance.pds_filtrati)
        # Se l'utente NON ha usato il filtro, restituiamo tutti i PDS normalmente
        instance._pds_list = list(instance.pds.all())
        # ~ instance._pds_list = list(instance.pds.all())
        return super().to_representation(instance)

    # --- 1. FUNZIONE DI CACHE PER LA LOGICA DEI DOCENTI (Sostituisce il vecchio sub-serializer) ---
    def _get_teacher_data(self, obj):
        if hasattr(obj, '_cached_teacher_data'):
            return obj._cached_teacher_data

        mod_off = obj.mod_off_id
        teacher_info = {"id": None, "name": None}

        # Controllo iniziale sulla matricola
        if not mod_off or getattr(mod_off.af_off, "doc_tit_matricola", None) == "-999999999":
            obj._cached_teacher_data = teacher_info
            return teacher_info

        # Calcolo ID (con controllo dominio ed eventuale cifratura)
        try:
            email = getattr(mod_off.doc_tit_id_ab, "email", None)
            if email and email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                teacher_info["id"] = email.split("@")[0]
            else:
                teacher_info["id"] = encrypt(mod_off.af_off.doc_tit_matricola)
        except Exception:
            pass

        # Calcolo Name
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

    # --- 2. OTTIMIZZAZIONE FATHERS (Senza StudyActivityFatherSerializer) ---
    def get_StudyActivityFathers(self, obj):
        if any(pds.af_pds_id == obj.erog_id for pds in obj._pds_list):
            return []
        
        # Estraiamo i dati unici via dizionario Python nativo basandoci su af_pds_id (o la chiave del padre)
        unique_fathers = {}
        for pds in obj._pds_list:
            father_id = getattr(pds, 'af_pds_id', None) # Modifica questo campo se la chiave del padre è un'altra
            if father_id and father_id not in unique_fathers:
                unique_fathers[father_id] = {
                    "FatherID": father_id,
                    "FatherName": getattr(pds, f"pds_desc_{self.lang}", None) # Adatta le chiavi a quelle che sputava fuori il vecchio serializer
                }
        return list(unique_fathers.values())

    def get_StudyActivityStudyPlans(self, obj):
        attr_name = f"pds_desc_{self.lang}"
        return set([getattr(pds, attr_name, None) for pds in obj._pds_list if getattr(pds, attr_name, None)])

    # --- 3. FUNZIONE DI CACHE PER RIDURRE LE CHIAMATE A _first_pds da 5 a 1 ---
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
        pds = self._get_cached_pds(obj)
        return getattr(pds, f"sett_desc_{self.lang}", None) if pds else None

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
    name = serializers.SerializerMethodField()
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

    def get_name(self, obj):
        request = self.context.get("request", None)
        if request and request.GET.get("lang") == "en":
            return obj.af_gen_des_eng
        return obj.des

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = ["id", "name", "year", "cycle", "etcs", "type"]


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
class StudyPlansActivitiesSerializer(ReadOnlyModelSerializer):
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

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_PlanTabs(self, obj):
        lang = self.get_requestLang()
        result = {}
        for q in obj.schemi.all():
            
            # evitiamo di prendere i percorsi part-time
            regole_standard = []
            for r in q.regole_filtrate:
                if len(q.regole_filtrate) == obj.regdid.cds.durata_anni:
                    regole_standard.append(r)

            if not regole_standard: continue
        
            result[q.schema_piano_id] = {
                "StudyPlanCOD": q.schema_piano_cod,
                "StudyPlanName": getattr(q, f"schema_piano_desc_{self.lang}", None),
                "StudyActivities": [
                    {
                        q.anno_corso_reg_sce: [
                                {
                                    "StudyActivityID": af.activities[0].af_pds_id,
                                    "StudyActivityCod": af.activities[0].ana_af_cod,
                                    "StudyActivityName": getattr(af.activities[0], f"ana_af_desc_{self.lang}", None),
                                    # ~ "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                    "StudyActivitySSD": set([activity.sett_cod for activity in af.activities]),
                                    # ~ "AfType": af.activities[0].ambito_desc_ita if len(af.activities) == 1 else None,
                                    "AfScope": getattr(af.activities[0], f"taf_desc_{self.lang}", None) if len(af.activities) == 1 else None,
                                } for af in q.af.all() if af.activities
                            ],
                    } for q in regole_standard
                ]
            }
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
class StudyPlansSerializer(ReadOnlyModelSerializer):
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

        self.fields['StatusDes'].source = f"stato_piano_studio_desc_{self.lang}"

    @extend_schema_field(serializers.ListField())
    def get_PlanTabs(self, obj):
        result = {}
        
        for q in obj.schemi.all():
            if q.schema_piano_cod not in result:
                result[q.schema_piano_cod] = []
                
            result[q.schema_piano_cod].append(
                {
                    "PlanTabId": q.schema_piano_id,
                    "PlanTabDes": getattr(q, f"schema_piano_desc_{self.lang}", None),
                    "PlanTabCod": q.schema_piano_cod,
                    # ~ "pdsCod": q.pds_regdid.pds_cod,
                    # ~ "pdsDes": q.pds_regdid.pds_des_it,
                    "ClaMiurCod": q.classe_miur_cod,
                    "ClaMiurDes": getattr(q, f"classe_miur_desc_{self.lang}", None),
                    "CommonFlg": q.pds_regdid.comune_flg,
                    "Rules": [
                        {
                            "SceId": rule.reg_sce_id,
                            "SceDes": getattr(rule, f"reg_sce_desc_{self.lang}", None),
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
                            "NotePre": getattr(rule, f"nota_pre_desc_{self.lang}", None),
                            "NotePost": getattr(rule, f"nota_post_desc_{self.lang}", None),
                            "Filters": rule.filtri_reg_sce_desc,
                            # ~ "opzFlg": q["opz_flg"],
                            "AfSubModules": [
                                {
                                    # ~ "scopeId": q["amb_id_af"],
                                    "StudyActivityID": af.activities[0].af_pds_id,
                                    "StudyActivityCod": af.activities[0].ana_af_cod,
                                    "StudyActivityName": getattr(af.activities[0], f"ana_af_desc_{self.lang}", None),
                                    "StudyActivitySemester": set([getattr(activity.erog_id, f"tipo_periodo_did_desc_{self.lang}", None) for activity in af.activities if getattr(activity, 'erog_id', None)]),
                                    "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                    "SettCod": set([activity.sett_cod for activity in af.activities]),
                                    "AfType": getattr(af.activities[0], f"ambito_desc_{self.lang}", None) if len(af.activities) == 1 else None,
                                    "AfScope": getattr(af.activities[0], f"taf_desc_{self.lang}", None) if len(af.activities) == 1 else None,
                                    "AfSubModules": [
                                        {
                                            "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                            "StudyActivityCod": m.ana_mod_cod,
                                            "StudyActivityName": getattr(m, f"ana_mod_desc_{self.lang}", None),
                                            "studyActivityPartitionCod": m.erog_id.part_stu_cod if m.erog_id and m.erog_id.part_stu_cod != "-999999999" else None,
                                            "studyActivityPartitionDes": getattr(m.erog_id, f"part_stu_desc_{self.lang}", None) if m.erog_id and getattr(m.erog_id, f"part_stu_desc_{self.lang}", None) != "#NULL#" else None,
                                            "StudyActivitySemester": getattr(m.erog_id, f"tipo_periodo_did_desc_{self.lang}", None) if m.erog_id else None,
                                            "StudyActivitySettCod": m.sett_cod,
                                            "StudyActivityCreditValue": m.cfu,
                                            "StudyActivityScope": getattr(m, f"ambito_desc_{self.lang}", None),
                                            "StudyActivityType": getattr(m, f"taf_desc_{self.lang}", None),
                                        } for m in af.activities
                                    ] if len(af.activities) > 1 else []
                                    
                                } for af in rule.af.all() if af.activities
                            ],
                            "blocchi": [
                                [
                                    {
                                        # ~ "scopeId": q["amb_id_af"],
                                        "AfId": af.activities[0].af_pds_id,
                                        "AfCod": af.activities[0].ana_af_cod,
                                        "AfDescription": getattr(af.activities[0], f"ana_af_desc_{self.lang}", None),
                                        "StudyActivitySemester": getattr(af.activities[0].erog_id, f"tipo_periodo_did_desc_{self.lang}", None) if len(af.activities) == 1 and getattr(af.activities[0], 'erog_id', None) else None,
                                        "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                        "SettCod": af.activities[0].sett_cod if len(af.activities) == 1 else None,
                                        "AfType": getattr(af.activities[0], f"ambito_desc_{self.lang}", None) if len(af.activities) == 1 else None,
                                        "AfScope": getattr(af.activities[0], f"taf_desc_{self.lang}", None) if len(af.activities) == 1 else None,
                                        "AfSubModules": [
                                            {
                                                "StudyActivityID": m.erog_id.erog_id if m.erog_id else None,
                                                "StudyActivityCod": m.ana_mod_cod,
                                                "StudyActivityName": getattr(m, f"ana_mod_desc_{self.lang}", None),
                                                "StudyActivitySemester": getattr(m.erog_id, f"tipo_periodo_did_desc_{self.lang}", None) if m.erog_id else None,
                                                "StudyActivitySettCod": m.sett_cod,
                                                "StudyActivityCreditValue": m.cfu,
                                                "StudyActivityScope": getattr(m, f"ambito_desc_{self.lang}", None),
                                                "StudyActivityType": getattr(m, f"taf_desc_{self.lang}", None),
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
