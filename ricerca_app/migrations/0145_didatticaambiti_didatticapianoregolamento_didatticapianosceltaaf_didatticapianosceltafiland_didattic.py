# Generated by Django 3.2.19 on 2023-06-28 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0144_auto_20230626_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='DidatticaAmbiti',
            fields=[
                ('amb_id', models.IntegerField(db_column='AMB_ID', primary_key=True, serialize=False)),
                ('des', models.CharField(blank=True, db_column='DES', max_length=255, null=True)),
                ('amb_sede_flg', models.IntegerField(blank=True, db_column='AMB_SEDE_FLG', null=True)),
                ('sys_flg', models.IntegerField(blank=True, db_column='SYS_FLG', null=True)),
                ('amb_aggr_flg', models.IntegerField(blank=True, db_column='AMB_AGGR_FLG', null=True)),
                ('prg_ord_amb', models.IntegerField(blank=True, db_column='PRG_ORD_AMB', null=True)),
                ('dt_ins', models.DateField(blank=True, db_column='DT_INS', null=True)),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
            ],
            options={
                'db_table': 'DIDATTICA_AMBITI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoRegolamento',
            fields=[
                ('regpiani_id', models.IntegerField(db_column='REGPIANI_ID', primary_key=True, serialize=False)),
                ('attinenza_cod', models.CharField(blank=True, db_column='ATTINENZA_COD', max_length=10, null=True)),
                ('cod', models.CharField(blank=True, db_column='COD', max_length=10, null=True)),
                ('aa_coorte_id', models.IntegerField(blank=True, db_column='AA_COORTE_ID', null=True)),
                ('aa_regpiani_id', models.IntegerField(blank=True, db_column='AA_REGPIANI_ID', null=True)),
                ('des', models.CharField(blank=True, db_column='DES', max_length=255, null=True)),
                ('def_flg', models.IntegerField(blank=True, db_column='DEF_FLG', null=True)),
                ('stato_cod', models.CharField(blank=True, db_column='STATO_COD', max_length=5, null=True)),
                ('stato_des', models.CharField(blank=True, db_column='STATO_DES', max_length=40, null=True)),
                ('regpiani_pdr_id', models.IntegerField(blank=True, db_column='REGPIANI_PDR_ID', null=True)),
                ('regpiani_pdr_cod', models.CharField(blank=True, db_column='REGPIANI_PDR_COD', max_length=10, null=True)),
                ('regpiani_pdr_des', models.CharField(blank=True, db_column='REGPIANI_PDR_DES', max_length=255, null=True)),
                ('regpiani_pdr_aa_coorte_id', models.IntegerField(blank=True, db_column='REGPIANI_PDR_AA_COORTE_ID', null=True)),
                ('regpiani_pdr_aa_regpiani_id', models.IntegerField(blank=True, db_column='REGPIANI_PDR_AA_REGPIANI_ID', null=True)),
                ('flg_exp_seg_stu', models.IntegerField(blank=True, db_column='FLG_EXP_SEG_STU', null=True)),
                ('data_exp_seg_stu', models.DateField(blank=True, db_column='DATA_EXP_SEG_STU', null=True)),
                ('nota', models.CharField(blank=True, db_column='NOTA', max_length=1000, null=True)),
                ('regdid', models.ForeignKey(blank=True, db_column='REGDID_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticaregolamento')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_REGOLAMENTO',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoSche',
            fields=[
                ('sche_piano_id', models.IntegerField(db_column='SCHE_PIANO_ID', primary_key=True, serialize=False)),
                ('sche_piano_cod', models.CharField(blank=True, db_column='SCHE_PIANO_COD', max_length=10, null=True)),
                ('sche_piano_des', models.CharField(blank=True, db_column='SCHE_PIANO_DES', max_length=255, null=True)),
                ('sche_piano_vis_web_flg', models.IntegerField(blank=True, db_column='SCHE_PIANO_VIS_WEB_FLG', null=True)),
                ('pds_cod', models.CharField(blank=True, db_column='PDS_COD', max_length=10, null=True)),
                ('pds_des', models.CharField(blank=True, db_column='PDS_DES', max_length=255, null=True)),
                ('comune_flg', models.IntegerField(blank=True, db_column='COMUNE_FLG', null=True)),
                ('ori_id', models.IntegerField(blank=True, db_column='ORI_ID', null=True)),
                ('ori_cod', models.CharField(blank=True, db_column='ORI_COD', max_length=10, null=True)),
                ('ori_des', models.CharField(blank=True, db_column='ORI_DES', max_length=255, null=True)),
                ('cla_m_id', models.IntegerField(blank=True, db_column='CLA_M_ID', null=True)),
                ('cla_miur_cod', models.CharField(blank=True, db_column='CLA_MIUR_COD', max_length=10, null=True)),
                ('cla_miur_des', models.CharField(blank=True, db_column='CLA_MIUR_DES', max_length=255, null=True)),
                ('apt_id', models.IntegerField(blank=True, db_column='APT_ID', null=True)),
                ('apt_cod', models.CharField(blank=True, db_column='APT_COD', max_length=10, null=True)),
                ('apt_des', models.CharField(blank=True, db_column='APT_DES', max_length=80, null=True)),
                ('data_ini_val', models.DateField(blank=True, db_column='DATA_INI_VAL', null=True)),
                ('data_fine_val', models.DateField(blank=True, db_column='DATA_FINE_VAL', null=True)),
                ('stato_piano_gen_cod', models.CharField(blank=True, db_column='STATO_PIANO_GEN_COD', max_length=10, null=True)),
                ('stato_piano_gen_des', models.CharField(blank=True, db_column='STATO_PIANO_GEN_DES', max_length=40, null=True)),
                ('contr_ac_piano_stu_cod', models.CharField(blank=True, db_column='CONTR_AC_PIANO_STU_COD', max_length=10, null=True)),
                ('blocco_af_freq_piano_stu_flg', models.IntegerField(blank=True, db_column='BLOCCO_AF_FREQ_PIANO_STU_FLG', null=True)),
                ('nota_sche_piano', models.CharField(blank=True, db_column='NOTA_SCHE_PIANO', max_length=1000, null=True)),
                ('sche_piano_des_txt_id', models.IntegerField(blank=True, db_column='SCHE_PIANO_DES_TXT_ID', null=True)),
                ('pds_regdid', models.ForeignKey(blank=True, db_column='PDS_REGDID_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapdsregolamento')),
                ('regpiani', models.ForeignKey(db_column='REGPIANI_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianoregolamento')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_SCHE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoSceltaVincoli',
            fields=[
                ('sce_id', models.IntegerField(db_column='SCE_ID', primary_key=True, serialize=False)),
                ('ord_num', models.IntegerField(blank=True, db_column='ORD_NUM', null=True)),
                ('sce_des', models.CharField(blank=True, db_column='SCE_DES', max_length=255, null=True)),
                ('pds_cod', models.CharField(blank=True, db_column='PDS_COD', max_length=10, null=True)),
                ('pds_des', models.CharField(blank=True, db_column='PDS_DES', max_length=255, null=True)),
                ('comune_flg', models.IntegerField(blank=True, db_column='COMUNE_FLG', null=True)),
                ('anno_corso', models.IntegerField(blank=True, db_column='ANNO_CORSO', null=True)),
                ('anno_corso_ant', models.IntegerField(blank=True, db_column='ANNO_CORSO_ANT', null=True)),
                ('tipo_regsce_cod', models.CharField(blank=True, db_column='TIPO_REGSCE_COD', max_length=10, null=True)),
                ('tipo_sce_cod', models.CharField(blank=True, db_column='TIPO_SCE_COD', max_length=5, null=True)),
                ('tipo_um_regsce_cod', models.CharField(blank=True, db_column='TIPO_UM_REGSCE_COD', max_length=5, null=True)),
                ('opz_flg', models.IntegerField(blank=True, db_column='OPZ_FLG', null=True)),
                ('min_unt', models.DecimalField(blank=True, db_column='MIN_UNT', decimal_places=2, max_digits=5, null=True)),
                ('max_unt', models.DecimalField(blank=True, db_column='MAX_UNT', decimal_places=2, max_digits=5, null=True)),
                ('livello', models.IntegerField(blank=True, db_column='LIVELLO', null=True)),
                ('vin_ord_num', models.IntegerField(blank=True, db_column='VIN_ORD_NUM', null=True)),
                ('vin_sce_des', models.CharField(blank=True, db_column='VIN_SCE_DES', max_length=255, null=True)),
                ('tipi_af_tipi_sce_id', models.IntegerField(blank=True, db_column='TIPI_AF_TIPI_SCE_ID', null=True)),
                ('tipo_af_cod', models.CharField(blank=True, db_column='TIPO_AF_COD', max_length=10, null=True)),
                ('tipo_af_des', models.CharField(blank=True, db_column='TIPO_AF_DES', max_length=80, null=True)),
                ('amb_id', models.IntegerField(blank=True, db_column='AMB_ID', null=True)),
                ('ambito_des', models.CharField(blank=True, db_column='AMBITO_DES', max_length=255, null=True)),
                ('sovran_flg', models.IntegerField(blank=True, db_column='SOVRAN_FLG', null=True)),
                ('sostegno_flg', models.IntegerField(blank=True, db_column='SOSTEGNO_FLG', null=True)),
                ('peso_sce', models.IntegerField(blank=True, db_column='PESO_SCE', null=True)),
                ('tesoretto_flg', models.IntegerField(blank=True, db_column='TESORETTO_FLG', null=True)),
                ('assegnazione_posti_flg', models.IntegerField(blank=True, db_column='ASSEGNAZIONE_POSTI_FLG', null=True)),
                ('delibera_flg', models.IntegerField(blank=True, db_column='DELIBERA_FLG', null=True)),
                ('azzera_cfu_flg', models.IntegerField(blank=True, db_column='AZZERA_CFU_FLG', null=True)),
                ('parametri_logistica_flg', models.IntegerField(blank=True, db_column='PARAMETRI_LOGISTICA_FLG', null=True)),
                ('tag_regsce_cod', models.CharField(blank=True, db_column='TAG_REGSCE_COD', max_length=20, null=True)),
                ('nota_pre', models.TextField(blank=True, db_column='NOTA_PRE', null=True)),
                ('nota_pre_vis_web_flg', models.IntegerField(blank=True, db_column='NOTA_PRE_VIS_WEB_FLG', null=True)),
                ('nota_post', models.TextField(blank=True, db_column='NOTA_POST', null=True)),
                ('nota_post_vis_web_flg', models.IntegerField(blank=True, db_column='NOTA_POST_VIS_WEB_FLG', null=True)),
                ('pds_regdid', models.ForeignKey(blank=True, db_column='PDS_REGDID_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapdsregolamento')),
                ('regpiani', models.ForeignKey(blank=True, db_column='REGPIANI_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianoregolamento')),
                ('vin', models.ForeignKey(blank=True, db_column='VIN_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianosceltavincoli')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_SCELTA_VINCOLI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoSceltaFilAnd',
            fields=[
                ('sce_fil_and_id', models.IntegerField(db_column='SCE_FIL_AND_ID', primary_key=True, serialize=False)),
                ('sce_fil_or_id', models.IntegerField(blank=True, db_column='SCE_FIL_OR_ID', null=True)),
                ('sce_fil_or_des', models.CharField(blank=True, db_column='SCE_FIL_OR_DES', max_length=255, null=True)),
                ('tipo_filtro_cod', models.CharField(blank=True, db_column='TIPO_FILTRO_COD', max_length=10, null=True)),
                ('tipo_filtro_des', models.CharField(blank=True, db_column='TIPO_FILTRO_DES', max_length=255, null=True)),
                ('af_gen_id', models.IntegerField(blank=True, db_column='AF_GEN_ID', null=True)),
                ('af_gen_cod', models.CharField(blank=True, db_column='AF_GEN_COD', max_length=20, null=True)),
                ('af_gen_des', models.CharField(blank=True, db_column='AF_GEN_DES', max_length=255, null=True)),
                ('dip_sce_fil_and_id', models.IntegerField(blank=True, db_column='DIP_SCE_FIL_AND_ID', null=True)),
                ('dip_sce_fil_and_cod', models.CharField(blank=True, db_column='DIP_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('dip_sce_fil_and_des', models.CharField(blank=True, db_column='DIP_SCE_FIL_AND_DES', max_length=255, null=True)),
                ('strac_sce_fil_and_id', models.IntegerField(blank=True, db_column='STRAC_SCE_FIL_AND_ID', null=True)),
                ('strac_sce_fil_and_cod', models.CharField(blank=True, db_column='STRAC_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('strac_sce_fil_and_des', models.CharField(blank=True, db_column='STRAC_SCE_FIL_AND_DES', max_length=255, null=True)),
                ('cds_sce_fil_and_id', models.IntegerField(blank=True, db_column='CDS_SCE_FIL_AND_ID', null=True)),
                ('cds_sce_fil_and_cod', models.CharField(blank=True, db_column='CDS_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('cds_sce_fil_and_nome', models.CharField(blank=True, db_column='CDS_SCE_FIL_AND_NOME', max_length=255, null=True)),
                ('cfu', models.DecimalField(blank=True, db_column='CFU', decimal_places=2, max_digits=5, null=True)),
                ('tipo_af_sce_fil_and_cod', models.CharField(blank=True, db_column='TIPO_AF_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('tipo_af_sce_fil_and_des', models.CharField(blank=True, db_column='TIPO_AF_SCE_FIL_AND_DES', max_length=80, null=True)),
                ('sett_cod', models.CharField(blank=True, db_column='SETT_COD', max_length=12, null=True)),
                ('tipo_corso_sce_fil_and_cod', models.CharField(blank=True, db_column='TIPO_CORSO_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('cla_miur_sce_fil_and_id', models.IntegerField(blank=True, db_column='CLA_MIUR_SCE_FIL_AND_ID', null=True)),
                ('cla_miur_sce_fil_and_cod', models.CharField(blank=True, db_column='CLA_MIUR_SCE_FIL_AND_COD', max_length=10, null=True)),
                ('cla_miur_sce_fil_and_des', models.CharField(blank=True, db_column='CLA_MIUR_SCE_FIL_AND_DES', max_length=255, null=True)),
                ('rif_cod', models.CharField(blank=True, db_column='RIF_COD', max_length=10, null=True)),
                ('sett_post_rif_flg', models.IntegerField(blank=True, db_column='SETT_POST_RIF_FLG', null=True)),
                ('tipo_ins_cod', models.CharField(blank=True, db_column='TIPO_INS_COD', max_length=10, null=True)),
                ('peso_sce_fil_and', models.IntegerField(blank=True, db_column='PESO_SCE_FIL_AND', null=True)),
                ('not_flg', models.IntegerField(blank=True, db_column='NOT_FLG', null=True)),
                ('sce', models.ForeignKey(blank=True, db_column='SCE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianosceltavincoli')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_SCELTA_FIL_AND',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoSceltaAf',
            fields=[
                ('sce_af_id', models.IntegerField(db_column='SCE_AF_ID', primary_key=True, serialize=False)),
                ('pds_cod', models.CharField(blank=True, db_column='PDS_COD', max_length=10, null=True)),
                ('pds_des', models.CharField(blank=True, db_column='PDS_DES', max_length=255, null=True)),
                ('sce_blk_id', models.IntegerField(blank=True, db_column='SCE_BLK_ID', null=True)),
                ('min_unt_blk', models.DecimalField(blank=True, db_column='MIN_UNT_BLK', decimal_places=2, max_digits=5, null=True)),
                ('max_unt_blk', models.DecimalField(blank=True, db_column='MAX_UNT_BLK', decimal_places=2, max_digits=5, null=True)),
                ('lingua_id', models.IntegerField(blank=True, db_column='LINGUA_ID', null=True)),
                ('blk_prg', models.IntegerField(blank=True, db_column='BLK_PRG', null=True)),
                ('lingua_iso6392_cod', models.CharField(blank=True, db_column='LINGUA_ISO6392_COD', max_length=3, null=True)),
                ('lingua_des', models.CharField(blank=True, db_column='LINGUA_DES', max_length=40, null=True)),
                ('lingua_num', models.IntegerField(blank=True, db_column='LINGUA_NUM', null=True)),
                ('regud_des_auto', models.CharField(blank=True, db_column='REGUD_DES_AUTO', max_length=1000, null=True)),
                ('regud_des_ute', models.CharField(blank=True, db_column='REGUD_DES_UTE', max_length=1000, null=True)),
                ('min_unt_af', models.DecimalField(blank=True, db_column='MIN_UNT_AF', decimal_places=2, max_digits=5, null=True)),
                ('max_unt_af', models.DecimalField(blank=True, db_column='MAX_UNT_AF', decimal_places=2, max_digits=5, null=True)),
                ('statutario_flg', models.IntegerField(blank=True, db_column='STATUTARIO_FLG', null=True)),
                ('def_verifica_flg', models.IntegerField(blank=True, db_column='DEF_VERIFICA_FLG', null=True)),
                ('contr_aa_off_flg', models.IntegerField(blank=True, db_column='CONTR_AA_OFF_FLG', null=True)),
                ('regdid_af_id', models.IntegerField(blank=True, db_column='REGDID_AF_ID', null=True)),
                ('pds_regdid_af_id', models.IntegerField(blank=True, db_column='PDS_REGDID_AF_ID', null=True)),
                ('pds_af_cod', models.CharField(blank=True, db_column='PDS_AF_COD', max_length=10, null=True)),
                ('pds_af_des', models.CharField(blank=True, db_column='PDS_AF_DES', max_length=255, null=True)),
                ('comune_af_flg', models.IntegerField(blank=True, db_column='COMUNE_AF_FLG', null=True)),
                ('attinenza_af_cod', models.CharField(blank=True, db_column='ATTINENZA_AF_COD', max_length=10, null=True)),
                ('of_id', models.IntegerField(blank=True, db_column='OF_ID', null=True)),
                ('cds_af_id', models.IntegerField(blank=True, db_column='CDS_AF_ID', null=True)),
                ('cds_af_cod', models.CharField(blank=True, db_column='CDS_AF_COD', max_length=10, null=True)),
                ('nome_af_cds', models.CharField(blank=True, db_column='NOME_AF_CDS', max_length=255, null=True)),
                ('cdsord_af_cod', models.CharField(blank=True, db_column='CDSORD_AF_COD', max_length=10, null=True)),
                ('aa_off_id', models.IntegerField(blank=True, db_column='AA_OFF_ID', null=True)),
                ('stato_of_cod', models.CharField(blank=True, db_column='STATO_OF_COD', max_length=5, null=True)),
                ('tipo_comp_af_id', models.IntegerField(blank=True, db_column='TIPO_COMP_AF_ID', null=True)),
                ('tipo_comp_af_cod', models.CharField(blank=True, db_column='TIPO_COMP_AF_COD', max_length=10, null=True)),
                ('des_tipo_comp_af', models.CharField(blank=True, db_column='DES_TIPO_COMP_AF', max_length=255, null=True)),
                ('af_gen_id', models.IntegerField(blank=True, db_column='AF_GEN_ID', null=True)),
                ('af_gen_cod', models.CharField(blank=True, db_column='AF_GEN_COD', max_length=20, null=True)),
                ('af_gen_des', models.CharField(blank=True, db_column='AF_GEN_DES', max_length=255, null=True)),
                ('anno_corso_af', models.IntegerField(blank=True, db_column='ANNO_CORSO_AF', null=True)),
                ('lista_anni_corso_af', models.CharField(blank=True, db_column='LISTA_ANNI_CORSO_AF', max_length=20, null=True)),
                ('af_regdid_id', models.IntegerField(blank=True, db_column='AF_REGDID_ID', null=True)),
                ('sett_cod', models.CharField(blank=True, db_column='SETT_COD', max_length=12, null=True)),
                ('tipo_af_cod_af', models.CharField(blank=True, db_column='TIPO_AF_COD_AF', max_length=10, null=True)),
                ('tipo_af_des_af', models.CharField(blank=True, db_column='TIPO_AF_DES_AF', max_length=80, null=True)),
                ('ambito_des_af', models.CharField(blank=True, db_column='AMBITO_DES_AF', max_length=255, null=True)),
                ('tipo_af_intercla_cod_af', models.CharField(blank=True, db_column='TIPO_AF_INTERCLA_COD_AF', max_length=10, null=True)),
                ('tipo_af_intercla_des_af', models.CharField(blank=True, db_column='TIPO_AF_INTERCLA_DES_AF', max_length=80, null=True)),
                ('amb_intercla_id_af', models.IntegerField(blank=True, db_column='AMB_INTERCLA_ID_AF', null=True)),
                ('ambito_intercla_des_af', models.CharField(blank=True, db_column='AMBITO_INTERCLA_DES_AF', max_length=255, null=True)),
                ('peso', models.DecimalField(blank=True, db_column='PESO', decimal_places=2, max_digits=5, null=True)),
                ('peso_foglie_non_log', models.DecimalField(blank=True, db_column='PESO_FOGLIE_NON_LOG', decimal_places=2, max_digits=5, null=True)),
                ('num_max_reit', models.IntegerField(blank=True, db_column='NUM_MAX_REIT', null=True)),
                ('non_erogabile_flg', models.IntegerField(blank=True, db_column='NON_EROGABILE_FLG', null=True)),
                ('livello_af_cod', models.CharField(blank=True, db_column='LIVELLO_AF_COD', max_length=10, null=True)),
                ('livello_af_des', models.CharField(blank=True, db_column='LIVELLO_AF_DES', max_length=40, null=True)),
                ('tipo_esa_cod', models.CharField(blank=True, db_column='TIPO_ESA_COD', max_length=5, null=True)),
                ('tipo_esa_des', models.CharField(blank=True, db_column='TIPO_ESA_DES', max_length=40, null=True)),
                ('tipo_val_cod', models.CharField(blank=True, db_column='TIPO_VAL_COD', max_length=5, null=True)),
                ('tipo_val_des', models.CharField(blank=True, db_column='TIPO_VAL_DES', max_length=40, null=True)),
                ('af_pdr_id', models.IntegerField(blank=True, db_column='AF_PDR_ID', null=True)),
                ('af_radice_id', models.IntegerField(blank=True, db_column='AF_RADICE_ID', null=True)),
                ('num_liv_albero', models.IntegerField(blank=True, db_column='NUM_LIV_ALBERO', null=True)),
                ('ciclo_id', models.IntegerField(blank=True, db_column='CICLO_ID', null=True)),
                ('ciclo_des', models.CharField(blank=True, db_column='CICLO_DES', max_length=40, null=True)),
                ('tipo_ciclo_cod', models.CharField(blank=True, db_column='TIPO_CICLO_COD', max_length=5, null=True)),
                ('des_tipo_ciclo', models.CharField(blank=True, db_column='DES_TIPO_CICLO', max_length=40, null=True)),
                ('org_did_sua_cod', models.IntegerField(blank=True, db_column='ORG_DID_SUA_COD', null=True)),
                ('sede_id', models.IntegerField(blank=True, db_column='SEDE_ID', null=True)),
                ('sede_des', models.CharField(blank=True, db_column='SEDE_DES', max_length=255, null=True)),
                ('tipo_rag_cod', models.CharField(blank=True, db_column='TIPO_RAG_COD', max_length=5, null=True)),
                ('tipo_rag_des', models.CharField(blank=True, db_column='TIPO_RAG_DES', max_length=40, null=True)),
                ('af_capogruppo_id', models.IntegerField(blank=True, db_column='AF_CAPOGRUPPO_ID', null=True)),
                ('scelta_mod_flg', models.IntegerField(blank=True, db_column='SCELTA_MOD_FLG', null=True)),
                ('num_regud', models.DecimalField(blank=True, db_column='NUM_REGUD', decimal_places=0, max_digits=38, null=True)),
                ('af', models.ForeignKey(blank=True, db_column='AF_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticaattivitaformativa')),
                ('amb_id_af', models.ForeignKey(blank=True, db_column='AMB_ID_AF', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticaambiti')),
                ('pds_regdid', models.ForeignKey(blank=True, db_column='PDS_REGDID_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapdsregolamento')),
                ('sce', models.ForeignKey(blank=True, db_column='SCE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianosceltavincoli')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_SCELTA_AF',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DidatticaPianoSceltaSchePiano',
            fields=[
                ('sche_piano', models.OneToOneField(db_column='SCHE_PIANO_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ricerca_app.didatticapianosche')),
                ('sche_statutario_flg', models.IntegerField(blank=True, db_column='SCHE_STATUTARIO_FLG', null=True)),
                ('sche_pds_regdid_id', models.IntegerField(blank=True, db_column='SCHE_PDS_REGDID_ID', null=True)),
                ('sche_pds_cod', models.CharField(blank=True, db_column='SCHE_PDS_COD', max_length=10, null=True)),
                ('sche_pds_des', models.CharField(blank=True, db_column='SCHE_PDS_DES', max_length=255, null=True)),
                ('sche_ori_id', models.IntegerField(blank=True, db_column='SCHE_ORI_ID', null=True)),
                ('sche_cla_m_id', models.IntegerField(blank=True, db_column='SCHE_CLA_M_ID', null=True)),
                ('sche_apt_id', models.IntegerField(blank=True, db_column='SCHE_APT_ID', null=True)),
                ('sche_nota', models.CharField(blank=True, db_column='SCHE_NOTA', max_length=1000, null=True)),
                ('data_ini_val', models.DateField(blank=True, db_column='DATA_INI_VAL', null=True)),
                ('data_fine_val', models.DateField(blank=True, db_column='DATA_FINE_VAL', null=True)),
                ('stato_piano_gen_cod', models.CharField(blank=True, db_column='STATO_PIANO_GEN_COD', max_length=10, null=True)),
                ('contr_ac_piano_stu_cod', models.CharField(blank=True, db_column='CONTR_AC_PIANO_STU_COD', max_length=10, null=True)),
                ('blocco_af_freq_piano_stu_flg', models.IntegerField(blank=True, db_column='BLOCCO_AF_FREQ_PIANO_STU_FLG', null=True)),
                ('ord_num', models.IntegerField(blank=True, db_column='ORD_NUM', null=True)),
                ('apt_slot_id', models.IntegerField(blank=True, db_column='APT_SLOT_ID', null=True)),
                ('apt_slot_cod', models.CharField(blank=True, db_column='APT_SLOT_COD', max_length=10, null=True)),
                ('apt_slot_des', models.CharField(blank=True, db_column='APT_SLOT_DES', max_length=255, null=True)),
                ('apt_slot_anno_corso', models.IntegerField(blank=True, db_column='APT_SLOT_ANNO_CORSO', null=True)),
                ('apt_slot_ord_num', models.IntegerField(blank=True, db_column='APT_SLOT_ORD_NUM', null=True)),
                ('sce_des', models.CharField(blank=True, db_column='SCE_DES', max_length=255, null=True)),
                ('pds_regdid_id', models.IntegerField(blank=True, db_column='PDS_REGDID_ID', null=True)),
                ('pds_cod', models.CharField(blank=True, db_column='PDS_COD', max_length=10, null=True)),
                ('pds_des', models.CharField(blank=True, db_column='PDS_DES', max_length=255, null=True)),
                ('comune_flg', models.IntegerField(blank=True, db_column='COMUNE_FLG', null=True)),
                ('anno_corso', models.IntegerField(blank=True, db_column='ANNO_CORSO', null=True)),
                ('anno_corso_ant', models.IntegerField(blank=True, db_column='ANNO_CORSO_ANT', null=True)),
                ('tipo_regsce_cod', models.CharField(blank=True, db_column='TIPO_REGSCE_COD', max_length=10, null=True)),
                ('tipo_sce_cod', models.CharField(blank=True, db_column='TIPO_SCE_COD', max_length=5, null=True)),
                ('tipo_sce_des', models.CharField(blank=True, db_column='TIPO_SCE_DES', max_length=40, null=True)),
                ('tipo_regsce_des', models.CharField(blank=True, db_column='TIPO_REGSCE_DES', max_length=40, null=True)),
                ('tipo_um_regsce_cod', models.CharField(blank=True, db_column='TIPO_UM_REGSCE_COD', max_length=5, null=True)),
                ('opz_flg', models.IntegerField(blank=True, db_column='OPZ_FLG', null=True)),
                ('min_unt', models.DecimalField(blank=True, db_column='MIN_UNT', decimal_places=2, max_digits=5, null=True)),
                ('max_unt', models.DecimalField(blank=True, db_column='MAX_UNT', decimal_places=2, max_digits=5, null=True)),
                ('livello', models.IntegerField(blank=True, db_column='LIVELLO', null=True)),
                ('vin_id', models.IntegerField(blank=True, db_column='VIN_ID', null=True)),
                ('vin_ord_num', models.IntegerField(blank=True, db_column='VIN_ORD_NUM', null=True)),
                ('vin_sce_des', models.CharField(blank=True, db_column='VIN_SCE_DES', max_length=255, null=True)),
                ('tipi_af_tipi_sce_id', models.IntegerField(blank=True, db_column='TIPI_AF_TIPI_SCE_ID', null=True)),
                ('tipo_af_cod', models.CharField(blank=True, db_column='TIPO_AF_COD', max_length=10, null=True)),
                ('tipo_af_des', models.CharField(blank=True, db_column='TIPO_AF_DES', max_length=80, null=True)),
                ('ambito_des', models.CharField(blank=True, db_column='AMBITO_DES', max_length=255, null=True)),
                ('sovran_flg', models.IntegerField(blank=True, db_column='SOVRAN_FLG', null=True)),
                ('sostegno_flg', models.IntegerField(blank=True, db_column='SOSTEGNO_FLG', null=True)),
                ('peso_sce', models.IntegerField(blank=True, db_column='PESO_SCE', null=True)),
                ('tesoretto_flg', models.IntegerField(blank=True, db_column='TESORETTO_FLG', null=True)),
                ('assegnazione_posti_flg', models.IntegerField(blank=True, db_column='ASSEGNAZIONE_POSTI_FLG', null=True)),
                ('delibera_flg', models.IntegerField(blank=True, db_column='DELIBERA_FLG', null=True)),
                ('azzera_cfu_flg', models.IntegerField(blank=True, db_column='AZZERA_CFU_FLG', null=True)),
                ('parametri_logistica_flg', models.IntegerField(blank=True, db_column='PARAMETRI_LOGISTICA_FLG', null=True)),
                ('tag_regsce_cod', models.CharField(blank=True, db_column='TAG_REGSCE_COD', max_length=20, null=True)),
                ('peso_af_sce', models.DecimalField(blank=True, db_column='PESO_AF_SCE', decimal_places=0, max_digits=38, null=True)),
                ('peso_min_singola_af', models.DecimalField(blank=True, db_column='PESO_MIN_SINGOLA_AF', decimal_places=0, max_digits=38, null=True)),
                ('peso_max_singola_af', models.DecimalField(blank=True, db_column='PESO_MAX_SINGOLA_AF', decimal_places=0, max_digits=38, null=True)),
                ('num_af_sce', models.DecimalField(blank=True, db_column='NUM_AF_SCE', decimal_places=0, max_digits=38, null=True)),
                ('peso_af_sce_stat', models.DecimalField(blank=True, db_column='PESO_AF_SCE_STAT', decimal_places=0, max_digits=38, null=True)),
                ('peso_af_sce_def_verifica', models.DecimalField(blank=True, db_column='PESO_AF_SCE_DEF_VERIFICA', decimal_places=0, max_digits=38, null=True)),
                ('num_blk', models.DecimalField(blank=True, db_column='NUM_BLK', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_stat', models.DecimalField(blank=True, db_column='NUM_BLK_STAT', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_def_verifica', models.DecimalField(blank=True, db_column='NUM_BLK_DEF_VERIFICA', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_contr_aa_off', models.DecimalField(blank=True, db_column='NUM_BLK_CONTR_AA_OFF', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_statutario_flg_div', models.DecimalField(blank=True, db_column='NUM_BLK_STATUTARIO_FLG_DIV', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_def_verifica_flg_div', models.DecimalField(blank=True, db_column='NUM_BLK_DEF_VERIFICA_FLG_DIV', decimal_places=0, max_digits=38, null=True)),
                ('num_blk_contr_aa_off_flg_div', models.DecimalField(blank=True, db_column='NUM_BLK_CONTR_AA_OFF_FLG_DIV', decimal_places=0, max_digits=38, null=True)),
                ('peso_blk', models.DecimalField(blank=True, db_column='PESO_BLK', decimal_places=0, max_digits=38, null=True)),
                ('af_stessa_taf_flg', models.DecimalField(blank=True, db_column='AF_STESSA_TAF_FLG', decimal_places=0, max_digits=38, null=True)),
                ('af_stessa_taf_intercla_flg', models.DecimalField(blank=True, db_column='AF_STESSA_TAF_INTERCLA_FLG', decimal_places=0, max_digits=38, null=True)),
                ('af_stesso_ambito_flg', models.DecimalField(blank=True, db_column='AF_STESSO_AMBITO_FLG', decimal_places=0, max_digits=38, null=True)),
                ('af_stesso_ambito_intercla_flg', models.DecimalField(blank=True, db_column='AF_STESSO_AMBITO_INTERCLA_FLG', decimal_places=0, max_digits=38, null=True)),
                ('amb_id_af_regsce', models.DecimalField(blank=True, db_column='AMB_ID_AF_REGSCE', decimal_places=0, max_digits=38, null=True)),
                ('tipo_af_cod_af_regsce', models.CharField(blank=True, db_column='TIPO_AF_COD_AF_REGSCE', max_length=10, null=True)),
                ('amb_intercla_id_af_regsce', models.DecimalField(blank=True, db_column='AMB_INTERCLA_ID_AF_REGSCE', decimal_places=0, max_digits=38, null=True)),
                ('tipo_af_intercla_cod_af_regsce', models.CharField(blank=True, db_column='TIPO_AF_INTERCLA_COD_AF_REGSCE', max_length=10, null=True)),
                ('num_af_taf_d', models.DecimalField(blank=True, db_column='NUM_AF_TAF_D', decimal_places=0, max_digits=38, null=True)),
                ('num_af_taf_intercla_d', models.DecimalField(blank=True, db_column='NUM_AF_TAF_INTERCLA_D', decimal_places=0, max_digits=38, null=True)),
                ('num_af_taf_e_f_s', models.DecimalField(blank=True, db_column='NUM_AF_TAF_E_F_S', decimal_places=0, max_digits=38, null=True)),
                ('num_af_taf_intercla_e_f_s', models.DecimalField(blank=True, db_column='NUM_AF_TAF_INTERCLA_E_F_S', decimal_places=0, max_digits=38, null=True)),
                ('sett_cod_af_regsce', models.CharField(blank=True, db_column='SETT_COD_AF_REGSCE', max_length=12, null=True)),
                ('nota_pre', models.TextField(blank=True, db_column='NOTA_PRE', null=True)),
                ('nota_pre_vis_web_flg', models.IntegerField(blank=True, db_column='NOTA_PRE_VIS_WEB_FLG', null=True)),
                ('nota_post', models.TextField(blank=True, db_column='NOTA_POST', null=True)),
                ('nota_post_vis_web_flg', models.IntegerField(blank=True, db_column='NOTA_POST_VIS_WEB_FLG', null=True)),
                ('amb', models.ForeignKey(blank=True, db_column='AMB_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticaambiti')),
                ('sce', models.ForeignKey(db_column='SCE_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticapianosceltavincoli')),
            ],
            options={
                'db_table': 'DIDATTICA_PIANO_SCELTA_SCHE_PIANO',
                'managed': True,
                'unique_together': {('sche_piano', 'sce')},
            },
        ),
    ]
