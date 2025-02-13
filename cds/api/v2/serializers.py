from collections import defaultdict
from .docs import examples

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
    DidatticaCopertura
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

# @extend_schema_serializer(examples=examples.CDS_SERIALIZER_EXAMPLE)
class CdsDetailSerializer(ReadOnlyModelSerializer):
    regDidId = serializers.IntegerField(source="regdid_id")
    academicYear = serializers.IntegerField(source="aa_reg_did")
    mandatoryAttendance = serializers.SerializerMethodField(method_name="get_mandatory_attendance")
    departmentId = serializers.IntegerField(source="cds.dip.dip_id")
    departmentCod = serializers.CharField(source="cds.dip.dip_cod")
    departmentName = serializers.CharField(source="cds.dip.dip_des_it")
    cdSId = serializers.IntegerField(source="cds.cds_id")
    cdSCod = serializers.CharField(source="cds.cds_cod")
    cdsOrdId = serializers.IntegerField(source="cds.cdsord_id")
    name = serializers.CharField(source="cds.nome_cds_it")
    type = serializers.CharField(source="cds.tipo_corso_cod")
    typeDescription = serializers.CharField(source="cds.tipo_corso_des")
    courseClassCod = serializers.CharField(source="cds.cla_miur_cod")
    courseClassName = serializers.CharField(source="cds.cla_miur_des")
    courseInterClassCod = serializers.CharField(source="cds.intercla_miur_cod")
    courseInterClassDes = serializers.CharField(source="cds.intercla_miur_des")
    duration = serializers.IntegerField(source="cds.durata_anni")
    ECTS = serializers.IntegerField(source="cds.valore_min")
    codicione = serializers.IntegerField(source="cds.codicione")
    jointDegree = serializers.CharField(source="titolo_congiunto_cod")
    status = serializers.CharField(source="stato_regdid_cod")
    area = serializers.CharField(source="cds.area_cds")
    
    erogationMode = serializers.CharField(source="erogazione")
    periods = serializers.CharField(source="periods")
    currentPeriods = serializers.CharField(source="currentPeriods")
    
    languages = serializers.SerializerMethodField()
    profiles = serializers.SerializerMethodField()
    additionalData = serializers.SerializerMethodField()
    courseAdditionalData = serializers.SerializerMethodField()
    offices = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()


    @extend_schema_field(serializers.ListField())
    def get_languages(self, obj):
        request = self.context.get("request", None)
        lang = "en" if request and request.GET.get("lang") == "en" else "it"
        
        lang_list = []
        lang_list.append(obj.lingue_it if lang == "it" or obj.lingue_eng is None else obj.lingue_eng)
    
        return lang_list

    @extend_schema_field(serializers.DictField())
    def get_courseAdditionalData(self, obj):
        altri_dati = getattr(obj, 'gruppi_cds', []) or []
        return  [
            {
                "coordinatorId": data.matricola_coordinatore,
                "coordinatorName": data.nome_origine_coordinatore,
                "viceCoordinatorId": data.matricola_vice_coordinatore,
                "viceCoordinatorName": data.nome_origine_vice_coordinatore,
                "studyManifesto": data.manifesto_studi,
                "educationalRules": data.regolamento_didattico,
                "educationalSystem": data.ordinamento_didattico,
           }
            for data in altri_dati
        ]
            
    @extend_schema_field(serializers.ListField())
    def get_offices(self, obj):
        offices = getattr(obj, 'uffici_cds', []) or []
        return [
            {
                "order": office.ordine,
                "name": office.nome_ufficio,
                "contact_id": office.matricola_riferimento,
                "contact_name": office.nome_origine_riferimento,
                "phone": office.telefono,
                "email": office.email,
                "building": office.edificio,
                "floor": office.piano,
                "hours": office.orari,
                "online_counter": office.sportello_online,
            }
            for office in offices
        ]        
    
    @extend_schema_field(serializers.ListField())
    def get_groups(self, obj):
        groups = getattr(obj, 'gruppi_cds', []) or []
        return [
            {
                "order": group.ordine,
                "id": group.id,
                "short_description_it": group.descr_breve_it,
                "short_description_eng": group.descr_breve_en,
                "long_description_it": group.descr_lunga_it,
                "long_description_eng": group.descr_lunga_en,
            }
            for group in groups
        ]
    
    
    
    @extend_schema_field(serializers.BooleanField())
    def get_mandatory_attendance(self, obj):
        return bool(obj.frequenza_obbligatoria)

    @extend_schema_field(serializers.ListField())
    def get_profiles(self, obj):
        request = self.context.get("request", None)
        lang = "en" if request and request.GET.get("lang") == "en" else "it"
        
        texts = getattr(obj, 'testi_regolamento', []) or []
        list = {}
        last_profile = ""

        for text in texts:
            text_type = text.tipo_testo_regdid_cod
            text_it = text.clob_txt_ita
            text_eng = text.clob_txt_eng
            profile_it = text.profilo
            profile_eng = text.profilo_eng

            if text_type not in ["FUNZIONI", "COMPETENZE", "SBOCCHI"]:
                list.append(text_eng if (text_eng is None and lang != "it") or lang == "it" else text_it)
            else:
                selected_profile = profile_it if (lang != "it" and profile_eng is None) or lang == "it" else profile_eng
                if selected_profile != last_profile:
                    last_profile = selected_profile
                    list[last_profile] = {}
                        
            list[last_profile][text_type] = text_it if (text_eng is None and lang != "it") or lang == "it" else text_eng
                    
        return list
    
    
   
    @extend_schema_field(serializers.ListField())
    def get_additionalData(self, obj):
        request = self.context.get("request", None)
        lang = "en" if request and request.GET.get("lang") == "en" else "it"
        for data in obj.altri_dati_regolamento:
            return (data.clob_txt_ita if (data.clob_txt_ita is None and lang != "it") or lang == "it" else data.clob_txt_eng) if hasattr(obj, 'altri_dati_regolamento') else []
        
    
    

    

    class Meta:
        model = DidatticaRegolamento
        fields = [
            "regDidId",
            "academicYear",
            "mandatoryAttendance",
            "departmentId",
            "departmentCod",
            "departmentName",
            "cdSId",
            "cdSCod",
            "cdsOrdId",
            "name",
            "type",
            "typeDescription",
            "courseClassCod",
            "courseClassName",
            "courseInterClassCod",
            "courseInterClassDes",
            "duration",
            "ECTS",
            "codicione",
            "jointDegree",
            "status",
            "area",
            "erogationMode",
            "languages",
            "texts",
            "additionalData",
            "courseAdditionalData",
            "offices",
            "groups",
        ]
        # language_field_map = {
        #     "languages": {"en": "lingue_eng"},
        #     "name": {"en": "cds.nome_cds_eng"},
        #     "departmentName": {"en": "cds.dip.dip_des_eng"},
        #     "area": {"en": "cds.area_cds_en"}
        # }
        

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


class DidatticaTestiAfSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DidatticaTestiAf
        exclude = ("af",)


@extend_schema_serializer(examples=examples.STUDY_ACTIVITY_DETAIL_SERIALIZER_EXAMPLE)
class StudyActivitiesDetailSerializer(ReadOnlyModelSerializer):
    id = serializers.IntegerField(source="af_id")
    cdsordId = serializers.IntegerField(source="cdsord_id")
    cdsordCod = serializers.CharField(source="cdsord_cod")
    cdsCod = serializers.CharField(source="cds.cds_cod")
    language = serializers.SerializerMethodField()
    dipDes = serializers.CharField(source="cds.dip.dip_des_it")
    dipCod = serializers.CharField(source="cds.dip.dip_cod")
    cdsName = serializers.CharField(source="cds.nome_cds_it")
    aaOrdId = serializers.IntegerField(source="aa_ord_id")
    statoCdsordCod = serializers.CharField(source="stato_cdsord_cod")
    regdidCod = serializers.CharField(source="regdid_cod")
    aaRegdidId = serializers.IntegerField(source="aa_regdid_id")
    statoRegdidCod = serializers.CharField(source="stato_regdid_cod")
    statoApprRegdidCod = serializers.CharField(source="stato_appr_regdid_cod")
    pdsCod = serializers.CharField(source="pds_cod")
    pdsDes = serializers.CharField(source="pds_des")
    comuneFlg = serializers.IntegerField(source="comune_flg")
    attinenzaCod = serializers.CharField(source="attinenza_cod")
    ofId = serializers.IntegerField(source="of_id")
    aaOffId = serializers.IntegerField(source="aa_off_id")
    statoOfCod = serializers.CharField(source="stato_of_cod")
    tipoCompAfId = serializers.IntegerField(source="tipo_comp_af_id")
    tipoCompAfCod = serializers.CharField(source="tipo_comp_af_cod")
    desTipoCompAf = serializers.CharField(source="des_tipo_comp_af")
    afGenId = serializers.IntegerField(source="af_gen_id")
    afGenCod = serializers.CharField(source="af_gen_cod")
    des = serializers.CharField(source="group_description")
    afGenDesEng = serializers.CharField(source="af_gen_des_eng")
    annoCorso = serializers.IntegerField(source="anno_corso")
    listaAnniCorso = serializers.CharField(source="lista_anni_corso")
    regDidId = serializers.CharField(
        source="regdid_id",
    )
    settCod = serializers.CharField(source="sett_cod")
    settDes = serializers.CharField(source="sett_des")
    tipoAfCod = serializers.CharField(source="tipo_af_cod")
    tipoAfDes = serializers.CharField(source="tipo_af_des")
    tipoAfInterclaCod = serializers.CharField(source="tipo_af_intercla_cod")
    tipoAfInterclaDes = serializers.CharField(source="tipo_af_intercla_des")
    ambId = serializers.IntegerField(source="amb_id")
    ambitoDes = serializers.CharField(source="ambito_des")
    peso = serializers.IntegerField()
    umPesoCod = serializers.CharField(source="um_peso_cod")
    umPesoDes = serializers.CharField(source="um_peso_des")
    freqObbligFlg = serializers.IntegerField(source="freq_obblig_flg")
    oreMinFreq = serializers.IntegerField(source="ore_min_freq")
    oreAttFront = serializers.IntegerField(source="ore_att_front")
    numMaxReit = serializers.IntegerField(source="num_max_reit")
    liberaFlg = serializers.IntegerField(source="libera_flg")
    sceltaModFlg = serializers.IntegerField(source="scelta_mod_flg")
    tipoEsaCod = serializers.CharField(source="tipo_esa_cod")
    tipoEsaDes = serializers.CharField(source="tipo_esa_des")
    tipoValCod = serializers.CharField(source="tipo_val_cod")
    tipoValDes = serializers.CharField(source="tipo_val_des")
    tipoInsCod = serializers.CharField(source="tipo_ins_cod")
    tipoInsDes = serializers.CharField(source="tipo_ins_des")
    seraleFlg = serializers.IntegerField(source="serale_flg")
    noMediaFlg = serializers.IntegerField(source="no_media_flg")
    sostegnoFlg = serializers.IntegerField(source="sostegno_flg")
    nota = serializers.CharField()
    afPdrId = serializers.IntegerField(source="af_pdr_id")
    fatherCode = serializers.IntegerField(source="af_radice_id")
    fatherName = serializers.CharField()
    numLivAlbero = serializers.IntegerField(source="num_liv_albero")
    cicloDes = serializers.CharField(source="ciclo_des")
    dataInizio = serializers.DateTimeField(source="data_inizio")
    dataFine = serializers.DateTimeField(source="data_fine")
    tipoCicloCod = serializers.CharField(source="tipo_ciclo_cod")
    desTipoCiclo = serializers.CharField(source="des_tipo_ciclo")
    codFisRespDid = serializers.CharField(source="cod_fis_resp_did")
    ruoloRespDidCod = serializers.CharField(source="ruolo_resp_did_cod")
    urlSitoWeb = serializers.URLField(source="url_sito_web")
    listaModDidAf = serializers.CharField(source="lista_mod_did_af")
    listaTafSetCfu = serializers.CharField(source="lista_taf_set_cfu")
    mutuataFlg = serializers.IntegerField(source="mutuata_flg")
    afMasterId = serializers.IntegerField(source="af_master_id")
    numAfFiglie = serializers.IntegerField(source="num_af_figlie")
    numAfFoglie = serializers.IntegerField(source="num_af_foglie")
    nonErogabileFlg = serializers.IntegerField(source="non_erogabile_flg")
    fatPartStuCod = serializers.CharField(source="fat_part_stu_cod")
    fatPartStuDes = serializers.CharField(source="fat_part_stu_des")
    partStuId = serializers.IntegerField(source="part_stu_id")
    partStuCod = serializers.CharField(source="part_stu_cod")
    partStuDes = serializers.CharField(source="part_stu_des")
    teacherId = serializers.SerializerMethodField()
    teacherName = serializers.CharField(source="full_name")
    testiAf = DidatticaTestiAfSerializer(source="DidatticaTestiAf", read_only=True)

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
            "cdsordId",
            "cdsordCod",
            "cdsCod",
            "language",
            "dipDes",
            "dipCod",
            "testiAf",
            "teacherId",
            "teacherName",
            "cdsName",
            "regDidId",
            "aaOrdId",
            "statoCdsordCod",
            "regdidCod",
            "aaRegdidId",
            "statoRegdidCod",
            "statoApprRegdidCod",
            "pdsCod",
            "pdsDes",
            "comuneFlg",
            "attinenzaCod",
            "ofId",
            "aaOffId",
            "statoOfCod",
            "tipoCompAfId",
            "tipoCompAfCod",
            "desTipoCompAf",
            "afGenId",
            "afGenCod",
            "des",
            "afGenDesEng",
            "annoCorso",
            "listaAnniCorso",
            "fatherCode",
            "fatherName",
            "settCod",
            "settDes",
            "tipoAfCod",
            "tipoAfDes",
            "tipoAfInterclaCod",
            "tipoAfInterclaDes",
            "ambId",
            "ambitoDes",
            "peso",
            "umPesoCod",
            "umPesoDes",
            "freqObbligFlg",
            "oreMinFreq",
            "oreAttFront",
            "numMaxReit",
            "liberaFlg",
            "sceltaModFlg",
            "tipoEsaCod",
            "tipoEsaDes",
            "tipoValCod",
            "tipoValDes",
            "tipoInsCod",
            "tipoInsDes",
            "seraleFlg",
            "noMediaFlg",
            "sostegnoFlg",
            "nota",
            "afPdrId",
            "numLivAlbero",
            "cicloDes",
            "dataInizio",
            "dataFine",
            "tipoCicloCod",
            "desTipoCiclo",
            "codFisRespDid",
            "ruoloRespDidCod",
            "urlSitoWeb",
            "listaModDidAf",
            "listaTafSetCfu",
            "mutuataFlg",
            "afMasterId",
            "numAfFiglie",
            "numAfFoglie",
            "nonErogabileFlg",
            "fatPartStuCod",
            "fatPartStuDes",
            "partStuId",
            "partStuCod",
            "partStuDes",
        ]
        language_field_map = {
            "des": {"en": "af_gen_des_eng"},
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
            "departmentURL"
        ]
        
        