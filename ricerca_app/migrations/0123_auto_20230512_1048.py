# Generated by Django 3.2.13 on 2023-05-12 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0122_auto_20230511_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='didatticadottoratoattivitaformativa',
            name='id_struttura_proponente',
            field=models.ForeignKey(blank=True, db_column='ID_STRUTTURA_PROPONENTE', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.unitaorganizzativa'),
        ),
        migrations.AlterField(
            model_name='didatticadottoratoattivitaformativa',
            name='rif_dottorato',
            field=models.CharField(blank=True, db_column='RIF_DOTTORATO', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='didatticadottoratoattivitaformativa',
            name='tipo_af',
            field=models.CharField(db_column='TIPO_AF', max_length=500),
        ),
    ]
