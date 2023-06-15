# Generated by Django 3.2.13 on 2023-05-22 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ricerca_app', '0127_auto_20230516_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitoWebCdsOggettiPortaleAltriDati',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('aa_regdid_id', models.IntegerField(db_column='AA_REGDID_ID')),
                ('id_oggetto_portale', models.IntegerField(db_column='ID_OGGETTO_PORTALE')),
                ('id_classe_oggetto_portale', models.CharField(db_column='ID_CLASSE_OGGETTO_PORTALE', max_length=1000)),
                ('titolo_it', models.CharField(blank=True, db_column='TITOLO_IT', max_length=1000, null=True)),
                ('titolo_en', models.CharField(blank=True, db_column='TITOLO_EN', max_length=1000, null=True)),
                ('testo_it', models.TextField(db_column='TESTO_IT')),
                ('testo_en', models.TextField(blank=True, db_column='TESTO_EN', null=True)),
                ('ordine', models.IntegerField(db_column='ORDINE')),
                ('stato', models.CharField(db_column='STATO', max_length=100)),
                ('dt_mod', models.DateField(db_column='DT_MOD')),
                ('cds', models.ForeignKey(db_column='CDS_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticacds')),
                ('id_user_mod', models.ForeignKey(db_column='ID_USER_MOD', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_OGGETTI_PORTALE_ALTRI_DATI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsTopic',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('topic_cod', models.CharField(db_column='TOPIC_COD', max_length=100)),
                ('descr_topic_it', models.CharField(db_column='DESCR_TOPIC_IT', max_length=2000)),
                ('descr_topic_en', models.CharField(blank=True, db_column='DESCR_TOPIC_EN', max_length=2000, null=True)),
                ('num_articolo', models.TextField(blank=True, db_column='NUM_ARTICOLO', null=True)),
                ('dt_mod', models.DateField(db_column='DT_MOD', null=True)),
                ('id_user_mod', models.ForeignKey(db_column='ID_USER_MOD', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_TOPIC',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='SitoWebCdsArticoliRegolamento',
        ),
    ]
