from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import validate_file_size, validate_image_file_extension

from .settings import cds_websites_exstudents_media_path


class CdsBrochure(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    aa = models.PositiveIntegerField(db_column="AA", blank=True, null=True)
    cds = models.ForeignKey(
        "cds.DidatticaCds",
        models.DO_NOTHING,
        db_column="ID_DIDATTICA_CDS",
        blank=True,
        null=True,
        to_field="cds_id",
    )
    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=100, blank=True, null=True
    )
    num_posti = models.IntegerField(db_column="NUM_POSTI", blank=True, null=True)
    descrizione_corso_it = models.TextField(
        db_column="DESCRIZIONE_CORSO_IT", blank=True, null=True
    )
    descrizione_corso_en = models.TextField(
        db_column="DESCRIZIONE_CORSO_EN", blank=True, null=True
    )
    accesso_corso_it = models.TextField(
        db_column="ACCESSO_CORSO_IT", blank=True, null=True
    )
    accesso_corso_en = models.TextField(
        db_column="ACCESSO_CORSO_EN", blank=True, null=True
    )
    obiettivi_corso_it = models.TextField(
        db_column="OBIETTIVI_CORSO_IT", blank=True, null=True
    )
    obiettivi_corso_en = models.TextField(
        db_column="OBIETTIVI_CORSO_EN", blank=True, null=True
    )
    sbocchi_professionali_it = models.TextField(
        db_column="SBOCCHI_PROFESSIONALI_IT", blank=True, null=True
    )
    sbocchi_professionali_en = models.TextField(
        db_column="SBOCCHI_PROFESSIONALI_EN", blank=True, null=True
    )
    tasse_contributi_esoneri_it = models.TextField(
        db_column="TASSE_CONTRIBUTI_ESONERI_IT", blank=True, null=True
    )
    tasse_contributi_esoneri_en = models.TextField(
        db_column="TASSE_CONTRIBUTI_ESONERI_EN", blank=True, null=True
    )
    borse_studio_it = models.TextField(
        db_column="BORSE_STUDIO_IT", blank=True, null=True
    )
    borse_studio_en = models.TextField(
        db_column="BORSE_STUDIO_EN", blank=True, null=True
    )
    agevolazioni_it = models.TextField(
        db_column="AGEVOLAZIONI_IT", blank=True, null=True
    )
    agevolazioni_en = models.TextField(
        db_column="AGEVOLAZIONI_EN", blank=True, null=True
    )
    corso_in_pillole_it = models.TextField(
        db_column="CORSO_IN_PILLOLE_IT", blank=True, null=True
    )
    corso_in_pillole_en = models.TextField(
        db_column="CORSO_IN_PILLOLE_EN", blank=True, null=True
    )
    cosa_si_studia_it = models.TextField(
        db_column="COSA_SI_STUDIA_IT", blank=True, null=True
    )
    cosa_si_studia_en = models.TextField(
        db_column="COSA_SI_STUDIA_EN", blank=True, null=True
    )
    come_iscriversi_it = models.TextField(
        db_column="COME_ISCRIVERSI_IT", blank=True, null=True
    )
    come_iscriversi_en = models.TextField(
        db_column="COME_ISCRIVERSI_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "CDS_BROCHURE"


class CdsBrochureExStudenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome = models.CharField(db_column="NOME", max_length=1000, blank=False, null=True)
    ordine = models.PositiveIntegerField(db_column="ORDINE", blank=False, null=True)
    profilo_it = models.TextField(db_column="PROFILO_IT", blank=True, null=True)
    profilo_en = models.TextField(db_column="PROFILO_EN", blank=True, null=True)
    link_it = models.CharField(
        db_column="LINK_IT", max_length=2000, blank=True, null=True
    )
    link_en = models.CharField(
        db_column="LINK_EN", max_length=2000, blank=True, null=True
    )
    cds_brochure = models.ForeignKey(
        CdsBrochure,
        models.CASCADE,
        db_column="ID_CDS_BROCHURE",
        to_field="id",
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )
    foto = models.FileField(
        upload_to=cds_websites_exstudents_media_path,
        validators=[validate_image_file_extension, validate_file_size],
        db_column="FOTO",
        max_length=1000,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "CDS_BROCHURE_EX_STUDENTI"


class CdsBrochureLink(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    ordine = models.PositiveIntegerField(db_column="ORDINE", blank=True, null=True)
    descrizione_link_it = models.CharField(
        db_column="DESCRIZIONE_LINK_IT", max_length=2000
    )
    descrizione_link_en = models.CharField(
        db_column="DESCRIZIONE_LINK_EN", max_length=2000, blank=True, null=True
    )
    link_it = models.CharField(
        db_column="LINK_IT", max_length=2000, blank=True, null=True
    )
    link_en = models.CharField(
        db_column="LINK_EN", max_length=2000, blank=True, null=True
    )
    cds_brochure = models.ForeignKey(
        CdsBrochure,
        models.CASCADE,
        db_column="ID_CDS_BROCHURE",
        to_field="id",
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "CDS_BROCHURE_LINK"


class CdsBrochureSlider(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    cds_brochure = models.ForeignKey(
        CdsBrochure,
        models.CASCADE,
        db_column="ID_CDS_BROCHURE",
        blank=True,
        null=True,
        to_field="id",
    )
    ordine = models.IntegerField(db_column="ORDINE", blank=True, null=True)
    slider_it = models.TextField(db_column="SLIDER_IT", blank=True, null=True)
    slider_en = models.TextField(db_column="SLIDER_EN", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "CDS_BROCHURE_SLIDER"
