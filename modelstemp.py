# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BrevettoDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_univoco = models.CharField(db_column='ID_UNIVOCO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    titolo = models.CharField(db_column='TITOLO', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    url_immagine = models.CharField(db_column='URL_IMMAGINE', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    breve_descrizione = models.TextField(db_column='BREVE_DESCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    id_area_tecnologica = models.ForeignKey('TipologiaAreaTecnologica', models.DO_NOTHING, db_column='ID_AREA_TECNOLOGICA', blank=True, null=True)  # Field name made lowercase.
    url_knowledge_share = models.CharField(db_column='URL_KNOWLEDGE_SHARE', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    applicazioni = models.TextField(db_column='APPLICAZIONI', blank=True, null=True)  # Field name made lowercase.
    vantaggi = models.TextField(db_column='VANTAGGI', blank=True, null=True)  # Field name made lowercase.
    trl_aggiornato = models.CharField(db_column='TRL_AGGIORNATO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    proprieta = models.CharField(db_column='PROPRIETA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    id_status_legale = models.ForeignKey('BrevettoStatusLegale', models.DO_NOTHING, db_column='ID_STATUS_LEGALE', blank=True, null=True)  # Field name made lowercase.
    data_priorita = models.DateField(db_column='DATA_PRIORITA', blank=True, null=True)  # Field name made lowercase.
    territorio = models.CharField(db_column='TERRITORIO', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    id_diritto_commerciale = models.ForeignKey('BrevettoDirittiCommerciali', models.DO_NOTHING, db_column='ID_DIRITTO_COMMERCIALE', blank=True, null=True)  # Field name made lowercase.
    id_disponibilita = models.ForeignKey('BrevettoDisponibilita', models.DO_NOTHING, db_column='ID_DISPONIBILITA', blank=True, null=True)  # Field name made lowercase.
    area_ks = models.CharField(db_column='AREA_KS', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BREVETTO_DATI_BASE'


class BrevettoDirittiCommerciali(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_diritto = models.CharField(db_column='DESCR_DIRITTO', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BREVETTO_DIRITTI_COMMERCIALI'


class BrevettoDisponibilita(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_disponibilita = models.CharField(db_column='DESCR_DISPONIBILITA', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BREVETTO_DISPONIBILITA'


class BrevettoInventori(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_brevetto = models.ForeignKey(BrevettoDatiBase, models.DO_NOTHING, db_column='ID_BREVETTO', blank=True, null=True)  # Field name made lowercase.
    matricola_inventore = models.ForeignKey('Personale', models.DO_NOTHING, db_column='MATRICOLA_INVENTORE', blank=True, null=True)  # Field name made lowercase.
    cognomenome_origine = models.CharField(db_column='COGNOMENOME_ORIGINE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BREVETTO_INVENTORI'


class BrevettoStatusLegale(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_status = models.CharField(db_column='DESCR_STATUS', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BREVETTO_STATUS_LEGALE'


class ComuniAll(models.Model):
    id_comune = models.IntegerField(db_column='ID_COMUNE', primary_key=True)  # Field name made lowercase.
    ds_comune = models.CharField(db_column='DS_COMUNE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_catasto = models.CharField(db_column='CD_CATASTO', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_istat = models.CharField(db_column='CD_ISTAT', max_length=6, blank=True, null=True)  # Field name made lowercase.
    dt_costituzione = models.DateTimeField(db_column='DT_COSTITUZIONE', blank=True, null=True)  # Field name made lowercase.
    dt_cessazione = models.DateTimeField(db_column='DT_CESSAZIONE', blank=True, null=True)  # Field name made lowercase.
    id_prov = models.IntegerField(db_column='ID_PROV', blank=True, null=True)  # Field name made lowercase.
    cd_sigla = models.CharField(db_column='CD_SIGLA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_prov = models.CharField(db_column='DS_PROV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_nazione = models.IntegerField(db_column='ID_NAZIONE', blank=True, null=True)  # Field name made lowercase.
    cd_iso3166_1_a2_nazione = models.CharField(db_column='CD_ISO3166_1_A2_NAZIONE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_nazione = models.CharField(db_column='DS_NAZIONE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMUNI_ALL'


class DidatticaAttivitaFormativa(models.Model):
    af_id = models.IntegerField(db_column='AF_ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='CDS_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='CDSORD_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    stato_regdid_cod = models.CharField(db_column='STATO_REGDID_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stato_appr_regdid_cod = models.CharField(db_column='STATO_APPR_REGDID_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey('DidatticaPdsRegolamento', models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    attinenza_cod = models.CharField(db_column='ATTINENZA_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_id = models.IntegerField(db_column='TIPO_COMP_AF_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    des_tipo_comp_af = models.CharField(db_column='DES_TIPO_COMP_AF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.IntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_des_eng = models.CharField(db_column='AF_GEN_DES_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    lista_anni_corso = models.CharField(db_column='LISTA_ANNI_CORSO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_regdid_id = models.IntegerField(db_column='AF_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sett_des = models.CharField(db_column='SETT_DES', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    freq_obblig_flg = models.IntegerField(db_column='FREQ_OBBLIG_FLG', blank=True, null=True)  # Field name made lowercase.
    ore_min_freq = models.IntegerField(db_column='ORE_MIN_FREQ', blank=True, null=True)  # Field name made lowercase.
    ore_att_front = models.IntegerField(db_column='ORE_ATT_FRONT', blank=True, null=True)  # Field name made lowercase.
    num_max_reit = models.IntegerField(db_column='NUM_MAX_REIT', blank=True, null=True)  # Field name made lowercase.
    libera_flg = models.IntegerField(db_column='LIBERA_FLG', blank=True, null=True)  # Field name made lowercase.
    scelta_mod_flg = models.IntegerField(db_column='SCELTA_MOD_FLG', blank=True, null=True)  # Field name made lowercase.
    tipo_esa_cod = models.CharField(db_column='TIPO_ESA_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_esa_des = models.CharField(db_column='TIPO_ESA_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_val_cod = models.CharField(db_column='TIPO_VAL_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_val_des = models.CharField(db_column='TIPO_VAL_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_des = models.CharField(db_column='TIPO_INS_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    serale_flg = models.IntegerField(db_column='SERALE_FLG', blank=True, null=True)  # Field name made lowercase.
    no_media_flg = models.IntegerField(db_column='NO_MEDIA_FLG', blank=True, null=True)  # Field name made lowercase.
    sostegno_flg = models.IntegerField(db_column='SOSTEGNO_FLG', blank=True, null=True)  # Field name made lowercase.
    nota = models.CharField(db_column='NOTA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    af_radice_id = models.IntegerField(db_column='AF_RADICE_ID', blank=True, null=True)  # Field name made lowercase.
    num_liv_albero = models.IntegerField(db_column='NUM_LIV_ALBERO', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    data_inizio = models.DateTimeField(db_column='DATA_INIZIO', blank=True, null=True)  # Field name made lowercase.
    data_fine = models.DateTimeField(db_column='DATA_FINE', blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    matricola_resp_did = models.CharField(db_column='MATRICOLA_RESP_DID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_fis_resp_did = models.CharField(db_column='COD_FIS_RESP_DID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(db_column='RUOLO_RESP_DID_COD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    url_sito_web = models.CharField(db_column='URL_SITO_WEB', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_lin_did_af = models.CharField(db_column='LISTA_LIN_DID_AF', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_mod_did_af = models.CharField(db_column='LISTA_MOD_DID_AF', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_taf_set_cfu = models.CharField(db_column='LISTA_TAF_SET_CFU', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    mutuata_flg = models.IntegerField(db_column='MUTUATA_FLG', blank=True, null=True)  # Field name made lowercase.
    af_master_id = models.IntegerField(db_column='AF_MASTER_ID', blank=True, null=True)  # Field name made lowercase.
    num_af_figlie = models.IntegerField(db_column='NUM_AF_FIGLIE', blank=True, null=True)  # Field name made lowercase.
    num_af_foglie = models.IntegerField(db_column='NUM_AF_FOGLIE', blank=True, null=True)  # Field name made lowercase.
    non_erogabile_flg = models.PositiveIntegerField(db_column='NON_EROGABILE_FLG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA'


class DidatticaCds(models.Model):
    cds_id = models.IntegerField(db_column='CDS_ID', primary_key=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nome_cds_it = models.CharField(db_column='NOME_CDS_IT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome_cds_eng = models.CharField(db_column='NOME_CDS_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rif_cod = models.CharField(db_column='RIF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rif_des = models.CharField(db_column='RIF_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    dip = models.ForeignKey('DidatticaDipartimento', models.DO_NOTHING, db_column='DIP_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    durata_anni = models.IntegerField(db_column='DURATA_ANNI', blank=True, null=True)  # Field name made lowercase.
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    tipo_titit_cod = models.CharField(db_column='TIPO_TITIT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_titit_des = models.CharField(db_column='TIPO_TITIT_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    min_cfu_comuni = models.IntegerField(db_column='MIN_CFU_COMUNI', blank=True, null=True)  # Field name made lowercase.
    cfu_max_rico = models.IntegerField(db_column='CFU_MAX_RICO', blank=True, null=True)  # Field name made lowercase.
    num_max_esami = models.IntegerField(db_column='NUM_MAX_ESAMI', blank=True, null=True)  # Field name made lowercase.
    perc_min_ore_stu_ind = models.FloatField(db_column='PERC_MIN_ORE_STU_IND', blank=True, null=True)  # Field name made lowercase.
    perc_max_ore_stu_ind = models.FloatField(db_column='PERC_MAX_ORE_STU_IND', blank=True, null=True)  # Field name made lowercase.
    tipo_spec_cod = models.CharField(db_column='TIPO_SPEC_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_spec_des = models.CharField(db_column='TIPO_SPEC_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scuola_spec_id = models.IntegerField(db_column='SCUOLA_SPEC_ID', blank=True, null=True)  # Field name made lowercase.
    scuola_spec_des = models.CharField(db_column='SCUOLA_SPEC_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cla_m_id = models.IntegerField(db_column='CLA_M_ID', blank=True, null=True)  # Field name made lowercase.
    cla_miur_cod = models.CharField(db_column='CLA_MIUR_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cla_miur_des = models.CharField(db_column='CLA_MIUR_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    intercla_m_id = models.IntegerField(db_column='INTERCLA_M_ID', blank=True, null=True)  # Field name made lowercase.
    intercla_miur_cod = models.CharField(db_column='INTERCLA_MIUR_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    intercla_miur_des = models.CharField(db_column='INTERCLA_MIUR_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codicione = models.CharField(db_column='CODICIONE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    min_diff_cfu_ord = models.IntegerField(db_column='MIN_DIFF_CFU_ORD', blank=True, null=True)  # Field name made lowercase.
    sett_post_rif_flg = models.IntegerField(db_column='SETT_POST_RIF_FLG', blank=True, null=True)  # Field name made lowercase.
    istat_cod = models.CharField(db_column='ISTAT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    max_punti = models.IntegerField(db_column='MAX_PUNTI', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    aa_att_id = models.IntegerField(db_column='AA_ATT_ID', blank=True, null=True)  # Field name made lowercase.
    data_attivazione = models.DateTimeField(db_column='DATA_ATTIVAZIONE', blank=True, null=True)  # Field name made lowercase.
    aa_dis_id = models.IntegerField(db_column='AA_DIS_ID', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cds_url_info_web = models.CharField(db_column='CDS_URL_INFO_WEB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cds_vis_web_flg = models.IntegerField(db_column='CDS_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    ccs_id = models.IntegerField(db_column='CCS_ID', blank=True, null=True)  # Field name made lowercase.
    ccs_cod = models.CharField(db_column='CCS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ccs_des = models.CharField(db_column='CCS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flg_exp_seg_stu = models.IntegerField(db_column='FLG_EXP_SEG_STU', blank=True, null=True)  # Field name made lowercase.
    data_exp_seg_stu = models.DateTimeField(db_column='DATA_EXP_SEG_STU', blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='CDSORD_ID', unique=True, blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_CDS'


class DidatticaCdsLingua(models.Model):
    lin_did_ord_id = models.IntegerField(db_column='LIN_DID_ORD_ID', primary_key=True)  # Field name made lowercase.
    cdsord = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDSORD_ID', blank=True, null=True)  # Field name made lowercase.
    lingua_id = models.IntegerField(db_column='LINGUA_ID', blank=True, null=True)  # Field name made lowercase.
    lingua_des_it = models.CharField(db_column='LINGUA_DES_IT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    iso6392_cod = models.CharField(db_column='ISO6392_COD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lingua_des_eng = models.CharField(db_column='LINGUA_DES_ENG', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_CDS_LINGUA'


class DidatticaCopertura(models.Model):
    coper_id = models.IntegerField(db_column='COPER_ID', primary_key=True)  # Field name made lowercase.
    af = models.ForeignKey(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID', blank=True, null=True)  # Field name made lowercase.
    personale = models.ForeignKey('Personale', models.DO_NOTHING, db_column='PERSONALE_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.IntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    af_gen_des = models.CharField(db_column='AF_GEN_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    cds_id = models.IntegerField(db_column='CDS_ID', blank=True, null=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='CDSORD_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_id = models.IntegerField(db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_regdid_id = models.IntegerField(db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    af_gen_des_eng = models.CharField(db_column='AF_GEN_DES_ENG', max_length=500, blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    sett_des = models.CharField(db_column='SETT_DES', max_length=400, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=400, blank=True, null=True)  # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ore_att_front = models.IntegerField(db_column='ORE_ATT_FRONT', blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    nota = models.TextField(db_column='NOTA', blank=True, null=True)  # Field name made lowercase.
    af_radice_id = models.IntegerField(db_column='AF_RADICE_ID', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=400, blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    matricola_resp_did = models.CharField(db_column='MATRICOLA_RESP_DID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cod_fis_resp_did = models.CharField(db_column='COD_FIS_RESP_DID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(db_column='RUOLO_RESP_DID_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cognome_titolare = models.CharField(db_column='COGNOME_TITOLARE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nome_titolare = models.CharField(db_column='NOME_TITOLARE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    matricola_titolare = models.CharField(db_column='MATRICOLA_TITOLARE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_cod = models.CharField(db_column='FAT_PART_STU_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_des = models.CharField(db_column='FAT_PART_STU_DES', max_length=400, blank=True, null=True)  # Field name made lowercase.
    part_stu_cod = models.CharField(db_column='PART_STU_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    part_stu_des = models.CharField(db_column='PART_STU_DES', max_length=400, blank=True, null=True)  # Field name made lowercase.
    tipo_fat_stu_cod = models.CharField(db_column='TIPO_FAT_STU_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    part_ini = models.CharField(db_column='PART_INI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    part_fine = models.CharField(db_column='PART_FINE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    non_erogabile_flg = models.IntegerField(db_column='NON_EROGABILE_FLG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    cds_des = models.CharField(db_column='CDS_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    coper_peso = models.FloatField(db_column='COPER_PESO', blank=True, null=True)  # Field name made lowercase.
    ore = models.PositiveIntegerField(db_column='ORE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_COPERTURA'


class DidatticaCoperturaTemp(models.Model):
    aa_from = models.IntegerField(db_column='AA_FROM', blank=True, null=True)  # Field name made lowercase.
    coper_id = models.BigIntegerField(db_column='COPER_ID', blank=True, null=True)  # Field name made lowercase.
    af_id = models.BigIntegerField(db_column='AF_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.BigIntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_gen_des = models.CharField(db_column='AF_GEN_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.BigIntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    cds_id = models.BigIntegerField(db_column='CDS_ID', blank=True, null=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cds_des = models.CharField(db_column='CDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.BigIntegerField(db_column='CDSORD_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.BigIntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_id = models.BigIntegerField(db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.BigIntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_regdid_id = models.BigIntegerField(db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    of_id = models.BigIntegerField(db_column='OF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    af_gen_des_eng = models.CharField(db_column='AF_GEN_DES_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sett_des = models.CharField(db_column='SETT_DES', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb_id = models.BigIntegerField(db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ore_att_front = models.FloatField(db_column='ORE_ATT_FRONT', blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nota = models.TextField(db_column='NOTA', blank=True, null=True)  # Field name made lowercase.
    af_radice_id = models.BigIntegerField(db_column='AF_RADICE_ID', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    matricola_resp_did = models.CharField(db_column='MATRICOLA_RESP_DID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_fis_resp_did = models.CharField(db_column='COD_FIS_RESP_DID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(db_column='RUOLO_RESP_DID_COD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cognome_titolare = models.CharField(db_column='COGNOME_TITOLARE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_titolare = models.CharField(db_column='NOME_TITOLARE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    matricola_titolare = models.CharField(db_column='MATRICOLA_TITOLARE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_cod = models.CharField(db_column='FAT_PART_STU_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_des = models.CharField(db_column='FAT_PART_STU_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    part_stu_cod = models.CharField(db_column='PART_STU_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    part_stu_des = models.CharField(db_column='PART_STU_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    tipo_fat_stu_cod = models.CharField(db_column='TIPO_FAT_STU_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_ini = models.CharField(db_column='PART_INI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    part_fine = models.CharField(db_column='PART_FINE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    matricola = models.CharField(db_column='MATRICOLA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cognome = models.CharField(db_column='COGNOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    non_erogabile_flg = models.IntegerField(db_column='NON_EROGABILE_FLG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    coper_peso = models.FloatField(db_column='COPER_PESO', blank=True, null=True)  # Field name made lowercase.
    ore = models.FloatField(db_column='ORE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_COPERTURA_TEMP'


class DidatticaDipartimento(models.Model):
    dip_id = models.IntegerField(db_column='DIP_ID', primary_key=True)  # Field name made lowercase.
    dip_cod = models.CharField(db_column='DIP_COD', unique=True, max_length=40, blank=True, null=True)  # Field name made lowercase.
    dip_des_it = models.CharField(db_column='DIP_DES_IT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dip_des_eng = models.CharField(db_column='DIP_DES_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dip_nome_breve = models.CharField(db_column='DIP_NOME_BREVE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dip_cd_csa = models.CharField(db_column='DIP_CD_CSA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    miur_dip_id = models.IntegerField(db_column='MIUR_DIP_ID', blank=True, null=True)  # Field name made lowercase.
    url_pubbl_off_f = models.CharField(db_column='URL_PUBBL_OFF_F', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dip_vis_web_flg = models.IntegerField(db_column='DIP_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_DIPARTIMENTO'


class DidatticaDottoratoCds(models.Model):
    dip_cod = models.ForeignKey(DidatticaDipartimento, models.DO_NOTHING, db_column='DIP_COD', blank=True, null=True)  # Field name made lowercase.
    cds_id_esse3 = models.IntegerField(db_column='CDS_ID_ESSE3', primary_key=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nome_cds_it = models.CharField(db_column='NOME_CDS_IT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rif_cod = models.CharField(db_column='RIF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rif_des = models.CharField(db_column='RIF_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    durata_anni = models.IntegerField(db_column='DURATA_ANNI', blank=True, null=True)  # Field name made lowercase.
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    tipo_titit_cod = models.CharField(db_column='TIPO_TITIT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_titit_des = models.CharField(db_column='TIPO_TITIT_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_spec_cod = models.CharField(db_column='TIPO_SPEC_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_spec_des = models.CharField(db_column='TIPO_SPEC_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    istat_cod = models.CharField(db_column='ISTAT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    max_punti = models.IntegerField(db_column='MAX_PUNTI', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    aa_att_id = models.IntegerField(db_column='AA_ATT_ID', blank=True, null=True)  # Field name made lowercase.
    aa_dis_id = models.IntegerField(db_column='AA_DIS_ID', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cds_url_info_web = models.CharField(db_column='CDS_URL_INFO_WEB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cds_vis_web_flg = models.IntegerField(db_column='CDS_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    cdsord_id_esse3 = models.IntegerField(db_column='CDSORD_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')  # Field name made lowercase.
    cdsord_des = models.CharField(db_column='CDSORD_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_DOTTORATO_CDS'
        unique_together = (('cds_id_esse3', 'aa_ord_id'),)


class DidatticaDottoratoPds(models.Model):
    cds_id_esse3 = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='CDS_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    aa_ord = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    pds_id_esse3 = models.IntegerField(db_column='PDS_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    pdsord_id_esse3 = models.IntegerField(db_column='PDSORD_ID_ESSE3', primary_key=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indir = models.CharField(db_column='INDIR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    orien = models.CharField(db_column='ORIEN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    stato_cod = models.CharField(db_column='STATO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    data_var = models.DateTimeField(db_column='DATA_VAR', blank=True, null=True)  # Field name made lowercase.
    val_min_tesi = models.IntegerField(db_column='VAL_MIN_TESI', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_DOTTORATO_PDS'


class DidatticaDottoratoRegolamento(models.Model):
    regdid_id_esse3 = models.IntegerField(db_column='REGDID_ID_ESSE3', primary_key=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    cds_id_esse3 = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='CDS_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regdid_des = models.CharField(db_column='REGDID_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_piani_studio = models.IntegerField(db_column='NUMERO_PIANI_STUDIO', blank=True, null=True)  # Field name made lowercase.
    frequenza_obbligatoria = models.IntegerField(db_column='FREQUENZA_OBBLIGATORIA', blank=True, null=True)  # Field name made lowercase.
    num_ciclo = models.IntegerField(db_column='NUM_CICLO', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    aa_ord = models.ForeignKey(DidatticaDottoratoCds, models.DO_NOTHING, db_column='AA_ORD_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_DOTTORATO_REGOLAMENTO'


class DidatticaPdsRegolamento(models.Model):
    pds_regdid_id = models.IntegerField(db_column='PDS_REGDID_ID', primary_key=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pds_des_it = models.CharField(db_column='PDS_DES_IT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_des_eng = models.CharField(db_column='PDS_DES_ENG', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_PDS_REGOLAMENTO'


class DidatticaRegolamento(models.Model):
    regdid_id = models.IntegerField(db_column='REGDID_ID', primary_key=True)  # Field name made lowercase.
    aa_reg_did = models.IntegerField(db_column='AA_REG_DID', blank=True, null=True)  # Field name made lowercase.
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID', blank=True, null=True)  # Field name made lowercase.
    stato_regdid_cod = models.CharField(db_column='STATO_REGDID_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stato_regdid_des = models.CharField(db_column='STATO_REGDID_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    numero_piani_studio = models.IntegerField(db_column='NUMERO_PIANI_STUDIO', blank=True, null=True)  # Field name made lowercase.
    anno_scelta_pds = models.IntegerField(db_column='ANNO_SCELTA_PDS', blank=True, null=True)  # Field name made lowercase.
    modalita_erogazione = models.CharField(db_column='MODALITA_EROGAZIONE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    frequenza_obbligatoria = models.IntegerField(db_column='FREQUENZA_OBBLIGATORIA', blank=True, null=True)  # Field name made lowercase.
    titolo_congiunto_cod = models.CharField(db_column='TITOLO_CONGIUNTO_COD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_REGOLAMENTO'


class DidatticaTestiAf(models.Model):
    af = models.OneToOneField(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID', primary_key=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    testi_af_id = models.IntegerField(db_column='TESTI_AF_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_testo_af_cod = models.CharField(db_column='TIPO_TESTO_AF_COD', max_length=100)  # Field name made lowercase.
    tipo_testo_af_des = models.TextField(db_column='TIPO_TESTO_AF_DES', blank=True, null=True)  # Field name made lowercase.
    tipo_testo_af_etic = models.CharField(db_column='TIPO_TESTO_AF_ETIC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_testo_af_etic_eng = models.TextField(db_column='TIPO_TESTO_AF_ETIC_ENG', blank=True, null=True)  # Field name made lowercase.
    obbl_flg = models.IntegerField(db_column='OBBL_FLG', blank=True, null=True)  # Field name made lowercase.
    testo_af_ita = models.TextField(db_column='TESTO_AF_ITA', blank=True, null=True)  # Field name made lowercase.
    testo_af_short_ita = models.TextField(db_column='TESTO_AF_SHORT_ITA', blank=True, null=True)  # Field name made lowercase.
    testo_af_fmt_ita = models.TextField(db_column='TESTO_AF_FMT_ITA', blank=True, null=True)  # Field name made lowercase.
    dt_ins_txt_clob_ita = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ITA', blank=True, null=True)  # Field name made lowercase.
    dt_mod_txt_clob_ita = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ITA', blank=True, null=True)  # Field name made lowercase.
    testo_af_eng = models.TextField(db_column='TESTO_AF_ENG', blank=True, null=True)  # Field name made lowercase.
    testo_af_short_eng = models.TextField(db_column='TESTO_AF_SHORT_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_ins_txt_clob_eng = models.TextField(db_column='DT_INS_TXT_CLOB_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_mod_txt_clob_eng = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    dt_ins_mod_max = models.DateTimeField(db_column='DT_INS_MOD_MAX', blank=True, null=True)  # Field name made lowercase.
    testo_af_fmt_eng = models.TextField(db_column='TESTO_AF_FMT_ENG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_TESTI_AF'
        unique_together = (('af', 'tipo_testo_af_cod'),)


class DidatticaTestiRegolamento(models.Model):
    txt_id = models.IntegerField(db_column='TXT_ID', primary_key=True)  # Field name made lowercase.
    regdid = models.ForeignKey(DidatticaRegolamento, models.DO_NOTHING, db_column='REGDID_ID')  # Field name made lowercase.
    tipo_testo_regdid_cod = models.CharField(db_column='TIPO_TESTO_REGDID_COD', max_length=100)  # Field name made lowercase.
    tipo_testo_regdid_des = models.CharField(db_column='TIPO_TESTO_REGDID_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clob_txt_ita = models.TextField(db_column='CLOB_TXT_ITA', blank=True, null=True)  # Field name made lowercase.
    clob_txt_eng = models.TextField(db_column='CLOB_TXT_ENG', blank=True, null=True)  # Field name made lowercase.
    profilo = models.TextField(db_column='PROFILO', blank=True, null=True)  # Field name made lowercase.
    profilo_eng = models.TextField(db_column='PROFILO_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_ins_txt_clob_ita = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ITA', blank=True, null=True)  # Field name made lowercase.
    dt_ins_txt_clob_eng = models.DateTimeField(db_column='DT_INS_TXT_CLOB_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    dt_mod_txt_clob_ita = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ITA', blank=True, null=True)  # Field name made lowercase.
    dt_mod_txt_clob_eng = models.DateTimeField(db_column='DT_MOD_TXT_CLOB_ENG', blank=True, null=True)  # Field name made lowercase.
    testo_regdid_url = models.CharField(db_column='TESTO_REGDID_URL', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIDATTICA_TESTI_REGOLAMENTO'


class DriveEtl(models.Model):
    dt_last_load = models.DateField(db_column='DT_LAST_LOAD')  # Field name made lowercase.
    aa_from = models.IntegerField(db_column='AA_FROM')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DRIVE_ETL'


class LaboratorioAltriDipartimenti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey('LaboratorioDatiBase', models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    id_dip = models.ForeignKey(DidatticaDipartimento, models.DO_NOTHING, db_column='id_dip', blank=True, null=True)
    descr_dip_lab = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LABORATORIO_ALTRI_DIPARTIMENTI'


class LaboratorioAttivita(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey('LaboratorioDatiBase', models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    id_tipologia_attivita = models.ForeignKey('LaboratorioTipologiaAttivita', models.DO_NOTHING, db_column='ID_TIPOLOGIA_ATTIVITA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_ATTIVITA'


class LaboratorioAttrezzature(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey('LaboratorioDatiBase', models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    tipologia = models.CharField(db_column='TIPOLOGIA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    fondi = models.CharField(db_column='FONDI', max_length=500, blank=True, null=True)  # Field name made lowercase.
    costo_unitario = models.FloatField(db_column='COSTO_UNITARIO', blank=True, null=True)  # Field name made lowercase.
    quantita = models.IntegerField(db_column='QUANTITA', blank=True, null=True)  # Field name made lowercase.
    tipo_rischi = models.CharField(db_column='TIPO_RISCHI', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_ATTREZZATURE'


class LaboratorioDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt_sottomissione = models.DateTimeField(db_column='DT_SOTTOMISSIONE', blank=True, null=True)  # Field name made lowercase.
    referente_compilazione = models.CharField(db_column='REFERENTE_COMPILAZIONE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    matricola_referente_compilazione = models.ForeignKey('Personale', models.DO_NOTHING, db_column='MATRICOLA_REFERENTE_COMPILAZIONE', blank=True, null=True)  # Field name made lowercase.
    email_compilazione = models.CharField(db_column='EMAIL_COMPILAZIONE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nome_laboratorio = models.CharField(db_column='NOME_LABORATORIO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    acronimo = models.CharField(db_column='ACRONIMO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    logo_laboratorio = models.CharField(db_column='LOGO_LABORATORIO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    dipartimento_riferimento = models.CharField(db_column='DIPARTIMENTO_RIFERIMENTO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    id_dipartimento_riferimento = models.ForeignKey(DidatticaDipartimento, models.DO_NOTHING, db_column='ID_DIPARTIMENTO_RIFERIMENTO', blank=True, null=True)  # Field name made lowercase.
    laboratorio_interdipartimentale = models.CharField(db_column='LABORATORIO_INTERDIPARTIMENTALE', max_length=400, blank=True, null=True)  # Field name made lowercase.
    altre_strutture_riferimento = models.CharField(db_column='ALTRE_STRUTTURE_RIFERIMENTO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    descr_altre_strutture_riferimento_it = models.TextField(db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_IT', blank=True, null=True)  # Field name made lowercase.
    descr_altre_strutture_riferimento_en = models.TextField(db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_EN', blank=True, null=True)  # Field name made lowercase.
    ambito = models.CharField(db_column='AMBITO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    finalita_ricerca_it = models.TextField(db_column='FINALITA_RICERCA_IT', blank=True, null=True)  # Field name made lowercase.
    finalita_ricerca_en = models.TextField(db_column='FINALITA_RICERCA_EN', blank=True, null=True)  # Field name made lowercase.
    finalita_didattica_it = models.TextField(db_column='FINALITA_DIDATTICA_IT', blank=True, null=True)  # Field name made lowercase.
    finalita_didattica_en = models.TextField(db_column='FINALITA_DIDATTICA_EN', blank=True, null=True)  # Field name made lowercase.
    finalita_servizi_it = models.TextField(db_column='FINALITA_SERVIZI_IT', blank=True, null=True)  # Field name made lowercase.
    finalita_servizi_en = models.TextField(db_column='FINALITA_SERVIZI_EN', blank=True, null=True)  # Field name made lowercase.
    responsabile_scientifico = models.CharField(db_column='RESPONSABILE_SCIENTIFICO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    matricola_responsabile_scientifico = models.ForeignKey('Personale', models.DO_NOTHING, db_column='MATRICOLA_RESPONSABILE_SCIENTIFICO', blank=True, null=True)  # Field name made lowercase.
    sede_dimensione = models.CharField(db_column='SEDE_DIMENSIONE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sede_note_descrittive = models.TextField(db_column='SEDE_NOTE_DESCRITTIVE', blank=True, null=True)  # Field name made lowercase.
    strumentazione_descrizione = models.TextField(db_column='STRUMENTAZIONE_DESCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    strumentazione_valore = models.CharField(db_column='STRUMENTAZIONE_VALORE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    preposto_sicurezza = models.CharField(db_column='PREPOSTO_SICUREZZA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    matricola_preposto_sicurezza = models.ForeignKey('Personale', models.DO_NOTHING, db_column='MATRICOLA_PREPOSTO_SICUREZZA', blank=True, null=True)  # Field name made lowercase.
    sito_web = models.CharField(db_column='SITO_WEB', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    id_infrastruttura_riferimento = models.ForeignKey('LaboratorioInfrastruttura', models.DO_NOTHING, db_column='ID_INFRASTRUTTURA_RIFERIMENTO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_DATI_BASE'


class LaboratorioDatiErc1(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    id_ricerca_erc1 = models.ForeignKey('RicercaErc1', models.DO_NOTHING, db_column='ID_RICERCA_ERC1', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_DATI_ERC1'


class LaboratorioInfrastruttura(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_INFRASTRUTTURA'


class LaboratorioPersonaleRicerca(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    matricola_personale_ricerca = models.CharField(db_column='MATRICOLA_PERSONALE_RICERCA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cognomenome_origine = models.CharField(db_column='COGNOMENOME_ORIGINE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_PERSONALE_RICERCA'


class LaboratorioPersonaleTecnico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    matricola_personale_tecnico = models.CharField(db_column='MATRICOLA_PERSONALE_TECNICO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ruolo = models.CharField(db_column='RUOLO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    field_impegno = models.FloatField(db_column='%IMPEGNO', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    cognomenome_origine = models.CharField(db_column='COGNOMENOME_ORIGINE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_PERSONALE_TECNICO'


class LaboratorioServiziErogati(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    matricola_responsabile = models.CharField(db_column='MATRICOLA_RESPONSABILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    responsabile_origine = models.CharField(db_column='RESPONSABILE_ORIGINE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    committenti = models.CharField(db_column='COMMITTENTI', max_length=500, blank=True, null=True)  # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)  # Field name made lowercase.
    durata_mesi = models.IntegerField(db_column='DURATA_MESI', blank=True, null=True)  # Field name made lowercase.
    importo_euro = models.FloatField(db_column='IMPORTO_EURO', blank=True, null=True)  # Field name made lowercase.
    strumentazione = models.TextField(db_column='STRUMENTAZIONE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_SERVIZI_EROGATI'


class LaboratorioServiziOfferti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    nome_servizio = models.TextField(db_column='NOME_SERVIZIO', blank=True, null=True)  # Field name made lowercase.
    descrizione_servizio = models.TextField(db_column='DESCRIZIONE_SERVIZIO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_SERVIZI_OFFERTI'


class LaboratorioTipologiaAttivita(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_TIPOLOGIA_ATTIVITA'


class LaboratorioTipologiaRischio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    tipologia_rischio = models.CharField(db_column='TIPOLOGIA_RISCHIO', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_TIPOLOGIA_RISCHIO'


class LaboratorioUbicazione(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_laboratorio_dati = models.ForeignKey(LaboratorioDatiBase, models.DO_NOTHING, db_column='ID_LABORATORIO_DATI', blank=True, null=True)  # Field name made lowercase.
    edificio = models.CharField(db_column='EDIFICIO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    piano = models.CharField(db_column='PIANO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sede_principale = models.CharField(db_column='SEDE_PRINCIPALE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='NOTE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LABORATORIO_UBICAZIONE'


class Personale(models.Model):
    id_ab = models.IntegerField(db_column='ID_AB', unique=True)  # Field name made lowercase.
    cd_esterno = models.CharField(db_column='CD_ESTERNO', max_length=60, blank=True, null=True)  # Field name made lowercase.
    matricola = models.CharField(db_column='MATRICOLA', unique=True, max_length=6)  # Field name made lowercase.
    matricola_sp = models.CharField(db_column='MATRICOLA_SP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cognome = models.CharField(db_column='COGNOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    middle_name = models.CharField(db_column='MIDDLE_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cod_fis = models.CharField(db_column='COD_FIS', unique=True, max_length=16, blank=True, null=True)  # Field name made lowercase.
    cd_genere = models.CharField(db_column='CD_GENERE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt_nascita = models.DateField(db_column='DT_NASCITA', blank=True, null=True)  # Field name made lowercase.
    id_comu_nasc = models.IntegerField(db_column='ID_COMU_NASC', blank=True, null=True)  # Field name made lowercase.
    ds_cittstra_nasc = models.CharField(db_column='DS_CITTSTRA_NASC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_comune_nasc = models.CharField(db_column='DS_COMUNE_NASC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_prov_nasc = models.CharField(db_column='DS_PROV_NASC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_sigla_nasc = models.CharField(db_column='CD_SIGLA_NASC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    id_nazione_nasc = models.IntegerField(db_column='ID_NAZIONE_NASC', blank=True, null=True)  # Field name made lowercase.
    ds_nazi_nasc = models.CharField(db_column='DS_NAZI_NASC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ds_nazi_breve_nasc = models.CharField(db_column='DS_NAZI_BREVE_NASC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    id_comu_res = models.ForeignKey(ComuniAll, models.DO_NOTHING, db_column='ID_COMU_RES', blank=True, null=True)  # Field name made lowercase.
    ds_comune_res = models.CharField(db_column='DS_COMUNE_RES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_cap_res = models.CharField(db_column='CD_CAP_RES', max_length=5, blank=True, null=True)  # Field name made lowercase.
    indirizzo_res = models.CharField(db_column='INDIRIZZO_RES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num_civico_res = models.CharField(db_column='NUM_CIVICO_RES', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cd_sigla_res = models.CharField(db_column='CD_SIGLA_RES', max_length=2, blank=True, null=True)  # Field name made lowercase.
    id_comu_dom = models.IntegerField(db_column='ID_COMU_DOM', blank=True, null=True)  # Field name made lowercase.
    ds_comune_dom = models.CharField(db_column='DS_COMUNE_DOM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_cap_dom = models.CharField(db_column='CD_CAP_DOM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    indirizzo_dom = models.CharField(db_column='INDIRIZZO_DOM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num_civico_dom = models.CharField(db_column='NUM_CIVICO_DOM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cd_sigla_dom = models.CharField(db_column='CD_SIGLA_DOM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cd_comparto = models.CharField(db_column='CD_COMPARTO', max_length=1)  # Field name made lowercase.
    ds_comparto = models.CharField(db_column='DS_COMPARTO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4)  # Field name made lowercase.
    ds_ruolo = models.CharField(db_column='DS_RUOLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ds_ruolo_locale = models.CharField(db_column='DS_RUOLO_LOCALE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    peso_ruolo = models.DecimalField(db_column='PESO_RUOLO', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dt_rap_ini = models.DateField(db_column='DT_RAP_INI', blank=True, null=True)  # Field name made lowercase.
    dt_rap_fin = models.DateField(db_column='DT_RAP_FIN', blank=True, null=True)  # Field name made lowercase.
    cd_ssd = models.CharField(db_column='CD_SSD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ds_ssd = models.CharField(db_column='DS_SSD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cd_fac = models.CharField(db_column='CD_FAC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ds_fac = models.CharField(db_column='DS_FAC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_uo_aff_org = models.ForeignKey('UnitaOrganizzativa', models.DO_NOTHING, db_column='CD_UO_AFF_ORG', blank=True, null=True)  # Field name made lowercase.
    ds_aff_org = models.CharField(db_column='DS_AFF_ORG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org_breve = models.CharField(db_column='DS_AFF_ORG_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cd_csa_aff_org2 = models.CharField(db_column='CD_CSA_AFF_ORG2', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org2 = models.CharField(db_column='DS_AFF_ORG2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org2_breve = models.CharField(db_column='DS_AFF_ORG2_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cd_csa_aff_org3 = models.CharField(db_column='CD_CSA_AFF_ORG3', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org3 = models.CharField(db_column='DS_AFF_ORG3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org3_breve = models.CharField(db_column='DS_AFF_ORG3_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cd_csa_aff_org4 = models.CharField(db_column='CD_CSA_AFF_ORG4', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org4 = models.CharField(db_column='DS_AFF_ORG4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org4_breve = models.CharField(db_column='DS_AFF_ORG4_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sede = models.CharField(db_column='SEDE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_sede = models.CharField(db_column='DS_SEDE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_sede_breve = models.CharField(db_column='DS_SEDE_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    profilo = models.CharField(db_column='PROFILO', max_length=11, blank=True, null=True)  # Field name made lowercase.
    ds_profilo = models.CharField(db_column='DS_PROFILO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ds_profilo_breve = models.CharField(db_column='DS_PROFILO_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cd_ateneo_corr = models.CharField(db_column='CD_ATENEO_CORR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ds_ateneo_corr = models.CharField(db_column='DS_ATENEO_CORR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_ini_rap_univ = models.DateField(db_column='DT_INI_RAP_UNIV', blank=True, null=True)  # Field name made lowercase.
    dt_fin_rap_univ = models.DateField(db_column='DT_FIN_RAP_UNIV', blank=True, null=True)  # Field name made lowercase.
    telrif = models.CharField(db_column='TELRIF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    urlcv = models.CharField(db_column='URLCV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fl_docente = models.PositiveIntegerField(db_column='FL_DOCENTE', blank=True, null=True)  # Field name made lowercase.
    cd_anagrafico = models.CharField(db_column='CD_ANAGRAFICO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inquadr = models.CharField(db_column='INQUADR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    badge = models.CharField(db_column='BADGE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tempo = models.CharField(db_column='TEMPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    id_contratto = models.IntegerField(db_column='ID_CONTRATTO', blank=True, null=True)  # Field name made lowercase.
    flg_cessato = models.IntegerField(db_column='FLG_CESSATO', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, db_column='USER_INS_ID', blank=True, null=True)  # Field name made lowercase.
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, db_column='USER_MOD_ID', blank=True, null=True)  # Field name made lowercase.
    cv_full_it = models.TextField(db_column='CV_FULL_IT', blank=True, null=True)  # Field name made lowercase.
    cv_short_it = models.TextField(db_column='CV_SHORT_IT', blank=True, null=True)  # Field name made lowercase.
    cv_full_eng = models.TextField(db_column='CV_FULL_ENG', blank=True, null=True)  # Field name made lowercase.
    cv_short_eng = models.TextField(db_column='CV_SHORT_ENG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PERSONALE'


class PersonaleContatti(models.Model):
    id_ab = models.IntegerField(db_column='ID_AB', primary_key=True)  # Field name made lowercase.
    cod_fis = models.ForeignKey(Personale, models.DO_NOTHING, db_column='COD_FIS', blank=True, null=True)  # Field name made lowercase.
    cd_tipo_cont = models.ForeignKey('PersonaleUoTipoContatto', models.DO_NOTHING, db_column='CD_TIPO_CONT')  # Field name made lowercase.
    contatto = models.CharField(db_column='CONTATTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prg_priorita = models.IntegerField(db_column='PRG_PRIORITA')  # Field name made lowercase.
    dt_ins_mod = models.DateField(db_column='DT_INS_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PERSONALE_CONTATTI'
        unique_together = (('id_ab', 'cd_tipo_cont', 'prg_priorita'),)


class PersonaleUoTipoContatto(models.Model):
    cod_contatto = models.CharField(db_column='COD_CONTATTO', primary_key=True, max_length=20)  # Field name made lowercase.
    descr_contatto = models.CharField(db_column='DESCR_CONTATTO', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PERSONALE_UO_TIPO_CONTATTO'


class ProgettoAmbitoTerritoriale(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ambito_territoriale = models.CharField(db_column='AMBITO_TERRITORIALE', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROGETTO_AMBITO_TERRITORIALE'


class ProgettoDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    anno_avvio = models.IntegerField(db_column='ANNO_AVVIO', blank=True, null=True)  # Field name made lowercase.
    id_ambito_territoriale = models.ForeignKey(ProgettoAmbitoTerritoriale, models.DO_NOTHING, db_column='ID_AMBITO_TERRITORIALE', blank=True, null=True)  # Field name made lowercase.
    id_tipologia_programma = models.ForeignKey('ProgettoTipologiaProgramma', models.DO_NOTHING, db_column='ID_TIPOLOGIA_PROGRAMMA', blank=True, null=True)  # Field name made lowercase.
    id_area_tecnologica = models.ForeignKey('TipologiaAreaTecnologica', models.DO_NOTHING, db_column='ID_AREA_TECNOLOGICA', blank=True, null=True)  # Field name made lowercase.
    id_dipartimento = models.IntegerField(db_column='ID_DIPARTIMENTO', blank=True, null=True)  # Field name made lowercase.
    titolo = models.CharField(db_column='TITOLO', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    descr_breve = models.TextField(db_column='DESCR_BREVE', blank=True, null=True)  # Field name made lowercase.
    url_immagine = models.CharField(db_column='URL_IMMAGINE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    abstract_ita = models.TextField(db_column='ABSTRACT_ITA', blank=True, null=True)  # Field name made lowercase.
    abstract_eng = models.TextField(db_column='ABSTRACT_ENG', blank=True, null=True)  # Field name made lowercase.
    url_sito_web = models.CharField(db_column='URL_SITO_WEB', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROGETTO_DATI_BASE'


class ProgettoResponsabileScientifico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola = models.ForeignKey(Personale, models.DO_NOTHING, db_column='MATRICOLA', blank=True, null=True)  # Field name made lowercase.
    nome_origine = models.CharField(db_column='NOME_ORIGINE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    id_progetto = models.IntegerField(db_column='ID_PROGETTO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROGETTO_RESPONSABILE_SCIENTIFICO'


class ProgettoTipologiaProgramma(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_programma = models.CharField(db_column='NOME_PROGRAMMA', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROGETTO_TIPOLOGIA_PROGRAMMA'


class PubblicazioneAutori(models.Model):
    item = models.ForeignKey('PubblicazioneDatiBase', models.DO_NOTHING, db_column='ITEM_ID')  # Field name made lowercase.
    codice_fiscale = models.CharField(db_column='CODICE_FISCALE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    id_ab = models.ForeignKey(Personale, models.DO_NOTHING, db_column='ID_AB', blank=True, null=True)  # Field name made lowercase.
    first_name = models.CharField(db_column='FIRST_NAME', max_length=1020, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='LAST_NAME', max_length=1020, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBBLICAZIONE_AUTORI'


class PubblicazioneCollection(models.Model):
    collection_id = models.IntegerField(db_column='COLLECTION_ID', primary_key=True)  # Field name made lowercase.
    community = models.ForeignKey('PubblicazioneCommunity', models.DO_NOTHING, db_column='COMMUNITY_ID', blank=True, null=True)  # Field name made lowercase.
    collection_name = models.CharField(db_column='COLLECTION_NAME', max_length=512, blank=True, null=True)  # Field name made lowercase.
    type_miur = models.CharField(db_column='TYPE_MIUR', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBBLICAZIONE_COLLECTION'


class PubblicazioneCommunity(models.Model):
    community_id = models.IntegerField(db_column='COMMUNITY_ID', primary_key=True)  # Field name made lowercase.
    community_name = models.CharField(db_column='COMMUNITY_NAME', max_length=512, blank=True, null=True)  # Field name made lowercase.
    parent_community_id = models.IntegerField(db_column='PARENT_COMMUNITY_ID', blank=True, null=True)  # Field name made lowercase.
    parent_community_name = models.CharField(db_column='PARENT_COMMUNITY_NAME', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBBLICAZIONE_COMMUNITY'


class PubblicazioneDatiBase(models.Model):
    item_id = models.IntegerField(db_column='ITEM_ID', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='TITLE', blank=True, null=True)  # Field name made lowercase.
    des_abstract = models.TextField(db_column='DES_ABSTRACT', blank=True, null=True)  # Field name made lowercase.
    des_abstracteng = models.TextField(db_column='DES_ABSTRACTENG', blank=True, null=True)  # Field name made lowercase.
    lan_iso = models.CharField(db_column='LAN_ISO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lan_iso_i18n = models.CharField(db_column='LAN_ISO_I18N', max_length=400, blank=True, null=True)  # Field name made lowercase.
    collection = models.ForeignKey(PubblicazioneCollection, models.DO_NOTHING, db_column='COLLECTION_ID', blank=True, null=True)  # Field name made lowercase.
    date_issued_year = models.IntegerField(db_column='DATE_ISSUED_YEAR', blank=True, null=True)  # Field name made lowercase.
    pubblicazione = models.CharField(db_column='PUBBLICAZIONE', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    label_pubblicazione = models.CharField(db_column='LABEL_PUBBLICAZIONE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contributors = models.TextField(db_column='CONTRIBUTORS', blank=True, null=True)  # Field name made lowercase.
    url_pubblicazione = models.CharField(db_column='URL_PUBBLICAZIONE', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBBLICAZIONE_DATI_BASE'


class RicercaAster1(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    ricerca_erc0_cod = models.ForeignKey('RicercaErc0', models.DO_NOTHING, db_column='RICERCA_ERC0_COD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RICERCA_ASTER1'


class RicercaAster2(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)  # Field name made lowercase.
    ricerca_aster1 = models.ForeignKey(RicercaAster1, models.DO_NOTHING, db_column='RICERCA_ASTER1_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_ASTER2'


class RicercaDocenteGruppo(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)  # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)  # Field name made lowercase.
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True, null=True)  # Field name made lowercase.
    ricerca_gruppo = models.ForeignKey('RicercaGruppo', models.DO_NOTHING, db_column='RICERCA_GRUPPO_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_DOCENTE_GRUPPO'


class RicercaDocenteLineaApplicata(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)  # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)  # Field name made lowercase.
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True, null=True)  # Field name made lowercase.
    ricerca_linea_applicata = models.ForeignKey('RicercaLineaApplicata', models.DO_NOTHING, db_column='RICERCA_LINEA_APPLICATA_ID', blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_DOCENTE_LINEA_APPLICATA'


class RicercaDocenteLineaBase(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)  # Field name made lowercase.
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)  # Field name made lowercase.
    personale = models.ForeignKey(Personale, models.DO_NOTHING, db_column='PERSONALE_ID', blank=True, null=True)  # Field name made lowercase.
    ricerca_linea_base = models.ForeignKey('RicercaLineaBase', models.DO_NOTHING, db_column='RICERCA_LINEA_BASE_ID', blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_DOCENTE_LINEA_BASE'


class RicercaErc0(models.Model):
    erc0_cod = models.CharField(db_column='ERC0_COD', primary_key=True, max_length=2)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100)  # Field name made lowercase.
    description_en = models.CharField(db_column='DESCRIPTION_EN', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RICERCA_ERC0'


class RicercaErc1(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    cod_erc1 = models.CharField(db_column='COD_ERC1', unique=True, max_length=40)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    ricerca_erc0_cod = models.ForeignKey(RicercaErc0, models.DO_NOTHING, db_column='RICERCA_ERC0_COD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RICERCA_ERC1'


class RicercaErc2(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    cod_erc2 = models.CharField(db_column='COD_ERC2', unique=True, max_length=60)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')  # Field name made lowercase.
    ricerca_erc1 = models.ForeignKey(RicercaErc1, models.DO_NOTHING, db_column='RICERCA_ERC1_ID', blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_ERC2'


class RicercaGruppo(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=200)  # Field name made lowercase.
    descrizione = models.TextField(db_column='DESCRIZIONE')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_GRUPPO'


class RicercaLineaApplicata(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)  # Field name made lowercase.
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO', blank=True, null=True)  # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)  # Field name made lowercase.
    ricerca_aster2 = models.ForeignKey(RicercaAster2, models.DO_NOTHING, db_column='RICERCA_ASTER2_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_LINEA_APPLICATA'


class RicercaLineaBase(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)  # Field name made lowercase.
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO', blank=True, null=True)  # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)  # Field name made lowercase.
    ricerca_erc2 = models.ForeignKey(RicercaErc2, models.DO_NOTHING, db_column='RICERCA_ERC2_ID')  # Field name made lowercase.
    user_ins = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)
    user_mod = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RICERCA_LINEA_BASE'


class SpinoffStartupAreaInnovazioneS3Calabria(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_area_s3 = models.CharField(db_column='DESCR_AREA_S3', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPINOFF_STARTUP_AREA_INNOVAZIONE_S3_CALABRIA'


class SpinoffStartupDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    piva = models.CharField(db_column='PIVA', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nome_azienda = models.CharField(db_column='NOME_AZIENDA', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    url_immagine = models.CharField(db_column='URL_IMMAGINE', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    descrizione_ita = models.TextField(db_column='DESCRIZIONE_ITA', blank=True, null=True)  # Field name made lowercase.
    descrizione_eng = models.TextField(db_column='DESCRIZIONE_ENG', blank=True, null=True)  # Field name made lowercase.
    url_sito_web = models.CharField(db_column='URL_SITO_WEB', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    referente_unical = models.CharField(db_column='REFERENTE_UNICAL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    matricola_referente_unical = models.ForeignKey(Personale, models.DO_NOTHING, db_column='MATRICOLA_REFERENTE_UNICAL', blank=True, null=True)  # Field name made lowercase.
    ceo = models.CharField(db_column='CEO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    id_area_tecnologica = models.ForeignKey('TipologiaAreaTecnologica', models.DO_NOTHING, db_column='ID_AREA_TECNOLOGICA', blank=True, null=True)  # Field name made lowercase.
    id_area_innovazione_s3_calabria = models.ForeignKey(SpinoffStartupAreaInnovazioneS3Calabria, models.DO_NOTHING, db_column='ID_AREA_INNOVAZIONE_S3_CALABRIA', blank=True, null=True)  # Field name made lowercase.
    is_startup = models.PositiveIntegerField(db_column='IS_STARTUP', blank=True, null=True)  # Field name made lowercase.
    is_spinoff = models.PositiveIntegerField(db_column='IS_SPINOFF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPINOFF_STARTUP_DATI_BASE'


class TerritorioIt(models.Model):
    cd_catasto = models.OneToOneField(ComuniAll, models.DO_NOTHING, db_column='CD_CATASTO', primary_key=True)  # Field name made lowercase.
    cd_istat = models.CharField(db_column='CD_ISTAT', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_comune = models.CharField(db_column='DS_COMUNE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_sigla = models.CharField(db_column='CD_SIGLA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_provincia = models.CharField(db_column='DS_PROVINCIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_770_regio = models.CharField(db_column='CD_770_REGIO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_regione = models.CharField(db_column='DS_REGIONE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TERRITORIO_IT'


class TipologiaAreaTecnologica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_area_ita = models.CharField(db_column='DESCR_AREA_ITA', max_length=1000)  # Field name made lowercase.
    descr_area_eng = models.CharField(db_column='DESCR_AREA_ENG', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIPOLOGIA_AREA_TECNOLOGICA'


class UnitaOrganizzativa(models.Model):
    uo = models.CharField(db_column='UO', primary_key=True, max_length=40)  # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB', unique=True)  # Field name made lowercase.
    cd_tipo_nodo = models.CharField(db_column='CD_TIPO_NODO', max_length=10)  # Field name made lowercase.
    ds_tipo_nodo = models.CharField(db_column='DS_TIPO_NODO', max_length=255)  # Field name made lowercase.
    denominazione = models.CharField(db_column='DENOMINAZIONE', max_length=255)  # Field name made lowercase.
    nome_esteso = models.CharField(db_column='NOME_ESTESO', max_length=255)  # Field name made lowercase.
    nome_breve = models.CharField(db_column='NOME_BREVE', max_length=50)  # Field name made lowercase.
    dt_inizio_val = models.DateTimeField(db_column='DT_INIZIO_VAL', blank=True, null=True)  # Field name made lowercase.
    dt_fine_val = models.DateTimeField(db_column='DT_FINE_VAL', blank=True, null=True)  # Field name made lowercase.
    dt_creazione = models.DateTimeField(db_column='DT_CREAZIONE', blank=True, null=True)  # Field name made lowercase.
    uo_padre = models.CharField(db_column='UO_PADRE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    id_ab_padre = models.IntegerField(db_column='ID_AB_PADRE', blank=True, null=True)  # Field name made lowercase.
    cd_tipo_nodo_padre = models.CharField(db_column='CD_TIPO_NODO_PADRE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ds_tipo_nodo_padre = models.CharField(db_column='DS_TIPO_NODO_PADRE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cd_macrotipo_nodo_padre = models.CharField(db_column='CD_MACROTIPO_NODO_PADRE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    denominazione_padre = models.CharField(db_column='DENOMINAZIONE_PADRE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome_esteso_padre = models.CharField(db_column='NOME_ESTESO_PADRE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome_breve_padre = models.CharField(db_column='NOME_BREVE_PADRE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dt_inizio_val_padre = models.DateTimeField(db_column='DT_INIZIO_VAL_PADRE', blank=True, null=True)  # Field name made lowercase.
    dt_fine_val_padre = models.DateTimeField(db_column='DT_FINE_VAL_PADRE', blank=True, null=True)  # Field name made lowercase.
    dt_creazione_padre = models.DateTimeField(db_column='DT_CREAZIONE_PADRE', blank=True, null=True)  # Field name made lowercase.
    cd_csa = models.CharField(db_column='CD_CSA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ds_mission = models.TextField(db_column='DS_MISSION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNITA_ORGANIZZATIVA'


class UnitaOrganizzativaContatti(models.Model):
    id_ab = models.OneToOneField(UnitaOrganizzativa, models.DO_NOTHING, db_column='ID_AB', primary_key=True)  # Field name made lowercase.
    cd_tipo_cont = models.ForeignKey(PersonaleUoTipoContatto, models.DO_NOTHING, db_column='CD_TIPO_CONT')  # Field name made lowercase.
    contatto = models.CharField(db_column='CONTATTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prg_priorita = models.IntegerField(db_column='PRG_PRIORITA')  # Field name made lowercase.
    denominazione = models.CharField(db_column='DENOMINAZIONE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_fine_val = models.DateTimeField(db_column='DT_FINE_VAL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNITA_ORGANIZZATIVA_CONTATTI'
        unique_together = (('id_ab', 'cd_tipo_cont', 'prg_priorita'),)


class UnitaOrganizzativaFunzioni(models.Model):
    matricola = models.CharField(db_column='MATRICOLA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_fis = models.ForeignKey(Personale, models.DO_NOTHING, db_column='COD_FIS', blank=True, null=True)  # Field name made lowercase.
    comparto = models.CharField(db_column='COMPARTO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ruolo = models.CharField(db_column='RUOLO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    unita_organizzativa_id = models.CharField(db_column='UNITA_ORGANIZZATIVA_ID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    funzione = models.CharField(db_column='FUNZIONE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    decorrenza = models.DateTimeField(db_column='DECORRENZA', blank=True, null=True)  # Field name made lowercase.
    termine = models.DateTimeField(db_column='TERMINE', blank=True, null=True)  # Field name made lowercase.
    ds_funzione = models.CharField(db_column='DS_FUNZIONE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fl_posorg = models.FloatField(db_column='FL_POSORG', blank=True, null=True)  # Field name made lowercase.
    fl_responsabile = models.FloatField(db_column='FL_RESPONSABILE', blank=True, null=True)  # Field name made lowercase.
    cd_funzbase = models.CharField(db_column='CD_FUNZBASE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNITA_ORGANIZZATIVA_FUNZIONI'


class UnitaOrganizzativaTipoFunzioni(models.Model):
    cd_tipo_nod = models.CharField(db_column='CD_TIPO_NOD', primary_key=True, max_length=100)  # Field name made lowercase.
    funzione = models.CharField(db_column='FUNZIONE', max_length=100)  # Field name made lowercase.
    descr_funzione = models.CharField(db_column='DESCR_FUNZIONE', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNITA_ORGANIZZATIVA_TIPO_FUNZIONI'
        unique_together = (('cd_tipo_nod', 'funzione'),)


class AccountsUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    is_staff = models.IntegerField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=96, blank=True, null=True)
    last_name = models.CharField(max_length=96, blank=True, null=True)
    is_active = models.IntegerField()
    email = models.CharField(max_length=254, blank=True, null=True)
    taxpayer_id = models.CharField(max_length=32, blank=True, null=True)
    origin = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AccountsUserGroups(models.Model):
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_groups'
        unique_together = (('user', 'group'),)


class AccountsUserUserPermissions(models.Model):
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
