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
    DidatticaCoperturaDettaglioOre
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


class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
    StudyActivityID = serializers.IntegerField(source="af_pds_id")
    StudyActivityCod = serializers.CharField(
        source="ana_mod_cod",
        help_text="",
        default=None,
    )
    StudyActivityCdSID = serializers.IntegerField(
        source="id_cds.cds_id",
        help_text="",
        default=None,
    )
    StudyActivityCdSCod = serializers.CharField(
        source="cds_cod",
        help_text="",
        default=None,
    )
    StudyActivityRegDidId = serializers.IntegerField(
        source="regdid_id",
        help_text="",
        default=None,
    )
    StudyActivityErogationYear = serializers.IntegerField(
        source="aa_off_id",
        help_text="",
        default=None,
    )
    StudyActivityECTS = serializers.IntegerField(
        source="cfu",
        help_text="",
        default=None,
    )
    StudyActivityYear = serializers.IntegerField(
        source="anno_corso",
        help_text="",
        default=None,
    )
    StudyActivityTeachingUnitTypeCod = serializers.CharField(
        source="taf_cod",
        help_text="",
        default=None,
    )
    StudyActivityTeachingUnitType = serializers.CharField(
        source="taf_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityName  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityLanguage  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityModalities  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherID  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherName  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiesModules  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityPartitions  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityRoot  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityHours  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyBorrows = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyBorrowedFrom  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitiyContents  = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityStudyPlans = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityCdSName = serializers.CharField(
        source="id_cds.nome_cds_it",
        help_text="",
        default=None,
    )
    StudyActivityCompulsory = serializers.CharField(
        source="flag_obbl",
        help_text="",
        default=None,
    )
    StudyActivitySSDCod = serializers.CharField(
        source="sett_cod",
        help_text="",
        default=None,
    )
    StudyActivitySSD = serializers.CharField(
        source="sett_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityPartitionDes = serializers.CharField(
        source="erog_id.part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivitySemester = serializers.CharField(
        source="erog_id.tipo_periodo_did_desc_ita",
        help_text="",
        default=None,
    )
    
    def get_StudyActivityName(self, obj):
        if not obj.erog_found: return obj.ana_af_desc_ita
        return obj.ana_mod_desc_ita
        
    def get_StudyActivityStudyPlans(self, obj):
        if obj.erog_found: return getattr(obj, "pds", [])
        return [obj.pds_desc_ita]
        
    def get_StudyActivityLanguage(self, obj):
        if obj.erog_found: return [obj.erog_id.lingua_did_desc_ita]
        result = []
        for erog in obj.moduli:
            result.append(erog.erog_id.lingua_did_desc_ita)
        return set(result)

    def get_StudyActivityTeacherID(self, obj):
        if obj.erog_id.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        email = obj.erog_id.mod_off_id.af_off.doc_tit_id_ab.email
        if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
            return email.split("@")[0]
        return encrypt(obj.erog_id.mod_off_id.af_off.doc_tit_matricola)

    def get_StudyActivityTeacherName(self, obj):
        try:
            doc = Personale.objects.filter(id_ab=obj.erog_id.mod_off_id.af_off.doc_tit_id_ab.id_ab).first()
            if doc: return f"{doc.cognome} {doc.nome}"
        except:
            pass
        return None

    def get_StudyActivityModalities(self, obj):
        if obj.erog_found:
            return [{
                "ModalityActivityCod": obj.mod_did_cod,
                "ModalityActivityDescription": obj.mod_did_desc_ita
            }]
        modalities = []
        for mod in obj.moduli:
            m = {
                    "ModalityActivityCod": mod.mod_did_cod,
                    "ModalityActivityDescription": mod.mod_did_desc_ita
                }
            if not m in modalities:
                modalities.append(m)
        return modalities

    def get_StudyActivitiesModules(self, obj):
        if not obj.moduli: return []
        moduli = obj.moduli.values("ana_mod_id", "ana_mod_cod", "ana_mod_desc_ita").distinct()
        if moduli.count() == 1: return []
        result = []
        for m in moduli:
            erog_list = []
            erogazioni = obj.moduli.filter(ana_mod_id=m["ana_mod_id"]).values(
                "erog_id",
                "erog_id__part_stu_cod",
                "erog_id__part_stu_desc_ita",
                "erog_id__fatt_part_stu_cod",
                "erog_id__fatt_part_stu_desc_ita",
                "erog_id__tipo_periodo_did_desc_ita",
            ).distinct().order_by("erog_id")
            if erogazioni.count() > 1:
                m_id = None
                for e in erogazioni:
                    erog_list.append(
                        {
                            "StudyActivityID": e["erog_id"],
                            "StudyActivityPartitionCod": e["erog_id__part_stu_cod"],
                            "StudyActivityPartitionDes": e["erog_id__part_stu_desc_ita"],
                            "StudyActivityExtendedPartitionCod": e["erog_id__fatt_part_stu_cod"],
                            "StudyActivityExtendedPartitionDes": e["erog_id__fatt_part_stu_desc_ita"],
                        }
                    )
            else:
                m_id = erogazioni.first()["erog_id"]
            
            result.append(
                {
                    "StudyActivityID": m_id,
                    "StudyActivityCod": m["ana_mod_cod"],
                    "StudyActivityName": m["ana_mod_desc_ita"],
                    "StudyActivitySemester": erogazioni.first()["erog_id__tipo_periodo_did_desc_ita"],
                    "StudyActivityPartitions": erog_list,
                }
            ) 
        return result
        
    def get_StudyActivityPartitions(self, obj):
        moduli = obj.moduli.values("ana_mod_id").distinct()
        if moduli.count() > 1:
            return []
        erog_list = []
        erogazioni = obj.moduli.values(
            "erog_id",
            "erog_id__part_stu_cod",
            "erog_id__part_stu_desc_ita",
            "erog_id__fatt_part_stu_cod",
            "erog_id__fatt_part_stu_desc_ita",
            "erog_id__tipo_periodo_did_desc_ita",
        ).distinct().order_by("erog_id")
        if erogazioni.count() > 1:
            for e in erogazioni:
                erog_list.append(
                    {
                        "StudyActivityID": e["erog_id"],
                        "StudyActivityPartitionCod": e["erog_id__part_stu_cod"],
                        "StudyActivityPartitionDes": e["erog_id__part_stu_desc_ita"],
                        "StudyActivityExtendedPartitionCod": e["erog_id__fatt_part_stu_cod"],
                        "StudyActivityExtendedPartitionDes": e["erog_id__fatt_part_stu_desc_ita"],
                    }
                )
        return erog_list

    def get_StudyActivityRoot(self, obj):
        if not obj.erog_found: return None
        if DidatticaAttivitaFormativaPds.objects.filter(af_pds_id=obj.erog_id.erog_id).exists():
            return None
        return {
            "StudyActivityID": obj.af_pds_id,
            "StudyActivityName": obj.ana_af_desc_ita,
            "StudyActivityCod": obj.ana_af_cod
        }

    def get_StudyActivityHours(self, obj):
        if not obj.erog_found: return []
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
            ore = cop.dettaglio_ore.all()
            for ora in ore:
                d = {
                    "ActivityType": ora.tipo_att_did_cod,
                    "Hours": ora.ore,
                    "StudyActivityTeacherID": teacher_id,
                    "StudyActivityTeacherName": f"{cop.doc_cognome} {cop.doc_nome}",
                }
                result.append(d)
        return result

    def get_StudyActivitiyBorrows(self, obj):
        result = []
        for m in obj.mutuazioni:
            for pds in m.pds.all():
                result.append({
                    "StudyActivityID": m.erog_id,
                    "StudyActivityName": pds.ana_mod_desc_ita,
                    "StudyActivityPartitionCod": m.part_stu_cod,
                    "StudyActivityPartition": m.part_stu_desc_ita,
                    "StudyActivityCdSCod": pds.cds_cod,
                    "StudyActivityCdSName": pds.id_cds.nome_cds_it,
                })
        return result
        
    def get_StudyActivitiyBorrowedFrom(self, obj):
        # ho trovato l'erog_id e corrisponde all'erogazione master
        # sono io l'attività master
        if not obj.mutuato_da: return None
        m = obj.mutuato_da.first()
        result = {
            "StudyActivityID": m.erog_id.erog_master_id,
            "StudyActivityName": m.ana_mod_desc_ita,
            "StudyActivityPartition": m.erog_id.part_stu_desc_ita,
            "StudyActivityCdSCod": m.cds_cod,
            "StudyActivityCdSName": m.id_cds.nome_cds_it,
            "StudyActivityStudyPlans": [],
        }
        for m in obj.mutuato_da:
            result["StudyActivityStudyPlans"].append(m.pds_desc_ita)
        result["StudyActivityStudyPlans"] = set(result["StudyActivityStudyPlans"])
        return result
    
    def get_StudyActivitiyContents(self, obj):
        if getattr(obj, "num_erogazioni", 1) > 1: return []
        result = []
        for testo in DidatticaTestiAfErogata.objects.filter(erog_id=obj.erog_id.erog_master_id).all():
            result.append({
                "StudyActivitiyContentCod": testo.campo_cod,
                "StudyActivitiyContentTitle": testo.campo_desc_ita,
                "StudyActivitiyContentDes": testo.testo_fmt_ita
            })
        return result
    
    class Meta:
        model = DidatticaAttivitaFormativaPds
        fields = [
            "StudyActivityID",
            "StudyActivityCod",
            "StudyActivityName",
            "StudyActivityPartitionDes",
            "StudyActivityRoot",
            "StudyActivityCdSID",
            "StudyActivityCdSCod",
            "StudyActivityRegDidId",
            "StudyActivityStudyPlans",
            "StudyActivityErogationYear",
            "StudyActivityECTS",
            "StudyActivityLanguage",
            "StudyActivityModalities",
            "StudyActivitySSDCod",
            "StudyActivitySSD",
            "StudyActivityCompulsory",
            "StudyActivityCdSName",
            "StudyActivityYear",
            "StudyActivitySemester",
            "StudyActivityTeacherID",
            "StudyActivityTeacherName",
            "StudyActivityTeachingUnitTypeCod",
            "StudyActivityTeachingUnitType",
            "StudyActivitiesModules",
            "StudyActivityPartitions",
            "StudyActivityHours",
            "StudyActivitiyBorrows",
            "StudyActivitiyBorrowedFrom",
            "StudyActivitiyContents",
        ]

        language_field_map = {
            "cds_name": {"it": "id_cds.nome_cds_it", "en": "id_cds.nome_cds_eng"},
            "sett_desc": {"it": "sett_desc_ita", "en": "sett_desc_eng"},
            "part": {"it": "erog_id.part_stu_desc_ita", "en": "erog_id.part_stu_desc_eng"},
        }

    
@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
class StudyActivitiesListSerializer(ReadOnlyModelSerializer):
    StudyActivityID = serializers.IntegerField(
        source="erog_id",
        help_text="",
        default=None,
    )
    StudyActivityCod = serializers.CharField(
        source="mod_off_id.ana_mod_cod",
        help_text="",
        default=None,
    )
    StudyActivityName = serializers.CharField(
        source="mod_off_id.ana_mod_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityCdSID = serializers.IntegerField(
        source="mod_off_id.af_off.id_cds.cds_id",
        help_text="",
        default=None,
    )
    StudyActivityCdSCod = serializers.CharField(
        source="mod_off_id.af_off.cds_cod",
        help_text="",
        default=None,
    )
    StudyActivityCdSName = serializers.CharField(
        source="mod_off_id.af_off.id_cds.nome_cds_it",
        help_text="",
        default=None,
    )
    DepartmentName = serializers.CharField(
        source="mod_off_id.af_off.id_cds.dip.dip_desc_ita",
        help_text="",
        default=None,
    )
    DepartmentCod = serializers.CharField(
        source="mod_off_id.af_off.id_cds.dip.dip_cod",
        help_text="",
        default=None,
    )
    StudyActivityLanguage = serializers.CharField(
        source="lingua_did_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivitySemester = serializers.CharField(
        source="tipo_periodo_did_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityTeacherID = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityPartitionCod = serializers.CharField(
        source="part_stu_cod",
        help_text="",
        default=None,
    )
    StudyActivityPartitionDes = serializers.CharField(
        source="part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityExtendedPartitionCod = serializers.CharField(
        source="fatt_part_stu_cod",
        help_text="",
        default=None,
    )
    StudyActivityExtendedPartitionDes = serializers.CharField(
        source="fatt_part_stu_desc_ita",
        help_text="",
        default=None,
    )
    StudyActivityStudyPlans = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityFathers = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityAcademicYear = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityYear = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitySSDCod = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivitySSD = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityRegDidId = serializers.SerializerMethodField(
        help_text=""
    )
    StudyActivityTeacherName = serializers.SerializerMethodField(
        help_text="",
    )

    def to_representation(self, instance):
        # Usiamo il prefetch in modo sicuro. 
        # Se non ci sono pds, first_pds sarà None (senza crashare!)
        # ~ instance._pds_list= list(instance.pds.all())
        instance._pds_list= list(instance.pds.all())
        return super().to_representation(instance)

    def get_StudyActivityTeacherName(self, obj):
        if obj.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            nome = obj.mod_off_id.doc_tit_id_ab.nome
            cognome = obj.mod_off_id.doc_tit_id_ab.cognome
            if nome and cognome:
                return f"{cognome} {nome}"
        except:
            pass
        return None
        
    def get_StudyActivityTeacherID(self, obj):
        if obj.mod_off_id.af_off.doc_tit_matricola == "-999999999":
            return None
        try:
            email = getattr(obj.mod_off_id.doc_tit_id_ab, "email", None)
            if email.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}"):
                return email.split("@")[0]
            return encrypt(obj.mod_off_id.af_off.doc_tit_matricola)
        except:
            pass
        return None
        
    def get_StudyActivityStudyPlans(self, obj):
        result = []
        for pds in obj._pds_list:
            result.append(pds.pds_desc_ita)
        return set(result)

    def get_StudyActivityFathers(self, obj):
        # Check in Python invece di .filter().exists()
        if any(pds.af_pds_id == obj.erog_id for pds in obj._pds_list):
            return []
        
        result = []
        for pds in obj._pds_list:
            result.append({
                "id": pds.af_pds_id,
                "cod": pds.ana_af_cod,
                "name": pds.ana_af_desc_ita,
                "pds": pds.pds_desc_ita,
            })
        return [dict(t) for t in {tuple(d.items()) for d in result}]

    def get_StudyActivityYear(self, obj):
        return obj._pds_list[0].anno_corso if obj._pds_list else None

    def get_StudyActivityAcademicYear(self, obj):
        return obj._pds_list[0].aa_off_id if obj._pds_list else None
        
    def get_StudyActivitySSDCod(self, obj):
        return obj._pds_list[0].sett_cod if obj._pds_list else None
        
    def get_StudyActivitySSD(self, obj):
        return obj._pds_list[0].sett_desc_ita if obj._pds_list else None
    
    def get_StudyActivityRegDidId(self, obj):
        return obj._pds_list[0].regdid_id if obj._pds_list else None
    
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
class StudyPlansSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(source="piano_studio_id")
    regDidId = serializers.IntegerField(source="regdid_id")
    # ~ relevanceCod = serializers.CharField(source="attinenza_cod")
    yearCoorteId = serializers.IntegerField(source="aa_coorte_id")
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
    cdSDuration = serializers.IntegerField(source="regdid.cds.durata_anni")
    planTabs = serializers.SerializerMethodField()

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.ListField())
    def get_planTabs(self, obj):
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
                "StudyPlanName": q.schema_piano_desc_ita,
                "StudyActivities": [
                    {
                        q.anno_corso_reg_sce: [
                                {
                                    "StudyActivityID": af.activities[0].af_pds_id,
                                    "StudyActivityCod": af.activities[0].ana_af_cod,
                                    "StudyActivityName": af.activities[0].ana_af_desc_ita,
                                    # ~ "CreditValue": af.activities[0].cfu if len(af.activities) == 1 else None,
                                    "StudyActivitySSD": set([activity.sett_cod for activity in af.activities]),
                                    # ~ "AfType": af.activities[0].ambito_desc_ita if len(af.activities) == 1 else None,
                                    "AfScope": af.activities[0].taf_desc_ita if len(af.activities) == 1 else None,
                                } for af in q.af.all() if af.activities
                            ],
                    } for q in regole_standard
                ]
            }
        return result
        
    class Meta:
        model = DidatticaPianiStudio
        fields = [
            "id",
            "regDidId",
            # ~ "relevanceCod",
            "yearCoorteId",
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
            "cdSDuration",
            "planTabs",
        ]
