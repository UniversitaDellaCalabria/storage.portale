# Generated by Django 4.2.10 on 2024-02-16 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ricerca_app", "0156_alter_didatticacdsaltridatiufficio_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DidatticaRegolamentoTipologiaAltriDati",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "tipo_testo_regdid_cod",
                    models.CharField(
                        db_column="TIPO_TESTO_REGDID_COD", max_length=100, unique=True
                    ),
                ),
                (
                    "tipo_testo_regdid_des",
                    models.CharField(
                        db_column="TIPO_TESTO_REGDID_DES", max_length=2000
                    ),
                ),
                (
                    "dt_mod",
                    models.DateTimeField(blank=True, db_column="DT_MOD", null=True),
                ),
                (
                    "id_user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_USER_MOD",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_REGOLAMENTO_TIPOLOGIA_ALTRI_DATI",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DidatticaRegolamentoAltriDati",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "clob_txt_ita",
                    models.TextField(blank=True, db_column="CLOB_TXT_ITA", null=True),
                ),
                (
                    "clob_txt_eng",
                    models.TextField(blank=True, db_column="CLOB_TXT_ENG", null=True),
                ),
                (
                    "dt_mod",
                    models.DateTimeField(blank=True, db_column="DT_MOD", null=True),
                ),
                (
                    "id_user_mod",
                    models.ForeignKey(
                        blank=True,
                        db_column="ID_USER_MOD",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "regdid",
                    models.ForeignKey(
                        db_column="REGDID_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ricerca_app.didatticaregolamento",
                    ),
                ),
                (
                    "tipo_testo_regdid_cod",
                    models.ForeignKey(
                        db_column="TIPO_TESTO_REGDID_COD",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ricerca_app.didatticaregolamentotipologiaaltridati",
                        to_field="tipo_testo_regdid_cod",
                    ),
                ),
            ],
            options={
                "db_table": "DIDATTICA_REGOLAMENTO_ALTRI_DATI",
                "managed": True,
            },
        ),
    ]
