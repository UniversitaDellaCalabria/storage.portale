# Generated by Django 3.2.13 on 2023-06-20 10:42

from django.db import migrations, models
import ricerca_app.models
import ricerca_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0136_auto_20230615_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='brevettodatibase',
            name='is_active',
            field=models.BooleanField(db_column='ATTIVO', default=True),
        ),
    ]
