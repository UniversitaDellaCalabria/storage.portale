from django.db import models
from generics.validators import validate_image_file_extension, validate_file_size
from patents.settings import patents_media_path


class BrevettoDirittiCommerciali(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_diritto = models.CharField(db_column="DESCR_DIRITTO", max_length=1000)

    def __str__(self):  # pragma: no cover
        return self.descr_diritto

    class Meta:
        managed = True
        db_table = "BREVETTO_DIRITTI_COMMERCIALI"


class BrevettoTerritori(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    territorio = models.CharField(db_column="TERRITORIO", max_length=80)

    def __str__(self):  # pragma: no cover
        return self.territorio

    class Meta:
        managed = True
        db_table = "BREVETTO_TERRITORI"


class BrevettoDisponibilita(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_disponibilita = models.CharField(
        db_column="DESCR_DISPONIBILITA", max_length=1000
    )

    def __str__(self):  # pragma: no cover
        return self.descr_disponibilita

    class Meta:
        managed = True
        db_table = "BREVETTO_DISPONIBILITA"


class BrevettoStatusLegale(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_status = models.CharField(db_column="DESCR_STATUS", max_length=1000)

    def __str__(self):  # pragma: no cover
        return self.descr_status

    class Meta:
        managed = True
        db_table = "BREVETTO_STATUS_LEGALE"


class BrevettoDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_univoco = models.CharField(db_column="ID_UNIVOCO", max_length=500, unique=True)
    titolo = models.TextField(db_column="TITOLO")
    url_immagine = models.URLField(
        db_column="URL_IMMAGINE", max_length=2000, blank=True, null=True
    )
    breve_descrizione = models.TextField(db_column="BREVE_DESCRIZIONE")
    area_tecnologica = models.ForeignKey(
        "companies.TipologiaAreaTecnologica",
        models.SET_NULL,
        db_column="ID_AREA_TECNOLOGICA",
        blank=True,
        null=True,
    )
    url_knowledge_share = models.URLField(
        db_column="URL_KNOWLEDGE_SHARE", max_length=2000, blank=True, null=True
    )
    applicazioni = models.TextField(db_column="APPLICAZIONI", blank=True, null=True)
    vantaggi = models.TextField(db_column="VANTAGGI", blank=True, null=True)
    trl_iniziale = models.PositiveSmallIntegerField(
        db_column="TRL_INIZIALE", blank=True, null=True
    )
    trl_aggiornato = models.PositiveSmallIntegerField(
        db_column="TRL_AGGIORNATO", blank=True, null=True
    )
    proprieta = models.TextField(db_column="PROPRIETA")
    status_legale = models.ForeignKey(
        BrevettoStatusLegale,
        models.SET_NULL,
        db_column="ID_STATUS_LEGALE",
        blank=True,
        null=True,
    )
    data_priorita = models.DateField(db_column="DATA_PRIORITA", blank=True, null=True)
    territorio = models.ForeignKey(
        BrevettoTerritori,
        models.SET_NULL,
        db_column="ID_BREVETTO_TERRITORI",
        blank=True,
        null=True,
    )
    diritto_commerciale = models.ForeignKey(
        BrevettoDirittiCommerciali,
        models.SET_NULL,
        db_column="ID_DIRITTO_COMMERCIALE",
        blank=True,
        null=True,
    )
    disponibilita = models.ForeignKey(
        BrevettoDisponibilita,
        models.SET_NULL,
        db_column="ID_DISPONIBILITA",
        blank=True,
        null=True,
    )

    area_ks = models.CharField(
        db_column="AREA_KS", max_length=2000, blank=True, null=True
    )
    nome_file_logo = models.FileField(
        upload_to=patents_media_path,
        validators=[validate_image_file_extension, validate_file_size],
        db_column="NOME_FILE_LOGO",
        max_length=1000,
        blank=True,
        null=True,
    )
    valorizzazione = models.CharField(
        max_length=255, blank=True, null=True, db_column="VALORIZZAZIONE"
    )
    is_active = models.BooleanField(default=True, db_column="ATTIVO")
    ordinamento = models.IntegerField(default=10, db_column="ORDINE")

    class Meta:
        managed = True
        db_table = "BREVETTO_DATI_BASE"
        ordering = ["ordinamento"]


class BrevettoInventori(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    brevetto = models.ForeignKey(
        BrevettoDatiBase, models.CASCADE, db_column="ID_BREVETTO", blank=True, null=True
    )
    matricola_inventore = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
        blank=True,
        null=True,
    )
    cognomenome_origine = models.CharField(
        db_column="COGNOMENOME_ORIGINE", max_length=200
    )

    def __str__(self):  # pragma: no cover
        return self.cognomenome_origine

    class Meta:
        managed = True
        db_table = "BREVETTO_INVENTORI"
