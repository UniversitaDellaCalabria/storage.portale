# Generated by Django 3.2.13 on 2022-09-09 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0080_alter_didatticacdsaltridatiufficio_cds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='didatticacdsaltridati',
            name='cds',
        ),
        migrations.AddField(
            model_name='didatticacdsaltridati',
            name='regdid_id',
            field=models.OneToOneField(db_column='REGDID_ID', default=1, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ricerca_app.didatticaregolamento'),
            preserve_default=False,
        ),
    ]
