# Generated by Django 3.2.13 on 2022-09-08 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0078_alter_didatticacdsaltridatiufficio_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='didatticacdsaltridatiufficio',
            name='cds',
            field=models.OneToOneField(db_column='CDS_ID', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.didatticacds'),
        ),
    ]
