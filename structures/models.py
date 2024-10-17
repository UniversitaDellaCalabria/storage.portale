from django.contrib.auth import get_user_model
from django.db import models
from generics.models import InsModAbstract


class ComuniAll(models.Model):
    id_comune = models.IntegerField(db_column="ID_COMUNE", primary_key=True)
    ds_comune = models.CharField(
        db_column="DS_COMUNE", max_length=255, blank=True, null=True
    )
    cd_catasto = models.CharField(
        db_column="CD_CATASTO", unique=True, max_length=255, blank=True, null=True
    )
    cd_istat = models.CharField(
        db_column="CD_ISTAT", max_length=6, blank=True, null=True
    )
    dt_costituzione = models.DateTimeField(
        db_column="DT_COSTITUZIONE", blank=True, null=True
    )
    dt_cessazione = models.DateTimeField(
        db_column="DT_CESSAZIONE", blank=True, null=True
    )
    id_prov = models.IntegerField(db_column="ID_PROV", blank=True, null=True)

    cd_sigla = models.CharField(
        db_column="CD_SIGLA", max_length=2, blank=True, null=True
    )
    ds_prov = models.CharField(
        db_column="DS_PROV", max_length=255, blank=True, null=True
    )
    id_nazione = models.IntegerField(db_column="ID_NAZIONE", blank=True, null=True)
    cd_iso3166_1_a2_nazione = models.CharField(
        db_column="CD_ISO3166_1_A2_NAZIONE", max_length=2, blank=True, null=True
    )
    ds_nazione = models.CharField(
        db_column="DS_NAZIONE", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "COMUNI_ALL"


class UnitaOrganizzativa(models.Model):
    uo = models.CharField(db_column="UO", primary_key=True, max_length=40)

    id_ab = models.IntegerField(db_column="ID_AB", unique=True, blank=True, null=True)

    cd_tipo_nodo = models.CharField(
        db_column="CD_TIPO_NODO", max_length=10, default="000"
    )
    ds_tipo_nodo = models.CharField(
        db_column="DS_TIPO_NODO", max_length=255, default="Non assegnato"
    )
    denominazione = models.CharField(
        db_column="DENOMINAZIONE", max_length=255, default="Non assegnato"
    )
    nome_esteso = models.CharField(
        db_column="NOME_ESTESO", max_length=255, default="Non assegnato"
    )
    nome_breve = models.CharField(
        db_column="NOME_BREVE", max_length=50, default="Non assegnato"
    )
    dt_inizio_val = models.DateTimeField(
        db_column="DT_INIZIO_VAL", blank=True, null=True
    )
    dt_fine_val = models.DateTimeField(db_column="DT_FINE_VAL", blank=True, null=True)
    dt_creazione = models.DateTimeField(db_column="DT_CREAZIONE", blank=True, null=True)
    uo_padre = models.CharField(
        db_column="UO_PADRE", max_length=40, blank=True, null=True
    )
    id_ab_padre = models.IntegerField(db_column="ID_AB_PADRE", blank=True, null=True)
    cd_tipo_nodo_padre = models.CharField(
        db_column="CD_TIPO_NODO_PADRE", max_length=10, blank=True, null=True
    )
    ds_tipo_nodo_padre = models.CharField(
        db_column="DS_TIPO_NODO_PADRE", max_length=255, blank=True, null=True
    )
    cd_macrotipo_nodo_padre = models.CharField(
        db_column="CD_MACROTIPO_NODO_PADRE", max_length=10, blank=True, null=True
    )
    denominazione_padre = models.CharField(
        db_column="DENOMINAZIONE_PADRE", max_length=255, blank=True, null=True
    )
    nome_esteso_padre = models.CharField(
        db_column="NOME_ESTESO_PADRE", max_length=255, blank=True, null=True
    )
    nome_breve_padre = models.CharField(
        db_column="NOME_BREVE_PADRE", max_length=50, blank=True, null=True
    )
    dt_inizio_val_padre = models.DateTimeField(
        db_column="DT_INIZIO_VAL_PADRE", blank=True, null=True
    )
    dt_fine_val_padre = models.DateTimeField(
        db_column="DT_FINE_VAL_PADRE", blank=True, null=True
    )
    dt_creazione_padre = models.DateTimeField(
        db_column="DT_CREAZIONE_PADRE", blank=True, null=True
    )
    cd_csa = models.CharField(
        db_column="CD_CSA", unique=True, max_length=40, blank=True, null=True
    )
    ds_mission = models.TextField(db_column="DS_MISSION", blank=True, null=True)

    def __str__(self):  # pragma: no cover
        return "{}".format(self.denominazione)

    class Meta:
        managed = True
        db_table = "UNITA_ORGANIZZATIVA"


class UnitaOrganizzativaFunzioni(models.Model):
    matricola = models.CharField(
        db_column="MATRICOLA", max_length=6, blank=True, null=True
    )
    cd_csa = models.ForeignKey(
        UnitaOrganizzativa,
        models.DO_NOTHING,
        db_column="CD_CSA",
        to_field="cd_csa",
        blank=True,
        null=True,
    )
    cod_fis = models.ForeignKey(
        "addressbook.Personale",
        models.DO_NOTHING,
        db_column="COD_FIS",
        blank=True,
        null=True,
        to_field="cod_fis",
    )
    comparto = models.CharField(
        db_column="COMPARTO", max_length=1, blank=True, null=True
    )
    ruolo = models.CharField(db_column="RUOLO", max_length=4, blank=True, null=True)
    funzione = models.CharField(
        db_column="FUNZIONE", max_length=6, blank=True, null=True
    )
    decorrenza = models.DateTimeField(db_column="DECORRENZA", blank=True, null=True)
    termine = models.DateTimeField(db_column="TERMINE", blank=True, null=True)
    ds_funzione = models.CharField(
        db_column="DS_FUNZIONE", max_length=100, blank=True, null=True
    )
    fl_posorg = models.FloatField(db_column="FL_POSORG", blank=True, null=True)
    fl_responsabile = models.FloatField(
        db_column="FL_RESPONSABILE", blank=True, null=True
    )
    cd_funzbase = models.CharField(
        db_column="CD_FUNZBASE", max_length=6, blank=True, null=True
    )
    id_ab = models.IntegerField(db_column="ID_AB", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "UNITA_ORGANIZZATIVA_FUNZIONI"


class UnitaOrganizzativaTipoFunzioni(models.Model):
    cd_tipo_nod = models.CharField(
        db_column="CD_TIPO_NOD", primary_key=True, max_length=100
    )
    funzione = models.CharField(db_column="FUNZIONE", max_length=100)
    descr_funzione = models.CharField(db_column="DESCR_FUNZIONE", max_length=1000)

    class Meta:
        managed = True
        db_table = "UNITA_ORGANIZZATIVA_TIPO_FUNZIONI"
        unique_together = (("cd_tipo_nod", "funzione"),)


class UnitaOrganizzativaContatti(models.Model):
    ab = models.OneToOneField(
        UnitaOrganizzativa,
        models.DO_NOTHING,
        db_column="ID_AB",
        primary_key=True,
        to_field="id_ab",
    )
    cd_tipo_cont = models.ForeignKey(
        "addressbook.PersonaleUoTipoContatto",
        models.DO_NOTHING,
        db_column="CD_TIPO_CONT",
    )
    contatto = models.CharField(
        db_column="CONTATTO", max_length=255, blank=True, null=True
    )
    prg_priorita = models.IntegerField(db_column="PRG_PRIORITA")
    denominazione = models.CharField(
        db_column="DENOMINAZIONE", max_length=255, blank=True, null=True
    )
    dt_fine_val = models.DateTimeField(db_column="DT_FINE_VAL", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "UNITA_ORGANIZZATIVA_CONTATTI"
        unique_together = (("ab", "cd_tipo_cont", "prg_priorita"),)


class TerritorioIt(models.Model):
    cd_catasto = models.OneToOneField(
        ComuniAll, models.DO_NOTHING, db_column="CD_CATASTO", primary_key=True
    )
    cd_istat = models.CharField(
        db_column="CD_ISTAT", max_length=6, blank=True, null=True
    )
    ds_comune = models.CharField(
        db_column="DS_COMUNE", max_length=255, blank=True, null=True
    )
    cd_sigla = models.CharField(
        db_column="CD_SIGLA", max_length=2, blank=True, null=True
    )
    ds_provincia = models.CharField(
        db_column="DS_PROVINCIA", max_length=255, blank=True, null=True
    )
    cd_770_regio = models.CharField(
        db_column="CD_770_REGIO", max_length=2, blank=True, null=True
    )
    ds_regione = models.CharField(
        db_column="DS_REGIONE", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "TERRITORIO_IT"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cd_catasto, self.cd_istat)


class DidatticaDipartimento(InsModAbstract):
    dip_id = models.IntegerField(db_column="DIP_ID", primary_key=True)
    dip_cod = models.CharField(
        db_column="DIP_COD", unique=True, max_length=40, blank=True, null=True
    )
    dip_des_it = models.CharField(
        db_column="DIP_DES_IT", max_length=255, blank=True, null=True
    )
    dip_des_eng = models.CharField(
        db_column="DIP_DES_ENG", max_length=255, blank=True, null=True
    )
    dip_nome_breve = models.CharField(
        db_column="DIP_NOME_BREVE", max_length=100, blank=True, null=True
    )
    dip_cd_csa = models.CharField(
        db_column="DIP_CD_CSA", max_length=40, blank=True, null=True
    )
    miur_dip_id = models.IntegerField(db_column="MIUR_DIP_ID", blank=True, null=True)
    url_pubbl_off_f = models.URLField(
        db_column="URL_PUBBL_OFF_F", max_length=255, blank=True, null=True
    )
    dip_vis_web_flg = models.IntegerField(
        db_column="DIP_VIS_WEB_FLG", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DIPARTIMENTO"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.dip_cod, self.dip_des_it)


class DidatticaDipartimentoUrl(models.Model):
    dip_cod = models.OneToOneField(
        DidatticaDipartimento,
        models.DO_NOTHING,
        db_column="ID_DIDATTICA_DIPARTIMENTO_COD",
        primary_key=True,
        to_field="dip_cod",
    )
    dip_url = models.URLField(db_column="DIP_URL", max_length=4000)

    class Meta:
        managed = True
        db_table = "DIDATTICA_DIPARTIMENTO_URL"


class DidatticaDipartimentoGruppi(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_breve_it = models.CharField(db_column="DESCR_BREVE_IT", max_length=1000)
    descr_breve_en = models.CharField(
        db_column="DESCR_BREVE_EN", max_length=1000, blank=True, null=True
    )
    descr_lunga_it = models.TextField(db_column="DESCR_LUNGA_IT", blank=True, null=True)
    descr_lunga_en = models.TextField(db_column="DESCR_LUNGA_EN", blank=True, null=True)
    didattica_dipartimento = models.ForeignKey(
        DidatticaDipartimento, models.DO_NOTHING, db_column="ID_DIDATTICA_DIPARTIMENTO"
    )
    ordine = models.IntegerField(db_column="ORDINE", default=10)
    visibile = models.BooleanField(db_column="VISIBILE", default=True)
    dt_mod = models.DateField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="ID_USER_MOD"
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DIPARTIMENTO_GRUPPI"
        ordering = ("ordine",)


class DidatticaDipartimentoGruppiComponenti(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_dipartimento_gruppi = models.ForeignKey(
        DidatticaDipartimentoGruppi,
        models.CASCADE,
        db_column="ID_DIDATTICA_DIPARTIMENTO_GRUPPI",
    )
    matricola = models.ForeignKey(
        "addressbook.Personale",
        models.SET_NULL,
        db_column="MATRICOLA",
        blank=True,
        null=True,
        to_field="matricola",
    )
    cognome = models.CharField(
        db_column="COGNOME", max_length=100, blank=True, null=True
    )
    nome = models.CharField(db_column="NOME", max_length=100, blank=True, null=True)
    funzione_it = models.CharField(
        db_column="FUNZIONE_IT", max_length=1000, blank=True, null=True
    )
    funzione_en = models.CharField(
        db_column="FUNZIONE_EN", max_length=1000, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE", default=10)
    visibile = models.BooleanField(db_column="VISIBILE", default=True)
    dt_mod = models.DateField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="ID_USER_MOD"
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_DIPARTIMENTO_GRUPPI_COMPONENTI"
        ordering = ("ordine",)
