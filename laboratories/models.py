from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import validate_file_size, validate_image_file_extension

from .settings import laboratories_media_path

class TipologiaRischio(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_tipologia = models.CharField(db_column="DESCR_TIPOLOGIA", max_length=1000)

    class Meta:
        managed = True
        db_table = "TIPOLOGIA_RISCHIO"

class LaboratorioAltriDipartimenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    id_dip = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="id_dip",
        blank=True,
        null=True,
    )
    descr_dip_lab = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "LABORATORIO_ALTRI_DIPARTIMENTI"


class LaboratorioAttivita(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    id_tipologia_attivita = models.ForeignKey(
        "LaboratorioTipologiaAttivita",
        models.PROTECT,
        db_column="ID_TIPOLOGIA_ATTIVITA",
        null=True,
    )
    descr_finalita_it = models.TextField(
        db_column="DESCR_FINALITA_IT", blank=False, null=True
    )
    descr_finalita_en = models.TextField(
        db_column="DESCR_FINALITA_EN", blank=False, null=True
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_ATTIVITA"


class LaboratorioAttrezzatureRischi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_attrezzature = models.ForeignKey(
        "LaboratorioAttrezzature",
        models.CASCADE,
        db_column="ID_LABORATORIO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    id_tipologia_rischio = models.ForeignKey(
        "TipologiaRischio",
        models.CASCADE,
        db_column="ID_TIPOLOGIA_RISCHIO",
        blank=True,
        null=True,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_ATTREZZATURE_RISCHI"


class LaboratorioFondo(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_fondo = models.CharField(
        db_column="NOME_FONDO", max_length=500, blank=False, null=False
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_FONDO"


class LaboratorioAttrezzatureFondi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_attrezzature = models.ForeignKey(
        "LaboratorioAttrezzature",
        models.CASCADE,
        db_column="ID_LABORATORIO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    id_laboratorio_fondo = models.ForeignKey(
        "LaboratorioFondo",
        models.CASCADE,
        db_column="ID_LABORATORIO_FONDO",
        blank=True,
        null=True,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_ATTREZZATURE_FONDI"


class LaboratorioAttrezzature(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    tipologia = models.CharField(
        db_column="TIPOLOGIA", max_length=500, blank=False, null=True
    )
    descrizione = models.TextField(db_column="DESCRIZIONE", blank=False, null=True)
    costo_unitario = models.FloatField(
        db_column="COSTO_UNITARIO", blank=False, null=True
    )
    quantita = models.IntegerField(db_column="QUANTITA", blank=False, null=True)

    class Meta:
        managed = True
        db_table = "LABORATORIO_ATTREZZATURE"


class LaboratorioInfrastruttura(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)

    def __str__(self):  # pragma: no cover
        return self.descrizione

    class Meta:
        managed = True
        db_table = "LABORATORIO_INFRASTRUTTURA"


class LaboratorioTipologiaAttivita(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)

    class Meta:
        managed = True
        db_table = "LABORATORIO_TIPOLOGIA_ATTIVITA"


class LaboratorioDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    dt_sottomissione = models.DateTimeField(
        db_column="DT_SOTTOMISSIONE", blank=True, null=True
    )
    referente_compilazione = models.CharField(
        db_column="REFERENTE_COMPILAZIONE", max_length=200, blank=True, null=True
    )
    matricola_referente_compilazione = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_REFERENTE_COMPILAZIONE",
        blank=True,
        null=True,
        related_name="matricola_referente_compilazione_personale",
        to_field="matricola",
    )
    email_compilazione = models.CharField(
        db_column="EMAIL_COMPILAZIONE", max_length=200, blank=True, null=True
    )
    nome_laboratorio = models.CharField(
        db_column="NOME_LABORATORIO", max_length=400, blank=False, null=True
    )
    acronimo = models.CharField(
        db_column="ACRONIMO", max_length=100, blank=True, null=True
    )
    logo_laboratorio = models.CharField(
        db_column="LOGO_LABORATORIO", max_length=400, blank=True, null=True
    )
    dipartimento_riferimento = models.CharField(
        db_column="DIPARTIMENTO_RIFERIMENTO", max_length=400, blank=True, null=True
    )
    id_dipartimento_riferimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="ID_DIPARTIMENTO_RIFERIMENTO",
        blank=True,
        null=True,
    )
    laboratorio_interdipartimentale = models.CharField(
        db_column="LABORATORIO_INTERDIPARTIMENTALE",
        max_length=400,
        blank=True,
        null=True,
    )
    altre_strutture_riferimento = models.CharField(
        db_column="ALTRE_STRUTTURE_RIFERIMENTO", max_length=400, blank=True, null=True
    )
    descr_altre_strutture_riferimento_it = models.TextField(
        db_column="DESCR_ALTRE_STRUTTURE_RIFERIMENTO_IT", blank=True, null=True
    )
    descr_altre_strutture_riferimento_en = models.TextField(
        db_column="DESCR_ALTRE_STRUTTURE_RIFERIMENTO_EN", blank=True, null=True
    )
    ambito = models.CharField(db_column="AMBITO", max_length=100, blank=True, null=True)
    finalita_ricerca_it = models.TextField(
        db_column="FINALITA_RICERCA_IT", blank=True, null=True
    )
    finalita_ricerca_en = models.TextField(
        db_column="FINALITA_RICERCA_EN", blank=True, null=True
    )
    finalita_didattica_it = models.TextField(
        db_column="FINALITA_DIDATTICA_IT", blank=True, null=True
    )
    finalita_didattica_en = models.TextField(
        db_column="FINALITA_DIDATTICA_EN", blank=True, null=True
    )
    finalita_servizi_it = models.TextField(
        db_column="FINALITA_SERVIZI_IT", blank=True, null=True
    )
    finalita_servizi_en = models.TextField(
        db_column="FINALITA_SERVIZI_EN", blank=True, null=True
    )
    responsabile_scientifico = models.CharField(
        db_column="RESPONSABILE_SCIENTIFICO", max_length=200, blank=True, null=True
    )
    matricola_responsabile_scientifico = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_RESPONSABILE_SCIENTIFICO",
        blank=True,
        null=True,
        related_name="matricola_responsabile_scientifico_personale",
        to_field="matricola",
    )
    sede_dimensione = models.CharField(
        db_column="SEDE_DIMENSIONE", max_length=100, blank=True, null=True
    )
    sede_note_descrittive = models.TextField(
        db_column="SEDE_NOTE_DESCRITTIVE", blank=True, null=True
    )
    strumentazione_descrizione = models.TextField(
        db_column="STRUMENTAZIONE_DESCRIZIONE",
    )
    strumentazione_valore = models.DecimalField(
        decimal_places=2,
        blank=True,
        null=True,
        max_digits=20,
        db_column="STRUMENTAZIONE_VALORE",
    )
    preposto_sicurezza = models.CharField(
        db_column="PREPOSTO_SICUREZZA", max_length=200, blank=True, null=True
    )
    matricola_preposto_sicurezza = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_PREPOSTO_SICUREZZA",
        blank=True,
        null=True,
        related_name="matricola_preposto_sicurezza_personale",
        to_field="matricola",
    )
    sito_web = models.CharField(
        db_column="SITO_WEB", max_length=1024, blank=True, null=True
    )
    id_infrastruttura_riferimento = models.ForeignKey(
        "LaboratorioInfrastruttura",
        models.SET_NULL,
        db_column="ID_INFRASTRUTTURA_RIFERIMENTO",
        blank=True,
        null=True,
    )
    nome_file_logo = models.FileField(
        upload_to=laboratories_media_path,
        validators=[validate_image_file_extension, validate_file_size],
        db_column="NOME_FILE_LOGO",
        max_length=1000,
        blank=True,
        null=True,
    )
    visibile = models.BooleanField(db_column="VISIBILE", default=False)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )
    tipologia_attivita = models.ManyToManyField(
        LaboratorioTipologiaAttivita, through="LaboratorioAttivita"
    )
    tipologia_rischio = models.ManyToManyField(
        TipologiaRischio, through="LaboratorioTipologiaRischio"
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_DATI_BASE"


class LaboratorioDatiErc1(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    id_ricerca_erc1 = models.ForeignKey(
        "research_lines.RicercaErc1",
        models.PROTECT,
        db_column="ID_RICERCA_ERC1",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_DATI_ERC1"


class LaboratorioPersonaleRicerca(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale_ricerca = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_PERSONALE_RICERCA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    cognomenome_origine = models.CharField(
        db_column="COGNOMENOME_ORIGINE", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_PERSONALE_RICERCA"


class LaboratorioPersonaleTecnico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale_tecnico = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_PERSONALE_TECNICO",
        blank=True,
        null=True,
        to_field="matricola",
    )
    ruolo = models.CharField(db_column="RUOLO", max_length=400, blank=True, null=True)
    percentuale_impegno = models.FloatField(
        db_column="PERCENTUALE_IMPEGNO", blank=True, null=True
    )
    cognomenome_origine = models.CharField(
        db_column="COGNOMENOME_ORIGINE", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_PERSONALE_TECNICO"


class LaboratorioServiziErogati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    descrizione = models.TextField(db_column="DESCRIZIONE", blank=False, null=True)
    matricola_responsabile = models.CharField(
        db_column="MATRICOLA_RESPONSABILE", max_length=20, blank=True, null=True
    )
    responsabile_origine = models.CharField(
        db_column="RESPONSABILE_ORIGINE", max_length=500, blank=True, null=True
    )
    committenti = models.CharField(
        db_column="COMMITTENTI", max_length=500, blank=False, null=True
    )
    anno = models.IntegerField(db_column="ANNO", blank=False, null=True)
    durata_mesi = models.IntegerField(db_column="DURATA_MESI", blank=False, null=True)
    importo_euro = models.FloatField(db_column="IMPORTO_EURO", blank=False, null=True)
    strumentazione = models.TextField(
        db_column="STRUMENTAZIONE", blank=False, null=True
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_SERVIZI_EROGATI"


class LaboratorioServiziOfferti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    nome_servizio = models.TextField(db_column="NOME_SERVIZIO", blank=False, null=True)
    descrizione_servizio = models.TextField(
        db_column="DESCRIZIONE_SERVIZIO", blank=False, null=True
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_SERVIZI_OFFERTI"


class LaboratorioTipologiaRischio(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    tipologia_rischio_origine = models.CharField(
        db_column="TIPOLOGIA_RISCHIO_ORIGINE", max_length=500, blank=True, null=True
    )
    id_tipologia_rischio = models.ForeignKey(
        TipologiaRischio,
        models.CASCADE,
        db_column="ID_TIPOLOGIA_RISCHIO",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "LABORATORIO_TIPOLOGIA_RISCHIO"


class LaboratorioUbicazione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    edificio = models.CharField(
        db_column="EDIFICIO", max_length=200, blank=False, null=True
    )
    piano = models.CharField(db_column="PIANO", max_length=100, blank=False, null=True)
    sede_principale = models.CharField(
        db_column="SEDE_PRINCIPALE", max_length=10, blank=False, null=True
    )
    note = models.TextField(db_column="NOTE", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "LABORATORIO_UBICAZIONE"

