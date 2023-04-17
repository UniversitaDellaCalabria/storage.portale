# Generated by Django 3.2.13 on 2023-03-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0100_alter_didatticadottoratoattivitaformativa_visualizza_orario'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitoWebCdsDatiBase',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('cds_cod', models.CharField(blank=True, db_column='CDS_COD', max_length=100, null=True)),
                ('nome_corso_it', models.CharField(db_column='NOME_CORSO_IT', max_length=500)),
                ('nome_corso_en', models.CharField(blank=True, db_column='NOME_CORSO_EN', max_length=500, null=True)),
                ('classe_laurea_it', models.CharField(blank=True, db_column='CLASSE_LAUREA_IT', max_length=100, null=True)),
                ('classe_laurea_en', models.CharField(blank=True, db_column='CLASSE_LAUREA_EN', max_length=100, null=True)),
                ('classe_laurea_interclasse_it', models.CharField(blank=True, db_column='CLASSE_LAUREA_INTERCLASSE_IT', max_length=100, null=True)),
                ('classe_laurea_interclasse_en', models.CharField(blank=True, db_column='CLASSE_LAUREA_INTERCLASSE_EN', max_length=100, null=True)),
                ('lingua_it', models.CharField(blank=True, db_column='LINGUA_IT', max_length=200, null=True)),
                ('lingua_en', models.CharField(blank=True, db_column='LINGUA_EN', max_length=200, null=True)),
                ('durata_it', models.CharField(blank=True, db_column='DURATA_IT', max_length=100, null=True)),
                ('durata_en', models.CharField(blank=True, db_column='DURATA_EN', max_length=100, null=True)),
                ('num_posti', models.IntegerField(blank=True, db_column='NUM_POSTI', null=True)),
                ('link_video_cds_it', models.CharField(blank=True, db_column='LINK_VIDEO_CDS_IT', max_length=500, null=True)),
                ('link_video_cds_en', models.CharField(blank=True, db_column='LINK_VIDEO_CDS_EN', max_length=500, null=True)),
                ('descrizione_corso_it', models.TextField(blank=True, db_column='DESCRIZIONE_CORSO_IT', null=True)),
                ('descrizione_corso_en', models.TextField(blank=True, db_column='DESCRIZIONE_CORSO_EN', null=True)),
                ('accesso_corso_it', models.TextField(blank=True, db_column='ACCESSO_CORSO_IT', null=True)),
                ('accesso_corso_en', models.TextField(blank=True, db_column='ACCESSO_CORSO_EN', null=True)),
                ('obiettivi_corso_it', models.TextField(blank=True, db_column='OBIETTIVI_CORSO_IT', null=True)),
                ('obiettivi_corso_en', models.TextField(blank=True, db_column='OBIETTIVI_CORSO_EN', null=True)),
                ('sbocchi_professionali_it', models.TextField(blank=True, db_column='SBOCCHI_PROFESSIONALI_IT', null=True)),
                ('sbocchi_professionali_en', models.TextField(blank=True, db_column='SBOCCHI_PROFESSIONALI_EN', null=True)),
                ('tasse_contributi_esoneri_it', models.TextField(blank=True, db_column='TASSE_CONTRIBUTI_ESONERI_IT', null=True)),
                ('tasse_contributi_esoneri_en', models.TextField(blank=True, db_column='TASSE_CONTRIBUTI_ESONERI_EN', null=True)),
                ('borse_studio_it', models.TextField(blank=True, db_column='BORSE_STUDIO_IT', null=True)),
                ('borse_studio_en', models.TextField(blank=True, db_column='BORSE_STUDIO_EN', null=True)),
                ('agevolazioni_it', models.TextField(blank=True, db_column='AGEVOLAZIONI_IT', null=True)),
                ('agevolazioni_en', models.TextField(blank=True, db_column='AGEVOLAZIONI_EN', null=True)),
                ('corso_in_pillole_it', models.TextField(blank=True, db_column='CORSO_IN_PILLOLE_IT', null=True)),
                ('corso_in_pillole_en', models.TextField(blank=True, db_column='CORSO_IN_PILLOLE_EN', null=True)),
                ('cosa_si_studia_it', models.TextField(blank=True, db_column='COSA_SI_STUDIA_IT', null=True)),
                ('cosa_si_studia_en', models.TextField(blank=True, db_column='COSA_SI_STUDIA_EN', null=True)),
                ('come_iscriversi_it', models.TextField(blank=True, db_column='COME_ISCRIVERSI_IT', null=True)),
                ('come_iscriversi_en', models.TextField(blank=True, db_column='COME_ISCRIVERSI_EN', null=True)),
                ('sito_web_it', models.CharField(blank=True, db_column='SITO_WEB_IT', max_length=2000, null=True)),
                ('sito_web_en', models.CharField(blank=True, db_column='SITO_WEB_EN', max_length=2000, null=True)),
                ('sito_web_cds_status', models.IntegerField(blank=True, db_column='SITO_WEB_CDS_STATUS', null=True)),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
                ('id_user_mod', models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_DATI_BASE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsDatiExcelTmp',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome_corso_it', models.CharField(db_column='NOME_CORSO_IT', max_length=500)),
                ('classe_laurea_it', models.CharField(blank=True, db_column='CLASSE_LAUREA_IT', max_length=100, null=True)),
                ('classe_laurea_interclasse', models.CharField(blank=True, db_column='CLASSE_LAUREA_INTERCLASSE', max_length=100, null=True)),
                ('lingua', models.CharField(blank=True, db_column='LINGUA', max_length=200, null=True)),
                ('durata', models.CharField(blank=True, db_column='DURATA', max_length=100, null=True)),
                ('num_posti', models.IntegerField(blank=True, db_column='NUM_POSTI', null=True)),
                ('link_video_cds', models.CharField(blank=True, db_column='LINK_VIDEO_CDS', max_length=500, null=True)),
                ('slider_autopromo1', models.TextField(blank=True, db_column='SLIDER_AUTOPROMO1', null=True)),
                ('slider_autopromo2', models.TextField(blank=True, db_column='SLIDER_AUTOPROMO2', null=True)),
                ('slider_autopromo3', models.TextField(blank=True, db_column='SLIDER_AUTOPROMO3', null=True)),
                ('descrizione_corso', models.TextField(blank=True, db_column='DESCRIZIONE_CORSO', null=True)),
                ('accesso_corso', models.TextField(blank=True, db_column='ACCESSO_CORSO', null=True)),
                ('obiettivi_corso', models.TextField(blank=True, db_column='OBIETTIVI_CORSO', null=True)),
                ('sbocchi_professionali', models.TextField(blank=True, db_column='SBOCCHI_PROFESSIONALI', null=True)),
                ('tasse_contributi_esoneri', models.TextField(blank=True, db_column='TASSE_CONTRIBUTI_ESONERI', null=True)),
                ('borse_studio', models.TextField(blank=True, db_column='BORSE_STUDIO', null=True)),
                ('agevolazioni', models.TextField(blank=True, db_column='AGEVOLAZIONI', null=True)),
                ('corso_in_pillole', models.TextField(blank=True, db_column='CORSO_IN_PILLOLE', null=True)),
                ('cosa_si_studia', models.TextField(blank=True, db_column='COSA_SI_STUDIA', null=True)),
                ('come_iscriversi', models.TextField(blank=True, db_column='COME_ISCRIVERSI', null=True)),
                ('descrizione_file1', models.TextField(blank=True, db_column='DESCRIZIONE_FILE1', null=True)),
                ('link_file1', models.TextField(blank=True, db_column='LINK_FILE1', null=True)),
                ('descrizione_file2', models.TextField(blank=True, db_column='DESCRIZIONE_FILE2', null=True)),
                ('link_file2', models.TextField(blank=True, db_column='LINK_FILE2', null=True)),
                ('descrizione_file3', models.TextField(blank=True, db_column='DESCRIZIONE_FILE3', null=True)),
                ('link_file3', models.TextField(blank=True, db_column='LINK_FILE3', null=True)),
                ('descrizione_file4', models.TextField(blank=True, db_column='DESCRIZIONE_FILE4', null=True)),
                ('link_file4', models.TextField(blank=True, db_column='LINK_FILE4', null=True)),
                ('descrizione_file5', models.TextField(blank=True, db_column='DESCRIZIONE_FILE5', null=True)),
                ('link_file5', models.TextField(blank=True, db_column='LINK_FILE5', null=True)),
                ('descrizione_file6', models.TextField(blank=True, db_column='DESCRIZIONE_FILE6', null=True)),
                ('link_file6', models.TextField(blank=True, db_column='LINK_FILE6', null=True)),
                ('ex_studente_profilo_1', models.TextField(blank=True, db_column='EX_STUDENTE_PROFILO_1', null=True)),
                ('ex_studente_link_1', models.TextField(blank=True, db_column='EX_STUDENTE_LINK_1', null=True)),
                ('ex_studente_profilo_2', models.TextField(blank=True, db_column='EX_STUDENTE_PROFILO_2', null=True)),
                ('ex_studente_link_2', models.TextField(blank=True, db_column='EX_STUDENTE_LINK_2', null=True)),
                ('ex_studente_profilo_3', models.TextField(blank=True, db_column='EX_STUDENTE_PROFILO_3', null=True)),
                ('ex_studente_link_3', models.TextField(blank=True, db_column='EX_STUDENTE_LINK_3', null=True)),
                ('ex_studente_profilo_4', models.TextField(blank=True, db_column='EX_STUDENTE_PROFILO_4', null=True)),
                ('ex_studente_link_4', models.TextField(blank=True, db_column='EX_STUDENTE_LINK_4', null=True)),
                ('sito_web', models.CharField(blank=True, db_column='SITO_WEB', max_length=2000, null=True)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_DATI_EXCEL_TMP',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsExStudenti',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ordine', models.PositiveIntegerField(blank=True, db_column='ORDINE', null=True)),
                ('profilo_it', models.TextField(db_column='PROFILO_IT')),
                ('profilo_en', models.TextField(blank=True, db_column='PROFILO_EN', null=True)),
                ('link_it', models.CharField(blank=True, db_column='LINK_IT', max_length=2000, null=True)),
                ('link_en', models.CharField(blank=True, db_column='LINK_EN', max_length=2000, null=True)),
                ('id_sito_web_cds_dati_base', models.IntegerField(db_column='ID_SITO_WEB_CDS_DATI_BASE')),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
                ('id_user_mod', models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_EX_STUDENTI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsLink',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ordine', models.PositiveIntegerField(blank=True, db_column='ORDINE', null=True)),
                ('descrizione_link_it', models.CharField(db_column='DESCRIZIONE_LINK_IT', max_length=2000)),
                ('descrizione_link_en', models.CharField(blank=True, db_column='DESCRIZIONE_LINK_EN', max_length=2000, null=True)),
                ('link_it', models.CharField(blank=True, db_column='LINK_IT', max_length=2000, null=True)),
                ('link_en', models.CharField(blank=True, db_column='LINK_EN', max_length=2000, null=True)),
                ('id_sito_web_cds_dati_base', models.IntegerField(db_column='ID_SITO_WEB_CDS_DATI_BASE')),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
                ('id_user_mod', models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_LINK',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsSlider',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ordine', models.PositiveIntegerField(blank=True, db_column='ORDINE', null=True)),
                ('slider_it', models.TextField(db_column='SLIDER_IT')),
                ('slider_en', models.TextField(blank=True, db_column='SLIDER_EN', null=True)),
                ('id_sito_web_cds_dati_base', models.IntegerField(db_column='ID_SITO_WEB_CDS_DATI_BASE')),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
                ('id_user_mod', models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_SLIDER',
                'managed': True,
            },
        ),
    ]
