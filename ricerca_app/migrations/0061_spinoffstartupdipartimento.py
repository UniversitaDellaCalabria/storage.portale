# Generated by Django 3.2.7 on 2022-05-20 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0060_didatticadottoratoattivitaformativa_didatticadottoratoattivitaformativaaltridocenti_didatticadottora'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpinoffStartupDipartimento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome_origine_dipartimento', models.CharField(db_column='NOME_ORIGINE_DIPARTIMENTO', max_length=1000)),
                ('id_didattica_dipartimento', models.ForeignKey(blank=True, db_column='ID_DIDATTICA_DIPARTIMENTO', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticadipartimento')),
                ('id_spinoff_startup_dati_base', models.ForeignKey(db_column='ID_SPINOFF_STARTUP_DATI_BASE', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.spinoffstartupdatibase')),
            ],
            options={
                'db_table': 'SPINOFF_STARTUP_DIPARTIMENTO',
                'managed': True,
            },
        ),
    ]