from rest_framework import serializers
from generics.utils import build_media_path, encrypt

from .docs import examples
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema_serializer,
)
from addressbook.models import Personale
from teachers.models import (
    DocenteMaterialeDidattico,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
    DocentePtaBacheca,
)
from addressbook.settings import (
    PERSON_CONTACTS_EXCLUDE_STRINGS,
    PERSON_CONTACTS_TO_TAKE,
    ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN,
)

from cds.models import DidatticaCopertura
from addressbook.utils import add_email_addresses
from structures.models import DidatticaDipartimento


@extend_schema_serializer(examples=examples.TEACHERS_SERIALIZER_EXAMPLE)
class TeachersSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    SSDCod = serializers.CharField(source="cd_ssd")
    SSDDescription = serializers.CharField(source="ds_ssd")
    CVFull = serializers.CharField(source="cv_full_it")
    CVShort = serializers.CharField(source="cv_short_it")
    profileId = serializers.IntegerField(source="profilo")
    profileDescription = serializers.CharField(source="ds_profilo")
    profileShortDescription = serializers.CharField(source="ds_profilo_breve")
    email = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.EmailField()))
    def get_email(self, obj):
        return add_email_addresses(obj["cod_fis"])

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        # return encrypt(obj["matricola"])
        if not obj.email:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in obj.email
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )

        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return (
            obj["cognome"]
            + " "
            + obj["nome"]
            + (" " + obj["middle_name"] if obj["middle_name"] else "")
        )

    class Meta:
        model = Personale
        fields = [
            "id",
            "name",
            "role",
            "roleDescription",
            "SSDCod",
            "SSDDescription",
            "CVFull",
            "CVShort",
            "profileId",
            "profileDescription",
            "profileShortDescription",
            "email",
        ]
        language_field_map = {
            "CVFull": {"it": "cv_full_it", "en": "cv_full_eng"},
            "CVShort": {"it": "cv_short_it", "en": "cv_short_eng"},
        }


@extend_schema_serializer(examples=examples.TEACHER_SERIALIZER_EXAMPLE)
class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    departmentInfo = serializers.SerializerMethodField()
    role = serializers.CharField(source="cd_ruolo")
    roleDescription = serializers.CharField(source="ds_ruolo_locale")
    SSDCod = serializers.CharField(source="cd_ssd")
    SSDDescription = serializers.CharField(source="ds_ssd")
    office = serializers.CharField(source="ds_aff_org")
    moreInfo = serializers.SerializerMethodField()
    officeReference = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    pec = serializers.SerializerMethodField()
    telOffice = serializers.SerializerMethodField()
    telCelOffice = serializers.SerializerMethodField()
    fax = serializers.SerializerMethodField()
    webSite = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()
    functions = serializers.SerializerMethodField()
    CVFull = serializers.CharField(source="cv_full_it")
    CVShort = serializers.CharField(source="cv_short_it")
    profileId = serializers.IntegerField(source="profilo")
    profileDescription = serializers.CharField(source="ds_profilo")
    profileShortDescription = serializers.CharField(source="ds_profilo_breve")

    @extend_schema_field(serializers.CharField())
    def get_id(self, obj):
        # return encrypt(obj.matricola)
        if not obj.email:
            official_email = None
        else:
            official_email = next(
                (
                    e
                    for e in obj.email
                    if e.endswith(f"@{ADDRESSBOOK_FRIENDLY_URL_MAIN_EMAIL_DOMAIN}")
                ),
                None,
            )

        return (
            official_email.split("@")[0] if official_email else encrypt(obj.matricola)
        )

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return (
            obj.cognome
            + " "
            + obj.nome
            + (" " + obj.middle_name if obj.middle_name else "")
        )

    def _get_dipartimento(self, obj):
        return DidatticaDipartimento.objects.filter(dip_cod=obj.cd_uo_aff_org.uo).only(
            "dip_id", "dip_cod", "dip_des_it", "dip_des_eng"
        )

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
    def get_departmentInfo(self, obj):
        return [
            {
                "departmentId": d.dip_id,
                "departmentCod": d.dip_cod,
                "departmentName": d.dip_des_it
                if self.context.get("language", "it") == "it"
                else d.dip_des_eng,
            }
            for d in self._get_dipartimento(obj)
        ]

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
    def get_moreInfo(self, obj):
        return [
            {
                "ORCID": obj.docente_pta_altri_dati.orcid,
                "PHOTOPATH": build_media_path(obj.docente_pta_altri_dati.path_foto),
                "PATHCV": build_media_path(obj.docente_pta_altri_dati.path_cv_ita)
                if obj.docente_pta_altri_dati.path_cv_ita
                else build_media_path(obj.docente_pta_altri_dati.path_cv_en),
                "BREVEBIO": obj.docente_pta_altri_dati.breve_bio
                if obj.docente_pta_altri_dati.breve_bio
                else obj.docente_pta_altri_dati.breve_bio_en,
                "ORARIORICEVIMENTO": obj.docente_pta_altri_dati.orario_ricevimento
                if obj.docente_pta_altri_dati.orario_ricevimento
                else obj.docente_pta_altri_dati.orario_ricevimento_en,
            }
        ]

    def get_contacts(self, obj, contactDescr):
        if contactDescr in PERSON_CONTACTS_TO_TAKE:
            for contact in obj.contatti:
                tipo = contact.cd_tipo_cont
                if tipo.descr_contatto not in PERSON_CONTACTS_EXCLUDE_STRINGS:
                    return contact.contatto
        return []

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_officeReference(self, obj):
        return self.get_contacts(obj, "Riferimento Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.EmailField()))
    def get_email(self, obj):
        return self.get_contacts(obj, "Posta Elettronica")

    @extend_schema_field(serializers.ListField(child=serializers.EmailField()))
    def get_pec(self, obj):
        return self.get_contacts(obj, "POSTA ELETTRONICA CERTIFICATA")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telOffice(self, obj):
        return self.get_contacts(obj, "Telefono Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_telCelOffice(self, obj):
        return self.get_contacts(obj, "Telefono Cellulare Ufficio")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_fax(self, obj):
        return self.get_contacts(obj, "Fax")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_webSite(self, obj):
        return self.get_contacts(obj, "URL Sito WEB")

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_cv(self, obj):
        return self.get_contacts(obj, "URL Sito WEB Curriculum Vitae")

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
    def get_functions(self, obj):
        return [
            {
                "functionCod": f.funzione,
                "structureCod": f.cd_csa.uo,
                "structureName": f.cd_csadenominazione,
            }
            for f in obj.functions
        ]

    class Meta:
        model = Personale
        fields = [
            "id",
            "name",
            "departmentInfo",
            "role",
            "roleDescription",
            "SSDCod",
            "SSDDescription",
            "office",
            "moreInfo",
            "officeReference",
            "email",
            "pec",
            "telOffice",
            "telCelOffice",
            "fax",
            "webSite",
            "cv",
            "functions",
            "CVFull",
            "CVShort",
            "profileId",
            "profileDescription",
            "profileShortDescription",
        ]


@extend_schema_serializer(examples=examples.PUBLICATIONS_SERIALIZER_EXAMPLE)
class PublicationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item_id")
    abstract = serializers.CharField(source="des_abstract")
    collection = serializers.SerializerMethodField()
    community = serializers.SerializerMethodField()
    publication = serializers.CharField(source="pubblicazione")
    label = serializers.CharField(source="label_pubblicazione")
    year = serializers.SerializerMethodField()
    url = serializers.CharField(source="url_pubblicazione")

    @extend_schema_field(serializers.CharField())
    def get_community(self, obj):
        return (
            obj.collection.community.community_name
            if obj.collection and obj.collection.community
            else None
        )

    @extend_schema_field(serializers.CharField())
    def get_collection(self, obj):
        return obj.collection.collection_name if obj.collection else None

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_year(self, obj):
        if obj.date_issued_year == 9999:
            return "in stampa"
        return obj.date_issued_year

    class Meta:
        model = PubblicazioneDatiBase
        fields = [
            "id",
            "title",
            "abstract",
            "collection",
            "community",
            "publication",
            "label",
            "year",
            "url",
        ]
        language_field_map = {
            "abstract": {"it": "des_abstract", "en": "des_abstracteng"},
        }


@extend_schema_serializer(examples=examples.PUBLICATION_SERIALIZER_EXAMPLE)
class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item_id")
    abstract = serializers.CharField(source="des_abstract")
    collection = serializers.SerializerMethodField()
    community = serializers.SerializerMethodField()
    publication = serializers.CharField(source="pubblicazione")
    label = serializers.CharField(source="label_pubblicazione")
    authors = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    url = serializers.CharField(source="url_pubblicazione")

    @extend_schema_field(
        serializers.ListField(
            child=serializers.DictField(child=serializers.CharField())
        )
    )
    def get_authors(self, obj):
        authors = []
        for a in obj.autori:
            if a.ab.matricola is None:
                full_name = a.last_name + " " + a.first_name
            else:
                full_name = a.ab.cognome + " " + a.ab.nome
                if a.ab.middle_name:
                    full_name = a.ab.cognome + " " + a.ab.nome + " " + a.ab.middle_name

            authors.append(
                {
                    "id": encrypt(a.ab.matricola),
                    "name": full_name,
                    "email": add_email_addresses(a.ab.cod_fis),
                }
            )
        return authors

    @extend_schema_field(serializers.CharField())
    def get_year(self, obj):
        if obj.date_issued_year == 9999:
            return "in stampa"
        return obj.date_issued_year

    @extend_schema_field(serializers.CharField())
    def get_community(self, obj):
        return (
            obj.collection.community.community_name
            if obj.collection and obj.collection.community
            else None
        )

    @extend_schema_field(serializers.CharField())
    def get_collection(self, obj):
        return obj.collection.collection_name if obj.collection else None

    class Meta:
        model = PubblicazioneDatiBase
        fields = [
            "id",
            "title",
            "abstract",
            "collection",
            "community",
            "publication",
            "label",
            "contributors",
            "authors",
            "year",
            "url",
        ]
        language_field_map = {
            "abstract": {"it": "des_abstract", "en": "des_abstracteng"},
        }


@extend_schema_serializer(examples=examples.TEACHERS_BASE_RESEARCH_LINES_EXAMPLE)
class TeachersBaseResearchLinesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source="ricercadocentelineabase__ricerca_linea_base__id"
    )
    description = serializers.CharField(
        source="ricercadocentelineabase__ricerca_linea_base__descrizione"
    )
    results = serializers.CharField(
        source="ricercadocentelineabase__ricerca_linea_base__descr_pubblicaz_prog_brevetto"
    )
    ERC0Id = serializers.CharField(
        source="ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__erc0_cod"
    )
    ERC0Name = serializers.CharField(
        source="ricercadocentelineabase__ricerca_linea_base__ricerca_erc2__ricerca_erc1__ricerca_erc0_cod__description"
    )

    class Meta:
        model = Personale
        fields = [
            "id",
            "description",
            "results",
            "ERC0Id",
            "ERC0Name",
        ]


@extend_schema_serializer(examples=examples.TEACHERS_APPLIED_RESEARCH_LINES_EXAMPLE)
class TeachersAppliedResearchLinesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source="ricercadocentelineaapplicata__ricerca_linea_applicata__id"
    )
    description = serializers.CharField(
        source="ricercadocentelineaapplicata__ricerca_linea_applicata__descrizione"
    )
    results = serializers.CharField(
        source="ricercadocentelineaapplicata__ricerca_linea_applicata__descr_pubblicaz_prog_brevetto"
    )
    ERC0Id = serializers.CharField(
        source="ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__erc0_cod"
    )
    ERC0Name = serializers.CharField(
        source="ricercadocentelineaapplicata__ricerca_linea_applicata__ricerca_aster2__ricerca_aster1__ricerca_erc0_cod__description"
    )

    class Meta:
        model = Personale
        fields = [
            "id",
            "description",
            "results",
            "ERC0Id",
            "ERC0Name",
        ]


@extend_schema_serializer(examples=examples.TEACHERS_STUDY_ACTIVITIES_EXAMPLE)
class TeachersStudyActivitiesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="af_id")
    cod = serializers.CharField(source="af_gen_cod")
    name = serializers.CharField(source="af_gen_des")
    cdsId = serializers.IntegerField(source="cds_id")
    cdsCod = serializers.CharField(source="cds_cod")
    regDidId = serializers.IntegerField(source="regdid_id")
    cdsName = serializers.CharField(source="cds_des")
    aa = serializers.IntegerField(source="aa_off_id")
    year = serializers.IntegerField(source="anno_corso")
    semester = serializers.CharField(source="ciclo_des")
    etcs = serializers.CharField(source="peso")
    language = serializers.CharField(source="af.lista_lin_did_af")
    ssd = serializers.CharField(source="sett_des")
    compulsory = serializers.BooleanField(source="af.freq_obblig_flg")
    partitionCod = serializers.CharField(source="fat_part_stu_cod")
    partitionDescription = serializers.CharField(source="fat_part_stu_des")
    partitionCod = serializers.IntegerField(source="part_stu_cod")
    partitionDescription = serializers.CharField(source="part_stu_des")
    partitionType = serializers.CharField(source="tipo_fat_stu_cod")
    partitionStart = serializers.CharField(source="part_ini")
    partitionEnd = serializers.CharField(source="part_fine")

    class Meta:
        model = DidatticaCopertura
        fields = [
            "id",
            "cod",
            "name",
            "cdsId",
            "cdsCod",
            "regDidId",
            "cdsName",
            "aa",
            "year",
            "semester",
            "etcs",
            "language",
            "ssd",
            "compulsory",
            "partitionCod",
            "partitionDescription",
            "partitionCod",
            "partitionDescription",
            "partitionType",
            "partitionStart",
            "partitionEnd",
        ]
        language_field_map = {
            "name": {"it": "af_gen_des", "en": "af_gen_des_eng"},
            "cdsName": {"it": "cds_des", "en": "af.cds.nome_cds_eng"},
        }


def _get_teacher_obj_publication_date(obj):
    if not obj.dt_pubblicazione:
        return None
    if not obj.dt_inizio_validita:
        return obj.dt_pubblicazione
    if not obj.dt_pubblicazione:
        return obj.dt_inizio_validita
    if obj.dt_pubblicazione > obj.dt_inizio_validita:
        return obj.dt_pubblicazione
    return obj.dt_inizio_validita


@extend_schema_serializer(examples=examples.TEACHERS_MATERIALS_EXAMPLE)
class TeachersMaterialsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="titolo")
    text = serializers.CharField(source="testo")
    textUrl = serializers.CharField(source="url_testo")
    order = serializers.IntegerField(source="ordine")
    active = serializers.BooleanField(source="attivo")
    publicationDate = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_publicationDate(self, obj):
        return _get_teacher_obj_publication_date(obj)

    class Meta:
        model = DocenteMaterialeDidattico
        fields = [
            "id",
            "title",
            "text",
            "textUrl",
            "order",
            "active",
            "publicationDate",
        ]
        language_field_map = {
            "title": {"it": "titolo", "en": "titolo_en"},
            "text": {"it": "testo", "en": "testo_en"},
            "textUrl": {"it": "url_testo", "en": "url_testo_en"},
        }


@extend_schema_serializer(examples=examples.PUBLICATIONS_COMMUNITY_TYPES_EXAMPLE)
class PublicationsCommunityTypesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="community_id")
    name = serializers.CharField(source="community_name")

    class Meta:
        model = PubblicazioneCommunity
        fields = [
            "id",
            "name",
        ]


@extend_schema_serializer(examples=examples.TEACHERS_NEWS_EXAMPLE)
class TeachersNewsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="titolo")
    textType = serializers.CharField(source="tipo_testo")
    text = serializers.CharField(source="testo")
    textUrl = serializers.CharField(source="url_testo")
    order = serializers.CharField(source="ordine")
    active = serializers.CharField(source="attivo")
    publicationDate = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_publicationDate(self, obj):
        return _get_teacher_obj_publication_date(obj)

    class Meta:
        model = DocentePtaBacheca
        fields = [
            "id",
            "title",
            "textType",
            "text",
            "textUrl",
            "order",
            "active",
            "publicationDate",
        ]
        language_field_map = {
            "title": {"it": "titolo", "en": "titolo_en"},
            "textType": {"it": "tipo_testo", "en": "tipo_testo_en"},
            "text": {"it": "testo", "en": "testo_en"},
            "textUrl": {"it": "url_testo", "en": "url_testo_en"},
        }
