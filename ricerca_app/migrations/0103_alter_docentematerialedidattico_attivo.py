# Generated by Django 3.2.13 on 2023-04-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0102_alter_docenteptabacheca_attivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docentematerialedidattico',
            name='attivo',
            field=models.BooleanField(db_column='ATTIVO'),
        ),
    ]
