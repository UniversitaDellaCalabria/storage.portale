# Generated by Django 3.2.7 on 2021-11-17 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0025_auto_20211115_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaboratorioInfrastruttura',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descrizione', models.CharField(db_column='DESCRIZIONE', max_length=1000)),
            ],
            options={
                'db_table': 'LABORATORIO_INFRASTRUTTURA',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='laboratoriodatibase',
            name='infrastruttura_riferimento',
        ),
        migrations.AddField(
            model_name='laboratoriodatibase',
            name='id_infrastruttura_riferimento',
            field=models.ForeignKey(blank=True, db_column='ID_INFRASTRUTTURA_RIFERIMENTO', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.laboratorioinfrastruttura'),
        ),
    ]
