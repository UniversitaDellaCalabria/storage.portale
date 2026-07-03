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
        managed = False
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
        managed = False
        db_table = "DIDATTICA_SSD"
        verbose_name = "SSD"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.ssd_id} {self.ssd_des}"


class DidatticaAttivitaFormativa(models.Model):
    af_off_id = models.IntegerField(db_column='AF_OFF_ID', primary_key=True)  # Field name made lowercase.
    ana_af_id = models.IntegerField(db_column='ANA_AF_ID')  # Field name made lowercase.
    ana_af_cod = models.CharField(db_column='ANA_AF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_ita = models.CharField(db_column='ANA_AF_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_eng = models.CharField(db_column='ANA_AF_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_af_cod = models.CharField(db_column='STATO_AF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stato_af_desc_ita = models.CharField(db_column='STATO_AF_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_desc_ita = models.CharField(db_column='TIPO_INS_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    off_did_id = models.IntegerField(db_column='OFF_DID_ID', blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stato_of_desc_ita = models.CharField(db_column='STATO_OF_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='ID_CDS', blank=True, null=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    doc_tit_id_ab = models.ForeignKey('addressbook.Personale', on_delete=models.DO_NOTHING, db_column='DOC_TIT_ID_AB', to_field='id_ab', blank=True, null=True, related_name='af')  # Field name made lowercase.
    doc_tit_matricola = models.CharField(db_column='DOC_TIT_MATRICOLA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    doc_tit_tipo_impegno = models.CharField(db_column='DOC_TIT_TIPO_IMPEGNO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flag_a_distanza = models.CharField(db_column='FLAG_A_DISTANZA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_af_off_integrato = models.CharField(db_column='FLAG_AF_OFF_INTEGRATO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_erogabile = models.CharField(db_column='FLAG_EROGABILE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_integrato = models.CharField(db_column='FLAG_INTEGRATO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_professionalizzante = models.CharField(db_column='FLAG_PROFESSIONALIZZANTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fl_ofa = models.CharField(db_column='FL_OFA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DIDATTICA_ATTIVITA_FORMATIVA"
        verbose_name = "Study activity"
        verbose_name_plural = "Study activities"
        # ~ ordering = ("ciclo_des",)

    def __str__(self):  # pragma: no cover
        return "{}".format(self.af_off_id)

    # ~ def checkIfMainCourse(self):
        # ~ return self.af_id == self.af_radice_id


class DidatticaAttivitaFormativaErogata(models.Model):
    erog_id = models.IntegerField(db_column='EROG_ID', primary_key=True)  # Field name made lowercase.
    lingua_did_cod = models.CharField(db_column='LINGUA_DID_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lingua_did_desc_ita = models.CharField(db_column='LINGUA_DID_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lingua_did_desc_eng = models.CharField(db_column='LINGUA_DID_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mod_off_id = models.ForeignKey('DidatticaAttivitaFormativaModulo', models.DO_NOTHING, db_column='MOD_OFF_ID', blank=True, null=True, related_name="erogazioni")
    part_stu_id = models.IntegerField(db_column='PART_STU_ID', blank=True, null=True)  # Field name made lowercase.
    part_stu_cod = models.CharField(db_column='PART_STU_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    part_stu_desc_ita = models.CharField(db_column='PART_STU_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    part_stu_desc_eng = models.CharField(db_column='PART_STU_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gruppo_stu_id = models.IntegerField(db_column='GRUPPO_STU_ID', blank=True, null=True)  # Field name made lowercase.
    gruppo_stu_cod = models.CharField(db_column='GRUPPO_STU_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    gruppo_stu_desc_ita = models.CharField(db_column='GRUPPO_STU_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gruppo_stu_desc_eng = models.CharField(db_column='GRUPPO_STU_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fatt_part_stu_cod = models.CharField(db_column='FATT_PART_STU_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fatt_part_stu_desc_ita = models.CharField(db_column='FATT_PART_STU_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fatt_part_stu_desc_eng = models.CharField(db_column='FATT_PART_STU_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fatt_gruppo_stu_cod = models.CharField(db_column='FATT_GRUPPO_STU_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fatt_gruppo_stu_desc_ita = models.CharField(db_column='FATT_GRUPPO_STU_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fatt_gruppo_stu_desc_eng = models.CharField(db_column='FATT_GRUPPO_STU_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_periodo_did_cod = models.CharField(db_column='TIPO_PERIODO_DID_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_periodo_did_desc_ita = models.CharField(db_column='TIPO_PERIODO_DID_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_periodo_did_desc_eng = models.CharField(db_column='TIPO_PERIODO_DID_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_inizio_periodo = models.DateField(db_column='DATA_INIZIO_PERIODO', blank=True, null=True)  # Field name made lowercase.
    data_fine_periodo = models.DateField(db_column='DATA_FINE_PERIODO', blank=True, null=True)  # Field name made lowercase.
    mod_did_cod = models.CharField(db_column='MOD_DID_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_ita = models.CharField(db_column='MOD_DID_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_eng = models.CharField(db_column='MOD_DID_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    erog_master_id = models.IntegerField(db_column='EROG_MASTER_ID', blank=True, null=True)  # Field name made lowercase.
    erogazione = models.IntegerField(db_column='EROGAZIONE', blank=True, null=True)  # Field name made lowercase.
    master = models.IntegerField(db_column='MASTER', blank=True, null=True)  # Field name made lowercase.
    mutuante = models.IntegerField(db_column='MUTUANTE', blank=True, null=True)  # Field name made lowercase.
    mutuata = models.IntegerField(db_column='MUTUATA', blank=True, null=True)  # Field name made lowercase.
    coperta = models.IntegerField(db_column='COPERTA', blank=True, null=True)  # Field name made lowercase.
    flag_master = models.CharField(db_column='FLAG_MASTER', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_mutuante = models.CharField(db_column='FLAG_MUTUANTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_mutuata = models.CharField(db_column='FLAG_MUTUATA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_coperta = models.CharField(db_column='FLAG_COPERTA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_EROGATA'
        ordering = ('erog_id',)


class DidatticaAttivitaFormativaModulo(models.Model):
    mod_off_id = models.IntegerField(db_column='MOD_OFF_ID', primary_key=True)  # Field name made lowercase.
    ana_mod_id = models.IntegerField(db_column='ANA_MOD_ID')  # Field name made lowercase.
    ana_mod_cod = models.CharField(db_column='ANA_MOD_COD', max_length=20)  # Field name made lowercase.
    ana_mod_desc_ita = models.CharField(db_column='ANA_MOD_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_mod_desc_eng = models.CharField(db_column='ANA_MOD_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_erog_mod = models.CharField(db_column='STATO_EROG_MOD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_off = models.ForeignKey('DidatticaAttivitaFormativa', models.DO_NOTHING, db_column='AF_OFF_ID', blank=True, null=True, related_name="moduli")  # Field name made lowercase.
    doc_tit_id_ab = models.ForeignKey('addressbook.Personale', on_delete=models.DO_NOTHING, db_column='DOC_TIT_ID_AB', to_field='id_ab', blank=True, null=True, related_name='doc_tit')  # Field name made lowercase.
    doc_tit_matricola = models.CharField(db_column='DOC_TIT_MATRICOLA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    doc_resp_mod_id_ab = models.ForeignKey('addressbook.Personale', on_delete=models.DO_NOTHING, db_column='DOC_RESP_MOD_ID_AB', to_field='id_ab', blank=True, null=True, related_name='doc_mod_tit')  # Field name made lowercase.
    doc_resp_mod_matricola = models.CharField(db_column='DOC_RESP_MOD_MATRICOLA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flag_a_distanza = models.CharField(db_column='FLAG_A_DISTANZA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_af_off_integrato = models.CharField(db_column='FLAG_AF_OFF_INTEGRATO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_erogabile = models.CharField(db_column='FLAG_EROGABILE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_integrato = models.CharField(db_column='FLAG_INTEGRATO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_professionalizzante = models.CharField(db_column='FLAG_PROFESSIONALIZZANTE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_MODULO'


class DidatticaAttivitaFormativaPds(models.Model):
    af_pds_id = models.IntegerField(db_column='AF_PDS_ID', primary_key=True)  # Field name made lowercase.
    id_cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='ID_CDS', blank=True, null=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ord_id = models.IntegerField(db_column='ORD_ID', blank=True, null=True)  # Field name made lowercase.
    ord_cod = models.CharField(db_column='ORD_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_id = models.IntegerField(db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    id_off = models.CharField(db_column='ID_OFF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_di_scelta_percorso = models.DecimalField(db_column='ANNO_DI_SCELTA_PERCORSO', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pds_regdid_comune_id = models.IntegerField(db_column='PDS_REGDID_COMUNE_ID', blank=True, null=True)  # Field name made lowercase.
    num_pds = models.IntegerField(db_column='NUM_PDS', blank=True, null=True)  # Field name made lowercase.
    pds_regdid_id = models.IntegerField(db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pds_desc_ita = models.CharField(db_column='PDS_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_desc_eng = models.CharField(db_column='PDS_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_id_riferimento = models.IntegerField(db_column='PDS_ID_RIFERIMENTO', blank=True, null=True)  # Field name made lowercase.
    lingua_cod = models.CharField(db_column='LINGUA_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ana_af_id = models.IntegerField(db_column='ANA_AF_ID', blank=True, null=True)  # Field name made lowercase.
    ana_af_cod = models.CharField(db_column='ANA_AF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_ita = models.CharField(db_column='ANA_AF_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_eng = models.CharField(db_column='ANA_AF_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_id = models.IntegerField(db_column='ANA_AF_CAPOG_ID', blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_cod = models.CharField(db_column='ANA_AF_CAPOG_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_desc_ita = models.CharField(db_column='ANA_AF_CAPOG_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_desc_eng = models.CharField(db_column='ANA_AF_CAPOG_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    flag_obbl = models.CharField(db_column='FLAG_OBBL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    flag_raggruppamento = models.CharField(db_column='FLAG_RAGGRUPPAMENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_capogruppo = models.CharField(db_column='FLAG_CAPOGRUPPO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_raggruppata = models.CharField(db_column='FLAG_RAGGRUPPATA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_no_raggr_o_capog = models.CharField(db_column='FLAG_NO_RAGGR_O_CAPOG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cfu = models.FloatField(db_column='CFU', blank=True, null=True)  # Field name made lowercase.
    ore = models.FloatField(db_column='ORE', blank=True, null=True)  # Field name made lowercase.
    erog_id = models.ForeignKey('DidatticaAttivitaFormativaErogata', models.DO_NOTHING, db_column='EROG_ID', blank=True, null=True, related_name="pds")  # Field name made lowercase.
    coper_id = models.IntegerField(db_column='COPER_ID')  # Field name made lowercase.
    mod_did_cod = models.CharField(db_column='MOD_DID_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_ita = models.CharField(db_column='MOD_DID_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_eng = models.CharField(db_column='MOD_DID_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    moduli_pds_id = models.IntegerField(db_column='MODULI_PDS_ID', blank=True, null=True)  # Field name made lowercase.
    ana_mod_sett_id = models.IntegerField(db_column='ANA_MOD_SETT_ID', blank=True, null=True)  # Field name made lowercase.
    flag_segmento = models.CharField(db_column='FLAG_SEGMENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sett_desc_ita = models.CharField(db_column='SETT_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sett_desc_eng = models.CharField(db_column='SETT_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_mod_id = models.IntegerField(db_column='ANA_MOD_ID', blank=True, null=True)  # Field name made lowercase.
    ana_mod_cod = models.CharField(db_column='ANA_MOD_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ana_mod_desc_ita = models.CharField(db_column='ANA_MOD_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ana_mod_desc_eng = models.CharField(db_column='ANA_MOD_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taf_cod = models.CharField(db_column='TAF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taf_desc_ita = models.CharField(db_column='TAF_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taf_desc_eng = models.CharField(db_column='TAF_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_ambito = models.IntegerField(db_column='ID_AMBITO', blank=True, null=True)  # Field name made lowercase.
    ambito_desc_ita = models.CharField(db_column='AMBITO_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ambito_desc_eng = models.CharField(db_column='AMBITO_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.
    off_did_id = models.IntegerField(db_column='OFF_DID_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        # ~ db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_PDS_ID'
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_PDS'
        unique_together = (('af_pds_id', 'moduli_pds_id', 'erog_id', 'coper_id', 'off_did_id'),)
        ordering = ('ana_mod_desc_ita',)


class DidatticaCds(models.Model):
    cds_id = models.IntegerField(db_column='ID_CDS', primary_key=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nome_cds_it = models.CharField(db_column='CDS_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome_cds_eng = models.CharField(db_column='CDS_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    normativa_cod = models.CharField(db_column='NORMATIVA_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    normativa_desc_ita = models.CharField(db_column='NORMATIVA_DESC_ITA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    dip = models.ForeignKey('structures.DidatticaDipartimento', models.DO_NOTHING, db_column='ID_DIP', to_field='dip_id', blank=True, null=True)  # Field name made lowercase.
    dip_cod = models.CharField(db_column='DIP_COD', max_length=6, blank=True, null=True)
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DESC_ITA', max_length=80, blank=True, null=True)  # Field name made lowercase.
    durata_anni = models.IntegerField(db_column='DURATA_ANNI', blank=True, null=True)  # Field name made lowercase. 
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cla_m_id = models.ForeignKey('DidatticaClasseLaurea', models.DO_NOTHING, db_column='ID_CLASSE_MIUR', blank=True, null=True)  # Field name made lowercase.
    cla_miur_cod = models.CharField(db_column='CLASSE_MIUR_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cla_miur_des = models.CharField(db_column='CLASSE_MIUR_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    intercla_m_id = models.IntegerField(db_column='ID_INTERCLASSE_MIUR', blank=True, null=True)  # Field name made lowercase.
    intercla_miur_cod = models.CharField(db_column='INTERCLASSE_MIUR_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    intercla_miur_des = models.CharField(db_column='INTERCLASSE_MIUR_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codicione = models.CharField(db_column='CODICIONE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flg_exp_seg_stu = models.IntegerField(db_column='FLG_EXP_SEG_STU', blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='ORD_ID', unique=True, blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='ORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_ORD_COD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    area_cds = models.CharField(db_column='AREA_CDS', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    area_cds_en = models.CharField(db_column='AREA_CDS_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = "DIDATTICA_CDS"
        verbose_name = "Cds"
        verbose_name_plural = verbose_name

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cds_cod, self.nome_cds_it)


class DidatticaCdsPeriodi(models.Model):
    ciclo_id = models.IntegerField(db_column="PERIODO_DIDATTICO_ID", primary_key=True)
    aa_id = models.IntegerField(db_column="AA_OFF_ID")
    cds_id = models.IntegerField(db_column="ID_CDS")
    cds_cod = models.CharField(db_column="CDS_COD", max_length=10)
    # ~ rag_tipi_ciclo_cod = models.CharField(db_column="RAG_TIPI_CICLO_COD", max_length=5)
    rag_tipi_ciclo_des = models.CharField(
        db_column="RAGGR_TIPI_PRIODO_DESC_ITA", max_length=40, blank=True, null=True
    )
    rag_tipi_ciclo_des_eng = models.CharField(
        db_column="RAGGR_TIPI_PRIODO_DESC_ENG", max_length=40, blank=True, null=True
    )
    tipo_ciclo_cod = models.CharField(db_column="TIPO_PERIODO_DID_COD", max_length=5)
    tipo_ciclo_des = models.CharField(db_column="TIPO_PERIODO_DID_DESC_ITA", max_length=40)
    # ~ tipo_ciclo_des_eng = models.CharField(
        # ~ db_column="TIPO_CICLO_DES_ENG", max_length=4000, blank=True, null=True
    # ~ )
    # ~ org_did_sua_cod = models.IntegerField(
        # ~ db_column="ORG_DID_SUA_COD", blank=True, null=True
    # ~ )
    # ~ ciclo_des = models.CharField(db_column="CICLO_DES", max_length=40)
    data_inizio = models.DateField(db_column="DATA_INIZIO_PERIODO")
    data_fine = models.DateField(db_column="DATA_FINE_PERIODO")
    # ~ durata = models.DecimalField(
        # ~ db_column="DURATA", max_digits=6, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ csa_cod = models.CharField(db_column="CSA_COD", max_length=2, blank=True, null=True)
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
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
        managed = False
        db_table = "DIDATTICA_CDS_ALTRI_DATI_UFFICIO"
        ordering = ("ordine",)
        # unique_together = (('cds', 'ordine'),)
        verbose_name = "Cds office other data"
        verbose_name_plural = verbose_name


class DidatticaCdsLingua(models.Model):
    # ~ id = models.AutoField(db_column="ID", primary_key=True)
    # ~ lin_did_ord_id = models.IntegerField(db_column="LIN_DID_ORD_ID", primary_key=True)
    cdsord = models.ForeignKey(
        DidatticaCds,
        models.DO_NOTHING,
        db_column="ORD_ID",
        # ~ blank=True,
        # ~ null=True,
        to_field="cdsord_id",
        related_name="didatticacdslingua",
        primary_key=True
    )
    # ~ lingua_id = models.IntegerField(db_column="LINGUA_ID", blank=True, null=True)
    lingua_des_it = models.CharField(
        db_column="LINGUA_DESC_ITA", max_length=100, blank=True, null=True
    )
    iso6392_cod = models.CharField(
        db_column="LINGUA_COD", max_length=3, blank=True, null=True
    )
    lingua_des_eng = models.CharField(
        db_column="LINGUA_DESC_ENG", max_length=100, blank=True, null=True
    )
    dt_ins_mod = models.DateField(db_column="DT_INS_MOD", blank=True, null=True)
    
    class Meta:
        managed = False
        # ~ db_table = "DIDATTICA_CDS_LINGUA_ID"
        db_table = "DIDATTICA_CDS_LINGUA"
        verbose_name = "Cds language"
        verbose_name_plural = "Cds languages"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cdsord.cds_cod, self.lingua_des_it)


class DidatticaCopertura(models.Model):
    coper_id = models.IntegerField(db_column='COPER_ID', primary_key=True)  # Field name made lowercase.
    erog = models.ForeignKey('DidatticaAttivitaFormativaErogata', models.DO_NOTHING, db_column='EROG_ID', blank=True, null=True, related_name="coperture")  # Field name made lowercase.
    tipo_coper_cod = models.CharField(db_column='TIPO_COPER_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_coper_desc_ita = models.CharField(db_column='TIPO_COPER_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_coper_desc_eng = models.CharField(db_column='TIPO_COPER_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_inc_cod = models.CharField(db_column='TIPO_INC_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_inc_desc_ita = models.CharField(db_column='TIPO_INC_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_inc_desc_eng = models.CharField(db_column='TIPO_INC_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rag_tipi_coper_cod = models.CharField(db_column='RAG_TIPI_COPER_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rag_tipi_coper_desc_ita = models.CharField(db_column='RAG_TIPI_COPER_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rag_tipi_coper_desc_eng = models.CharField(db_column='RAG_TIPI_COPER_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_coper_cod = models.CharField(db_column='STATO_COPER_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stato_coper_desc_ita = models.CharField(db_column='STATO_COPER_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_coper_desc_eng = models.CharField(db_column='STATO_COPER_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_docente_responsabile = models.CharField(db_column='FLAG_DOCENTE_RESPONSABILE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_copresenza = models.CharField(db_column='FLAG_COPRESENZA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_inizio_att_dida = models.DateField(db_column='DATA_INIZIO_ATT_DIDA', blank=True, null=True)  # Field name made lowercase.
    data_fine_att_dida = models.DateField(db_column='DATA_FINE_ATT_DIDA', blank=True, null=True)  # Field name made lowercase.
    data_inizio_incarico_dida = models.DateField(db_column='DATA_INIZIO_INCARICO_DIDA', blank=True, null=True)  # Field name made lowercase.
    data_fine_incarico_dida = models.DateField(db_column='DATA_FINE_INCARICO_DIDA', blank=True, null=True)  # Field name made lowercase.
    data_rinuncia = models.DateField(db_column='DATA_RINUNCIA', blank=True, null=True)  # Field name made lowercase.
    data_conferimento_incarico = models.DateField(db_column='DATA_CONFERIMENTO_INCARICO', blank=True, null=True)  # Field name made lowercase.
    data_inizio_contratto = models.DateField(db_column='DATA_INIZIO_CONTRATTO', blank=True, null=True)  # Field name made lowercase.
    data_fine_contratto = models.DateField(db_column='DATA_FINE_CONTRATTO', blank=True, null=True)  # Field name made lowercase.
    doc_id_ab = models.ForeignKey('addressbook.Personale', on_delete=models.DO_NOTHING, db_column='DOC_ID_AB', to_field='id_ab', blank=True, null=True)  # Field name made lowercase.
    doc_matricola = models.CharField(db_column='DOC_MATRICOLA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    doc_cognome = models.CharField(db_column='DOC_COGNOME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    doc_nome = models.CharField(db_column='DOC_NOME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    compenso = models.DecimalField(db_column='COMPENSO', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    compenso_effettivo = models.DecimalField(db_column='COMPENSO_EFFETTIVO', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ore = models.DecimalField(db_column='ORE', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cfu = models.IntegerField(db_column='CFU', blank=True, null=True)  # Field name made lowercase.
    doc_tipo_impegno = models.CharField(db_column='DOC_TIPO_IMPEGNO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_emittente_desc_ita = models.CharField(db_column='TIPO_EMITTENTE_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_emittente_desc_eng = models.CharField(db_column='TIPO_EMITTENTE_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_atto_cod = models.CharField(db_column='TIPO_ATTO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_atto_desc_ita = models.CharField(db_column='TIPO_ATTO_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_atto_desc_eng = models.CharField(db_column='TIPO_ATTO_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_emittente_cod = models.CharField(db_column='TIPO_EMITTENTE_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    motivo_atto_cod = models.CharField(db_column='MOTIVO_ATTO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    motivo_atto_desc_ita = models.CharField(db_column='MOTIVO_ATTO_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    motivo_atto_desc_eng = models.CharField(db_column='MOTIVO_ATTO_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_atto = models.CharField(db_column='NUMERO_ATTO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    data_atto = models.DateField(db_column='DATA_ATTO', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DIDATTICA_COPERTURA"
        verbose_name = "Teaching coverage"
        verbose_name_plural = "Teaching coverages"


class DidatticaCoperturaDettaglioOre(models.Model):
    ore_coper_id = models.IntegerField(db_column='ORE_COPER_ID', primary_key=True)  # Field name made lowercase.
    coper = models.ForeignKey(DidatticaCopertura, models.DO_NOTHING, db_column='COPER_ID', related_name="dettaglio_ore")  # Field name made lowercase.
    tipo_att_did_cod = models.CharField(db_column='TIPO_ATT_DID_COD', max_length=10)  # Field name made lowercase.
    ore = models.DecimalField(db_column='ORE', max_digits=6, decimal_places=2)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DIDATTICA_COPERTURA_DETTAGLIO_ORE"
        verbose_name = "Teaching coverage hours detail"
        verbose_name_plural = "Teaching coverage hours details"


class DidatticaPdsRegolamento(models.Model):
    pds_regdid_id = models.IntegerField(db_column="PDS_REGDID_ID", primary_key=True)
    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=30, blank=True, null=True
    )
    pds_des_it = models.CharField(
        db_column="PDS_DESC_ITA", max_length=255, blank=True, null=True
    )
    pds_des_eng = models.CharField(
        db_column="PDS_DESC_ENG", max_length=2000, blank=True, null=True
    )
    comune_flg = models.CharField(db_column="FLAG_COMUNE", max_length=2, blank=True, null=True)
    valore_min = models.IntegerField(db_column="VALORE_MIN", blank=True, null=True)
    regdid = models.ForeignKey(
        "DidatticaRegolamento",
        models.DO_NOTHING,
        db_column="REGDID_ID",
        blank=True,
        null=True,
    )
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DIDATTICA_PDS_REGOLAMENTO"
        verbose_name = "Academic pathway"
        verbose_name_plural = "Academic pathways"


class DidatticaRegolamento(models.Model):
    regdid_id = models.IntegerField(db_column="REGDID_ID", primary_key=True)
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=10, blank=True, null=True)
    aa_reg_did = models.IntegerField(db_column="AA_ATT_ID", blank=True, null=True)
    cds = models.ForeignKey(
        DidatticaCds, models.DO_NOTHING, db_column="ID_CDS", blank=True, null=True
    )
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stato_regdid_cod = models.CharField(
        db_column="STATO_REGDID_COD", max_length=5, blank=True, null=True
    )
    stato_regdid_des = models.CharField(
        db_column="STATO_REGDID_DESC_ITA", max_length=40, blank=True, null=True
    )
    modalita_erogazione = models.CharField(
        db_column="MOD_DID_DESC_ITA", max_length=100, blank=True, null=True
    )
    frequenza_obbligatoria = models.IntegerField(
        db_column="FREQUENZA_OBBLIGATORIA", blank=True, null=True
    )
    titolo_congiunto_cod = models.CharField(
        db_column="TITOLO_CONGIUNTO", max_length=100, blank=True, null=True
    )
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
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
        managed = False
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
        managed = False
        db_table = "DIDATTICA_REGOLAMENTO_ALTRI_DATI"
        verbose_name = "Didactic regulation other data"
        verbose_name_plural = "Didactic regulation other data"


class DidatticaTestiAfErogata(models.Model):
    syll_inc_doc_id = models.IntegerField(db_column='SYLL_INC_DOC_ID', primary_key=True)  # Field name made lowercase. The composite primary key (SYLL_INC_DOC_ID, EROG_ID, CAMPO_COD) found, that is not supported. The first column is selected.
    erog_id = models.ForeignKey('DidatticaAttivitaFormativaErogata', on_delete=models.DO_NOTHING, db_column='EROG_ID', null=True, blank=True, related_name="testi")  # Field name made lowercase.
    campo_cod = models.CharField(db_column='CAMPO_COD', max_length=100, db_collation='utf8mb4_unicode_ci')  # Field name made lowercase.
    campo_etic_ita = models.CharField(db_column='CAMPO_ETIC_ITA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    campo_etic_eng = models.CharField(db_column='CAMPO_ETIC_ENG', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    campo_desc_ita = models.CharField(db_column='CAMPO_DESC_ITA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    campo_desc_eng = models.CharField(db_column='CAMPO_DESC_ENG', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    testo_fmt_ita = models.TextField(db_column='TESTO_FMT_ITA', blank=True, null=True)  # Field name made lowercase.
    testo_fmt_eng = models.TextField(db_column='TESTO_FMT_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_TESTI_AF_EROGATA'
        unique_together = (('syll_inc_doc_id', 'erog_id', 'campo_cod'),)
        verbose_name = "Study activity text"
        verbose_name_plural = "Study activity texts"


class DidatticaTestiRegolamento(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    regdid = models.ForeignKey(
        DidatticaRegolamento, models.DO_NOTHING, db_column="REGDID_ID"
    )
    tipo_testo_regdid_cod = models.CharField(
        db_column="TIPO_TESTO_REG_COD", max_length=100
    )
    tipo_testo_regdid_des = models.CharField(
        db_column="TIPO_TESTO_REG_DESC_ITA", max_length=255, blank=True, null=True
    )
    clob_txt_ita = models.TextField(db_column="TESTO_ITA", blank=True, null=True)

    clob_txt_eng = models.TextField(db_column="TESTO_ENG", blank=True, null=True)
    dt_ins_mod = models.DateTimeField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DIDATTICA_TESTI_REGOLAMENTO_ID"
        verbose_name = "Didactic regulation text"
        verbose_name_plural = "Didactic regulation texts"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.regdid, self.tipo_testo_regdid_cod)


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
        managed = False
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
        managed = False
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
        managed = False
        db_table = "DIDATTICA_CDS_GRUPPI_COMPONENTI"
        ordering = ("ordine",)
        verbose_name = "Cds group member"
        verbose_name_plural = "Cds group members"

    def __str__(self):  # pragma: no cover
        return f"{self.didattica_cds_gruppi} - {self.cognome} {self.nome}"


class DidatticaClasseLaurea(models.Model):
    cla_m_id = models.IntegerField(db_column="ID_CLASSE_MIUR", primary_key=True)
    cla_miur_cod = models.CharField(db_column="CLASSE_MIUR_COD", max_length=20)
    cla_miur_des = models.CharField(db_column="CLASSE_MIUR_DESC_ITA", max_length=1000)

    class Meta:
        managed = False
        db_table = "DIDATTICA_CLASSE_LAUREA"
        verbose_name = "Classe laurea"
        verbose_name_plural = "Classi laurea"


class DidatticaAmbiti(models.Model):
    amb_id = models.IntegerField(db_column="ID_AMBITO", primary_key=True)
    des = models.CharField(db_column="AMBITO_DESC_ITA", max_length=255, blank=True, null=True)
    des_eng = models.CharField(db_column="AMBITO_DESC_ENG", max_length=255, blank=True, null=True)
    prg_ord_amb = models.IntegerField(db_column="PRG_ORD_AMB", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_INS_MOD", blank=True, null=True)
    # ~ amb_sede_flg = models.IntegerField(db_column="AMB_SEDE_FLG", blank=True, null=True)
    # ~ sys_flg = models.IntegerField(db_column="SYS_FLG", blank=True, null=True)
    # ~ amb_aggr_flg = models.IntegerField(db_column="AMB_AGGR_FLG", blank=True, null=True)
    # ~ dt_ins = models.DateField(db_column="DT_INS_MOD", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "DIDATTICA_AMBITI"
        verbose_name = "Scope"
        verbose_name_plural = "Scopes"


# ~ class DidatticaPianoRegolamento(models.Model):
    # ~ regpiani_id = models.IntegerField(db_column="REGPIANI_ID", primary_key=True)
    # ~ regdid = models.ForeignKey(
        # ~ "DidatticaRegolamento",
        # ~ models.DO_NOTHING,
        # ~ db_column="REGDID_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ attinenza_cod = models.CharField(
        # ~ db_column="ATTINENZA_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ cod = models.CharField(db_column="COD", max_length=10, blank=True, null=True)
    # ~ aa_coorte_id = models.IntegerField(db_column="AA_COORTE_ID", blank=True, null=True)
    # ~ aa_regpiani_id = models.IntegerField(
        # ~ db_column="AA_REGPIANI_ID", blank=True, null=True
    # ~ )
    # ~ des = models.CharField(db_column="DES", max_length=255, blank=True, null=True)
    # ~ def_flg = models.IntegerField(db_column="DEF_FLG", blank=True, null=True)
    # ~ stato_cod = models.CharField(
        # ~ db_column="STATO_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ stato_des = models.CharField(
        # ~ db_column="STATO_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ regpiani_pdr_id = models.IntegerField(
        # ~ db_column="REGPIANI_PDR_ID", blank=True, null=True
    # ~ )
    # ~ regpiani_pdr_cod = models.CharField(
        # ~ db_column="REGPIANI_PDR_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ regpiani_pdr_des = models.CharField(
        # ~ db_column="REGPIANI_PDR_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ regpiani_pdr_aa_coorte_id = models.IntegerField(
        # ~ db_column="REGPIANI_PDR_AA_COORTE_ID", blank=True, null=True
    # ~ )
    # ~ regpiani_pdr_aa_regpiani_id = models.IntegerField(
        # ~ db_column="REGPIANI_PDR_AA_REGPIANI_ID", blank=True, null=True
    # ~ )
    # ~ flg_exp_seg_stu = models.IntegerField(
        # ~ db_column="FLG_EXP_SEG_STU", blank=True, null=True
    # ~ )
    # ~ data_exp_seg_stu = models.DateField(
        # ~ db_column="DATA_EXP_SEG_STU", blank=True, null=True
    # ~ )
    # ~ nota = models.CharField(db_column="NOTA", max_length=1000, blank=True, null=True)

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_REGOLAMENTO"
        # ~ verbose_name = "Regulation study plan"
        # ~ verbose_name_plural = "Regulation study plans"


# ~ class DidatticaPianoSceltaAf(models.Model):
    # ~ sce_af_id = models.IntegerField(db_column="SCE_AF_ID", primary_key=True)
    # ~ sce = models.ForeignKey(
        # ~ "DidatticaPianoSceltaVincoli",
        # ~ models.DO_NOTHING,
        # ~ db_column="SCE_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ pds_regdid = models.ForeignKey(
        # ~ DidatticaPdsRegolamento,
        # ~ models.DO_NOTHING,
        # ~ db_column="PDS_REGDID_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ pds_cod = models.CharField(
        # ~ db_column="PDS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ pds_des = models.CharField(
        # ~ db_column="PDS_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ sce_blk_id = models.IntegerField(db_column="SCE_BLK_ID", blank=True, null=True)
    # ~ min_unt_blk = models.DecimalField(
        # ~ db_column="MIN_UNT_BLK", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ max_unt_blk = models.DecimalField(
        # ~ db_column="MAX_UNT_BLK", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ lingua_id = models.IntegerField(db_column="LINGUA_ID", blank=True, null=True)
    # ~ blk_prg = models.IntegerField(db_column="BLK_PRG", blank=True, null=True)
    # ~ lingua_iso6392_cod = models.CharField(
        # ~ db_column="LINGUA_ISO6392_COD", max_length=3, blank=True, null=True
    # ~ )
    # ~ lingua_des = models.CharField(
        # ~ db_column="LINGUA_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ lingua_num = models.IntegerField(db_column="LINGUA_NUM", blank=True, null=True)
    # ~ af = models.ForeignKey(
        # ~ DidatticaAttivitaFormativa,
        # ~ models.DO_NOTHING,
        # ~ db_column="AF_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ regud_des_auto = models.CharField(
        # ~ db_column="REGUD_DES_AUTO", max_length=1000, blank=True, null=True
    # ~ )
    # ~ regud_des_ute = models.CharField(
        # ~ db_column="REGUD_DES_UTE", max_length=1000, blank=True, null=True
    # ~ )
    # ~ min_unt_af = models.DecimalField(
        # ~ db_column="MIN_UNT_AF", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ max_unt_af = models.DecimalField(
        # ~ db_column="MAX_UNT_AF", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ statutario_flg = models.IntegerField(
        # ~ db_column="STATUTARIO_FLG", blank=True, null=True
    # ~ )
    # ~ def_verifica_flg = models.IntegerField(
        # ~ db_column="DEF_VERIFICA_FLG", blank=True, null=True
    # ~ )
    # ~ contr_aa_off_flg = models.IntegerField(
        # ~ db_column="CONTR_AA_OFF_FLG", blank=True, null=True
    # ~ )
    # ~ regdid_af_id = models.IntegerField(db_column="REGDID_AF_ID", blank=True, null=True)
    # ~ pds_regdid_af_id = models.IntegerField(
        # ~ db_column="PDS_REGDID_AF_ID", blank=True, null=True
    # ~ )
    # ~ pds_af_cod = models.CharField(
        # ~ db_column="PDS_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ pds_af_des = models.CharField(
        # ~ db_column="PDS_AF_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ comune_af_flg = models.IntegerField(
        # ~ db_column="COMUNE_AF_FLG", blank=True, null=True
    # ~ )
    # ~ attinenza_af_cod = models.CharField(
        # ~ db_column="ATTINENZA_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ of_id = models.IntegerField(db_column="OF_ID", blank=True, null=True)
    # ~ cds_af_id = models.IntegerField(db_column="CDS_AF_ID", blank=True, null=True)
    # ~ cds_af_cod = models.CharField(
        # ~ db_column="CDS_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ nome_af_cds = models.CharField(
        # ~ db_column="NOME_AF_CDS", max_length=255, blank=True, null=True
    # ~ )
    # ~ cdsord_af_cod = models.CharField(
        # ~ db_column="CDSORD_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ aa_off_id = models.IntegerField(db_column="AA_OFF_ID", blank=True, null=True)
    # ~ stato_of_cod = models.CharField(
        # ~ db_column="STATO_OF_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_comp_af_id = models.IntegerField(
        # ~ db_column="TIPO_COMP_AF_ID", blank=True, null=True
    # ~ )
    # ~ tipo_comp_af_cod = models.CharField(
        # ~ db_column="TIPO_COMP_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ des_tipo_comp_af = models.CharField(
        # ~ db_column="DES_TIPO_COMP_AF", max_length=255, blank=True, null=True
    # ~ )
    # ~ af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    # ~ af_gen_cod = models.CharField(
        # ~ db_column="AF_GEN_COD", max_length=20, blank=True, null=True
    # ~ )
    # ~ af_gen_des = models.CharField(
        # ~ db_column="AF_GEN_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ anno_corso_af = models.IntegerField(
        # ~ db_column="ANNO_CORSO_AF", blank=True, null=True
    # ~ )
    # ~ lista_anni_corso_af = models.CharField(
        # ~ db_column="LISTA_ANNI_CORSO_AF", max_length=20, blank=True, null=True
    # ~ )
    # ~ af_regdid_id = models.IntegerField(db_column="AF_REGDID_ID", blank=True, null=True)
    # ~ sett_cod = models.CharField(
        # ~ db_column="SETT_COD", max_length=12, blank=True, null=True
    # ~ )
    # ~ tipo_af_cod_af = models.CharField(
        # ~ db_column="TIPO_AF_COD_AF", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_af_des_af = models.CharField(
        # ~ db_column="TIPO_AF_DES_AF", max_length=80, blank=True, null=True
    # ~ )
    # ~ amb_id_af = models.ForeignKey(
        # ~ DidatticaAmbiti, models.DO_NOTHING, db_column="AMB_ID_AF", blank=True, null=True
    # ~ )
    # ~ ambito_des_af = models.CharField(
        # ~ db_column="AMBITO_DES_AF", max_length=255, blank=True, null=True
    # ~ )
    # ~ tipo_af_intercla_cod_af = models.CharField(
        # ~ db_column="TIPO_AF_INTERCLA_COD_AF", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_af_intercla_des_af = models.CharField(
        # ~ db_column="TIPO_AF_INTERCLA_DES_AF", max_length=80, blank=True, null=True
    # ~ )
    # ~ amb_intercla_id_af = models.IntegerField(
        # ~ db_column="AMB_INTERCLA_ID_AF", blank=True, null=True
    # ~ )
    # ~ ambito_intercla_des_af = models.CharField(
        # ~ db_column="AMBITO_INTERCLA_DES_AF", max_length=255, blank=True, null=True
    # ~ )
    # ~ peso = models.DecimalField(
        # ~ db_column="PESO", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ peso_foglie_non_log = models.DecimalField(
        # ~ db_column="PESO_FOGLIE_NON_LOG",
        # ~ max_digits=5,
        # ~ decimal_places=2,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_max_reit = models.IntegerField(db_column="NUM_MAX_REIT", blank=True, null=True)
    # ~ non_erogabile_flg = models.IntegerField(
        # ~ db_column="NON_EROGABILE_FLG", blank=True, null=True
    # ~ )
    # ~ livello_af_cod = models.CharField(
        # ~ db_column="LIVELLO_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ livello_af_des = models.CharField(
        # ~ db_column="LIVELLO_AF_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ tipo_esa_cod = models.CharField(
        # ~ db_column="TIPO_ESA_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_esa_des = models.CharField(
        # ~ db_column="TIPO_ESA_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ tipo_val_cod = models.CharField(
        # ~ db_column="TIPO_VAL_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_val_des = models.CharField(
        # ~ db_column="TIPO_VAL_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ af_pdr_id = models.IntegerField(db_column="AF_PDR_ID", blank=True, null=True)
    # ~ af_radice_id = models.IntegerField(db_column="AF_RADICE_ID", blank=True, null=True)
    # ~ num_liv_albero = models.IntegerField(
        # ~ db_column="NUM_LIV_ALBERO", blank=True, null=True
    # ~ )
    # ~ ciclo_id = models.IntegerField(db_column="CICLO_ID", blank=True, null=True)
    # ~ ciclo_des = models.CharField(
        # ~ db_column="CICLO_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ tipo_ciclo_cod = models.CharField(
        # ~ db_column="TIPO_CICLO_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ des_tipo_ciclo = models.CharField(
        # ~ db_column="DES_TIPO_CICLO", max_length=40, blank=True, null=True
    # ~ )
    # ~ org_did_sua_cod = models.IntegerField(
        # ~ db_column="ORG_DID_SUA_COD", blank=True, null=True
    # ~ )
    # ~ sede_id = models.IntegerField(db_column="SEDE_ID", blank=True, null=True)
    # ~ sede_des = models.CharField(
        # ~ db_column="SEDE_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ tipo_rag_cod = models.CharField(
        # ~ db_column="TIPO_RAG_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_rag_des = models.CharField(
        # ~ db_column="TIPO_RAG_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ af_capogruppo_id = models.IntegerField(
        # ~ db_column="AF_CAPOGRUPPO_ID", blank=True, null=True
    # ~ )
    # ~ scelta_mod_flg = models.IntegerField(
        # ~ db_column="SCELTA_MOD_FLG", blank=True, null=True
    # ~ )
    # ~ num_regud = models.DecimalField(
        # ~ db_column="NUM_REGUD", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_SCELTA_AF"
        # ~ ordering = ("ciclo_des",)
        # ~ verbose_name = "Study plan study activity choice"
        # ~ verbose_name_plural = "Study plan study activity choices"


# ~ class DidatticaPianoSceltaFilAnd(models.Model):
    # ~ sce_fil_and_id = models.IntegerField(db_column="SCE_FIL_AND_ID", primary_key=True)
    # ~ sce = models.ForeignKey(
        # ~ "DidatticaPianoSceltaVincoli",
        # ~ models.DO_NOTHING,
        # ~ db_column="SCE_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ sce_fil_or_id = models.IntegerField(
        # ~ db_column="SCE_FIL_OR_ID", blank=True, null=True
    # ~ )
    # ~ sce_fil_or_des = models.CharField(
        # ~ db_column="SCE_FIL_OR_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ tipo_filtro_cod = models.CharField(
        # ~ db_column="TIPO_FILTRO_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_filtro_des = models.CharField(
        # ~ db_column="TIPO_FILTRO_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ af_gen_id = models.IntegerField(db_column="AF_GEN_ID", blank=True, null=True)
    # ~ af_gen_cod = models.CharField(
        # ~ db_column="AF_GEN_COD", max_length=20, blank=True, null=True
    # ~ )
    # ~ af_gen_des = models.CharField(
        # ~ db_column="AF_GEN_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ dip_sce_fil_and_id = models.IntegerField(
        # ~ db_column="DIP_SCE_FIL_AND_ID", blank=True, null=True
    # ~ )
    # ~ dip_sce_fil_and_cod = models.CharField(
        # ~ db_column="DIP_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ dip_sce_fil_and_des = models.CharField(
        # ~ db_column="DIP_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ strac_sce_fil_and_id = models.IntegerField(
        # ~ db_column="STRAC_SCE_FIL_AND_ID", blank=True, null=True
    # ~ )
    # ~ strac_sce_fil_and_cod = models.CharField(
        # ~ db_column="STRAC_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ strac_sce_fil_and_des = models.CharField(
        # ~ db_column="STRAC_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ cds_sce_fil_and_id = models.IntegerField(
        # ~ db_column="CDS_SCE_FIL_AND_ID", blank=True, null=True
    # ~ )
    # ~ cds_sce_fil_and_cod = models.CharField(
        # ~ db_column="CDS_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ cds_sce_fil_and_nome = models.CharField(
        # ~ db_column="CDS_SCE_FIL_AND_NOME", max_length=255, blank=True, null=True
    # ~ )
    # ~ cfu = models.DecimalField(
        # ~ db_column="CFU", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ tipo_af_sce_fil_and_cod = models.CharField(
        # ~ db_column="TIPO_AF_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_af_sce_fil_and_des = models.CharField(
        # ~ db_column="TIPO_AF_SCE_FIL_AND_DES", max_length=80, blank=True, null=True
    # ~ )
    # ~ sett_cod = models.CharField(
        # ~ db_column="SETT_COD", max_length=12, blank=True, null=True
    # ~ )
    # ~ tipo_corso_sce_fil_and_cod = models.CharField(
        # ~ db_column="TIPO_CORSO_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ cla_miur_sce_fil_and_id = models.IntegerField(
        # ~ db_column="CLA_MIUR_SCE_FIL_AND_ID", blank=True, null=True
    # ~ )
    # ~ cla_miur_sce_fil_and_cod = models.CharField(
        # ~ db_column="CLA_MIUR_SCE_FIL_AND_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ cla_miur_sce_fil_and_des = models.CharField(
        # ~ db_column="CLA_MIUR_SCE_FIL_AND_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ rif_cod = models.CharField(
        # ~ db_column="RIF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ sett_post_rif_flg = models.IntegerField(
        # ~ db_column="SETT_POST_RIF_FLG", blank=True, null=True
    # ~ )
    # ~ tipo_ins_cod = models.CharField(
        # ~ db_column="TIPO_INS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ peso_sce_fil_and = models.IntegerField(
        # ~ db_column="PESO_SCE_FIL_AND", blank=True, null=True
    # ~ )
    # ~ not_flg = models.IntegerField(db_column="NOT_FLG", blank=True, null=True)

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_SCELTA_FIL_AND"
        # ~ verbose_name = "Study plan choice filter"
        # ~ verbose_name_plural = "Study plan choice filters"


# ~ class DidatticaPianoSceltaSchePiano(models.Model):
    # ~ sche_piano = models.OneToOneField(
        # ~ "DidatticaPianoSche",
        # ~ models.DO_NOTHING,
        # ~ db_column="SCHE_PIANO_ID",
        # ~ primary_key=True,
        # ~ related_name="didatticapianosceltaschepiano"
    # ~ )
    # ~ sche_statutario_flg = models.BooleanField(
        # ~ db_column="SCHE_STATUTARIO_FLG", default=False
    # ~ )
    # ~ sche_pds_regdid_id = models.IntegerField(
        # ~ db_column="SCHE_PDS_REGDID_ID", blank=True, null=True
    # ~ )
    # ~ sche_pds_cod = models.CharField(
        # ~ db_column="SCHE_PDS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ sche_pds_des = models.CharField(
        # ~ db_column="SCHE_PDS_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ sche_ori_id = models.IntegerField(db_column="SCHE_ORI_ID", blank=True, null=True)
    # ~ sche_cla_m_id = models.IntegerField(
        # ~ db_column="SCHE_CLA_M_ID", blank=True, null=True
    # ~ )
    # ~ sche_apt_id = models.IntegerField(db_column="SCHE_APT_ID", blank=True, null=True)
    # ~ sche_nota = models.CharField(
        # ~ db_column="SCHE_NOTA", max_length=1000, blank=True, null=True
    # ~ )
    # ~ data_ini_val = models.DateField(db_column="DATA_INI_VAL", blank=True, null=True)
    # ~ data_fine_val = models.DateField(db_column="DATA_FINE_VAL", blank=True, null=True)
    # ~ stato_piano_gen_cod = models.CharField(
        # ~ db_column="STATO_PIANO_GEN_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ contr_ac_piano_stu_cod = models.CharField(
        # ~ db_column="CONTR_AC_PIANO_STU_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ blocco_af_freq_piano_stu_flg = models.IntegerField(
        # ~ db_column="BLOCCO_AF_FREQ_PIANO_STU_FLG", blank=True, null=True
    # ~ )
    # ~ sce = models.ForeignKey(
        # ~ "DidatticaPianoSceltaVincoli", models.DO_NOTHING, db_column="SCE_ID"
    # ~ )
    # ~ ord_num = models.IntegerField(db_column="ORD_NUM", blank=True, null=True)
    # ~ apt_slot_id = models.IntegerField(db_column="APT_SLOT_ID", blank=True, null=True)
    # ~ apt_slot_cod = models.CharField(
        # ~ db_column="APT_SLOT_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ apt_slot_des = models.CharField(
        # ~ db_column="APT_SLOT_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ apt_slot_anno_corso = models.IntegerField(
        # ~ db_column="APT_SLOT_ANNO_CORSO", blank=True, null=True
    # ~ )
    # ~ apt_slot_ord_num = models.IntegerField(
        # ~ db_column="APT_SLOT_ORD_NUM", blank=True, null=True
    # ~ )
    # ~ sce_des = models.CharField(
        # ~ db_column="SCE_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ pds_regdid_id = models.IntegerField(
        # ~ db_column="PDS_REGDID_ID", blank=True, null=True
    # ~ )
    # ~ pds_cod = models.CharField(
        # ~ db_column="PDS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ pds_des = models.CharField(
        # ~ db_column="PDS_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    # ~ anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    # ~ anno_corso_ant = models.IntegerField(
        # ~ db_column="ANNO_CORSO_ANT", blank=True, null=True
    # ~ )
    # ~ tipo_regsce_cod = models.CharField(
        # ~ db_column="TIPO_REGSCE_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_sce_cod = models.CharField(
        # ~ db_column="TIPO_SCE_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_sce_des = models.CharField(
        # ~ db_column="TIPO_SCE_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ tipo_regsce_des = models.CharField(
        # ~ db_column="TIPO_REGSCE_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ tipo_um_regsce_cod = models.CharField(
        # ~ db_column="TIPO_UM_REGSCE_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ opz_flg = models.IntegerField(db_column="OPZ_FLG", blank=True, null=True)
    # ~ min_unt = models.DecimalField(
        # ~ db_column="MIN_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ max_unt = models.DecimalField(
        # ~ db_column="MAX_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ livello = models.IntegerField(db_column="LIVELLO", blank=True, null=True)
    # ~ vin_id = models.IntegerField(db_column="VIN_ID", blank=True, null=True)
    # ~ vin_ord_num = models.IntegerField(db_column="VIN_ORD_NUM", blank=True, null=True)
    # ~ vin_sce_des = models.CharField(
        # ~ db_column="VIN_SCE_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ tipi_af_tipi_sce_id = models.IntegerField(
        # ~ db_column="TIPI_AF_TIPI_SCE_ID", blank=True, null=True
    # ~ )
    # ~ tipo_af_cod = models.CharField(
        # ~ db_column="TIPO_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_af_des = models.CharField(
        # ~ db_column="TIPO_AF_DES", max_length=80, blank=True, null=True
    # ~ )
    # ~ amb = models.ForeignKey(
        # ~ DidatticaAmbiti, models.DO_NOTHING, db_column="AMB_ID", blank=True, null=True
    # ~ )
    # ~ ambito_des = models.CharField(
        # ~ db_column="AMBITO_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ sovran_flg = models.IntegerField(db_column="SOVRAN_FLG", blank=True, null=True)
    # ~ sostegno_flg = models.IntegerField(db_column="SOSTEGNO_FLG", blank=True, null=True)
    # ~ peso_sce = models.IntegerField(db_column="PESO_SCE", blank=True, null=True)
    # ~ tesoretto_flg = models.IntegerField(
        # ~ db_column="TESORETTO_FLG", blank=True, null=True
    # ~ )
    # ~ assegnazione_posti_flg = models.IntegerField(
        # ~ db_column="ASSEGNAZIONE_POSTI_FLG", blank=True, null=True
    # ~ )
    # ~ delibera_flg = models.IntegerField(db_column="DELIBERA_FLG", blank=True, null=True)
    # ~ azzera_cfu_flg = models.IntegerField(
        # ~ db_column="AZZERA_CFU_FLG", blank=True, null=True
    # ~ )
    # ~ parametri_logistica_flg = models.IntegerField(
        # ~ db_column="PARAMETRI_LOGISTICA_FLG", blank=True, null=True
    # ~ )
    # ~ tag_regsce_cod = models.CharField(
        # ~ db_column="TAG_REGSCE_COD", max_length=20, blank=True, null=True
    # ~ )
    # ~ peso_af_sce = models.DecimalField(
        # ~ db_column="PESO_AF_SCE", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ peso_min_singola_af = models.DecimalField(
        # ~ db_column="PESO_MIN_SINGOLA_AF",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ peso_max_singola_af = models.DecimalField(
        # ~ db_column="PESO_MAX_SINGOLA_AF",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_af_sce = models.DecimalField(
        # ~ db_column="NUM_AF_SCE", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ peso_af_sce_stat = models.DecimalField(
        # ~ db_column="PESO_AF_SCE_STAT",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ peso_af_sce_def_verifica = models.DecimalField(
        # ~ db_column="PESO_AF_SCE_DEF_VERIFICA",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_blk = models.DecimalField(
        # ~ db_column="NUM_BLK", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ num_blk_stat = models.DecimalField(
        # ~ db_column="NUM_BLK_STAT", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ num_blk_def_verifica = models.DecimalField(
        # ~ db_column="NUM_BLK_DEF_VERIFICA",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_blk_contr_aa_off = models.DecimalField(
        # ~ db_column="NUM_BLK_CONTR_AA_OFF",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_blk_statutario_flg_div = models.DecimalField(
        # ~ db_column="NUM_BLK_STATUTARIO_FLG_DIV",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_blk_def_verifica_flg_div = models.DecimalField(
        # ~ db_column="NUM_BLK_DEF_VERIFICA_FLG_DIV",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_blk_contr_aa_off_flg_div = models.DecimalField(
        # ~ db_column="NUM_BLK_CONTR_AA_OFF_FLG_DIV",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ peso_blk = models.DecimalField(
        # ~ db_column="PESO_BLK", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ af_stessa_taf_flg = models.DecimalField(
        # ~ db_column="AF_STESSA_TAF_FLG",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ af_stessa_taf_intercla_flg = models.DecimalField(
        # ~ db_column="AF_STESSA_TAF_INTERCLA_FLG",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ af_stesso_ambito_flg = models.DecimalField(
        # ~ db_column="AF_STESSO_AMBITO_FLG",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ af_stesso_ambito_intercla_flg = models.DecimalField(
        # ~ db_column="AF_STESSO_AMBITO_INTERCLA_FLG",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ amb_id_af_regsce = models.DecimalField(
        # ~ db_column="AMB_ID_AF_REGSCE",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ tipo_af_cod_af_regsce = models.CharField(
        # ~ db_column="TIPO_AF_COD_AF_REGSCE", max_length=10, blank=True, null=True
    # ~ )
    # ~ amb_intercla_id_af_regsce = models.DecimalField(
        # ~ db_column="AMB_INTERCLA_ID_AF_REGSCE",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ tipo_af_intercla_cod_af_regsce = models.CharField(
        # ~ db_column="TIPO_AF_INTERCLA_COD_AF_REGSCE", max_length=10, blank=True, null=True
    # ~ )
    # ~ num_af_taf_d = models.DecimalField(
        # ~ db_column="NUM_AF_TAF_D", max_digits=38, decimal_places=0, blank=True, null=True
    # ~ )
    # ~ num_af_taf_intercla_d = models.DecimalField(
        # ~ db_column="NUM_AF_TAF_INTERCLA_D",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_af_taf_e_f_s = models.DecimalField(
        # ~ db_column="NUM_AF_TAF_E_F_S",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ num_af_taf_intercla_e_f_s = models.DecimalField(
        # ~ db_column="NUM_AF_TAF_INTERCLA_E_F_S",
        # ~ max_digits=38,
        # ~ decimal_places=0,
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ sett_cod_af_regsce = models.CharField(
        # ~ db_column="SETT_COD_AF_REGSCE", max_length=12, blank=True, null=True
    # ~ )
    # ~ nota_pre = models.TextField(db_column="NOTA_PRE", blank=True, null=True)
    # ~ nota_pre_vis_web_flg = models.IntegerField(
        # ~ db_column="NOTA_PRE_VIS_WEB_FLG", blank=True, null=True
    # ~ )
    # ~ nota_post = models.TextField(db_column="NOTA_POST", blank=True, null=True)
    # ~ nota_post_vis_web_flg = models.IntegerField(
        # ~ db_column="NOTA_POST_VIS_WEB_FLG", blank=True, null=True
    # ~ )

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_SCELTA_SCHE_PIANO"
        # ~ unique_together = (("sche_piano", "sce"),)
        # ~ verbose_name = "Study plan sheet choice plan"
        # ~ verbose_name_plural = "Study plan sheet choice plans"


# ~ class DidatticaPianoSceltaVincoli(models.Model):
    # ~ sce_id = models.IntegerField(db_column="SCE_ID", primary_key=True)
    # ~ regpiani = models.ForeignKey(
        # ~ DidatticaPianoRegolamento,
        # ~ models.DO_NOTHING,
        # ~ db_column="REGPIANI_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ ord_num = models.IntegerField(db_column="ORD_NUM", blank=True, null=True)
    # ~ sce_des = models.CharField(
        # ~ db_column="SCE_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ pds_regdid = models.ForeignKey(
        # ~ DidatticaPdsRegolamento,
        # ~ models.DO_NOTHING,
        # ~ db_column="PDS_REGDID_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ pds_cod = models.CharField(
        # ~ db_column="PDS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ pds_des = models.CharField(
        # ~ db_column="PDS_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    # ~ anno_corso = models.IntegerField(db_column="ANNO_CORSO", blank=True, null=True)
    # ~ anno_corso_ant = models.IntegerField(
        # ~ db_column="ANNO_CORSO_ANT", blank=True, null=True
    # ~ )
    # ~ tipo_regsce_cod = models.CharField(
        # ~ db_column="TIPO_REGSCE_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_sce_cod = models.CharField(
        # ~ db_column="TIPO_SCE_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ tipo_um_regsce_cod = models.CharField(
        # ~ db_column="TIPO_UM_REGSCE_COD", max_length=5, blank=True, null=True
    # ~ )
    # ~ opz_flg = models.IntegerField(db_column="OPZ_FLG", blank=True, null=True)
    # ~ min_unt = models.DecimalField(
        # ~ db_column="MIN_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ max_unt = models.DecimalField(
        # ~ db_column="MAX_UNT", max_digits=5, decimal_places=2, blank=True, null=True
    # ~ )
    # ~ livello = models.IntegerField(db_column="LIVELLO", blank=True, null=True)
    # ~ vin = models.ForeignKey(
        # ~ "self", models.DO_NOTHING, db_column="VIN_ID", blank=True, null=True
    # ~ )
    # ~ vin_ord_num = models.IntegerField(db_column="VIN_ORD_NUM", blank=True, null=True)
    # ~ vin_sce_des = models.CharField(
        # ~ db_column="VIN_SCE_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ tipi_af_tipi_sce_id = models.IntegerField(
        # ~ db_column="TIPI_AF_TIPI_SCE_ID", blank=True, null=True
    # ~ )
    # ~ tipo_af_cod = models.CharField(
        # ~ db_column="TIPO_AF_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ tipo_af_des = models.CharField(
        # ~ db_column="TIPO_AF_DES", max_length=80, blank=True, null=True
    # ~ )
    # ~ amb_id = models.IntegerField(db_column="AMB_ID", blank=True, null=True)
    # ~ ambito_des = models.CharField(
        # ~ db_column="AMBITO_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ sovran_flg = models.IntegerField(db_column="SOVRAN_FLG", blank=True, null=True)
    # ~ sostegno_flg = models.IntegerField(db_column="SOSTEGNO_FLG", blank=True, null=True)
    # ~ peso_sce = models.IntegerField(db_column="PESO_SCE", blank=True, null=True)
    # ~ tesoretto_flg = models.IntegerField(
        # ~ db_column="TESORETTO_FLG", blank=True, null=True
    # ~ )
    # ~ assegnazione_posti_flg = models.IntegerField(
        # ~ db_column="ASSEGNAZIONE_POSTI_FLG", blank=True, null=True
    # ~ )
    # ~ delibera_flg = models.IntegerField(db_column="DELIBERA_FLG", blank=True, null=True)
    # ~ azzera_cfu_flg = models.IntegerField(
        # ~ db_column="AZZERA_CFU_FLG", blank=True, null=True
    # ~ )
    # ~ parametri_logistica_flg = models.IntegerField(
        # ~ db_column="PARAMETRI_LOGISTICA_FLG", blank=True, null=True
    # ~ )
    # ~ tag_regsce_cod = models.CharField(
        # ~ db_column="TAG_REGSCE_COD", max_length=20, blank=True, null=True
    # ~ )
    # ~ nota_pre = models.TextField(db_column="NOTA_PRE", blank=True, null=True)
    # ~ nota_pre_vis_web_flg = models.IntegerField(
        # ~ db_column="NOTA_PRE_VIS_WEB_FLG", blank=True, null=True
    # ~ )
    # ~ nota_post = models.TextField(db_column="NOTA_POST", blank=True, null=True)
    # ~ nota_post_vis_web_flg = models.IntegerField(
        # ~ db_column="NOTA_POST_VIS_WEB_FLG", blank=True, null=True
    # ~ )

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_SCELTA_VINCOLI"
        # ~ verbose_name = "Study plan constraint choice"
        # ~ verbose_name_plural = "Study plan constraint choices"


# ~ class DidatticaPianoSche(models.Model):
    # ~ sche_piano_id = models.IntegerField(db_column="SCHE_PIANO_ID", primary_key=True)
    # ~ regpiani = models.ForeignKey(
        # ~ DidatticaPianoRegolamento, models.DO_NOTHING, db_column="REGPIANI_ID", related_name="didatticapianosche"
    # ~ )
    # ~ sche_piano_cod = models.CharField(
        # ~ db_column="SCHE_PIANO_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ sche_piano_des = models.CharField(
        # ~ db_column="SCHE_PIANO_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ sche_piano_vis_web_flg = models.IntegerField(
        # ~ db_column="SCHE_PIANO_VIS_WEB_FLG", blank=True, null=True
    # ~ )
    # ~ pds_regdid = models.ForeignKey(
        # ~ DidatticaPdsRegolamento,
        # ~ models.DO_NOTHING,
        # ~ db_column="PDS_REGDID_ID",
        # ~ blank=True,
        # ~ null=True,
    # ~ )
    # ~ pds_cod = models.CharField(
        # ~ db_column="PDS_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ pds_des = models.CharField(
        # ~ db_column="PDS_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ comune_flg = models.IntegerField(db_column="COMUNE_FLG", blank=True, null=True)
    # ~ ori_id = models.IntegerField(db_column="ORI_ID", blank=True, null=True)
    # ~ ori_cod = models.CharField(
        # ~ db_column="ORI_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ ori_des = models.CharField(
        # ~ db_column="ORI_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ cla_m_id = models.IntegerField(db_column="CLA_M_ID", blank=True, null=True)
    # ~ cla_miur_cod = models.CharField(
        # ~ db_column="CLA_MIUR_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ cla_miur_des = models.CharField(
        # ~ db_column="CLA_MIUR_DES", max_length=255, blank=True, null=True
    # ~ )
    # ~ apt_id = models.IntegerField(db_column="APT_ID", blank=True, null=True)
    # ~ apt_cod = models.CharField(
        # ~ db_column="APT_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ apt_des = models.CharField(
        # ~ db_column="APT_DES", max_length=80, blank=True, null=True
    # ~ )
    # ~ data_ini_val = models.DateField(db_column="DATA_INI_VAL", blank=True, null=True)
    # ~ data_fine_val = models.DateField(db_column="DATA_FINE_VAL", blank=True, null=True)
    # ~ stato_piano_gen_cod = models.CharField(
        # ~ db_column="STATO_PIANO_GEN_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ stato_piano_gen_des = models.CharField(
        # ~ db_column="STATO_PIANO_GEN_DES", max_length=40, blank=True, null=True
    # ~ )
    # ~ contr_ac_piano_stu_cod = models.CharField(
        # ~ db_column="CONTR_AC_PIANO_STU_COD", max_length=10, blank=True, null=True
    # ~ )
    # ~ blocco_af_freq_piano_stu_flg = models.IntegerField(
        # ~ db_column="BLOCCO_AF_FREQ_PIANO_STU_FLG", blank=True, null=True
    # ~ )
    # ~ nota_sche_piano = models.CharField(
        # ~ db_column="NOTA_SCHE_PIANO", max_length=1000, blank=True, null=True
    # ~ )
    # ~ sche_piano_des_txt_id = models.IntegerField(
        # ~ db_column="SCHE_PIANO_DES_TXT_ID", blank=True, null=True
    # ~ )

    # ~ class Meta:
        # ~ managed = False
        # ~ db_table = "DIDATTICA_PIANO_SCHE"
        # ~ verbose_name = "Study plan sheet"
        # ~ verbose_name_plural = "Study plan sheets"


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
        managed = False
        db_table = "DIDATTICA_CDS_TIPO_CORSO"
        verbose_name = "Cds course type"
        verbose_name_plural = "Cds course types"


class DidatticaPianiStudio(models.Model):
    piano_studio_id = models.IntegerField(db_column='PIANO_STUDIO_ID', primary_key=True)  # Field name made lowercase.
    piano_studio_cod = models.CharField(db_column='PIANO_STUDIO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    aa_coorte_id = models.IntegerField(db_column='AA_COORTE_ID', blank=True, null=True)  # Field name made lowercase.
    aa_revisione_id = models.IntegerField(db_column='AA_REVISIONE_ID', blank=True, null=True)  # Field name made lowercase.
    stato_piano_studio_cod = models.CharField(db_column='STATO_PIANO_STUDIO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stato_piano_studio_desc_ita = models.CharField(db_column='STATO_PIANO_STUDIO_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_piano_studio_desc_eng = models.CharField(db_column='STATO_PIANO_STUDIO_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PIANI_STUDIO'


class DidatticaPianiSchema(models.Model):
    schema_piano_id = models.IntegerField(db_column='SCHEMA_PIANO_ID', primary_key=True)  # Field name made lowercase.
    piano_studio = models.ForeignKey('DidatticaPianiStudio', models.DO_NOTHING, db_column='PIANO_STUDIO_ID', related_name="schemi")  # Field name made lowercase.
    schema_piano_cod = models.CharField(db_column='SCHEMA_PIANO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schema_piano_desc_ita = models.CharField(db_column='SCHEMA_PIANO_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    schema_piano_desc_eng = models.CharField(db_column='SCHEMA_PIANO_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_schema_visibile_web = models.CharField(db_column='FLAG_SCHEMA_VISIBILE_WEB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey('DidatticaPdsRegolamento', models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    id_classe_miur = models.IntegerField(db_column='ID_CLASSE_MIUR', blank=True, null=True)  # Field name made lowercase.
    classe_miur_cod = models.CharField(db_column='CLASSE_MIUR_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    classe_miur_desc_ita = models.CharField(db_column='CLASSE_MIUR_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classe_miur_desc_eng = models.CharField(db_column='CLASSE_MIUR_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_schema_statutario = models.CharField(db_column='FLAG_SCHEMA_STATUTARIO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alt_part_time_cod = models.CharField(db_column='ALT_PART_TIME_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PIANI_SCHEMA'


class DidatticaPianiRegSce(models.Model):
    reg_sce_id = models.IntegerField(db_column='REG_SCE_ID', primary_key=True)  # Field name made lowercase.
    schema_piano = models.ForeignKey('DidatticaPianiSchema', models.DO_NOTHING, db_column='SCHEMA_PIANO_ID', related_name="regole")  # Field name made lowercase.
    aa_off_id_reg_sce = models.IntegerField(db_column='AA_OFF_ID_REG_SCE', blank=True, null=True)  # Field name made lowercase.
    anno_corso_reg_sce = models.IntegerField(db_column='ANNO_CORSO_REG_SCE', blank=True, null=True)  # Field name made lowercase.
    progressivo_reg_sce = models.IntegerField(db_column='PROGRESSIVO_REG_SCE', blank=True, null=True)  # Field name made lowercase.
    tipo_reg_sce_cod = models.CharField(db_column='TIPO_REG_SCE_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_um_reg_sce_cod = models.CharField(db_column='TIPO_UM_REG_SCE_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    minimo = models.DecimalField(db_column='MINIMO', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    massimo = models.DecimalField(db_column='MASSIMO', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    anno_anticipo = models.IntegerField(db_column='ANNO_ANTICIPO', blank=True, null=True)  # Field name made lowercase.
    reg_sce_desc_ita = models.CharField(db_column='REG_SCE_DESC_ITA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reg_sce_desc_eng = models.CharField(db_column='REG_SCE_DESC_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nota_pre_desc_ita = models.TextField(db_column='NOTA_PRE_DESC_ITA', blank=True, null=True)  # Field name made lowercase.
    nota_pre_desc_eng = models.TextField(db_column='NOTA_PRE_DESC_ENG', blank=True, null=True)  # Field name made lowercase.
    nota_post_desc_ita = models.TextField(db_column='NOTA_POST_DESC_ITA', blank=True, null=True)  # Field name made lowercase.
    nota_post_desc_eng = models.TextField(db_column='NOTA_POST_DESC_ENG', blank=True, null=True)  # Field name made lowercase.
    filtri_reg_sce_desc = models.TextField(db_column='FILTRI_REG_SCE_DESC', blank=True, null=True)  # Field name made lowercase.
    cond_reg_sce_desc = models.TextField(db_column='COND_REG_SCE_DESC', blank=True, null=True)  # Field name made lowercase.
    ateneo_id = models.IntegerField(db_column='ATENEO_ID', blank=True, null=True)  # Field name made lowercase.
    ateneo_des = models.CharField(db_column='ATENEO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taf_cod = models.CharField(db_column='TAF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    id_ambito = models.IntegerField(db_column='ID_AMBITO', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PIANI_REG_SCE'


class DidatticaPianiBloccoSce(models.Model):
    blocco_sce_id = models.IntegerField(db_column='BLOCCO_SCE_ID', primary_key=True)  # Field name made lowercase.
    reg_sce = models.ForeignKey('DidatticaPianiRegSce', models.DO_NOTHING, db_column='REG_SCE_ID', blank=True, null=True, related_name='blocchi')  # Field name made lowercase.
    progressivo_blocco_sce = models.IntegerField(db_column='PROGRESSIVO_BLOCCO_SCE', blank=True, null=True)  # Field name made lowercase.
    lingua_cod = models.CharField(db_column='LINGUA_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ord_num_lingua = models.IntegerField(db_column='ORD_NUM_LINGUA', blank=True, null=True)  # Field name made lowercase.
    cond_blocco_sce_desc = models.TextField(db_column='COND_BLOCCO_SCE_DESC', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PIANI_BLOCCO_SCE'

        
class DidatticaPianiAfRegSce(models.Model):
    af_reg_sce_id = models.IntegerField(db_column='AF_REG_SCE_ID', primary_key=True)  # Field name made lowercase.
    reg_sce = models.ForeignKey('DidatticaPianiRegSce', models.DO_NOTHING, db_column='REG_SCE_ID', blank=True, null=True, related_name='af')  # Field name made lowercase.
    blocco_sce = models.ForeignKey('DidatticaPianiBloccoSce', models.DO_NOTHING, db_column='BLOCCO_SCE_ID', blank=True, null=True, related_name='af_blocco')  # Field name made lowercase.
    af_pds_id = models.IntegerField(db_column='AF_PDS_ID', blank=True, null=True)  # Field name made lowercase.
    aa_off_id_af_reg_sce = models.IntegerField(db_column='AA_OFF_ID_AF_REG_SCE', blank=True, null=True)  # Field name made lowercase.
    flag_statutaria = models.CharField(db_column='FLAG_STATUTARIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_verifica_piani = models.CharField(db_column='FLAG_VERIFICA_PIANI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag_controllo_anno_offerta = models.CharField(db_column='FLAG_CONTROLLO_ANNO_OFFERTA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PIANI_AF_REG_SCE'


class VDidatticaAfPianiStudio(models.Model):
    af_pds_id = models.IntegerField(db_column='AF_PDS_ID', primary_key=True)  # Field name made lowercase.
    id_cds = models.IntegerField(db_column='ID_CDS', blank=True, null=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ord_id = models.IntegerField(db_column='ORD_ID', blank=True, null=True)  # Field name made lowercase.
    ord_cod = models.CharField(db_column='ORD_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_id = models.IntegerField(db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    id_off = models.CharField(db_column='ID_OFF', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    anno_di_scelta_percorso = models.DecimalField(db_column='ANNO_DI_SCELTA_PERCORSO', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pds_regdid_comune_id = models.IntegerField(db_column='PDS_REGDID_COMUNE_ID', blank=True, null=True)  # Field name made lowercase.
    num_pds = models.IntegerField(db_column='NUM_PDS', blank=True, null=True)  # Field name made lowercase.
    pds_regdid_id = models.IntegerField(db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    pds_desc_ita = models.CharField(db_column='PDS_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    pds_desc_eng = models.CharField(db_column='PDS_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    pds_id_riferimento = models.IntegerField(db_column='PDS_ID_RIFERIMENTO', blank=True, null=True)  # Field name made lowercase.
    lingua_cod = models.CharField(db_column='LINGUA_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_id = models.IntegerField(db_column='ANA_AF_ID', blank=True, null=True)  # Field name made lowercase.
    ana_af_cod = models.CharField(db_column='ANA_AF_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_ita = models.CharField(db_column='ANA_AF_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_desc_eng = models.CharField(db_column='ANA_AF_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_id = models.IntegerField(db_column='ANA_AF_CAPOG_ID', blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_cod = models.CharField(db_column='ANA_AF_CAPOG_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_desc_ita = models.CharField(db_column='ANA_AF_CAPOG_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_af_capog_desc_eng = models.CharField(db_column='ANA_AF_CAPOG_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.DecimalField(db_column='ANNO_CORSO', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    flag_obbl = models.CharField(db_column='FLAG_OBBL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    flag_raggruppamento = models.CharField(db_column='FLAG_RAGGRUPPAMENTO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    flag_capogruppo = models.CharField(db_column='FLAG_CAPOGRUPPO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    flag_raggruppata = models.CharField(db_column='FLAG_RAGGRUPPATA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    flag_no_raggr_o_capog = models.CharField(db_column='FLAG_NO_RAGGR_O_CAPOG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    cfu = models.DecimalField(db_column='CFU', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ore = models.DecimalField(db_column='ORE', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    erog_id = models.ForeignKey('DidatticaAttivitaFormativaErogata', models.DO_NOTHING, db_column='EROG_ID', blank=True, null=True, related_name="v_pds")  # Field name made lowercase.
    mod_did_cod = models.CharField(db_column='MOD_DID_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_ita = models.CharField(db_column='MOD_DID_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    mod_did_desc_eng = models.CharField(db_column='MOD_DID_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    moduli_pds_id = models.IntegerField(db_column='MODULI_PDS_ID', blank=True, null=True)  # Field name made lowercase.
    ana_mod_sett_id = models.IntegerField(db_column='ANA_MOD_SETT_ID', blank=True, null=True)  # Field name made lowercase.
    flag_segmento = models.CharField(db_column='FLAG_SEGMENTO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    sett_desc_ita = models.CharField(db_column='SETT_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    sett_desc_eng = models.CharField(db_column='SETT_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_mod_id = models.IntegerField(db_column='ANA_MOD_ID', blank=True, null=True)  # Field name made lowercase.
    ana_mod_cod = models.CharField(db_column='ANA_MOD_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_mod_desc_ita = models.CharField(db_column='ANA_MOD_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ana_mod_desc_eng = models.CharField(db_column='ANA_MOD_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    taf_cod = models.CharField(db_column='TAF_COD', max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    taf_desc_ita = models.CharField(db_column='TAF_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    taf_desc_eng = models.CharField(db_column='TAF_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    id_ambito = models.IntegerField(db_column='ID_AMBITO', blank=True, null=True)  # Field name made lowercase.
    ambito_desc_ita = models.CharField(db_column='AMBITO_DESC_ITA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ambito_desc_eng = models.CharField(db_column='AMBITO_DESC_ENG', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.
    off_did_id = models.IntegerField(db_column='OFF_DID_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V2_DIDATTICA_AF_PIANI_STUDIO'

