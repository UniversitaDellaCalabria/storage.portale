# Generated by Django 3.2.20 on 2023-09-01 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0147_auto_20230721_1256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='didatticaattivitaformativa',
            options={'managed': True, 'ordering': ('ciclo_des',)},
        ),
        migrations.AlterModelOptions(
            name='didatticapianosceltaaf',
            options={'managed': True, 'ordering': ('ciclo_des',)},
        ),
    ]
