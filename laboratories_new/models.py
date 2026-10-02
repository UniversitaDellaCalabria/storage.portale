from django.contrib.auth import get_user_model
from django.db import models
from generics.validators import validate_file_size, validate_image_file_extension

from .settings import laboratories_media_path

class LaboratorioInfrastruttura(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    nome = models.CharField(db_column="NOME", max_length=100, blank=True, null=True)
    descrizione_it = models.TextField(
        db_column="DESCRIZIONE_IT", blank=False, null=False
    )
    descrizione_en = models.TextField(db_column="DESCRIZIONE_EN", blank=True, null=True)
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
    descrizione_it = models.TextField(
        db_column="DESCRIZIONE_IT", blank=False, null=False
    )
    descrizione_en = models.TextField(db_column="DESCRIZIONE_EN", blank=True, null=True)
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


class AmbitiS3(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    codice = models.CharField(db_column="CODICE", max_length=100, blank=True, null=True)
    denominazione_it = models.CharField(
        db_column="DENOMINAZIONE_IT", max_length=500, blank=True, null=True
    )
    denominazione_en = models.CharField(
        db_column="DENOMINAZIONE_EN", max_length=500, blank=True, null=True
    )
    descrizione_it = models.TextField(db_column="DESCRIZIONE_IT", blank=True, null=True)
    descrizione_en = models.TextField(db_column="DESCRIZIONE_EN", blank=True, null=True)
    attivo = models.BooleanField(db_column="ATTIVO", default=True)

    class Meta:
        managed = False
        db_table = "AMBITI"


class TraiettorieS3(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    ambito = models.ForeignKey(
        "AmbitiS3",
        models.CASCADE,
        db_column="ID_AMBITO",
        blank=True,
        null=True,
    )
    numero = models.IntegerField(db_column="NUMERO", blank=True, null=True)
    codice = models.CharField(db_column="CODICE", max_length=100, blank=True, null=True)
    denominazione_it = models.CharField(
        db_column="DENOMINAZIONE_IT", max_length=500, blank=True, null=True
    )
    denominazione_en = models.CharField(
        db_column="DENOMINAZIONE_EN", max_length=500, blank=True, null=True
    )
    attiva = models.BooleanField(db_column="ATTIVA", default=True)

    class Meta:
        managed = False
        db_table = "TRAIETTORIE"


class LaboratorioDatiBase(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
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
        "AmbitiS3",
        models.SET_NULL,
        db_column="ID_AMBITO_S3_PREVALENTE",
        blank=True,
        null=True,
    )
    tipologia = models.CharField(
        db_column="TIPOLOGIA", max_length=100, blank=True, null=True
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
        db_column="id_user_mod",
        blank=True,
        null=True,
        related_name="laboratories_new_datibase_set",
    )
    # tipologia_attivita = models.ManyToManyField(
    #     LaboratorioTipologiaAttivita, through="LaboratorioAttivita"
    # )

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
        related_name="laboratories_new_erc1",
    )
    dt_mod = models.DateField(db_column="DT_MOD", blank=True, null=True)
    id_user_mod = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        db_column="id_user_mod",
        blank=True,
        null=True,
        related_name="laboratories_new_datierc1_set",
    )

    class Meta:
        managed = False
        db_table = "LABORATORIO_DATI_ERC1"


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
    superficie_mq = models.IntegerField(
        db_column="SUPERFICIE_MQ", blank=True, null=True
    )
    sede_principale = models.CharField(
        db_column="SEDE_PRINCIPALE", max_length=10, blank=False, null=True
    )
    note = models.TextField(db_column="NOTE", blank=True, null=True)
    path_file_planimetria = models.CharField(
        db_column="PATH_FILE_PLANIMETRIA", max_length=1000, blank=True, null=True
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
        db_table = "LABORATORIO_UBICAZIONE"


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
    principale = models.BooleanField(db_column="PRINCIPALE", blank=True, null=True)
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
    ente_provenienza = models.CharField(
        db_column="ENTE_PROVENIENZA", max_length=500, blank=True, null=True
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
