# Generated by Django 3.2.4 on 2021-08-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0016_auto_20210811_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubblicazionedatibase',
            name='url_pubblicazione',
            field=models.CharField(blank=True, db_column='URL_PUBBLICAZIONE', max_length=500, null=True),
        ),
    ]
