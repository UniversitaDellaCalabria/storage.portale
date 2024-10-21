# Generated by Django 4.2.16 on 2024-10-21 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("regdid", "0001_initial"),
        ("cds", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SitoWebCdsOggettiPortale",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("aa_regdid_id", models.IntegerField(db_column="AA_REGDID_ID")),
                (
                    "id_oggetto_portale",
                    models.IntegerField(db_column="ID_OGGETTO_PORTALE"),
                ),
                (
                    "id_classe_oggetto_portale",
                    models.CharField(
                        db_column="ID_CLASSE_OGGETTO_PORTALE", max_length=1000
                    ),
                ),
                ("titolo_it", models.TextField(db_column="TITOLO_IT")),
                ("titolo_en", models.TextField(db_column="TITOLO_EN")),
                (
                    "testo_it",
                    models.TextField(blank=True, db_column="TESTO_IT", null=True),
                ),
                (
                    "testo_en",
                    models.TextField(blank=True, db_column="TESTO_EN", null=True),
                ),
                ("visibile", models.IntegerField(db_column="VISIBILE")),
                ("dt_mod", models.DateTimeField(db_column="DT_MOD")),
                (
                    "cds",
                    models.ForeignKey(
                        db_column="ID_DIDATTICA_CDS",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="cds.didatticacds",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_OGGETTI_PORTALE",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SitoWebCdsTipoDato",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "descr_breve",
                    models.CharField(db_column="DESCR_BREVE", max_length=100),
                ),
                (
                    "descr_lunga",
                    models.CharField(
                        blank=True, db_column="DESCR_LUNGA", max_length=2000, null=True
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_TIPO_DATO",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SitoWebCdsTopic",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "descr_topic_it",
                    models.CharField(db_column="DESCR_TOPIC_IT", max_length=2000),
                ),
                (
                    "descr_topic_en",
                    models.CharField(
                        blank=True,
                        db_column="DESCR_TOPIC_EN",
                        max_length=2000,
                        null=True,
                    ),
                ),
                (
                    "tag",
                    models.CharField(
                        blank=True, db_column="TAG", max_length=100, null=True
                    ),
                ),
                ("visibile", models.IntegerField(db_column="VISIBILE")),
                ("dt_mod", models.DateField(db_column="DT_MOD")),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_TOPIC",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SitoWebCdsTopicArticoliReg",
            fields=[
                ("visibile", models.BooleanField(db_column="VISIBILE", default=False)),
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("titolo_it", models.CharField(db_column="TITOLO_IT", max_length=1000)),
                (
                    "titolo_en",
                    models.CharField(
                        blank=True, db_column="TITOLO_EN", max_length=1000, null=True
                    ),
                ),
                (
                    "testo_it",
                    models.TextField(blank=True, db_column="TESTO_IT", null=True),
                ),
                (
                    "testo_en",
                    models.TextField(blank=True, db_column="TESTO_EN", null=True),
                ),
                ("ordine", models.IntegerField(db_column="ORDINE")),
                ("dt_mod", models.DateTimeField(db_column="DT_MOD")),
                (
                    "didattica_cds_articoli_regolamento",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="regdid.didatticacdsarticoliregolamento",
                    ),
                ),
                (
                    "sito_web_cds_oggetti_portale",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_SITO_WEB_CDS_OGGETTI_PORTALE",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cds_websites.sitowebcdsoggettiportale",
                    ),
                ),
                (
                    "sito_web_cds_topic",
                    models.ForeignKey(
                        db_column="ID_SITO_WEB_CDS_TOPIC",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="cds_websites.sitowebcdstopic",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_TOPIC_ARTICOLI_REG",
                "managed": True,
                "unique_together": {
                    ("sito_web_cds_topic", "didattica_cds_articoli_regolamento")
                },
            },
        ),
        migrations.CreateModel(
            name="SitoWebCdsTopicArticoliRegAltriDati",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("ordine", models.PositiveIntegerField(db_column="ORDINE")),
                (
                    "titolo_it",
                    models.CharField(
                        blank=True, db_column="TITOLO_IT", max_length=1000, null=True
                    ),
                ),
                (
                    "titolo_en",
                    models.CharField(
                        blank=True, db_column="TITOLO_EN", max_length=1000, null=True
                    ),
                ),
                ("testo_it", models.TextField(db_column="TESTO_IT")),
                (
                    "testo_en",
                    models.TextField(blank=True, db_column="TESTO_EN", null=True),
                ),
                (
                    "link",
                    models.CharField(
                        blank=True, db_column="LINK", max_length=1000, null=True
                    ),
                ),
                ("visibile", models.IntegerField(db_column="VISIBILE")),
                ("dt_mod", models.DateField(db_column="DT_MOD")),
                (
                    "sito_web_cds_tipo_dato",
                    models.ForeignKey(
                        db_column="ID_SITO_WEB_CDS_TIPO_DATO",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="cds_websites.sitowebcdstipodato",
                    ),
                ),
                (
                    "sito_web_cds_topic_articoli_reg",
                    models.ForeignKey(
                        db_column="ID_SITO_WEB_CDS_TOPIC_ARTICOLI_REG",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cds_websites.sitowebcdstopicarticolireg",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_TOPIC_ARTICOLI_REG_ALTRI_DATI",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SitoWebCdsSubArticoliRegolamento",
            fields=[
                ("visibile", models.BooleanField(db_column="VISIBILE", default=False)),
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("titolo_it", models.CharField(db_column="TITOLO_IT", max_length=1000)),
                (
                    "titolo_en",
                    models.CharField(
                        blank=True, db_column="TITOLO_EN", max_length=1000, null=True
                    ),
                ),
                ("testo_it", models.TextField(db_column="TESTO_IT")),
                (
                    "testo_en",
                    models.TextField(blank=True, db_column="TESTO_EN", null=True),
                ),
                ("ordine", models.IntegerField(db_column="ORDINE")),
                ("dt_mod", models.DateTimeField(db_column="DT_MOD")),
                (
                    "sito_web_cds_topic_articoli_reg",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_SITO_WEB_CDS_TOPIC_ARTICOLI_REG",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cds_websites.sitowebcdstopicarticolireg",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="user_mod_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_CDS_SUB_ARTICOLI_REGOLAMENTO",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SitoWebArticoliRegolamentoStrutturaTopic",
            fields=[
                ("visibile", models.BooleanField(db_column="VISIBILE", default=False)),
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                ("titolo_it", models.TextField(db_column="TITOLO_IT")),
                (
                    "titolo_en",
                    models.TextField(blank=True, db_column="TITOLO_EN", null=True),
                ),
                (
                    "ordine",
                    models.IntegerField(blank=True, db_column="ORDINE", null=True),
                ),
                ("dt_mod", models.DateTimeField(db_column="DT_MOD")),
                (
                    "did_art_regolamento_struttura",
                    models.ForeignKey(
                        db_column="ID_DID_ART_REGOLAMENTO_STRUTTURA",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="regdid.didatticaarticoliregolamentostruttura",
                    ),
                ),
                (
                    "sito_web_cds_topic",
                    models.ForeignKey(
                        db_column="ID_SITO_WEB_CDS_TOPIC",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="cds_websites.sitowebcdstopic",
                    ),
                ),
                (
                    "user_mod",
                    models.ForeignKey(
                        db_column="user_mod_id",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "SITO_WEB_ARTICOLI_REGOLAMENTO_STRUTTURA_TOPIC",
                "managed": True,
            },
        ),
    ]
