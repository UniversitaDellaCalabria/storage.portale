# Generated by Django 3.2.13 on 2023-05-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0125_auto_20230512_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='didatticadottoratoattivitaformativa',
            name='struttura_proponente_origine',
            field=models.CharField(blank=True, db_column='STRUTTURA_PROPONENTE_ORIGINE', max_length=255, null=True),
        ),
    ]
