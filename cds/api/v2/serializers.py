from collections import defaultdict
from .docs import examples
from django.conf import settings
from addressbook.utils import append_email_addresses
# from cds.settings import CDS_BROCHURE_IS_VISIBLE, CDS_BROCHURE_MEDIA_PATH

from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from generics.api.serializers import ReadOnlyModelSerializer
from generics.utils import encrypt, build_media_path
from rest_framework import serializers


from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsTipoCorso,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
    DidatticaCdsCollegamento,
    DidatticaTestiAf,
    DidatticaCopertura,
    DidatticaCdsPeriodi,
    DidatticaAttivitaFormativaModalita,
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

    # @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    # def get_languages(self, obj):
    #     return [lang.iso6392_cod for lang in obj.cds.lingue]

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

    # intro = serializers.SerializerMethodField()  # ??
    # doc = serializers.SerializerMethodField()  # ??
    # url = serializers.CharField(source="URL_CDS")  # ??
    # video = serializers.SerializerMethodField()  # ??
    # goals = serializers.CharField(source="OBB_SPEC")  # ??
    # access = serializers.CharField(source="REQ_ACC")  # ??
    # admission = serializers.CharField(source="REQ_ACC_2")  # ??

    profiles = serializers.SerializerMethodField()

    # finalTest = serializers.CharField(source="PROVA_FINALE")  # ??
    # finalTestMode = serializers.CharField(source="PROVA_FINALE_2")  # ??

    satisfactionSurvey = serializers.IntegerField(source="cds.codicione")
    jointDegree = serializers.CharField(source="titolo_congiunto_cod")
    studyManifesto = serializers.CharField(source="didatticacdsaltridati.manifesto_studi")
    didacticRegulation = serializers.SerializerMethodField(method_name="get_didactic_regulation")
    teachingSystem = serializers.SerializerMethodField()
    teachingSystemYear = serializers.SerializerMethodField()
    # otherData = serializers.SerializerMethodField()
    officesData = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()
    currentPeriods = serializers.SerializerMethodField()

    # @extend_schema_field(serializers.CharField())
    # def get_video(self, obj):
    #     if obj.URL_CDS_VIDEO:
    #         return build_media_path(obj.URL_CDS_VIDEO, CDS_BROCHURE_MEDIA_PATH)

    # @extend_schema_field(serializers.CharField())
    # def get_doc(self, obj):
    #     if obj.URL_CDS_DOC:
    #         return (
    #             build_media_path(obj.URL_CDS_DOC, CDS_BROCHURE_MEDIA_PATH)
    #             if CDS_BROCHURE_IS_VISIBLE
    #             else None
    #         )

    # @extend_schema_field(serializers.CharField())
    # def get_intro(self, obj):
    #     return obj.INTRO_CDS_FMT if obj.INTRO_CDS_FMT else obj.DESC_COR_BRE

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

    # @extend_schema_field(serializers.CharField())
    # def get_didacticRegulation(self, obj):
    #     altri_dati = getattr(obj, "otherData", []) or []
    #     return (
    #         build_media_path(altri_dati[0].regolamento_didattico)
    #         if altri_dati != []
    #         else None
    #     )
    
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
        list = {}
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


    # @extend_schema_field(serializers.ListField())
    # def get_otherData(self, obj):
    #     altri_dati = getattr(obj, "otherData", [])
    #     return [
    #         {
    #             "coordinatorId": ad.matricola_coordinatore,
    #             "coordinatorName": ad.nome_origine_coordinatore,
    #             "viceCoordinatorId": ad.matricola_vice_coordinatore,
    #             "viceCoordinatorName": ad.nome_origine_vice_coordinatore,
    #             "studyManifesto": ad.manifesto_studi,
    #             "educationalRules": ad.regolamento_didattico,
    #             "educationalSystem": ad.ordinamento_didattico,
    #         }
    #         for ad in altri_dati
    #     ]

    @extend_schema_field(serializers.ListField())
    def get_officesData(self, obj):
        officeData = getattr(obj, "officesData", []) or []

        return [
            {
                "ordine": item.ordine,
                "nome_ufficio": item.nome_ufficio,
                "matricola_riferimento": item.matricola_riferimento,
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


class StudyActivitiesDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source="af_id", help_text="The ID of the study activity."
    )
    genCod = serializers.CharField(
        source="af_gen_cod", help_text="Code of the study activity."
    )
    des = serializers.SerializerMethodField()
    cdsId = serializers.IntegerField(
        source="cds.cds_id", help_text="The ID of the degree program."
    )
    cdsCod = serializers.CharField(
        source="cds.cds_cod", help_text="Code of the degree program."
    )
    language = serializers.SerializerMethodField(
        help_text="List of languages available for the study activity."
    )
    regDidId = serializers.IntegerField(
        source="regdid_id",
        help_text="Regulation identifier associated with the activity.",
    )
    pdsCod = serializers.CharField(
        source="pds_cod", help_text="Code of the study plan."
    )
    pdsDes = serializers.CharField(
        source="pds_des", help_text="Description of the study plan."
    )
    erogationYear = serializers.SerializerMethodField()
    semester = serializers.CharField(
        source="ciclo_des", help_text="Semester in which the activity is offered."
    )
    erogationLanguage = serializers.SerializerMethodField()
    ects = serializers.IntegerField(
        source="peso", help_text="ECTS credits for the activity."
    )
    hours = serializers.SerializerMethodField()
    modalities = serializers.SerializerMethodField()
    ssd = serializers.CharField(
        source="sett_des", help_text="Code of the scientific-disciplinary sector (SSD)."
    )
    ssdCod = serializers.CharField(
        source="sett_cod", help_text="Description of the SSD."
    )
    compulsoryActivity = serializers.IntegerField(
        source="freq_obblig_flg",
        help_text="Flag indicating if the activity is compulsory.",
    )
    cdsName = serializers.CharField(
        source="cds.nome_cds_it", help_text="Name of the degree program in Italian."
    )
    teachingUnitTypeCod = serializers.CharField(
        source="tipo_af_cod", help_text="Code of the teaching unit type."
    )
    teachingUnitType = serializers.CharField(
        source="tipo_af_des", help_text="Description of the teaching unit type."
    )
    interclassTeachingUnitTypeCod = serializers.CharField(
        source="tipo_af_intercla_cod",
        help_text="Code of the interclass teaching unit type.",
    )
    interclassTeachingUnitType = serializers.CharField(
        source="tipo_af_intercla_des",
        help_text="Description of the interclass teaching unit type.",
    )
    teacherId = serializers.SerializerMethodField()
    # teacherName = serializers.SerializerMethodField(help_text="Full name of the teacher responsible for the activity.",)
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
    # modules = serializers.SerializerMethodField()
    root = serializers.SerializerMethodField()

    # mutuataDa = serializers.SerializerMethodField()

    def get_root(self, obj):
        return getattr(obj, "activityRoot", None)

    @extend_schema_field(serializers.CharField())
    def get_teacherId(self, obj):
        matricola = getattr(obj, "matricola_resp_did", None)
        return encrypt(matricola)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_modalities(self, obj):
        modalities = DidatticaAttivitaFormativaModalita.objects.filter(
            af_id=obj.af_id
        ).only("mod_did_af_id", "mod_did_cod", "mod_did_des")
        return [
            {
                "id": m.mod_did_af_id,
                "cod": m.mod_did_cod,
                "des": m.mod_did_des,
            }
            for m in modalities
        ]

    @extend_schema_field(serializers.ListField())
    def get_hours(self, obj):
        # Recupera le ore correlate con i dati necessari utilizzando select_related e only per l'ottimizzazione delle query
        hours = (
            DidatticaCoperturaDettaglioOre.objects.select_related(
                "coper__personale", "coper"
            )
            .filter(coper__stato_coper_cod="R", coper__af_id=obj.af_id)
            .only(
                "tipo_att_did_cod",
                "ore",
                "coper__personale__id_ab",
                "coper__personale__matricola",
                "coper__personale__nome",
                "coper__personale__cognome",
                "coper__personale__middle_name",
                "coper__personale__flg_cessato",
            )
        )

        # Appende gli indirizzi email alle ore filtrate
        append_email_addresses(hours, [h.coper.personale.id_ab for h in hours])

        # Converte le ore in un formato più leggibile
        formatted_hours = [
            {
                "tipoAttDidCod": h.tipo_att_did_cod,
                "ore": h.ore,
                "idAb": h.coper.personale.id_ab,
                "matricola": h.coper.personale.matricola,
                "name": h.coper.personale.nome,
                "lastName": h.coper.personale.cognome,
                "middleName": h.coper.personale.middle_name,
                "idCopertura": h.coper_id,
                "flgCessato": h.coper.personale.flg_cessato,
            }
            for h in hours
        ]

        # Unisce le ore duplicate basate su criteri specifici
        clean_list = []
        to_skip = set()

        for i, hour in enumerate(formatted_hours):
            if i in to_skip:
                continue

            combined_hour = hour.copy()

            for j, other_hour in enumerate(formatted_hours):
                if j <= i or j in to_skip:
                    continue

                # Verifica se possono essere combinate
                if (
                    combined_hour["tipoAttDidCod"] == other_hour["tipoAttDidCod"]
                    and combined_hour["matricola"] == other_hour["matricola"]
                    and combined_hour["idCopertura"] != other_hour["idCopertura"]
                ):
                    combined_hour["ore"] += other_hour["ore"]
                    to_skip.add(j)

            clean_list.append(combined_hour)

        return clean_list

    @extend_schema_field(serializers.CharField())
    def get_des(self, obj):
        return getattr(obj, "group_description", obj.des)

    @extend_schema_field(serializers.CharField())
    def get_erogationYear(self, obj):
        if obj.anno_corso:
            return obj.regdid.aa_reg_did + obj.anno_corso - 1
        else:
            activityRoot = getattr(obj, "activityRoot", None)
            return (
                activityRoot[0].regdid.aa_reg_did + activityRoot[0].anno_corso - 1
                if activityRoot
                else None
            )

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_language(self, obj):
        list_language = getattr(obj, "lista_lin_did_af", None)
        if list_language:
            return list_language.replace(" ", "").split(",")
        return []

    # # def get_mutuataDa(self, obj):
    #     language = self.get_requestLang()
    #     mutuata_da = None
    #     if obj.mutuata_flg == 1:
    #         mutuata_da = (
    #             DidatticaAttivitaFormativa.objects.filter(af_id=obj.af_master_id)
    #             .only(
    #                 "af_id",
    #                 "af_gen_cod",
    #                 "des",
    #                 "cds__cds_cod",
    #                 "cds__cds_id",
    #                 "cds__nome_cds_it",
    #                 "cds__nome_cds_eng",
    #                 "pds_cod",
    #                 "pds_des",
    #                 "af_gen_des_eng",
    #                 "ciclo_des",
    #                 "regdid__regdid_id",
    #                 "regdid__aa_reg_did",
    #                 "anno_corso",
    #                 "didatticacopertura__coper_peso",
    #             )
    #             .first()
    #         )
    #     return (
    #         {
    #             "afId": mutuata_da.af_id,
    #             "des": mutuata_da.des
    #             if (language == "it" or mutuata_da.af_gen_des_eng is None)
    #             else mutuata_da.af_gen_des_eng,
    #             "semester": mutuata_da.ciclo_des,
    #             "courseYear": mutuata_da.anno_corso,
    #             "erogationYear": (
    #                 mutuata_da.regdid.aa_reg_did + mutuata_da.anno_corso - 1
    #             )
    #             if mutuata_da.anno_corso
    #             else None,
    #             "regDidId": mutuata_da.regdid.regdid_id,
    #             "cdsId": mutuata_da.cds.cds_id,
    #             "cdsName": mutuata_da.cds.nome_cds_it
    #             if (language == "it" or mutuata_da.cds.nome_cds_eng is None)
    #             else mutuata_da.cds.nome_cds_eng,
    #             "cdsCod": mutuata_da.cds.cds_cod,
    #             "pdsCod": mutuata_da.pds_cod,
    #             "pdsDes": mutuata_da.pds_des,
    #         }
    #         if mutuata_da
    #         else None
    #     )

    def get_requestLang(self):
        request = self.context.get("request", None)
        return "en" if request and request.GET.get("lang") == "en" else "it"

    @extend_schema_field(serializers.CharField())
    def get_erogationLanguage(self, obj):
        language = self.get_requestLang()

        texts = (
            DidatticaTestiAf.objects.filter(tipo_testo_af_cod="LINGUA_INS")
            .only("testo_af_ita", "testo_af_eng")
            .first()
        )

        return (
            texts.testo_af_ita
            if (texts.testo_af_ita is None and language != "en") or language == "it"
            else texts.testo_af_eng
        )

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = [
            "id",
            "genCod",
            "des",
            "cdsId",
            "cdsCod",
            "language",
            "regDidId",
            "pdsCod",
            "pdsDes",
            "erogationYear",
            "erogationLanguage",
            "semester",
            "ects",
            "hours",
            "modalities",
            "ssd",
            "ssdCod",
            "compulsoryActivity",
            "cdsName",
            "teachingUnitTypeCod",
            "teachingUnitType",
            "interclassTeachingUnitTypeCod",
            "interclassTeachingUnitType",
            "teacherId",
            # "teacherName",
            "partitionCod",
            "partitionDes",
            "extendedPartitionCod",
            "extendedPartitionDes",
            # "modules",
            "root",
            # "mutuataDa",
        ]
        language_field_map = {
            "des": {"en": "af_gen_des_eng"},
            "cdsName": {"en": "cds.nome_cds_eng"},
        }


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_LIST_SERIALIZER_EXAMPLE)
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
        language_field_map = {
            "des": {"en": "af_gen_des_eng"},
        }


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
        pass

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        return encrypt(getattr(obj, "personale__matricola", None))

    class Meta:
        model = DidatticaCopertura
        fields = [
            "fullName",
            "id",
            "teacherDepartmentID",
            "teacherOffice",
            "departmentURL",
        ]
