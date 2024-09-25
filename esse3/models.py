from django.db import models


class DidatticaAttivitaFormativaEsse3(models.Model):
    ad_id_esse3 = models.IntegerField(db_column="AD_ID_ESSE3", primary_key=True)
    ad_cod = models.CharField(db_column="AD_COD", max_length=10, blank=True, null=True)
    ad_des = models.CharField(db_column="AD_DES", max_length=255, blank=True, null=True)
    tipo_entita = models.IntegerField(db_column="TIPO_ENTITA", blank=True, null=True)
    peso = models.FloatField(db_column="PESO", blank=True, null=True)
    data_ins = models.DateTimeField(db_column="DATA_INS", blank=True, null=True)
    data_mod = models.DateTimeField(db_column="DATA_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_ATTIVITA_FORMATIVA_ESSE3"


class DidatticaCdsEsse3(models.Model):
    dip_id_esse3 = models.IntegerField(db_column="DIP_ID_ESSE3", blank=True, null=True)
    dip_cod = models.CharField(db_column="DIP_COD", max_length=6, blank=True, null=True)
    cds_id_esse3 = models.IntegerField(db_column="CDS_ID_ESSE3", primary_key=True)
    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=10, blank=True, null=True
    )
    nome_cds_it = models.CharField(
        db_column="NOME_CDS_IT", max_length=255, blank=True, null=True
    )
    rif_cod = models.CharField(
        db_column="RIF_COD", max_length=10, blank=True, null=True
    )
    rif_des = models.CharField(
        db_column="RIF_DES", max_length=255, blank=True, null=True
    )
    tipo_corso_cod = models.CharField(
        db_column="TIPO_CORSO_COD", max_length=10, blank=True, null=True
    )
    tipo_corso_des = models.CharField(
        db_column="TIPO_CORSO_DES", max_length=80, blank=True, null=True
    )
    durata_anni = models.IntegerField(db_column="DURATA_ANNI", blank=True, null=True)
    valore_min = models.IntegerField(db_column="VALORE_MIN", blank=True, null=True)
    tipo_titit_cod = models.CharField(
        db_column="TIPO_TITIT_COD", max_length=10, blank=True, null=True
    )
    tipo_titit_des = models.CharField(
        db_column="TIPO_TITIT_DES", max_length=255, blank=True, null=True
    )
    tipo_spec_cod = models.CharField(
        db_column="TIPO_SPEC_COD", max_length=10, blank=True, null=True
    )
    tipo_spec_des = models.CharField(
        db_column="TIPO_SPEC_DES", max_length=255, blank=True, null=True
    )
    istat_cod = models.CharField(
        db_column="ISTAT_COD", max_length=10, blank=True, null=True
    )
    max_punti = models.IntegerField(db_column="MAX_PUNTI", blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column="UM_PESO_COD", max_length=5, blank=True, null=True
    )
    um_peso_des = models.CharField(
        db_column="UM_PESO_DES", max_length=40, blank=True, null=True
    )
    aa_att_id = models.IntegerField(db_column="AA_ATT_ID", blank=True, null=True)
    aa_dis_id = models.IntegerField(db_column="AA_DIS_ID", blank=True, null=True)
    url = models.CharField(db_column="URL", max_length=2000, blank=True, null=True)
    cds_url_info_web = models.CharField(
        db_column="CDS_URL_INFO_WEB", max_length=2000, blank=True, null=True
    )
    cds_vis_web_flg = models.IntegerField(
        db_column="CDS_VIS_WEB_FLG", blank=True, null=True
    )
    cdsord_id_esse3 = models.IntegerField(
        db_column="CDSORD_ID_ESSE3", blank=True, null=True
    )
    cdsord_cod = models.CharField(
        db_column="CDSORD_COD", max_length=10, blank=True, null=True
    )
    aa_ord_id = models.IntegerField(db_column="AA_ORD_ID", blank=True, null=True)
    cdsord_des = models.CharField(
        db_column="CDSORD_DES", max_length=255, blank=True, null=True
    )
    stato_cdsord_cod = models.CharField(
        db_column="STATO_CDSORD_COD", max_length=5, blank=True, null=True
    )
    dt_ins = models.DateTimeField(db_column="DT_INS", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_ESSE3"
