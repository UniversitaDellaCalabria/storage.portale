# Generated by Django 3.2.7 on 2022-02-09 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0046_progettoricercatore'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricercagruppo',
            name='ricerca_erc1',
            field=models.ForeignKey(blank=True, db_column='RICERCA_ERC1_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.ricercaerc1'),
        ),
    ]
