from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from generics.models import InsModAbstract, Permissions
from generics.validators import validate_file_size, validate_pdf_file_extension
from regdid.settings import (
    OFFICE_REGDIDS_APPROVAL,
    OFFICE_REGDIDS_DEPARTMENT,
    OFFICE_REGDIDS_REVISION,
)

from cds.settings import (
    cds_manifesto_media_path,
    cds_ordinamento_media_path,
    cds_regolamento_media_path,
)


class DidatticaCdsCollegamento(models.Model):
    cds = models.OneToOneField(
        "DidatticaCds",
        models.CASCADE,
        db_column="ID_DIDATTICA_CDS",
        to_field="cds_id",
        related_name="cds_collegamento",
        primary_key=True,
    )

    cds_prec = models.OneToOneField(
        "DidatticaCds",
        models.CASCADE,
        db_column="ID_DIDATTICA_CDS_PREC",
        to_field="cds_id",
        related_name="cds_collegamento_prec",
        unique=True,
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_COLLEGAMENTO"
        ordering = ["-cds__cds_cod"]
        unique_together = (("cds", "cds_prec"),)
        verbose_name = "Cds Morph"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.cds.cds_cod}-{self.cds_prec.cds_cod}"


class DidatticaSsd(models.Model):
    ssd_id = models.CharField(db_column="SSD_ID", primary_key=True, max_length=100)
    ssd_des = models.CharField(db_column="SSD_DES", max_length=2000)

    class Meta:
        managed = True
        db_table = "DIDATTICA_SSD"
        verbose_name = "SSD"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.ssd_id} {self.ssd_des}"


class DidatticaAttivitaFormativa(models.Model):
    af_id = models.IntegerField(db_column="AF_ID", primary_key=True)
    cds = models.ForeignKey(
        "DidatticaCds", models.DO_NOTHING, db_column="CDS_ID", blank=True, null=True
    )
    cdsord_id = models.IntegerField(db_column="CDSORD_ID", blank=True, null=True)
    cdsord_cod = models.CharField(
        db_column="CDSORD_COD", max_length=10, blank=True, null=True
    )
    aa_ord_id = models.IntegerField(db_column="AA_ORD_ID", blank=True, null=True)
    stato_cdsord_cod = models.CharField(
        db_column="STATO_CDSORD_COD", max_length=5, blank=True, null=True
    )
    regdid = models.ForeignKey(
        "DidatticaRegolamento",
        models.DO_NOTHING,
        db_column="REGDID_ID",
        blank=True,
        null=True,
    )
    regdid_cod = models.CharField(
        db_column="REGDID_COD", max_length=10, blank=True, null=True
    )
    aa_regdid_id = models.IntegerField(db_column="AA_REGDID_ID", blank=True, null=True)
    stato_regdid_cod = models.CharField(
        db_column="STATO_REGDID_COD", max_length=5, blank=True, null=True
    )
    stato_appr_regdid_cod = models.CharField(
        db_column="STATO_APPR_REGDID_COD", max_length=5, blank=True, null=True
    )
    pds_regdid = models.ForeignKey(
        "DidatticaPdsRegolamento",
        models.DO_NOTHING,
        db_column="PDS_REGDID_ID",
        blank=True,
        null=True,
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=10, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )
    comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    attinenza_cod = models.CharField(
        db_column="ATTINENZA_COD", max_length=10, blank=True, null=True
    )
    of_id = models.IntegerField(db_column="OF_ID", blank=True, null=True)
    aa_off_id = models.IntegerField(db_column="AA_OFF_ID", blank=True, null=True)
    stato_of_cod = models.CharField(
        db_column="STATO_OF_COD", max_length=5, blank=True, null=True
    )
    tipo_comp_af_id = models.IntegerField(
        db_column="TIPO_COMP_AF_ID", blank=True, null=True
    )
    tipo_comp_af_cod = models.CharField(
        db_column="TIPO_COMP_AF_COD", max_length=10, blank=True, null=True
    )
    des_tipo_comp_af = models.CharField(
        db_column="DES_TIPO_COMP_AF", max_length=255, blank=True, null=True
    )
    af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    af_gen_cod = models.CharField(
        db_column="AF_GEN_COD", max_length=20, blank=True, null=True
    )
    des = models.CharField(db_column="DES", max_length=255, blank=True, null=True)
    af_gen_des_eng = models.CharField(
        db_column="AF_GEN_DES_ENG", max_length=255, blank=True, null=True
    )
    anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    lista_anni_corso = models.CharField(
        db_column="LISTA_ANNI_CORSO", max_length=20, blank=True, null=True
    )
    af_regdid_id = models.IntegerField(db_column="AF_REGDID_ID", blank=True, null=True)
    sett_cod = models.CharField(
        db_column="SETT_COD", max_length=12, blank=True, null=True
    )
    sett_des = models.CharField(
        db_column="SETT_DES", max_length=150, blank=True, null=True
    )
    tipo_af_cod = models.CharField(
        db_column="TIPO_AF_COD", max_length=10, blank=True, null=True
    )
    tipo_af_des = models.CharField(
        db_column="TIPO_AF_DES", max_length=80, blank=True, null=True
    )
    tipo_af_intercla_cod = models.CharField(
        db_column="TIPO_AF_INTERCLA_COD", max_length=40, blank=True, null=True
    )
    tipo_af_intercla_des = models.CharField(
        db_column="TIPO_AF_INTERCLA_DES", max_length=200, blank=True, null=True
    )
    amb_id = models.IntegerField(db_column="AMB_ID", blank=True, null=True)
    ambito_des = models.CharField(
        db_column="AMBITO_DES", max_length=255, blank=True, null=True
    )
    peso = models.IntegerField(db_column="PESO", blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column="UM_PESO_COD", max_length=5, blank=True, null=True
    )
    um_peso_des = models.CharField(
        db_column="UM_PESO_DES", max_length=40, blank=True, null=True
    )
    freq_obblig_flg = models.IntegerField(
        db_column="FREQ_OBBLIG_FLG", blank=True, null=True
    )
    ore_min_freq = models.IntegerField(db_column="ORE_MIN_FREQ", blank=True, null=True)
    ore_att_front = models.IntegerField(
        db_column="ORE_ATT_FRONT", blank=True, null=True
    )
    num_max_reit = models.IntegerField(db_column="NUM_MAX_REIT", blank=True, null=True)
    libera_flg = models.IntegerField(db_column="LIBERA_FLG", blank=True, null=True)
    scelta_mod_flg = models.IntegerField(
        db_column="SCELTA_MOD_FLG", blank=True, null=True
    )
    tipo_esa_cod = models.CharField(
        db_column="TIPO_ESA_COD", max_length=5, blank=True, null=True
    )
    tipo_esa_des = models.CharField(
        db_column="TIPO_ESA_DES", max_length=40, blank=True, null=True
    )
    tipo_val_cod = models.CharField(
        db_column="TIPO_VAL_COD", max_length=5, blank=True, null=True
    )
    tipo_val_des = models.CharField(
        db_column="TIPO_VAL_DES", max_length=40, blank=True, null=True
    )
    tipo_ins_cod = models.CharField(
        db_column="TIPO_INS_COD", max_length=10, blank=True, null=True
    )
    tipo_ins_des = models.CharField(
        db_column="TIPO_INS_DES", max_length=40, blank=True, null=True
    )
    serale_flg = models.IntegerField(db_column="SERALE_FLG", blank=True, null=True)
    no_media_flg = models.IntegerField(db_column="NO_MEDIA_FLG", blank=True, null=True)
    sostegno_flg = models.IntegerField(db_column="SOSTEGNO_FLG", blank=True, null=True)
    nota = models.CharField(db_column="NOTA", max_length=2000, blank=True, null=True)
    af_pdr_id = models.IntegerField(db_column="AF_PDR_ID", blank=True, null=True)
    af_radice_id = models.IntegerField(db_column="AF_RADICE_ID", blank=True, null=True)
    num_liv_albero = models.IntegerField(
        db_column="NUM_LIV_ALBERO", blank=True, null=True
    )
    ciclo_des = models.CharField(
        db_column="CICLO_DES", max_length=40, blank=True, null=True
    )
    data_inizio = models.DateTimeField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateTimeField(db_column="DATA_FINE", blank=True, null=True)
    tipo_ciclo_cod = models.CharField(
        db_column="TIPO_CICLO_COD", max_length=5, blank=True, null=True
    )
    des_tipo_ciclo = models.CharField(
        db_column="DES_TIPO_CICLO", max_length=40, blank=True, null=True
    )
    matricola_resp_did = models.ForeignKey(
        "addressbook.Personale",
        models.DO_NOTHING,
        db_column="MATRICOLA_RESP_DID",
        blank=True,
        null=True,
        to_field="matricola",
    )
    cod_fis_resp_did = models.CharField(
        db_column="COD_FIS_RESP_DID", max_length=16, blank=True, null=True
    )
    ruolo_resp_did_cod = models.CharField(
        db_column="RUOLO_RESP_DID_COD", max_length=4, blank=True, null=True
    )
    url_sito_web = models.URLField(
        db_column="URL_SITO_WEB", max_length=2000, blank=True, null=True
    )
    lista_lin_did_af = models.CharField(
        db_column="LISTA_LIN_DID_AF", max_length=2000, blank=True, null=True
    )
    lista_mod_did_af = models.CharField(
        db_column="LISTA_MOD_DID_AF", max_length=2000, blank=True, null=True
    )
    lista_taf_set_cfu = models.CharField(
        db_column="LISTA_TAF_SET_CFU", max_length=2000, blank=True, null=True
    )
    mutuata_flg = models.IntegerField(db_column="MUTUATA_FLG", blank=True, null=True)
    af_master_id = models.IntegerField(db_column="AF_MASTER_ID", blank=True, null=True)
    num_af_figlie = models.IntegerField(
        db_column="NUM_AF_FIGLIE", blank=True, null=True
    )
    num_af_foglie = models.IntegerField(
        db_column="NUM_AF_FOGLIE", blank=True, null=True
    )
    non_erogabile_flg = models.PositiveIntegerField(
        db_column="NON_EROGABILE_FLG", blank=True, null=True
    )
    fat_part_stu_cod = models.CharField(
        db_column="FAT_PART_STU_COD", max_length=40, blank=True, null=True
    )
    fat_part_stu_des = models.CharField(
        db_column="FAT_PART_STU_DES", max_length=500, blank=True, null=True
    )
    part_stu_id = models.IntegerField(db_column="PART_STU_ID", blank=True, null=True)
    part_stu_cod = models.CharField(
        db_column="PART_STU_COD", max_length=100, blank=True, null=True
    )
    part_stu_des = models.CharField(
        db_column="PART_STU_DES", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_ATTIVITA_FORMATIVA"
        verbose_name = "Study activity"
        verbose_name_plural = "Study activities"
        ordering = ("ciclo_des",)

    def __str__(self):  # pragma: no cover
        return "{}".format(self.af_id)

    def checkIfMainCourse(self):
        return self.af_id == self.af_radice_id


class DidatticaAttivitaFormativaModalita(models.Model):
    mod_did_af_id = models.IntegerField(db_column="MOD_DID_AF_ID", primary_key=True)
    af = models.ForeignKey(
        DidatticaAttivitaFormativa, models.DO_NOTHING, db_column="AF_ID"
    )
    mod_did_cod = models.CharField(db_column="MOD_DID_COD", max_length=40)
    mod_did_des = models.CharField(db_column="MOD_DID_DES", max_length=1000)

    class Meta:
        managed = True
        db_table = "DIDATTICA_ATTIVITA_FORMATIVA_MODALITA"
        verbose_name = "Study activity mode"
        verbose_name_plural = "Study activity modes"


class DidatticaCds(InsModAbstract):
    cds_id = models.IntegerField(db_column="CDS_ID", primary_key=True)
    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=10, blank=True, null=True
    )
    nome_cds_it = models.CharField(
        db_column="NOME_CDS_IT", max_length=255, blank=True, null=True
    )
    nome_cds_eng = models.CharField(
        db_column="NOME_CDS_ENG", max_length=255, blank=True, null=True
    )

    rif_cod = models.CharField(
        db_column="RIF_COD", max_length=10, blank=True, null=True
    )

    rif_des = models.CharField(
        db_column="RIF_DES", max_length=40, blank=True, null=True
    )
    dip = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="DIP_ID",
        blank=True,
        null=True,
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
    min_cfu_comuni = models.IntegerField(
        db_column="MIN_CFU_COMUNI", blank=True, null=True
    )
    cfu_max_rico = models.IntegerField(db_column="CFU_MAX_RICO", blank=True, null=True)
    num_max_esami = models.IntegerField(
        db_column="NUM_MAX_ESAMI", blank=True, null=True
    )
    perc_min_ore_stu_ind = models.FloatField(
        db_column="PERC_MIN_ORE_STU_IND", blank=True, null=True
    )
    perc_max_ore_stu_ind = models.FloatField(
        db_column="PERC_MAX_ORE_STU_IND", blank=True, null=True
    )
    tipo_spec_cod = models.CharField(
        db_column="TIPO_SPEC_COD", max_length=10, blank=True, null=True
    )
    tipo_spec_des = models.CharField(
        db_column="TIPO_SPEC_DES", max_length=255, blank=True, null=True
    )
    scuola_spec_id = models.IntegerField(
        db_column="SCUOLA_SPEC_ID", blank=True, null=True
    )
    scuola_spec_des = models.CharField(
        db_column="SCUOLA_SPEC_DES", max_length=255, blank=True, null=True
    )
    cla_m_id = models.IntegerField(db_column="CLA_M_ID", blank=True, null=True)
    cla_miur_cod = models.CharField(
        db_column="CLA_MIUR_COD", max_length=20, blank=True, null=True
    )
    cla_miur_des = models.CharField(
        db_column="CLA_MIUR_DES", max_length=255, blank=True, null=True
    )
    intercla_m_id = models.IntegerField(
        db_column="INTERCLA_M_ID", blank=True, null=True
    )
    intercla_miur_cod = models.CharField(
        db_column="INTERCLA_MIUR_COD", max_length=20, blank=True, null=True
    )
    intercla_miur_des = models.CharField(
        db_column="INTERCLA_MIUR_DES", max_length=255, blank=True, null=True
    )
    codicione = models.CharField(
        db_column="CODICIONE", max_length=255, blank=True, null=True
    )
    min_diff_cfu_ord = models.IntegerField(
        db_column="MIN_DIFF_CFU_ORD", blank=True, null=True
    )
    sett_post_rif_flg = models.IntegerField(
        db_column="SETT_POST_RIF_FLG", blank=True, null=True
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
    data_attivazione = models.DateTimeField(
        db_column="DATA_ATTIVAZIONE", blank=True, null=True
    )
    aa_dis_id = models.IntegerField(db_column="AA_DIS_ID", blank=True, null=True)
    url = models.URLField(db_column="URL", max_length=255, blank=True, null=True)
    cds_url_info_web = models.URLField(
        db_column="CDS_URL_INFO_WEB", max_length=255, blank=True, null=True
    )
    cds_vis_web_flg = models.IntegerField(
        db_column="CDS_VIS_WEB_FLG", blank=True, null=True
    )
    ccs_id = models.IntegerField(db_column="CCS_ID", blank=True, null=True)
    ccs_cod = models.CharField(
        db_column="CCS_COD", max_length=10, blank=True, null=True
    )
    ccs_des = models.CharField(
        db_column="CCS_DES", max_length=255, blank=True, null=True
    )
    flg_exp_seg_stu = models.IntegerField(
        db_column="FLG_EXP_SEG_STU", blank=True, null=True
    )
    data_exp_seg_stu = models.DateTimeField(
        db_column="DATA_EXP_SEG_STU", blank=True, null=True
    )
    cdsord_id = models.IntegerField(
        db_column="CDSORD_ID", unique=True, blank=True, null=True
    )
    cdsord_cod = models.CharField(
        db_column="CDSORD_COD", max_length=10, blank=True, null=True
    )
    aa_ord_id = models.IntegerField(db_column="AA_ORD_ID", blank=True, null=True)
    stato_cdsord_cod = models.CharField(
        db_column="STATO_CDSORD_COD", max_length=5, blank=True, null=True
    )
    area_cds = models.CharField(
        db_column="AREA_CDS", max_length=1000, blank=True, null=True
    )
    area_cds_en = models.CharField(
        db_column="AREA_CDS_EN", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS"
        verbose_name = "Cds"
        verbose_name_plural = verbose_name

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cds_cod, self.nome_cds_it)


class DidatticaCdsPeriodi(models.Model):
    ciclo_id = models.IntegerField(db_column="CICLO_ID", primary_key=True)
    aa_id = models.IntegerField(db_column="AA_ID")
    cds_id = models.IntegerField(db_column="CDS_ID")
    cds_cod = models.CharField(db_column="CDS_COD", max_length=10)
    rag_tipi_ciclo_cod = models.CharField(db_column="RAG_TIPI_CICLO_COD", max_length=5)
    rag_tipi_ciclo_des = models.CharField(
        db_column="RAG_TIPI_CICLO_DES", max_length=40, blank=True, null=True
    )
    tipo_ciclo_cod = models.CharField(db_column="TIPO_CICLO_COD", max_length=5)
    tipo_ciclo_des = models.CharField(db_column="TIPO_CICLO_DES", max_length=40)
    tipo_ciclo_des_eng = models.CharField(
        db_column="TIPO_CICLO_DES_ENG", max_length=4000, blank=True, null=True
    )
    org_did_sua_cod = models.IntegerField(
        db_column="ORG_DID_SUA_COD", blank=True, null=True
    )
    ciclo_des = models.CharField(db_column="CICLO_DES", max_length=40)
    data_inizio = models.DateField(db_column="DATA_INIZIO")
    data_fine = models.DateField(db_column="DATA_FINE")
    durata = models.DecimalField(
        db_column="DURATA", max_digits=6, decimal_places=2, blank=True, null=True
    )
    csa_cod = models.CharField(db_column="CSA_COD", max_length=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_PERIODI"
        verbose_name = "Study course period"
        verbose_name_plural = "Study course periods"


class DidatticaCdsAltriDatiUfficio(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    cds = models.ForeignKey(
        DidatticaCds, models.DO_NOTHING, db_column="ID_DIDATTICA_CDS"
    )
    ordine = models.IntegerField(db_column="ORDINE")
    nome_ufficio = models.CharField(
        db_column="NOME_UFFICIO", max_length=1000, blank=True, null=True
    )
    matricola_riferimento = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA_RIFERIMENTO",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_origine_riferimento = models.CharField(
        db_column="NOME_ORIGINE_RIFERIMENTO", max_length=1000, blank=True, null=True
    )
    telefono = models.CharField(
        db_column="TELEFONO", max_length=1000, blank=True, null=True
    )
    email = models.CharField(db_column="EMAIL", max_length=1000, blank=True, null=True)
    edificio = models.CharField(
        db_column="EDIFICIO", max_length=1000, blank=True, null=True
    )
    piano = models.CharField(db_column="PIANO", max_length=1000, blank=True, null=True)
    orari = models.CharField(db_column="ORARI", max_length=1000, blank=True, null=True)
    sportello_online = models.CharField(
        db_column="SPORTELLO_ONLINE", max_length=2000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_ALTRI_DATI_UFFICIO"
        ordering = ("ordine",)
        # unique_together = (('cds', 'ordine'),)
        verbose_name = "Cds office other data"
        verbose_name_plural = verbose_name


class DidatticaCdsLingua(models.Model):
    lin_did_ord_id = models.IntegerField(db_column="LIN_DID_ORD_ID", primary_key=True)
    cdsord = models.ForeignKey(
        DidatticaCds,
        models.DO_NOTHING,
        db_column="CDSORD_ID",
        blank=True,
        null=True,
        to_field="cdsord_id",
        related_name="didatticacdslingua",
    )
    lingua_id = models.IntegerField(db_column="LINGUA_ID", blank=True, null=True)
    lingua_des_it = models.CharField(
        db_column="LINGUA_DES_IT", max_length=100, blank=True, null=True
    )
    iso6392_cod = models.CharField(
        db_column="ISO6392_COD", max_length=3, blank=True, null=True
    )
    lingua_des_eng = models.CharField(
        db_column="LINGUA_DES_ENG", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_LINGUA"
        verbose_name = "Cds language"
        verbose_name_plural = "Cds languages"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cdsord.cds_cod, self.lingua_des_it)


class DidatticaCopertura(InsModAbstract):
    coper_id = models.IntegerField(db_column="COPER_ID", primary_key=True)

    af = models.ForeignKey(
        DidatticaAttivitaFormativa,
        models.DO_NOTHING,
        db_column="AF_ID",
        blank=True,
        null=True,
    )
    personale = models.ForeignKey(
        "addressbook.Personale",
        models.DO_NOTHING,
        db_column="PERSONALE_ID",
        blank=True,
        null=True,
    )
    af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    af_gen_cod = models.CharField(
        db_column="AF_GEN_COD", max_length=40, blank=True, null=True
    )
    af_gen_des = models.CharField(
        db_column="AF_GEN_DES", max_length=500, blank=True, null=True
    )
    aa_off_id = models.IntegerField(db_column="AA_OFF_ID", blank=True, null=True)
    cds_id = models.IntegerField(db_column="CDS_ID", blank=True, null=True)
    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=40, blank=True, null=True
    )
    cdsord_id = models.IntegerField(db_column="CDSORD_ID", blank=True, null=True)
    cdsord_cod = models.CharField(
        db_column="CDSORD_COD", max_length=40, blank=True, null=True
    )
    aa_ord_id = models.IntegerField(db_column="AA_ORD_ID", blank=True, null=True)
    regdid_id = models.IntegerField(db_column="REGDID_ID", blank=True, null=True)
    regdid_cod = models.CharField(
        db_column="REGDID_COD", max_length=40, blank=True, null=True
    )
    aa_regdid_id = models.IntegerField(db_column="AA_REGDID_ID", blank=True, null=True)
    pds_regdid_id = models.IntegerField(
        db_column="PDS_REGDID_ID", blank=True, null=True
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=40, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=500, blank=True, null=True
    )
    of_id = models.IntegerField(db_column="OF_ID", blank=True, null=True)
    stato_of_cod = models.CharField(
        db_column="STATO_OF_COD", max_length=20, blank=True, null=True
    )
    tipo_comp_af_cod = models.CharField(
        db_column="TIPO_COMP_AF_COD", max_length=40, blank=True, null=True
    )
    af_gen_des_eng = models.CharField(
        db_column="AF_GEN_DES_ENG", max_length=500, blank=True, null=True
    )
    anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    sett_cod = models.CharField(
        db_column="SETT_COD", max_length=40, blank=True, null=True
    )
    sett_des = models.CharField(
        db_column="SETT_DES", max_length=400, blank=True, null=True
    )
    tipo_af_cod = models.CharField(
        db_column="TIPO_AF_COD", max_length=40, blank=True, null=True
    )
    tipo_af_des = models.CharField(
        db_column="TIPO_AF_DES", max_length=400, blank=True, null=True
    )
    amb_id = models.IntegerField(db_column="AMB_ID", blank=True, null=True)
    ambito_des = models.CharField(
        db_column="AMBITO_DES", max_length=500, blank=True, null=True
    )
    peso = models.IntegerField(db_column="PESO", blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column="UM_PESO_COD", max_length=20, blank=True, null=True
    )
    ore_att_front = models.IntegerField(
        db_column="ORE_ATT_FRONT", blank=True, null=True
    )
    tipo_ins_cod = models.CharField(
        db_column="TIPO_INS_COD", max_length=40, blank=True, null=True
    )
    nota = models.TextField(db_column="NOTA", blank=True, null=True)
    af_radice_id = models.IntegerField(db_column="AF_RADICE_ID", blank=True, null=True)
    ciclo_des = models.CharField(
        db_column="CICLO_DES", max_length=400, blank=True, null=True
    )
    tipo_ciclo_cod = models.CharField(
        db_column="TIPO_CICLO_COD", max_length=40, blank=True, null=True
    )
    des_tipo_ciclo = models.CharField(
        db_column="DES_TIPO_CICLO", max_length=400, blank=True, null=True
    )
    matricola_resp_did = models.CharField(
        db_column="MATRICOLA_RESP_DID", max_length=20, blank=True, null=True
    )
    cod_fis_resp_did = models.CharField(
        db_column="COD_FIS_RESP_DID", max_length=16, blank=True, null=True
    )
    ruolo_resp_did_cod = models.CharField(
        db_column="RUOLO_RESP_DID_COD", max_length=40, blank=True, null=True
    )
    cognome_titolare = models.CharField(
        db_column="COGNOME_TITOLARE", max_length=200, blank=True, null=True
    )
    nome_titolare = models.CharField(
        db_column="NOME_TITOLARE", max_length=200, blank=True, null=True
    )
    matricola_titolare = models.CharField(
        db_column="MATRICOLA_TITOLARE", max_length=20, blank=True, null=True
    )
    fat_part_stu_cod = models.CharField(
        db_column="FAT_PART_STU_COD", max_length=40, blank=True, null=True
    )
    fat_part_stu_des = models.CharField(
        db_column="FAT_PART_STU_DES", max_length=400, blank=True, null=True
    )
    part_stu_cod = models.CharField(
        db_column="PART_STU_COD", max_length=40, blank=True, null=True
    )
    part_stu_des = models.CharField(
        db_column="PART_STU_DES", max_length=400, blank=True, null=True
    )
    tipo_fat_stu_cod = models.CharField(
        db_column="TIPO_FAT_STU_COD", max_length=20, blank=True, null=True
    )
    part_ini = models.CharField(
        db_column="PART_INI", max_length=100, blank=True, null=True
    )
    part_fine = models.CharField(
        db_column="PART_FINE", max_length=100, blank=True, null=True
    )
    non_erogabile_flg = models.IntegerField(
        db_column="NON_EROGABILE_FLG", blank=True, null=True
    )
    dt_ins = models.DateTimeField(db_column="DT_INS", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    cds_des = models.CharField(
        db_column="CDS_DES", max_length=500, blank=True, null=True
    )
    coper_peso = models.FloatField(db_column="COPER_PESO", blank=True, null=True)
    ore = models.PositiveIntegerField(db_column="ORE", blank=True, null=True)
    stato_coper_cod = models.CharField(
        db_column="STATO_COPER_COD", max_length=10, blank=True, null=True
    )
    stato_coper_des = models.CharField(
        db_column="STATO_COPER_DES", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_COPERTURA"
        verbose_name = "Teaching coverage"
        verbose_name_plural = "Teaching coverages"


class DidatticaCoperturaDettaglioOre(models.Model):
    ore_coper_det_id = models.IntegerField(
        db_column="ORE_COPER_DET_ID", primary_key=True
    )
    coper = models.ForeignKey(
        DidatticaCopertura, models.DO_NOTHING, db_column="COPER_ID"
    )
    tipo_att_did_cod = models.CharField(db_column="TIPO_ATT_DID_COD", max_length=10)
    ore = models.DecimalField(db_column="ORE", max_digits=6, decimal_places=2)
    dt_ins = models.DateField(db_column="DT_INS", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_COPERTURA_DETTAGLIO_ORE"
        verbose_name = "Teaching coverage hours detail"
        verbose_name_plural = "Teaching coverage hours details"


class DidatticaPdsRegolamento(InsModAbstract):
    pds_regdid_id = models.IntegerField(db_column="PDS_REGDID_ID", primary_key=True)
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=30, blank=True, null=True
    )
    pds_des_it = models.CharField(
        db_column="PDS_DES_IT", max_length=255, blank=True, null=True
    )
    pds_des_eng = models.CharField(
        db_column="PDS_DES_ENG", max_length=2000, blank=True, null=True
    )
    comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    valore_min = models.IntegerField(db_column="VALORE_MIN", blank=True, null=True)
    regdid = models.ForeignKey(
        "DidatticaRegolamento",
        models.DO_NOTHING,
        db_column="REGDID_ID",
        blank=True,
        null=True,
    )
    # aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')

    class Meta:
        managed = True
        db_table = "DIDATTICA_PDS_REGOLAMENTO"
        verbose_name = "Academic pathway"
        verbose_name_plural = "Academic pathways"


class DidatticaRegolamento(InsModAbstract):
    regdid_id = models.IntegerField(db_column="REGDID_ID", primary_key=True)
    aa_reg_did = models.IntegerField(db_column="AA_REG_DID", blank=True, null=True)
    cds = models.ForeignKey(
        DidatticaCds, models.DO_NOTHING, db_column="CDS_ID", blank=True, null=True
    )
    stato_regdid_cod = models.CharField(
        db_column="STATO_REGDID_COD", max_length=5, blank=True, null=True
    )
    stato_regdid_des = models.CharField(
        db_column="STATO_REGDID_DES", max_length=40, blank=True, null=True
    )
    numero_piani_studio = models.IntegerField(
        db_column="NUMERO_PIANI_STUDIO", blank=True, null=True
    )
    anno_scelta_pds = models.IntegerField(
        db_column="ANNO_SCELTA_PDS", blank=True, null=True
    )
    modalita_erogazione = models.CharField(
        db_column="MODALITA_EROGAZIONE", max_length=100, blank=True, null=True
    )
    frequenza_obbligatoria = models.IntegerField(
        db_column="FREQUENZA_OBBLIGATORIA", blank=True, null=True
    )
    titolo_congiunto_cod = models.CharField(
        db_column="TITOLO_CONGIUNTO_COD", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_REGOLAMENTO"

        verbose_name = "Didactic regulation"
        verbose_name_plural = "Didactic regulations"

    def get_ordinamento_didattico(self):
        # se è stato caricato un ordinamento per quest'anno, lo restituisco
        other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=self).first()
        if other_data and other_data.ordinamento_didattico:
            return (self.aa_reg_did, other_data.ordinamento_didattico)

        prev_regdid = DidatticaRegolamento.objects.filter(
            cds=self.cds, aa_reg_did=self.aa_reg_did - 1
        ).first()
        if not prev_regdid:
            return None
        return prev_regdid.get_ordinamento_didattico()

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.regdid_id, self.aa_reg_did)


class DidatticaRegolamentoTipologiaAltriDati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_testo_regdid_cod = models.CharField(
        db_column="TIPO_TESTO_REGDID_COD", unique=True, max_length=100
    )
    tipo_testo_regdid_des = models.CharField(
        db_column="TIPO_TESTO_REGDID_DES", max_length=2000
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
        db_table = "DIDATTICA_REGOLAMENTO_TIPOLOGIA_ALTRI_DATI"
        verbose_name = "Didactic regulation other data type"
        verbose_name_plural = "Didactic regulation other data types"


class DidatticaRegolamentoAltriDati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    regdid = models.ForeignKey(
        DidatticaRegolamento, models.CASCADE, db_column="ID_DIDATTICA_REGOLAMENTO"
    )
    tipo_testo_regdid_cod = models.ForeignKey(
        DidatticaRegolamentoTipologiaAltriDati,
        models.PROTECT,
        db_column="ID_DIDATTICA_REGOLAMENTO_TIPOLOGIA_ALTRI_DATI",
        to_field="tipo_testo_regdid_cod",
    )
    clob_txt_ita = models.TextField(db_column="CLOB_TXT_ITA", blank=True, null=True)
    clob_txt_eng = models.TextField(db_column="CLOB_TXT_ENG", blank=True, null=True)
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
        db_table = "DIDATTICA_REGOLAMENTO_ALTRI_DATI"
        verbose_name = "Didactic regulation other data"
        verbose_name_plural = "Didactic regulation other data"


class DidatticaTestiAf(InsModAbstract):
    af = models.OneToOneField(
        DidatticaAttivitaFormativa,
        models.DO_NOTHING,
        db_column="AF_ID",
        primary_key=True,
        related_name="didatticaf",
    )
    aa_off_id = models.IntegerField(db_column="AA_OFF_ID", blank=True, null=True)
    testi_af_id = models.IntegerField(db_column="TESTI_AF_ID", blank=True, null=True)
    tipo_testo_af_cod = models.CharField(db_column="TIPO_TESTO_AF_COD", max_length=100)
    tipo_testo_af_des = models.TextField(
        db_column="TIPO_TESTO_AF_DES", blank=True, null=True
    )
    tipo_testo_af_etic = models.CharField(
        db_column="TIPO_TESTO_AF_ETIC", max_length=255, blank=True, null=True
    )
    tipo_testo_af_etic_eng = models.TextField(
        db_column="TIPO_TESTO_AF_ETIC_ENG", blank=True, null=True
    )
    obbl_flg = models.IntegerField(db_column="OBBL_FLG", blank=True, null=True)
    testo_af_ita = models.TextField(db_column="TESTO_AF_ITA", blank=True, null=True)
    testo_af_short_ita = models.TextField(
        db_column="TESTO_AF_SHORT_ITA", blank=True, null=True
    )
    testo_af_fmt_ita = models.TextField(
        db_column="TESTO_AF_FMT_ITA", blank=True, null=True
    )
    dt_ins_txt_clob_ita = models.DateTimeField(
        db_column="DT_INS_TXT_CLOB_ITA", blank=True, null=True
    )
    dt_mod_txt_clob_ita = models.DateTimeField(
        db_column="DT_MOD_TXT_CLOB_ITA", blank=True, null=True
    )
    testo_af_eng = models.TextField(db_column="TESTO_AF_ENG", blank=True, null=True)
    testo_af_short_eng = models.TextField(
        db_column="TESTO_AF_SHORT_ENG", blank=True, null=True
    )
    dt_ins_txt_clob_eng = models.TextField(
        db_column="DT_INS_TXT_CLOB_ENG", blank=True, null=True
    )
    dt_mod_txt_clob_eng = models.DateTimeField(
        db_column="DT_MOD_TXT_CLOB_ENG", blank=True, null=True
    )
    dt_ins_mod_max = models.DateTimeField(
        db_column="DT_INS_MOD_MAX", blank=True, null=True
    )
    testo_af_fmt_eng = models.TextField(
        db_column="TESTO_AF_FMT_ENG", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_TESTI_AF"
        unique_together = (("af", "tipo_testo_af_cod"),)
        verbose_name = "Study activity text"
        verbose_name_plural = "Study activity texts"


class DidatticaTestiRegolamento(InsModAbstract):
    txt_id = models.IntegerField(db_column="TXT_ID", primary_key=True)
    regdid = models.ForeignKey(
        DidatticaRegolamento, models.DO_NOTHING, db_column="REGDID_ID"
    )
    tipo_testo_regdid_cod = models.CharField(
        db_column="TIPO_TESTO_REGDID_COD", max_length=100
    )
    tipo_testo_regdid_des = models.CharField(
        db_column="TIPO_TESTO_REGDID_DES", max_length=255, blank=True, null=True
    )
    clob_txt_ita = models.TextField(db_column="CLOB_TXT_ITA", blank=True, null=True)

    clob_txt_eng = models.TextField(db_column="CLOB_TXT_ENG", blank=True, null=True)

    testo_regdid_url = models.URLField(
        db_column="TESTO_REGDID_URL", max_length=1024, blank=True, null=True
    )
    profilo = models.TextField(db_column="PROFILO", blank=True, null=True)
    profilo_eng = models.TextField(db_column="PROFILO_ENG", blank=True, null=True)
    dt_ins_txt_clob_ita = models.DateTimeField(
        db_column="DT_INS_TXT_CLOB_ITA", blank=True, null=True
    )
    dt_ins_txt_clob_eng = models.DateTimeField(
        db_column="DT_INS_TXT_CLOB_ENG", blank=True, null=True
    )
    dt_mod_txt_clob_ita = models.DateTimeField(
        db_column="DT_MOD_TXT_CLOB_ITA", blank=True, null=True
    )
    dt_mod_txt_clob_eng = models.DateTimeField(
        db_column="DT_MOD_TXT_CLOB_ENG", blank=True, null=True
    )
    dt_ins = models.DateTimeField(db_column="DT_INS", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_TESTI_REGOLAMENTO"
        verbose_name = "Didactic regulation text"
        verbose_name_plural = "Didactic regulation texts"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.txt_id, self.tipo_testo_regdid_cod)


class DidatticaCdsAltriDati(models.Model):
    regdid = models.OneToOneField(
        DidatticaRegolamento,
        models.DO_NOTHING,
        db_column="ID_DIDATTICA_REGOLAMENTO",
        primary_key=True,
    )
    matricola_coordinatore = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        related_name="coordinatore",
        db_column="ID_PERSONALE_MATRICOLA_COORDINATORE",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_origine_coordinatore = models.CharField(
        db_column="NOME_ORIGINE_COORDINATORE", max_length=1000, blank=True, null=True
    )
    matricola_vice_coordinatore = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        related_name="vice_coordinatore",
        db_column="ID_PERSONALE_MATRICOLA_VICE_COORDINATORE",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_origine_vice_coordinatore = models.CharField(
        db_column="NOME_ORIGINE_VICE_COORDINATORE",
        max_length=1000,
        blank=True,
        null=True,
    )
    # num_posti = models.IntegerField(db_column='NUM_POSTI', blank=True, null=True)
    # modalita_iscrizione = models.TextField(db_column='MODALITA_ISCRIZIONE', blank=True, null=True)
    manifesto_studi = models.FileField(
        upload_to=cds_manifesto_media_path,
        validators=[validate_pdf_file_extension, validate_file_size],
        db_column="MANIFESTO_STUDI",
        max_length=255,
        blank=True,
        null=True,
    )
    regolamento_didattico = models.FileField(
        upload_to=cds_regolamento_media_path,
        validators=[validate_pdf_file_extension, validate_file_size],
        db_column="REGOLAMENTO_DIDATTICO",
        max_length=255,
        blank=True,
        null=True,
    )
    ordinamento_didattico = models.FileField(
        upload_to=cds_ordinamento_media_path,
        validators=[validate_pdf_file_extension, validate_file_size],
        db_column="ORDINAMENTO_DIDATTICO",
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_ALTRI_DATI"
        verbose_name = "Cds other data"
        verbose_name_plural = verbose_name


class DidatticaCdsGruppi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_breve_it = models.CharField(db_column="DESCR_BREVE_IT", max_length=1000)
    descr_breve_en = models.CharField(
        db_column="DESCR_BREVE_EN", max_length=1000, blank=True, null=True
    )
    descr_lunga_it = models.TextField(db_column="DESCR_LUNGA_IT", blank=True, null=True)
    descr_lunga_en = models.TextField(db_column="DESCR_LUNGA_EN", blank=True, null=True)
    didattica_cds = models.ForeignKey(
        DidatticaCds, models.DO_NOTHING, db_column="ID_DIDATTICA_CDS"
    )
    ordine = models.IntegerField(db_column="ORDINE", default=10)
    visibile = models.BooleanField(db_column="VISIBILE", default=True)
    dt_mod = models.DateField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(),
        models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_GRUPPI"
        ordering = ("ordine",)
        verbose_name = "Cds group"
        verbose_name_plural = "Cds groups"

    def __str__(self):  # pragma: no cover
        return self.descr_breve_it


class DidatticaCdsGruppiComponenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_cds_gruppi = models.ForeignKey(
        DidatticaCdsGruppi, models.CASCADE, db_column="ID_DIDATTICA_CDS_GRUPPI"
    )
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
        blank=True,
        null=True,
    )
    cognome = models.CharField(
        db_column="COGNOME", max_length=100, blank=True, null=True
    )
    nome = models.CharField(db_column="NOME", max_length=100, blank=True, null=True)
    funzione_it = models.CharField(
        db_column="FUNZIONE_IT", max_length=1000, blank=True, null=True
    )
    funzione_en = models.CharField(
        db_column="FUNZIONE_EN", max_length=1000, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE", default=10)
    visibile = models.BooleanField(db_column="VISIBILE", default=True)
    dt_mod = models.DateField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(),
        models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_GRUPPI_COMPONENTI"
        ordering = ("ordine",)
        verbose_name = "Cds group member"
        verbose_name_plural = "Cds group members"

    def __str__(self):  # pragma: no cover
        return f"{self.didattica_cds_gruppi} - {self.cognome} {self.nome}"


class DidatticaClasseLaurea(models.Model):
    cla_m_id = models.IntegerField(db_column="CLA_M_ID", primary_key=True)
    cla_miur_cod = models.CharField(db_column="CLA_MIUR_COD", max_length=20)
    cla_miur_des = models.CharField(db_column="CLA_MIUR_DES", max_length=1000)

    class Meta:
        managed = True
        db_table = "DIDATTICA_CLASSE_LAUREA"
        verbose_name = "Classe laurea"
        verbose_name_plural = "Classi laurea"


class DidatticaAmbiti(models.Model):
    amb_id = models.IntegerField(db_column="AMB_ID", primary_key=True)
    des = models.CharField(db_column="DES", max_length=255, blank=True, null=True)
    amb_sede_flg = models.IntegerField(db_column="AMB_SEDE_FLG", blank=True, null=True)
    sys_flg = models.IntegerField(db_column="SYS_FLG", blank=True, null=True)
    amb_aggr_flg = models.IntegerField(db_column="AMB_AGGR_FLG", blank=True, null=True)
    prg_ord_amb = models.IntegerField(db_column="PRG_ORD_AMB", blank=True, null=True)
    dt_ins = models.DateField(db_column="DT_INS", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_AMBITI"
        verbose_name = "Scope"
        verbose_name_plural = "Scopes"


class DidatticaPianoRegolamento(models.Model):
    regpiani_id = models.IntegerField(db_column="REGPIANI_ID", primary_key=True)
    regdid = models.ForeignKey(
        "DidatticaRegolamento",
        models.DO_NOTHING,
        db_column="REGDID_ID",
        blank=True,
        null=True,
    )
    attinenza_cod = models.CharField(
        db_column="ATTINENZA_COD", max_length=10, blank=True, null=True
    )
    cod = models.CharField(db_column="COD", max_length=10, blank=True, null=True)
    aa_coorte_id = models.IntegerField(db_column="AA_COORTE_ID", blank=True, null=True)
    aa_regpiani_id = models.IntegerField(
        db_column="AA_REGPIANI_ID", blank=True, null=True
    )
    des = models.CharField(db_column="DES", max_length=255, blank=True, null=True)
    def_flg = models.IntegerField(db_column="DEF_FLG", blank=True, null=True)
    stato_cod = models.CharField(
        db_column="STATO_COD", max_length=5, blank=True, null=True
    )
    stato_des = models.CharField(
        db_column="STATO_DES", max_length=40, blank=True, null=True
    )
    regpiani_pdr_id = models.IntegerField(
        db_column="REGPIANI_PDR_ID", blank=True, null=True
    )
    regpiani_pdr_cod = models.CharField(
        db_column="REGPIANI_PDR_COD", max_length=10, blank=True, null=True
    )
    regpiani_pdr_des = models.CharField(
        db_column="REGPIANI_PDR_DES", max_length=255, blank=True, null=True
    )
    regpiani_pdr_aa_coorte_id = models.IntegerField(
        db_column="REGPIANI_PDR_AA_COORTE_ID", blank=True, null=True
    )
    regpiani_pdr_aa_regpiani_id = models.IntegerField(
        db_column="REGPIANI_PDR_AA_REGPIANI_ID", blank=True, null=True
    )
    flg_exp_seg_stu = models.IntegerField(
        db_column="FLG_EXP_SEG_STU", blank=True, null=True
    )
    data_exp_seg_stu = models.DateField(
        db_column="DATA_EXP_SEG_STU", blank=True, null=True
    )
    nota = models.CharField(db_column="NOTA", max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_REGOLAMENTO"
        verbose_name = "Regulation study plan"
        verbose_name_plural = "Regulation study plans"


class DidatticaPianoSceltaAf(models.Model):
    sce_af_id = models.IntegerField(db_column="SCE_AF_ID", primary_key=True)    
    sce = models.ForeignKey(
        "DidatticaPianoSceltaVincoli",
        models.DO_NOTHING,
        db_column="SCE_ID",
        blank=True,
        null=True,
    )
    pds_regdid = models.ForeignKey(
        DidatticaPdsRegolamento,
        models.DO_NOTHING,
        db_column="PDS_REGDID_ID",
        blank=True,
        null=True,
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=10, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )
    sce_blk_id = models.IntegerField(db_column="SCE_BLK_ID", blank=True, null=True)
    min_unt_blk = models.DecimalField(
        db_column="MIN_UNT_BLK", max_digits=5, decimal_places=2, blank=True, null=True
    )
    max_unt_blk = models.DecimalField(
        db_column="MAX_UNT_BLK", max_digits=5, decimal_places=2, blank=True, null=True
    )
    lingua_id = models.IntegerField(db_column="LINGUA_ID", blank=True, null=True)
    blk_prg = models.IntegerField(db_column="BLK_PRG", blank=True, null=True)
    lingua_iso6392_cod = models.CharField(
        db_column="LINGUA_ISO6392_COD", max_length=3, blank=True, null=True
    )
    lingua_des = models.CharField(
        db_column="LINGUA_DES", max_length=40, blank=True, null=True
    )
    lingua_num = models.IntegerField(db_column="LINGUA_NUM", blank=True, null=True)
    af = models.ForeignKey(
        DidatticaAttivitaFormativa,
        models.DO_NOTHING,
        db_column="AF_ID",
        blank=True,
        null=True,
    )
    regud_des_auto = models.CharField(
        db_column="REGUD_DES_AUTO", max_length=1000, blank=True, null=True
    )
    regud_des_ute = models.CharField(
        db_column="REGUD_DES_UTE", max_length=1000, blank=True, null=True
    )
    min_unt_af = models.DecimalField(
        db_column="MIN_UNT_AF", max_digits=5, decimal_places=2, blank=True, null=True
    )
    max_unt_af = models.DecimalField(
        db_column="MAX_UNT_AF", max_digits=5, decimal_places=2, blank=True, null=True
    )
    statutario_flg = models.IntegerField(
        db_column="STATUTARIO_FLG", blank=True, null=True
    )
    def_verifica_flg = models.IntegerField(
        db_column="DEF_VERIFICA_FLG", blank=True, null=True
    )
    contr_aa_off_flg = models.IntegerField(
        db_column="CONTR_AA_OFF_FLG", blank=True, null=True
    )
    regdid_af_id = models.IntegerField(db_column="REGDID_AF_ID", blank=True, null=True)
    pds_regdid_af_id = models.IntegerField(
        db_column="PDS_REGDID_AF_ID", blank=True, null=True
    )
    pds_af_cod = models.CharField(
        db_column="PDS_AF_COD", max_length=10, blank=True, null=True
    )
    pds_af_des = models.CharField(
        db_column="PDS_AF_DES", max_length=255, blank=True, null=True
    )
    comune_af_flg = models.IntegerField(
        db_column="COMUNE_AF_FLG", blank=True, null=True
    )
    attinenza_af_cod = models.CharField(
        db_column="ATTINENZA_AF_COD", max_length=10, blank=True, null=True
    )
    of_id = models.IntegerField(db_column="OF_ID", blank=True, null=True)
    cds_af_id = models.IntegerField(db_column="CDS_AF_ID", blank=True, null=True)
    cds_af_cod = models.CharField(
        db_column="CDS_AF_COD", max_length=10, blank=True, null=True
    )
    nome_af_cds = models.CharField(
        db_column="NOME_AF_CDS", max_length=255, blank=True, null=True
    )
    cdsord_af_cod = models.CharField(
        db_column="CDSORD_AF_COD", max_length=10, blank=True, null=True
    )
    aa_off_id = models.IntegerField(db_column="AA_OFF_ID", blank=True, null=True)
    stato_of_cod = models.CharField(
        db_column="STATO_OF_COD", max_length=5, blank=True, null=True
    )
    tipo_comp_af_id = models.IntegerField(
        db_column="TIPO_COMP_AF_ID", blank=True, null=True
    )
    tipo_comp_af_cod = models.CharField(
        db_column="TIPO_COMP_AF_COD", max_length=10, blank=True, null=True
    )
    des_tipo_comp_af = models.CharField(
        db_column="DES_TIPO_COMP_AF", max_length=255, blank=True, null=True
    )
    af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    af_gen_cod = models.CharField(
        db_column="AF_GEN_COD", max_length=20, blank=True, null=True
    )
    af_gen_des = models.CharField(
        db_column="AF_GEN_DES", max_length=255, blank=True, null=True
    )
    anno_corso_af = models.IntegerField(
        db_column="ANNO_CORSO_AF", blank=True, null=True
    )
    lista_anni_corso_af = models.CharField(
        db_column="LISTA_ANNI_CORSO_AF", max_length=20, blank=True, null=True
    )
    af_regdid_id = models.IntegerField(db_column="AF_REGDID_ID", blank=True, null=True)
    sett_cod = models.CharField(
        db_column="SETT_COD", max_length=12, blank=True, null=True
    )
    tipo_af_cod_af = models.CharField(
        db_column="TIPO_AF_COD_AF", max_length=10, blank=True, null=True
    )
    tipo_af_des_af = models.CharField(
        db_column="TIPO_AF_DES_AF", max_length=80, blank=True, null=True
    )
    amb_id_af = models.ForeignKey(
        DidatticaAmbiti, models.DO_NOTHING, db_column="AMB_ID_AF", blank=True, null=True
    )
    ambito_des_af = models.CharField(
        db_column="AMBITO_DES_AF", max_length=255, blank=True, null=True
    )
    tipo_af_intercla_cod_af = models.CharField(
        db_column="TIPO_AF_INTERCLA_COD_AF", max_length=10, blank=True, null=True
    )
    tipo_af_intercla_des_af = models.CharField(
        db_column="TIPO_AF_INTERCLA_DES_AF", max_length=80, blank=True, null=True
    )
    amb_intercla_id_af = models.IntegerField(
        db_column="AMB_INTERCLA_ID_AF", blank=True, null=True
    )
    ambito_intercla_des_af = models.CharField(
        db_column="AMBITO_INTERCLA_DES_AF", max_length=255, blank=True, null=True
    )
    peso = models.DecimalField(
        db_column="PESO", max_digits=5, decimal_places=2, blank=True, null=True
    )
    peso_foglie_non_log = models.DecimalField(
        db_column="PESO_FOGLIE_NON_LOG",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    num_max_reit = models.IntegerField(db_column="NUM_MAX_REIT", blank=True, null=True)
    non_erogabile_flg = models.IntegerField(
        db_column="NON_EROGABILE_FLG", blank=True, null=True
    )
    livello_af_cod = models.CharField(
        db_column="LIVELLO_AF_COD", max_length=10, blank=True, null=True
    )
    livello_af_des = models.CharField(
        db_column="LIVELLO_AF_DES", max_length=40, blank=True, null=True
    )
    tipo_esa_cod = models.CharField(
        db_column="TIPO_ESA_COD", max_length=5, blank=True, null=True
    )
    tipo_esa_des = models.CharField(
        db_column="TIPO_ESA_DES", max_length=40, blank=True, null=True
    )
    tipo_val_cod = models.CharField(
        db_column="TIPO_VAL_COD", max_length=5, blank=True, null=True
    )
    tipo_val_des = models.CharField(
        db_column="TIPO_VAL_DES", max_length=40, blank=True, null=True
    )
    af_pdr_id = models.IntegerField(db_column="AF_PDR_ID", blank=True, null=True)
    af_radice_id = models.IntegerField(db_column="AF_RADICE_ID", blank=True, null=True)
    num_liv_albero = models.IntegerField(
        db_column="NUM_LIV_ALBERO", blank=True, null=True
    )
    ciclo_id = models.IntegerField(db_column="CICLO_ID", blank=True, null=True)
    ciclo_des = models.CharField(
        db_column="CICLO_DES", max_length=40, blank=True, null=True
    )
    tipo_ciclo_cod = models.CharField(
        db_column="TIPO_CICLO_COD", max_length=5, blank=True, null=True
    )
    des_tipo_ciclo = models.CharField(
        db_column="DES_TIPO_CICLO", max_length=40, blank=True, null=True
    )
    org_did_sua_cod = models.IntegerField(
        db_column="ORG_DID_SUA_COD", blank=True, null=True
    )
    sede_id = models.IntegerField(db_column="SEDE_ID", blank=True, null=True)
    sede_des = models.CharField(
        db_column="SEDE_DES", max_length=255, blank=True, null=True
    )
    tipo_rag_cod = models.CharField(
        db_column="TIPO_RAG_COD", max_length=5, blank=True, null=True
    )
    tipo_rag_des = models.CharField(
        db_column="TIPO_RAG_DES", max_length=40, blank=True, null=True
    )
    af_capogruppo_id = models.IntegerField(
        db_column="AF_CAPOGRUPPO_ID", blank=True, null=True
    )
    scelta_mod_flg = models.IntegerField(
        db_column="SCELTA_MOD_FLG", blank=True, null=True
    )
    num_regud = models.DecimalField(
        db_column="NUM_REGUD", max_digits=38, decimal_places=0, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_SCELTA_AF"
        ordering = ("ciclo_des",)
        verbose_name = "Study plan study activity choice"
        verbose_name_plural = "Study plan study activity choices"


class DidatticaPianoSceltaFilAnd(models.Model):
    sce_fil_and_id = models.IntegerField(db_column="SCE_FIL_AND_ID", primary_key=True)
    sce = models.ForeignKey(
        "DidatticaPianoSceltaVincoli",
        models.DO_NOTHING,
        db_column="SCE_ID",
        blank=True,
        null=True,
    )
    sce_fil_or_id = models.IntegerField(
        db_column="SCE_FIL_OR_ID", blank=True, null=True
    )
    sce_fil_or_des = models.CharField(
        db_column="SCE_FIL_OR_DES", max_length=255, blank=True, null=True
    )
    tipo_filtro_cod = models.CharField(
        db_column="TIPO_FILTRO_COD", max_length=10, blank=True, null=True
    )
    tipo_filtro_des = models.CharField(
        db_column="TIPO_FILTRO_DES", max_length=255, blank=True, null=True
    )
    af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    af_gen_cod = models.CharField(
        db_column="AF_GEN_COD", max_length=20, blank=True, null=True
    )
    af_gen_des = models.CharField(
        db_column="AF_GEN_DES", max_length=255, blank=True, null=True
    )
    dip_sce_fil_and_id = models.IntegerField(
        db_column="DIP_SCE_FIL_AND_ID", blank=True, null=True
    )
    dip_sce_fil_and_cod = models.CharField(
        db_column="DIP_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    dip_sce_fil_and_des = models.CharField(
        db_column="DIP_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    )
    strac_sce_fil_and_id = models.IntegerField(
        db_column="STRAC_SCE_FIL_AND_ID", blank=True, null=True
    )
    strac_sce_fil_and_cod = models.CharField(
        db_column="STRAC_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    strac_sce_fil_and_des = models.CharField(
        db_column="STRAC_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    )
    cds_sce_fil_and_id = models.IntegerField(
        db_column="CDS_SCE_FIL_AND_ID", blank=True, null=True
    )
    cds_sce_fil_and_cod = models.CharField(
        db_column="CDS_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    cds_sce_fil_and_nome = models.CharField(
        db_column="CDS_SCE_FIL_AND_NOME", max_length=255, blank=True, null=True
    )
    cfu = models.DecimalField(
        db_column="CFU", max_digits=5, decimal_places=2, blank=True, null=True
    )
    tipo_af_sce_fil_and_cod = models.CharField(
        db_column="TIPO_AF_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    tipo_af_sce_fil_and_des = models.CharField(
        db_column="TIPO_AF_SCE_FIL_AND_DES", max_length=80, blank=True, null=True
    )
    sett_cod = models.CharField(
        db_column="SETT_COD", max_length=12, blank=True, null=True
    )
    tipo_corso_sce_fil_and_cod = models.CharField(
        db_column="TIPO_CORSO_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    cla_miur_sce_fil_and_id = models.IntegerField(
        db_column="CLA_MIUR_SCE_FIL_AND_ID", blank=True, null=True
    )
    cla_miur_sce_fil_and_cod = models.CharField(
        db_column="CLA_MIUR_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    )
    cla_miur_sce_fil_and_des = models.CharField(
        db_column="CLA_MIUR_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    )
    rif_cod = models.CharField(
        db_column="RIF_COD", max_length=10, blank=True, null=True
    )
    sett_post_rif_flg = models.IntegerField(
        db_column="SETT_POST_RIF_FLG", blank=True, null=True
    )
    tipo_ins_cod = models.CharField(
        db_column="TIPO_INS_COD", max_length=10, blank=True, null=True
    )
    peso_sce_fil_and = models.IntegerField(
        db_column="PESO_SCE_FIL_AND", blank=True, null=True
    )
    not_flg = models.IntegerField(db_column="NOT_FLG", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_SCELTA_FIL_AND"
        verbose_name = "Study plan choice filter"
        verbose_name_plural = "Study plan choice filters"


class DidatticaPianoSceltaSchePiano(models.Model):
    sche_piano = models.OneToOneField(
        "DidatticaPianoSche",
        models.DO_NOTHING,
        db_column="SCHE_PIANO_ID",
        primary_key=True,
        related_name="didatticapianosceltaschepiano"
    )
    sche_statutario_flg = models.BooleanField(
        db_column="SCHE_STATUTARIO_FLG", default=False
    )
    sche_pds_regdid_id = models.IntegerField(
        db_column="SCHE_PDS_REGDID_ID", blank=True, null=True
    )
    sche_pds_cod = models.CharField(
        db_column="SCHE_PDS_COD", max_length=10, blank=True, null=True
    )
    sche_pds_des = models.CharField(
        db_column="SCHE_PDS_DES", max_length=255, blank=True, null=True
    )
    sche_ori_id = models.IntegerField(db_column="SCHE_ORI_ID", blank=True, null=True)
    sche_cla_m_id = models.IntegerField(
        db_column="SCHE_CLA_M_ID", blank=True, null=True
    )
    sche_apt_id = models.IntegerField(db_column="SCHE_APT_ID", blank=True, null=True)
    sche_nota = models.CharField(
        db_column="SCHE_NOTA", max_length=1000, blank=True, null=True
    )
    data_ini_val = models.DateField(db_column="DATA_INI_VAL", blank=True, null=True)
    data_fine_val = models.DateField(db_column="DATA_FINE_VAL", blank=True, null=True)
    stato_piano_gen_cod = models.CharField(
        db_column="STATO_PIANO_GEN_COD", max_length=10, blank=True, null=True
    )
    contr_ac_piano_stu_cod = models.CharField(
        db_column="CONTR_AC_PIANO_STU_COD", max_length=10, blank=True, null=True
    )
    blocco_af_freq_piano_stu_flg = models.IntegerField(
        db_column="BLOCCO_AF_FREQ_PIANO_STU_FLG", blank=True, null=True
    )
    sce = models.ForeignKey(
        "DidatticaPianoSceltaVincoli", models.DO_NOTHING, db_column="SCE_ID"
    )
    ord_num = models.IntegerField(db_column="ORD_NUM", blank=True, null=True)
    apt_slot_id = models.IntegerField(db_column="APT_SLOT_ID", blank=True, null=True)
    apt_slot_cod = models.CharField(
        db_column="APT_SLOT_COD", max_length=10, blank=True, null=True
    )
    apt_slot_des = models.CharField(
        db_column="APT_SLOT_DES", max_length=255, blank=True, null=True
    )
    apt_slot_anno_corso = models.IntegerField(
        db_column="APT_SLOT_ANNO_CORSO", blank=True, null=True
    )
    apt_slot_ord_num = models.IntegerField(
        db_column="APT_SLOT_ORD_NUM", blank=True, null=True
    )
    sce_des = models.CharField(
        db_column="SCE_DES", max_length=255, blank=True, null=True
    )
    pds_regdid_id = models.IntegerField(
        db_column="PDS_REGDID_ID", blank=True, null=True
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=10, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )
    comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    anno_corso_ant = models.IntegerField(
        db_column="ANNO_CORSO_ANT", blank=True, null=True
    )
    tipo_regsce_cod = models.CharField(
        db_column="TIPO_REGSCE_COD", max_length=10, blank=True, null=True
    )
    tipo_sce_cod = models.CharField(
        db_column="TIPO_SCE_COD", max_length=5, blank=True, null=True
    )
    tipo_sce_des = models.CharField(
        db_column="TIPO_SCE_DES", max_length=40, blank=True, null=True
    )
    tipo_regsce_des = models.CharField(
        db_column="TIPO_REGSCE_DES", max_length=40, blank=True, null=True
    )
    tipo_um_regsce_cod = models.CharField(
        db_column="TIPO_UM_REGSCE_COD", max_length=5, blank=True, null=True
    )
    opz_flg = models.IntegerField(db_column="OPZ_FLG", blank=True, null=True)
    min_unt = models.DecimalField(
        db_column="MIN_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    )
    max_unt = models.DecimalField(
        db_column="MAX_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    )
    livello = models.IntegerField(db_column="LIVELLO", blank=True, null=True)
    vin_id = models.IntegerField(db_column="VIN_ID", blank=True, null=True)
    vin_ord_num = models.IntegerField(db_column="VIN_ORD_NUM", blank=True, null=True)
    vin_sce_des = models.CharField(
        db_column="VIN_SCE_DES", max_length=255, blank=True, null=True
    )
    tipi_af_tipi_sce_id = models.IntegerField(
        db_column="TIPI_AF_TIPI_SCE_ID", blank=True, null=True
    )
    tipo_af_cod = models.CharField(
        db_column="TIPO_AF_COD", max_length=10, blank=True, null=True
    )
    tipo_af_des = models.CharField(
        db_column="TIPO_AF_DES", max_length=80, blank=True, null=True
    )
    amb = models.ForeignKey(
        DidatticaAmbiti, models.DO_NOTHING, db_column="AMB_ID", blank=True, null=True
    )
    ambito_des = models.CharField(
        db_column="AMBITO_DES", max_length=255, blank=True, null=True
    )
    sovran_flg = models.IntegerField(db_column="SOVRAN_FLG", blank=True, null=True)
    sostegno_flg = models.IntegerField(db_column="SOSTEGNO_FLG", blank=True, null=True)
    peso_sce = models.IntegerField(db_column="PESO_SCE", blank=True, null=True)
    tesoretto_flg = models.IntegerField(
        db_column="TESORETTO_FLG", blank=True, null=True
    )
    assegnazione_posti_flg = models.IntegerField(
        db_column="ASSEGNAZIONE_POSTI_FLG", blank=True, null=True
    )
    delibera_flg = models.IntegerField(db_column="DELIBERA_FLG", blank=True, null=True)
    azzera_cfu_flg = models.IntegerField(
        db_column="AZZERA_CFU_FLG", blank=True, null=True
    )
    parametri_logistica_flg = models.IntegerField(
        db_column="PARAMETRI_LOGISTICA_FLG", blank=True, null=True
    )
    tag_regsce_cod = models.CharField(
        db_column="TAG_REGSCE_COD", max_length=20, blank=True, null=True
    )
    peso_af_sce = models.DecimalField(
        db_column="PESO_AF_SCE", max_digits=38, decimal_places=0, blank=True, null=True
    )
    peso_min_singola_af = models.DecimalField(
        db_column="PESO_MIN_SINGOLA_AF",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    peso_max_singola_af = models.DecimalField(
        db_column="PESO_MAX_SINGOLA_AF",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_af_sce = models.DecimalField(
        db_column="NUM_AF_SCE", max_digits=38, decimal_places=0, blank=True, null=True
    )
    peso_af_sce_stat = models.DecimalField(
        db_column="PESO_AF_SCE_STAT",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    peso_af_sce_def_verifica = models.DecimalField(
        db_column="PESO_AF_SCE_DEF_VERIFICA",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_blk = models.DecimalField(
        db_column="NUM_BLK", max_digits=38, decimal_places=0, blank=True, null=True
    )
    num_blk_stat = models.DecimalField(
        db_column="NUM_BLK_STAT", max_digits=38, decimal_places=0, blank=True, null=True
    )
    num_blk_def_verifica = models.DecimalField(
        db_column="NUM_BLK_DEF_VERIFICA",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_blk_contr_aa_off = models.DecimalField(
        db_column="NUM_BLK_CONTR_AA_OFF",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_blk_statutario_flg_div = models.DecimalField(
        db_column="NUM_BLK_STATUTARIO_FLG_DIV",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_blk_def_verifica_flg_div = models.DecimalField(
        db_column="NUM_BLK_DEF_VERIFICA_FLG_DIV",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_blk_contr_aa_off_flg_div = models.DecimalField(
        db_column="NUM_BLK_CONTR_AA_OFF_FLG_DIV",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    peso_blk = models.DecimalField(
        db_column="PESO_BLK", max_digits=38, decimal_places=0, blank=True, null=True
    )
    af_stessa_taf_flg = models.DecimalField(
        db_column="AF_STESSA_TAF_FLG",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    af_stessa_taf_intercla_flg = models.DecimalField(
        db_column="AF_STESSA_TAF_INTERCLA_FLG",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    af_stesso_ambito_flg = models.DecimalField(
        db_column="AF_STESSO_AMBITO_FLG",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    af_stesso_ambito_intercla_flg = models.DecimalField(
        db_column="AF_STESSO_AMBITO_INTERCLA_FLG",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    amb_id_af_regsce = models.DecimalField(
        db_column="AMB_ID_AF_REGSCE",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    tipo_af_cod_af_regsce = models.CharField(
        db_column="TIPO_AF_COD_AF_REGSCE", max_length=10, blank=True, null=True
    )
    amb_intercla_id_af_regsce = models.DecimalField(
        db_column="AMB_INTERCLA_ID_AF_REGSCE",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    tipo_af_intercla_cod_af_regsce = models.CharField(
        db_column="TIPO_AF_INTERCLA_COD_AF_REGSCE", max_length=10, blank=True, null=True
    )
    num_af_taf_d = models.DecimalField(
        db_column="NUM_AF_TAF_D", max_digits=38, decimal_places=0, blank=True, null=True
    )
    num_af_taf_intercla_d = models.DecimalField(
        db_column="NUM_AF_TAF_INTERCLA_D",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_af_taf_e_f_s = models.DecimalField(
        db_column="NUM_AF_TAF_E_F_S",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    num_af_taf_intercla_e_f_s = models.DecimalField(
        db_column="NUM_AF_TAF_INTERCLA_E_F_S",
        max_digits=38,
        decimal_places=0,
        blank=True,
        null=True,
    )
    sett_cod_af_regsce = models.CharField(
        db_column="SETT_COD_AF_REGSCE", max_length=12, blank=True, null=True
    )
    nota_pre = models.TextField(db_column="NOTA_PRE", blank=True, null=True)
    nota_pre_vis_web_flg = models.IntegerField(
        db_column="NOTA_PRE_VIS_WEB_FLG", blank=True, null=True
    )
    nota_post = models.TextField(db_column="NOTA_POST", blank=True, null=True)
    nota_post_vis_web_flg = models.IntegerField(
        db_column="NOTA_POST_VIS_WEB_FLG", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_SCELTA_SCHE_PIANO"
        unique_together = (("sche_piano", "sce"),)
        verbose_name = "Study plan sheet choice plan"
        verbose_name_plural = "Study plan sheet choice plans"


class DidatticaPianoSceltaVincoli(models.Model):
    sce_id = models.IntegerField(db_column="SCE_ID", primary_key=True)
    regpiani = models.ForeignKey(
        DidatticaPianoRegolamento,
        models.DO_NOTHING,
        db_column="REGPIANI_ID",
        blank=True,
        null=True,
    )
    ord_num = models.IntegerField(db_column="ORD_NUM", blank=True, null=True)
    sce_des = models.CharField(
        db_column="SCE_DES", max_length=255, blank=True, null=True
    )
    pds_regdid = models.ForeignKey(
        DidatticaPdsRegolamento,
        models.DO_NOTHING,
        db_column="PDS_REGDID_ID",
        blank=True,
        null=True,
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=10, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )
    comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    anno_corso_ant = models.IntegerField(
        db_column="ANNO_CORSO_ANT", blank=True, null=True
    )
    tipo_regsce_cod = models.CharField(
        db_column="TIPO_REGSCE_COD", max_length=10, blank=True, null=True
    )
    tipo_sce_cod = models.CharField(
        db_column="TIPO_SCE_COD", max_length=5, blank=True, null=True
    )
    tipo_um_regsce_cod = models.CharField(
        db_column="TIPO_UM_REGSCE_COD", max_length=5, blank=True, null=True
    )
    opz_flg = models.IntegerField(db_column="OPZ_FLG", blank=True, null=True)
    min_unt = models.DecimalField(
        db_column="MIN_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    )
    max_unt = models.DecimalField(
        db_column="MAX_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    )
    livello = models.IntegerField(db_column="LIVELLO", blank=True, null=True)
    vin = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="VIN_ID", blank=True, null=True
    )
    vin_ord_num = models.IntegerField(db_column="VIN_ORD_NUM", blank=True, null=True)
    vin_sce_des = models.CharField(
        db_column="VIN_SCE_DES", max_length=255, blank=True, null=True
    )
    tipi_af_tipi_sce_id = models.IntegerField(
        db_column="TIPI_AF_TIPI_SCE_ID", blank=True, null=True
    )
    tipo_af_cod = models.CharField(
        db_column="TIPO_AF_COD", max_length=10, blank=True, null=True
    )
    tipo_af_des = models.CharField(
        db_column="TIPO_AF_DES", max_length=80, blank=True, null=True
    )
    amb_id = models.IntegerField(db_column="AMB_ID", blank=True, null=True)
    ambito_des = models.CharField(
        db_column="AMBITO_DES", max_length=255, blank=True, null=True
    )
    sovran_flg = models.IntegerField(db_column="SOVRAN_FLG", blank=True, null=True)
    sostegno_flg = models.IntegerField(db_column="SOSTEGNO_FLG", blank=True, null=True)
    peso_sce = models.IntegerField(db_column="PESO_SCE", blank=True, null=True)
    tesoretto_flg = models.IntegerField(
        db_column="TESORETTO_FLG", blank=True, null=True
    )
    assegnazione_posti_flg = models.IntegerField(
        db_column="ASSEGNAZIONE_POSTI_FLG", blank=True, null=True
    )
    delibera_flg = models.IntegerField(db_column="DELIBERA_FLG", blank=True, null=True)
    azzera_cfu_flg = models.IntegerField(
        db_column="AZZERA_CFU_FLG", blank=True, null=True
    )
    parametri_logistica_flg = models.IntegerField(
        db_column="PARAMETRI_LOGISTICA_FLG", blank=True, null=True
    )
    tag_regsce_cod = models.CharField(
        db_column="TAG_REGSCE_COD", max_length=20, blank=True, null=True
    )
    nota_pre = models.TextField(db_column="NOTA_PRE", blank=True, null=True)
    nota_pre_vis_web_flg = models.IntegerField(
        db_column="NOTA_PRE_VIS_WEB_FLG", blank=True, null=True
    )
    nota_post = models.TextField(db_column="NOTA_POST", blank=True, null=True)
    nota_post_vis_web_flg = models.IntegerField(
        db_column="NOTA_POST_VIS_WEB_FLG", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_SCELTA_VINCOLI"
        verbose_name = "Study plan constraint choice"
        verbose_name_plural = "Study plan constraint choices"


class DidatticaPianoSche(models.Model):
    sche_piano_id = models.IntegerField(db_column="SCHE_PIANO_ID", primary_key=True)
    regpiani = models.ForeignKey(
        DidatticaPianoRegolamento, models.DO_NOTHING, db_column="REGPIANI_ID", related_name="didatticapianosche"
    )
    sche_piano_cod = models.CharField(
        db_column="SCHE_PIANO_COD", max_length=10, blank=True, null=True
    )
    sche_piano_des = models.CharField(
        db_column="SCHE_PIANO_DES", max_length=255, blank=True, null=True
    )
    sche_piano_vis_web_flg = models.IntegerField(
        db_column="SCHE_PIANO_VIS_WEB_FLG", blank=True, null=True
    )
    pds_regdid = models.ForeignKey(
        DidatticaPdsRegolamento,
        models.DO_NOTHING,
        db_column="PDS_REGDID_ID",
        blank=True,
        null=True,
    )
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=10, blank=True, null=True
    )
    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )
    comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    ori_id = models.IntegerField(db_column="ORI_ID", blank=True, null=True)
    ori_cod = models.CharField(
        db_column="ORI_COD", max_length=10, blank=True, null=True
    )
    ori_des = models.CharField(
        db_column="ORI_DES", max_length=255, blank=True, null=True
    )
    cla_m_id = models.IntegerField(db_column="CLA_M_ID", blank=True, null=True)
    cla_miur_cod = models.CharField(
        db_column="CLA_MIUR_COD", max_length=10, blank=True, null=True
    )
    cla_miur_des = models.CharField(
        db_column="CLA_MIUR_DES", max_length=255, blank=True, null=True
    )
    apt_id = models.IntegerField(db_column="APT_ID", blank=True, null=True)
    apt_cod = models.CharField(
        db_column="APT_COD", max_length=10, blank=True, null=True
    )
    apt_des = models.CharField(
        db_column="APT_DES", max_length=80, blank=True, null=True
    )
    data_ini_val = models.DateField(db_column="DATA_INI_VAL", blank=True, null=True)
    data_fine_val = models.DateField(db_column="DATA_FINE_VAL", blank=True, null=True)
    stato_piano_gen_cod = models.CharField(
        db_column="STATO_PIANO_GEN_COD", max_length=10, blank=True, null=True
    )
    stato_piano_gen_des = models.CharField(
        db_column="STATO_PIANO_GEN_DES", max_length=40, blank=True, null=True
    )
    contr_ac_piano_stu_cod = models.CharField(
        db_column="CONTR_AC_PIANO_STU_COD", max_length=10, blank=True, null=True
    )
    blocco_af_freq_piano_stu_flg = models.IntegerField(
        db_column="BLOCCO_AF_FREQ_PIANO_STU_FLG", blank=True, null=True
    )
    nota_sche_piano = models.CharField(
        db_column="NOTA_SCHE_PIANO", max_length=1000, blank=True, null=True
    )
    sche_piano_des_txt_id = models.IntegerField(
        db_column="SCHE_PIANO_DES_TXT_ID", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_PIANO_SCHE"
        verbose_name = "Study plan sheet"
        verbose_name_plural = "Study plan sheets"


class DidatticaCdsTipoCorso(Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_corso_cod = models.CharField(
        db_column="TIPO_CORSO_COD", max_length=10, blank=True, null=True
    )
    tipo_corso_des = models.CharField(
        db_column="TIPO_CORSO_DES", max_length=80, blank=True, null=True
    )
    note = models.CharField(db_column="NOTE", max_length=400, blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_TIPO_CORSO"
        verbose_name = "Cds course type"
        verbose_name_plural = "Cds course types"
