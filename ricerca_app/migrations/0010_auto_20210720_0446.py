# Generated by Django 3.2 on 2021-07-20 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0009_laboratorioattivita_laboratorioattrezzature_laboratoriodatibase_laboratoriodatierc1_laboratorioperso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratorioattivita',
            name='id_laboratorio_dati',
            field=models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.CASCADE, to='ricerca_app.laboratoriodatibase'),
        ),
        migrations.AlterField(
            model_name='laboratorioattrezzature',
            name='costo_unitario',
            field=models.FloatField(blank=True, db_column='COSTO_UNITARIO', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioattrezzature',
            name='descrizione',
            field=models.TextField(blank=True, db_column='DESCRIZIONE', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioattrezzature',
            name='quantita',
            field=models.IntegerField(blank=True, db_column='QUANTITA', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioattrezzature',
            name='tipologia',
            field=models.CharField(blank=True, db_column='TIPOLOGIA', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='laboratoriodatibase',
            name='id_dipartimento_riferimento',
            field=models.ForeignKey(blank=True, db_column='ID_DIPARTIMENTO_RIFERIMENTO', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticadipartimento'),
        ),
        migrations.AlterField(
            model_name='laboratoriodatibase',
            name='matricola_preposto_sicurezza',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_PREPOSTO_SICUREZZA', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matricola_preposto_sicurezza_personale', to='ricerca_app.personale'),
        ),
        migrations.AlterField(
            model_name='laboratoriodatibase',
            name='matricola_referente_compilazione',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_REFERENTE_COMPILAZIONE', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matricola_referente_compilazione_personale', to='ricerca_app.personale'),
        ),
        migrations.AlterField(
            model_name='laboratoriodatibase',
            name='matricola_responsabile_scientifico',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_RESPONSABILE_SCIENTIFICO', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matricola_responsabile_scientifico_personale', to='ricerca_app.personale'),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='anno',
            field=models.IntegerField(blank=False, db_column='ANNO', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='committenti',
            field=models.CharField(blank=False, db_column='COMMITTENTI', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='descrizione',
            field=models.TextField(blank=False, db_column='DESCRIZIONE', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='durata_mesi',
            field=models.IntegerField(blank=False, db_column='DURATA_MESI', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='importo_euro',
            field=models.FloatField(blank=False, db_column='IMPORTO_EURO', null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='matricola_responsabile',
            field=models.CharField(blank=True, db_column='MATRICOLA_RESPONSABILE', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='responsabile_origine',
            field=models.CharField(blank=True, db_column='RESPONSABILE_ORIGINE', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='laboratorioservizierogati',
            name='strumentazione',
            field=models.TextField(blank=False, db_column='STRUMENTAZIONE', null=True),
        ),
        migrations.CreateModel(
            name='LaboratorioTipologiaRischio',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tipologia_rischio', models.CharField(blank=True, db_column='TIPOLOGIA_RISCHIO', max_length=500, null=True)),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.CASCADE, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_TIPOLOGIA_RISCHIO',
                'managed': True,
            },
        ),
    ]
