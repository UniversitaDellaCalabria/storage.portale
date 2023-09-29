# Generated by Django 3.2 on 2021-07-20 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0010_auto_20210720_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricercaerc0',
            name='description_en',
            field=models.CharField(blank=True, db_column='DESCRIPTION_EN', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laboratoriopersonalericerca',
            name='matricola_personale_ricerca',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_PERSONALE_RICERCA', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.personale'),
        ),
        migrations.AlterField(
            model_name='laboratoriopersonaletecnico',
            name='matricola_personale_tecnico',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_PERSONALE_TECNICO', null=True, on_delete=django.db.models.deletion.CASCADE, to='ricerca_app.personale'),
        ),
    ]
