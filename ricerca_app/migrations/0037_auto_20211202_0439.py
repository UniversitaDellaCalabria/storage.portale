# Generated by Django 3.2.7 on 2021-12-02 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0036_laboratoriodatibase_nome_file_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitaorganizzativafunzioni',
            name='unita_organizzativa',
        ),
        migrations.AddField(
            model_name='unitaorganizzativa',
            name='cd_csa',
            field=models.CharField(blank=True, db_column='CD_CSA', max_length=40, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='unitaorganizzativafunzioni',
            name='cd_csa',
            field=models.ForeignKey(blank=True, db_column='CD_CSA', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.unitaorganizzativa'),
        ),
    ]
