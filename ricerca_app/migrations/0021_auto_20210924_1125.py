# Generated by Django 3.2.7 on 2021-09-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0020_auto_20210915_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='didatticacopertura',
            name='coper_peso',
            field=models.FloatField(blank=True, db_column='COPER_PESO', null=True),
        ),
        migrations.AddField(
            model_name='didatticacopertura',
            name='ore',
            field=models.PositiveIntegerField(blank=True, db_column='ORE', null=True),
        ),
    ]
