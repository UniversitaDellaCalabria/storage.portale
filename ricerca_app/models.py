# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `# managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Personale(models.Model):
    id_ab = models.IntegerField(db_column='ID_AB')
    cd_esterno = models.CharField(
        db_column='CD_ESTERNO', max_length=60, blank=True, null=True)
    matricola = models.CharField(
        db_column='MATRICOLA', unique=True, max_length=6)
    matricola_sp = models.CharField(
        db_column='MATRICOLA_SP', max_length=255, blank=True, null=True)
    nome = models.CharField(
        db_column='NOME', max_length=100, blank=True, null=True)
    cognome = models.CharField(
        db_column='COGNOME', max_length=100, blank=True, null=True)
    middle_name = models.CharField(
        db_column='MIDDLE_NAME', max_length=100, blank=True, null=True)
    cod_fis = models.CharField(
        db_column='COD_FIS', unique=True, max_length=16, blank=True, null=True)
    cd_genere = models.CharField(
        db_column='CD_GENERE', max_length=1, blank=True, null=True)
    dt_nascita = models.DateField(
        db_column='DT_NASCITA', blank=True, null=True)
    id_comu_nasc = models.IntegerField(
        db_column='ID_COMU_NASC', blank=True, null=True)
    ds_cittstra_nasc = models.CharField(
        db_column='DS_CITTSTRA_NASC', max_length=255, blank=True, null=True)
    ds_comune_nasc = models.CharField(
        db_column='DS_COMUNE_NASC', max_length=255, blank=True, null=True)
    ds_prov_nasc = models.CharField(
        db_column='DS_PROV_NASC', max_length=255, blank=True, null=True)
    cd_sigla_nasc = models.CharField(
        db_column='CD_SIGLA_NASC', max_length=2, blank=True, null=True)
    id_nazione_nasc = models.IntegerField(
        db_column='ID_NAZIONE_NASC', blank=True, null=True)
    ds_nazi_nasc = models.CharField(
        db_column='DS_NAZI_NASC', max_length=100, blank=True, null=True)
    ds_nazi_breve_nasc = models.CharField(
        db_column='DS_NAZI_BREVE_NASC', max_length=20, blank=True, null=True)
    id_comu_res = models.IntegerField(
        db_column='ID_COMU_RES', blank=True, null=True)
    ds_comune_res = models.CharField(
        db_column='DS_COMUNE_RES', max_length=255, blank=True, null=True)
    cd_cap_res = models.CharField(
        db_column='CD_CAP_RES', max_length=5, blank=True, null=True)
    indirizzo_res = models.CharField(
        db_column='INDIRIZZO_RES', max_length=255, blank=True, null=True)
    num_civico_res = models.CharField('Numero Civico Residenza',
                                      db_column='NUM_CIVICO_RES', max_length=15, blank=True, null=True)
    cd_sigla_res = models.CharField(
        db_column='CD_SIGLA_RES', max_length=2, blank=True, null=True)
    id_comu_dom = models.IntegerField(
        db_column='ID_COMU_DOM', blank=True, null=True)
    ds_comune_dom = models.CharField(
        db_column='DS_COMUNE_DOM', max_length=255, blank=True, null=True)
    cd_cap_dom = models.CharField(
        db_column='CD_CAP_DOM', max_length=5, blank=True, null=True)
    indirizzo_dom = models.CharField(
        db_column='INDIRIZZO_DOM', max_length=255, blank=True, null=True)
    num_civico_dom = models.CharField(
        db_column='NUM_CIVICO_DOM', max_length=15, blank=True, null=True)
    cd_sigla_dom = models.CharField(
        db_column='CD_SIGLA_DOM', max_length=2, blank=True, null=True)
    cd_comparto = models.CharField(db_column='CD_COMPARTO', max_length=1)
    ds_comparto = models.CharField(
        db_column='DS_COMPARTO', max_length=40, blank=True, null=True)
    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4)
    ds_ruolo = models.CharField(
        db_column='DS_RUOLO', max_length=40, blank=True, null=True)
    ds_ruolo_locale = models.CharField(
        db_column='DS_RUOLO_LOCALE', max_length=40, blank=True, null=True)
    peso_ruolo = models.DecimalField(
        db_column='PESO_RUOLO', max_digits=10, decimal_places=0, blank=True, null=True)
    dt_rap_ini = models.DateField(
        db_column='DT_RAP_INI', blank=True, null=True)
    dt_rap_fin = models.DateField(
        db_column='DT_RAP_FIN', blank=True, null=True)
    cd_ssd = models.CharField(
        db_column='CD_SSD', max_length=12, blank=True, null=True)
    ds_ssd = models.CharField(
        db_column='DS_SSD', max_length=100, blank=True, null=True)
    cd_fac = models.CharField(
        db_column='CD_FAC', max_length=10, blank=True, null=True)
    ds_fac = models.CharField(
        db_column='DS_FAC', max_length=255, blank=True, null=True)
    aff_org = models.CharField(
        db_column='AFF_ORG', max_length=6, blank=True, null=True)
    ds_aff_org = models.CharField(
        db_column='DS_AFF_ORG', max_length=255, blank=True, null=True)
    ds_aff_org_breve = models.CharField(
        db_column='DS_AFF_ORG_BREVE', max_length=50, blank=True, null=True)
    aff_org2 = models.CharField(
        db_column='AFF_ORG2', max_length=6, blank=True, null=True)
    ds_aff_org2 = models.CharField(
        db_column='DS_AFF_ORG2', max_length=255, blank=True, null=True)
    ds_aff_org2_breve = models.CharField(
        db_column='DS_AFF_ORG2_BREVE', max_length=50, blank=True, null=True)
    aff_org3 = models.CharField(
        db_column='AFF_ORG3', max_length=6, blank=True, null=True)
    ds_aff_org3 = models.CharField(
        db_column='DS_AFF_ORG3', max_length=255, blank=True, null=True)
    ds_aff_org3_breve = models.CharField(
        db_column='DS_AFF_ORG3_BREVE', max_length=50, blank=True, null=True)
    aff_org4 = models.CharField(
        db_column='AFF_ORG4', max_length=6, blank=True, null=True)
    ds_aff_org4 = models.CharField(
        db_column='DS_AFF_ORG4', max_length=255, blank=True, null=True)
    ds_aff_org4_breve = models.CharField(
        db_column='DS_AFF_ORG4_BREVE', max_length=50, blank=True, null=True)
    sede = models.CharField(
        db_column='SEDE', max_length=6, blank=True, null=True)
    ds_sede = models.CharField(
        db_column='DS_SEDE', max_length=255, blank=True, null=True)
    ds_sede_breve = models.CharField(
        db_column='DS_SEDE_BREVE', max_length=50, blank=True, null=True)
    profilo = models.CharField(
        db_column='PROFILO', max_length=11, blank=True, null=True)
    ds_profilo = models.CharField(
        db_column='DS_PROFILO', max_length=100, blank=True, null=True)
    ds_profilo_breve = models.CharField(
        db_column='DS_PROFILO_BREVE', max_length=50, blank=True, null=True)
    cd_ateneo_corr = models.CharField(
        db_column='CD_ATENEO_CORR', max_length=10, blank=True, null=True)
    ds_ateneo_corr = models.CharField(
        db_column='DS_ATENEO_CORR', max_length=255, blank=True, null=True)
    dt_ini_rap_univ = models.DateField(
        db_column='DT_INI_RAP_UNIV', blank=True, null=True)
    dt_fin_rap_univ = models.DateField(
        db_column='DT_FIN_RAP_UNIV', blank=True, null=True)
    telrif = models.CharField(
        db_column='TELRIF', max_length=255, blank=True, null=True)
    email = models.CharField(
        db_column='EMAIL', max_length=255, blank=True, null=True)
    urlcv = models.CharField(
        db_column='URLCV', max_length=255, blank=True, null=True)
    fl_docente = models.PositiveIntegerField(
        db_column='FL_DOCENTE', blank=True, null=True)
    cd_anagrafico = models.CharField(
        db_column='CD_ANAGRAFICO', max_length=20, blank=True, null=True)
    inquadr = models.CharField(
        db_column='INQUADR', max_length=50, blank=True, null=True)
    badge = models.CharField(
        db_column='BADGE', max_length=255, blank=True, null=True)
    tempo = models.CharField(
        db_column='TEMPO', max_length=1, blank=True, null=True)
    id_contratto = models.IntegerField(
        db_column='ID_CONTRATTO', blank=True, null=True)
    flg_cessato = models.IntegerField(
        db_column='FLG_CESSATO', blank=True, null=True)
    dt_ins = models.DateField(db_column='DT_INS')
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_personale',
                                 on_delete=models.SET_NULL,
                                 db_column='USER_INS_ID',
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_personale',
                                 on_delete=models.SET_NULL,
                                 db_column='USER_MOD_ID',
                                 blank=True, null=True)

    class Meta:
        db_table = 'PERSONALE'
        verbose_name_plural = _("Personale")

    def __str__(self):
        return '{} {} [{}]'.format(self.nome,
                                   self.cognome, self.matricola)


class InsModAbstract(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS', auto_now_add=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', auto_now=True,
                                  blank=True, null=True)

    class Meta:
        abstract = True


class RicercaAster1(InsModAbstract):
    descrizione = models.TextField(db_column='DESCRIZIONE',
                                   max_length=200)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_aster1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_aster1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_ASTER1'
        verbose_name_plural = _("Aster 1")
        ordering = ('descrizione',)

    def __str__(self):
        return '{}'.format(self.descrizione)


class RicercaAster2(InsModAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)
    ricerca_aster1 = models.ForeignKey(RicercaAster1,
                                       models.DO_NOTHING,
                                       db_column='RICERCA_ASTER1_ID')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_aster2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_aster2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_ASTER2'
        verbose_name_plural = _("Aster 2")
        ordering = ('ricerca_aster1',)

    def __str__(self):
        return '{} {}'.format(self.ricerca_aster1,
                              self.descrizione)


class RicercaDocenteGruppo(InsModAbstract):
    ricerca_gruppo = models.ForeignKey('RicercaGruppo',
                                       models.DO_NOTHING,
                                       db_column='RICERCA_GRUPPO_ID')
    docente = models.ForeignKey(Personale, models.DO_NOTHING,
                                db_column='PERSONALE_ID', blank=True, null=True)
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_dg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_dg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_DOCENTE_GRUPPO'
        verbose_name_plural = _("Docente Gruppi di Ricerca")
        ordering = ('-dt_fine',)

    def __str__(self):
        return '{} [{}]'.format(self.docente,
                                self.ricerca_gruppo.nome)


class RicercaDocenteLineaApplicata(InsModAbstract):
    ricerca_linea_applicata = models.ForeignKey('RicercaLineaApplicata',
                                                models.DO_NOTHING,
                                                db_column='RICERCA_LINEA_APPLICATA_ID',
                                                blank=True, null=True)
    docente = models.ForeignKey(Personale, models.DO_NOTHING,
                                db_column='PERSONALE_ID', blank=True, null=True)
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_dla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_dla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_DOCENTE_LINEA_APPLICATA'
        verbose_name_plural = _("Docente Linea Applicata")


class RicercaDocenteLineaBase(InsModAbstract):
    ricerca_linea_base = models.ForeignKey('RicercaLineaBase',
                                           models.DO_NOTHING,
                                           db_column='RICERCA_LINEA_BASE_ID',
                                           blank=True, null=True)
    docente = models.ForeignKey(Personale, models.DO_NOTHING,
                                db_column='PERSONALE_ID',
                                blank=True, null=True)
    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_dlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_dlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_DOCENTE_LINEA_BASE'
        verbose_name_plural = _("Docente Linea Base")


class RicercaErc1(InsModAbstract):
    cod_erc1 = models.CharField(db_column='COD_ERC1', unique=True,
                                max_length=40)
    descrizione = models.TextField(db_column='DESCRIZIONE', max_length=200)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_erc1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_erc1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_ERC1'
        verbose_name_plural = _("Erc 1")

    def __str__(self):
        return '{} {}'.format(self.cod_erc1,
                              self.descrizione)


class RicercaErc2(InsModAbstract):
    cod_erc2 = models.CharField(db_column='COD_ERC2', unique=True,
                                max_length=60)
    descrizione = models.TextField(db_column='DESCRIZIONE', max_length=200)
    ricerca_erc1 = models.ForeignKey(RicercaErc1, models.DO_NOTHING,
                                     db_column='RICERCA_ERC1_ID',
                                     blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_erc2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_erc2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_ERC2'
        verbose_name_plural = _("Erc 2")

    def __str__(self):
        return '{} {}'.format(self.cod_erc2,
                              self.descrizione)


class RicercaGruppo(InsModAbstract):
    nome = models.CharField(db_column='NOME', max_length=200)
    descrizione = models.TextField(db_column='DESCRIZIONE',
                                   max_length=2000)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_GRUPPO'
        verbose_name_plural = _("Gruppo di Ricerca")
        ordering = ('nome', )

    def __str__(self):
        return '{}'.format(self.nome)


class RicercaLineaApplicata(InsModAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    ricerca_aster2 = models.ForeignKey(RicercaAster2, models.DO_NOTHING,
                                       db_column='RICERCA_ASTER2_ID')
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
                                                     max_length=1000, blank=True, null=True)
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(), related_name='user_ins_la',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(), related_name='user_mod_la',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_LINEA_APPLICATA'
        verbose_name_plural = _("Linea Applicata")
        ordering = ('ricerca_aster2', )

    def __str__(self):
        return '{} {}'.format(self.ricerca_aster2, self.descrizione)


class RicercaLineaBase(InsModAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    ricerca_erc2 = models.ForeignKey(RicercaErc2,
                                     models.DO_NOTHING,
                                     db_column='RICERCA_ERC2_ID')
    descr_pubblicaz_prog_brevetto = models.TextField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
                                                     max_length=1000,
                                                     blank=True, null=True)
    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(), related_name='user_ins_lb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(), related_name='user_mod_lb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'RICERCA_LINEA_BASE'
        verbose_name_plural = _("Linea di Base")
        ordering = ('ricerca_erc2', )

    def __str__(self):
        return '{} {}'.format(self.ricerca_erc2, self.descrizione)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class ComuniAll(models.Model):
    id_comune = models.IntegerField(db_column='ID_COMUNE', primary_key=True)
    ds_comune = models.CharField(
        db_column='DS_COMUNE', max_length=255, blank=True, null=True)
    cd_catasto = models.CharField(
        db_column='CD_CATASTO', unique=True, max_length=255, blank=True, null=True)
    cd_istat = models.CharField(
        db_column='CD_ISTAT', max_length=6, blank=True, null=True)
    dt_costituzione = models.DateTimeField(
        db_column='DT_COSTITUZIONE', blank=True, null=True)
    dt_cessazione = models.DateTimeField(
        db_column='DT_CESSAZIONE', blank=True, null=True)
    id_prov = models.IntegerField(db_column='ID_PROV', blank=True, null=True)
    cd_sigla = models.CharField(
        db_column='CD_SIGLA', max_length=2, blank=True, null=True)
    ds_prov = models.CharField(
        db_column='DS_PROV', max_length=255, blank=True, null=True)
    id_nazione = models.IntegerField(
        db_column='ID_NAZIONE', blank=True, null=True)
    cd_iso3166_1_a2_nazione = models.CharField(
        db_column='CD_ISO3166_1_A2_NAZIONE', max_length=2, blank=True, null=True)
    ds_nazione = models.CharField(
        db_column='DS_NAZIONE', max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'COMUNI_ALL'

    def __str__(self):
        return '{} {}'.format(self.id_comune, self.ds_comune)


class DidatticaCds(InsModAbstract):
    cds_id = models.IntegerField(
        db_column='CDS_ID', primary_key=True)
    cds_cod = models.CharField(
        db_column='CDS_COD', max_length=10, blank=True, null=True)
    nome_cds_it = models.CharField(
        db_column='NOME_CDS_IT', max_length=255, blank=True, null=True)
    nome_cds_eng = models.CharField(
        db_column='NOME_CDS_ENG', max_length=255, blank=True, null=True)
    rif_cod = models.CharField(
        db_column='RIF_COD', max_length=10, blank=True, null=True)
    rif_des = models.CharField(
        db_column='RIF_DES', max_length=40, blank=True, null=True)
    dip = models.ForeignKey('DidatticaDipartimento', models.DO_NOTHING,
                            db_column='DIP_ID', blank=True, null=True)
    tipo_corso_cod = models.CharField(
        db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)
    tipo_corso_des = models.CharField(
        db_column='TIPO_CORSO_DES', max_length=80, blank=True, null=True)
    durata_anni = models.IntegerField(
        db_column='DURATA_ANNI', blank=True, null=True)
    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    tipo_titit_cod = models.CharField(
        db_column='TIPO_TITIT_COD', max_length=10, blank=True, null=True)
    tipo_titit_des = models.CharField(
        db_column='TIPO_TITIT_DES', max_length=255, blank=True, null=True)
    min_cfu_comuni = models.IntegerField(
        db_column='MIN_CFU_COMUNI', blank=True, null=True)
    cfu_max_rico = models.IntegerField(
        db_column='CFU_MAX_RICO', blank=True, null=True)
    num_max_esami = models.IntegerField(
        db_column='NUM_MAX_ESAMI', blank=True, null=True)
    perc_min_ore_stu_ind = models.FloatField(
        db_column='PERC_MIN_ORE_STU_IND', blank=True, null=True)
    perc_max_ore_stu_ind = models.FloatField(
        db_column='PERC_MAX_ORE_STU_IND', blank=True, null=True)
    tipo_spec_cod = models.CharField(
        db_column='TIPO_SPEC_COD', max_length=10, blank=True, null=True)
    tipo_spec_des = models.CharField(
        db_column='TIPO_SPEC_DES', max_length=255, blank=True, null=True)
    scuola_spec_id = models.IntegerField(
        db_column='SCUOLA_SPEC_ID', blank=True, null=True)
    scuola_spec_des = models.CharField(
        db_column='SCUOLA_SPEC_DES', max_length=255, blank=True, null=True)
    cla_m_id = models.IntegerField(db_column='CLA_M_ID', blank=True, null=True)
    cla_miur_cod = models.CharField(
        db_column='CLA_MIUR_COD', max_length=10, blank=True, null=True)
    cla_miur_des = models.CharField(
        db_column='CLA_MIUR_DES', max_length=255, blank=True, null=True)
    intercla_m_id = models.IntegerField(
        db_column='INTERCLA_M_ID', blank=True, null=True)
    intercla_miur_cod = models.CharField(
        db_column='INTERCLA_MIUR_COD', max_length=10, blank=True, null=True)
    intercla_miur_des = models.CharField(
        db_column='INTERCLA_MIUR_DES', max_length=255, blank=True, null=True)
    codicione = models.CharField(
        db_column='CODICIONE', max_length=255, blank=True, null=True)
    min_diff_cfu_ord = models.IntegerField(
        db_column='MIN_DIFF_CFU_ORD', blank=True, null=True)
    sett_post_rif_flg = models.IntegerField(
        db_column='SETT_POST_RIF_FLG', blank=True, null=True)
    istat_cod = models.CharField(
        db_column='ISTAT_COD', max_length=10, blank=True, null=True)
    max_punti = models.IntegerField(
        db_column='MAX_PUNTI', blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column='UM_PESO_COD', max_length=5, blank=True, null=True)
    um_peso_des = models.CharField(
        db_column='UM_PESO_DES', max_length=40, blank=True, null=True)
    aa_att_id = models.IntegerField(
        db_column='AA_ATT_ID', blank=True, null=True)
    data_attivazione = models.DateTimeField(
        db_column='DATA_ATTIVAZIONE', blank=True, null=True)
    aa_dis_id = models.IntegerField(
        db_column='AA_DIS_ID', blank=True, null=True)
    url = models.CharField(
        db_column='URL', max_length=255, blank=True, null=True)
    cds_url_info_web = models.CharField(
        db_column='CDS_URL_INFO_WEB', max_length=255, blank=True, null=True)
    cds_vis_web_flg = models.IntegerField(
        db_column='CDS_VIS_WEB_FLG', blank=True, null=True)
    ccs_id = models.IntegerField(db_column='CCS_ID', blank=True, null=True)
    ccs_cod = models.CharField(
        db_column='CCS_COD', max_length=10, blank=True, null=True)
    ccs_des = models.CharField(
        db_column='CCS_DES', max_length=255, blank=True, null=True)
    flg_exp_seg_stu = models.IntegerField(
        db_column='FLG_EXP_SEG_STU', blank=True, null=True)
    data_exp_seg_stu = models.DateTimeField(
        db_column='DATA_EXP_SEG_STU', blank=True, null=True)
    cdsord_id = models.IntegerField(
        db_column='CDSORD_ID', unique=True, blank=True, null=True)
    cdsord_cod = models.CharField(
        db_column='CDSORD_COD', max_length=10, blank=True, null=True)
    aa_ord_id = models.IntegerField(
        db_column='AA_ORD_ID', blank=True, null=True)
    stato_cdsord_cod = models.CharField(
        db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'DIDATTICA_CDS'

    def __str__(self):
        return '{} {}'.format(self.cds_id, self.nome_cds_it)


class DidatticaCdsLingua(models.Model):
    lin_did_ord_id = models.IntegerField(
        db_column='LIN_DID_ORD_ID', primary_key=True)
    cdsord = models.ForeignKey(
        DidatticaCds, models.DO_NOTHING, to_field='cdsord_id', db_column='CDSORD_ID', blank=True, null=True)
    lingua_id = models.IntegerField(
        db_column='LINGUA_ID', blank=True, null=True)
    lingua_des_it = models.CharField(
        db_column='LINGUA_DES_IT', max_length=100, blank=True, null=True)
    iso6392_cod = models.CharField(
        db_column='ISO6392_COD', max_length=3, blank=True, null=True)
    lingua_des_eng = models.CharField(
        db_column='LINGUA_DES_ENG', max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'DIDATTICA_CDS_LINGUA'

    def __str__(self):
        return '{} {}'.format(self.lin_did_ord_id, self.lingua_des_it)


class DidatticaDipartimento(InsModAbstract):
    dip_id = models.IntegerField(db_column='DIP_ID', primary_key=True)
    dip_cod = models.CharField(
        db_column='DIP_COD', max_length=40, blank=True, null=True)
    dip_des_it = models.CharField(
        db_column='DIP_DES_IT', max_length=255, blank=True, null=True)
    dip_des_eng = models.CharField(
        db_column='DIP_DES_ENG', max_length=255, blank=True, null=True)
    dip_nome_breve = models.CharField(
        db_column='DIP_NOME_BREVE', max_length=100, blank=True, null=True)
    dip_cd_csa = models.CharField(
        db_column='DIP_CD_CSA', max_length=40, blank=True, null=True)
    miur_dip_id = models.IntegerField(
        db_column='MIUR_DIP_ID', blank=True, null=True)
    url_pubbl_off_f = models.CharField(
        db_column='URL_PUBBL_OFF_F', max_length=255, blank=True, null=True)
    dip_vis_web_flg = models.IntegerField(
        db_column='DIP_VIS_WEB_FLG', blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'DIDATTICA_DIPARTIMENTO'
        verbose_name_plural = _("Didattica Dipartimento")

    def __str__(self):
        return '{} {}'.format(self.dip_cod, self.dip_des_it)


class DidatticaRegolamento(InsModAbstract):
    regdid_id = models.IntegerField(db_column='REGDID_ID', primary_key=True)
    aa_reg_did = models.IntegerField(
        db_column='AA_REG_DID', blank=True, null=True)
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING,
                            db_column='CDS_ID', blank=True, null=True)
    stato_regdid_cod = models.CharField(
        db_column='STATO_REGDID_COD', max_length=5, blank=True, null=True)
    stato_regdid_des = models.CharField(
        db_column='STATO_REGDID_DES', max_length=40, blank=True, null=True)
    numero_piani_studio = models.IntegerField(
        db_column='NUMERO_PIANI_STUDIO', blank=True, null=True)
    anno_scelta_pds = models.IntegerField(
        db_column='ANNO_SCELTA_PDS', blank=True, null=True)
    modalita_erogazione = models.CharField(
        db_column='MODALITA_EROGAZIONE', max_length=100, blank=True, null=True)
    frequenza_obbligatoria = models.IntegerField(
        db_column='FREQUENZA_OBBLIGATORIA', blank=True, null=True)
    titolo_congiunto_cod = models.CharField(
        db_column='TITOLO_CONGIUNTO_COD', max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'DIDATTICA_REGOLAMENTO'

    def __str__(self):
        return '{} {}'.format(self.regdid_id, self.aa_reg_did)


class DidatticaTestiRegolamento(InsModAbstract):
    txt_id = models.IntegerField(db_column='TXT_ID', primary_key=True)
    regdid = models.ForeignKey(
        DidatticaRegolamento, models.DO_NOTHING, db_column='REGDID_ID')
    tipo_testo_regdid_cod = models.CharField(
        db_column='TIPO_TESTO_REGDID_COD', max_length=100)
    tipo_testo_regdid_des = models.CharField(
        db_column='TIPO_TESTO_REGDID_DES', max_length=255, blank=True, null=True)
    clob_txt_ita = models.TextField(
        db_column='CLOB_TXT_ITA', blank=True, null=True)
    clob_txt_eng = models.TextField(
        db_column='CLOB_TXT_ENG', blank=True, null=True)
    profilo = models.TextField(db_column='PROFILO', blank=True, null=True)
    profilo_eng = models.TextField(
        db_column='PROFILO_ENG', blank=True, null=True)
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)
    dt_ins_txt_clob_ita = models.DateTimeField(
        db_column='DT_INS_TXT_CLOB_ITA', blank=True, null=True)
    dt_ins_txt_clob_eng = models.DateTimeField(
        db_column='DT_INS_TXT_CLOB_ENG', blank=True, null=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'DIDATTICA_TESTI_REGOLAMENTO'

    def __str__(self):
        return '{} {}'.format(self.txt_id, self.tipo_testo_regdid_cod)


class TerritorioIt(models.Model):
    cd_catasto = models.OneToOneField(
        ComuniAll, models.DO_NOTHING, db_column='CD_CATASTO', primary_key=True)
    cd_istat = models.CharField(
        db_column='CD_ISTAT', max_length=6, blank=True, null=True)
    ds_comune = models.CharField(
        db_column='DS_COMUNE', max_length=255, blank=True, null=True)
    cd_sigla = models.CharField(
        db_column='CD_SIGLA', max_length=2, blank=True, null=True)
    ds_provincia = models.CharField(
        db_column='DS_PROVINCIA', max_length=255, blank=True, null=True)
    cd_770_regio = models.CharField(
        db_column='CD_770_REGIO', max_length=2, blank=True, null=True)
    ds_regione = models.CharField(
        db_column='DS_REGIONE', max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'TERRITORIO_IT'

    def __str__(self):
        return '{} {}'.format(self.cd_catasto, self.cd_istat)


class CdSList(models.Model):
    regdidid = models.IntegerField(db_column='RegDidId', primary_key=True)
    cdsid = models.IntegerField(db_column='CdSId', blank=True, null=True)
    academicyear = models.IntegerField(
        db_column='AcademicYear', blank=True, null=True)
    cdsnameit = models.CharField(
        db_column='CdSNameIT', max_length=255, blank=True, null=True)
    cdsnameeng = models.CharField(
        db_column='CdSNameENG', max_length=255, blank=True, null=True)
    departmentid = models.CharField(
        db_column='DepartmentId', max_length=40, blank=True, null=True)
    departmentnameit = models.CharField(
        db_column='DepartmentNameIT', max_length=255, blank=True, null=True)
    departmentnameeng = models.CharField(
        db_column='DepartmentNameENG', max_length=255, blank=True, null=True)
    coursetypeid = models.CharField(
        db_column='CourseTypeId', max_length=10, blank=True, null=True)
    coursetypename = models.CharField(
        db_column='CourseTypeName', max_length=80, blank=True, null=True)
    courseclassid = models.CharField(
        db_column='CourseClassId', max_length=10, blank=True, null=True)
    courseclassname = models.CharField(
        db_column='CourseClassName', max_length=255, blank=True, null=True)
    cdslanguageit = models.CharField(
        db_column='CdsLanguageIT', max_length=100, blank=True, null=True)
    cdslanguageeng = models.CharField(
        db_column='CdSLanguageENG', max_length=100, blank=True, null=True)
    cdsduration = models.IntegerField(
        db_column='CdSDuration', blank=True, null=True)
    cdsects = models.IntegerField(db_column='CdSECTS', blank=True, null=True)
    cdsattendance = models.IntegerField(
        db_column='CdSAttendance', blank=True, null=True)
    jointdegree = models.CharField(
        db_column='JointDegree', max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'CDSLIST'
