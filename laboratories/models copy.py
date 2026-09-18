from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import validate_file_size, validate_image_file_extension

from .settings import laboratories_media_path


class TipologiaRischio(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_rischio_it = models.CharField(
            db_column="TIPO_RISCHIO_IT", max_length=500, blank=True, null=True
        )
    tipo_rischio_en = models.CharField(
        db_column="TIPO_RISCHIO_EN", max_length=500, blank=True, null=True
    )
    descrizione_it = models.TextField(
        db_column="DESCRIZIONE_IT", blank=True, null=True
    )
    descrizione_en = models.TextField(
        db_column="DESCRIZIONE_EN", blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
            get_user_model(),
            on_delete=models.SET_NULL,
            db_column="user_mod_id",
            blank=True,
            null=True,
        )
    class Meta:
        managed = False
        db_table = "TIPOLOGIA_RISCHIO"

#TO DO
class LaboratorioAltriDipartimenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    didattica_dipartimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="ID_DIDATTICA_DIPARTIMENTO",
        blank=True,
        null=True,
    )
    descr_dip_lab = models.CharField(max_length=400, db_column="DESCR_DIP_LAB", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "LABORATORIO_ALTRI_DIPARTIMENTI"


class LaboratorioAttivita(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    tipologia_attivita = models.ForeignKey(
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
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ATTIVITA"


class LaboratorioAttrezzatureRischi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_attrezzature = models.ForeignKey(
        "LaboratorioAttrezzature",
        models.CASCADE,
        db_column="ID_LABORATORIO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    tipologia_rischio = models.ForeignKey(
        "LaboratorioTipoRischio",
        models.CASCADE,
        db_column="ID_TIPO_RISCHIO",
        blank=False,
        null=False,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ATTREZZATURE_RISCHI"


class LaboratorioFondo(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_fondo = models.CharField(
        db_column="NOME_FONDO", max_length=500, blank=False, null=False
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_FONDO"

#TO_DO
class LaboratorioAttrezzatureFondi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_attrezzature = models.ForeignKey(
        "LaboratorioAttrezzature",
        models.CASCADE,
        db_column="ID_LABORATORIO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    laboratorio_fondo = models.ForeignKey(
        "LaboratorioFondo",
        models.CASCADE,
        db_column="ID_LABORATORIO_FONDO",
        blank=True,
        null=True,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ATTREZZATURE_FONDI"


class LaboratorioAttrezzature(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    laboratorio_catalogo_attrezzature = models.ForeignKey(
        "LaboratorioCatalogoAttrezzature",
        models.DO_NOTHING,
        db_column="ID_LABORATORIO_CATALOGO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    # tipologia = models.CharField(
    #     db_column="TIPOLOGIA", max_length=500, blank=False, null=True
    # )
    # descrizione = models.TextField(db_column="DESCRIZIONE", blank=False, null=True)
    # costo_unitario = models.FloatField(
    #     db_column="COSTO_UNITARIO", blank=False, null=True
    # )
    # quantita = models.IntegerField(db_column="QUANTITA", blank=False, null=True)

    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    note = models.TextField(db_column="NOTE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ATTREZZATURE"


class LaboratorioInfrastruttura(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    # descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)
    nome = models.CharField(
        db_column="NOME", max_length=100, blank=True, null=True
    )
    descrizione_it = models.TextField(db_column="DESCRIZIONE_IT", blank=False, null=False)
    descrizione_en = models.TextField(
        db_column="DESCRIZIONE_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    def __str__(self):  # pragma: no cover
        return self.descrizione_it

    class Meta:
        managed = False
        db_table = "LABORATORIO_INFRASTRUTTURA"


class LaboratorioTipologiaAttivita(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    # descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)

    descrizione_it = models.TextField(db_column="DESCRIZIONE_IT", blank=False, null=False)
    descrizione_en = models.TextField(
        db_column="DESCRIZIONE_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_TIPO_ATTIVITA"


class LaboratorioDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    # dt_sottomissione = models.DateTimeField(
    #     db_column="DT_SOTTOMISSIONE", blank=True, null=True
    # )
    # referente_compilazione = models.CharField(
    #     db_column="REFERENTE_COMPILAZIONE", max_length=200, blank=True, null=True
    # )
    # matricola_referente_compilazione = models.ForeignKey(
    #     "addressbook.Personale",
    #     models.SET_NULL,
    #     db_column="ID_PERSONALE_MATRICOLA_REFERENTE_COMPILAZIONE",
    #     blank=True,
    #     null=True,
    #     related_name="matricola_referente_compilazione_personale",
    #     to_field="matricola",
    # )
    # email_compilazione = models.CharField(
    #     db_column="EMAIL_COMPILAZIONE", max_length=200, blank=True, null=True
    # )
    ubicazione = models.TextField(db_column="UBICAZIONE", blank=True, null=True)
    descrizione = models.TextField(db_column="DESCRIZIONE", blank=True, null=True)
    nome_laboratorio = models.CharField(
        db_column="NOME_LABORATORIO", max_length=400, blank=False, null=True
    )
    acronimo = models.CharField(
        db_column="ACRONIMO", max_length=100, blank=True, null=True
    )
    logo_laboratorio = models.CharField(
        db_column="LOGO_LABORATORIO", max_length=400, blank=True, null=True
    )
    # dipartimento_riferimento_nome = models.CharField(
    #     db_column="DIPARTIMENTO_RIFERIMENTO", max_length=400, blank=True, null=True
    # )
    # dipartimento_riferimento = models.ForeignKey(
    #     "structures.DidatticaDipartimento",
    #     models.DO_NOTHING,
    #     db_column="ID_DIPARTIMENTO_RIFERIMENTO",
    #     blank=True,
    #     null=True,
    # )
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
    ambito_s3_prevalente = models.ForeignKey(
        "AmbitiS3", # CONTROLLARE!
        models.SET_NULL,
        db_column="ID_AMBITO_S3_PREVALENTE",
        blank=True,
        null=True,
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
    # responsabile_scientifico = models.CharField(
    #     db_column="RESPONSABILE_SCIENTIFICO", max_length=200, blank=True, null=True
    # )
    # matricola_responsabile_scientifico = models.ForeignKey(
    #     "addressbook.Personale",
    #     models.SET_NULL,
    #     db_column="ID_PERSONALE_MATRICOLA_RESPONSABILE_SCIENTIFICO",
    #     blank=True,
    #     null=True,
    #     related_name="matricola_responsabile_scientifico_personale",
    #     to_field="matricola",
    # )
    # sede_dimensione = models.CharField(
    #     db_column="SEDE_DIMENSIONE", max_length=100, blank=True, null=True
    # )
    # sede_note_descrittive = models.TextField(
    #     db_column="SEDE_NOTE_DESCRITTIVE", blank=True, null=True
    # )
    # strumentazione_descrizione = models.TextField(
    #     db_column="STRUMENTAZIONE_DESCRIZIONE",
    # )
    # strumentazione_valore = models.DecimalField(
    #     decimal_places=2,
    #     blank=True,
    #     null=True,
    #     max_digits=20,
    #     db_column="STRUMENTAZIONE_VALORE",
    # )
    # preposto_sicurezza = models.CharField(
    #     db_column="PREPOSTO_SICUREZZA", max_length=200, blank=True, null=True
    # )
    # matricola_preposto_sicurezza = models.ForeignKey(
    #     "addressbook.Personale",
    #     models.SET_NULL,
    #     db_column="ID_PERSONALE_MATRICOLA_PREPOSTO_SICUREZZA",
    #     blank=True,
    #     null=True,
    #     related_name="matricola_preposto_sicurezza_personale",
    #     to_field="matricola",
    # )
    sito_web = models.CharField(
        db_column="SITO_WEB", max_length=1024, blank=True, null=True
    )
    infrastruttura_riferimento = models.ForeignKey(
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
    user_mod = models.ForeignKey(
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
        managed = False
        db_table = "LABORATORIO_DATI_BASE"


class LaboratorioDatiErc1(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    ricerca_erc1 = models.ForeignKey(
        "research_lines.RicercaErc1",
        models.PROTECT,
        db_column="ID_RICERCA_ERC1",
        blank=True,
        null=True,
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_DATI_ERC1"

#TO_DO
class LaboratorioPersonaleRicerca(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale_ricerca = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    cognomenome_origine = models.CharField(
        db_column="COGNOMENOME_ORIGINE", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_PERSONALE_RICERCA"

#TO_DO
class LaboratorioPersonaleTecnico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale_tecnico = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA",
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
        managed = False
        db_table = "LABORATORIO_PERSONALE_TECNICO"


class LaboratorioServiziErogati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
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
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_SERVIZI_EROGATI"

#TO_DO
class LaboratorioServiziOfferti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
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
        managed = False
        db_table = "LABORATORIO_SERVIZI_OFFERTI"

#TO_DO
class LaboratorioTipologiaRischio(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    tipologia_rischio_origine = models.CharField(
        db_column="TIPOLOGIA_RISCHIO_ORIGINE", max_length=500, blank=True, null=True
    )
    tipologia_rischio = models.ForeignKey(
        TipologiaRischio,
        models.CASCADE,
        db_column="ID_TIPOLOGIA_RISCHIO",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_TIPOLOGIA_RISCHIO"


class LaboratorioUbicazione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
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
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_UBICAZIONE"


#NUOVE
class LaboratorioTipoManutenzione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo = models.CharField(
        db_column="TIPO", max_length=100, blank=True, null=True
    )
    descrizione_it = models.TextField(
        db_column="DESCRIZIONE_IT", blank=True, null=True
    )
    descrizione_en = models.TextField(
        db_column="DESCRIZIONE_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_TIPO_MANUTENZIONE"

class LaboratorioTipoAccreditamento(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo = models.CharField(
        db_column="TIPO", max_length=100, blank=True, null=True
    )
    ente = models.CharField(
        db_column="ENTE", max_length=1000, blank=True, null=True
    )
    descrizione_it = models.TextField(
        db_column="DESCRIZIONE_IT", blank=True, null=True
    )
    descrizione_en = models.TextField(
        db_column="DESCRIZIONE_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_TIPO_ACCREDITAMENTO"

class LaboratorioServiziAccreditamento(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_tipo_accreditamento = models.ForeignKey(
        "LaboratorioTipoAccreditamento",
        models.CASCADE,
        db_column="ID_LABORATORIO_TIPO_ACCREDITAMENTO",
        blank=True,
        null=True,
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_scadenza = models.DateField(db_column="DATA_SCADENZA", blank=True, null=True)
    laboratorio_servizi = models.ForeignKey(
        "LaboratorioServizi",
        models.CASCADE,
        db_column="ID_LABORATORIO_SERVIZI",
        blank=True,
        null=True,
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_SERVIZI_ACCREDITAMENTO"


class LaboratorioServizi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI_BASE",
        blank=True,
        null=True,
    )
    traiettoria_s3 = models.ForeignKey(
        "TraiettorieS3",
        models.CASCADE,
        db_column="ID_TRAIETTORIA_S3",
        blank=True,
        null=True,
    )
    laboratorio_anagrafica_servizi = models.ForeignKey(
        "LaboratorioAnagraficaServizi",
        models.CASCADE,
        db_column="ID_LABORATORIO_ANAGRAFICA_SERVIZI",
        blank=True,
        null=True,
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    costo_interni = models.DecimalField(
        db_column="COSTO_INTERNI",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    costo_esterni = models.DecimalField(
        db_column="COSTO_ESTERNI",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    descrizione_it = models.TextField(db_column="DESCRIZIONE_IT", blank=True, null=True)
    descrizione_en = models.TextField(db_column="DESCRIZIONE_EN", blank=True, null=True)
    parole_chiavi = models.TextField(db_column="PAROLE_CHIAVI", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_SERVIZI"

class LaboratorioRuolo(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_ruolo_it = models.CharField(
        db_column="DESCR_RUOLO_IT", max_length=2000, blank=True, null=True
    )
    descr_ruolo_en = models.CharField(
        db_column="DESCR_RUOLO_EN", max_length=2000, blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_RUOLO"

class LaboratorioResponsabile(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    laboratorio_ruolo = models.ForeignKey(
        "LaboratorioRuolo",
        models.CASCADE,
        db_column="ID_LABORATORIO_RUOLO",
        blank=True,
        null=True,
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_RESPONSABILE"

class LaboratorioDipartimenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    didattica_dipartimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.CASCADE,
        db_column="ID_DIDATTICA_DIPARTIMENTO",
        blank=True,
        null=True,
    )
    descr_dip_lab = models.CharField(
        db_column="DESCR_DIP_LAB", max_length=400, blank=True, null=True
    )
    principale = models.BooleanField(
        db_column="PRINCIPALE", blank=True, null=True
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_DIPARTIMENTI"

class LaboratorioComitatoGestione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_COMITATO_GESTIONE"

class LaboratorioCatalogoAttrezzature(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descrizione_it = models.TextField(db_column="DESCRIZIONE_IT", blank=True, null=True)
    descrizione_en = models.TextField(db_column="DESCRIZIONE_EN", blank=True, null=True)
    marca = models.CharField(
        db_column="MARCA", max_length=200, blank=True, null=True
    )
    modello = models.CharField(
        db_column="MODELLO", max_length=200, blank=True, null=True
    )
    serial_number = models.CharField(
        db_column="SERIAL_NUMBER", max_length=200, blank=True, null=True
    )
    anno_acquisizione = models.PositiveIntegerField(
        db_column="ANNO_ACQUISIZIONE", blank=True, null=True
    )
    numero_inventario = models.IntegerField(
        db_column="NUMERO_INVENTARIO", unique=True, blank=False, null=False
    )
    laboratorio_fondo = models.ForeignKey(
        "LaboratorioFondo",
        models.CASCADE,
        db_column="ID_LABORATORIO_FONDO",
        blank=True,
        null=True,
    )
    localizzazione_in_lab = models.CharField(
        db_column="LOCALIZZAZIONE_IN_LAB", max_length=200, blank=True, null=True
    )
    flag_presidio_sicurezza = models.BooleanField(
        db_column="FLAG_PRESIDIO_SICUREZZA", blank=True, null=True
    )
    valore = models.DecimalField(
        db_column="VALORE",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_CATALOGO_ATTREZZATURE"

class LaboratorioAttrezzatureManutenzioni(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_catalogo_attrezzature = models.ForeignKey(
        "LaboratorioCatalogoAttrezzature",
        models.DO_NOTHING,
        db_column="ID_LABORATORIO_CATALOGO_ATTREZZATURE",
        blank=True,
        null=True,
    )
    laboratorio_tipo_manutenzione = models.ForeignKey(
        "LaboratorioTipoManutenzione",
        models.CASCADE,
        db_column="ID_LABORATORIO_TIPO_MANUTENZIONE",
        blank=True,
        null=True,
    )
    data_prevista = models.DateField(db_column="DATA_PREVISTA", blank=True, null=True)
    data_effettiva = models.DateField(db_column="DATA_EFFETTIVA", blank=True, null=True)
    descrizione = models.TextField(db_column="DESCRIZIONE", blank=True, null=True)
    ente = models.CharField(
        db_column="ENTE", max_length=1000, blank=True, null=True
    )
    doc_certificazione = models.CharField(
        db_column="DOC_CERTIFICAZIONE", max_length=1000, blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ATTREZZATURE_MANUTENZIONI"

class LaboratorioAnagraficaServizi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_servizio_it = models.TextField(
        db_column="NOME_SERVIZIO_IT", blank=True, null=True
    )
    nome_servizio_en = models.TextField(
        db_column="NOME_SERVIZIO_EN", blank=True, null=True
    )
    descrizione_servizio_it = models.TextField(
        db_column="DESCRIZIONE_SERVIZIO_IT", blank=True, null=True
    )
    descrizione_servizio_en = models.TextField(
        db_column="DESCRIZIONE_SERVIZIO_EN", blank=True, null=True
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_ANAGRAFICA_SERVIZI"

class LaboratorioAffiliati(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    laboratorio_dati_base = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column="ID_LABORATORIO_DATI",
        blank=True,
        null=True,
    )
    matricola_personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_cognome = models.CharField(
        db_column="NOME_COGNOME", max_length=200, blank=True, null=True
    )
    laboratorio_ruolo = models.ForeignKey(
        "LaboratorioRuolo",
        models.CASCADE,
        db_column="ID_LABORATORIO_RUOLO",
        blank=True,
        null=True,
    )
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_AFFILIATI"