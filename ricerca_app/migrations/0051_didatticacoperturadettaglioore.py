# Generated by Django 3.2.7 on 2022-02-23 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0050_auto_20220222_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='DidatticaCoperturaDettaglioOre',
            fields=[
                ('ore_coper_det_id', models.IntegerField(db_column='ORE_COPER_DET_ID', primary_key=True, serialize=False)),
                ('tipo_att_did_cod', models.CharField(db_column='TIPO_ATT_DID_COD', max_length=10)),
                ('ore', models.DecimalField(db_column='ORE', decimal_places=2, max_digits=6)),
                ('dt_ins', models.DateField(blank=True, db_column='DT_INS', null=True)),
                ('dt_mod', models.DateField(blank=True, db_column='DT_MOD', null=True)),
                ('coper', models.ForeignKey(db_column='COPER_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticacopertura')),
            ],
            options={
                'db_table': 'DIDATTICA_COPERTURA_DETTAGLIO_ORE',
                'managed': True,
            },
        ),
    ]
