# Generated by Django 3.2.19 on 2023-06-06 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ricerca_app', '0134_auto_20230606_1232'),
    ]

    operations = [
        # migrations.AlterField(
            # model_name='sitowebcdsarticoliregaltridati',
            # name='id_user_mod',
            # field=models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        # ),
        migrations.AlterField(
            model_name='sitowebcdsarticoliregolamento',
            name='id_user_mod',
            field=models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sitowebcdsoggettiportale',
            name='id_user_mod',
            field=models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        # migrations.AlterField(
            # model_name='sitowebcdsoggettiportalealtridati',
            # name='id_user_mod',
            # field=models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True),
        # ),
        migrations.AlterField(
            model_name='sitowebcdstopic',
            name='id_user_mod',
            field=models.ForeignKey(blank=True, db_column='ID_USER_MOD', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sitowebcdstopicarticolireg',
            name='id_user_mod',
            field=models.IntegerField(blank=True, db_column='ID_USER_MOD', null=True),
        ),
    ]
