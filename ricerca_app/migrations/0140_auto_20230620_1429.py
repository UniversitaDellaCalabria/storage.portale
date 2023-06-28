# Generated by Django 3.2.13 on 2023-06-20 14:29

from django.db import migrations, models
import ricerca_app.models
import ricerca_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0139_auto_20230620_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progettodatibase',
            options={'managed': True, 'ordering': ['ordinamento']},
        ),
        migrations.AddField(
            model_name='progettodatibase',
            name='is_active',
            field=models.BooleanField(db_column='ATTIVO', default=True),
        ),
        migrations.AddField(
            model_name='progettodatibase',
            name='ordinamento',
            field=models.IntegerField(db_column='ORDINAMENTO', default=10),
        ),
    ]