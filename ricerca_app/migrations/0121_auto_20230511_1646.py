# Generated by Django 3.2.13 on 2023-05-11 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0120_auto_20230511_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brevettodatibase',
            name='territorio',
            field=models.ForeignKey(blank=True, db_column='TERRITORIO', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ricerca_app.brevettoterritori'),
        ),
    ]
