# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class RicercaAbstract(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS', auto_now_add=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', auto_now=True,
                                  blank=True, null=True)

    class Meta:
        abstract = True


class Personale(models.Model):
    id_ab = models.IntegerField(db_column='ID_AB')
    cd_esterno = models.CharField(db_column='CD_ESTERNO', max_length=60, blank=True, null=True)
    matricola = models.CharField(db_column='MATRICOLA', unique=True, max_length=6)
    matricola_sp = models.CharField(db_column='MATRICOLA_SP', max_length=255, blank=True, null=True)
    nome = models.CharField(db_column='NOME', max_length=100, blank=True, null=True)
    cognome = models.CharField(db_column='COGNOME', max_length=100, blank=True, null=True)
    middle_name = models.CharField(db_column='MIDDLE_NAME', max_length=100, blank=True, null=True)
    cod_fis = models.CharField(db_column='COD_FIS', unique=True, max_length=16, blank=True, null=True)
    cd_genere = models.CharField(db_column='CD_GENERE', max_length=1, blank=True, null=True)
    dt_nascita = models.DateField(db_column='DT_NASCITA', blank=True, null=True)
    id_comu_nasc = models.IntegerField(db_column='ID_COMU_NASC', blank=True, null=True)
    ds_cittstra_nasc = models.CharField(db_column='DS_CITTSTRA_NASC', max_length=255, blank=True, null=True)
    ds_comune_nasc = models.CharField(db_column='DS_COMUNE_NASC', max_length=255, blank=True, null=True)
    ds_prov_nasc = models.CharField(db_column='DS_PROV_NASC', max_length=255, blank=True, null=True)
    cd_sigla_nasc = models.CharField(db_column='CD_SIGLA_NASC', max_length=2, blank=True, null=True)
    id_nazione_nasc = models.IntegerField(db_column='ID_NAZIONE_NASC', blank=True, null=True)
    ds_nazi_nasc = models.CharField(db_column='DS_NAZI_NASC', max_length=100, blank=True, null=True)
    ds_nazi_breve_nasc = models.CharField(db_column='DS_NAZI_BREVE_NASC', max_length=20, blank=True, null=True)
    id_comu_res = models.IntegerField(db_column='ID_COMU_RES', blank=True, null=True)
    ds_comune_res = models.CharField(db_column='DS_COMUNE_RES', max_length=255, blank=True, null=True)
    cd_cap_res = models.CharField(db_column='CD_CAP_RES', max_length=5, blank=True, null=True)
    indirizzo_res = models.CharField(db_column='INDIRIZZO_RES', max_length=255, blank=True, null=True)
    num_civico_res = models.CharField(db_column='NUM_CIVICO_RES', max_length=15, blank=True, null=True)
    cd_sigla_res = models.CharField(db_column='CD_SIGLA_RES', max_length=2, blank=True, null=True)
    id_comu_dom = models.IntegerField(db_column='ID_COMU_DOM', blank=True, null=True)
    ds_comune_dom = models.CharField(db_column='DS_COMUNE_DOM', max_length=255, blank=True, null=True)
    cd_cap_dom = models.CharField(db_column='CD_CAP_DOM', max_length=5, blank=True, null=True)
    indirizzo_dom = models.CharField(db_column='INDIRIZZO_DOM', max_length=255, blank=True, null=True)
    num_civico_dom = models.CharField(db_column='NUM_CIVICO_DOM', max_length=15, blank=True, null=True)
    cd_sigla_dom = models.CharField(db_column='CD_SIGLA_DOM', max_length=2, blank=True, null=True)
    cd_comparto = models.CharField(db_column='CD_COMPARTO', max_length=1)
    ds_comparto = models.CharField(db_column='DS_COMPARTO', max_length=40, blank=True, null=True)
    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4)
    ds_ruolo = models.CharField(db_column='DS_RUOLO', max_length=40, blank=True, null=True)
    ds_ruolo_locale = models.CharField(db_column='DS_RUOLO_LOCALE', max_length=40, blank=True, null=True)
    peso_ruolo = models.DecimalField(db_column='PESO_RUOLO', max_digits=10, decimal_places=0, blank=True, null=True)
    dt_rap_ini = models.DateField(db_column='DT_RAP_INI', blank=True, null=True)
    dt_rap_fin = models.DateField(db_column='DT_RAP_FIN', blank=True, null=True)
    cd_ssd = models.CharField(db_column='CD_SSD', max_length=12, blank=True, null=True)
    ds_ssd = models.CharField(db_column='DS_SSD', max_length=100, blank=True, null=True)
    cd_fac = models.CharField(db_column='CD_FAC', max_length=10, blank=True, null=True)
    ds_fac = models.CharField(db_column='DS_FAC', max_length=255, blank=True, null=True)
    aff_org = models.CharField(db_column='AFF_ORG', max_length=6, blank=True, null=True)
    ds_aff_org = models.CharField(db_column='DS_AFF_ORG', max_length=255, blank=True, null=True)
    ds_aff_org_breve = models.CharField(db_column='DS_AFF_ORG_BREVE', max_length=50, blank=True, null=True)
    aff_org2 = models.CharField(db_column='AFF_ORG2', max_length=6, blank=True, null=True)
    ds_aff_org2 = models.CharField(db_column='DS_AFF_ORG2', max_length=255, blank=True, null=True)
    ds_aff_org2_breve = models.CharField(db_column='DS_AFF_ORG2_BREVE', max_length=50, blank=True, null=True)
    aff_org3 = models.CharField(db_column='AFF_ORG3', max_length=6, blank=True, null=True)
    ds_aff_org3 = models.CharField(db_column='DS_AFF_ORG3', max_length=255, blank=True, null=True)
    ds_aff_org3_breve = models.CharField(db_column='DS_AFF_ORG3_BREVE', max_length=50, blank=True, null=True)
    aff_org4 = models.CharField(db_column='AFF_ORG4', max_length=6, blank=True, null=True)
    ds_aff_org4 = models.CharField(db_column='DS_AFF_ORG4', max_length=255, blank=True, null=True)
    ds_aff_org4_breve = models.CharField(db_column='DS_AFF_ORG4_BREVE', max_length=50, blank=True, null=True)
    sede = models.CharField(db_column='SEDE', max_length=6, blank=True, null=True)
    ds_sede = models.CharField(db_column='DS_SEDE', max_length=255, blank=True, null=True)
    ds_sede_breve = models.CharField(db_column='DS_SEDE_BREVE', max_length=50, blank=True, null=True)
    profilo = models.CharField(db_column='PROFILO', max_length=11, blank=True, null=True)
    ds_profilo = models.CharField(db_column='DS_PROFILO', max_length=100, blank=True, null=True)
    ds_profilo_breve = models.CharField(db_column='DS_PROFILO_BREVE', max_length=50, blank=True, null=True)
    cd_ateneo_corr = models.CharField(db_column='CD_ATENEO_CORR', max_length=10, blank=True, null=True)
    ds_ateneo_corr = models.CharField(db_column='DS_ATENEO_CORR', max_length=255, blank=True, null=True)
    dt_ini_rap_univ = models.DateField(db_column='DT_INI_RAP_UNIV', blank=True, null=True)
    dt_fin_rap_univ = models.DateField(db_column='DT_FIN_RAP_UNIV', blank=True, null=True)
    telrif = models.CharField(db_column='TELRIF', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=255, blank=True, null=True)
    urlcv = models.CharField(db_column='URLCV', max_length=255, blank=True, null=True)
    fl_docente = models.PositiveIntegerField(db_column='FL_DOCENTE', blank=True, null=True)
    cd_anagrafico = models.CharField(db_column='CD_ANAGRAFICO', max_length=20, blank=True, null=True)
    inquadr = models.CharField(db_column='INQUADR', max_length=50, blank=True, null=True)
    badge = models.CharField(db_column='BADGE', max_length=255, blank=True, null=True)
    tempo = models.CharField(db_column='TEMPO', max_length=1, blank=True, null=True)
    id_contratto = models.IntegerField(db_column='ID_CONTRATTO', blank=True, null=True)
    flg_cessato = models.IntegerField(db_column='FLG_CESSATO', blank=True, null=True)
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


class RicercaAster1(RicercaAbstract):
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


class RicercaAster2(RicercaAbstract):
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
                              

class RicercaDocenteGruppo(RicercaAbstract):
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


class RicercaDocenteLineaApplicata(RicercaAbstract):
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


class RicercaDocenteLineaBase(RicercaAbstract):
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


class RicercaErc1(RicercaAbstract):
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


class RicercaErc2(RicercaAbstract):
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


class RicercaGruppo(RicercaAbstract):
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


class RicercaLineaApplicata(RicercaAbstract):
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
    

class RicercaLineaBase(RicercaAbstract):
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
