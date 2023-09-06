# Generated by Django 3.2.20 on 2023-09-05 10:32

from django.db import migrations, models
import ricerca_app.models
import ricerca_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0148_auto_20230901_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratoriodatibase',
            name='nome_file_logo',
            field=models.FileField(blank=True, db_column='NOME_FILE_LOGO', max_length=1000, null=True, upload_to=ricerca_app.models.patents_media_path, validators=[ricerca_app.validators.validate_image_file_extension, ricerca_app.validators.validate_file_size]),

        ),
    ]
