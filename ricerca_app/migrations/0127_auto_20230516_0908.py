# Generated by Django 3.2.13 on 2023-05-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0126_auto_20230512_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docentematerialedidattico',
            name='titolo',
            field=models.CharField(db_column='TITOLO', max_length=200),
        ),
    ]
