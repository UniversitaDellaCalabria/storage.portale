# Generated by Django 3.2.13 on 2023-04-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0102_sitowebcdsdatibase_aa'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitowebcdsexstudenti',
            name='nome',
            field=models.CharField(blank=True, db_column='NOME', max_length=1000, null=True),
        ),
    ]
