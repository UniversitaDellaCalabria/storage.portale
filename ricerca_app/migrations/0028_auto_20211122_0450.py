# Generated by Django 3.2.7 on 2021-11-22 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0027_auto_20211117_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrevettoDatiBase',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('id_univoco', models.CharField(blank=True, db_column='ID_UNIVOCO', max_length=500, null=True)),
                ('titolo', models.CharField(blank=True, db_column='TITOLO', max_length=2000, null=True)),
                ('url_immagine', models.CharField(blank=True, db_column='URL_IMMAGINE', max_length=2000, null=True)),
                ('breve_descrizione', models.TextField(blank=True, db_column='BREVE_DESCRIZIONE', null=True)),
                ('url_knowledge_share', models.CharField(blank=True, db_column='URL_KNOWLEDGE_SHARE', max_length=2000, null=True)),
                ('applicazioni', models.TextField(blank=True, db_column='APPLICAZIONI', null=True)),
                ('vantaggi', models.TextField(blank=True, db_column='VANTAGGI', null=True)),
                ('trl_aggiornato', models.CharField(blank=True, db_column='TRL_AGGIORNATO', max_length=500, null=True)),
                ('proprieta', models.CharField(blank=True, db_column='PROPRIETA', max_length=2000, null=True)),
                ('data_priorita', models.DateField(blank=True, db_column='DATA_PRIORITA', null=True)),
                ('territorio', models.CharField(blank=True, db_column='TERRITORIO', max_length=2000, null=True)),
                ('area_ks', models.CharField(blank=True, db_column='AREA_KS', max_length=2000, null=True)),
            ],
            options={
                'db_table': 'BREVETTO_DATI_BASE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BrevettoDirittiCommerciali',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_diritto', models.CharField(db_column='DESCR_DIRITTO', max_length=1000)),
            ],
            options={
                'db_table': 'BREVETTO_DIRITTI_COMMERCIALI',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BrevettoDisponibilita',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_disponibilita', models.CharField(db_column='DESCR_DISPONIBILITA', max_length=1000)),
            ],
            options={
                'db_table': 'BREVETTO_DISPONIBILITA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BrevettoStatusLegale',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_status', models.CharField(db_column='DESCR_STATUS', max_length=1000)),
            ],
            options={
                'db_table': 'BREVETTO_STATUS_LEGALE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipologiaAreaTecnologica',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_area_ita', models.CharField(db_column='DESCR_AREA_ITA', max_length=1000)),
                ('descr_area_eng', models.CharField(blank=True, db_column='DESCR_AREA_ENG', max_length=1000, null=True)),
            ],
            options={
                'db_table': 'TIPOLOGIA_AREA_TECNOLOGICA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BrevettoInventori',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('cognomenome_origine', models.CharField(blank=True, db_column='COGNOMENOME_ORIGINE', max_length=200, null=True)),
                ('id_brevetto', models.ForeignKey(blank=True, db_column='ID_BREVETTO', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.brevettodatibase')),
                ('matricola_inventore', models.ForeignKey(blank=True, db_column='MATRICOLA_INVENTORE', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale')),
            ],
            options={
                'db_table': 'BREVETTO_INVENTORI',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='brevettodatibase',
            name='id_area_tecnologica',
            field=models.ForeignKey(blank=True, db_column='ID_AREA_TECNOLOGICA', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.tipologiaareatecnologica'),
        ),
        migrations.AddField(
            model_name='brevettodatibase',
            name='id_diritto_commerciale',
            field=models.ForeignKey(blank=True, db_column='ID_DIRITTO_COMMERCIALE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.brevettodiritticommerciali'),
        ),
        migrations.AddField(
            model_name='brevettodatibase',
            name='id_disponibilita',
            field=models.ForeignKey(blank=True, db_column='ID_DISPONIBILITA', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.brevettodisponibilita'),
        ),
        migrations.AddField(
            model_name='brevettodatibase',
            name='id_status_legale',
            field=models.ForeignKey(blank=True, db_column='ID_STATUS_LEGALE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.brevettostatuslegale'),
        ),
    ]
