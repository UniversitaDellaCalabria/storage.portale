from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import (
    orcid_validator,
    validate_file_size,
    validate_image_file_extension,
    validate_image_size_ratio,
    validate_pdf_file_extension,
)

from teachers.settings import (
    teacher_cv_en_media_path,
    teacher_cv_ita_media_path,
    teacher_photo_media_path,
)


class DocenteMaterialeDidattico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
    )
    titolo = models.CharField(db_column="TITOLO", max_length=200)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=200, blank=True, null=True
    )
    testo = models.TextField(db_column="TESTO")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    url_testo = models.URLField(
        db_column="URL_TESTO", max_length=400, blank=True, null=True
    )
    url_testo_en = models.URLField(
        db_column="URL_TESTO_EN", max_length=400, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE")
    attivo = models.BooleanField(db_column="ATTIVO")
    dt_pubblicazione = models.DateTimeField(
        db_column="DT_PUBBLICAZIONE", blank=True, null=True
    )
    dt_inizio_validita = models.DateTimeField(
        db_column="DT_INIZIO_VALIDITA", blank=True, null=True
    )
    dt_fine_validita = models.DateTimeField(
        db_column="DT_FINE_VALIDITA", blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DOCENTE_MATERIALE_DIDATTICO"
        ordering = ("ordine", "-dt_pubblicazione", "-dt_inizio_validita")


class DocentePtaAltriDati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola = models.OneToOneField(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
        related_name="docente_pta_altri_dati",
    )
    path_foto = models.FileField(
        upload_to=teacher_photo_media_path,
        validators=[
            validate_image_file_extension,
            validate_file_size,
            validate_image_size_ratio,
        ],
        db_column="PATH_FOTO",
        max_length=500,
        blank=True,
        null=True,
    )
    path_cv_ita = models.FileField(
        upload_to=teacher_cv_ita_media_path,
        validators=[validate_pdf_file_extension, validate_file_size],
        db_column="PATH_CV_ITA",
        max_length=500,
        blank=True,
        null=True,
    )
    path_cv_en = models.FileField(
        upload_to=teacher_cv_en_media_path,
        validators=[validate_pdf_file_extension, validate_file_size],
        db_column="PATH_CV_EN",
        max_length=500,
        blank=True,
        null=True,
    )
    breve_bio = models.TextField(db_column="BREVE_BIO", blank=True, null=True)
    breve_bio_en = models.TextField(db_column="BREVE_BIO_EN", blank=True, null=True)
    orario_ricevimento = models.TextField(
        db_column="ORARIO_RICEVIMENTO", blank=True, null=True
    )
    orario_ricevimento_en = models.TextField(
        db_column="ORARIO_RICEVIMENTO_EN", blank=True, null=True
    )
    orcid = models.CharField(
        validators=[orcid_validator],
        db_column="ORCID",
        max_length=100,
        blank=True,
        null=True,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DOCENTE_PTA_ALTRI_DATI"


class DocentePtaBacheca(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
    )
    tipo_testo = models.CharField(db_column="TIPO_TESTO", max_length=100)
    tipo_testo_en = models.CharField(
        db_column="TIPO_TESTO_EN", max_length=100, blank=True, null=True
    )
    titolo = models.CharField(db_column="TITOLO", max_length=200)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=200, blank=True, null=True
    )
    testo = models.TextField(db_column="TESTO")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    url_testo = models.URLField(
        db_column="URL_TESTO", max_length=400, blank=True, null=True
    )
    url_testo_en = models.URLField(
        db_column="URL_TESTO_EN", max_length=400, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE")
    attivo = models.BooleanField(db_column="ATTIVO")
    dt_pubblicazione = models.DateTimeField(
        db_column="DT_PUBBLICAZIONE", blank=True, null=True
    )
    dt_inizio_validita = models.DateTimeField(
        db_column="DT_INIZIO_VALIDITA", blank=True, null=True
    )
    dt_fine_validita = models.DateTimeField(
        db_column="DT_FINE_VALIDITA", blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DOCENTE_PTA_BACHECA"
        ordering = ("ordine", "-dt_pubblicazione", "-dt_inizio_validita")


class PubblicazioneAutori(models.Model):
    item = models.ForeignKey(
        "PubblicazioneDatiBase", 
        models.CASCADE, 
        db_column="ITEM_ID",
    )
    codice_fiscale = models.CharField(
        db_column="CODICE_FISCALE", max_length=16, blank=True, primary_key=True
    )
    ab = models.ForeignKey(
        "addressbook.Personale",
        models.DO_NOTHING,
        db_column="ID_AB",
        blank=True,
        null=True,
        to_field="id_ab",
    )
    first_name = models.CharField(
        db_column="FIRST_NAME", max_length=1020, blank=True, null=True
    )
    last_name = models.CharField(
        db_column="LAST_NAME", max_length=1020, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PUBBLICAZIONE_AUTORI"


class PubblicazioneCollection(models.Model):
    collection_id = models.IntegerField(db_column="COLLECTION_ID", primary_key=True)
    community = models.ForeignKey(
        "PubblicazioneCommunity",
        models.DO_NOTHING,
        db_column="COMMUNITY_ID",
        blank=True,
        null=True,
    )
    collection_name = models.CharField(
        db_column="COLLECTION_NAME", max_length=512, blank=True, null=True
    )
    type_miur = models.CharField(
        db_column="TYPE_MIUR", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PUBBLICAZIONE_COLLECTION"


class PubblicazioneCommunity(models.Model):
    community_id = models.IntegerField(db_column="COMMUNITY_ID", primary_key=True)
    community_name = models.CharField(
        db_column="COMMUNITY_NAME", max_length=512, blank=True, null=True
    )
    parent_community_id = models.IntegerField(
        db_column="PARENT_COMMUNITY_ID", blank=True, null=True
    )
    parent_community_name = models.CharField(
        db_column="PARENT_COMMUNITY_NAME", max_length=512, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PUBBLICAZIONE_COMMUNITY"


class PubblicazioneDatiBase(models.Model):
    item_id = models.IntegerField(db_column="ITEM_ID", primary_key=True)
    title = models.TextField(db_column="TITLE", blank=True, null=True)
    des_abstract = models.TextField(db_column="DES_ABSTRACT", blank=True, null=True)
    des_abstracteng = models.TextField(
        db_column="DES_ABSTRACTENG", blank=True, null=True
    )
    lan_iso = models.CharField(
        db_column="LAN_ISO", max_length=200, blank=True, null=True
    )
    lan_iso_i18n = models.CharField(
        db_column="LAN_ISO_I18N", max_length=400, blank=True, null=True
    )
    collection = models.ForeignKey(
        PubblicazioneCollection,
        models.DO_NOTHING,
        db_column="COLLECTION_ID",
        blank=True,
        null=True,
    )
    date_issued_year = models.IntegerField(
        db_column="DATE_ISSUED_YEAR", blank=True, null=True
    )
    pubblicazione = models.CharField(
        db_column="PUBBLICAZIONE", max_length=1024, blank=True, null=True
    )
    label_pubblicazione = models.CharField(
        db_column="LABEL_PUBBLICAZIONE", max_length=100, blank=True, null=True
    )
    contributors = models.TextField(db_column="CONTRIBUTORS", blank=True, null=True)
    url_pubblicazione = models.URLField(
        db_column="URL_PUBBLICAZIONE", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PUBBLICAZIONE_DATI_BASE"
