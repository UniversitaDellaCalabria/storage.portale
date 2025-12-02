from django.db import models
from generics.models import Permissions
from advanced_training.settings import (
    OFFICE_ADVANCED_TRAINING,
)


class AltaFormazioneConsiglioScientificoEsterno(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_cons = models.CharField(db_column="NOME_CONS", max_length=1000)
    ruolo_cons = models.CharField(
        db_column="RUOLO_CONS", max_length=1000, blank=True, null=True
    )
    ente_cons = models.CharField(
        db_column="ENTE_CONS", max_length=1000, blank=True, null=True
    )
    alta_formazione_dati_base = models.ForeignKey(
        "AltaFormazioneDatiBase",
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_DATI_BASE",
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_ESTERNO"


class AltaFormazioneConsiglioScientificoInterno(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola_cons = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="ID_PERSONALE_MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_origine_cons = models.CharField(db_column="NOME_ORIGINE_CONS", max_length=1000)
    alta_formazione_dati_base = models.ForeignKey(
        "AltaFormazioneDatiBase",
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_DATI_BASE",
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_INTERNO"


class AltaFormazioneDatiBase(Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    titolo_it = models.CharField(
        db_column="TITOLO_IT", max_length=512, blank=True, null=True
    )
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=512, blank=True, null=True
    )
    anno_rilevazione = models.IntegerField(
        db_column="ANNO_RILEVAZIONE", blank=True, null=True
    )
    dipartimento_riferimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="ID_DIPARTIMENTO_RIFERIMENTO",
        blank=True,
        null=True,
    )
    alta_formazione_tipo_corso = models.ForeignKey(
        "AltaFormazioneTipoCorso",
        models.SET_NULL,
        db_column="ID_ALTA_FORMAZIONE_TIPO_CORSO",
        blank=True,
        null=True,
    )
    lingua = models.CharField(db_column="LINGUA", max_length=512, blank=True, null=True)
    alta_formazione_mod_erogazione = models.ForeignKey(
        "AltaFormazioneModalitaErogazione",
        models.DO_NOTHING,
        db_column="ID_ALTA_FORMAZIONE_MOD_EROGAZIONE",
        blank=True,
        null=True,
    )
    ore = models.IntegerField(blank=True, null=True, db_column="ORE")
    mesi = models.IntegerField(blank=True, null=True, db_column="MESI")
    data_inizio = models.DateField(db_column="DATA_INIZIO", blank=True, null=True)
    data_fine = models.DateField(db_column="DATA_FINE", blank=True, null=True)
    sede_corso = models.CharField(
        db_column="SEDE_CORSO", max_length=2000, blank=True, null=True
    )
    num_min_partecipanti = models.IntegerField(
        db_column="NUM_MIN_PARTECIPANTI", blank=True, null=True
    )
    num_max_partecipanti = models.IntegerField(
        db_column="NUM_MAX_PARTECIPANTI", blank=True, null=True
    )
    uditori_ammessi = models.CharField(
        db_column="UDITORI_AMMESSI", max_length=200, blank=True, null=True
    )
    num_max_uditori = models.IntegerField(
        db_column="NUM_MAX_UDITORI", blank=True, null=True
    )
    requisiti_ammissione = models.TextField(
        db_column="REQUISITI_AMMISSIONE", blank=True, null=True
    )
    titolo_rilasciato = models.TextField(
        db_column="TITOLO_RILASCIATO", blank=True, null=True
    )
    doppio_titolo = models.TextField(db_column="DOPPIO_TITOLO", blank=True, null=True)
    matricola_direttore_scientifico = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        to_field="matricola",
        db_column="ID_PERSONALE_MATRICOLA_DIRETTORE_SCIENTIFICO",
        blank=True,
        null=True,
        related_name="direttore_scientifico",  # AGGIUNTO per evitare conflitti
    )
    nome_origine_direttore_scientifico = models.TextField(
        db_column="NOME_ORIGINE_DIRETTORE_SCIENTIFICO", blank=True, null=True
    )
    quota_iscrizione = models.FloatField(
        db_column="QUOTA_ISCRIZIONE", blank=True, null=True
    )
    quota_uditori = models.FloatField(db_column="QUOTA_UDITORI", blank=True, null=True)
    funzione_lavoro = models.TextField(
        db_column="FUNZIONE_LAVORO", blank=True, null=True
    )
    obiettivi_formativi_summer_school = models.TextField(
        db_column="OBIETTIVI_FORMATIVI_SUMMER_SCHOOL", blank=True, null=True
    )
    competenze = models.TextField(db_column="COMPETENZE", blank=True, null=True)
    sbocchi_occupazionali = models.TextField(
        db_column="SBOCCHI_OCCUPAZIONALI", blank=True, null=True
    )
    obiettivi_formativi_corso = models.TextField(
        db_column="OBIETTIVI_FORMATIVI_CORSO", blank=True, null=True
    )
    modalita_svolgimento_prova_finale = models.TextField(
        db_column="MODALITA_SVOLGIMENTO_PROVA_FINALE", blank=True, null=True
    )
    numero_moduli = models.FloatField(db_column="NUMERO_MODULI", blank=True, null=True)
    stage_tirocinio = models.TextField(
        db_column="STAGE_TIROCINIO", blank=True, null=True
    )
    ore_stage_tirocinio = models.IntegerField(
        db_column="ORE_STAGE_TIROCINIO", blank=True, null=True
    )
    cfu_stage = models.IntegerField(db_column="CFU_STAGE", blank=True, null=True)
    mesi_stage = models.IntegerField(db_column="MESI_STAGE", blank=True, null=True)
    tipo_aziende_enti_tirocinio = models.TextField(
        db_column="TIPO_AZIENDE_ENTI_TIROCINIO", blank=True, null=True
    )
    project_work = models.TextField(db_column="PROJECT_WORK", blank=True, null=True)
    contenuti_tempi_criteri_cfu = models.TextField(
        db_column="CONTENUTI_TEMPI_CRITERI_CFU", blank=True, null=True
    )
    path_piano_finanziario = models.CharField(
        db_column="PATH_PIANO_FINANZIARIO", max_length=500, blank=True, null=True
    )
    path_doc_delibera = models.CharField(
        db_column="PATH_DOC_DELIBERA", max_length=500, blank=True, null=True
    )
    matricola_proponente = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        to_field="matricola",
        db_column="MATRICOLA_PROPONENTE",
        blank=True,
        null=True,
        related_name="proponente",
    )
    cognome_proponente = models.CharField(
        db_column="COGNOME_PROPONENTE", max_length=200, blank=True, null=True
    )
    nome_proponente = models.CharField(
        db_column="NOME_PROPONENTE", max_length=200, blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_ADVANCED_TRAINING,)

    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()

        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return (
                user_office.office.organizational_structure.unique_code
                == self.dipartimento_riferimento.dip_cod
            )
        return True

    def get_current_status(self):
        return (
            self.altaformazionestatusstorico_set.filter(id_alta_formazione_dati_base=self.id)
            .order_by("-data_status", "-dt_mod", "-id")
            .first()
        )

    
    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()
        
        dati_base_status = self.get_current_status()

        if dati_base_status is None:
            return False
            
        status_cod = dati_base_status.id_alta_formazione_status.status_cod
        
        if status_cod == "0" and offices_names[0] in user_offices_names:
            return True
        elif status_cod == "1" and offices_names[1] in user_offices_names:
            return True
        elif status_cod == "2" and offices_names[2] in user_offices_names:
            return True
        # ecc... ????
        
        return False
    
    def _check_lock_permission(self, user_offices_names, **kwargs):
        return self._check_edit_permission(user_offices_names, **kwargs)
    

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_DATI_BASE"
        unique_together = (("titolo_it", "data_inizio"),)


class AltaFormazioneAttivitaFormative(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase,
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_DATI_BASE",
    )
    nome = models.CharField(db_column="NOME", max_length=500, blank=True, null=True)
    programma = models.TextField(db_column="PROGRAMMA", blank=True, null=True)
    bibliografia = models.TextField(db_column="BIBLIOGRAFIA", blank=True, null=True)
    modalita_verifica_finale = models.TextField(
        db_column="MODALITA_VERIFICA_FINALE", blank=True, null=True
    )
    alta_formazione_attivita_formativa_padre = models.ForeignKey(
        "self",
        models.SET_NULL,
        db_column="ID_ALTA_FORMAZIONE_ATTIVITA_FORMATIVA_PADRE",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_ATTIVITA_FORMATIVE"


class AltaFormazioneAttivitaFormativeDocenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    alta_formazione_attivita_formative = models.ForeignKey(
        AltaFormazioneAttivitaFormative,
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_ATTIVITA_FORMATIVE",
    )
    matricola_docente = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_DOCENTE",
        blank=True,
        null=True,
        to_field="matricola",
    )
    nome_docente = models.CharField(
        db_column="NOME_DOCENTE", max_length=200, blank=True, null=True
    )
    cognome_docente = models.CharField(
        db_column="COGNOME_DOCENTE", max_length=200, blank=True, null=True
    )
    tipologia_docente = models.ForeignKey(
        "AltaFormazioneTipologiaDocente",
        models.SET_NULL,
        db_column="ID_TIPOLOGIA_DOCENTE",
        blank=True,
        null=True,
    )
    durata_in_ore = models.IntegerField(
        db_column="DURATA_IN_ORE", blank=True, null=True
    )
    ssd = models.CharField(db_column="SSD", max_length=100, blank=True, null=True)
    cfu = models.IntegerField(db_column="CFU", blank=True, null=True)
    argomento = models.TextField(db_column="ARGOMENTO", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_ATTIVITA_FORMATIVE_DOCENTI"


class AltaFormazioneIncaricoDidattico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    alta_formazione_piano_didattico = models.ForeignKey(
        "AltaFormazionePianoDidattico",
        models.SET_NULL,
        db_column="ID_ALTA_FORMAZIONE_PIANO_DIDATTICO",
        blank=True,
        null=True,
    )
    alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    modulo = models.TextField(db_column="MODULO", blank=True, null=True)
    num_ore = models.CharField(db_column="NUM_ORE", max_length=5, blank=True, null=True)
    docente = models.CharField(
        db_column="DOCENTE", max_length=2000, blank=True, null=True
    )
    qualifica = models.CharField(
        db_column="QUALIFICA", max_length=2000, blank=True, null=True
    )
    ente = models.TextField(db_column="ENTE", blank=True, null=True)
    tipologia = models.CharField(
        db_column="TIPOLOGIA", max_length=1000, blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_INCARICO_DIDATTICO"


class AltaFormazioneModalitaErogazione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_MODALITA_EROGAZIONE"

    def __str__(self):
        return self.descrizione


class AltaFormazioneModalitaSelezione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_selezione = models.CharField(db_column="TIPO_SELEZIONE", max_length=100)
    alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_MODALITA_SELEZIONE"


class AltaFormazionePartner(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    denominazione = models.CharField(db_column="DENOMINAZIONE", max_length=1000)
    tipologia = models.CharField(
        db_column="TIPOLOGIA", max_length=1000, blank=True, null=True
    )
    sito_web = models.CharField(
        db_column="SITO_WEB", max_length=2000, blank=True, null=True
    )
    alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_PARTNER"


class AltaFormazionePianoDidattico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    modulo = models.TextField(db_column="MODULO")
    ssd = models.CharField(db_column="SSD", max_length=500, blank=True, null=True)
    num_ore = models.IntegerField(db_column="NUM_ORE", blank=True, null=True)
    cfu = models.IntegerField(db_column="CFU", blank=True, null=True)
    verifica_finale = models.IntegerField(
        db_column="VERIFICA_FINALE", blank=True, null=True
    )
    alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_PIANO_DIDATTICO"


class AltaFormazioneTipologiaDocente(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=500)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_TIPOLOGIA_DOCENTE"

    def __str__(self):
        return self.descrizione


class AltaFormazioneTipoCorso(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_corso_descr = models.CharField(db_column="TIPO_CORSO_DESCR", max_length=256)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)  # AGGIUNTO

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_TIPO_CORSO"

    def __str__(self):
        return self.tipo_corso_descr


class AltaFormazioneFinestraTemporale(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    titolo = models.CharField(db_column="TITOLO", max_length=256)
    data_inizio = models.DateField(db_column="DATA_INIZIO")
    data_fine = models.DateField(db_column="DATA_FINE")
    anno_accademico = models.CharField(db_column="ANNO_ACCADEMICO", max_length=9)
    note = models.TextField(db_column="NOTE", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_FINESTRA_TEMPORALE"

    def __str__(self):
        return self.titolo


class AltaFormazioneStatus(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    status_cod = models.CharField(db_column="STATUS_COD", max_length=50)
    status_desc = models.CharField(db_column="STATUS_DESC", max_length=256)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_STATUS"

    def __str__(self):
        return self.status_desc


class AltaFormazioneStatusStorico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    motivazione = models.TextField(db_column="MOTIVAZIONE", blank=True, null=True)
    data_status = models.DateField(db_column="DATA_STATUS", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.IntegerField(blank=True, null=True)
    id_alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    id_alta_formazione_status = models.ForeignKey(
        AltaFormazioneStatus, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_STATUS"
    )

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_STATUS_STORICO"

    def __str__(self):
        return self.status_desc
