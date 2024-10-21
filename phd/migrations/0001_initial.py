# Generated by Django 4.2.16 on 2024-10-21 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("structures", "0001_initial"),
        ("cds", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("addressbook", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DidatticaDottoratoAttivitaFormativa",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "nome_af",
                    models.CharField(db_column="NOME_AF", max_length=1000, null=True),
                ),
                ("ssd", models.CharField(db_column="SSD", max_length=1000, null=True)),
                ("numero_ore", models.IntegerField(db_column="NUMERO_ORE", null=True)),
                ("cfu", models.IntegerField(db_column="CFU", null=True)),
                ("tipo_af", models.CharField(db_column="TIPO_AF", max_length=500)),
                (
                    "rif_dottorato",
                    models.CharField(
                        blank=True,
                        db_column="RIF_DOTTORATO",
                        max_length=1000,
                        null=True,
                    ),
                ),
                ("ciclo", models.IntegerField(db_column="CICLO")),
                (
                    "struttura_proponente_origine",
                    models.CharField(
                        blank=True,
                        db_column="STRUTTURA_PROPONENTE_ORIGINE",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("contenuti_af", models.TextField(db_column="CONTENUTI_AF", null=True)),
                (
                    "prerequisiti",
                    models.TextField(blank=True, db_column="PREREQUISITI", null=True),
                ),
                (
                    "num_min_studenti",
                    models.IntegerField(
                        blank=True, db_column="NUM_MIN_STUDENTI", null=True
                    ),
                ),
                (
                    "num_max_studenti",
                    models.IntegerField(
                        blank=True, db_column="NUM_MAX_STUDENTI", null=True
                    ),
                ),
                (
                    "verifica_finale",
                    models.BooleanField(db_column="VERIFICA_FINALE", default=False),
                ),
                (
                    "modalita_verifica",
                    models.CharField(
                        blank=True,
                        db_column="MODALITA_VERIFICA",
                        max_length=1000,
                        null=True,
                    ),
                ),
                (
                    "avvio",
                    models.CharField(
                        blank=True, db_column="AVVIO", max_length=255, null=True
                    ),
                ),
                (
                    "fine",
                    models.CharField(
                        blank=True, db_column="FINE", max_length=255, null=True
                    ),
                ),
                (
                    "orario_aule",
                    models.TextField(blank=True, db_column="ORARIO_AULE", null=True),
                ),
                ("note", models.TextField(blank=True, db_column="NOTE", null=True)),
                (
                    "visualizza_orario",
                    models.BooleanField(db_column="VISUALIZZA_ORARIO", default=False),
                ),
                (
                    "dt_mod",
                    models.DateTimeField(blank=True, db_column="DT_MOD", null=True),
                ),
                (
                    "didattica_ssd",
                    models.ForeignKey(
                        db_column="ID_DIDATTICA_SSD",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cds.didatticassd",
                    ),
                ),
                (
                    "struttura_proponente",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_STRUTTURA_PROPONENTE",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="structures.unitaorganizzativa",
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoAttivitaFormativaTipologia",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("nome_it", models.CharField(db_column="NOME_IT", max_length=255)),
                (
                    "nome_en",
                    models.CharField(
                        blank=True, db_column="NOME_EN", max_length=255, null=True
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_TIPOLOGIA",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoCds",
            fields=[
                ("dt_ins", models.DateTimeField(auto_now_add=True, db_column="DT_INS")),
                (
                    "dt_mod",
                    models.DateTimeField(auto_now=True, db_column="DT_MOD", null=True),
                ),
                (
                    "cds_id_esse3",
                    models.IntegerField(
                        db_column="CDS_ID_ESSE3", primary_key=True, serialize=False
                    ),
                ),
                (
                    "cds_cod",
                    models.CharField(
                        blank=True, db_column="CDS_COD", max_length=10, null=True
                    ),
                ),
                (
                    "nome_cds_it",
                    models.CharField(
                        blank=True, db_column="NOME_CDS_IT", max_length=255, null=True
                    ),
                ),
                (
                    "rif_cod",
                    models.CharField(
                        blank=True, db_column="RIF_COD", max_length=10, null=True
                    ),
                ),
                (
                    "rif_des",
                    models.CharField(
                        blank=True, db_column="RIF_DES", max_length=255, null=True
                    ),
                ),
                (
                    "tipo_corso_cod",
                    models.CharField(
                        blank=True, db_column="TIPO_CORSO_COD", max_length=10, null=True
                    ),
                ),
                (
                    "tipo_corso_des",
                    models.CharField(
                        blank=True, db_column="TIPO_CORSO_DES", max_length=80, null=True
                    ),
                ),
                (
                    "durata_anni",
                    models.IntegerField(blank=True, db_column="DURATA_ANNI", null=True),
                ),
                (
                    "valore_min",
                    models.IntegerField(blank=True, db_column="VALORE_MIN", null=True),
                ),
                (
                    "tipo_titit_cod",
                    models.CharField(
                        blank=True, db_column="TIPO_TITIT_COD", max_length=10, null=True
                    ),
                ),
                (
                    "tipo_titit_des",
                    models.CharField(
                        blank=True,
                        db_column="TIPO_TITIT_DES",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "tipo_spec_cod",
                    models.CharField(
                        blank=True, db_column="TIPO_SPEC_COD", max_length=10, null=True
                    ),
                ),
                (
                    "tipo_spec_des",
                    models.CharField(
                        blank=True, db_column="TIPO_SPEC_DES", max_length=255, null=True
                    ),
                ),
                (
                    "istat_cod",
                    models.CharField(
                        blank=True, db_column="ISTAT_COD", max_length=10, null=True
                    ),
                ),
                (
                    "max_punti",
                    models.IntegerField(blank=True, db_column="MAX_PUNTI", null=True),
                ),
                (
                    "um_peso_cod",
                    models.CharField(
                        blank=True, db_column="UM_PESO_COD", max_length=5, null=True
                    ),
                ),
                (
                    "um_peso_des",
                    models.CharField(
                        blank=True, db_column="UM_PESO_DES", max_length=40, null=True
                    ),
                ),
                (
                    "aa_att_id",
                    models.IntegerField(blank=True, db_column="AA_ATT_ID", null=True),
                ),
                (
                    "aa_dis_id",
                    models.IntegerField(blank=True, db_column="AA_DIS_ID", null=True),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, db_column="URL", max_length=255, null=True
                    ),
                ),
                (
                    "cds_url_info_web",
                    models.URLField(
                        blank=True,
                        db_column="CDS_URL_INFO_WEB",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "cds_vis_web_flg",
                    models.IntegerField(
                        blank=True, db_column="CDS_VIS_WEB_FLG", null=True
                    ),
                ),
                (
                    "cdsord_id_esse3",
                    models.IntegerField(
                        blank=True, db_column="CDSORD_ID_ESSE3", null=True
                    ),
                ),
                (
                    "cdsord_cod",
                    models.CharField(
                        blank=True, db_column="CDSORD_COD", max_length=10, null=True
                    ),
                ),
                ("aa_ord_id", models.IntegerField(db_column="AA_ORD_ID")),
                (
                    "cdsord_des",
                    models.CharField(
                        blank=True, db_column="CDSORD_DES", max_length=255, null=True
                    ),
                ),
                (
                    "stato_cdsord_cod",
                    models.CharField(
                        blank=True,
                        db_column="STATO_CDSORD_COD",
                        max_length=5,
                        null=True,
                    ),
                ),
                (
                    "dip_cod",
                    models.ForeignKey(
                        blank=True,
                        db_column="DIP_COD",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="structures.didatticadipartimento",
                        to_field="dip_cod",
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_CDS",
                "managed": True,
                "unique_together": {("cds_id_esse3", "aa_ord_id")},
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoRegolamento",
            fields=[
                ("dt_ins", models.DateTimeField(auto_now_add=True, db_column="DT_INS")),
                (
                    "dt_mod",
                    models.DateTimeField(auto_now=True, db_column="DT_MOD", null=True),
                ),
                (
                    "regdid_id_esse3",
                    models.IntegerField(
                        db_column="REGDID_ID_ESSE3", primary_key=True, serialize=False
                    ),
                ),
                (
                    "aa_regdid_id",
                    models.IntegerField(
                        blank=True, db_column="AA_REGDID_ID", null=True
                    ),
                ),
                (
                    "regdid_cod",
                    models.CharField(
                        blank=True, db_column="REGDID_COD", max_length=255, null=True
                    ),
                ),
                (
                    "regdid_des",
                    models.CharField(
                        blank=True, db_column="REGDID_DES", max_length=255, null=True
                    ),
                ),
                (
                    "numero_piani_studio",
                    models.IntegerField(
                        blank=True, db_column="NUMERO_PIANI_STUDIO", null=True
                    ),
                ),
                (
                    "frequenza_obbligatoria",
                    models.IntegerField(
                        blank=True, db_column="FREQUENZA_OBBLIGATORIA", null=True
                    ),
                ),
                (
                    "num_ciclo",
                    models.IntegerField(blank=True, db_column="NUM_CICLO", null=True),
                ),
                (
                    "aa_ord",
                    models.ForeignKey(
                        db_column="AA_ORD_ID",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aaord_ddr",
                        to="phd.didatticadottoratocds",
                    ),
                ),
                (
                    "cds_id_esse3",
                    models.ForeignKey(
                        blank=True,
                        db_column="CDS_ID_ESSE3",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="idesse3_ddr",
                        to="phd.didatticadottoratocds",
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_REGOLAMENTO",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoPds",
            fields=[
                ("dt_ins", models.DateTimeField(auto_now_add=True, db_column="DT_INS")),
                (
                    "dt_mod",
                    models.DateTimeField(auto_now=True, db_column="DT_MOD", null=True),
                ),
                (
                    "pds_id_esse3",
                    models.IntegerField(
                        blank=True, db_column="PDS_ID_ESSE3", null=True
                    ),
                ),
                (
                    "pdsord_id_esse3",
                    models.IntegerField(
                        db_column="PDSORD_ID_ESSE3", primary_key=True, serialize=False
                    ),
                ),
                (
                    "pds_cod",
                    models.CharField(
                        blank=True, db_column="PDS_COD", max_length=40, null=True
                    ),
                ),
                (
                    "pds_des",
                    models.CharField(
                        blank=True, db_column="PDS_DES", max_length=255, null=True
                    ),
                ),
                (
                    "indir",
                    models.CharField(
                        blank=True, db_column="INDIR", max_length=255, null=True
                    ),
                ),
                (
                    "orien",
                    models.CharField(
                        blank=True, db_column="ORIEN", max_length=255, null=True
                    ),
                ),
                (
                    "valore_min",
                    models.IntegerField(blank=True, db_column="VALORE_MIN", null=True),
                ),
                (
                    "stato_cod",
                    models.CharField(
                        blank=True, db_column="STATO_COD", max_length=5, null=True
                    ),
                ),
                (
                    "data_var",
                    models.DateTimeField(blank=True, db_column="DATA_VAR", null=True),
                ),
                (
                    "val_min_tesi",
                    models.IntegerField(
                        blank=True, db_column="VAL_MIN_TESI", null=True
                    ),
                ),
                (
                    "aa_ord",
                    models.ForeignKey(
                        blank=True,
                        db_column="AA_ORD_ID",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="aaord_ddpds",
                        to="phd.didatticadottoratocds",
                    ),
                ),
                (
                    "cds_id_esse3",
                    models.ForeignKey(
                        blank=True,
                        db_column="CDS_ID_ESSE3",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="idesse3_ddpds",
                        to="phd.didatticadottoratocds",
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_PDS",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoAttivitaFormativaDocente",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "cognome_nome_origine",
                    models.CharField(db_column="COGNOME_NOME_ORIGINE", max_length=200),
                ),
                (
                    "dt_mod",
                    models.DateTimeField(blank=True, db_column="DT_MOD", null=True),
                ),
                (
                    "didattica_dottorato_attivita_formativa",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="phd.didatticadottoratoattivitaformativa",
                    ),
                ),
                (
                    "matricola",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_PERSONALE_MATRICOLA",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="addressbook.personale",
                        to_field="matricola",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_DOCENTE",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaDottoratoAttivitaFormativaAltriDocenti",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "cognome_nome_origine",
                    models.CharField(db_column="COGNOME_NOME_ORIGINE", max_length=200),
                ),
                (
                    "dt_mod",
                    models.DateTimeField(blank=True, db_column="DT_MOD", null=True),
                ),
                (
                    "didattica_dottorato_attivita_formativa",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="phd.didatticadottoratoattivitaformativa",
                    ),
                ),
                (
                    "matricola",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_PERSONALE_MATRICOLA",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="addressbook.personale",
                        to_field="matricola",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_ALTRI_DOCENTI",
                "managed": True,
            },
        ),
        migrations.AddField(
            model_name="didatticadottoratoattivitaformativa",
            name="tipologia",
            field=models.ForeignKey(
                db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_TIPOLOGIA",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="phd.didatticadottoratoattivitaformativatipologia",
            ),
        ),
        migrations.AddField(
            model_name="didatticadottoratoattivitaformativa",
            name="user_mod",
            field=models.ForeignKey(
                blank=True,
                db_column="user_mod_id",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
