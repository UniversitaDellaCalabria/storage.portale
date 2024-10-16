from django.contrib.auth import get_user_model
from django.db import models
from generics.models import VisibileAbstract


class SitoWebCdsOggettiPortale(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    cds = models.ForeignKey(
        "cds.DidatticaCds", models.DO_NOTHING, db_column="ID_DIDATTICA_CDS"
    )
    aa_regdid_id = models.IntegerField(db_column="AA_REGDID_ID")
    id_oggetto_portale = models.IntegerField(db_column="ID_OGGETTO_PORTALE")
    id_classe_oggetto_portale = models.CharField(
        db_column="ID_CLASSE_OGGETTO_PORTALE", max_length=1000
    )
    id_sito_web_cds_topic = models.IntegerField(
        db_column="ID_SITO_WEB_CDS_TOPIC", blank=True, null=True
    )
    titolo_it = models.TextField(db_column="TITOLO_IT")
    titolo_en = models.TextField(db_column="TITOLO_EN")
    testo_it = models.TextField(db_column="TESTO_IT", blank=True, null=True)
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    visibile = models.IntegerField(db_column="VISIBILE")
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.titolo_it} - {self.aa_regdid_id}"

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_OGGETTI_PORTALE"


class SitoWebArticoliRegolamentoStrutturaTopic(VisibileAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_sito_web_cds_topic = models.ForeignKey(
        "SitoWebCdsTopic", models.DO_NOTHING, db_column="ID_SITO_WEB_CDS_TOPIC"
    )
    id_did_art_regolamento_struttura = models.ForeignKey(
        "regdid.DidatticaArticoliRegolamentoStruttura",
        models.DO_NOTHING,
        db_column="ID_DID_ART_REGOLAMENTO_STRUTTURA",
    )
    titolo_it = models.TextField(db_column="TITOLO_IT")
    titolo_en = models.TextField(db_column="TITOLO_EN", blank=True, null=True)
    ordine = models.IntegerField(db_column="ORDINE", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_ARTICOLI_REGOLAMENTO_STRUTTURA_TOPIC"


class SitoWebCdsTopic(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_topic_it = models.CharField(db_column="DESCR_TOPIC_IT", max_length=2000)
    descr_topic_en = models.CharField(
        db_column="DESCR_TOPIC_EN", max_length=2000, blank=True, null=True
    )
    tag = models.CharField(db_column="TAG", max_length=100, blank=True, null=True)
    visibile = models.IntegerField(db_column="VISIBILE")
    dt_mod = models.DateField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_TOPIC"


class SitoWebCdsTopicArticoliReg(VisibileAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    titolo_it = models.CharField(db_column="TITOLO_IT", max_length=1000)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=1000, blank=True, null=True
    )
    testo_it = models.TextField(db_column="TESTO_IT", blank=True, null=True)
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    id_sito_web_cds_topic = models.ForeignKey(
        "SitoWebCdsTopic", models.PROTECT, db_column="ID_SITO_WEB_CDS_TOPIC"
    )
    id_sito_web_cds_oggetti_portale = models.ForeignKey(
        "SitoWebCdsOggettiPortale",
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_OGGETTI_PORTALE",
        blank=True,
        null=True,
    )
    id_didattica_cds_articoli_regolamento = models.ForeignKey(
        "regdid.DidatticaCdsArticoliRegolamento",
        models.CASCADE,
        db_column="ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO",
        blank=True,
        null=True,
    )
    ordine = models.IntegerField(db_column="ORDINE")
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_TOPIC_ARTICOLI_REG"
        unique_together = (
            ("id_sito_web_cds_topic", "id_didattica_cds_articoli_regolamento"),
        )


class SitoWebCdsSubArticoliRegolamento(VisibileAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_sito_web_cds_topic_articoli_reg = models.ForeignKey(
        "SitoWebCdsTopicArticoliReg",
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_TOPIC_ARTICOLI_REG",
        blank=True,
        null=True,
    )
    titolo_it = models.CharField(db_column="TITOLO_IT", max_length=1000)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=1000, blank=True, null=True
    )
    testo_it = models.TextField(db_column="TESTO_IT")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    ordine = models.IntegerField(db_column="ORDINE")
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_SUB_ARTICOLI_REGOLAMENTO"


class SitoWebCdsTipoDato(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_breve = models.CharField(db_column="DESCR_BREVE", max_length=100)
    descr_lunga = models.CharField(
        db_column="DESCR_LUNGA", max_length=2000, blank=True, null=True
    )

    def __str__(self):
        return self.descr_breve

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_TIPO_DATO"


class SitoWebCdsTopicArticoliRegAltriDati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_sito_web_cds_topic_articoli_reg = models.ForeignKey(
        SitoWebCdsTopicArticoliReg,
        models.CASCADE,
        db_column="ID_SITO_WEB_CDS_TOPIC_ARTICOLI_REG",
    )
    ordine = models.PositiveIntegerField(db_column="ORDINE")
    id_sito_web_cds_tipo_dato = models.ForeignKey(
        SitoWebCdsTipoDato, models.PROTECT, db_column="ID_SITO_WEB_CDS_TIPO_DATO"
    )
    titolo_it = models.CharField(
        db_column="TITOLO_IT", max_length=1000, blank=True, null=True
    )
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=1000, blank=True, null=True
    )
    testo_it = models.TextField(db_column="TESTO_IT")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    link = models.CharField(db_column="LINK", max_length=1000, blank=True, null=True)
    visibile = models.IntegerField(db_column="VISIBILE")
    dt_mod = models.DateField(db_column="DT_MOD")
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SITO_WEB_CDS_TOPIC_ARTICOLI_REG_ALTRI_DATI"
