from rest_framework import serializers
from generics.utils import encrypt

# from .docs import examples
# from drf_spectacular.utils import (
#     extend_schema_field,
#     extend_schema_serializer,
# )
from addressbook.models import Personale
from teachers.models import (
    DocenteMaterialeDidattico,
    PubblicazioneCommunity,
    PubblicazioneDatiBase,
)
from cds.models import DidatticaCopertura


class TeachersSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    departmentId = serializers.IntegerField(source="dip_id")
    departmentCod = serializers.CharField(source="dip_cod")
    departmentName = serializers.CharField(source="dip_des_it")
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

    def get_email(self, obj):
        return obj["email"] if obj["email"] != "" and obj["email"] is not None else []

    def get_id(self, obj):
        return encrypt(obj["matricola"])

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
            "departmentId",
            "departmentCod",
            "departmentName",
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
            "departmentName": {"it": "dip_des_it", "en": "dip_des_eng"},
        }


class PublicationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item_id")
    abstract = serializers.CharField(source="des_abstract")
    collection = serializers.CharField(source="collection.collection_name")
    publication = serializers.CharField(source="pubblicazione")
    label = serializers.CharField(source="label_pubblicazione")
    url = serializers.CharField(source="url_pubblicazione")

    class Meta:
        model = PubblicazioneDatiBase
        fields = [
            "id",
            "title",
            "abstract",
            "collection",
            "publication",
            "label",
            "contributors",
            "date_issued_year",
            "url",
        ]
        language_field_map = {
            "abstract": {"it": "des_abstract", "en": "des_abstracteng"},
        }


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item_id")
    title = serializers.CharField(source="title")
    abstract = serializers.CharField(source="des_abstract")
    collection = serializers.CharField(source="collection.collection_name")
    community = serializers.CharField(source="collection.collection_id.collection_name")
    publication = serializers.CharField(source="pubblicazione")
    label = serializers.CharField(source="label_pubblicazione")
    contributors = serializers.ListField(source="contributors")
    # authors = serializers.SerializerMethodField()
    url = serializers.CharField(source="url_pubblicazione")

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
            # "authors"
            "url",
        ]
        language_field_map = {
            "abstract": {"it": "des_abstract", "en": "des_abstracteng"},
        }


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
    semester = serializers.IntegerField(source="ciclo_des")
    etcs = serializers.IntegerField(source="peso")
    language = serializers.CharField(source="af__lista_lin_did_af")
    ssd = serializers.CharField(source="sett_des")
    compulsory = serializers.BooleanField(source="af__freq_obblig_flg")
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
            "cdsName": {"it": "cds_des", "en": "af__cds__nome_cds_eng"},
        }


class TeachersMaterialsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="titolo")
    text = serializers.CharField(source="testo")
    textUrl = serializers.CharField(source="url_testo")
    order = serializers.IntegerField(source="ordine")
    active = serializers.BooleanField(source="attivo")
    publicationDate = serializers.SerializerMethodField()

    def _get_teacher_obj_publication_date(self, obj):
        if not obj["dt_pubblicazione"]:
            return None
        if not obj["dt_inizio_validita"]:
            return obj["dt_pubblicazione"]
        if not obj["dt_pubblicazione"]:
            return obj["dt_inizio_validita"]
        if obj["dt_pubblicazione"] > obj["dt_inizio_validita"]:
            return obj["dt_pubblicazione"]
        return obj["dt_inizio_validita"]

    def get_publicationDate(self, obj):
        return self._get_teacher_obj_publication_date(obj)

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


class PublicationsCommunityTypesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="community_id")
    name = serializers.CharField(source="community_name")

    class Meta:
        model = PubblicazioneCommunity
        fields = [
            "id",
            "name",
        ]
