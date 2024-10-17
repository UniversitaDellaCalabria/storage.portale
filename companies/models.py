from django.db import models
from generics.validators import (
    validate_file_size,
    validate_image_file_extension,
    validate_piva,
)

from .settings import companies_media_path


class TipologiaAreaTecnologica(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_area_ita = models.CharField(db_column="DESCR_AREA_ITA", max_length=1000)
    descr_area_eng = models.CharField(
        db_column="DESCR_AREA_ENG", max_length=1000, blank=True, null=True
    )

    def __str__(self):  # pragma: no cover
        return self.descr_area_ita

    class Meta:
        managed = True
        db_table = "TIPOLOGIA_AREA_TECNOLOGICA"


class SpinoffStartupAreaInnovazioneS3Calabria(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_area_s3 = models.CharField(db_column="DESCR_AREA_S3", max_length=1000)

    def __str__(self):  # pragma: no cover
        return self.descr_area_s3

    class Meta:
        managed = True
        db_table = "SPINOFF_STARTUP_AREA_INNOVAZIONE_S3_CALABRIA"


class SpinoffStartupDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    piva = models.CharField(
        db_column="PIVA",
        max_length=30,
        validators=[
            validate_piva,
        ],
        unique=True,
    )
    nome_azienda = models.CharField(db_column="NOME_AZIENDA", max_length=1000)
    nome_file_logo = models.FileField(
        upload_to=companies_media_path,
        validators=[validate_image_file_extension, validate_file_size],
        db_column="NOME_FILE_LOGO",
        max_length=1000,
        blank=True,
        null=True,
    )
    descrizione_ita = models.TextField(db_column="DESCRIZIONE_ITA")
    descrizione_eng = models.TextField(
        db_column="DESCRIZIONE_ENG", blank=True, null=True
    )
    url_sito_web = models.URLField(
        db_column="URL_SITO_WEB", max_length=4000, blank=True, null=True
    )
    referente_unical = models.CharField(db_column="REFERENTE_UNICAL", max_length=1000)
    matricola_referente_unical = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        to_field="matricola",
        db_column="MATRICOLA_REFERENTE_UNICAL",
        blank=True,
        null=True,
    )
    ceo = models.CharField(db_column="CEO", max_length=1000, blank=True, null=True)
    area_tecnologica = models.ForeignKey(
        TipologiaAreaTecnologica, models.DO_NOTHING, db_column="ID_AREA_TECNOLOGICA"
    )
    area_innovazione_s3_calabria = models.ForeignKey(
        SpinoffStartupAreaInnovazioneS3Calabria,
        models.SET_NULL,
        db_column="ID_AREA_INNOVAZIONE_S3_CALABRIA",
        blank=True,
        null=True,
    )
    is_startup = models.BooleanField(db_column="IS_STARTUP", default=False)
    is_spinoff = models.BooleanField(db_column="IS_SPINOFF", default=False)
    is_active = models.BooleanField(default=True, db_column="ATTIVO")
    ordinamento = models.IntegerField(default=10, db_column="ORDINE")

    class Meta:
        managed = True
        db_table = "SPINOFF_STARTUP_DATI_BASE"
        ordering = ["ordinamento"]


class SpinoffStartupDipartimento(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    spinoff_startup_dati_base = models.ForeignKey(
        SpinoffStartupDatiBase, models.CASCADE, db_column="ID_SPINOFF_STARTUP_DATI_BASE"
    )
    nome_origine_dipartimento = models.CharField(
        db_column="NOME_ORIGINE_DIPARTIMENTO", max_length=1000
    )
    didattica_dipartimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.CASCADE,
        db_column="ID_DIDATTICA_DIPARTIMENTO",
        blank=True,
        null=True,
    )

    def __str__(self):  # pragma: no cover
        return self.nome_origine_dipartimento

    class Meta:
        managed = True
        db_table = "SPINOFF_STARTUP_DIPARTIMENTO"
