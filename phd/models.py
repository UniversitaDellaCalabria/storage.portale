from django.contrib.auth import get_user_model
from django.db import models
from generics.models import InsModAbstract


class DidatticaDottoratoAttivitaFormativaTipologia(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_it = models.CharField(db_column="NOME_IT", max_length=255)
    nome_en = models.CharField(
        db_column="NOME_EN", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_TIPOLOGIA"

    def __str__(self):
        return self.nome_it


class DidatticaDottoratoAttivitaFormativa(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_af = models.CharField(
        db_column="NOME_AF", max_length=1000, blank=False, null=True
    )
    ssd = models.CharField(db_column="SSD", max_length=1000, blank=False, null=True)
    didattica_ssd = models.ForeignKey(
        "cds.DidatticaSsd",
        on_delete=models.SET_NULL,
        db_column="ID_DIDATTICA_SSD",
        blank=False,
        null=True,
        to_field="ssd_id",
    )
    numero_ore = models.IntegerField(db_column="NUMERO_ORE", blank=False, null=True)
    cfu = models.IntegerField(db_column="CFU", blank=False, null=True)
    tipo_af = models.CharField(db_column="TIPO_AF", max_length=500)
    tipologia = models.ForeignKey(
        DidatticaDottoratoAttivitaFormativaTipologia,
        models.SET_NULL,
        db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_TIPOLOGIA",
        blank=False,
        null=True,
    )
    rif_dottorato = models.CharField(
        db_column="RIF_DOTTORATO", max_length=1000, blank=True, null=True
    )
    ciclo = models.IntegerField(db_column="CICLO")
    struttura_proponente = models.ForeignKey(
        "structures.UnitaOrganizzativa",
        models.DO_NOTHING,
        db_column="ID_STRUTTURA_PROPONENTE",
        blank=True,
        null=True,
    )
    struttura_proponente_origine = models.CharField(
        db_column="STRUTTURA_PROPONENTE_ORIGINE", max_length=255, blank=True, null=True
    )
    contenuti_af = models.TextField(db_column="CONTENUTI_AF", blank=False, null=True)
    prerequisiti = models.TextField(db_column="PREREQUISITI", blank=True, null=True)
    num_min_studenti = models.IntegerField(
        db_column="NUM_MIN_STUDENTI", blank=True, null=True
    )
    num_max_studenti = models.IntegerField(
        db_column="NUM_MAX_STUDENTI", blank=True, null=True
    )
    verifica_finale = models.BooleanField(db_column="VERIFICA_FINALE", default=False)
    modalita_verifica = models.CharField(
        db_column="MODALITA_VERIFICA", max_length=1000, blank=True, null=True
    )
    avvio = models.CharField(db_column="AVVIO", blank=True, null=True, max_length=255)
    fine = models.CharField(db_column="FINE", blank=True, null=True, max_length=255)
    orario_aule = models.TextField(db_column="ORARIO_AULE", blank=True, null=True)
    note = models.TextField(db_column="NOTE", blank=True, null=True)
    visualizza_orario = models.BooleanField(
        db_column="VISUALIZZA_ORARIO", default=False
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(), models.SET_NULL, db_column="user_mod_id", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA"


class DidatticaDottoratoAttivitaFormativaAltriDocenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_dottorato_attivita_formativa = models.ForeignKey(
        DidatticaDottoratoAttivitaFormativa,
        models.CASCADE,
        db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA",
        blank=True,
        null=True,
    )
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
        blank=True,
        null=True,
    )
    cognome_nome_origine = models.CharField(
        db_column="COGNOME_NOME_ORIGINE", max_length=200
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(), models.SET_NULL, db_column="user_mod_id", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_ALTRI_DOCENTI"


class DidatticaDottoratoAttivitaFormativaDocente(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_dottorato_attivita_formativa = models.ForeignKey(
        DidatticaDottoratoAttivitaFormativa,
        models.CASCADE,
        db_column="ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA",
        blank=True,
        null=True,
    )
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE_MATRICOLA",
        to_field="matricola",
        blank=True,
        null=True,
    )
    cognome_nome_origine = models.CharField(
        db_column="COGNOME_NOME_ORIGINE", max_length=200
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(), models.SET_NULL, db_column="user_mod_id", blank=True, null=True
    )

    def __str__(self):  # pragma: no cover
        return self.cognome_nome_origine

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_DOCENTE"


class DidatticaDottoratoCds(InsModAbstract):
    dip_cod = models.ForeignKey(
        "structures.DidatticaDipartimento",
        models.DO_NOTHING,
        db_column="DIP_COD",
        blank=True,
        null=True,
        to_field="dip_cod",
    )

    cds_id_esse3 = models.IntegerField(db_column="CDS_ID_ESSE3", primary_key=True)

    cds_cod = models.CharField(
        db_column="CDS_COD", max_length=10, blank=True, null=True
    )
    nome_cds_it = models.CharField(
        db_column="NOME_CDS_IT", max_length=255, blank=True, null=True
    )

    rif_cod = models.CharField(
        db_column="RIF_COD", max_length=10, blank=True, null=True
    )

    rif_des = models.CharField(
        db_column="RIF_DES", max_length=255, blank=True, null=True
    )
    tipo_corso_cod = models.CharField(
        db_column="TIPO_CORSO_COD", max_length=10, blank=True, null=True
    )
    tipo_corso_des = models.CharField(
        db_column="TIPO_CORSO_DES", max_length=80, blank=True, null=True
    )

    durata_anni = models.IntegerField(db_column="DURATA_ANNI", blank=True, null=True)

    valore_min = models.IntegerField(db_column="VALORE_MIN", blank=True, null=True)
    tipo_titit_cod = models.CharField(
        db_column="TIPO_TITIT_COD", max_length=10, blank=True, null=True
    )
    tipo_titit_des = models.CharField(
        db_column="TIPO_TITIT_DES", max_length=255, blank=True, null=True
    )
    tipo_spec_cod = models.CharField(
        db_column="TIPO_SPEC_COD", max_length=10, blank=True, null=True
    )
    tipo_spec_des = models.CharField(
        db_column="TIPO_SPEC_DES", max_length=255, blank=True, null=True
    )
    istat_cod = models.CharField(
        db_column="ISTAT_COD", max_length=10, blank=True, null=True
    )

    max_punti = models.IntegerField(db_column="MAX_PUNTI", blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column="UM_PESO_COD", max_length=5, blank=True, null=True
    )
    um_peso_des = models.CharField(
        db_column="UM_PESO_DES", max_length=40, blank=True, null=True
    )

    aa_att_id = models.IntegerField(db_column="AA_ATT_ID", blank=True, null=True)

    aa_dis_id = models.IntegerField(db_column="AA_DIS_ID", blank=True, null=True)

    url = models.URLField(db_column="URL", max_length=255, blank=True, null=True)
    cds_url_info_web = models.URLField(
        db_column="CDS_URL_INFO_WEB", max_length=255, blank=True, null=True
    )
    cds_vis_web_flg = models.IntegerField(
        db_column="CDS_VIS_WEB_FLG", blank=True, null=True
    )
    cdsord_id_esse3 = models.IntegerField(
        db_column="CDSORD_ID_ESSE3", blank=True, null=True
    )
    cdsord_cod = models.CharField(
        db_column="CDSORD_COD", max_length=10, blank=True, null=True
    )

    aa_ord_id = models.IntegerField(db_column="AA_ORD_ID")
    cdsord_des = models.CharField(
        db_column="CDSORD_DES", max_length=255, blank=True, null=True
    )
    stato_cdsord_cod = models.CharField(
        db_column="STATO_CDSORD_COD", max_length=5, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_CDS"
        unique_together = (("cds_id_esse3", "aa_ord_id"),)


class DidatticaDottoratoPds(InsModAbstract):
    cds_id_esse3 = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column="CDS_ID_ESSE3",
        blank=True,
        null=True,
        related_name="idesse3_ddpds",
    )

    aa_ord = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column="AA_ORD_ID",
        blank=True,
        null=True,
        related_name="aaord_ddpds",
    )

    pds_id_esse3 = models.IntegerField(db_column="PDS_ID_ESSE3", blank=True, null=True)

    pdsord_id_esse3 = models.IntegerField(db_column="PDSORD_ID_ESSE3", primary_key=True)

    pds_cod = models.CharField(
        db_column="PDS_COD", max_length=40, blank=True, null=True
    )

    pds_des = models.CharField(
        db_column="PDS_DES", max_length=255, blank=True, null=True
    )

    indir = models.CharField(db_column="INDIR", max_length=255, blank=True, null=True)

    orien = models.CharField(db_column="ORIEN", max_length=255, blank=True, null=True)

    valore_min = models.IntegerField(db_column="VALORE_MIN", blank=True, null=True)
    stato_cod = models.CharField(
        db_column="STATO_COD", max_length=5, blank=True, null=True
    )

    data_var = models.DateTimeField(db_column="DATA_VAR", blank=True, null=True)

    val_min_tesi = models.IntegerField(db_column="VAL_MIN_TESI", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_PDS"


class DidatticaDottoratoRegolamento(InsModAbstract):
    regdid_id_esse3 = models.IntegerField(db_column="REGDID_ID_ESSE3", primary_key=True)

    aa_regdid_id = models.IntegerField(db_column="AA_REGDID_ID", blank=True, null=True)
    cds_id_esse3 = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column="CDS_ID_ESSE3",
        blank=True,
        null=True,
        related_name="idesse3_ddr",
    )
    regdid_cod = models.CharField(
        db_column="REGDID_COD", max_length=255, blank=True, null=True
    )
    regdid_des = models.CharField(
        db_column="REGDID_DES", max_length=255, blank=True, null=True
    )
    numero_piani_studio = models.IntegerField(
        db_column="NUMERO_PIANI_STUDIO", blank=True, null=True
    )
    frequenza_obbligatoria = models.IntegerField(
        db_column="FREQUENZA_OBBLIGATORIA", blank=True, null=True
    )

    num_ciclo = models.IntegerField(db_column="NUM_CICLO", blank=True, null=True)
    aa_ord = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column="AA_ORD_ID",
        related_name="aaord_ddr",
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DOTTORATO_REGOLAMENTO"
