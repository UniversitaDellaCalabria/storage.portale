# Generated by Django 3.2.7 on 2022-03-08 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0054_alter_unitaorganizzativafunzioni_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitaorganizzativafunzioni',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterModelTable(
            name='unitaorganizzativafunzioni',
            table='UNITA_ORGANIZZATIVA_FUNZIONI',
        ),
    ]