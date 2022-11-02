# Generated by Django 3.2.13 on 2022-10-25 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0090_docentematerialedidattico_docenteptaaltridati_docenteptabacheca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docentematerialedidattico',
            name='matricola',
            field=models.ForeignKey(db_column='MATRICOLA', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale', to_field='matricola'),
        ),
        migrations.AlterField(
            model_name='docenteptaaltridati',
            name='matricola',
            field=models.OneToOneField(db_column='MATRICOLA', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale', to_field='matricola'),
        ),
        migrations.AlterField(
            model_name='docenteptabacheca',
            name='matricola',
            field=models.ForeignKey(db_column='MATRICOLA', on_delete=django.db.models.deletion.DO_NOTHING, to='ricerca_app.personale', to_field='matricola'),
        ),
    ]
