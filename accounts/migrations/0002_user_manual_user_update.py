# Generated by Django 4.2.10 on 2024-10-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="manual_user_update",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Ultimo aggiornamento manuale dei dati",
            ),
        ),
    ]
