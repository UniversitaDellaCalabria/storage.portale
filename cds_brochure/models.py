from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import validate_file_size, validate_image_file_extension

from .settings import cds_websites_exstudents_media_path


class SitoWebCdsDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    # id_didattica_regolamento = models.ForeignKey(DidatticaRegolamento, models.DO_NOTHING, db_column='ID_DIDATTICA_REGOLAMENTO', blank=True, null=True, to_field='regdid_id')
    aa = models.PositiveIntegerField(db_column="AA", blank=True, null=True)
    cds = models.ForeignKey(
        "cds.DidatticaCds",
        models.DO_NOTHING,
        db_column="CDS_ID",
        blank=True,
        null=True,
        to_field="cds_id",
    )
    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=100, blank=True, null=True
    )
    # nome_corso_it = models.CharField(db_column='NOME_CORSO_IT', max_length=500)
    # nome_corso_en = models.CharField(db_column='NOME_CORSO_EN', max_length=500, blank=True, null=True)
    # classe_laurea_it = models.CharField(db_column='CLASSE_LAUREA_IT', max_length=100, blank=True, null=True)
    # classe_laurea_en = models.CharField(db_column='CLASSE_LAUREA_EN', max_length=100, blank=True, null=True)
    # classe_laurea_interclasse_it = models.CharField(db_column='CLASSE_LAUREA_INTERCLASSE_IT', max_length=100, blank=True, null=True)
    # classe_laurea_interclasse_en = models.CharField(db_column='CLASSE_LAUREA_INTERCLASSE_EN', max_length=100, blank=True, null=True)
    # lingua_it = models.CharField(db_column='LINGUA_IT', max_length=200, blank=True, null=True)
    # lingua_en = models.CharField(db_column='LINGUA_EN', max_length=200, blank=True, null=True)
    # durata = models.CharField(db_column='DURATA', max_length=100, blank=True, null=True)
    num_posti = models.IntegerField(db_column="NUM_POSTI", blank=True, null=True)
    # link_video_cds_it = models.CharField(db_column='LINK_VIDEO_CDS_IT', max_length=500, blank=True, null=True)
    # link_video_cds_en = models.CharField(db_column='LINK_VIDEO_CDS_EN', max_length=500, blank=True, null=True)
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
    # sito_web_it = models.CharField(db_column='SITO_WEB_IT', max_length=2000, blank=True, null=True)
    # sito_web_en = models.CharField(db_column='SITO_WEB_EN', max_length=2000, blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="ID_USER_MOD",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_DATI_BASE"


class SitoWebCdsDatiExcelTmpOld(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_corso_it = models.CharField(db_column="NOME_CORSO_IT", max_length=500)
    classe_laurea_it = models.CharField(
        db_column="CLASSE_LAUREA_IT", max_length=100, blank=True, null=True
    )
    classe_laurea_interclasse = models.CharField(
        db_column="CLASSE_LAUREA_INTERCLASSE", max_length=100, blank=True, null=True
    )
    lingua = models.CharField(db_column="LINGUA", max_length=200, blank=True, null=True)
    durata = models.CharField(db_column="DURATA", max_length=100, blank=True, null=True)
    num_posti = models.IntegerField(db_column="NUM_POSTI", blank=True, null=True)
    link_video_cds = models.CharField(
        db_column="LINK_VIDEO_CDS", max_length=500, blank=True, null=True
    )
    slider_autopromo1 = models.TextField(
        db_column="SLIDER_AUTOPROMO1", blank=True, null=True
    )
    slider_autopromo2 = models.TextField(
        db_column="SLIDER_AUTOPROMO2", blank=True, null=True
    )
    slider_autopromo3 = models.TextField(
        db_column="SLIDER_AUTOPROMO3", blank=True, null=True
    )
    descrizione_corso = models.TextField(
        db_column="DESCRIZIONE_CORSO", blank=True, null=True
    )
    accesso_corso = models.TextField(db_column="ACCESSO_CORSO", blank=True, null=True)
    obiettivi_corso = models.TextField(
        db_column="OBIETTIVI_CORSO", blank=True, null=True
    )
    sbocchi_professionali = models.TextField(
        db_column="SBOCCHI_PROFESSIONALI", blank=True, null=True
    )
    tasse_contributi_esoneri = models.TextField(
        db_column="TASSE_CONTRIBUTI_ESONERI", blank=True, null=True
    )
    borse_studio = models.TextField(db_column="BORSE_STUDIO", blank=True, null=True)
    agevolazioni = models.TextField(db_column="AGEVOLAZIONI", blank=True, null=True)
    corso_in_pillole = models.TextField(
        db_column="CORSO_IN_PILLOLE", blank=True, null=True
    )
    cosa_si_studia = models.TextField(db_column="COSA_SI_STUDIA", blank=True, null=True)
    come_iscriversi = models.TextField(
        db_column="COME_ISCRIVERSI", blank=True, null=True
    )
    descrizione_file1 = models.TextField(
        db_column="DESCRIZIONE_FILE1", blank=True, null=True
    )
    link_file1 = models.TextField(db_column="LINK_FILE1", blank=True, null=True)
    descrizione_file2 = models.TextField(
        db_column="DESCRIZIONE_FILE2", blank=True, null=True
    )
    link_file2 = models.TextField(db_column="LINK_FILE2", blank=True, null=True)
    descrizione_file3 = models.TextField(
        db_column="DESCRIZIONE_FILE3", blank=True, null=True
    )
    link_file3 = models.TextField(db_column="LINK_FILE3", blank=True, null=True)
    descrizione_file4 = models.TextField(
        db_column="DESCRIZIONE_FILE4", blank=True, null=True
    )
    link_file4 = models.TextField(db_column="LINK_FILE4", blank=True, null=True)
    descrizione_file5 = models.TextField(
        db_column="DESCRIZIONE_FILE5", blank=True, null=True
    )
    link_file5 = models.TextField(db_column="LINK_FILE5", blank=True, null=True)
    descrizione_file6 = models.TextField(
        db_column="DESCRIZIONE_FILE6", blank=True, null=True
    )
    link_file6 = models.TextField(db_column="LINK_FILE6", blank=True, null=True)
    ex_studente_profilo_1 = models.TextField(
        db_column="EX_STUDENTE_PROFILO_1", blank=True, null=True
    )
    ex_studente_link_1 = models.TextField(
        db_column="EX_STUDENTE_LINK_1", blank=True, null=True
    )
    ex_studente_profilo_2 = models.TextField(
        db_column="EX_STUDENTE_PROFILO_2", blank=True, null=True
    )
    ex_studente_link_2 = models.TextField(
        db_column="EX_STUDENTE_LINK_2", blank=True, null=True
    )
    ex_studente_profilo_3 = models.TextField(
        db_column="EX_STUDENTE_PROFILO_3", blank=True, null=True
    )
    ex_studente_link_3 = models.TextField(
        db_column="EX_STUDENTE_LINK_3", blank=True, null=True
    )
    ex_studente_profilo_4 = models.TextField(
        db_column="EX_STUDENTE_PROFILO_4", blank=True, null=True
    )
    ex_studente_link_4 = models.TextField(
        db_column="EX_STUDENTE_LINK_4", blank=True, null=True
    )
    sito_web = models.CharField(
        db_column="SITO_WEB", max_length=2000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_DATI_EXCEL_TMP_OLD"


class SitoWebCdsExStudenti(models.Model):
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
    id_sito_web_cds_dati_base = models.ForeignKey(
        SitoWebCdsDatiBase,
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_DATI_BASE",
        to_field="id",
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="ID_USER_MOD",
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
        db_table = "SITO_WEB_CDS_EX_STUDENTI"


class SitoWebCdsLink(models.Model):
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
    id_sito_web_cds_dati_base = models.ForeignKey(
        SitoWebCdsDatiBase,
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_DATI_BASE",
        to_field="id",
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="ID_USER_MOD",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_LINK"


class SitoWebCdsSlider(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_sito_web_cds_dati_base = models.ForeignKey(
        SitoWebCdsDatiBase,
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_DATI_BASE",
        blank=True,
        null=True,
        to_field="id",
    )
    ordine = models.IntegerField(db_column="ORDINE", blank=True, null=True)
    slider_it = models.TextField(db_column="SLIDER_IT", blank=True, null=True)
    slider_en = models.TextField(db_column="SLIDER_EN", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="ID_USER_MOD",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_SLIDER"
