# Generated by Django 3.2.13 on 2023-03-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0100_alter_didatticadottoratoattivitaformativa_visualizza_orario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spinoffstartupdatibase',
            name='is_spinoff',
            field=models.BooleanField(db_column='IS_SPINOFF', default=False),
        ),
        migrations.AlterField(
            model_name='spinoffstartupdatibase',
            name='is_startup',
            field=models.BooleanField(db_column='IS_STARTUP', default=False),
        ),
    ]
