# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from django.contrib.auth import get_user_model
from django.db import models


class InsModAbstract(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS', auto_now_add=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', auto_now=True,
                                  blank=True, null=True)

    class Meta:
        abstract = True


class ComuniAll(models.Model):
    # Field name made lowercase.
    id_comune = models.IntegerField(db_column='ID_COMUNE', primary_key=True)
    ds_comune = models.CharField(db_column='DS_COMUNE', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    cd_catasto = models.CharField(db_column='CD_CATASTO', unique=True, max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cd_istat = models.CharField(
        db_column='CD_ISTAT',
        max_length=6,
        blank=True,
        null=True)
    dt_costituzione = models.DateTimeField(db_column='DT_COSTITUZIONE', blank=True,
                                           null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_cessazione = models.DateTimeField(
        db_column='DT_CESSAZIONE', blank=True, null=True)
    # Field name made lowercase.
    id_prov = models.IntegerField(db_column='ID_PROV', blank=True, null=True)
    # Field name made lowercase.
    cd_sigla = models.CharField(
        db_column='CD_SIGLA',
        max_length=2,
        blank=True,
        null=True)
    # Field name made lowercase.
    ds_prov = models.CharField(
        db_column='DS_PROV',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    id_nazione = models.IntegerField(
        db_column='ID_NAZIONE', blank=True, null=True)
    cd_iso3166_1_a2_nazione = models.CharField(db_column='CD_ISO3166_1_A2_NAZIONE', max_length=2, blank=True,
                                               null=True)  # Field name made lowercase.
    ds_nazione = models.CharField(db_column='DS_NAZIONE', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'comuni_all'


class DidatticaAttivitaFormativa(InsModAbstract):
    # Field name made lowercase.
    af_id = models.IntegerField(db_column='AF_ID', primary_key=True)
    cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='CDS_ID', blank=True,
                            null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cdsord_id = models.IntegerField(
        db_column='CDSORD_ID', blank=True, null=True)
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_ord_id = models.IntegerField(
        db_column='AA_ORD_ID', blank=True, null=True)
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True,
                               null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_regdid_id = models.IntegerField(
        db_column='AA_REGDID_ID', blank=True, null=True)
    stato_regdid_cod = models.CharField(db_column='STATO_REGDID_COD', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.
    stato_appr_regdid_cod = models.CharField(db_column='STATO_APPR_REGDID_COD', max_length=5, blank=True,
                                             null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey('DidatticaPdsRegolamento', models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=10,
        blank=True,
        null=True)
    # Field name made lowercase.
    pds_des = models.CharField(
        db_column='PDS_DES',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    comune_flg = models.IntegerField(
        db_column='COMUNE_FLG', blank=True, null=True)
    attinenza_cod = models.CharField(db_column='ATTINENZA_COD', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)
    # Field name made lowercase.
    aa_off_id = models.IntegerField(
        db_column='AA_OFF_ID', blank=True, null=True)
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=5, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_comp_af_id = models.IntegerField(db_column='TIPO_COMP_AF_ID', blank=True,
                                          null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=10, blank=True,
                                        null=True)  # Field name made lowercase.
    des_tipo_comp_af = models.CharField(db_column='DES_TIPO_COMP_AF', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    af_gen_id = models.IntegerField(
        db_column='AF_GEN_ID', blank=True, null=True)
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    des = models.CharField(
        db_column='DES',
        max_length=255,
        blank=True,
        null=True)
    af_gen_des_eng = models.CharField(db_column='AF_GEN_DES_ENG', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    # Field name made lowercase.
    anno_corso = models.IntegerField(
        db_column='ANNO_CORSO', blank=True, null=True)
    lista_anni_corso = models.CharField(db_column='LISTA_ANNI_CORSO', max_length=20, blank=True,
                                        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    af_regdid_id = models.IntegerField(
        db_column='AF_REGDID_ID', blank=True, null=True)
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.
    sett_des = models.CharField(db_column='SETT_DES', max_length=150, blank=True,
                                null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True,
                                   null=True)  # Field name made lowercase.
    freq_obblig_flg = models.IntegerField(db_column='FREQ_OBBLIG_FLG', blank=True,
                                          null=True)  # Field name made lowercase.
    # Field name made lowercase.
    ore_min_freq = models.IntegerField(
        db_column='ORE_MIN_FREQ', blank=True, null=True)
    # Field name made lowercase.
    ore_att_front = models.IntegerField(
        db_column='ORE_ATT_FRONT', blank=True, null=True)
    # Field name made lowercase.
    num_max_reit = models.IntegerField(
        db_column='NUM_MAX_REIT', blank=True, null=True)
    # Field name made lowercase.
    libera_flg = models.IntegerField(
        db_column='LIBERA_FLG', blank=True, null=True)
    scelta_mod_flg = models.IntegerField(db_column='SCELTA_MOD_FLG', blank=True,
                                         null=True)  # Field name made lowercase.
    tipo_esa_cod = models.CharField(db_column='TIPO_ESA_COD', max_length=5, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_esa_des = models.CharField(db_column='TIPO_ESA_DES', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_val_cod = models.CharField(db_column='TIPO_VAL_COD', max_length=5, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_val_des = models.CharField(db_column='TIPO_VAL_DES', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    tipo_ins_des = models.CharField(db_column='TIPO_INS_DES', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    serale_flg = models.IntegerField(
        db_column='SERALE_FLG', blank=True, null=True)
    # Field name made lowercase.
    no_media_flg = models.IntegerField(
        db_column='NO_MEDIA_FLG', blank=True, null=True)
    # Field name made lowercase.
    sostegno_flg = models.IntegerField(
        db_column='SOSTEGNO_FLG', blank=True, null=True)
    # Field name made lowercase.
    nota = models.CharField(
        db_column='NOTA',
        max_length=2000,
        blank=True,
        null=True)
    # Field name made lowercase.
    af_radice_id = models.IntegerField(
        db_column='AF_RADICE_ID', blank=True, null=True)
    num_liv_albero = models.IntegerField(db_column='NUM_LIV_ALBERO', blank=True,
                                         null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_inizio = models.DateTimeField(
        db_column='DATA_INIZIO', blank=True, null=True)
    # Field name made lowercase.
    data_fine = models.DateTimeField(
        db_column='DATA_FINE', blank=True, null=True)
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    matricola_resp_did = models.CharField(db_column='MATRICOLA_RESP_DID', max_length=6, blank=True,
                                          null=True)  # Field name made lowercase.
    cod_fis_resp_did = models.CharField(db_column='COD_FIS_RESP_DID', max_length=16, blank=True,
                                        null=True)  # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(db_column='RUOLO_RESP_DID_COD', max_length=4, blank=True,
                                          null=True)  # Field name made lowercase.
    url_sito_web = models.CharField(db_column='URL_SITO_WEB', max_length=2000, blank=True,
                                    null=True)  # Field name made lowercase.
    lista_lin_did_af = models.CharField(db_column='LISTA_LIN_DID_AF', max_length=2000, blank=True,
                                        null=True)  # Field name made lowercase.
    lista_mod_did_af = models.CharField(db_column='LISTA_MOD_DID_AF', max_length=2000, blank=True,
                                        null=True)  # Field name made lowercase.
    lista_taf_set_cfu = models.CharField(db_column='LISTA_TAF_SET_CFU', max_length=2000, blank=True,
                                         null=True)  # Field name made lowercase.
    # Field name made lowercase.
    mutuata_flg = models.IntegerField(
        db_column='MUTUATA_FLG', blank=True, null=True)
    # Field name made lowercase.
    af_master_id = models.IntegerField(
        db_column='AF_MASTER_ID', blank=True, null=True)
    # Field name made lowercase.
    num_af_figlie = models.IntegerField(
        db_column='NUM_AF_FIGLIE', blank=True, null=True)
    # Field name made lowercase.
    num_af_foglie = models.IntegerField(
        db_column='NUM_AF_FOGLIE', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'didattica_attivita_formativa'

    def __str__(self):
        return '{}'.format(self.af_id)

    def checkIfMainCourse(self):
        return self.af_id == self.af_radice_id


class DidatticaCds(InsModAbstract):
    # Field name made lowercase.
    cds_id = models.IntegerField(db_column='CDS_ID', primary_key=True)
    # Field name made lowercase.
    cds_cod = models.CharField(
        db_column='CDS_COD',
        max_length=10,
        blank=True,
        null=True)
    nome_cds_it = models.CharField(db_column='NOME_CDS_IT', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    nome_cds_eng = models.CharField(db_column='NOME_CDS_ENG', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    rif_cod = models.CharField(
        db_column='RIF_COD',
        max_length=10,
        blank=True,
        null=True)
    # Field name made lowercase.
    rif_des = models.CharField(
        db_column='RIF_DES',
        max_length=40,
        blank=True,
        null=True)
    dip = models.ForeignKey('DidatticaDipartimento', models.DO_NOTHING, db_column='DIP_ID', blank=True,
                            null=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True,
                                      null=True)  # Field name made lowercase.
    # Field name made lowercase.
    durata_anni = models.IntegerField(
        db_column='DURATA_ANNI', blank=True, null=True)
    # Field name made lowercase.
    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    tipo_titit_cod = models.CharField(db_column='TIPO_TITIT_COD', max_length=10, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo_titit_des = models.CharField(db_column='TIPO_TITIT_DES', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    min_cfu_comuni = models.IntegerField(db_column='MIN_CFU_COMUNI', blank=True,
                                         null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cfu_max_rico = models.IntegerField(
        db_column='CFU_MAX_RICO', blank=True, null=True)
    # Field name made lowercase.
    num_max_esami = models.IntegerField(
        db_column='NUM_MAX_ESAMI', blank=True, null=True)
    perc_min_ore_stu_ind = models.FloatField(db_column='PERC_MIN_ORE_STU_IND', blank=True,
                                             null=True)  # Field name made lowercase.
    perc_max_ore_stu_ind = models.FloatField(db_column='PERC_MAX_ORE_STU_IND', blank=True,
                                             null=True)  # Field name made lowercase.
    tipo_spec_cod = models.CharField(db_column='TIPO_SPEC_COD', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    tipo_spec_des = models.CharField(db_column='TIPO_SPEC_DES', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    scuola_spec_id = models.IntegerField(db_column='SCUOLA_SPEC_ID', blank=True,
                                         null=True)  # Field name made lowercase.
    scuola_spec_des = models.CharField(db_column='SCUOLA_SPEC_DES', max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cla_m_id = models.IntegerField(db_column='CLA_M_ID', blank=True, null=True)
    cla_miur_cod = models.CharField(db_column='CLA_MIUR_COD', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    cla_miur_des = models.CharField(db_column='CLA_MIUR_DES', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    intercla_m_id = models.IntegerField(
        db_column='INTERCLA_M_ID', blank=True, null=True)
    intercla_miur_cod = models.CharField(db_column='INTERCLA_MIUR_COD', max_length=10, blank=True,
                                         null=True)  # Field name made lowercase.
    intercla_miur_des = models.CharField(db_column='INTERCLA_MIUR_DES', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase.
    codicione = models.CharField(db_column='CODICIONE', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    min_diff_cfu_ord = models.IntegerField(db_column='MIN_DIFF_CFU_ORD', blank=True,
                                           null=True)  # Field name made lowercase.
    sett_post_rif_flg = models.IntegerField(db_column='SETT_POST_RIF_FLG', blank=True,
                                            null=True)  # Field name made lowercase.
    istat_cod = models.CharField(db_column='ISTAT_COD', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    max_punti = models.IntegerField(
        db_column='MAX_PUNTI', blank=True, null=True)
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_att_id = models.IntegerField(
        db_column='AA_ATT_ID', blank=True, null=True)
    data_attivazione = models.DateTimeField(db_column='DATA_ATTIVAZIONE', blank=True,
                                            null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_dis_id = models.IntegerField(
        db_column='AA_DIS_ID', blank=True, null=True)
    # Field name made lowercase.
    url = models.CharField(
        db_column='URL',
        max_length=255,
        blank=True,
        null=True)
    cds_url_info_web = models.CharField(db_column='CDS_URL_INFO_WEB', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    cds_vis_web_flg = models.IntegerField(db_column='CDS_VIS_WEB_FLG', blank=True,
                                          null=True)  # Field name made lowercase.
    # Field name made lowercase.
    ccs_id = models.IntegerField(db_column='CCS_ID', blank=True, null=True)
    # Field name made lowercase.
    ccs_cod = models.CharField(
        db_column='CCS_COD',
        max_length=10,
        blank=True,
        null=True)
    # Field name made lowercase.
    ccs_des = models.CharField(
        db_column='CCS_DES',
        max_length=255,
        blank=True,
        null=True)
    flg_exp_seg_stu = models.IntegerField(db_column='FLG_EXP_SEG_STU', blank=True,
                                          null=True)  # Field name made lowercase.
    data_exp_seg_stu = models.DateTimeField(db_column='DATA_EXP_SEG_STU', blank=True,
                                            null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='CDSORD_ID', unique=True, blank=True,
                                    null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_ord_id = models.IntegerField(
        db_column='AA_ORD_ID', blank=True, null=True)
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_cds'

    def __str__(self):
        return '{} {}'.format(self.cds_id, self.nome_cds_it)


class DidatticaCdsLingua(models.Model):
    # Field name made lowercase.
    lin_did_ord_id = models.IntegerField(
        db_column='LIN_DID_ORD_ID', primary_key=True)
    cdsord = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDSORD_ID', blank=True,
                               null=True, to_field='cdsord_id')  # Field name made lowercase.
    # Field name made lowercase.
    lingua_id = models.IntegerField(
        db_column='LINGUA_ID', blank=True, null=True)
    lingua_des_it = models.CharField(db_column='LINGUA_DES_IT', max_length=100, blank=True,
                                     null=True)  # Field name made lowercase.
    iso6392_cod = models.CharField(db_column='ISO6392_COD', max_length=3, blank=True,
                                   null=True)  # Field name made lowercase.
    lingua_des_eng = models.CharField(db_column='LINGUA_DES_ENG', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_cds_lingua'

    def __str__(self):
        return '{} {}'.format(self.lin_did_ord_id, self.lingua_des_it)


class DidatticaCopertura(InsModAbstract):
    # Field name made lowercase.
    coper_id = models.IntegerField(db_column='COPER_ID', primary_key=True)
    personale = models.ForeignKey('Personale', models.DO_NOTHING, db_column='PERSONALE_ID', blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_id = models.IntegerField(db_column='AA_ID', blank=True, null=True)
    # Field name made lowercase.
    aa_off_id = models.IntegerField(
        db_column='AA_OFF_ID', blank=True, null=True)
    af = models.ForeignKey(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID', blank=True,
                           null=True)  # Field name made lowercase.
    # Field name made lowercase.
    af_radice_id = models.IntegerField(
        db_column='AF_RADICE_ID', blank=True, null=True)
    # Field name made lowercase.
    ore = models.IntegerField(db_column='ORE', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'didattica_copertura'


class DidatticaDipartimento(InsModAbstract):
    # Field name made lowercase.
    dip_id = models.IntegerField(db_column='DIP_ID', primary_key=True)
    dip_cod = models.CharField(db_column='DIP_COD', unique=True, max_length=40, blank=True,
                               null=True)  # Field name made lowercase.
    dip_des_it = models.CharField(db_column='DIP_DES_IT', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    dip_des_eng = models.CharField(db_column='DIP_DES_ENG', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    dip_nome_breve = models.CharField(db_column='DIP_NOME_BREVE', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.
    dip_cd_csa = models.CharField(db_column='DIP_CD_CSA', max_length=40, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    miur_dip_id = models.IntegerField(
        db_column='MIUR_DIP_ID', blank=True, null=True)
    url_pubbl_off_f = models.CharField(db_column='URL_PUBBL_OFF_F', max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.
    dip_vis_web_flg = models.IntegerField(db_column='DIP_VIS_WEB_FLG', blank=True,
                                          null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_dipartimento'

    def __str__(self):
        return '{} {}'.format(self.dip_cod, self.dip_des_it)


class DidatticaDottoratoCds(InsModAbstract):
    dip_cod = models.ForeignKey(DidatticaDipartimento, models.DO_NOTHING, db_column='DIP_COD', blank=True,
                                null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cds_id_esse3 = models.IntegerField(
        db_column='CDS_ID_ESSE3', primary_key=True)
    # Field name made lowercase.
    cds_cod = models.CharField(
        db_column='CDS_COD',
        max_length=10,
        blank=True,
        null=True)
    nome_cds_it = models.CharField(db_column='NOME_CDS_IT', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    rif_cod = models.CharField(
        db_column='RIF_COD',
        max_length=10,
        blank=True,
        null=True)
    # Field name made lowercase.
    rif_des = models.CharField(
        db_column='RIF_DES',
        max_length=255,
        blank=True,
        null=True)
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True,
                                      null=True)  # Field name made lowercase.
    # Field name made lowercase.
    durata_anni = models.IntegerField(
        db_column='DURATA_ANNI', blank=True, null=True)
    # Field name made lowercase.
    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    tipo_titit_cod = models.CharField(db_column='TIPO_TITIT_COD', max_length=10, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo_titit_des = models.CharField(db_column='TIPO_TITIT_DES', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo_spec_cod = models.CharField(db_column='TIPO_SPEC_COD', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    tipo_spec_des = models.CharField(db_column='TIPO_SPEC_DES', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    istat_cod = models.CharField(db_column='ISTAT_COD', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    max_punti = models.IntegerField(
        db_column='MAX_PUNTI', blank=True, null=True)
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_att_id = models.IntegerField(
        db_column='AA_ATT_ID', blank=True, null=True)
    # Field name made lowercase.
    aa_dis_id = models.IntegerField(
        db_column='AA_DIS_ID', blank=True, null=True)
    # Field name made lowercase.
    url = models.CharField(
        db_column='URL',
        max_length=255,
        blank=True,
        null=True)
    cds_url_info_web = models.CharField(db_column='CDS_URL_INFO_WEB', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    cds_vis_web_flg = models.IntegerField(db_column='CDS_VIS_WEB_FLG', blank=True,
                                          null=True)  # Field name made lowercase.
    cdsord_id_esse3 = models.IntegerField(db_column='CDSORD_ID_ESSE3', blank=True,
                                          null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')
    cdsord_des = models.CharField(db_column='CDSORD_DES', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_dottorato_cds'
        unique_together = (('cds_id_esse3', 'aa_ord_id'),)


class DidatticaDottoratoPds(InsModAbstract):
    cds_id_esse3 = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='CDS_ID_ESSE3', blank=True,
                                     null=True, related_name='idesse3_ddpds')  # Field name made lowercase.

    aa_ord = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='AA_ORD_ID', blank=True,
                               null=True, related_name='aaord_ddpds')  # Field name made lowercase.
    # Field name made lowercase.
    pds_id_esse3 = models.IntegerField(
        db_column='PDS_ID_ESSE3', blank=True, null=True)
    # Field name made lowercase.
    pdsord_id_esse3 = models.IntegerField(
        db_column='PDSORD_ID_ESSE3', primary_key=True)
    # Field name made lowercase.
    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    pds_des = models.CharField(
        db_column='PDS_DES',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    indir = models.CharField(
        db_column='INDIR',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    orien = models.CharField(
        db_column='ORIEN',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    stato_cod = models.CharField(db_column='STATO_COD', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_var = models.DateTimeField(
        db_column='DATA_VAR', blank=True, null=True)
    # Field name made lowercase.
    val_min_tesi = models.IntegerField(
        db_column='VAL_MIN_TESI', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'didattica_dottorato_pds'


class DidatticaDottoratoRegolamento(InsModAbstract):
    # Field name made lowercase.
    regdid_id_esse3 = models.IntegerField(
        db_column='REGDID_ID_ESSE3', primary_key=True)
    # Field name made lowercase.
    aa_regdid_id = models.IntegerField(
        db_column='AA_REGDID_ID', blank=True, null=True)
    cds_id_esse3 = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='CDS_ID_ESSE3', blank=True,
                                     null=True, related_name='idesse3_ddr')  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    regdid_des = models.CharField(db_column='REGDID_DES', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    numero_piani_studio = models.IntegerField(db_column='NUMERO_PIANI_STUDIO', blank=True,
                                              null=True)  # Field name made lowercase.
    frequenza_obbligatoria = models.IntegerField(db_column='FREQUENZA_OBBLIGATORIA', blank=True,
                                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    num_ciclo = models.IntegerField(
        db_column='NUM_CICLO', blank=True, null=True)
    aa_ord = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING,
                               db_column='AA_ORD_ID', related_name='aaord_ddr')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_dottorato_regolamento'


class DidatticaPdsRegolamento(InsModAbstract):
    # Field name made lowercase.
    pds_regdid_id = models.IntegerField(
        db_column='PDS_REGDID_ID', primary_key=True)
    # Field name made lowercase.
    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=30,
        blank=True,
        null=True)
    pds_des_it = models.CharField(db_column='PDS_DES_IT', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    pds_des_eng = models.CharField(db_column='PDS_DES_ENG', max_length=2000, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    comune_flg = models.IntegerField(
        db_column='COMUNE_FLG', blank=True, null=True)
    # Field name made lowercase.
    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True,
                               null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')

    class Meta:
        managed = True
        db_table = 'didattica_pds_regolamento'


class DidatticaRegolamento(InsModAbstract):
    # Field name made lowercase.
    regdid_id = models.IntegerField(db_column='REGDID_ID', primary_key=True)
    # Field name made lowercase.
    aa_reg_did = models.IntegerField(
        db_column='AA_REG_DID', blank=True, null=True)
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID', blank=True,
                            null=True)  # Field name made lowercase.
    stato_regdid_cod = models.CharField(db_column='STATO_REGDID_COD', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.
    stato_regdid_des = models.CharField(db_column='STATO_REGDID_DES', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    numero_piani_studio = models.IntegerField(db_column='NUMERO_PIANI_STUDIO', blank=True,
                                              null=True)  # Field name made lowercase.
    anno_scelta_pds = models.IntegerField(db_column='ANNO_SCELTA_PDS', blank=True,
                                          null=True)  # Field name made lowercase.
    modalita_erogazione = models.CharField(db_column='MODALITA_EROGAZIONE', max_length=100, blank=True,
                                           null=True)  # Field name made lowercase.
    frequenza_obbligatoria = models.IntegerField(db_column='FREQUENZA_OBBLIGATORIA', blank=True,
                                                 null=True)  # Field name made lowercase.
    titolo_congiunto_cod = models.CharField(db_column='TITOLO_CONGIUNTO_COD', max_length=100, blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_regolamento'

    def __str__(self):
        return '{} {}'.format(self.regdid_id, self.aa_reg_did)


class DidatticaTestiAf(InsModAbstract):
    af = models.OneToOneField(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID',
                              primary_key=True)  # Field name made lowercase.
    # Field name made lowercase.
    aa_off_id = models.IntegerField(
        db_column='AA_OFF_ID', blank=True, null=True)
    # Field name made lowercase.
    testi_af_id = models.IntegerField(
        db_column='TESTI_AF_ID', blank=True, null=True)
    # Field name made lowercase.
    tipo_testo_af_cod = models.CharField(
        db_column='TIPO_TESTO_AF_COD', max_length=100)
    tipo_testo_af_des = models.TextField(db_column='TIPO_TESTO_AF_DES', blank=True,
                                         null=True)  # Field name made lowercase.
    tipo_testo_af_etic = models.CharField(db_column='TIPO_TESTO_AF_ETIC', max_length=255, blank=True,
                                          null=True)  # Field name made lowercase.
    tipo_testo_af_etic_eng = models.TextField(db_column='TIPO_TESTO_AF_ETIC_ENG', blank=True,
                                              null=True)  # Field name made lowercase.
    # Field name made lowercase.
    obbl_flg = models.IntegerField(db_column='OBBL_FLG', blank=True, null=True)
    # Field name made lowercase.
    testo_af_ita = models.TextField(
        db_column='TESTO_AF_ITA', blank=True, null=True)
    testo_af_short_ita = models.TextField(db_column='TESTO_AF_SHORT_ITA', blank=True,
                                          null=True)  # Field name made lowercase.
    testo_af_fmt_ita = models.TextField(db_column='TESTO_AF_FMT_ITA', blank=True,
                                        null=True)  # Field name made lowercase.
    dt_ins_txt_clob_ita = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ITA', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_mod_txt_clob_ita = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ITA', blank=True,
                                               null=True)  # Field name made lowercase.
    # Field name made lowercase.
    testo_af_eng = models.TextField(
        db_column='TESTO_AF_ENG', blank=True, null=True)
    testo_af_short_eng = models.TextField(db_column='TESTO_AF_SHORT_ENG', blank=True,
                                          null=True)  # Field name made lowercase.
    dt_ins_txt_clob_eng = models.TextField(db_column='DT_INS_TXT_CLOB_ENG', blank=True,
                                           null=True)  # Field name made lowercase.
    dt_mod_txt_clob_eng = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ENG', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_ins_mod_max = models.DateTimeField(db_column='DT_INS_MOD_MAX', blank=True,
                                          null=True)  # Field name made lowercase.
    testo_af_fmt_eng = models.TextField(db_column='TESTO_AF_FMT_ENG', blank=True,
                                        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'didattica_testi_af'
        unique_together = (('af', 'tipo_testo_af_cod'),)


class DidatticaTestiRegolamento(InsModAbstract):
    # Field name made lowercase.
    txt_id = models.IntegerField(db_column='TXT_ID', primary_key=True)
    regdid = models.ForeignKey(DidatticaRegolamento, models.DO_NOTHING,
                               db_column='REGDID_ID')  # Field name made lowercase.
    tipo_testo_regdid_cod = models.CharField(db_column='TIPO_TESTO_REGDID_COD',
                                             max_length=100)  # Field name made lowercase.
    tipo_testo_regdid_des = models.CharField(db_column='TIPO_TESTO_REGDID_DES', max_length=255, blank=True,
                                             null=True)  # Field name made lowercase.
    # Field name made lowercase.
    clob_txt_ita = models.TextField(
        db_column='CLOB_TXT_ITA', blank=True, null=True)
    # Field name made lowercase.
    clob_txt_eng = models.TextField(
        db_column='CLOB_TXT_ENG', blank=True, null=True)
    # Field name made lowercase.
    profilo = models.TextField(db_column='PROFILO', blank=True, null=True)
    # Field name made lowercase.
    profilo_eng = models.TextField(
        db_column='PROFILO_ENG', blank=True, null=True)
    dt_ins_txt_clob_ita = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ITA', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_ins_txt_clob_eng = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ENG', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_mod_txt_clob_ita = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ITA', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_mod_txt_clob_eng = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ENG', blank=True,
                                               null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'didattica_testi_regolamento'

    def __str__(self):
        return '{} {}'.format(self.txt_id, self.tipo_testo_regdid_cod)


class FunzioniUnitaOrganizzativa(models.Model):
    matricola = models.CharField(db_column='MATRICOLA', max_length=6, blank=True,
                                 null=True)  # Field name made lowercase.
    cod_fis = models.ForeignKey('Personale', models.DO_NOTHING, db_column='COD_FIS', blank=True,
                                null=True)  # Field name made lowercase.
    # Field name made lowercase.
    comparto = models.CharField(
        db_column='COMPARTO',
        max_length=1,
        blank=True,
        null=True)
    # Field name made lowercase.
    ruolo = models.CharField(
        db_column='RUOLO',
        max_length=4,
        blank=True,
        null=True)
    unita_organizzativa = models.ForeignKey('UnitaOrganizzativa', models.DO_NOTHING, db_column='UNITA_ORGANIZZATIVA_ID',
                                            blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    funzione = models.CharField(
        db_column='FUNZIONE',
        max_length=6,
        blank=True,
        null=True)
    # Field name made lowercase.
    decorrenza = models.DateTimeField(
        db_column='DECORRENZA', blank=True, null=True)
    # Field name made lowercase.
    termine = models.DateTimeField(db_column='TERMINE', blank=True, null=True)
    ds_funzione = models.CharField(db_column='DS_FUNZIONE', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    fl_posorg = models.FloatField(db_column='FL_POSORG', blank=True, null=True)
    fl_responsabile = models.FloatField(db_column='FL_RESPONSABILE', blank=True,
                                        null=True)  # Field name made lowercase.
    cd_funzbase = models.CharField(db_column='CD_FUNZBASE', max_length=6, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'funzioni_unita_organizzativa'


class Personale(InsModAbstract):
    # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB')
    cd_esterno = models.CharField(db_column='CD_ESTERNO', max_length=60, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    matricola = models.CharField(
        db_column='MATRICOLA',
        unique=True,
        max_length=6)
    matricola_sp = models.CharField(db_column='MATRICOLA_SP', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    nome = models.CharField(
        db_column='NOME',
        max_length=100,
        blank=True,
        null=True)
    # Field name made lowercase.
    cognome = models.CharField(
        db_column='COGNOME',
        max_length=100,
        blank=True,
        null=True)
    middle_name = models.CharField(db_column='MIDDLE_NAME', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    cod_fis = models.CharField(db_column='COD_FIS', unique=True, max_length=16, blank=True,
                               null=True)  # Field name made lowercase.
    cd_genere = models.CharField(db_column='CD_GENERE', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_nascita = models.DateField(
        db_column='DT_NASCITA', blank=True, null=True)
    # Field name made lowercase.
    id_comu_nasc = models.IntegerField(
        db_column='ID_COMU_NASC', blank=True, null=True)
    ds_cittstra_nasc = models.CharField(db_column='DS_CITTSTRA_NASC', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    ds_comune_nasc = models.CharField(db_column='DS_COMUNE_NASC', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    ds_prov_nasc = models.CharField(db_column='DS_PROV_NASC', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    cd_sigla_nasc = models.CharField(db_column='CD_SIGLA_NASC', max_length=2, blank=True,
                                     null=True)  # Field name made lowercase.
    id_nazione_nasc = models.IntegerField(db_column='ID_NAZIONE_NASC', blank=True,
                                          null=True)  # Field name made lowercase.
    ds_nazi_nasc = models.CharField(db_column='DS_NAZI_NASC', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    ds_nazi_breve_nasc = models.CharField(db_column='DS_NAZI_BREVE_NASC', max_length=20, blank=True,
                                          null=True)  # Field name made lowercase.
    id_comu_res = models.ForeignKey(ComuniAll, models.DO_NOTHING, db_column='ID_COMU_RES', blank=True,
                                    null=True)  # Field name made lowercase.
    ds_comune_res = models.CharField(db_column='DS_COMUNE_RES', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    cd_cap_res = models.CharField(db_column='CD_CAP_RES', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    indirizzo_res = models.CharField(db_column='INDIRIZZO_RES', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    num_civico_res = models.CharField(db_column='NUM_CIVICO_RES', max_length=15, blank=True,
                                      null=True)  # Field name made lowercase.
    cd_sigla_res = models.CharField(db_column='CD_SIGLA_RES', max_length=2, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    id_comu_dom = models.IntegerField(
        db_column='ID_COMU_DOM', blank=True, null=True)
    ds_comune_dom = models.CharField(db_column='DS_COMUNE_DOM', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    cd_cap_dom = models.CharField(db_column='CD_CAP_DOM', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    indirizzo_dom = models.CharField(db_column='INDIRIZZO_DOM', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    num_civico_dom = models.CharField(db_column='NUM_CIVICO_DOM', max_length=15, blank=True,
                                      null=True)  # Field name made lowercase.
    cd_sigla_dom = models.CharField(db_column='CD_SIGLA_DOM', max_length=2, blank=True,
                                    null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cd_comparto = models.CharField(db_column='CD_COMPARTO', max_length=1)
    ds_comparto = models.CharField(db_column='DS_COMPARTO', max_length=40, blank=True,
                                   null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4)
    ds_ruolo = models.CharField(db_column='DS_RUOLO', max_length=40, blank=True,
                                null=True)  # Field name made lowercase.
    ds_ruolo_locale = models.CharField(db_column='DS_RUOLO_LOCALE', max_length=40, blank=True,
                                       null=True)  # Field name made lowercase.
    peso_ruolo = models.DecimalField(db_column='PESO_RUOLO', max_digits=10, decimal_places=0, blank=True,
                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_rap_ini = models.DateField(
        db_column='DT_RAP_INI', blank=True, null=True)
    # Field name made lowercase.
    dt_rap_fin = models.DateField(
        db_column='DT_RAP_FIN', blank=True, null=True)
    # Field name made lowercase.
    cd_ssd = models.CharField(
        db_column='CD_SSD',
        max_length=12,
        blank=True,
        null=True)
    # Field name made lowercase.
    ds_ssd = models.CharField(
        db_column='DS_SSD',
        max_length=100,
        blank=True,
        null=True)
    # Field name made lowercase.
    cd_fac = models.CharField(
        db_column='CD_FAC',
        max_length=10,
        blank=True,
        null=True)
    # Field name made lowercase.
    ds_fac = models.CharField(
        db_column='DS_FAC',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    aff_org = models.CharField(
        db_column='AFF_ORG',
        max_length=6,
        blank=True,
        null=True)
    ds_aff_org = models.CharField(db_column='DS_AFF_ORG', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    ds_aff_org_breve = models.CharField(db_column='DS_AFF_ORG_BREVE', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aff_org2 = models.CharField(
        db_column='AFF_ORG2',
        max_length=6,
        blank=True,
        null=True)
    ds_aff_org2 = models.CharField(db_column='DS_AFF_ORG2', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    ds_aff_org2_breve = models.CharField(db_column='DS_AFF_ORG2_BREVE', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aff_org3 = models.CharField(
        db_column='AFF_ORG3',
        max_length=6,
        blank=True,
        null=True)
    ds_aff_org3 = models.CharField(db_column='DS_AFF_ORG3', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    ds_aff_org3_breve = models.CharField(db_column='DS_AFF_ORG3_BREVE', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    # Field name made lowercase.
    aff_org4 = models.CharField(
        db_column='AFF_ORG4',
        max_length=6,
        blank=True,
        null=True)
    ds_aff_org4 = models.CharField(db_column='DS_AFF_ORG4', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    ds_aff_org4_breve = models.CharField(db_column='DS_AFF_ORG4_BREVE', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    # Field name made lowercase.
    sede = models.CharField(
        db_column='SEDE',
        max_length=6,
        blank=True,
        null=True)
    # Field name made lowercase.
    ds_sede = models.CharField(
        db_column='DS_SEDE',
        max_length=255,
        blank=True,
        null=True)
    ds_sede_breve = models.CharField(db_column='DS_SEDE_BREVE', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    profilo = models.CharField(
        db_column='PROFILO',
        max_length=11,
        blank=True,
        null=True)
    ds_profilo = models.CharField(db_column='DS_PROFILO', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    ds_profilo_breve = models.CharField(db_column='DS_PROFILO_BREVE', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    cd_ateneo_corr = models.CharField(db_column='CD_ATENEO_CORR', max_length=10, blank=True,
                                      null=True)  # Field name made lowercase.
    ds_ateneo_corr = models.CharField(db_column='DS_ATENEO_CORR', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_ini_rap_univ = models.DateField(
        db_column='DT_INI_RAP_UNIV', blank=True, null=True)
    # Field name made lowercase.
    dt_fin_rap_univ = models.DateField(
        db_column='DT_FIN_RAP_UNIV', blank=True, null=True)
    # Field name made lowercase.
    telrif = models.CharField(
        db_column='TELRIF',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    email = models.CharField(
        db_column='EMAIL',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    urlcv = models.CharField(
        db_column='URLCV',
        max_length=255,
        blank=True,
        null=True)
    fl_docente = models.PositiveIntegerField(db_column='FL_DOCENTE', blank=True,
                                             null=True)  # Field name made lowercase.
    cd_anagrafico = models.CharField(db_column='CD_ANAGRAFICO', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    inquadr = models.CharField(
        db_column='INQUADR',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    badge = models.CharField(
        db_column='BADGE',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    tempo = models.CharField(
        db_column='TEMPO',
        max_length=1,
        blank=True,
        null=True)
    # Field name made lowercase.
    id_contratto = models.IntegerField(
        db_column='ID_CONTRATTO', blank=True, null=True)
    # Field name made lowercase.
    flg_cessato = models.IntegerField(
        db_column='FLG_CESSATO', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_personale',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_personale',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personale'

    def __str__(self):
        return '{} {} [{}]'.format(self.nome,
                                   self.cognome, self.matricola)


class RicercaAster1(InsModAbstract):
    # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_ra1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_ra1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_aster1'

    def __str__(self):
        return '{}'.format(self.descrizione)


class RicercaAster2(InsModAbstract):
    # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)
    ricerca_aster1 = models.ForeignKey(RicercaAster1, models.DO_NOTHING,
                                       db_column='RICERCA_ASTER1_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_ra2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_ra2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_aster2'

    def __str__(self):
        return '{} {}'.format(self.ricerca_aster1,
                              self.descrizione)


class RicercaDocenteGruppo(InsModAbstract):
    # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True,
                                  null=True)  # Field name made lowercase.
    ricerca_gruppo = models.ForeignKey('RicercaGruppo', models.DO_NOTHING,
                                       db_column='RICERCA_GRUPPO_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_docente_gruppo'

    def __str__(self):
        return '{} [{}]'.format(self.docente,
                                self.ricerca_gruppo.nome)


class RicercaDocenteLineaApplicata(InsModAbstract):
    # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS')
    # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)
    # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True,
                                  null=True)  # Field name made lowercase.
    ricerca_linea_applicata = models.ForeignKey('RicercaLineaApplicata', models.DO_NOTHING,
                                                db_column='RICERCA_LINEA_APPLICATA_ID', blank=True,
                                                null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_docente_linea_applicata'


class RicercaDocenteLineaBase(InsModAbstract):
    # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True,
                                  null=True)  # Field name made lowercase.
    ricerca_linea_base = models.ForeignKey('RicercaLineaBase', models.DO_NOTHING, db_column='RICERCA_LINEA_BASE_ID',
                                           blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_docente_linea_base'


class RicercaErc1(InsModAbstract):
    # Field name made lowercase.
    cod_erc1 = models.CharField(
        db_column='COD_ERC1',
        unique=True,
        max_length=40)
    # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_re1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_re1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_erc1'

    def __str__(self):
        return '{} {}'.format(self.cod_erc1,
                              self.descrizione)


class RicercaErc2(InsModAbstract):
    # Field name made lowercase.
    cod_erc2 = models.CharField(
        db_column='COD_ERC2',
        unique=True,
        max_length=60)
    # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')
    ricerca_erc1 = models.ForeignKey(RicercaErc1, models.DO_NOTHING, db_column='RICERCA_ERC1_ID', blank=True,
                                     null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_re2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_re2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_erc2'

    def __str__(self):
        return '{} {}'.format(self.cod_erc2,
                              self.descrizione)


class RicercaGruppo(InsModAbstract):
    # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=200)
    # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_gruppo'

    def __str__(self):
        return '{}'.format(self.nome)


class RicercaLineaApplicata(InsModAbstract):
    # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO', blank=True,
                                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    ricerca_aster2 = models.ForeignKey(RicercaAster2, models.DO_NOTHING,
                                       db_column='RICERCA_ASTER2_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_linea_applicata'

    def __str__(self):
        return '{} {}'.format(self.ricerca_aster2, self.descrizione)


class RicercaLineaBase(InsModAbstract):
    # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO', blank=True,
                                                     null=True)  # Field name made lowercase.
    # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    ricerca_erc2 = models.ForeignKey(RicercaErc2, models.DO_NOTHING,
                                     db_column='RICERCA_ERC2_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ricerca_linea_base'

    def __str__(self):
        return '{} {}'.format(self.ricerca_erc2, self.descrizione)


class TerritorioIt(models.Model):
    cd_catasto = models.OneToOneField(ComuniAll, models.DO_NOTHING, db_column='CD_CATASTO',
                                      primary_key=True)  # Field name made lowercase.
    # Field name made lowercase.
    cd_istat = models.CharField(
        db_column='CD_ISTAT',
        max_length=6,
        blank=True,
        null=True)
    ds_comune = models.CharField(db_column='DS_COMUNE', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    # Field name made lowercase.
    cd_sigla = models.CharField(
        db_column='CD_SIGLA',
        max_length=2,
        blank=True,
        null=True)
    ds_provincia = models.CharField(db_column='DS_PROVINCIA', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    cd_770_regio = models.CharField(db_column='CD_770_REGIO', max_length=2, blank=True,
                                    null=True)  # Field name made lowercase.
    ds_regione = models.CharField(db_column='DS_REGIONE', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'territorio_it'

    def __str__(self):
        return '{} {}'.format(self.cd_catasto, self.cd_istat)


class UnitaOrganizzativa(models.Model):
    # Field name made lowercase.
    uo = models.CharField(db_column='UO', primary_key=True, max_length=40)
    # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB', blank=True, null=True)
    # Field name made lowercase.
    uo_padre = models.CharField(
        db_column='UO_PADRE',
        max_length=6,
        blank=True,
        null=True)
    # Field name made lowercase.
    id_ab_padre = models.IntegerField(
        db_column='ID_AB_PADRE', blank=True, null=True)
    # Field name made lowercase.
    tipo = models.CharField(
        db_column='TIPO',
        max_length=10,
        blank=True,
        null=True)
    descr_tipo = models.CharField(db_column='DESCR_TIPO', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_in = models.DateTimeField(db_column='DATA_IN', blank=True, null=True)
    # Field name made lowercase.
    data_fin = models.DateTimeField(
        db_column='DATA_FIN', blank=True, null=True)
    # Field name made lowercase.
    descr = models.CharField(
        db_column='DESCR',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    breve = models.CharField(
        db_column='BREVE',
        max_length=50,
        blank=True,
        null=True)
    # Field name made lowercase.
    data_ins = models.DateTimeField(
        db_column='DATA_INS', blank=True, null=True)
    # Field name made lowercase.
    data_mod = models.DateTimeField(
        db_column='DATA_MOD', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'unita_organizzativa'
