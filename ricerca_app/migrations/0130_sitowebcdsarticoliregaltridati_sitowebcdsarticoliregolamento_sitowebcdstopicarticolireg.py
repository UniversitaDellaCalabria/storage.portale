# Generated by Django 3.2.13 on 2023-05-23 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ricerca_app', '0129_alter_sitowebcdstopic_id_user_mod'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitoWebCdsArticoliRegolamento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('aa_regdid_id', models.IntegerField(db_column='AA_REGDID_ID')),
                ('numero', models.PositiveIntegerField(blank=True, db_column='NUMERO', null=True)),
                ('titolo_it', models.CharField(db_column='TITOLO_IT', max_length=2000)),
                ('contenuto_it', models.TextField(db_column='CONTENUTO_IT')),
                ('titolo_en', models.CharField(blank=True, db_column='TITOLO_EN', max_length=2000, null=True)),
                ('contenuto_en', models.TextField(blank=True, db_column='CONTENUTO_EN', null=True)),
                ('stato', models.CharField(blank=True, db_column='STATO', max_length=100, null=True)),
                ('dt_mod', models.DateField(db_column='DT_MOD')),
                ('cds', models.ForeignKey(db_column='CDS_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticacds')),
                ('id_user_mod', models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_ARTICOLI_REGOLAMENTO',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsArticoliRegAltriDati',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ordine', models.PositiveIntegerField(db_column='ORDINE')),
                ('titolo_en', models.CharField(blank=True, db_column='TITOLO_EN', max_length=1000, null=True)),
                ('titolo_it', models.CharField(blank=True, db_column='TITOLO_IT', max_length=1000, null=True)),
                ('testo_it', models.TextField(db_column='TESTO_IT')),
                ('testo_en', models.TextField(blank=True, db_column='TESTO_EN', null=True)),
                ('stato', models.CharField(db_column='STATO', max_length=100)),
                ('dt_mod', models.DateField(db_column='DT_MOD')),
                ('id_sito_web_cds_articoli_regolamento', models.ForeignKey(db_column='ID_SITO_WEB_CDS_ARTICOLI_REGOLAMENTO', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdsarticoliregolamento')),
                ('id_user_mod', models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_ARTICOLI_REG_ALTRI_DATI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SitoWebCdsTopicArticoliReg',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ordine', models.IntegerField(db_column='ORDINE')),
                ('cds_id', models.IntegerField(blank=True, db_column='CDS_ID', null=True)),
                ('topic_cod', models.CharField(blank=True, db_column='TOPIC_COD', max_length=100, null=True)),
                ('dt_mod', models.DateField(db_column='DT_MOD')),
                ('id_user_mod', models.IntegerField(db_column='ID_USER_MOD')),
                ('id_sito_web_cds_articoli_regolamento', models.ForeignKey(db_column='ID_SITO_WEB_CDS_ARTICOLI_REGOLAMENTO', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdsarticoliregolamento')),
                ('id_sito_web_cds_topic', models.ForeignKey(db_column='ID_SITO_WEB_CDS_TOPIC', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.sitowebcdstopic')),
            ],
            options={
                'db_table': 'SITO_WEB_CDS_TOPIC_ARTICOLI_REG',
                'managed': True,
                'unique_together': {('id_sito_web_cds_topic', 'id_sito_web_cds_articoli_regolamento')},
            },
        ),
    ]