# Generated by Django 3.2.13 on 2023-06-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0143_auto_20230626_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='brevettodatibase',
            name='trl_iniziale',
            field=models.PositiveSmallIntegerField(blank=True, db_column='TRL_INIZIALE', null=True),
        ),
        migrations.AddField(
            model_name='brevettodatibase',
            name='valorizzazione',
            field=models.CharField(blank=True, db_column='VALORIZZAZIONE', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='brevettodatibase',
            name='trl_aggiornato',
            field=models.PositiveSmallIntegerField(blank=True, db_column='TRL_AGGIORNATO', null=True),
        ),
    ]