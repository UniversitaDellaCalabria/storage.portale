# Generated by Django 3.2.13 on 2022-10-03 19:56

from django.db import migrations, models
import ricerca_app.models
import ricerca_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0083_auto_20220929_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spinoffstartupdatibase',
            name='nome_file_logo',
            field=models.FileField(blank=True, db_column='NOME_FILE_LOGO', max_length=1000, null=True, upload_to=ricerca_app.models.companies_media_path, validators=[ricerca_app.validators.validate_image_file_extension, ricerca_app.validators.validate_file_size]),
        ),
    ]