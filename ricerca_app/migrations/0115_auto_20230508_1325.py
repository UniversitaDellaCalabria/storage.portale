# Generated by Django 3.2.13 on 2023-05-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ricerca_app', '0114_auto_20230428_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brevettodatibase',
            name='url_immagine',
            field=models.URLField(blank=True, db_column='URL_IMMAGINE', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='brevettodatibase',
            name='url_knowledge_share',
            field=models.URLField(blank=True, db_column='URL_KNOWLEDGE_SHARE', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='didatticaattivitaformativa',
            name='url_sito_web',
            field=models.URLField(blank=True, db_column='URL_SITO_WEB', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='didatticacds',
            name='cds_url_info_web',
            field=models.URLField(blank=True, db_column='CDS_URL_INFO_WEB', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='didatticacds',
            name='url',
            field=models.URLField(blank=True, db_column='URL', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='didatticadipartimento',
            name='url_pubbl_off_f',
            field=models.URLField(blank=True, db_column='URL_PUBBL_OFF_F', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='didatticadipartimentourl',
            name='dip_url',
            field=models.URLField(db_column='DIP_URL', max_length=4000),
        ),
        migrations.AlterField(
            model_name='didatticadottoratocds',
            name='cds_url_info_web',
            field=models.URLField(blank=True, db_column='CDS_URL_INFO_WEB', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='didatticadottoratocds',
            name='url',
            field=models.URLField(blank=True, db_column='URL', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='didatticatestiregolamento',
            name='testo_regdid_url',
            field=models.URLField(blank=True, db_column='TESTO_REGDID_URL', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='docentematerialedidattico',
            name='url_testo',
            field=models.URLField(blank=True, db_column='URL_TESTO', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='docentematerialedidattico',
            name='url_testo_en',
            field=models.URLField(blank=True, db_column='URL_TESTO_EN', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='docenteptabacheca',
            name='url_testo',
            field=models.URLField(blank=True, db_column='URL_TESTO', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='docenteptabacheca',
            name='url_testo_en',
            field=models.URLField(blank=True, db_column='URL_TESTO_EN', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='personale',
            name='urlcv',
            field=models.URLField(blank=True, db_column='URLCV', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='progettodatibase',
            name='url_immagine',
            field=models.URLField(blank=True, db_column='URL_IMMAGINE', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='progettodatibase',
            name='url_sito_web',
            field=models.URLField(blank=True, db_column='URL_SITO_WEB', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='pubblicazionedatibase',
            name='url_pubblicazione',
            field=models.URLField(blank=True, db_column='URL_PUBBLICAZIONE', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='spinoffstartupdatibase',
            name='url_sito_web',
            field=models.URLField(blank=True, db_column='URL_SITO_WEB', max_length=4000, null=True),
        ),
    ]
