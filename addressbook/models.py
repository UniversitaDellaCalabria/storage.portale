from django.contrib.auth import get_user_model
from django.db import models
from generics.models import InsModAbstract


class Personale(InsModAbstract):
    id_ab = models.IntegerField(db_column="ID_AB", unique=True)
    cd_esterno = models.CharField(
        db_column="CD_ESTERNO", max_length=60, blank=True, null=True
    )
    matricola = models.CharField(db_column="MATRICOLA", unique=True, max_length=6)
    matricola_sp = models.CharField(
        db_column="MATRICOLA_SP", max_length=255, blank=True, null=True
    )
    nome = models.CharField(db_column="NOME", max_length=100, blank=True, null=True)
    cognome = models.CharField(
        db_column="COGNOME", max_length=100, blank=True, null=True
    )
    middle_name = models.CharField(
        db_column="MIDDLE_NAME", max_length=100, blank=True, null=True
    )
    cod_fis = models.CharField(
        db_column="COD_FIS", unique=True, max_length=16, blank=True, null=True
    )
    cd_genere = models.CharField(
        db_column="CD_GENERE", max_length=1, blank=True, null=True
    )
    dt_nascita = models.DateField(db_column="DT_NASCITA", blank=True, null=True)
    id_comu_nasc = models.IntegerField(db_column="ID_COMU_NASC", blank=True, null=True)
    ds_cittstra_nasc = models.CharField(
        db_column="DS_CITTSTRA_NASC", max_length=255, blank=True, null=True
    )
    ds_comune_nasc = models.CharField(
        db_column="DS_COMUNE_NASC", max_length=255, blank=True, null=True
    )
    ds_prov_nasc = models.CharField(
        db_column="DS_PROV_NASC", max_length=255, blank=True, null=True
    )
    cd_sigla_nasc = models.CharField(
        db_column="CD_SIGLA_NASC", max_length=2, blank=True, null=True
    )
    id_nazione_nasc = models.IntegerField(
        db_column="ID_NAZIONE_NASC", blank=True, null=True
    )
    ds_nazi_nasc = models.CharField(
        db_column="DS_NAZI_NASC", max_length=100, blank=True, null=True
    )
    ds_nazi_breve_nasc = models.CharField(
        db_column="DS_NAZI_BREVE_NASC", max_length=20, blank=True, null=True
    )
    comu_res = models.ForeignKey(
        "structures.ComuniAll",
        models.DO_NOTHING,
        db_column="ID_COMU_RES",
        blank=True,
        null=True,
    )
    ds_comune_res = models.CharField(
        db_column="DS_COMUNE_RES", max_length=255, blank=True, null=True
    )
    cd_cap_res = models.CharField(
        db_column="CD_CAP_RES", max_length=5, blank=True, null=True
    )
    indirizzo_res = models.CharField(
        db_column="INDIRIZZO_RES", max_length=255, blank=True, null=True
    )
    num_civico_res = models.CharField(
        db_column="NUM_CIVICO_RES", max_length=15, blank=True, null=True
    )
    cd_sigla_res = models.CharField(
        db_column="CD_SIGLA_RES", max_length=2, blank=True, null=True
    )
    id_comu_dom = models.IntegerField(db_column="ID_COMU_DOM", blank=True, null=True)
    ds_comune_dom = models.CharField(
        db_column="DS_COMUNE_DOM", max_length=255, blank=True, null=True
    )
    cd_cap_dom = models.CharField(
        db_column="CD_CAP_DOM", max_length=5, blank=True, null=True
    )
    indirizzo_dom = models.CharField(
        db_column="INDIRIZZO_DOM", max_length=255, blank=True, null=True
    )
    num_civico_dom = models.CharField(
        db_column="NUM_CIVICO_DOM", max_length=15, blank=True, null=True
    )
    cd_sigla_dom = models.CharField(
        db_column="CD_SIGLA_DOM", max_length=2, blank=True, null=True
    )
    cd_comparto = models.CharField(db_column="CD_COMPARTO", max_length=1)
    ds_comparto = models.CharField(
        db_column="DS_COMPARTO", max_length=40, blank=True, null=True
    )
    cd_ruolo = models.CharField(db_column="CD_RUOLO", max_length=4)
    ds_ruolo = models.CharField(
        db_column="DS_RUOLO", max_length=40, blank=True, null=True
    )
    ds_ruolo_locale = models.CharField(
        db_column="DS_RUOLO_LOCALE", max_length=40, blank=True, null=True
    )
    peso_ruolo = models.DecimalField(
        db_column="PESO_RUOLO", max_digits=10, decimal_places=0, blank=True, null=True
    )
    dt_rap_ini = models.DateField(db_column="DT_RAP_INI", blank=True, null=True)

    dt_rap_fin = models.DateField(db_column="DT_RAP_FIN", blank=True, null=True)
    cd_ssd = models.CharField(db_column="CD_SSD", max_length=12, blank=True, null=True)
    ds_ssd = models.CharField(db_column="DS_SSD", max_length=100, blank=True, null=True)
    cd_fac = models.CharField(db_column="CD_FAC", max_length=10, blank=True, null=True)
    ds_fac = models.CharField(db_column="DS_FAC", max_length=255, blank=True, null=True)
    cd_uo_aff_org = models.ForeignKey(
        "structures.UnitaOrganizzativa",
        models.DO_NOTHING,
        db_column="CD_UO_AFF_ORG",
        blank=True,
        null=True,
    )
    ds_aff_org = models.CharField(
        db_column="DS_AFF_ORG", max_length=255, blank=True, null=True
    )
    ds_aff_org_breve = models.CharField(
        db_column="DS_AFF_ORG_BREVE", max_length=50, blank=True, null=True
    )
    cd_csa_aff_org2 = models.CharField(
        db_column="CD_CSA_AFF_ORG2", max_length=6, blank=True, null=True
    )
    ds_aff_org2 = models.CharField(
        db_column="DS_AFF_ORG2", max_length=255, blank=True, null=True
    )
    ds_aff_org2_breve = models.CharField(
        db_column="DS_AFF_ORG2_BREVE", max_length=50, blank=True, null=True
    )
    cd_csa_aff_org3 = models.CharField(
        db_column="CD_CSA_AFF_ORG3", max_length=6, blank=True, null=True
    )
    ds_aff_org3 = models.CharField(
        db_column="DS_AFF_ORG3", max_length=255, blank=True, null=True
    )
    ds_aff_org3_breve = models.CharField(
        db_column="DS_AFF_ORG3_BREVE", max_length=50, blank=True, null=True
    )
    cd_csa_aff_org4 = models.CharField(
        db_column="CD_CSA_AFF_ORG4", max_length=6, blank=True, null=True
    )
    ds_aff_org4 = models.CharField(
        db_column="DS_AFF_ORG4", max_length=255, blank=True, null=True
    )
    ds_aff_org4_breve = models.CharField(
        db_column="DS_AFF_ORG4_BREVE", max_length=50, blank=True, null=True
    )
    sede = models.CharField(db_column="SEDE", max_length=6, blank=True, null=True)
    ds_sede = models.CharField(
        db_column="DS_SEDE", max_length=255, blank=True, null=True
    )
    ds_sede_breve = models.CharField(
        db_column="DS_SEDE_BREVE", max_length=50, blank=True, null=True
    )
    profilo = models.CharField(
        db_column="PROFILO", max_length=11, blank=True, null=True
    )
    ds_profilo = models.CharField(
        db_column="DS_PROFILO", max_length=100, blank=True, null=True
    )
    ds_profilo_breve = models.CharField(
        db_column="DS_PROFILO_BREVE", max_length=50, blank=True, null=True
    )
    cd_ateneo_corr = models.CharField(
        db_column="CD_ATENEO_CORR", max_length=10, blank=True, null=True
    )
    ds_ateneo_corr = models.CharField(
        db_column="DS_ATENEO_CORR", max_length=255, blank=True, null=True
    )
    dt_ini_rap_univ = models.DateField(
        db_column="DT_INI_RAP_UNIV", blank=True, null=True
    )
    dt_fin_rap_univ = models.DateField(
        db_column="DT_FIN_RAP_UNIV", blank=True, null=True
    )
    telrif = models.CharField(db_column="TELRIF", max_length=255, blank=True, null=True)
    email = models.CharField(db_column="EMAIL", max_length=255, blank=True, null=True)
    urlcv = models.URLField(db_column="URLCV", max_length=255, blank=True, null=True)
    fl_docente = models.PositiveIntegerField(
        db_column="FL_DOCENTE", blank=True, null=True
    )
    cd_anagrafico = models.CharField(
        db_column="CD_ANAGRAFICO", max_length=20, blank=True, null=True
    )
    inquadr = models.CharField(
        db_column="INQUADR", max_length=50, blank=True, null=True
    )
    badge = models.CharField(db_column="BADGE", max_length=255, blank=True, null=True)
    tempo = models.CharField(db_column="TEMPO", max_length=1, blank=True, null=True)
    id_contratto = models.IntegerField(db_column="ID_CONTRATTO", blank=True, null=True)

    flg_cessato = models.IntegerField(db_column="FLG_CESSATO", blank=True, null=True)
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_personale",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_personale",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    cv_full_it = models.TextField(db_column="CV_FULL_IT", blank=True, null=True)
    cv_short_it = models.TextField(db_column="CV_SHORT_IT", blank=True, null=True)
    cv_full_eng = models.TextField(db_column="CV_FULL_ENG", blank=True, null=True)
    cv_short_eng = models.TextField(db_column="CV_SHORT_ENG", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PERSONALE"

    def __str__(self):  # pragma: no cover
        return "{} {} [{}]".format(self.cognome, self.nome, self.matricola)


class PersonaleAttivoTuttiRuoli(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    id_ab = models.BigIntegerField(db_column="ID_AB", blank=True, null=True)
    matricola = models.ForeignKey(
        Personale,
        models.DO_NOTHING,
        db_column="MATRICOLA",
        to_field="matricola",
        blank=True, 
        null=True,
        related_name="personaleattivotuttiruoli",
    )
    cod_fis = models.CharField(
        db_column="COD_FIS", max_length=16, blank=True, null=True
    )
    cd_ruolo = models.CharField(
        db_column="CD_RUOLO", max_length=4, blank=True, null=True
    )
    ds_ruolo = models.CharField(
        db_column="DS_RUOLO", max_length=40, blank=True, null=True
    )
    ds_ruolo_breve = models.CharField(
        db_column="DS_RUOLO_BREVE", max_length=20, blank=True, null=True
    )
    cd_tipo_ruolo = models.CharField(
        db_column="CD_TIPO_RUOLO", max_length=2, blank=True, null=True
    )
    ds_tipo_ruolo = models.CharField(
        db_column="DS_TIPO_RUOLO", max_length=80, blank=True, null=True
    )
    cd_inquadr = models.CharField(
        db_column="CD_INQUADR", max_length=50, blank=True, null=True
    )
    ds_inquadr = models.CharField(
        db_column="DS_INQUADR", max_length=80, blank=True, null=True
    )
    cd_uo_aff_org = models.ForeignKey(
        "structures.UnitaOrganizzativa",
        models.DO_NOTHING,
        db_column="CD_UO_AFF_ORG",
        blank=True,
        null=True,
    )
    ds_aff_org = models.CharField(
        db_column="DS_AFF_ORG", max_length=255, blank=True, null=True
    )
    ds_aff_org_breve = models.CharField(
        db_column="DS_AFF_ORG_BREVE", max_length=50, blank=True, null=True
    )
    fl_tipo_rap = models.FloatField(db_column="FL_TIPO_RAP", blank=True, null=True)
    cd_ssd = models.CharField(db_column="CD_SSD", max_length=12, blank=True, null=True)
    ds_ssd = models.CharField(db_column="DS_SSD", max_length=100, blank=True, null=True)
    ds_ssd_breve = models.CharField(
        db_column="DS_SSD_BREVE", max_length=20, blank=True, null=True
    )
    area_ssd = models.CharField(
        db_column="AREA_SSD", max_length=2, blank=True, null=True
    )
    ds_area_ssd = models.CharField(
        db_column="DS_AREA_SSD", max_length=100, blank=True, null=True
    )
    cd_riferimento = models.CharField(
        db_column="CD_RIFERIMENTO", max_length=10, blank=True, null=True
    )
    ds_riferimento = models.CharField(
        db_column="DS_RIFERIMENTO", max_length=120, blank=True, null=True
    )
    peso_inc = models.IntegerField(db_column="PESO_INC", blank=True, null=True)
    peso_ric = models.IntegerField(db_column="PESO_RIC", blank=True, null=True)
    sede = models.CharField(db_column="SEDE", max_length=6, blank=True, null=True)
    ds_sede = models.CharField(
        db_column="DS_SEDE", max_length=255, blank=True, null=True
    )
    dt_rap_ini = models.DateTimeField(db_column="DT_RAP_INI", blank=True, null=True)
    cd_profilo = models.CharField(
        db_column="CD_PROFILO", max_length=11, blank=True, null=True
    )
    ds_profilo = models.CharField(
        db_column="DS_PROFILO", max_length=100, blank=True, null=True
    )
    fl_docente = models.IntegerField(db_column="FL_DOCENTE", blank=True, null=True)
    cd_onorifico = models.CharField(
        db_column="CD_ONORIFICO", max_length=4, blank=True, null=True
    )
    ds_onorifico = models.CharField(
        db_column="DS_ONORIFICO", max_length=100, blank=True, null=True
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod_id = models.CharField(
        db_column="USER_MOD_ID", max_length=32, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PERSONALE_ATTIVO_TUTTI_RUOLI"


class PersonaleUoTipoContatto(models.Model):
    cod_contatto = models.CharField(
        db_column="COD_CONTATTO", primary_key=True, max_length=20
    )
    descr_contatto = models.CharField(db_column="DESCR_CONTATTO", max_length=200)

    class Meta:
        managed = True
        db_table = "PERSONALE_UO_TIPO_CONTATTO"


class PersonaleContatti(models.Model):
    id_ab = models.IntegerField(db_column="ID_AB", primary_key=True)
    cod_fis = models.ForeignKey(
        Personale,
        models.DO_NOTHING,
        db_column="COD_FIS",
        blank=True,
        null=True,
        to_field="cod_fis",
        related_name="personalecontatti",
    )
    cd_tipo_cont = models.ForeignKey(
        PersonaleUoTipoContatto, models.DO_NOTHING, db_column="CD_TIPO_CONT"
    )
    contatto = models.CharField(
        db_column="CONTATTO", max_length=255, blank=True, null=True
    )
    prg_priorita = models.IntegerField(db_column="PRG_PRIORITA")
    dt_ins_mod = models.DateField(db_column="DT_INS_MOD", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PERSONALE_CONTATTI"
        unique_together = (("id_ab", "cd_tipo_cont", "prg_priorita"),)


class PersonalePrioritaRuolo(models.Model):
    cd_ruolo = models.CharField(db_column="CD_RUOLO", primary_key=True, max_length=50)
    ds_ruolo = models.CharField(
        db_column="DS_RUOLO", max_length=1000, blank=True, null=True
    )
    priorita = models.IntegerField(db_column="PRIORITA", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PERSONALE_PRIORITA_RUOLO"
