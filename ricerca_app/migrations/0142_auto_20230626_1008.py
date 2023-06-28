# Generated by Django 3.2.13 on 2023-06-26 10:08

from django.db import migrations, models
import ricerca_app.models
import ricerca_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0141_auto_20230621_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docenteptaaltridati',
            name='path_cv_en',
            field=models.FileField(blank=True, db_column='PATH_CV_EN', max_length=500, null=True, upload_to=ricerca_app.models.teacher_cv_en_media_path, validators=[ricerca_app.validators.validate_pdf_file_extension, ricerca_app.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='docenteptaaltridati',
            name='path_cv_ita',
            field=models.FileField(blank=True, db_column='PATH_CV_ITA', max_length=500, null=True, upload_to=ricerca_app.models.teacher_cv_ita_media_path, validators=[ricerca_app.validators.validate_pdf_file_extension, ricerca_app.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='docenteptaaltridati',
            name='path_foto',
            field=models.FileField(blank=True, db_column='PATH_FOTO', max_length=500, null=True, upload_to=ricerca_app.models.teacher_photo_media_path, validators=[ricerca_app.validators.validate_image_file_extension, ricerca_app.validators.validate_file_size, ricerca_app.validators.validate_image_size_ratio]),
        ),
    ]