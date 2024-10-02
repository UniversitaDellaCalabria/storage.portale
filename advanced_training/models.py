from django.db import models


class AltaFormazioneConsiglioScientificoEsterno(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_cons = models.CharField(db_column="NOME_CONS", max_length=1000)
    ruolo_cons = models.CharField(
        db_column="RUOLO_CONS", max_length=1000, blank=True, null=True
    )
    ente_cons = models.CharField(
        db_column="ENTE_CONS", max_length=1000, blank=True, null=True
    )
    id_alta_formazione_dati_base = models.ForeignKey(
        "AltaFormazioneDatiBase",
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_DATI_BASE",
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_ESTERNO"


class AltaFormazioneConsiglioScientificoInterno(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    matricola_cons = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA_CONS",
        blank=True,
        null=True,
    )
    nome_origine_cons = models.CharField(db_column="NOME_ORIGINE_CONS", max_length=1000)
    id_alta_formazione_dati_base = models.ForeignKey(
        "AltaFormazioneDatiBase",
        models.CASCADE,
        db_column="ID_ALTA_FORMAZIONE_DATI_BASE",
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_INTERNO"


class AltaFormazioneDatiBase(models.Model):
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
    id_dipartiento_riferimento = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="ID_DIPARTIENTO_RIFERIMENTO",
        blank=True,
        null=True,
    )
    id_alta_formazione_tipo_corso = models.ForeignKey(
        "AltaFormazioneTipoCorso",
        models.SET_NULL,
        db_column="ID_ALTA_FORMAZIONE_TIPO_CORSO",
        blank=True,
        null=True,
    )
    lingua = models.CharField(db_column="LINGUA", max_length=512, blank=True, null=True)
    id_alta_formazione_mod_erogazione = models.ForeignKey(
        "AltaFormazioneModalitaErogazione",
        models.DO_NOTHING,
        db_column="ID_ALTA_FORMAZIONE_MOD_EROGAZIONE",
        blank=True,
        null=True,
    )
    ore = models.IntegerField(blank=True, null=True)
    mesi = models.IntegerField(blank=True, null=True)
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
        db_column="MATRICOLA_DIRETTORE_SCIENTIFICO",
        blank=True,
        null=True,
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
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_DATI_BASE"
        unique_together = (("titolo_it", "data_inizio"),)


class AltaFormazioneIncaricoDidattico(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    id_alta_formazione_piano_didattico = models.ForeignKey(
        "AltaFormazionePianoDidattico",
        models.SET_NULL,
        db_column="ID_ALTA_FORMAZIONE_PIANO_DIDATTICO",
        blank=True,
        null=True,
    )
    id_alta_formazione_dati_base = models.ForeignKey(
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

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_INCARICO_DIDATTICO"


class AltaFormazioneModalitaErogazione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=1000)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_MODALITA_EROGAZIONE"


class AltaFormazioneModalitaSelezione(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_selezione = models.CharField(db_column="TIPO_SELEZIONE", max_length=100)
    id_alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

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
    id_alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

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
    id_alta_formazione_dati_base = models.ForeignKey(
        AltaFormazioneDatiBase, models.CASCADE, db_column="ID_ALTA_FORMAZIONE_DATI_BASE"
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_PIANO_DIDATTICO"


class AltaFormazioneTipoCorso(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    tipo_corso_descr = models.CharField(db_column="TIPO_CORSO_DESCR", max_length=256)
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ALTA_FORMAZIONE_TIPO_CORSO"
