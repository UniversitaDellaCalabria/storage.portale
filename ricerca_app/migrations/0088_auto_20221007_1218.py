# Generated by Django 3.2.13 on 2022-10-07 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0087_auto_20221007_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progettoresponsabilescientifico',
            name='matricola',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale', to_field='matricola'),
        ),
        migrations.AlterField(
            model_name='progettoricercatore',
            name='matricola',
            field=models.ForeignKey(blank=True, db_column='MATRICOLA', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale', to_field='matricola'),
        ),
    ]