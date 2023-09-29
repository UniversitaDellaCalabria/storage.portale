# Generated by Django 3.2 on 2021-07-30 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0013_didatticatestiregolamento_testo_regdid_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratoriodatibase',
            name='sito_web',
            field=models.CharField(blank=True, db_column='SITO_WEB', max_length=1024, null=True),
        ),
        migrations.CreateModel(
            name='LaboratorioAltriDipartimenti',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descr_dip_lab', models.CharField(blank=True, max_length=400, null=True)),
                ('id_dip', models.ForeignKey(blank=True, db_column='id_dip', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticadipartimento')),
                ('id_laboratorio_dati', models.ForeignKey(blank=True, db_column='ID_LABORATORIO_DATI', null=True, on_delete=django.db.models.deletion.CASCADE, to='ricerca_app.laboratoriodatibase')),
            ],
            options={
                'db_table': 'LABORATORIO_ALTRI_DIPARTIMENTI',
                'managed': True,
            },
        ),
    ]
