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


class Docente(RicercaAbstract):
    nome = models.CharField(db_column='NOME', max_length=200)
    cognome = models.CharField(db_column='COGNOME', max_length=200)
    cod_fis = models.CharField(_('Codice Fiscale'), db_column='COD_FIS',
                               unique=True, max_length=16)
    matricola = models.CharField(db_column='MATRICOLA',
                                 max_length=100, blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_doc',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_doc',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        db_table = 'DOCENTE'
        verbose_name_plural = _("Docente")

    def __str__(self):
        return '{} {}'.format(self.nome, self.cognome)


class RicercaAster1(RicercaAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE',
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


class RicercaDocenteGruppo(RicercaAbstract):
    ricerca_gruppo = models.ForeignKey('RicercaGruppo',
                                       models.DO_NOTHING,
                                       db_column='RICERCA_GRUPPO_ID')
    docente = models.ForeignKey(Docente, models.DO_NOTHING,
                                db_column='DOCENTE_ID', blank=True, null=True)
    dt_inizio = models.DateTimeField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateTimeField(db_column='DT_FINE', blank=True, null=True)
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


class RicercaDocenteLineaApplicata(RicercaAbstract):
    ricerca_linea_applicata = models.ForeignKey('RicercaLineaApplicata',
                                                models.DO_NOTHING,
                                                db_column='RICERCA_LINEA_APPLICATA_ID',
                                                blank=True, null=True)
    docente = models.ForeignKey(Docente, models.DO_NOTHING,
                                db_column='DOCENTE_ID', blank=True, null=True)
    dt_inizio = models.DateTimeField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateTimeField(db_column='DT_FINE', blank=True, null=True)
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
    docente = models.ForeignKey(Docente, models.DO_NOTHING,
                                db_column='DOCENTE_ID',
                                blank=True, null=True)
    dt_inizio = models.DateTimeField(db_column='DT_INIZIO', blank=True, null=True)
    dt_fine = models.DateTimeField(db_column='DT_FINE', blank=True, null=True)
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
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)
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


class RicercaErc2(RicercaAbstract):
    cod_erc2 = models.CharField(db_column='COD_ERC2', unique=True,
                                max_length=60)
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)
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


class RicercaGruppo(RicercaAbstract):
    nome = models.CharField(db_column='NOME', max_length=200)
    descrizione = models.CharField(db_column='DESCRIZIONE',
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


class RicercaLineaApplicata(RicercaAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    ricerca_aster2 = models.ForeignKey(RicercaAster2, models.DO_NOTHING,
                                       db_column='RICERCA_ASTER2_ID')
    descr_pubblicaz_prog_brevetto = models.CharField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
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


class RicercaLineaBase(RicercaAbstract):
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    ricerca_erc2 = models.ForeignKey(RicercaErc2,
                                     models.DO_NOTHING,
                                     db_column='RICERCA_ERC2_ID')
    descr_pubblicaz_prog_brevetto = models.CharField(db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
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
