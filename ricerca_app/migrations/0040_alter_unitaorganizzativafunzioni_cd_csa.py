# Generated by Django 3.2.7 on 2021-12-06 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0039_brevettodatibase_nome_file_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitaorganizzativafunzioni',
            name='cd_csa',
            field=models.ForeignKey(blank=True, db_column='CD_CSA', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.unitaorganizzativa', to_field='cd_csa'),
        ),
    ]
