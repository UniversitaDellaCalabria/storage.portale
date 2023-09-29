# Generated by Django 3.2.7 on 2021-11-24 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0028_auto_20211122_0450'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpinoffAreaInnovazioneS3Calabria',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_area_s3', models.CharField(db_column='DESCR_AREA_S3', max_length=1000)),
            ],
            options={
                'db_table': 'SPINOFF_AREA_INNOVAZIONE_S3_CALABRIA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SpinoffDatiBase',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('piva', models.CharField(blank=True, db_column='PIVA', max_length=30, null=True)),
                ('nome_azienda', models.CharField(blank=True, db_column='NOME_AZIENDA', max_length=1000, null=True)),
                ('url_immagine', models.CharField(blank=True, db_column='URL_IMMAGINE', max_length=4000, null=True)),
                ('descrizione_ita', models.TextField(blank=True, db_column='DESCRIZIONE_ITA', null=True)),
                ('descrizione_eng', models.TextField(blank=True, db_column='DESCRIZIONE_ENG', null=True)),
                ('url_sito_web', models.CharField(blank=True, db_column='URL_SITO_WEB', max_length=4000, null=True)),
                ('referente_unical', models.CharField(blank=True, db_column='REFERENTE_UNICAL', max_length=1000, null=True)),
                ('ceo', models.CharField(blank=True, db_column='CEO', max_length=1000, null=True)),
                ('is_startup', models.PositiveIntegerField(blank=True, db_column='IS_STARTUP', null=True)),
                ('is_spinoff', models.PositiveIntegerField(blank=True, db_column='IS_SPINOFF', null=True)),
                ('id_area_innovazione_s3_calabria', models.ForeignKey(blank=True, db_column='ID_AREA_INNOVAZIONE_S3_CALABRIA', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.spinoffareainnovaziones3calabria')),
                ('id_area_tecnologica', models.ForeignKey(blank=True, db_column='ID_AREA_TECNOLOGICA', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.tipologiaareatecnologica')),
                ('matricola_referente_unical', models.ForeignKey(blank=True, db_column='MATRICOLA_REFERENTE_UNICAL', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.personale')),
            ],
            options={
                'db_table': 'SPINOFF_DATI_BASE',
                'managed': True,
            },
        ),
    ]
