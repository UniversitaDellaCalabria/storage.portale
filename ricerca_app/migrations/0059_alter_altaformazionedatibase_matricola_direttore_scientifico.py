# Generated by Django 3.2.7 on 2022-03-22 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0058_alter_unitaorganizzativafunzioni_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='altaformazionedatibase',
            name='matricola_direttore_scientifico',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA_DIRETTORE_SCIENTIFICO', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.personale', to_field='matricola'),
        ),
    ]
