from django.db import models


class ProgettoAmbitoTerritoriale(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)

    ambito_territoriale = models.CharField(
        db_column="AMBITO_TERRITORIALE", max_length=100
    )

    def __str__(self):  # pragma: no cover
        return self.ambito_territoriale

    class Meta:
        managed = True
        db_table = "PROGETTO_AMBITO_TERRITORIALE"


class ProgettoDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)

    anno_avvio = models.IntegerField(db_column="ANNO_AVVIO", blank=True, null=True)
    id_ambito_territoriale = models.ForeignKey(
        ProgettoAmbitoTerritoriale,
        models.SET_NULL,
        db_column="ID_AMBITO_TERRITORIALE",
        blank=True,
        null=True,
    )
    id_tipologia_programma = models.ForeignKey(
        "ProgettoTipologiaProgramma",
        models.SET_NULL,
        db_column="ID_TIPOLOGIA_PROGRAMMA",
        blank=True,
        null=True,
    )
    id_area_tecnologica = models.ForeignKey(
        "companies.TipologiaAreaTecnologica",
        models.SET_NULL,
        db_column="ID_AREA_TECNOLOGICA",
        blank=True,
        null=True,
    )
    uo = models.ForeignKey(
        "structures.UnitaOrganizzativa",
        models.DO_NOTHING,
        to_field="uo",
        db_column="UO",
        blank=True,
        null=True,
    )

    titolo = models.CharField(
        db_column="TITOLO", max_length=4000, blank=True, null=True
    )

    descr_breve = models.TextField(db_column="DESCR_BREVE", blank=True, null=True)
    url_immagine = models.URLField(
        db_column="URL_IMMAGINE", max_length=1000, blank=True, null=True
    )

    abstract_ita = models.TextField(db_column="ABSTRACT_ITA", blank=True, null=True)

    abstract_eng = models.TextField(db_column="ABSTRACT_ENG", blank=True, null=True)
    url_sito_web = models.URLField(
        db_column="URL_SITO_WEB", max_length=1000, blank=True, null=True
    )
    call = models.CharField(db_column="CALL", max_length=1000, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_column="ATTIVO")
    ordinamento = models.IntegerField(default=10, db_column="ORDINE")

    class Meta:
        managed = True
        db_table = "PROGETTO_DATI_BASE"
        ordering = ["ordinamento"]


class ProgettoRicercatore(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        to_field="matricola",
        db_column="MATRICOLA",
        blank=True,
        null=True,
    )
    nome_origine = models.CharField(db_column="NOME_ORIGINE", max_length=1000)
    id_progetto = models.ForeignKey(
        ProgettoDatiBase, models.CASCADE, db_column="ID_PROGETTO"
    )

    def __str__(self):  # pragma: no cover
        return self.nome_origine

    class Meta:
        managed = True
        db_table = "PROGETTO_RICERCATORE"


class ProgettoResponsabileScientifico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        to_field="matricola",
        db_column="MATRICOLA",
        blank=True,
        null=True,
    )
    nome_origine = models.CharField(db_column="NOME_ORIGINE", max_length=1000)

    id_progetto = models.ForeignKey(
        ProgettoDatiBase, models.CASCADE, db_column="ID_PROGETTO"
    )

    def __str__(self):  # pragma: no cover
        return self.nome_origine

    class Meta:
        managed = True
        db_table = "PROGETTO_RESPONSABILE_SCIENTIFICO"


class ProgettoTipologiaProgramma(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)

    nome_programma = models.CharField(db_column="NOME_PROGRAMMA", max_length=1000)

    def __str__(self):  # pragma: no cover
        return self.nome_programma

    class Meta:
        managed = True
        db_table = "PROGETTO_TIPOLOGIA_PROGRAMMA"
