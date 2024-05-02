from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from organizational_area.models import OrganizationalStructureOfficeEmployee

from .validators import *
from . settings import *


def patents_media_path(instance, filename): # pragma: no cover
    return f'portale/brevetti/loghi/{filename}'

def laboratories_media_path(instance, filename): # pragma: no cover
    return f'portale/laboratori/loghi/{filename}'

def cds_websites_exstudents_media_path(instance, filename): # pragma: no cover
    return f'portale/sito_web_cds/ex_studenti/{filename}'

def companies_media_path(instance, filename): # pragma: no cover
    return f'portale/spinoff-startup/loghi/{filename}'

def teacher_photo_media_path(instance, filename): # pragma: no cover
    return f'portale/docenti_pta/foto/{filename}'

def teacher_cv_en_media_path(instance, filename): # pragma: no cover
    return f'portale/docenti_pta/cv_en/{filename}'

def teacher_cv_ita_media_path(instance, filename): # pragma: no cover
    return f'portale/docenti_pta/cv_ita/{filename}'

def cds_manifesto_media_path(instance, filename): # pragma: no cover
    return f'portale/cds/manifesti/{instance.regdid_id.aa_reg_did}/{filename}'

def cds_regolamento_media_path(instance, filename): # pragma: no cover
    return f'portale/cds/regolamenti/{instance.regdid_id.aa_reg_did}/{filename}'

def cds_ordinamento_media_path(instance, filename): # pragma: no cover
    return f'portale/cds/ordinamenti/{instance.regdid_id.aa_reg_did}/{filename}'

def cds_multimedia_media_path(instance, filename): # pragma: no cover
    return f'portale/cds_media_brochure/{filename}'


class PermissionsModAbstract(models.Model):
    
    @classmethod
    def get_offices_names(cls, **kwargs):
        '''
        Returns a tuple containing the names of the relevant offices
        for this model
        '''
        raise NotImplementedError()
    
    @classmethod
    def user_has_offices(cls, user, **kwargs):
        '''
        Returns whether or not the user is part of any office related to the model,
        without performing any additional checks
        '''
        return cls._get_all_user_offices(user, **kwargs).exists()
    
    @classmethod
    def _get_all_user_offices(cls, user, **kwargs):
        '''
        Returns a queryset containing all the active offices a user is part of,
        among the ones related to the model, without performing any additional checks
        '''  
        return OrganizationalStructureOfficeEmployee.objects.filter(employee=user,
                                                                    office__is_active=True,
                                                                    office__name__in=cls.get_offices_names(),
                                                                    office__organizational_structure__is_active=True)
        
    
    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        '''
        Performs advanced checks on an office record: all_user_offices.get(office__name=office_name)
        
        example:
            check if the given office's unique_code mathes the department code related to the object            
        '''
        return True
    
    def _check_access_permission(self, user_offices_names, **kwargs):
        '''
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to access the object 
        
        default: the user is part of at least one office related to the model 
        '''
        return len(user_offices_names) > 0
    
    def _check_edit_permission(self, user_offices_names, **kwargs):
        '''
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to edit the object 
        '''
        return False
    
    def _check_lock_permission(self, user_offices_names, **kwargs):
        '''
        Given the offices names the user's already been checked to be part of,
        returns whether or not they have the permission to acquire a lock on the object 
        '''
        return False

    def get_user_offices_names(self, user, **kwargs):
        '''
        Returns a tuple containing the offices names a user is part of,
        among the ones returned by get_offices_names(),
        that matches all the conditions of _is_valid_office()
        '''
        try:
            self._all_user_offices = self._all_user_offices 
        except AttributeError:
            self._all_user_offices = {}
        
        # avoid querying the same offices for the same user multiple times on the same object
        if not user in self._all_user_offices:
            self._all_user_offices[user] = self._get_all_user_offices(user, **kwargs)
        return tuple(user_office.office.name for user_office in self._all_user_offices[user]
                     if self._is_valid_office(user_office.office.name, self._all_user_offices[user], **kwargs))
        
    
    def get_user_permissions_and_offices(self, user, **kwargs):
        '''
        Returns a dict containing whether or not the user possesses 
        the following permissions: access, edit, lock,
        together with offices: user's offices names
        '''
        user_offices_names = self.get_user_offices_names(user, **kwargs)
        return {
            'permissions': {
                'access': user.is_superuser or self._check_access_permission(user_offices_names, **kwargs),
                'edit': user.is_superuser or self._check_edit_permission(user_offices_names, **kwargs),
                'lock': user.is_superuser or self._check_lock_permission(user_offices_names, **kwargs)
            },
            'offices': user_offices_names
        }
        
    class Meta:
        abstract = True


class InsModAbstract(models.Model):
    dt_ins = models.DateTimeField(db_column='DT_INS', auto_now_add=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', auto_now=True,
                                  blank=True, null=True)

    class Meta:
        abstract = True


class VisibileModAbstract(models.Model):
    visibile = models.BooleanField(db_column='VISIBILE', default=False)

    class Meta:
        abstract = True


class ComuniAll(models.Model):

    id_comune = models.IntegerField(db_column='ID_COMUNE', primary_key=True)
    ds_comune = models.CharField(
        db_column='DS_COMUNE',
        max_length=255,
        blank=True,
        null=True)
    cd_catasto = models.CharField(
        db_column='CD_CATASTO',
        unique=True,
        max_length=255,
        blank=True,
        null=True)

    cd_istat = models.CharField(
        db_column='CD_ISTAT',
        max_length=6,
        blank=True,
        null=True)
    dt_costituzione = models.DateTimeField(
        db_column='DT_COSTITUZIONE', blank=True, null=True)

    dt_cessazione = models.DateTimeField(
        db_column='DT_CESSAZIONE', blank=True, null=True)

    id_prov = models.IntegerField(db_column='ID_PROV', blank=True, null=True)

    cd_sigla = models.CharField(
        db_column='CD_SIGLA',
        max_length=2,
        blank=True,
        null=True)

    ds_prov = models.CharField(
        db_column='DS_PROV',
        max_length=255,
        blank=True,
        null=True)

    id_nazione = models.IntegerField(
        db_column='ID_NAZIONE', blank=True, null=True)
    cd_iso3166_1_a2_nazione = models.CharField(
        db_column='CD_ISO3166_1_A2_NAZIONE',
        max_length=2,
        blank=True,
        null=True)
    ds_nazione = models.CharField(
        db_column='DS_NAZIONE',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'COMUNI_ALL'


class DidatticaSsd(models.Model):
    ssd_id = models.CharField(db_column='SSD_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    ssd_des = models.CharField(db_column='SSD_DES', max_length=2000)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_SSD'

    def __str__(self):
        return f'{self.ssd_id} {self.ssd_des}'


class DidatticaAttivitaFormativa(models.Model):
    af_id = models.IntegerField(db_column='AF_ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='CDS_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_id = models.IntegerField(db_column='CDSORD_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    regdid_cod = models.CharField(db_column='REGDID_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    stato_regdid_cod = models.CharField(db_column='STATO_REGDID_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stato_appr_regdid_cod = models.CharField(db_column='STATO_APPR_REGDID_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey('DidatticaPdsRegolamento', models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    attinenza_cod = models.CharField(db_column='ATTINENZA_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_id = models.IntegerField(db_column='TIPO_COMP_AF_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    des_tipo_comp_af = models.CharField(db_column='DES_TIPO_COMP_AF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.IntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_des_eng = models.CharField(db_column='AF_GEN_DES_ENG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    lista_anni_corso = models.CharField(db_column='LISTA_ANNI_CORSO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_regdid_id = models.IntegerField(db_column='AF_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sett_des = models.CharField(db_column='SETT_DES', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    tipo_af_intercla_cod = models.CharField(db_column='TIPO_AF_INTERCLA_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_af_intercla_des = models.CharField(db_column='TIPO_AF_INTERCLA_DES', max_length=200, blank=True, null=True)  # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    freq_obblig_flg = models.IntegerField(db_column='FREQ_OBBLIG_FLG', blank=True, null=True)  # Field name made lowercase.
    ore_min_freq = models.IntegerField(db_column='ORE_MIN_FREQ', blank=True, null=True)  # Field name made lowercase.
    ore_att_front = models.IntegerField(db_column='ORE_ATT_FRONT', blank=True, null=True)  # Field name made lowercase.
    num_max_reit = models.IntegerField(db_column='NUM_MAX_REIT', blank=True, null=True)  # Field name made lowercase.
    libera_flg = models.IntegerField(db_column='LIBERA_FLG', blank=True, null=True)  # Field name made lowercase.
    scelta_mod_flg = models.IntegerField(db_column='SCELTA_MOD_FLG', blank=True, null=True)  # Field name made lowercase.
    tipo_esa_cod = models.CharField(db_column='TIPO_ESA_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_esa_des = models.CharField(db_column='TIPO_ESA_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_val_cod = models.CharField(db_column='TIPO_VAL_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_val_des = models.CharField(db_column='TIPO_VAL_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_ins_des = models.CharField(db_column='TIPO_INS_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    serale_flg = models.IntegerField(db_column='SERALE_FLG', blank=True, null=True)  # Field name made lowercase.
    no_media_flg = models.IntegerField(db_column='NO_MEDIA_FLG', blank=True, null=True)  # Field name made lowercase.
    sostegno_flg = models.IntegerField(db_column='SOSTEGNO_FLG', blank=True, null=True)  # Field name made lowercase.
    nota = models.CharField(db_column='NOTA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    af_pdr_id = models.IntegerField(db_column='AF_PDR_ID', blank=True, null=True)  # Field name made lowercase.
    af_radice_id = models.IntegerField(db_column='AF_RADICE_ID', blank=True, null=True)  # Field name made lowercase.
    num_liv_albero = models.IntegerField(db_column='NUM_LIV_ALBERO', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    data_inizio = models.DateTimeField(db_column='DATA_INIZIO', blank=True, null=True)  # Field name made lowercase.
    data_fine = models.DateTimeField(db_column='DATA_FINE', blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    matricola_resp_did = models.ForeignKey('Personale', models.DO_NOTHING, db_column='MATRICOLA_RESP_DID', blank=True, null=True, to_field='matricola')  # Field name made lowercase.
    cod_fis_resp_did = models.CharField(db_column='COD_FIS_RESP_DID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(db_column='RUOLO_RESP_DID_COD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    url_sito_web = models.URLField(db_column='URL_SITO_WEB', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_lin_did_af = models.CharField(db_column='LISTA_LIN_DID_AF', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_mod_did_af = models.CharField(db_column='LISTA_MOD_DID_AF', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lista_taf_set_cfu = models.CharField(db_column='LISTA_TAF_SET_CFU', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    mutuata_flg = models.IntegerField(db_column='MUTUATA_FLG', blank=True, null=True)  # Field name made lowercase.
    af_master_id = models.IntegerField(db_column='AF_MASTER_ID', blank=True, null=True)  # Field name made lowercase.
    num_af_figlie = models.IntegerField(db_column='NUM_AF_FIGLIE', blank=True, null=True)  # Field name made lowercase.
    num_af_foglie = models.IntegerField(db_column='NUM_AF_FOGLIE', blank=True, null=True)  # Field name made lowercase.
    non_erogabile_flg = models.PositiveIntegerField(db_column='NON_EROGABILE_FLG', blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_cod = models.CharField(db_column='FAT_PART_STU_COD', max_length=40, blank=True, null=True)  # Field name made lowercase.
    fat_part_stu_des = models.CharField(db_column='FAT_PART_STU_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.
    part_stu_id = models.IntegerField(db_column='PART_STU_ID', blank=True, null=True)  # Field name made lowercase.
    part_stu_cod = models.CharField(db_column='PART_STU_COD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    part_stu_des = models.CharField(db_column='PART_STU_DES', max_length=500, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA'
        ordering = ('ciclo_des',)

    def __str__(self): # pragma: no cover
        return '{}'.format(self.af_id)

    def checkIfMainCourse(self):
        return self.af_id == self.af_radice_id


class DidatticaAttivitaFormativaEsse3(models.Model):
    ad_id_esse3 = models.IntegerField(db_column='AD_ID_ESSE3', primary_key=True)  # Field name made lowercase.
    ad_cod = models.CharField(db_column='AD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ad_des = models.CharField(db_column='AD_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_entita = models.IntegerField(db_column='TIPO_ENTITA', blank=True, null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    data_ins = models.DateTimeField(db_column='DATA_INS', blank=True, null=True)  # Field name made lowercase.
    data_mod = models.DateTimeField(db_column='DATA_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_ESSE3'


class DidatticaAttivitaFormativaModalita(models.Model):
    mod_did_af_id = models.IntegerField(db_column='MOD_DID_AF_ID', primary_key=True)  # Field name made lowercase.
    af = models.ForeignKey(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID')  # Field name made lowercase.
    mod_did_cod = models.CharField(db_column='MOD_DID_COD', max_length=40)  # Field name made lowercase.
    mod_did_des = models.CharField(db_column='MOD_DID_DES', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_ATTIVITA_FORMATIVA_MODALITA'


class DidatticaCds(InsModAbstract):

    cds_id = models.IntegerField(db_column='CDS_ID', primary_key=True)

    cds_cod = models.CharField(
        db_column='CDS_COD',
        max_length=10,
        blank=True,
        null=True)
    nome_cds_it = models.CharField(
        db_column='NOME_CDS_IT',
        max_length=255,
        blank=True,
        null=True)
    nome_cds_eng = models.CharField(
        db_column='NOME_CDS_ENG',
        max_length=255,
        blank=True,
        null=True)

    rif_cod = models.CharField(
        db_column='RIF_COD',
        max_length=10,
        blank=True,
        null=True)

    rif_des = models.CharField(
        db_column='RIF_DES',
        max_length=40,
        blank=True,
        null=True)
    dip = models.ForeignKey(
        'DidatticaDipartimento',
        models.DO_NOTHING,
        db_column='DIP_ID',
        blank=True,
        null=True)
    tipo_corso_cod = models.CharField(
        db_column='TIPO_CORSO_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_corso_des = models.CharField(
        db_column='TIPO_CORSO_DES',
        max_length=80,
        blank=True,
        null=True)

    durata_anni = models.IntegerField(
        db_column='DURATA_ANNI', blank=True, null=True)

    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    tipo_titit_cod = models.CharField(
        db_column='TIPO_TITIT_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_titit_des = models.CharField(
        db_column='TIPO_TITIT_DES',
        max_length=255,
        blank=True,
        null=True)
    min_cfu_comuni = models.IntegerField(
        db_column='MIN_CFU_COMUNI', blank=True, null=True)

    cfu_max_rico = models.IntegerField(
        db_column='CFU_MAX_RICO', blank=True, null=True)

    num_max_esami = models.IntegerField(
        db_column='NUM_MAX_ESAMI', blank=True, null=True)
    perc_min_ore_stu_ind = models.FloatField(
        db_column='PERC_MIN_ORE_STU_IND',
        blank=True,
        null=True)
    perc_max_ore_stu_ind = models.FloatField(
        db_column='PERC_MAX_ORE_STU_IND',
        blank=True,
        null=True)
    tipo_spec_cod = models.CharField(
        db_column='TIPO_SPEC_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_spec_des = models.CharField(
        db_column='TIPO_SPEC_DES',
        max_length=255,
        blank=True,
        null=True)
    scuola_spec_id = models.IntegerField(
        db_column='SCUOLA_SPEC_ID', blank=True, null=True)
    scuola_spec_des = models.CharField(
        db_column='SCUOLA_SPEC_DES',
        max_length=255,
        blank=True,
        null=True)

    cla_m_id = models.IntegerField(db_column='CLA_M_ID', blank=True, null=True)
    cla_miur_cod = models.CharField(
        db_column='CLA_MIUR_COD',
        max_length=10,
        blank=True,
        null=True)
    cla_miur_des = models.CharField(
        db_column='CLA_MIUR_DES',
        max_length=255,
        blank=True,
        null=True)

    intercla_m_id = models.IntegerField(
        db_column='INTERCLA_M_ID', blank=True, null=True)
    intercla_miur_cod = models.CharField(
        db_column='INTERCLA_MIUR_COD',
        max_length=10,
        blank=True,
        null=True)
    intercla_miur_des = models.CharField(
        db_column='INTERCLA_MIUR_DES',
        max_length=255,
        blank=True,
        null=True)
    codicione = models.CharField(
        db_column='CODICIONE',
        max_length=255,
        blank=True,
        null=True)
    min_diff_cfu_ord = models.IntegerField(
        db_column='MIN_DIFF_CFU_ORD', blank=True, null=True)
    sett_post_rif_flg = models.IntegerField(
        db_column='SETT_POST_RIF_FLG', blank=True, null=True)
    istat_cod = models.CharField(
        db_column='ISTAT_COD',
        max_length=10,
        blank=True,
        null=True)

    max_punti = models.IntegerField(
        db_column='MAX_PUNTI', blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column='UM_PESO_COD',
        max_length=5,
        blank=True,
        null=True)
    um_peso_des = models.CharField(
        db_column='UM_PESO_DES',
        max_length=40,
        blank=True,
        null=True)

    aa_att_id = models.IntegerField(
        db_column='AA_ATT_ID', blank=True, null=True)
    data_attivazione = models.DateTimeField(
        db_column='DATA_ATTIVAZIONE', blank=True, null=True)

    aa_dis_id = models.IntegerField(
        db_column='AA_DIS_ID', blank=True, null=True)

    url = models.URLField(
        db_column='URL',
        max_length=255,
        blank=True,
        null=True)
    cds_url_info_web = models.URLField(
        db_column='CDS_URL_INFO_WEB',
        max_length=255,
        blank=True,
        null=True)
    cds_vis_web_flg = models.IntegerField(
        db_column='CDS_VIS_WEB_FLG', blank=True, null=True)

    ccs_id = models.IntegerField(db_column='CCS_ID', blank=True, null=True)

    ccs_cod = models.CharField(
        db_column='CCS_COD',
        max_length=10,
        blank=True,
        null=True)

    ccs_des = models.CharField(
        db_column='CCS_DES',
        max_length=255,
        blank=True,
        null=True)
    flg_exp_seg_stu = models.IntegerField(
        db_column='FLG_EXP_SEG_STU', blank=True, null=True)
    data_exp_seg_stu = models.DateTimeField(
        db_column='DATA_EXP_SEG_STU', blank=True, null=True)
    cdsord_id = models.IntegerField(
        db_column='CDSORD_ID',
        unique=True,
        blank=True,
        null=True)
    cdsord_cod = models.CharField(
        db_column='CDSORD_COD',
        max_length=10,
        blank=True,
        null=True)

    aa_ord_id = models.IntegerField(
        db_column='AA_ORD_ID', blank=True, null=True)
    stato_cdsord_cod = models.CharField(
        db_column='STATO_CDSORD_COD',
        max_length=5,
        blank=True,
        null=True)
    # Field name made lowercase.
    area_cds = models.CharField(
        db_column='AREA_CDS',
        max_length=1000,
        blank=True,
        null=True)
    area_cds_en = models.CharField(db_column='AREA_CDS_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.cds_id, self.nome_cds_it)


class DidatticaCdsEsse3(models.Model):
    dip_id_esse3 = models.IntegerField(db_column='DIP_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    dip_cod = models.CharField(db_column='DIP_COD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cds_id_esse3 = models.IntegerField(db_column='CDS_ID_ESSE3', primary_key=True)  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nome_cds_it = models.CharField(db_column='NOME_CDS_IT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rif_cod = models.CharField(db_column='RIF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rif_des = models.CharField(db_column='RIF_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    durata_anni = models.IntegerField(db_column='DURATA_ANNI', blank=True, null=True)  # Field name made lowercase.
    valore_min = models.IntegerField(db_column='VALORE_MIN', blank=True, null=True)  # Field name made lowercase.
    tipo_titit_cod = models.CharField(db_column='TIPO_TITIT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_titit_des = models.CharField(db_column='TIPO_TITIT_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_spec_cod = models.CharField(db_column='TIPO_SPEC_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_spec_des = models.CharField(db_column='TIPO_SPEC_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    istat_cod = models.CharField(db_column='ISTAT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    max_punti = models.IntegerField(db_column='MAX_PUNTI', blank=True, null=True)  # Field name made lowercase.
    um_peso_cod = models.CharField(db_column='UM_PESO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    um_peso_des = models.CharField(db_column='UM_PESO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    aa_att_id = models.IntegerField(db_column='AA_ATT_ID', blank=True, null=True)  # Field name made lowercase.
    aa_dis_id = models.IntegerField(db_column='AA_DIS_ID', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    cds_url_info_web = models.CharField(db_column='CDS_URL_INFO_WEB', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    cds_vis_web_flg = models.IntegerField(db_column='CDS_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    cdsord_id_esse3 = models.IntegerField(db_column='CDSORD_ID_ESSE3', blank=True, null=True)  # Field name made lowercase.
    cdsord_cod = models.CharField(db_column='CDSORD_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID', blank=True, null=True)  # Field name made lowercase.
    cdsord_des = models.CharField(db_column='CDSORD_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stato_cdsord_cod = models.CharField(db_column='STATO_CDSORD_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_ESSE3'



class DidatticaCdsPeriodi(models.Model):
    ciclo_id = models.IntegerField(db_column='CICLO_ID', primary_key=True)  # Field name made lowercase.
    aa_id = models.IntegerField(db_column='AA_ID')  # Field name made lowercase.
    cds_id = models.IntegerField(db_column='CDS_ID')  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=10)  # Field name made lowercase.
    rag_tipi_ciclo_cod = models.CharField(db_column='RAG_TIPI_CICLO_COD', max_length=5)  # Field name made lowercase.
    rag_tipi_ciclo_des = models.CharField(db_column='RAG_TIPI_CICLO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5)  # Field name made lowercase.
    tipo_ciclo_des = models.CharField(db_column='TIPO_CICLO_DES', max_length=40)  # Field name made lowercase.
    tipo_ciclo_des_eng = models.CharField(db_column='TIPO_CICLO_DES_ENG', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    org_did_sua_cod = models.IntegerField(db_column='ORG_DID_SUA_COD', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40)  # Field name made lowercase.
    data_inizio = models.DateField(db_column='DATA_INIZIO')  # Field name made lowercase.
    data_fine = models.DateField(db_column='DATA_FINE')  # Field name made lowercase.
    durata = models.DecimalField(db_column='DURATA', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    csa_cod = models.CharField(db_column='CSA_COD', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_PERIODI'


class DidatticaCdsAltriDatiUfficio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID')  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE')  # Field name made lowercase.
    nome_ufficio = models.CharField(db_column='NOME_UFFICIO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    matricola_riferimento = models.ForeignKey('Personale', models.SET_NULL, db_column='MATRICOLA_RIFERIMENTO', blank=True, null=True, to_field='matricola')  # Field name made lowercase.
    nome_origine_riferimento = models.CharField(db_column='NOME_ORIGINE_RIFERIMENTO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    edificio = models.CharField(db_column='EDIFICIO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    piano = models.CharField(db_column='PIANO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    orari = models.CharField(db_column='ORARI', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    sportello_online = models.CharField(db_column='SPORTELLO_ONLINE', max_length=2000, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_ALTRI_DATI_UFFICIO'
        ordering = ('ordine',)
        # unique_together = (('cds', 'ordine'),)


class DidatticaCdsLingua(models.Model):

    lin_did_ord_id = models.IntegerField(
        db_column='LIN_DID_ORD_ID', primary_key=True)
    cdsord = models.ForeignKey(
        DidatticaCds,
        models.DO_NOTHING,
        db_column='CDSORD_ID',
        blank=True,
        null=True,
        to_field='cdsord_id',
        related_name='didatticacdslingua')

    lingua_id = models.IntegerField(
        db_column='LINGUA_ID', blank=True, null=True)
    lingua_des_it = models.CharField(
        db_column='LINGUA_DES_IT',
        max_length=100,
        blank=True,
        null=True)
    iso6392_cod = models.CharField(
        db_column='ISO6392_COD',
        max_length=3,
        blank=True,
        null=True)
    lingua_des_eng = models.CharField(
        db_column='LINGUA_DES_ENG',
        max_length=100,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_LINGUA'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.lin_did_ord_id, self.lingua_des_it)


class DidatticaCopertura(InsModAbstract):

    # Field name made lowercase.
    coper_id = models.IntegerField(db_column='COPER_ID', primary_key=True)
    # Field name made lowercase.
    af = models.ForeignKey(
        DidatticaAttivitaFormativa,
        models.DO_NOTHING,
        db_column='AF_ID',
        blank=True,
        null=True)
    # Field name made lowercase.
    personale = models.ForeignKey(
        'Personale',
        models.DO_NOTHING,
        db_column='PERSONALE_ID',
        blank=True,
        null=True)
    # Field name made lowercase.
    af_gen_id = models.IntegerField(
        db_column='AF_GEN_ID', blank=True, null=True)
    # Field name made lowercase.
    af_gen_cod = models.CharField(
        db_column='AF_GEN_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    af_gen_des = models.CharField(
        db_column='AF_GEN_DES',
        max_length=500,
        blank=True,
        null=True)
    # Field name made lowercase.
    aa_off_id = models.IntegerField(
        db_column='AA_OFF_ID', blank=True, null=True)
    # Field name made lowercase.
    cds_id = models.IntegerField(db_column='CDS_ID', blank=True, null=True)
    # Field name made lowercase.
    cds_cod = models.CharField(
        db_column='CDS_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    cdsord_id = models.IntegerField(
        db_column='CDSORD_ID', blank=True, null=True)
    # Field name made lowercase.
    cdsord_cod = models.CharField(
        db_column='CDSORD_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    aa_ord_id = models.IntegerField(
        db_column='AA_ORD_ID', blank=True, null=True)
    # Field name made lowercase.
    regdid_id = models.IntegerField(
        db_column='REGDID_ID', blank=True, null=True)
    # Field name made lowercase.
    regdid_cod = models.CharField(
        db_column='REGDID_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    aa_regdid_id = models.IntegerField(
        db_column='AA_REGDID_ID', blank=True, null=True)
    # Field name made lowercase.
    pds_regdid_id = models.IntegerField(
        db_column='PDS_REGDID_ID', blank=True, null=True)
    # Field name made lowercase.
    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    pds_des = models.CharField(
        db_column='PDS_DES',
        max_length=500,
        blank=True,
        null=True)
    # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)
    # Field name made lowercase.
    stato_of_cod = models.CharField(
        db_column='STATO_OF_COD',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(
        db_column='TIPO_COMP_AF_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    af_gen_des_eng = models.CharField(
        db_column='AF_GEN_DES_ENG',
        max_length=500,
        blank=True,
        null=True)
    # Field name made lowercase.
    anno_corso = models.IntegerField(
        db_column='ANNO_CORSO', blank=True, null=True)
    # Field name made lowercase.
    sett_cod = models.CharField(
        db_column='SETT_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    sett_des = models.CharField(
        db_column='SETT_DES',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    tipo_af_cod = models.CharField(
        db_column='TIPO_AF_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    tipo_af_des = models.CharField(
        db_column='TIPO_AF_DES',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)
    # Field name made lowercase.
    ambito_des = models.CharField(
        db_column='AMBITO_DES',
        max_length=500,
        blank=True,
        null=True)
    # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)
    # Field name made lowercase.
    um_peso_cod = models.CharField(
        db_column='UM_PESO_COD',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    ore_att_front = models.IntegerField(
        db_column='ORE_ATT_FRONT', blank=True, null=True)
    # Field name made lowercase.
    tipo_ins_cod = models.CharField(
        db_column='TIPO_INS_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    nota = models.TextField(db_column='NOTA', blank=True, null=True)
    # Field name made lowercase.
    af_radice_id = models.IntegerField(
        db_column='AF_RADICE_ID', blank=True, null=True)
    # Field name made lowercase.
    ciclo_des = models.CharField(
        db_column='CICLO_DES',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(
        db_column='TIPO_CICLO_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    des_tipo_ciclo = models.CharField(
        db_column='DES_TIPO_CICLO',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    matricola_resp_did = models.CharField(
        db_column='MATRICOLA_RESP_DID',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    cod_fis_resp_did = models.CharField(
        db_column='COD_FIS_RESP_DID',
        max_length=16,
        blank=True,
        null=True)
    # Field name made lowercase.
    ruolo_resp_did_cod = models.CharField(
        db_column='RUOLO_RESP_DID_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    cognome_titolare = models.CharField(
        db_column='COGNOME_TITOLARE',
        max_length=200,
        blank=True,
        null=True)
    # Field name made lowercase.
    nome_titolare = models.CharField(
        db_column='NOME_TITOLARE',
        max_length=200,
        blank=True,
        null=True)
    # Field name made lowercase.
    matricola_titolare = models.CharField(
        db_column='MATRICOLA_TITOLARE',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    fat_part_stu_cod = models.CharField(
        db_column='FAT_PART_STU_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    fat_part_stu_des = models.CharField(
        db_column='FAT_PART_STU_DES',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    part_stu_cod = models.CharField(
        db_column='PART_STU_COD',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    part_stu_des = models.CharField(
        db_column='PART_STU_DES',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase.
    tipo_fat_stu_cod = models.CharField(
        db_column='TIPO_FAT_STU_COD',
        max_length=20,
        blank=True,
        null=True)
    # Field name made lowercase.
    part_ini = models.CharField(
        db_column='PART_INI',
        max_length=100,
        blank=True,
        null=True)
    # Field name made lowercase.
    part_fine = models.CharField(
        db_column='PART_FINE',
        max_length=100,
        blank=True,
        null=True)
    # Field name made lowercase.
    non_erogabile_flg = models.IntegerField(
        db_column='NON_EROGABILE_FLG', blank=True, null=True)
    # Field name made lowercase.
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)
    # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)
    # Field name made lowercase.
    cds_des = models.CharField(
        db_column='CDS_DES',
        max_length=500,
        blank=True,
        null=True)
    # Field name made lowercase.
    coper_peso = models.FloatField(
        db_column='COPER_PESO', blank=True, null=True)
    # Field name made lowercase.
    ore = models.PositiveIntegerField(db_column='ORE', blank=True, null=True)
    stato_coper_cod = models.CharField(db_column='STATO_COPER_COD', max_length=10, blank=True,null=True)  # Field name made lowercase.
    stato_coper_des = models.CharField(db_column='STATO_COPER_DES', max_length=100, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_COPERTURA'


class DidatticaCoperturaDettaglioOre(models.Model):
    ore_coper_det_id = models.IntegerField(db_column='ORE_COPER_DET_ID', primary_key=True)  # Field name made lowercase.
    coper = models.ForeignKey(DidatticaCopertura, models.DO_NOTHING, db_column='COPER_ID')  # Field name made lowercase.
    tipo_att_did_cod = models.CharField(db_column='TIPO_ATT_DID_COD', max_length=10)  # Field name made lowercase.
    ore = models.DecimalField(db_column='ORE', max_digits=6, decimal_places=2)  # Field name made lowercase.
    dt_ins = models.DateField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_COPERTURA_DETTAGLIO_ORE'


class DidatticaDipartimento(InsModAbstract):

    dip_id = models.IntegerField(db_column='DIP_ID', primary_key=True)
    dip_cod = models.CharField(
        db_column='DIP_COD',
        unique=True,
        max_length=40,
        blank=True,
        null=True)
    dip_des_it = models.CharField(
        db_column='DIP_DES_IT',
        max_length=255,
        blank=True,
        null=True)
    dip_des_eng = models.CharField(
        db_column='DIP_DES_ENG',
        max_length=255,
        blank=True,
        null=True)
    dip_nome_breve = models.CharField(
        db_column='DIP_NOME_BREVE',
        max_length=100,
        blank=True,
        null=True)
    dip_cd_csa = models.CharField(
        db_column='DIP_CD_CSA',
        max_length=40,
        blank=True,
        null=True)

    miur_dip_id = models.IntegerField(
        db_column='MIUR_DIP_ID', blank=True, null=True)
    url_pubbl_off_f = models.URLField(
        db_column='URL_PUBBL_OFF_F',
        max_length=255,
        blank=True,
        null=True)
    dip_vis_web_flg = models.IntegerField(
        db_column='DIP_VIS_WEB_FLG', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DIPARTIMENTO'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.dip_cod, self.dip_des_it)


class DidatticaDipartimentoUrl(models.Model):
    dip_cod = models.OneToOneField(DidatticaDipartimento,
                                   models.DO_NOTHING,
                                   db_column='DIP_COD',
                                   primary_key=True,
                                   to_field='dip_cod')  # Field name made lowercase.
    dip_url = models.URLField(db_column='DIP_URL',
                               max_length=4000)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DIPARTIMENTO_URL'


class DidatticaDottoratoAttivitaFormativaTipologia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_it = models.CharField(db_column='NOME_IT', max_length=255)  # Field name made lowercase.
    nome_en = models.CharField(db_column='NOME_EN', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_TIPOLOGIA'

    def __str__(self):
        return self.nome_it


class DidatticaDottoratoAttivitaFormativa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_af = models.CharField(db_column='NOME_AF', max_length=1000, blank=False, null=True)  # Field name made lowercase.
    ssd = models.CharField(db_column='SSD', max_length=1000, blank=False, null=True)  # Field name made lowercase.
    id_didattica_ssd = models.ForeignKey('DidatticaSsd', on_delete=models.SET_NULL, db_column='ID_DIDATTICA_SSD', blank=False, null=True, to_field='ssd_id') # Field name made lowercase.
    numero_ore = models.IntegerField(db_column='NUMERO_ORE', blank=False, null=True)  # Field name made lowercase.
    cfu = models.IntegerField(db_column='CFU', blank=False, null=True)  # Field name made lowercase.
    tipo_af = models.CharField(db_column='TIPO_AF', max_length=500)  # Field name made lowercase.
    tipologia = models.ForeignKey('DidatticaDottoratoAttivitaFormativaTipologia', models.SET_NULL, db_column='TIPOLOGIA', blank=False, null=True)
    rif_dottorato = models.CharField(db_column='RIF_DOTTORATO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ciclo = models.IntegerField(db_column='CICLO')  # Field name made lowercase.
    id_struttura_proponente = models.ForeignKey('UnitaOrganizzativa', models.DO_NOTHING, db_column='ID_STRUTTURA_PROPONENTE', blank=True, null=True)  # Field name made lowercase.
    struttura_proponente_origine = models.CharField(db_column='STRUTTURA_PROPONENTE_ORIGINE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contenuti_af = models.TextField(db_column='CONTENUTI_AF', blank=False, null=True)  # Field name made lowercase.
    prerequisiti = models.TextField(db_column='PREREQUISITI', blank=True, null=True)  # Field name made lowercase.
    num_min_studenti = models.IntegerField(db_column='NUM_MIN_STUDENTI', blank=True, null=True)  # Field name made lowercase.
    num_max_studenti = models.IntegerField(db_column='NUM_MAX_STUDENTI', blank=True, null=True)  # Field name made lowercase.
    verifica_finale = models.BooleanField(db_column='VERIFICA_FINALE', default=False)  # Field name made lowercase.
    modalita_verifica = models.CharField(db_column='MODALITA_VERIFICA', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    avvio = models.CharField(db_column='AVVIO', blank=True, null=True, max_length=255)  # Field name made lowercase.
    fine = models.CharField(db_column='FINE', blank=True, null=True, max_length=255)  # Field name made lowercase.
    orario_aule = models.TextField(db_column='ORARIO_AULE', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='NOTE', blank=True, null=True)  # Field name made lowercase.
    visualizza_orario = models.BooleanField(db_column='VISUALIZZA_ORARIO',default=False)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA'


class DidatticaDottoratoAttivitaFormativaAltriDocenti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_didattica_dottorato_attivita_formativa = models.ForeignKey(DidatticaDottoratoAttivitaFormativa, models.CASCADE, db_column='ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA', blank=True, null=True)  # Field name made lowercase.
    matricola = models.ForeignKey('Personale', models.CASCADE, db_column='MATRICOLA', to_field='matricola', blank=True, null=True)  # Field name made lowercase.
    cognome_nome_origine = models.CharField(db_column='COGNOME_NOME_ORIGINE', max_length=200)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_ALTRI_DOCENTI'


class DidatticaDottoratoAttivitaFormativaDocente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_didattica_dottorato_attivita_formativa = models.ForeignKey(DidatticaDottoratoAttivitaFormativa, models.CASCADE, db_column='ID_DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA', blank=True, null=True)  # Field name made lowercase.
    matricola = models.ForeignKey('Personale', models.CASCADE, db_column='MATRICOLA', to_field='matricola', blank=True, null=True)  # Field name made lowercase.
    cognome_nome_origine = models.CharField(db_column='COGNOME_NOME_ORIGINE', max_length=200)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    def __str__(self): # pragma: no cover
        return self.cognome_nome_origine

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_ATTIVITA_FORMATIVA_DOCENTE'


class DidatticaDottoratoCds(InsModAbstract):
    dip_cod = models.ForeignKey(
        DidatticaDipartimento,
        models.DO_NOTHING,
        db_column='DIP_COD',
        blank=True,
        null=True,
        to_field='dip_cod')

    cds_id_esse3 = models.IntegerField(
        db_column='CDS_ID_ESSE3', primary_key=True)

    cds_cod = models.CharField(
        db_column='CDS_COD',
        max_length=10,
        blank=True,
        null=True)
    nome_cds_it = models.CharField(
        db_column='NOME_CDS_IT',
        max_length=255,
        blank=True,
        null=True)

    rif_cod = models.CharField(
        db_column='RIF_COD',
        max_length=10,
        blank=True,
        null=True)

    rif_des = models.CharField(
        db_column='RIF_DES',
        max_length=255,
        blank=True,
        null=True)
    tipo_corso_cod = models.CharField(
        db_column='TIPO_CORSO_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_corso_des = models.CharField(
        db_column='TIPO_CORSO_DES',
        max_length=80,
        blank=True,
        null=True)

    durata_anni = models.IntegerField(
        db_column='DURATA_ANNI', blank=True, null=True)

    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    tipo_titit_cod = models.CharField(
        db_column='TIPO_TITIT_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_titit_des = models.CharField(
        db_column='TIPO_TITIT_DES',
        max_length=255,
        blank=True,
        null=True)
    tipo_spec_cod = models.CharField(
        db_column='TIPO_SPEC_COD',
        max_length=10,
        blank=True,
        null=True)
    tipo_spec_des = models.CharField(
        db_column='TIPO_SPEC_DES',
        max_length=255,
        blank=True,
        null=True)
    istat_cod = models.CharField(
        db_column='ISTAT_COD',
        max_length=10,
        blank=True,
        null=True)

    max_punti = models.IntegerField(
        db_column='MAX_PUNTI', blank=True, null=True)
    um_peso_cod = models.CharField(
        db_column='UM_PESO_COD',
        max_length=5,
        blank=True,
        null=True)
    um_peso_des = models.CharField(
        db_column='UM_PESO_DES',
        max_length=40,
        blank=True,
        null=True)

    aa_att_id = models.IntegerField(
        db_column='AA_ATT_ID', blank=True, null=True)

    aa_dis_id = models.IntegerField(
        db_column='AA_DIS_ID', blank=True, null=True)

    url = models.URLField(
        db_column='URL',
        max_length=255,
        blank=True,
        null=True)
    cds_url_info_web = models.URLField(
        db_column='CDS_URL_INFO_WEB',
        max_length=255,
        blank=True,
        null=True)
    cds_vis_web_flg = models.IntegerField(
        db_column='CDS_VIS_WEB_FLG', blank=True, null=True)
    cdsord_id_esse3 = models.IntegerField(
        db_column='CDSORD_ID_ESSE3', blank=True, null=True)
    cdsord_cod = models.CharField(
        db_column='CDSORD_COD',
        max_length=10,
        blank=True,
        null=True)

    aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')
    cdsord_des = models.CharField(
        db_column='CDSORD_DES',
        max_length=255,
        blank=True,
        null=True)
    stato_cdsord_cod = models.CharField(
        db_column='STATO_CDSORD_COD',
        max_length=5,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_CDS'
        unique_together = (('cds_id_esse3', 'aa_ord_id'),)


class DidatticaDottoratoPds(InsModAbstract):
    cds_id_esse3 = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column='CDS_ID_ESSE3',
        blank=True,
        null=True,
        related_name='idesse3_ddpds')

    aa_ord = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column='AA_ORD_ID',
        blank=True,
        null=True,
        related_name='aaord_ddpds')

    pds_id_esse3 = models.IntegerField(
        db_column='PDS_ID_ESSE3', blank=True, null=True)

    pdsord_id_esse3 = models.IntegerField(
        db_column='PDSORD_ID_ESSE3', primary_key=True)

    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=40,
        blank=True,
        null=True)

    pds_des = models.CharField(
        db_column='PDS_DES',
        max_length=255,
        blank=True,
        null=True)

    indir = models.CharField(
        db_column='INDIR',
        max_length=255,
        blank=True,
        null=True)

    orien = models.CharField(
        db_column='ORIEN',
        max_length=255,
        blank=True,
        null=True)

    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    stato_cod = models.CharField(
        db_column='STATO_COD',
        max_length=5,
        blank=True,
        null=True)

    data_var = models.DateTimeField(
        db_column='DATA_VAR', blank=True, null=True)

    val_min_tesi = models.IntegerField(
        db_column='VAL_MIN_TESI', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_PDS'


class DidatticaDottoratoRegolamento(InsModAbstract):

    regdid_id_esse3 = models.IntegerField(
        db_column='REGDID_ID_ESSE3', primary_key=True)

    aa_regdid_id = models.IntegerField(
        db_column='AA_REGDID_ID', blank=True, null=True)
    cds_id_esse3 = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column='CDS_ID_ESSE3',
        blank=True,
        null=True,
        related_name='idesse3_ddr')
    regdid_cod = models.CharField(
        db_column='REGDID_COD',
        max_length=255,
        blank=True,
        null=True)
    regdid_des = models.CharField(
        db_column='REGDID_DES',
        max_length=255,
        blank=True,
        null=True)
    numero_piani_studio = models.IntegerField(
        db_column='NUMERO_PIANI_STUDIO',
        blank=True,
        null=True)
    frequenza_obbligatoria = models.IntegerField(
        db_column='FREQUENZA_OBBLIGATORIA',
        blank=True,
        null=True)

    num_ciclo = models.IntegerField(
        db_column='NUM_CICLO', blank=True, null=True)
    aa_ord = models.ForeignKey(
        DidatticaDottoratoCds,
        models.DO_NOTHING,
        db_column='AA_ORD_ID',
        related_name='aaord_ddr')

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DOTTORATO_REGOLAMENTO'


class DidatticaPdsRegolamento(InsModAbstract):

    pds_regdid_id = models.IntegerField(
        db_column='PDS_REGDID_ID', primary_key=True)

    pds_cod = models.CharField(
        db_column='PDS_COD',
        max_length=30,
        blank=True,
        null=True)
    pds_des_it = models.CharField(
        db_column='PDS_DES_IT',
        max_length=255,
        blank=True,
        null=True)
    pds_des_eng = models.CharField(
        db_column='PDS_DES_ENG',
        max_length=2000,
        blank=True,
        null=True)

    comune_flg = models.IntegerField(
        db_column='COMUNE_FLG', blank=True, null=True)

    valore_min = models.IntegerField(
        db_column='VALORE_MIN', blank=True, null=True)
    regdid = models.ForeignKey(
        'DidatticaRegolamento',
        models.DO_NOTHING,
        db_column='REGDID_ID',
        blank=True,
        null=True)

    # aa_ord_id = models.IntegerField(db_column='AA_ORD_ID')

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PDS_REGOLAMENTO'


class DidatticaRegolamento(InsModAbstract):

    regdid_id = models.IntegerField(db_column='REGDID_ID', primary_key=True)

    aa_reg_did = models.IntegerField(
        db_column='AA_REG_DID', blank=True, null=True)
    cds = models.ForeignKey(
        DidatticaCds,
        models.DO_NOTHING,
        db_column='CDS_ID',
        blank=True,
        null=True)
    stato_regdid_cod = models.CharField(
        db_column='STATO_REGDID_COD',
        max_length=5,
        blank=True,
        null=True)
    stato_regdid_des = models.CharField(
        db_column='STATO_REGDID_DES',
        max_length=40,
        blank=True,
        null=True)
    numero_piani_studio = models.IntegerField(
        db_column='NUMERO_PIANI_STUDIO',
        blank=True,
        null=True)
    anno_scelta_pds = models.IntegerField(
        db_column='ANNO_SCELTA_PDS', blank=True, null=True)
    modalita_erogazione = models.CharField(
        db_column='MODALITA_EROGAZIONE',
        max_length=100,
        blank=True,
        null=True)
    frequenza_obbligatoria = models.IntegerField(
        db_column='FREQUENZA_OBBLIGATORIA',
        blank=True,
        null=True)
    titolo_congiunto_cod = models.CharField(
        db_column='TITOLO_CONGIUNTO_COD',
        max_length=100,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_REGOLAMENTO'

    def get_ordinamento_didattico(self):
        # se è stato caricato un ordinamento per quest'anno, lo restituisco
        other_data = DidatticaCdsAltriDati.objects.filter(regdid_id=self).first()
        if other_data and other_data.ordinamento_didattico:
            return (self.aa_reg_did, other_data.ordinamento_didattico)

        prev_regdid = DidatticaRegolamento.objects.filter(cds=self.cds, aa_reg_did=self.aa_reg_did-1).first()
        if not prev_regdid: return None
        return prev_regdid.get_ordinamento_didattico()

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.regdid_id, self.aa_reg_did)


class DidatticaRegolamentoTipologiaAltriDati(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_testo_regdid_cod = models.CharField(db_column='TIPO_TESTO_REGDID_COD', unique=True, max_length=100)  # Field name made lowercase.
    tipo_testo_regdid_des = models.CharField(db_column='TIPO_TESTO_REGDID_DES', max_length=2000)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.SET_NULL, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_REGOLAMENTO_TIPOLOGIA_ALTRI_DATI'


class DidatticaRegolamentoAltriDati(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    regdid = models.ForeignKey(DidatticaRegolamento, models.CASCADE, db_column='REGDID_ID')  # Field name made lowercase.
    tipo_testo_regdid_cod = models.ForeignKey(DidatticaRegolamentoTipologiaAltriDati, models.PROTECT, db_column='TIPO_TESTO_REGDID_COD', to_field='tipo_testo_regdid_cod')  # Field name made lowercase.
    clob_txt_ita = models.TextField(db_column='CLOB_TXT_ITA', blank=True, null=True)  # Field name made lowercase.
    clob_txt_eng = models.TextField(db_column='CLOB_TXT_ENG', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.SET_NULL, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_REGOLAMENTO_ALTRI_DATI'


class DidatticaTestiAf(InsModAbstract):
    af = models.OneToOneField(
        DidatticaAttivitaFormativa,
        models.DO_NOTHING,
        db_column='AF_ID',
        primary_key=True)

    aa_off_id = models.IntegerField(
        db_column='AA_OFF_ID', blank=True, null=True)

    testi_af_id = models.IntegerField(
        db_column='TESTI_AF_ID', blank=True, null=True)

    tipo_testo_af_cod = models.CharField(
        db_column='TIPO_TESTO_AF_COD', max_length=100)
    tipo_testo_af_des = models.TextField(
        db_column='TIPO_TESTO_AF_DES', blank=True, null=True)
    tipo_testo_af_etic = models.CharField(
        db_column='TIPO_TESTO_AF_ETIC',
        max_length=255,
        blank=True,
        null=True)
    tipo_testo_af_etic_eng = models.TextField(
        db_column='TIPO_TESTO_AF_ETIC_ENG',
        blank=True,
        null=True)

    obbl_flg = models.IntegerField(db_column='OBBL_FLG', blank=True, null=True)

    testo_af_ita = models.TextField(
        db_column='TESTO_AF_ITA', blank=True, null=True)
    testo_af_short_ita = models.TextField(
        db_column='TESTO_AF_SHORT_ITA', blank=True, null=True)
    testo_af_fmt_ita = models.TextField(
        db_column='TESTO_AF_FMT_ITA', blank=True, null=True)
    dt_ins_txt_clob_ita = models.DateTimeField(
        db_column='DT_INS_TXT_CLOB_ITA',
        blank=True,
        null=True)
    dt_mod_txt_clob_ita = models.DateTimeField(
        db_column='DT_MOD_TXT_CLOB_ITA',
        blank=True,
        null=True)

    testo_af_eng = models.TextField(
        db_column='TESTO_AF_ENG', blank=True, null=True)
    testo_af_short_eng = models.TextField(
        db_column='TESTO_AF_SHORT_ENG', blank=True, null=True)
    dt_ins_txt_clob_eng = models.TextField(
        db_column='DT_INS_TXT_CLOB_ENG',
        blank=True,
        null=True)
    dt_mod_txt_clob_eng = models.DateTimeField(
        db_column='DT_MOD_TXT_CLOB_ENG',
        blank=True,
        null=True)
    dt_ins_mod_max = models.DateTimeField(
        db_column='DT_INS_MOD_MAX', blank=True, null=True)
    testo_af_fmt_eng = models.TextField(
        db_column='TESTO_AF_FMT_ENG', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_TESTI_AF'
        unique_together = (('af', 'tipo_testo_af_cod'),)


class DidatticaTestiRegolamento(InsModAbstract):

    txt_id = models.IntegerField(db_column='TXT_ID', primary_key=True)
    regdid = models.ForeignKey(DidatticaRegolamento, models.DO_NOTHING,
                               db_column='REGDID_ID')
    tipo_testo_regdid_cod = models.CharField(
        db_column='TIPO_TESTO_REGDID_COD',
        max_length=100)
    tipo_testo_regdid_des = models.CharField(
        db_column='TIPO_TESTO_REGDID_DES',
        max_length=255,
        blank=True,
        null=True)

    clob_txt_ita = models.TextField(
        db_column='CLOB_TXT_ITA', blank=True, null=True)

    clob_txt_eng = models.TextField(
        db_column='CLOB_TXT_ENG', blank=True, null=True)

    testo_regdid_url = models.URLField(
        db_column='TESTO_REGDID_URL',
        max_length=1024,
        blank=True,
        null=True)

    profilo = models.TextField(db_column='PROFILO', blank=True, null=True)

    profilo_eng = models.TextField(
        db_column='PROFILO_ENG', blank=True, null=True)
    dt_ins_txt_clob_ita = models.DateTimeField(
        db_column='DT_INS_TXT_CLOB_ITA',
        blank=True,
        null=True)
    dt_ins_txt_clob_eng = models.DateTimeField(
        db_column='DT_INS_TXT_CLOB_ENG',
        blank=True,
        null=True)
    dt_mod_txt_clob_ita = models.DateTimeField(
        db_column='DT_MOD_TXT_CLOB_ITA',
        blank=True,
        null=True)
    dt_mod_txt_clob_eng = models.DateTimeField(
        db_column='DT_MOD_TXT_CLOB_ENG',
        blank=True,
        null=True)
    dt_ins = models.DateTimeField(db_column='DT_INS', blank=True, null=True)
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_TESTI_REGOLAMENTO'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.txt_id, self.tipo_testo_regdid_cod)


class DocenteMaterialeDidattico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola = models.ForeignKey('Personale', models.CASCADE, db_column='MATRICOLA', to_field='matricola')  # Field name made lowercase.
    titolo = models.CharField(db_column='TITOLO', max_length=200)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    testo = models.TextField(db_column='TESTO')  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    url_testo = models.URLField(db_column='URL_TESTO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    url_testo_en = models.URLField(db_column='URL_TESTO_EN', max_length=400, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE')  # Field name made lowercase.
    attivo = models.BooleanField(db_column='ATTIVO')  # Field name made lowercase.
    dt_pubblicazione = models.DateTimeField(db_column='DT_PUBBLICAZIONE', blank=True, null=True)  # Field name made lowercase.
    dt_inizio_validita = models.DateTimeField(db_column='DT_INIZIO_VALIDITA', blank=True, null=True)  # Field name made lowercase.
    dt_fine_validita = models.DateTimeField(db_column='DT_FINE_VALIDITA', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DOCENTE_MATERIALE_DIDATTICO'
        ordering = ('ordine', '-dt_pubblicazione', '-dt_inizio_validita')


class DocentePtaAltriDati(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola = models.OneToOneField('Personale', models.CASCADE, db_column='MATRICOLA', to_field='matricola')  # Field name made lowercase.
    path_foto = models.FileField(
        upload_to=teacher_photo_media_path,
        validators=[validate_image_file_extension,
                    validate_file_size,
                    validate_image_size_ratio],
        db_column='PATH_FOTO',
        max_length=500,
        blank=True,
        null=True) # Field name made lowercase.
    path_cv_ita = models.FileField(
        upload_to=teacher_cv_ita_media_path,
        validators=[validate_pdf_file_extension,
                    validate_file_size],
        db_column='PATH_CV_ITA',
        max_length=500,
        blank=True,
        null=True)  # Field name made lowercase.
    path_cv_en = models.FileField(
        upload_to=teacher_cv_en_media_path,
        validators=[validate_pdf_file_extension,
                    validate_file_size],
        db_column='PATH_CV_EN',
        max_length=500,
        blank=True,
        null=True)  # Field name made lowercase.
    breve_bio = models.TextField(db_column='BREVE_BIO', blank=True, null=True)  # Field name made lowercase.
    breve_bio_en = models.TextField(db_column='BREVE_BIO_EN', blank=True, null=True)  # Field name made lowercase.
    orario_ricevimento = models.TextField(db_column='ORARIO_RICEVIMENTO', blank=True, null=True)  # Field name made lowercase.
    orario_ricevimento_en = models.TextField(db_column='ORARIO_RICEVIMENTO_EN', blank=True, null=True)  # Field name made lowercase.
    orcid = models.CharField(validators=[orcid_validator], db_column='ORCID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DOCENTE_PTA_ALTRI_DATI'


class DocentePtaBacheca(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola = models.ForeignKey('Personale', models.CASCADE, db_column='MATRICOLA', to_field='matricola')  # Field name made lowercase.
    tipo_testo = models.CharField(db_column='TIPO_TESTO', max_length=100)  # Field name made lowercase.
    tipo_testo_en = models.CharField(db_column='TIPO_TESTO_EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    titolo = models.CharField(db_column='TITOLO', max_length=200)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    testo = models.TextField(db_column='TESTO')  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    url_testo = models.URLField(db_column='URL_TESTO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    url_testo_en = models.URLField(db_column='URL_TESTO_EN', max_length=400, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE')  # Field name made lowercase.
    attivo = models.BooleanField(db_column='ATTIVO')  # Field name made lowercase.
    dt_pubblicazione = models.DateTimeField(db_column='DT_PUBBLICAZIONE', blank=True, null=True)  # Field name made lowercase.
    dt_inizio_validita = models.DateTimeField(db_column='DT_INIZIO_VALIDITA', blank=True, null=True)  # Field name made lowercase.
    dt_fine_validita = models.DateTimeField(db_column='DT_FINE_VALIDITA', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.ForeignKey(get_user_model(), models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DOCENTE_PTA_BACHECA'
        ordering = ('ordine', '-dt_pubblicazione', '-dt_inizio_validita')


class UnitaOrganizzativa(models.Model):
    # Field name made lowercase.
    uo = models.CharField(db_column='UO', primary_key=True, max_length=40)
    # Field name made lowercase.
    id_ab = models.IntegerField(
        db_column='ID_AB',
        unique=True,
        blank=True,
        null=True)
    # Field name made lowercase.
    cd_tipo_nodo = models.CharField(
        db_column='CD_TIPO_NODO',
        max_length=10,
        default="000")
    ds_tipo_nodo = models.CharField(
        db_column='DS_TIPO_NODO',
        max_length=255,
        default="Non assegnato")  # Field name made lowercase.
    denominazione = models.CharField(
        db_column='DENOMINAZIONE',
        max_length=255,
        default="Non assegnato")  # Field name made lowercase.
    nome_esteso = models.CharField(
        db_column='NOME_ESTESO',
        max_length=255,
        default="Non assegnato")  # Field name made lowercase.
    # Field name made lowercase.
    nome_breve = models.CharField(
        db_column='NOME_BREVE',
        max_length=50,
        default="Non assegnato")
    # Field name made lowercase.
    dt_inizio_val = models.DateTimeField(
        db_column='DT_INIZIO_VAL', blank=True, null=True)
    # Field name made lowercase.
    dt_fine_val = models.DateTimeField(
        db_column='DT_FINE_VAL', blank=True, null=True)
    # Field name made lowercase.
    dt_creazione = models.DateTimeField(
        db_column='DT_CREAZIONE', blank=True, null=True)
    # Field name made lowercase.
    uo_padre = models.CharField(
        db_column='UO_PADRE',
        max_length=40,
        blank=True,
        null=True)
    # Field name made lowercase.
    id_ab_padre = models.IntegerField(
        db_column='ID_AB_PADRE', blank=True, null=True)
    cd_tipo_nodo_padre = models.CharField(
        db_column='CD_TIPO_NODO_PADRE',
        max_length=10,
        blank=True,
        null=True)  # Field name made lowercase.
    ds_tipo_nodo_padre = models.CharField(
        db_column='DS_TIPO_NODO_PADRE',
        max_length=255,
        blank=True,
        null=True)  # Field name made lowercase.
    cd_macrotipo_nodo_padre = models.CharField(
        db_column='CD_MACROTIPO_NODO_PADRE',
        max_length=10,
        blank=True,
        null=True)  # Field name made lowercase.
    denominazione_padre = models.CharField(
        db_column='DENOMINAZIONE_PADRE',
        max_length=255,
        blank=True,
        null=True)  # Field name made lowercase.
    nome_esteso_padre = models.CharField(
        db_column='NOME_ESTESO_PADRE',
        max_length=255,
        blank=True,
        null=True)  # Field name made lowercase.
    nome_breve_padre = models.CharField(
        db_column='NOME_BREVE_PADRE',
        max_length=50,
        blank=True,
        null=True)  # Field name made lowercase.
    dt_inizio_val_padre = models.DateTimeField(
        db_column='DT_INIZIO_VAL_PADRE',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_fine_val_padre = models.DateTimeField(
        db_column='DT_FINE_VAL_PADRE', blank=True, null=True)
    dt_creazione_padre = models.DateTimeField(
        db_column='DT_CREAZIONE_PADRE',
        blank=True,
        null=True)  # Field name made lowercase.
    cd_csa = models.CharField(
        db_column='CD_CSA',
        unique=True,
        max_length=40,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    ds_mission = models.TextField(
        db_column='DS_MISSION', blank=True, null=True)

    def __str__(self): # pragma: no cover
        return '{}'.format(self.denominazione)

    class Meta:
        managed = True
        db_table = 'UNITA_ORGANIZZATIVA'


class UnitaOrganizzativaFunzioni(models.Model):
    matricola = models.CharField(
        db_column='MATRICOLA',
        max_length=6,
        blank=True,
        null=True)
    cd_csa = models.ForeignKey(
        UnitaOrganizzativa,
        models.DO_NOTHING,
        db_column='CD_CSA',
        to_field='cd_csa',
        blank=True,
        null=True)  # Field name made lowercase.
    cod_fis = models.ForeignKey(
        'Personale',
        models.DO_NOTHING,
        db_column='COD_FIS',
        blank=True,
        null=True,
        to_field='cod_fis')

    comparto = models.CharField(
        db_column='COMPARTO',
        max_length=1,
        blank=True,
        null=True)

    ruolo = models.CharField(
        db_column='RUOLO',
        max_length=4,
        blank=True,
        null=True)
    funzione = models.CharField(
        db_column='FUNZIONE',
        max_length=6,
        blank=True,
        null=True)

    decorrenza = models.DateTimeField(
        db_column='DECORRENZA', blank=True, null=True)

    termine = models.DateTimeField(db_column='TERMINE', blank=True, null=True)
    ds_funzione = models.CharField(
        db_column='DS_FUNZIONE',
        max_length=100,
        blank=True,
        null=True)

    fl_posorg = models.FloatField(db_column='FL_POSORG', blank=True, null=True)
    fl_responsabile = models.FloatField(
        db_column='FL_RESPONSABILE', blank=True, null=True)
    cd_funzbase = models.CharField(
        db_column='CD_FUNZBASE',
        max_length=6,
        blank=True,
        null=True)

    id_ab = models.IntegerField(db_column='ID_AB', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'UNITA_ORGANIZZATIVA_FUNZIONI'


class UnitaOrganizzativaTipoFunzioni(models.Model):
    # Field name made lowercase.
    cd_tipo_nod = models.CharField(
        db_column='CD_TIPO_NOD',
        primary_key=True,
        max_length=100)
    # Field name made lowercase.
    funzione = models.CharField(db_column='FUNZIONE', max_length=100)
    # Field name made lowercase.
    descr_funzione = models.CharField(
        db_column='DESCR_FUNZIONE', max_length=1000)

    class Meta:
        managed = True
        db_table = 'UNITA_ORGANIZZATIVA_TIPO_FUNZIONI'
        unique_together = (('cd_tipo_nod', 'funzione'),)


class LaboratorioAltriDipartimenti(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        'LaboratorioDatiBase',
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    id_dip = models.ForeignKey(
        DidatticaDipartimento,
        models.DO_NOTHING,
        db_column='id_dip',
        blank=True,
        null=True)
    descr_dip_lab = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'LABORATORIO_ALTRI_DIPARTIMENTI'


class LaboratorioAttivita(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        'LaboratorioDatiBase',
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    id_tipologia_attivita = models.ForeignKey(
        'LaboratorioTipologiaAttivita',
        models.PROTECT,
        db_column='ID_TIPOLOGIA_ATTIVITA',
        null=True)  # Field name made lowercase.

    descr_finalita_it = models.TextField(
        db_column='DESCR_FINALITA_IT', blank=False, null=True)

    descr_finalita_en = models.TextField(
        db_column='DESCR_FINALITA_EN', blank=False, null=True)

    class Meta:
        managed = True
        db_table = 'LABORATORIO_ATTIVITA'

class LaboratorioAttrezzatureRischi(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_attrezzature = models.ForeignKey(
        'LaboratorioAttrezzature',
        models.CASCADE,
        db_column='ID_LABORATORIO_ATTREZZATURE',
        blank=True,
        null=True)  # Field name made lowercase.
    id_tipologia_rischio = models.ForeignKey(
        'TipologiaRischio',
        models.CASCADE,
        db_column='ID_TIPOLOGIA_RISCHIO',
        blank=True,
        null=True)  # Field name made lowercase.

    dt_mod = models.DateTimeField(db_column='DT_MOD',
                              blank=True, null=True) # Field name made lowercase.

    user_mod_id = models.ForeignKey(get_user_model(),
                                 on_delete=models.SET_NULL,
                                 db_column='user_mod_id',
                                 blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'LABORATORIO_ATTREZZATURE_RISCHI'

class LaboratorioFondo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome_fondo = models.CharField(
        db_column='NOME_FONDO',
        max_length=500,
        blank=False,
        null=False) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_FONDO'

class LaboratorioAttrezzatureFondi(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_attrezzature = models.ForeignKey(
        'LaboratorioAttrezzature',
        models.CASCADE,
        db_column='ID_LABORATORIO_ATTREZZATURE',
        blank=True,
        null=True)  # Field name made lowercase.
    id_laboratorio_fondo = models.ForeignKey(
        'LaboratorioFondo',
        models.CASCADE,
        db_column='ID_LABORATORIO_FONDO',
        blank=True,
        null=True)  # Field name made lowercase.

    dt_mod = models.DateTimeField(db_column='DT_MOD',
                              blank=True, null=True) # Field name made lowercase.

    user_mod_id = models.ForeignKey(get_user_model(),
                                 on_delete=models.SET_NULL,
                                 db_column='user_mod_id',
                                 blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'LABORATORIO_ATTREZZATURE_FONDI'


class LaboratorioAttrezzature(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        'LaboratorioDatiBase',
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    tipologia = models.CharField(
        db_column='TIPOLOGIA',
        max_length=500,
        blank=False,
        null=True)
    # Field name made lowercase.
    descrizione = models.TextField(
        db_column='DESCRIZIONE', blank=False, null=True) # Field name made lowercase.
    costo_unitario = models.FloatField(
        db_column='COSTO_UNITARIO', blank=False, null=True) # Field name made lowercase.
    quantita = models.IntegerField(
        db_column='QUANTITA', blank=False, null=True) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_ATTREZZATURE'


class LaboratorioInfrastruttura(models.Model):
    # Field name made lowercase.
    id = models.BigAutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=1000)


    def __str__(self): # pragma: no cover
        return self.descrizione

    class Meta:
        managed = True
        db_table = 'LABORATORIO_INFRASTRUTTURA'


class LaboratorioTipologiaAttivita(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=1000)

    class Meta:
        managed = True
        db_table = 'LABORATORIO_TIPOLOGIA_ATTIVITA'

class TipologiaRischio(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_tipologia = models.CharField(db_column='DESCR_TIPOLOGIA', max_length=1000)

    class Meta:
        managed = True
        db_table = 'TIPOLOGIA_RISCHIO'

class LaboratorioDatiBase(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    dt_sottomissione = models.DateTimeField(
        db_column='DT_SOTTOMISSIONE', blank=True, null=True)
    referente_compilazione = models.CharField(
        db_column='REFERENTE_COMPILAZIONE',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_referente_compilazione = models.ForeignKey(
        'Personale',
        models.SET_NULL,
        db_column='MATRICOLA_REFERENTE_COMPILAZIONE',
        blank=True,
        null=True,
        related_name="matricola_referente_compilazione_personale",
        to_field="matricola")  # Field name made lowercase.
    email_compilazione = models.CharField(
        db_column='EMAIL_COMPILAZIONE',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    nome_laboratorio = models.CharField(
        db_column='NOME_LABORATORIO',
        max_length=400,
        blank=False,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    acronimo = models.CharField(
        db_column='ACRONIMO',
        max_length=100,
        blank=True,
        null=True)
    logo_laboratorio = models.CharField(
        db_column='LOGO_LABORATORIO',
        max_length=400,
        blank=True,
        null=True)  # Field name made lowercase.
    dipartimento_riferimento = models.CharField(
        db_column='DIPARTIMENTO_RIFERIMENTO',
        max_length=400,
        blank=True,
        null=True)  # Field name made lowercase.
    id_dipartimento_riferimento = models.ForeignKey(
        DidatticaDipartimento,
        models.DO_NOTHING,
        db_column='ID_DIPARTIMENTO_RIFERIMENTO',
        blank=True,
        null=True)  # Field name made lowercase.
    laboratorio_interdipartimentale = models.CharField(
        db_column='LABORATORIO_INTERDIPARTIMENTALE',
        max_length=400,
        blank=True,
        null=True)  # Field name made lowercase.
    altre_strutture_riferimento = models.CharField(
        db_column='ALTRE_STRUTTURE_RIFERIMENTO',
        max_length=400,
        blank=True,
        null=True)  # Field name made lowercase.
    descr_altre_strutture_riferimento_it = models.TextField(
        db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_IT',
        blank=True,
        null=True)  # Field name made lowercase.
    descr_altre_strutture_riferimento_en = models.TextField(
        db_column='DESCR_ALTRE_STRUTTURE_RIFERIMENTO_EN',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    ambito = models.CharField(
        db_column='AMBITO',
        max_length=100,
        blank=True,
        null=True)
    finalita_ricerca_it = models.TextField(
        db_column='FINALITA_RICERCA_IT',
        blank=True,
        null=True)  # Field name made lowercase.
    finalita_ricerca_en = models.TextField(
        db_column='FINALITA_RICERCA_EN',
        blank=True,
        null=True)  # Field name made lowercase.
    finalita_didattica_it = models.TextField(
        db_column='FINALITA_DIDATTICA_IT',
        blank=True,
        null=True)  # Field name made lowercase.
    finalita_didattica_en = models.TextField(
        db_column='FINALITA_DIDATTICA_EN',
        blank=True,
        null=True)  # Field name made lowercase.
    finalita_servizi_it = models.TextField(
        db_column='FINALITA_SERVIZI_IT',
        blank=True,
        null=True)  # Field name made lowercase.
    finalita_servizi_en = models.TextField(
        db_column='FINALITA_SERVIZI_EN',
        blank=True,
        null=True)  # Field name made lowercase.
    responsabile_scientifico = models.CharField(
        db_column='RESPONSABILE_SCIENTIFICO',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_responsabile_scientifico = models.ForeignKey(
        'Personale',
        models.SET_NULL,
        db_column='MATRICOLA_RESPONSABILE_SCIENTIFICO',
        blank=True,
        null=True,
        related_name="matricola_responsabile_scientifico_personale",
        to_field="matricola")  # Field name made lowercase.
    sede_dimensione = models.CharField(
        db_column='SEDE_DIMENSIONE',
        max_length=100,
        blank=True,
        null=True)  # Field name made lowercase.
    sede_note_descrittive = models.TextField(
        db_column='SEDE_NOTE_DESCRITTIVE',
        blank=True,
        null=True)  # Field name made lowercase.
    strumentazione_descrizione = models.TextField(
        db_column='STRUMENTAZIONE_DESCRIZIONE',
    )  # Field name made lowercase.
    strumentazione_valore = models.DecimalField(
        decimal_places=2,
        blank=True,
        null=True,
        max_digits=20,
        db_column='STRUMENTAZIONE_VALORE')  # Field name made lowercase.
    preposto_sicurezza = models.CharField(
        db_column='PREPOSTO_SICUREZZA',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_preposto_sicurezza = models.ForeignKey(
        'Personale',
        models.SET_NULL,
        db_column='MATRICOLA_PREPOSTO_SICUREZZA',
        blank=True,
        null=True,
        related_name="matricola_preposto_sicurezza_personale",
        to_field="matricola")  # Field name made lowercase.
    # Field name made lowercase.
    sito_web = models.CharField(
        db_column='SITO_WEB',
        max_length=1024,
        blank=True,
        null=True)
    id_infrastruttura_riferimento = models.ForeignKey(
        'LaboratorioInfrastruttura',
        models.SET_NULL,
        db_column='ID_INFRASTRUTTURA_RIFERIMENTO',
        blank=True,
        null=True)  # Field name made lowercase.
    nome_file_logo = models.FileField(
        upload_to=laboratories_media_path,
        validators=[validate_image_file_extension,
                    validate_file_size],
        db_column='NOME_FILE_LOGO',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.

    visibile = models.BooleanField(db_column='VISIBILE',
                                   default=False)  # Field name made lowercase.

    dt_mod = models.DateTimeField(db_column='DT_MOD',
                              blank=True, null=True) # Field name made lowercase.

    user_mod_id = models.ForeignKey(get_user_model(),
                                 on_delete=models.SET_NULL,
                                 db_column='user_mod_id',
                                 blank=True, null=True)

    tipologia_attivita = models.ManyToManyField(
        LaboratorioTipologiaAttivita, through="LaboratorioAttivita")

    tipologia_rischio = models.ManyToManyField(
        TipologiaRischio, through="LaboratorioTipologiaRischio")

    class Meta:
        managed = True
        db_table = 'LABORATORIO_DATI_BASE'


class LaboratorioDatiErc1(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    id_ricerca_erc1 = models.ForeignKey(
        'RicercaErc1',
        models.PROTECT,
        db_column='ID_RICERCA_ERC1',
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_DATI_ERC1'


class LaboratorioPersonaleRicerca(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_personale_ricerca = models.ForeignKey(
        "Personale",
        models.SET_NULL,
        db_column='MATRICOLA_PERSONALE_RICERCA',
        blank=True,
        null=True,
        to_field="matricola")  # Field name made lowercase.
    cognomenome_origine = models.CharField(
        db_column='COGNOMENOME_ORIGINE',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_PERSONALE_RICERCA'


class LaboratorioPersonaleTecnico(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_personale_tecnico = models.ForeignKey(
        "Personale",
        models.SET_NULL,
        db_column='MATRICOLA_PERSONALE_TECNICO',
        blank=True,
        null=True,
        to_field="matricola")  # Field name made lowercase.
    # Field name made lowercase.
    ruolo = models.CharField(
        db_column='RUOLO',
        max_length=400,
        blank=True,
        null=True)
    # Field name made lowercase. Field renamed to remove unsuitable
    # characters. Field renamed because it started with '_'.
    percentuale_impegno = models.FloatField(
        db_column='PERCENTUALE_IMPEGNO', blank=True, null=True)
    cognomenome_origine = models.CharField(
        db_column='COGNOMENOME_ORIGINE',
        max_length=200,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_PERSONALE_TECNICO'


class LaboratorioServiziErogati(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    descrizione = models.TextField(
        db_column='DESCRIZIONE', blank=False, null=True)
    matricola_responsabile = models.CharField(
        db_column='MATRICOLA_RESPONSABILE',
        max_length=20,
        blank=True,
        null=True)  # Field name made lowercase.
    responsabile_origine = models.CharField(
        db_column='RESPONSABILE_ORIGINE',
        max_length=500,
        blank=True,
        null=True)  # Field name made lowercase.
    committenti = models.CharField(
        db_column='COMMITTENTI',
        max_length=500,
        blank=False,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    anno = models.IntegerField(db_column='ANNO', blank=False, null=True)
    # Field name made lowercase.
    durata_mesi = models.IntegerField(
        db_column='DURATA_MESI', blank=False, null=True)
    # Field name made lowercase.
    importo_euro = models.FloatField(
        db_column='IMPORTO_EURO', blank=False, null=True)
    # Field name made lowercase.
    strumentazione = models.TextField(
        db_column='STRUMENTAZIONE', blank=False, null=True)

    class Meta:
        managed = True
        db_table = 'LABORATORIO_SERVIZI_EROGATI'


class LaboratorioServiziOfferti(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    nome_servizio = models.TextField(
        db_column='NOME_SERVIZIO', blank=False, null=True)
    descrizione_servizio = models.TextField(
        db_column='DESCRIZIONE_SERVIZIO',
        blank=False,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_SERVIZI_OFFERTI'


class LaboratorioTipologiaRischio(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        "LaboratorioDatiBase",
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    tipologia_rischio_origine = models.CharField(
        db_column='TIPOLOGIA_RISCHIO_ORIGINE',
        max_length=500,
        blank=True,
        null=True)  # Field name made lowercase.
    id_tipologia_rischio = models.ForeignKey(
        "TipologiaRischio",
        models.CASCADE,
        db_column='ID_TIPOLOGIA_RISCHIO',
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LABORATORIO_TIPOLOGIA_RISCHIO'


class LaboratorioUbicazione(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_laboratorio_dati = models.ForeignKey(
        LaboratorioDatiBase,
        models.CASCADE,
        db_column='ID_LABORATORIO_DATI',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    edificio = models.CharField(
        db_column='EDIFICIO',
        max_length=200,
        blank=False,
        null=True)
    # Field name made lowercase.
    piano = models.CharField(
        db_column='PIANO',
        max_length=100,
        blank=False,
        null=True)
    sede_principale = models.CharField(
        db_column='SEDE_PRINCIPALE',
        max_length=10,
        blank=False,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    note = models.TextField(db_column='NOTE', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'LABORATORIO_UBICAZIONE'


class Personale(InsModAbstract):

    id_ab = models.IntegerField(db_column='ID_AB', unique=True)
    cd_esterno = models.CharField(
        db_column='CD_ESTERNO',
        max_length=60,
        blank=True,
        null=True)

    matricola = models.CharField(
        db_column='MATRICOLA',
        unique=True,
        max_length=6)
    matricola_sp = models.CharField(
        db_column='MATRICOLA_SP',
        max_length=255,
        blank=True,
        null=True)

    nome = models.CharField(
        db_column='NOME',
        max_length=100,
        blank=True,
        null=True)

    cognome = models.CharField(
        db_column='COGNOME',
        max_length=100,
        blank=True,
        null=True)
    middle_name = models.CharField(
        db_column='MIDDLE_NAME',
        max_length=100,
        blank=True,
        null=True)
    cod_fis = models.CharField(
        db_column='COD_FIS',
        unique=True,
        max_length=16,
        blank=True,
        null=True)
    cd_genere = models.CharField(
        db_column='CD_GENERE',
        max_length=1,
        blank=True,
        null=True)

    dt_nascita = models.DateField(
        db_column='DT_NASCITA', blank=True, null=True)

    id_comu_nasc = models.IntegerField(
        db_column='ID_COMU_NASC', blank=True, null=True)
    ds_cittstra_nasc = models.CharField(
        db_column='DS_CITTSTRA_NASC',
        max_length=255,
        blank=True,
        null=True)
    ds_comune_nasc = models.CharField(
        db_column='DS_COMUNE_NASC',
        max_length=255,
        blank=True,
        null=True)
    ds_prov_nasc = models.CharField(
        db_column='DS_PROV_NASC',
        max_length=255,
        blank=True,
        null=True)
    cd_sigla_nasc = models.CharField(
        db_column='CD_SIGLA_NASC',
        max_length=2,
        blank=True,
        null=True)
    id_nazione_nasc = models.IntegerField(
        db_column='ID_NAZIONE_NASC', blank=True, null=True)
    ds_nazi_nasc = models.CharField(
        db_column='DS_NAZI_NASC',
        max_length=100,
        blank=True,
        null=True)
    ds_nazi_breve_nasc = models.CharField(
        db_column='DS_NAZI_BREVE_NASC',
        max_length=20,
        blank=True,
        null=True)
    id_comu_res = models.ForeignKey(
        ComuniAll,
        models.DO_NOTHING,
        db_column='ID_COMU_RES',
        blank=True,
        null=True)
    ds_comune_res = models.CharField(
        db_column='DS_COMUNE_RES',
        max_length=255,
        blank=True,
        null=True)
    cd_cap_res = models.CharField(
        db_column='CD_CAP_RES',
        max_length=5,
        blank=True,
        null=True)
    indirizzo_res = models.CharField(
        db_column='INDIRIZZO_RES',
        max_length=255,
        blank=True,
        null=True)
    num_civico_res = models.CharField(
        db_column='NUM_CIVICO_RES',
        max_length=15,
        blank=True,
        null=True)
    cd_sigla_res = models.CharField(
        db_column='CD_SIGLA_RES',
        max_length=2,
        blank=True,
        null=True)

    id_comu_dom = models.IntegerField(
        db_column='ID_COMU_DOM', blank=True, null=True)
    ds_comune_dom = models.CharField(
        db_column='DS_COMUNE_DOM',
        max_length=255,
        blank=True,
        null=True)
    cd_cap_dom = models.CharField(
        db_column='CD_CAP_DOM',
        max_length=5,
        blank=True,
        null=True)
    indirizzo_dom = models.CharField(
        db_column='INDIRIZZO_DOM',
        max_length=255,
        blank=True,
        null=True)
    num_civico_dom = models.CharField(
        db_column='NUM_CIVICO_DOM',
        max_length=15,
        blank=True,
        null=True)
    cd_sigla_dom = models.CharField(
        db_column='CD_SIGLA_DOM',
        max_length=2,
        blank=True,
        null=True)

    cd_comparto = models.CharField(db_column='CD_COMPARTO', max_length=1)
    ds_comparto = models.CharField(
        db_column='DS_COMPARTO',
        max_length=40,
        blank=True,
        null=True)

    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4)
    ds_ruolo = models.CharField(
        db_column='DS_RUOLO',
        max_length=40,
        blank=True,
        null=True)
    ds_ruolo_locale = models.CharField(
        db_column='DS_RUOLO_LOCALE',
        max_length=40,
        blank=True,
        null=True)
    peso_ruolo = models.DecimalField(
        db_column='PESO_RUOLO',
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True)

    dt_rap_ini = models.DateField(
        db_column='DT_RAP_INI', blank=True, null=True)

    dt_rap_fin = models.DateField(
        db_column='DT_RAP_FIN', blank=True, null=True)

    cd_ssd = models.CharField(
        db_column='CD_SSD',
        max_length=12,
        blank=True,
        null=True)

    ds_ssd = models.CharField(
        db_column='DS_SSD',
        max_length=100,
        blank=True,
        null=True)

    cd_fac = models.CharField(
        db_column='CD_FAC',
        max_length=10,
        blank=True,
        null=True)

    ds_fac = models.CharField(
        db_column='DS_FAC',
        max_length=255,
        blank=True,
        null=True)

    cd_uo_aff_org = models.ForeignKey(
        'UnitaOrganizzativa',
        models.DO_NOTHING,
        db_column='CD_UO_AFF_ORG',
        blank=True,
        null=True)  # Field name made lowercase.

    ds_aff_org = models.CharField(
        db_column='DS_AFF_ORG',
        max_length=255,
        blank=True,
        null=True)
    ds_aff_org_breve = models.CharField(
        db_column='DS_AFF_ORG_BREVE',
        max_length=50,
        blank=True,
        null=True)

    cd_csa_aff_org2 = models.CharField(
        db_column='CD_CSA_AFF_ORG2',
        max_length=6,
        blank=True,
        null=True)  # Field name made lowercase.

    ds_aff_org2 = models.CharField(
        db_column='DS_AFF_ORG2',
        max_length=255,
        blank=True,
        null=True)
    ds_aff_org2_breve = models.CharField(
        db_column='DS_AFF_ORG2_BREVE',
        max_length=50,
        blank=True,
        null=True)

    cd_csa_aff_org3 = models.CharField(
        db_column='CD_CSA_AFF_ORG3',
        max_length=6,
        blank=True,
        null=True)  # Field name made lowercase.

    ds_aff_org3 = models.CharField(
        db_column='DS_AFF_ORG3',
        max_length=255,
        blank=True,
        null=True)
    ds_aff_org3_breve = models.CharField(
        db_column='DS_AFF_ORG3_BREVE',
        max_length=50,
        blank=True,
        null=True)

    cd_csa_aff_org4 = models.CharField(
        db_column='CD_CSA_AFF_ORG4',
        max_length=6,
        blank=True,
        null=True)  # Field name made lowercase.

    ds_aff_org4 = models.CharField(
        db_column='DS_AFF_ORG4',
        max_length=255,
        blank=True,
        null=True)
    ds_aff_org4_breve = models.CharField(
        db_column='DS_AFF_ORG4_BREVE',
        max_length=50,
        blank=True,
        null=True)

    sede = models.CharField(
        db_column='SEDE',
        max_length=6,
        blank=True,
        null=True)

    ds_sede = models.CharField(
        db_column='DS_SEDE',
        max_length=255,
        blank=True,
        null=True)
    ds_sede_breve = models.CharField(
        db_column='DS_SEDE_BREVE',
        max_length=50,
        blank=True,
        null=True)

    profilo = models.CharField(
        db_column='PROFILO',
        max_length=11,
        blank=True,
        null=True)
    ds_profilo = models.CharField(
        db_column='DS_PROFILO',
        max_length=100,
        blank=True,
        null=True)
    ds_profilo_breve = models.CharField(
        db_column='DS_PROFILO_BREVE',
        max_length=50,
        blank=True,
        null=True)
    cd_ateneo_corr = models.CharField(
        db_column='CD_ATENEO_CORR',
        max_length=10,
        blank=True,
        null=True)
    ds_ateneo_corr = models.CharField(
        db_column='DS_ATENEO_CORR',
        max_length=255,
        blank=True,
        null=True)

    dt_ini_rap_univ = models.DateField(
        db_column='DT_INI_RAP_UNIV', blank=True, null=True)

    dt_fin_rap_univ = models.DateField(
        db_column='DT_FIN_RAP_UNIV', blank=True, null=True)

    telrif = models.CharField(
        db_column='TELRIF',
        max_length=255,
        blank=True,
        null=True)

    email = models.CharField(
        db_column='EMAIL',
        max_length=255,
        blank=True,
        null=True)

    urlcv = models.URLField(
        db_column='URLCV',
        max_length=255,
        blank=True,
        null=True)
    fl_docente = models.PositiveIntegerField(
        db_column='FL_DOCENTE', blank=True, null=True)
    cd_anagrafico = models.CharField(
        db_column='CD_ANAGRAFICO',
        max_length=20,
        blank=True,
        null=True)

    inquadr = models.CharField(
        db_column='INQUADR',
        max_length=50,
        blank=True,
        null=True)

    badge = models.CharField(
        db_column='BADGE',
        max_length=255,
        blank=True,
        null=True)

    tempo = models.CharField(
        db_column='TEMPO',
        max_length=1,
        blank=True,
        null=True)

    id_contratto = models.IntegerField(
        db_column='ID_CONTRATTO', blank=True, null=True)

    flg_cessato = models.IntegerField(
        db_column='FLG_CESSATO', blank=True, null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_personale',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_personale',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    # Field name made lowercase.
    cv_full_it = models.TextField(
        db_column='CV_FULL_IT', blank=True, null=True)

    # Field name made lowercase.
    cv_short_it = models.TextField(
        db_column='CV_SHORT_IT', blank=True, null=True)

    # Field name made lowercase.
    cv_full_eng = models.TextField(
        db_column='CV_FULL_ENG', blank=True, null=True)

    # Field name made lowercase.
    cv_short_eng = models.TextField(
        db_column='CV_SHORT_ENG', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PERSONALE'

    def __str__(self): # pragma: no cover
        return '{} {} [{}]'.format(self.cognome,
                                   self.nome, self.matricola)



class PersonaleAttivoTuttiRuoli(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_ab = models.BigIntegerField(db_column='ID_AB', blank=True, null=True)  # Field name made lowercase.
    matricola = models.CharField(db_column='MATRICOLA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_fis = models.CharField(db_column='COD_FIS', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cd_ruolo = models.CharField(db_column='CD_RUOLO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ds_ruolo = models.CharField(db_column='DS_RUOLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ds_ruolo_breve = models.CharField(db_column='DS_RUOLO_BREVE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cd_tipo_ruolo = models.CharField(db_column='CD_TIPO_RUOLO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_tipo_ruolo = models.CharField(db_column='DS_TIPO_RUOLO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    cd_inquadr = models.CharField(db_column='CD_INQUADR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ds_inquadr = models.CharField(db_column='DS_INQUADR', max_length=80, blank=True, null=True)  # Field name made lowercase.
    cd_uo_aff_org = models.ForeignKey('UnitaOrganizzativa', models.DO_NOTHING, db_column='CD_UO_AFF_ORG', blank=True,null=True)  # Field name made lowercase.
    ds_aff_org = models.CharField(db_column='DS_AFF_ORG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ds_aff_org_breve = models.CharField(db_column='DS_AFF_ORG_BREVE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fl_tipo_rap = models.FloatField(db_column='FL_TIPO_RAP', blank=True, null=True)  # Field name made lowercase.
    cd_ssd = models.CharField(db_column='CD_SSD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ds_ssd = models.CharField(db_column='DS_SSD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ds_ssd_breve = models.CharField(db_column='DS_SSD_BREVE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    area_ssd = models.CharField(db_column='AREA_SSD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ds_area_ssd = models.CharField(db_column='DS_AREA_SSD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cd_riferimento = models.CharField(db_column='CD_RIFERIMENTO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ds_riferimento = models.CharField(db_column='DS_RIFERIMENTO', max_length=120, blank=True, null=True)  # Field name made lowercase.
    peso_inc = models.IntegerField(db_column='PESO_INC', blank=True, null=True)  # Field name made lowercase.
    peso_ric = models.IntegerField(db_column='PESO_RIC', blank=True, null=True)  # Field name made lowercase.
    sede = models.CharField(db_column='SEDE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ds_sede = models.CharField(db_column='DS_SEDE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt_rap_ini = models.DateTimeField(db_column='DT_RAP_INI', blank=True, null=True)  # Field name made lowercase.
    cd_profilo = models.CharField(db_column='CD_PROFILO', max_length=11, blank=True, null=True)  # Field name made lowercase.
    ds_profilo = models.CharField(db_column='DS_PROFILO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fl_docente = models.IntegerField(db_column='FL_DOCENTE', blank=True, null=True)  # Field name made lowercase.
    cd_onorifico = models.CharField(db_column='CD_ONORIFICO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ds_onorifico = models.CharField(db_column='DS_ONORIFICO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    user_mod_id = models.CharField(db_column='USER_MOD_ID', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PERSONALE_ATTIVO_TUTTI_RUOLI'




class PersonaleUoTipoContatto(models.Model):
    # Field name made lowercase.
    cod_contatto = models.CharField(
        db_column='COD_CONTATTO',
        primary_key=True,
        max_length=20)
    # Field name made lowercase.
    descr_contatto = models.CharField(
        db_column='DESCR_CONTATTO', max_length=200)

    class Meta:
        managed = True
        db_table = 'PERSONALE_UO_TIPO_CONTATTO'


class UnitaOrganizzativaContatti(models.Model):
    id_ab = models.OneToOneField(
        UnitaOrganizzativa,
        models.DO_NOTHING,
        db_column='ID_AB',
        primary_key=True,
        to_field='id_ab')  # Field name made lowercase.
    cd_tipo_cont = models.ForeignKey(
        PersonaleUoTipoContatto,
        models.DO_NOTHING,
        db_column='CD_TIPO_CONT')  # Field name made lowercase.
    # Field name made lowercase.
    contatto = models.CharField(
        db_column='CONTATTO',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    prg_priorita = models.IntegerField(db_column='PRG_PRIORITA')
    denominazione = models.CharField(
        db_column='DENOMINAZIONE',
        max_length=255,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    dt_fine_val = models.DateTimeField(
        db_column='DT_FINE_VAL', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'UNITA_ORGANIZZATIVA_CONTATTI'
        unique_together = (('id_ab', 'cd_tipo_cont', 'prg_priorita'),)


class PersonaleContatti(models.Model):

    # Field name made lowercase.
    id_ab = models.IntegerField(db_column='ID_AB', primary_key=True)
    cod_fis = models.ForeignKey(
        Personale,
        models.DO_NOTHING,
        db_column='COD_FIS',
        blank=True,
        null=True,
        to_field='cod_fis',
        related_name='personalecontatti')  # Field name made lowercase.
    cd_tipo_cont = models.ForeignKey(
        'PersonaleUoTipoContatto',
        models.DO_NOTHING,
        db_column='CD_TIPO_CONT')  # Field name made lowercase.
    # Field name made lowercase.
    contatto = models.CharField(
        db_column='CONTATTO',
        max_length=255,
        blank=True,
        null=True)
    # Field name made lowercase.
    prg_priorita = models.IntegerField(db_column='PRG_PRIORITA')
    # Field name made lowercase.
    dt_ins_mod = models.DateField(
        db_column='DT_INS_MOD', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PERSONALE_CONTATTI'
        unique_together = (('id_ab', 'cd_tipo_cont', 'prg_priorita'),)


class PersonalePrioritaRuolo(models.Model):
    cd_ruolo = models.CharField(db_column='CD_RUOLO', primary_key=True, max_length=50)  # Field name made lowercase.
    ds_ruolo = models.CharField(db_column='DS_RUOLO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    priorita = models.IntegerField(db_column='PRIORITA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PERSONALE_PRIORITA_RUOLO'

class PubblicazioneAutori(models.Model):
    # Field name made lowercase.
    item = models.ForeignKey(
        'PubblicazioneDatiBase',
        models.CASCADE,
        db_column='ITEM_ID')
    codice_fiscale = models.CharField(
        db_column='CODICE_FISCALE',
        max_length=16,
        blank=True,
        null=True)  # Field name made lowercase.
    id_ab = models.ForeignKey(
        Personale,
        models.DO_NOTHING,
        db_column='ID_AB',
        blank=True,
        null=True,
        to_field='id_ab')  # Field name made lowercase.
    # Field name made lowercase.
    first_name = models.CharField(
        db_column='FIRST_NAME',
        max_length=1020,
        blank=True,
        null=True)
    # Field name made lowercase.
    last_name = models.CharField(
        db_column='LAST_NAME',
        max_length=1020,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'PUBBLICAZIONE_AUTORI'


class PubblicazioneCollection(models.Model):
    # Field name made lowercase.
    collection_id = models.IntegerField(
        db_column='COLLECTION_ID', primary_key=True)
    community = models.ForeignKey(
        'PubblicazioneCommunity',
        models.DO_NOTHING,
        db_column='COMMUNITY_ID',
        blank=True,
        null=True)  # Field name made lowercase.
    collection_name = models.CharField(
        db_column='COLLECTION_NAME',
        max_length=512,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    type_miur = models.CharField(
        db_column='TYPE_MIUR',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'PUBBLICAZIONE_COLLECTION'


class PubblicazioneCommunity(models.Model):
    # Field name made lowercase.
    community_id = models.IntegerField(
        db_column='COMMUNITY_ID', primary_key=True)
    community_name = models.CharField(
        db_column='COMMUNITY_NAME',
        max_length=512,
        blank=True,
        null=True)  # Field name made lowercase.
    parent_community_id = models.IntegerField(
        db_column='PARENT_COMMUNITY_ID',
        blank=True,
        null=True)  # Field name made lowercase.
    parent_community_name = models.CharField(
        db_column='PARENT_COMMUNITY_NAME',
        max_length=512,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PUBBLICAZIONE_COMMUNITY'


class PubblicazioneDatiBase(models.Model):
    # Field name made lowercase.
    item_id = models.IntegerField(db_column='ITEM_ID', primary_key=True)
    # Field name made lowercase.
    title = models.TextField(db_column='TITLE', blank=True, null=True)
    # Field name made lowercase.
    des_abstract = models.TextField(
        db_column='DES_ABSTRACT', blank=True, null=True)
    # Field name made lowercase.
    des_abstracteng = models.TextField(
        db_column='DES_ABSTRACTENG', blank=True, null=True)
    # Field name made lowercase.
    lan_iso = models.CharField(
        db_column='LAN_ISO',
        max_length=200,
        blank=True,
        null=True)
    lan_iso_i18n = models.CharField(
        db_column='LAN_ISO_I18N',
        max_length=400,
        blank=True,
        null=True)  # Field name made lowercase.
    collection = models.ForeignKey(
        PubblicazioneCollection,
        models.DO_NOTHING,
        db_column='COLLECTION_ID',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    date_issued_year = models.IntegerField(
        db_column='DATE_ISSUED_YEAR', blank=True, null=True)
    pubblicazione = models.CharField(
        db_column='PUBBLICAZIONE',
        max_length=1024,
        blank=True,
        null=True)  # Field name made lowercase.
    label_pubblicazione = models.CharField(
        db_column='LABEL_PUBBLICAZIONE',
        max_length=100,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    contributors = models.TextField(
        db_column='CONTRIBUTORS', blank=True, null=True)
    # Field name made lowercase.
    url_pubblicazione = models.URLField(
        db_column='URL_PUBBLICAZIONE', max_length=500, blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'PUBBLICAZIONE_DATI_BASE'


class RicercaAster1(InsModAbstract):

    descrizione = models.TextField(db_column='DESCRIZIONE')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_ra1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_ra1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    ricerca_erc0_cod = models.ForeignKey(
        'RicercaErc0',
        models.PROTECT,
        db_column='RICERCA_ERC0_COD',
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_ASTER1'

    def __str__(self): # pragma: no cover
        return '{}'.format(self.descrizione)


class RicercaAster2(InsModAbstract):

    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=200)
    ricerca_aster1 = models.ForeignKey(
        RicercaAster1,
        models.DO_NOTHING,
        db_column='RICERCA_ASTER1_ID')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_ra2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_ra2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_ASTER2'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.ricerca_aster1,
                              self.descrizione)


class RicercaDocenteGruppo(InsModAbstract):

    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)

    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(
        Personale,
        models.CASCADE,
        db_column='PERSONALE_ID',
        blank=True,
        null=True)
    ricerca_gruppo = models.ForeignKey(
        'RicercaGruppo',
        models.CASCADE,
        db_column='RICERCA_GRUPPO_ID')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_DOCENTE_GRUPPO'

    def __str__(self): # pragma: no cover
        return '{} [{}]'.format(self.personale,
                                self.ricerca_gruppo.nome)


class RicercaDocenteLineaApplicata(InsModAbstract):

    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)

    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(
        Personale,
        models.CASCADE,
        db_column='PERSONALE_ID',
        blank=True,
        null=True)
    ricerca_linea_applicata = models.ForeignKey(
        'RicercaLineaApplicata',
        models.CASCADE,
        db_column='RICERCA_LINEA_APPLICATA_ID',
        blank=True,
        null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_DOCENTE_LINEA_APPLICATA'


class RicercaDocenteLineaBase(InsModAbstract):

    dt_inizio = models.DateField(db_column='DT_INIZIO', blank=True, null=True)

    dt_fine = models.DateField(db_column='DT_FINE', blank=True, null=True)
    personale = models.ForeignKey(
        Personale,
        models.CASCADE,
        db_column='PERSONALE_ID',
        blank=True,
        null=True)
    ricerca_linea_base = models.ForeignKey(
        'RicercaLineaBase',
        models.CASCADE,
        db_column='RICERCA_LINEA_BASE_ID',
        blank=True,
        null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rdlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rdlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_DOCENTE_LINEA_BASE'


class RicercaErc0(models.Model):
    # Field name made lowercase.
    erc0_cod = models.CharField(
        db_column='ERC0_COD',
        primary_key=True,
        max_length=2)
    # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100)
    description_en = models.CharField(
        db_column='DESCRIPTION_EN',
        max_length=100,
        blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'RICERCA_ERC0'


class RicercaErc1(InsModAbstract):

    cod_erc1 = models.CharField(
        db_column='COD_ERC1',
        unique=True,
        max_length=40)

    descrizione = models.TextField(db_column='DESCRIZIONE')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_re1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_re1',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    ricerca_erc0_cod = models.ForeignKey(
        RicercaErc0,
        models.PROTECT,
        db_column='RICERCA_ERC0_COD',
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_ERC1'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.cod_erc1,
                              self.descrizione)


class RicercaErc2(InsModAbstract):

    cod_erc2 = models.CharField(
        db_column='COD_ERC2',
        unique=True,
        max_length=60)

    descrizione = models.TextField(db_column='DESCRIZIONE')
    ricerca_erc1 = models.ForeignKey(
        RicercaErc1,
        models.PROTECT,
        db_column='RICERCA_ERC1_ID',
        blank=True,
        null=True)
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_re2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_re2',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_ERC2'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.cod_erc2,
                              self.descrizione)


class RicercaGruppo(InsModAbstract):

    nome = models.CharField(db_column='NOME', max_length=200)

    descrizione = models.TextField(db_column='DESCRIZIONE')
    ricerca_erc1 = models.ForeignKey(RicercaErc1, models.SET_NULL, db_column='RICERCA_ERC1_ID', blank=True, null=True)  # Field name made lowercase.
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rg',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_GRUPPO'

    def __str__(self): # pragma: no cover
        return '{}'.format(self.nome)


class RicercaLineaApplicata(InsModAbstract, VisibileModAbstract):

    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(
        db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
        blank=True,
        null=True)

    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    ricerca_aster2 = models.ForeignKey(
        RicercaAster2,
        models.DO_NOTHING,
        db_column='RICERCA_ASTER2_ID')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rla',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_LINEA_APPLICATA'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.ricerca_aster2, self.descrizione)


class RicercaLineaBase(InsModAbstract, VisibileModAbstract):

    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(
        db_column='DESCR_PUBBLICAZ_PROG_BREVETTO',
        blank=True,
        null=True)

    anno = models.IntegerField(db_column='ANNO', blank=True, null=True)
    ricerca_erc2 = models.ForeignKey(RicercaErc2, models.DO_NOTHING,
                                     db_column='RICERCA_ERC2_ID')
    user_ins = models.ForeignKey(get_user_model(),
                                 related_name='user_ins_rlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    user_mod = models.ForeignKey(get_user_model(),
                                 related_name='user_mod_rlb',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RICERCA_LINEA_BASE'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.ricerca_erc2, self.descrizione)


class TerritorioIt(models.Model):
    cd_catasto = models.OneToOneField(
        ComuniAll,
        models.DO_NOTHING,
        db_column='CD_CATASTO',
        primary_key=True)

    cd_istat = models.CharField(
        db_column='CD_ISTAT',
        max_length=6,
        blank=True,
        null=True)
    ds_comune = models.CharField(
        db_column='DS_COMUNE',
        max_length=255,
        blank=True,
        null=True)

    cd_sigla = models.CharField(
        db_column='CD_SIGLA',
        max_length=2,
        blank=True,
        null=True)
    ds_provincia = models.CharField(
        db_column='DS_PROVINCIA',
        max_length=255,
        blank=True,
        null=True)
    cd_770_regio = models.CharField(
        db_column='CD_770_REGIO',
        max_length=2,
        blank=True,
        null=True)
    ds_regione = models.CharField(
        db_column='DS_REGIONE',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'TERRITORIO_IT'

    def __str__(self): # pragma: no cover
        return '{} {}'.format(self.cd_catasto, self.cd_istat)


class BrevettoDirittiCommerciali(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_diritto = models.CharField(
        db_column='DESCR_DIRITTO', max_length=1000)

    def __str__(self): # pragma: no cover
        return self.descr_diritto

    class Meta:
        managed = True
        db_table = 'BREVETTO_DIRITTI_COMMERCIALI'


class BrevettoTerritori(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    territorio = models.CharField(db_column='TERRITORIO', max_length=80)

    def __str__(self): # pragma: no cover
        return self.territorio

    class Meta:
        managed = True
        db_table = 'BREVETTO_TERRITORI'



class BrevettoDisponibilita(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_disponibilita = models.CharField(
        db_column='DESCR_DISPONIBILITA', max_length=1000)

    def __str__(self): # pragma: no cover
        return self.descr_disponibilita

    class Meta:
        managed = True
        db_table = 'BREVETTO_DISPONIBILITA'

class TipologiaAreaTecnologica(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_area_ita = models.CharField(
        db_column='DESCR_AREA_ITA', max_length=1000)
    descr_area_eng = models.CharField(
        db_column='DESCR_AREA_ENG',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.

    def __str__(self): # pragma: no cover
        return self.descr_area_ita

    class Meta:
        managed = True
        db_table = 'TIPOLOGIA_AREA_TECNOLOGICA'


class BrevettoStatusLegale(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_status = models.CharField(db_column='DESCR_STATUS', max_length=1000)


    def __str__(self): # pragma: no cover
        return self.descr_status

    class Meta:
        managed = True
        db_table = 'BREVETTO_STATUS_LEGALE'


class BrevettoDatiBase(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    id_univoco = models.CharField(
        db_column='ID_UNIVOCO',
        max_length=500,
        unique=True)
    # Field name made lowercase.
    titolo = models.TextField(db_column='TITOLO')
    url_immagine = models.URLField(
        db_column='URL_IMMAGINE',
        max_length=2000,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    breve_descrizione = models.TextField(db_column='BREVE_DESCRIZIONE')
    id_area_tecnologica = models.ForeignKey(
        TipologiaAreaTecnologica,
        models.SET_NULL,
        db_column='ID_AREA_TECNOLOGICA',
        blank=True,
        null=True)  # Field name made lowercase.
    url_knowledge_share = models.URLField(
        db_column='URL_KNOWLEDGE_SHARE',
        max_length=2000,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    applicazioni = models.TextField(
        db_column='APPLICAZIONI', blank=True, null=True)
    # Field name made lowercase.
    vantaggi = models.TextField(db_column='VANTAGGI', blank=True, null=True)
    trl_iniziale = models.PositiveSmallIntegerField(
        db_column='TRL_INIZIALE',
        blank=True,
        null=True)
    trl_aggiornato = models.PositiveSmallIntegerField(
        db_column='TRL_AGGIORNATO',
        blank=True,
        null=True)
    proprieta = models.TextField(db_column='PROPRIETA')
    id_status_legale = models.ForeignKey(
        BrevettoStatusLegale,
        models.SET_NULL,
        db_column='ID_STATUS_LEGALE',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_priorita = models.DateField(
        db_column='DATA_PRIORITA', blank=True, null=True)
    # Field name made lowercase.
    territorio = models.ForeignKey(
        BrevettoTerritori,
        models.SET_NULL,
        db_column='TERRITORIO',
        blank=True,
        null=True)
    id_diritto_commerciale = models.ForeignKey(
        BrevettoDirittiCommerciali,
        models.SET_NULL,
        db_column='ID_DIRITTO_COMMERCIALE',
        blank=True,
        null=True)  # Field name made lowercase.
    id_disponibilita = models.ForeignKey(
        BrevettoDisponibilita,
        models.SET_NULL,
        db_column='ID_DISPONIBILITA',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    area_ks = models.CharField(
        db_column='AREA_KS',
        max_length=2000,
        blank=True,
        null=True)
    nome_file_logo = models.FileField(
        upload_to=patents_media_path,
        validators=[validate_image_file_extension,
                    validate_file_size],
        db_column='NOME_FILE_LOGO',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.
    valorizzazione = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column='VALORIZZAZIONE')
    is_active = models.BooleanField(default=True, db_column='ATTIVO')
    ordinamento = models.IntegerField(default=10, db_column='ORDINE')

    class Meta:
        managed = True
        db_table = 'BREVETTO_DATI_BASE'
        ordering = ["ordinamento"]


class BrevettoInventori(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    id_brevetto = models.ForeignKey(
        BrevettoDatiBase,
        models.CASCADE,
        db_column='ID_BREVETTO',
        blank=True,
        null=True)  # Field name made lowercase.
    matricola_inventore = models.ForeignKey(
        'Personale',
        models.SET_NULL,
        db_column='MATRICOLA_INVENTORE',
        to_field='matricola',
        blank=True,
        null=True)  # Field name made lowercase.
    cognomenome_origine = models.CharField(
        db_column='COGNOMENOME_ORIGINE',
        max_length=200)  # Field name made lowercase.

    def __str__(self): # pragma: no cover
        return self.cognomenome_origine

    class Meta:
        managed = True
        db_table = 'BREVETTO_INVENTORI'


class SpinoffStartupAreaInnovazioneS3Calabria(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descr_area_s3 = models.CharField(
        db_column='DESCR_AREA_S3', max_length=1000)

    def __str__(self): # pragma: no cover
        return self.descr_area_s3

    class Meta:
        managed = True
        db_table = 'SPINOFF_STARTUP_AREA_INNOVAZIONE_S3_CALABRIA'


class SpinoffStartupDatiBase(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    piva = models.CharField(
        db_column='PIVA',
        max_length=30,
        validators=[validate_piva,],
        unique=True)
    nome_azienda = models.CharField(
        db_column='NOME_AZIENDA',
        max_length=1000)  # Field name made lowercase.
    nome_file_logo = models.FileField(
        upload_to=companies_media_path,
        validators=[validate_image_file_extension,
                    validate_file_size],
        db_column='NOME_FILE_LOGO',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    descrizione_ita = models.TextField(db_column='DESCRIZIONE_ITA')
    # Field name made lowercase.
    descrizione_eng = models.TextField(
        db_column='DESCRIZIONE_ENG', blank=True, null=True)
    url_sito_web = models.URLField(
        db_column='URL_SITO_WEB',
        max_length=4000,
        blank=True,
        null=True)  # Field name made lowercase.
    referente_unical = models.CharField(
        db_column='REFERENTE_UNICAL',
        max_length=1000)  # Field name made lowercase.
    matricola_referente_unical = models.ForeignKey(Personale,
        models.SET_NULL,
        to_field='matricola',
        db_column='MATRICOLA_REFERENTE_UNICAL',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    ceo = models.CharField(
        db_column='CEO',
        max_length=1000,
        blank=True,
        null=True)
    id_area_tecnologica = models.ForeignKey(
        'TipologiaAreaTecnologica',
        models.DO_NOTHING,
        db_column='ID_AREA_TECNOLOGICA')  # Field name made lowercase.
    id_area_innovazione_s3_calabria = models.ForeignKey(
        SpinoffStartupAreaInnovazioneS3Calabria,
        models.SET_NULL,
        db_column='ID_AREA_INNOVAZIONE_S3_CALABRIA',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    is_startup = models.BooleanField(
        db_column='IS_STARTUP', default=False)
    # Field name made lowercase.
    is_spinoff = models.BooleanField(
        db_column='IS_SPINOFF', default=False)
    is_active = models.BooleanField(default=True, db_column='ATTIVO')
    ordinamento = models.IntegerField(default=10, db_column='ORDINE')

    class Meta:
        managed = True
        db_table = 'SPINOFF_STARTUP_DATI_BASE'
        ordering = ["ordinamento"]



class SpinoffStartupDipartimento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_spinoff_startup_dati_base = models.ForeignKey(SpinoffStartupDatiBase, models.CASCADE, db_column='ID_SPINOFF_STARTUP_DATI_BASE')  # Field name made lowercase.
    nome_origine_dipartimento = models.CharField(db_column='NOME_ORIGINE_DIPARTIMENTO', max_length=1000)  # Field name made lowercase.
    id_didattica_dipartimento = models.ForeignKey(DidatticaDipartimento, models.CASCADE, db_column='ID_DIDATTICA_DIPARTIMENTO', blank=True, null=True)  # Field name made lowercase.

    def __str__(self): # pragma: no cover
        return self.nome_origine_dipartimento

    class Meta:
        managed = True
        db_table = 'SPINOFF_STARTUP_DIPARTIMENTO'


class ProgettoAmbitoTerritoriale(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    ambito_territoriale = models.CharField(
        db_column='AMBITO_TERRITORIALE', max_length=100)

    def __str__(self): # pragma: no cover
        return self.ambito_territoriale

    class Meta:
        managed = True
        db_table = 'PROGETTO_AMBITO_TERRITORIALE'


class ProgettoDatiBase(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    anno_avvio = models.IntegerField(
        db_column='ANNO_AVVIO', blank=True, null=True)
    id_ambito_territoriale = models.ForeignKey(
        ProgettoAmbitoTerritoriale,
        models.SET_NULL,
        db_column='ID_AMBITO_TERRITORIALE',
        blank=True,
        null=True)  # Field name made lowercase.
    id_tipologia_programma = models.ForeignKey(
        'ProgettoTipologiaProgramma',
        models.SET_NULL,
        db_column='ID_TIPOLOGIA_PROGRAMMA',
        blank=True,
        null=True)  # Field name made lowercase.
    id_area_tecnologica = models.ForeignKey(
        'TipologiaAreaTecnologica',
        models.SET_NULL,
        db_column='ID_AREA_TECNOLOGICA',
        blank=True,
        null=True)  # Field name made lowercase.
    uo = models.ForeignKey(
        'UnitaOrganizzativa',
        models.DO_NOTHING,
        to_field='uo',
        db_column='UO',
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    titolo = models.CharField(
        db_column='TITOLO',
        max_length=4000,
        blank=True,
        null=True)
    # Field name made lowercase.
    descr_breve = models.TextField(
        db_column='DESCR_BREVE', blank=True, null=True)
    url_immagine = models.URLField(
        db_column='URL_IMMAGINE',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.
    # Field name made lowercase.
    abstract_ita = models.TextField(
        db_column='ABSTRACT_ITA', blank=True, null=True)
    # Field name made lowercase.
    abstract_eng = models.TextField(
        db_column='ABSTRACT_ENG', blank=True, null=True)
    url_sito_web = models.URLField(
        db_column='URL_SITO_WEB',
        max_length=1000,
        blank=True,
        null=True)  # Field name made lowercase.
    call = models.CharField(db_column='CALL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(default=True, db_column='ATTIVO')
    ordinamento = models.IntegerField(default=10, db_column='ORDINE')

    class Meta:
        managed = True
        db_table = 'PROGETTO_DATI_BASE'
        ordering = ["ordinamento"]


class ProgettoRicercatore(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola = models.ForeignKey(Personale, models.CASCADE,to_field='matricola', db_column='MATRICOLA', blank=True, null=True)  # Field name made lowercase.
    nome_origine = models.CharField(db_column='NOME_ORIGINE', max_length=1000)  # Field name made lowercase.
    id_progetto = models.ForeignKey(ProgettoDatiBase, models.CASCADE, db_column='ID_PROGETTO')  # Field name made lowercase.

    def __str__(self): # pragma: no cover
        return self.nome_origine

    class Meta:
        managed = True
        db_table = 'PROGETTO_RICERCATORE'


class ProgettoResponsabileScientifico(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    matricola = models.ForeignKey(
        Personale,
        models.CASCADE,
        to_field='matricola',
        db_column='MATRICOLA',
        blank=True,
        null=True)  # Field name made lowercase.
    nome_origine = models.CharField(
        db_column='NOME_ORIGINE',
        max_length=1000)  # Field name made lowercase.
    # Field name made lowercase.
    id_progetto = models.ForeignKey(ProgettoDatiBase, models.CASCADE, db_column='ID_PROGETTO')  # Field name made lowercase.

    def __str__(self): # pragma: no cover
        return self.nome_origine

    class Meta:
        managed = True
        db_table = 'PROGETTO_RESPONSABILE_SCIENTIFICO'


class ProgettoTipologiaProgramma(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome_programma = models.CharField(
        db_column='NOME_PROGRAMMA', max_length=1000)


    def __str__(self): # pragma: no cover
        return self.nome_programma

    class Meta:
        managed = True
        db_table = 'PROGETTO_TIPOLOGIA_PROGRAMMA'


class AltaFormazioneConsiglioScientificoEsterno(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_cons = models.CharField(db_column='NOME_CONS', max_length=1000)  # Field name made lowercase.
    ruolo_cons = models.CharField(db_column='RUOLO_CONS', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ente_cons = models.CharField(db_column='ENTE_CONS', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey('AltaFormazioneDatiBase', models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_ESTERNO'


class AltaFormazioneConsiglioScientificoInterno(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matricola_cons = models.ForeignKey('Personale', models.SET_NULL, db_column='MATRICOLA_CONS', blank=True, null=True)  # Field name made lowercase.
    nome_origine_cons = models.CharField(db_column='NOME_ORIGINE_CONS', max_length=1000)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey('AltaFormazioneDatiBase', models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_CONSIGLIO_SCIENTIFICO_INTERNO'


class AltaFormazioneDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    titolo_it = models.CharField(db_column='TITOLO_IT', max_length=512, blank=True, null=True)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=512, blank=True, null=True)  # Field name made lowercase.
    anno_rilevazione = models.IntegerField(db_column='ANNO_RILEVAZIONE', blank=True, null=True)  # Field name made lowercase.
    id_dipartiento_riferimento = models.ForeignKey('DidatticaDipartimento', models.DO_NOTHING,db_column='ID_DIPARTIENTO_RIFERIMENTO', blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_tipo_corso = models.ForeignKey('AltaFormazioneTipoCorso', models.SET_NULL, db_column='ID_ALTA_FORMAZIONE_TIPO_CORSO', blank=True, null=True)  # Field name made lowercase.
    lingua = models.CharField(db_column='LINGUA', max_length=512, blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_mod_erogazione = models.ForeignKey('AltaFormazioneModalitaErogazione', models.DO_NOTHING, db_column='ID_ALTA_FORMAZIONE_MOD_EROGAZIONE', blank=True, null=True)  # Field name made lowercase.
    ore = models.IntegerField(blank=True, null=True)
    mesi = models.IntegerField(blank=True, null=True)
    data_inizio = models.DateField(db_column='DATA_INIZIO', blank=True, null=True)  # Field name made lowercase.
    data_fine = models.DateField(db_column='DATA_FINE', blank=True, null=True)  # Field name made lowercase.
    sede_corso = models.CharField(db_column='SEDE_CORSO', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    num_min_partecipanti = models.IntegerField(db_column='NUM_MIN_PARTECIPANTI', blank=True, null=True)  # Field name made lowercase.
    num_max_partecipanti = models.IntegerField(db_column='NUM_MAX_PARTECIPANTI', blank=True, null=True)  # Field name made lowercase.
    uditori_ammessi = models.CharField(db_column='UDITORI_AMMESSI', max_length=200, blank=True, null=True)  # Field name made lowercase.
    num_max_uditori = models.IntegerField(db_column='NUM_MAX_UDITORI', blank=True, null=True)  # Field name made lowercase.
    requisiti_ammissione = models.TextField(db_column='REQUISITI_AMMISSIONE', blank=True, null=True)  # Field name made lowercase.
    titolo_rilasciato = models.TextField(db_column='TITOLO_RILASCIATO', blank=True, null=True)  # Field name made lowercase.
    doppio_titolo = models.TextField(db_column='DOPPIO_TITOLO', blank=True, null=True)  # Field name made lowercase.
    matricola_direttore_scientifico = models.ForeignKey('Personale', models.SET_NULL, to_field='matricola', db_column='MATRICOLA_DIRETTORE_SCIENTIFICO', blank=True, null=True)  # Field name made lowercase.
    nome_origine_direttore_scientifico = models.TextField(db_column='NOME_ORIGINE_DIRETTORE_SCIENTIFICO', blank=True, null=True)  # Field name made lowercase.
    quota_iscrizione = models.FloatField(db_column='QUOTA_ISCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    quota_uditori = models.FloatField(db_column='QUOTA_UDITORI', blank=True, null=True)  # Field name made lowercase.
    funzione_lavoro = models.TextField(db_column='FUNZIONE_LAVORO', blank=True, null=True)  # Field name made lowercase.
    obiettivi_formativi_summer_school = models.TextField(db_column='OBIETTIVI_FORMATIVI_SUMMER_SCHOOL', blank=True, null=True)  # Field name made lowercase.
    competenze = models.TextField(db_column='COMPETENZE', blank=True, null=True)  # Field name made lowercase.
    sbocchi_occupazionali = models.TextField(db_column='SBOCCHI_OCCUPAZIONALI', blank=True, null=True)  # Field name made lowercase.
    obiettivi_formativi_corso = models.TextField(db_column='OBIETTIVI_FORMATIVI_CORSO', blank=True, null=True)  # Field name made lowercase.
    modalita_svolgimento_prova_finale = models.TextField(db_column='MODALITA_SVOLGIMENTO_PROVA_FINALE', blank=True, null=True)  # Field name made lowercase.
    numero_moduli = models.FloatField(db_column='NUMERO_MODULI', blank=True, null=True)  # Field name made lowercase.
    stage_tirocinio = models.TextField(db_column='STAGE_TIROCINIO', blank=True, null=True)  # Field name made lowercase.
    ore_stage_tirocinio = models.IntegerField(db_column='ORE_STAGE_TIROCINIO', blank=True, null=True)  # Field name made lowercase.
    cfu_stage = models.IntegerField(db_column='CFU_STAGE', blank=True, null=True)  # Field name made lowercase.
    mesi_stage = models.IntegerField(db_column='MESI_STAGE', blank=True, null=True)  # Field name made lowercase.
    tipo_aziende_enti_tirocinio = models.TextField(db_column='TIPO_AZIENDE_ENTI_TIROCINIO', blank=True, null=True)  # Field name made lowercase.
    project_work = models.TextField(db_column='PROJECT_WORK', blank=True, null=True)  # Field name made lowercase.
    contenuti_tempi_criteri_cfu = models.TextField(db_column='CONTENUTI_TEMPI_CRITERI_CFU', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_DATI_BASE'
        unique_together = (('titolo_it', 'data_inizio'),)


class AltaFormazioneIncaricoDidattico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_alta_formazione_piano_didattico = models.ForeignKey('AltaFormazionePianoDidattico', models.SET_NULL, db_column='ID_ALTA_FORMAZIONE_PIANO_DIDATTICO', blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey(AltaFormazioneDatiBase, models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    modulo = models.TextField(db_column='MODULO', blank=True, null=True)  # Field name made lowercase.
    num_ore = models.CharField(db_column='NUM_ORE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    docente = models.CharField(db_column='DOCENTE', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    qualifica = models.CharField(db_column='QUALIFICA', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    ente = models.TextField(db_column='ENTE', blank=True, null=True)  # Field name made lowercase.
    tipologia = models.CharField(db_column='TIPOLOGIA', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_INCARICO_DIDATTICO'


class AltaFormazioneModalitaErogazione(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descrizione = models.CharField(db_column='DESCRIZIONE', max_length=1000)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_MODALITA_EROGAZIONE'


class AltaFormazioneModalitaSelezione(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_selezione = models.CharField(db_column='TIPO_SELEZIONE', max_length=100)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey(AltaFormazioneDatiBase, models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_MODALITA_SELEZIONE'


class AltaFormazionePartner(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    denominazione = models.CharField(db_column='DENOMINAZIONE', max_length=1000)  # Field name made lowercase.
    tipologia = models.CharField(db_column='TIPOLOGIA', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    sito_web = models.CharField(db_column='SITO_WEB', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey(AltaFormazioneDatiBase, models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_PARTNER'


class AltaFormazionePianoDidattico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modulo = models.TextField(db_column='MODULO')  # Field name made lowercase.
    ssd = models.CharField(db_column='SSD', max_length=500, blank=True, null=True)  # Field name made lowercase.
    num_ore = models.IntegerField(db_column='NUM_ORE', blank=True, null=True)  # Field name made lowercase.
    cfu = models.IntegerField(db_column='CFU', blank=True, null=True)  # Field name made lowercase.
    verifica_finale = models.IntegerField(db_column='VERIFICA_FINALE', blank=True, null=True)  # Field name made lowercase.
    id_alta_formazione_dati_base = models.ForeignKey(AltaFormazioneDatiBase, models.CASCADE, db_column='ID_ALTA_FORMAZIONE_DATI_BASE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_PIANO_DIDATTICO'


class AltaFormazioneTipoCorso(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_corso_descr = models.CharField(db_column='TIPO_CORSO_DESCR', max_length=256)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ALTA_FORMAZIONE_TIPO_CORSO'


class DidatticaCdsAltriDati(models.Model):
    regdid_id = models.OneToOneField(DidatticaRegolamento, models.DO_NOTHING, db_column='REGDID_ID', primary_key=True)  # Field name made lowercase.
    matricola_coordinatore = models.ForeignKey('Personale', models.SET_NULL, related_name='coordinatore', db_column='MATRICOLA_COORDINATORE', blank=True, null=True, to_field='matricola')  # Field name made lowercase.
    nome_origine_coordinatore = models.CharField(db_column='NOME_ORIGINE_COORDINATORE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    matricola_vice_coordinatore = models.ForeignKey('Personale', models.SET_NULL, related_name='vice_coordinatore', db_column='MATRICOLA_VICE_COORDINATORE', blank=True, null=True, to_field='matricola')  # Field name made lowercase.
    nome_origine_vice_coordinatore = models.CharField(db_column='NOME_ORIGINE_VICE_COORDINATORE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    # num_posti = models.IntegerField(db_column='NUM_POSTI', blank=True, null=True)  # Field name made lowercase.
    # modalita_iscrizione = models.TextField(db_column='MODALITA_ISCRIZIONE', blank=True, null=True)  # Field name made lowercase.
    manifesto_studi = models.FileField(
        upload_to=cds_manifesto_media_path,
        validators=[validate_pdf_file_extension,
                    validate_file_size],
        db_column='MANIFESTO_STUDI',
        max_length=255,
        blank=True,
        null=True)
    regolamento_didattico = models.FileField(
        upload_to=cds_regolamento_media_path,
        validators=[validate_pdf_file_extension,
                    validate_file_size],
        db_column='REGOLAMENTO_DIDATTICO',
        max_length=255,
        blank=True,
        null=True)
    ordinamento_didattico = models.FileField(
        upload_to=cds_ordinamento_media_path,
        validators=[validate_pdf_file_extension,
                    validate_file_size],
        db_column='ORDINAMENTO_DIDATTICO',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_ALTRI_DATI'


class DidatticaCdsGruppi(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_breve_it = models.CharField(db_column='DESCR_BREVE_IT', max_length=1000)  # Field name made lowercase.
    descr_breve_en = models.CharField(db_column='DESCR_BREVE_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    descr_lunga_it = models.TextField(db_column='DESCR_LUNGA_IT', blank=True, null=True)  # Field name made lowercase.
    descr_lunga_en = models.TextField(db_column='DESCR_LUNGA_EN', blank=True, null=True)  # Field name made lowercase.
    id_didattica_cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='ID_DIDATTICA_CDS')  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', default=10)  # Field name made lowercase.
    visibile = models.BooleanField(db_column='VISIBILE', default=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_GRUPPI'
        ordering = ('ordine',)

    def __str__(self): # pragma: no cover
        return self.descr_breve_it


class DidatticaCdsGruppiComponenti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_didattica_cds_gruppi = models.ForeignKey(DidatticaCdsGruppi, models.CASCADE, db_column='ID_DIDATTICA_CDS_GRUPPI')  # Field name made lowercase.
    matricola = models.ForeignKey(Personale, models.SET_NULL, db_column='MATRICOLA', to_field='matricola', blank=True, null=True)  # Field name made lowercase.
    cognome = models.CharField(db_column='COGNOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    funzione_it = models.CharField(db_column='FUNZIONE_IT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    funzione_en = models.CharField(db_column='FUNZIONE_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', default=10)  # Field name made lowercase.
    visibile = models.BooleanField(db_column='VISIBILE', default=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_GRUPPI_COMPONENTI'
        ordering = ('ordine',)

    def __str__(self): # pragma: no cover
        return f'{self.id_didattica_cds_gruppi} - {self.cognome} {self.nome}'


class DidatticaDipartimentoGruppi(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_breve_it = models.CharField(db_column='DESCR_BREVE_IT', max_length=1000)  # Field name made lowercase.
    descr_breve_en = models.CharField(db_column='DESCR_BREVE_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    descr_lunga_it = models.TextField(db_column='DESCR_LUNGA_IT', blank=True, null=True)  # Field name made lowercase.
    descr_lunga_en = models.TextField(db_column='DESCR_LUNGA_EN', blank=True, null=True)  # Field name made lowercase.
    id_didattica_dipartimento = models.ForeignKey(DidatticaDipartimento, models.DO_NOTHING, db_column='ID_DIDATTICA_DIPARTIMENTO')  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', default=10)  # Field name made lowercase.
    visibile = models.BooleanField(db_column='VISIBILE', default=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DIPARTIMENTO_GRUPPI'
        ordering = ('ordine',)


class DidatticaDipartimentoGruppiComponenti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_didattica_dipartimento_gruppi = models.ForeignKey(DidatticaDipartimentoGruppi, models.CASCADE, db_column='ID_DIDATTICA_DIPARTIMENTO_GRUPPI')  # Field name made lowercase.
    matricola = models.ForeignKey(Personale, models.SET_NULL, db_column='MATRICOLA', blank=True, null=True, to_field='matricola')  # Field name made lowercase.
    cognome = models.CharField(db_column='COGNOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    funzione_it = models.CharField(db_column='FUNZIONE_IT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    funzione_en = models.CharField(db_column='FUNZIONE_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', default=10)  # Field name made lowercase.
    visibile = models.BooleanField(db_column='VISIBILE', default=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_DIPARTIMENTO_GRUPPI_COMPONENTI'
        ordering = ('ordine',)


class DidatticaClasseLaurea(models.Model):
    cla_m_id = models.IntegerField(db_column='CLA_M_ID', primary_key=True)
    cla_miur_cod = models.CharField(db_column='CLA_MIUR_COD', max_length=20)
    cla_miur_des = models.CharField(db_column='CLA_MIUR_DES', max_length=1000)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CLASSE_LAUREA'


class SitoWebCdsDatiBase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # id_didattica_regolamento = models.ForeignKey(DidatticaRegolamento, models.DO_NOTHING, db_column='ID_DIDATTICA_REGOLAMENTO', blank=True, null=True, to_field='regdid_id')  # Field name made lowercase.
    aa = models.PositiveIntegerField(db_column='AA', blank=True, null=True )  # Field name made lowercase.
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID', blank=True, null=True, to_field='cds_id')  # Field name made lowercase.
    cds_cod = models.CharField(db_column='CDS_COD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # nome_corso_it = models.CharField(db_column='NOME_CORSO_IT', max_length=500)  # Field name made lowercase.
    # nome_corso_en = models.CharField(db_column='NOME_CORSO_EN', max_length=500, blank=True, null=True)  # Field name made lowercase.
    # classe_laurea_it = models.CharField(db_column='CLASSE_LAUREA_IT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # classe_laurea_en = models.CharField(db_column='CLASSE_LAUREA_EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # classe_laurea_interclasse_it = models.CharField(db_column='CLASSE_LAUREA_INTERCLASSE_IT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # classe_laurea_interclasse_en = models.CharField(db_column='CLASSE_LAUREA_INTERCLASSE_EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # lingua_it = models.CharField(db_column='LINGUA_IT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    # lingua_en = models.CharField(db_column='LINGUA_EN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    # durata = models.CharField(db_column='DURATA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    num_posti = models.IntegerField(db_column='NUM_POSTI', blank=True, null=True)  # Field name made lowercase.
    # link_video_cds_it = models.CharField(db_column='LINK_VIDEO_CDS_IT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    # link_video_cds_en = models.CharField(db_column='LINK_VIDEO_CDS_EN', max_length=500, blank=True, null=True)  # Field name made lowercase.
    descrizione_corso_it = models.TextField(db_column='DESCRIZIONE_CORSO_IT', blank=True, null=True)  # Field name made lowercase.
    descrizione_corso_en = models.TextField(db_column='DESCRIZIONE_CORSO_EN', blank=True, null=True)  # Field name made lowercase.
    accesso_corso_it = models.TextField(db_column='ACCESSO_CORSO_IT', blank=True, null=True)  # Field name made lowercase.
    accesso_corso_en = models.TextField(db_column='ACCESSO_CORSO_EN', blank=True, null=True)  # Field name made lowercase.
    obiettivi_corso_it = models.TextField(db_column='OBIETTIVI_CORSO_IT', blank=True, null=True)  # Field name made lowercase.
    obiettivi_corso_en = models.TextField(db_column='OBIETTIVI_CORSO_EN', blank=True, null=True)  # Field name made lowercase.
    sbocchi_professionali_it = models.TextField(db_column='SBOCCHI_PROFESSIONALI_IT', blank=True, null=True)  # Field name made lowercase.
    sbocchi_professionali_en = models.TextField(db_column='SBOCCHI_PROFESSIONALI_EN', blank=True, null=True)  # Field name made lowercase.
    tasse_contributi_esoneri_it = models.TextField(db_column='TASSE_CONTRIBUTI_ESONERI_IT', blank=True, null=True)  # Field name made lowercase.
    tasse_contributi_esoneri_en = models.TextField(db_column='TASSE_CONTRIBUTI_ESONERI_EN', blank=True, null=True)  # Field name made lowercase.
    borse_studio_it = models.TextField(db_column='BORSE_STUDIO_IT', blank=True, null=True)  # Field name made lowercase.
    borse_studio_en = models.TextField(db_column='BORSE_STUDIO_EN', blank=True, null=True)  # Field name made lowercase.
    agevolazioni_it = models.TextField(db_column='AGEVOLAZIONI_IT', blank=True, null=True)  # Field name made lowercase.
    agevolazioni_en = models.TextField(db_column='AGEVOLAZIONI_EN', blank=True, null=True)  # Field name made lowercase.
    corso_in_pillole_it = models.TextField(db_column='CORSO_IN_PILLOLE_IT', blank=True, null=True)  # Field name made lowercase.
    corso_in_pillole_en = models.TextField(db_column='CORSO_IN_PILLOLE_EN', blank=True, null=True)  # Field name made lowercase.
    cosa_si_studia_it = models.TextField(db_column='COSA_SI_STUDIA_IT', blank=True, null=True)  # Field name made lowercase.
    cosa_si_studia_en = models.TextField(db_column='COSA_SI_STUDIA_EN', blank=True, null=True)  # Field name made lowercase.
    come_iscriversi_it = models.TextField(db_column='COME_ISCRIVERSI_IT', blank=True, null=True)  # Field name made lowercase.
    come_iscriversi_en = models.TextField(db_column='COME_ISCRIVERSI_EN', blank=True, null=True)  # Field name made lowercase.
    # sito_web_it = models.CharField(db_column='SITO_WEB_IT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    # sito_web_en = models.CharField(db_column='SITO_WEB_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_DATI_BASE'


class SitoWebCdsDatiExcelTmpOld(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_corso_it = models.CharField(db_column='NOME_CORSO_IT', max_length=500)  # Field name made lowercase.
    classe_laurea_it = models.CharField(db_column='CLASSE_LAUREA_IT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    classe_laurea_interclasse = models.CharField(db_column='CLASSE_LAUREA_INTERCLASSE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lingua = models.CharField(db_column='LINGUA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    durata = models.CharField(db_column='DURATA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    num_posti = models.IntegerField(db_column='NUM_POSTI', blank=True, null=True)  # Field name made lowercase.
    link_video_cds = models.CharField(db_column='LINK_VIDEO_CDS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    slider_autopromo1 = models.TextField(db_column='SLIDER_AUTOPROMO1', blank=True, null=True)  # Field name made lowercase.
    slider_autopromo2 = models.TextField(db_column='SLIDER_AUTOPROMO2', blank=True, null=True)  # Field name made lowercase.
    slider_autopromo3 = models.TextField(db_column='SLIDER_AUTOPROMO3', blank=True, null=True)  # Field name made lowercase.
    descrizione_corso = models.TextField(db_column='DESCRIZIONE_CORSO', blank=True, null=True)  # Field name made lowercase.
    accesso_corso = models.TextField(db_column='ACCESSO_CORSO', blank=True, null=True)  # Field name made lowercase.
    obiettivi_corso = models.TextField(db_column='OBIETTIVI_CORSO', blank=True, null=True)  # Field name made lowercase.
    sbocchi_professionali = models.TextField(db_column='SBOCCHI_PROFESSIONALI', blank=True, null=True)  # Field name made lowercase.
    tasse_contributi_esoneri = models.TextField(db_column='TASSE_CONTRIBUTI_ESONERI', blank=True, null=True)  # Field name made lowercase.
    borse_studio = models.TextField(db_column='BORSE_STUDIO', blank=True, null=True)  # Field name made lowercase.
    agevolazioni = models.TextField(db_column='AGEVOLAZIONI', blank=True, null=True)  # Field name made lowercase.
    corso_in_pillole = models.TextField(db_column='CORSO_IN_PILLOLE', blank=True, null=True)  # Field name made lowercase.
    cosa_si_studia = models.TextField(db_column='COSA_SI_STUDIA', blank=True, null=True)  # Field name made lowercase.
    come_iscriversi = models.TextField(db_column='COME_ISCRIVERSI', blank=True, null=True)  # Field name made lowercase.
    descrizione_file1 = models.TextField(db_column='DESCRIZIONE_FILE1', blank=True, null=True)  # Field name made lowercase.
    link_file1 = models.TextField(db_column='LINK_FILE1', blank=True, null=True)  # Field name made lowercase.
    descrizione_file2 = models.TextField(db_column='DESCRIZIONE_FILE2', blank=True, null=True)  # Field name made lowercase.
    link_file2 = models.TextField(db_column='LINK_FILE2', blank=True, null=True)  # Field name made lowercase.
    descrizione_file3 = models.TextField(db_column='DESCRIZIONE_FILE3', blank=True, null=True)  # Field name made lowercase.
    link_file3 = models.TextField(db_column='LINK_FILE3', blank=True, null=True)  # Field name made lowercase.
    descrizione_file4 = models.TextField(db_column='DESCRIZIONE_FILE4', blank=True, null=True)  # Field name made lowercase.
    link_file4 = models.TextField(db_column='LINK_FILE4', blank=True, null=True)  # Field name made lowercase.
    descrizione_file5 = models.TextField(db_column='DESCRIZIONE_FILE5', blank=True, null=True)  # Field name made lowercase.
    link_file5 = models.TextField(db_column='LINK_FILE5', blank=True, null=True)  # Field name made lowercase.
    descrizione_file6 = models.TextField(db_column='DESCRIZIONE_FILE6', blank=True, null=True)  # Field name made lowercase.
    link_file6 = models.TextField(db_column='LINK_FILE6', blank=True, null=True)  # Field name made lowercase.
    ex_studente_profilo_1 = models.TextField(db_column='EX_STUDENTE_PROFILO_1', blank=True, null=True)  # Field name made lowercase.
    ex_studente_link_1 = models.TextField(db_column='EX_STUDENTE_LINK_1', blank=True, null=True)  # Field name made lowercase.
    ex_studente_profilo_2 = models.TextField(db_column='EX_STUDENTE_PROFILO_2', blank=True, null=True)  # Field name made lowercase.
    ex_studente_link_2 = models.TextField(db_column='EX_STUDENTE_LINK_2', blank=True, null=True)  # Field name made lowercase.
    ex_studente_profilo_3 = models.TextField(db_column='EX_STUDENTE_PROFILO_3', blank=True, null=True)  # Field name made lowercase.
    ex_studente_link_3 = models.TextField(db_column='EX_STUDENTE_LINK_3', blank=True, null=True)  # Field name made lowercase.
    ex_studente_profilo_4 = models.TextField(db_column='EX_STUDENTE_PROFILO_4', blank=True, null=True)  # Field name made lowercase.
    ex_studente_link_4 = models.TextField(db_column='EX_STUDENTE_LINK_4', blank=True, null=True)  # Field name made lowercase.
    sito_web = models.CharField(db_column='SITO_WEB', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_DATI_EXCEL_TMP_OLD'


class SitoWebCdsExStudenti(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=1000, blank=False, null=True)  # Field name made lowercase.
    ordine = models.PositiveIntegerField(db_column='ORDINE', blank=False, null=True)  # Field name made lowercase.
    profilo_it = models.TextField(db_column='PROFILO_IT', blank=True, null=True)  # Field name made lowercase.
    profilo_en = models.TextField(db_column='PROFILO_EN', blank=True, null=True)  # Field name made lowercase.
    link_it = models.CharField(db_column='LINK_IT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    link_en = models.CharField(db_column='LINK_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    id_sito_web_cds_dati_base = models.ForeignKey(SitoWebCdsDatiBase, models.CASCADE, db_column='ID_SITO_WEB_CDS_DATI_BASE', to_field='id')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.
    foto = models.FileField(
        upload_to=cds_websites_exstudents_media_path,
        validators=[validate_image_file_extension, validate_file_size],
        db_column='FOTO',
        max_length=1000,
        blank=True,
        null=True) # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_EX_STUDENTI'


class SitoWebCdsLink(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ordine = models.PositiveIntegerField(db_column='ORDINE', blank=True, null=True)  # Field name made lowercase.
    descrizione_link_it = models.CharField(db_column='DESCRIZIONE_LINK_IT', max_length=2000)  # Field name made lowercase.
    descrizione_link_en = models.CharField(db_column='DESCRIZIONE_LINK_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    link_it = models.CharField(db_column='LINK_IT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    link_en = models.CharField(db_column='LINK_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    id_sito_web_cds_dati_base = models.ForeignKey(SitoWebCdsDatiBase, models.CASCADE, db_column='ID_SITO_WEB_CDS_DATI_BASE', to_field='id') # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_LINK'


class SitoWebCdsSlider(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_sito_web_cds_dati_base = models.ForeignKey(SitoWebCdsDatiBase, models.CASCADE, db_column='ID_SITO_WEB_CDS_DATI_BASE', blank=True, null=True, to_field='id')  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', blank=True, null=True)  # Field name made lowercase.
    slider_it = models.TextField(db_column='SLIDER_IT', blank=True, null=True)  # Field name made lowercase.
    slider_en = models.TextField(db_column='SLIDER_EN', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_SLIDER'


class SitoWebCdsOggettiPortale(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID')  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID')  # Field name made lowercase.
    id_oggetto_portale = models.IntegerField(db_column='ID_OGGETTO_PORTALE')  # Field name made lowercase.
    id_classe_oggetto_portale = models.CharField(db_column='ID_CLASSE_OGGETTO_PORTALE',
                                                 max_length=1000)  # Field name made lowercase.
    id_sito_web_cds_topic = models.IntegerField(db_column='ID_SITO_WEB_CDS_TOPIC', blank=True,
                                                null=True)  # Field name made lowercase.
    titolo_it = models.TextField(db_column='TITOLO_IT')  # Field name made lowercase.
    titolo_en = models.TextField(db_column='TITOLO_EN')  # Field name made lowercase.
    testo_it = models.TextField(db_column='TESTO_IT', blank=True, null=True)  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_OGGETTI_PORTALE'


# class SitoWebCdsOggettiPortaleAltriDati(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # id_sito_web_cds_oggetti_portale = models.ForeignKey(SitoWebCdsOggettiPortale, models.DO_NOTHING,
                                                        # db_column='ID_SITO_WEB_CDS_OGGETTI_PORTALE')  # Field name made lowercase.
    # ordine = models.PositiveIntegerField(db_column='ORDINE')  # Field name made lowercase.
    # tipo_dato = models.CharField(db_column='TIPO_DATO', max_length=100)  # Field name made lowercase.
    # titolo_en = models.CharField(db_column='TITOLO_EN', max_length=1000, blank=True,
                                 # null=True)  # Field name made lowercase.
    # titolo_it = models.CharField(db_column='TITOLO_IT', max_length=1000, blank=True,
                                 # null=True)  # Field name made lowercase.
    # testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    # testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    # visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.
    # dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    # id_user_mod = models.IntegerField(db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    # class Meta:
        # managed = True
        # db_table = 'SITO_WEB_CDS_OGGETTI_PORTALE_ALTRI_DATI'


class SitoWebCdsArticoliRegolamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey(DidatticaCds, models.DO_NOTHING, db_column='CDS_ID')  # Field name made lowercase.
    aa_regdid_id = models.IntegerField(db_column='AA_REGDID_ID')  # Field name made lowercase.
    numero = models.PositiveIntegerField(db_column='NUMERO', blank=True, null=True)  # Field name made lowercase.
    titolo_articolo_it = models.CharField(db_column='TITOLO_ARTICOLO_IT', max_length=2000)  # Field name made lowercase.
    testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    titolo_articolo_en = models.CharField(db_column='TITOLO_ARTICOLO_EN', max_length=2000, blank=True,
                                          null=True)  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_ARTICOLI_REGOLAMENTO'


# class SitoWebCdsArticoliRegAltriDati(models.Model):
    # visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # id_sito_web_cds_articoli_regolamento = models.ForeignKey(SitoWebCdsArticoliRegolamento, models.DO_NOTHING,
                                                             # db_column='ID_SITO_WEB_CDS_ARTICOLI_REGOLAMENTO')  # Field name made lowercase.
    # ordine = models.PositiveIntegerField(db_column='ORDINE')  # Field name made lowercase.
    # titolo_en = models.CharField(db_column='TITOLO_EN', max_length=1000, blank=True,
                                 # null=True)  # Field name made lowercase.
    # titolo_it = models.CharField(db_column='TITOLO_IT', max_length=1000, blank=True,
                                 # null=True)  # Field name made lowercase.
    # testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    # testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    # dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    # id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    # class Meta:
        # managed = True
        # db_table = 'SITO_WEB_CDS_ARTICOLI_REG_ALTRI_DATI'


class SitoWebCdsTopic(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_topic_it = models.CharField(db_column='DESCR_TOPIC_IT', max_length=2000)  # Field name made lowercase.
    descr_topic_en = models.CharField(db_column='DESCR_TOPIC_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.
    visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_TOPIC'


class SitoWebCdsTopicArticoliReg(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    titolo_it = models.CharField(db_column='TITOLO_IT', max_length=1000)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    id_sito_web_cds_topic = models.ForeignKey(SitoWebCdsTopic, models.DO_NOTHING, db_column='ID_SITO_WEB_CDS_TOPIC')  # Field name made lowercase.
    id_sito_web_cds_oggetti_portale = models.ForeignKey(SitoWebCdsOggettiPortale, models.CASCADE, db_column='ID_SITO_WEB_CDS_OGGETTI_PORTALE', blank=True, null=True)  # Field name made lowercase.
    id_sito_web_cds_articoli_regolamento = models.ForeignKey(SitoWebCdsArticoliRegolamento, models.DO_NOTHING, db_column='ID_SITO_WEB_CDS_ARTICOLI_REGOLAMENTO', blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.
    visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_TOPIC_ARTICOLI_REG'
        unique_together = (('id_sito_web_cds_topic', 'id_sito_web_cds_articoli_regolamento'),)


class SitoWebCdsTipoDato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_breve = models.CharField(db_column='DESCR_BREVE', max_length=100)  # Field name made lowercase.
    descr_lunga = models.CharField(db_column='DESCR_LUNGA', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_TIPO_DATO'


class SitoWebCdsTopicArticoliRegAltriDati(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_sito_web_cds_topic_articoli_reg = models.ForeignKey(SitoWebCdsTopicArticoliReg, models.CASCADE, db_column='ID_SITO_WEB_CDS_TOPIC_ARTICOLI_REG')  # Field name made lowercase.
    ordine = models.PositiveIntegerField(db_column='ORDINE')  # Field name made lowercase.
    id_sito_web_cds_tipo_dato = models.ForeignKey(SitoWebCdsTipoDato, models.PROTECT, db_column='ID_SITO_WEB_CDS_TIPO_DATO')  # Field name made lowercase.
    titolo_it = models.CharField(db_column='TITOLO_IT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    visibile = models.IntegerField(db_column='VISIBILE')  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, db_column='ID_USER_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SITO_WEB_CDS_TOPIC_ARTICOLI_REG_ALTRI_DATI'


class DidatticaAmbiti(models.Model):
    amb_id = models.IntegerField(db_column='AMB_ID', primary_key=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amb_sede_flg = models.IntegerField(db_column='AMB_SEDE_FLG', blank=True, null=True)  # Field name made lowercase.
    sys_flg = models.IntegerField(db_column='SYS_FLG', blank=True, null=True)  # Field name made lowercase.
    amb_aggr_flg = models.IntegerField(db_column='AMB_AGGR_FLG', blank=True, null=True)  # Field name made lowercase.
    prg_ord_amb = models.IntegerField(db_column='PRG_ORD_AMB', blank=True, null=True)  # Field name made lowercase.
    dt_ins = models.DateField(db_column='DT_INS', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_AMBITI'


class DidatticaPianoRegolamento(models.Model):
    regpiani_id = models.IntegerField(db_column='REGPIANI_ID', primary_key=True)  # Field name made lowercase.
    regdid = models.ForeignKey('DidatticaRegolamento', models.DO_NOTHING, db_column='REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    attinenza_cod = models.CharField(db_column='ATTINENZA_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cod = models.CharField(db_column='COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_coorte_id = models.IntegerField(db_column='AA_COORTE_ID', blank=True, null=True)  # Field name made lowercase.
    aa_regpiani_id = models.IntegerField(db_column='AA_REGPIANI_ID', blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    def_flg = models.IntegerField(db_column='DEF_FLG', blank=True, null=True)  # Field name made lowercase.
    stato_cod = models.CharField(db_column='STATO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stato_des = models.CharField(db_column='STATO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    regpiani_pdr_id = models.IntegerField(db_column='REGPIANI_PDR_ID', blank=True, null=True)  # Field name made lowercase.
    regpiani_pdr_cod = models.CharField(db_column='REGPIANI_PDR_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    regpiani_pdr_des = models.CharField(db_column='REGPIANI_PDR_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regpiani_pdr_aa_coorte_id = models.IntegerField(db_column='REGPIANI_PDR_AA_COORTE_ID', blank=True, null=True)  # Field name made lowercase.
    regpiani_pdr_aa_regpiani_id = models.IntegerField(db_column='REGPIANI_PDR_AA_REGPIANI_ID', blank=True, null=True)  # Field name made lowercase.
    flg_exp_seg_stu = models.IntegerField(db_column='FLG_EXP_SEG_STU', blank=True, null=True)  # Field name made lowercase.
    data_exp_seg_stu = models.DateField(db_column='DATA_EXP_SEG_STU', blank=True, null=True)  # Field name made lowercase.
    nota = models.CharField(db_column='NOTA', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_REGOLAMENTO'


class DidatticaPianoSceltaAf(models.Model):
    sce_af_id = models.IntegerField(db_column='SCE_AF_ID', primary_key=True)  # Field name made lowercase.
    sce = models.ForeignKey('DidatticaPianoSceltaVincoli', models.DO_NOTHING, db_column='SCE_ID', blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey(DidatticaPdsRegolamento, models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sce_blk_id = models.IntegerField(db_column='SCE_BLK_ID', blank=True, null=True)  # Field name made lowercase.
    min_unt_blk = models.DecimalField(db_column='MIN_UNT_BLK', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    max_unt_blk = models.DecimalField(db_column='MAX_UNT_BLK', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lingua_id = models.IntegerField(db_column='LINGUA_ID', blank=True, null=True)  # Field name made lowercase.
    blk_prg = models.IntegerField(db_column='BLK_PRG', blank=True, null=True)  # Field name made lowercase.
    lingua_iso6392_cod = models.CharField(db_column='LINGUA_ISO6392_COD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lingua_des = models.CharField(db_column='LINGUA_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    lingua_num = models.IntegerField(db_column='LINGUA_NUM', blank=True, null=True)  # Field name made lowercase.
    af = models.ForeignKey(DidatticaAttivitaFormativa, models.DO_NOTHING, db_column='AF_ID', blank=True, null=True)  # Field name made lowercase.
    regud_des_auto = models.CharField(db_column='REGUD_DES_AUTO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    regud_des_ute = models.CharField(db_column='REGUD_DES_UTE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    min_unt_af = models.DecimalField(db_column='MIN_UNT_AF', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    max_unt_af = models.DecimalField(db_column='MAX_UNT_AF', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    statutario_flg = models.IntegerField(db_column='STATUTARIO_FLG', blank=True, null=True)  # Field name made lowercase.
    def_verifica_flg = models.IntegerField(db_column='DEF_VERIFICA_FLG', blank=True, null=True)  # Field name made lowercase.
    contr_aa_off_flg = models.IntegerField(db_column='CONTR_AA_OFF_FLG', blank=True, null=True)  # Field name made lowercase.
    regdid_af_id = models.IntegerField(db_column='REGDID_AF_ID', blank=True, null=True)  # Field name made lowercase.
    pds_regdid_af_id = models.IntegerField(db_column='PDS_REGDID_AF_ID', blank=True, null=True)  # Field name made lowercase.
    pds_af_cod = models.CharField(db_column='PDS_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_af_des = models.CharField(db_column='PDS_AF_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_af_flg = models.IntegerField(db_column='COMUNE_AF_FLG', blank=True, null=True)  # Field name made lowercase.
    attinenza_af_cod = models.CharField(db_column='ATTINENZA_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    of_id = models.IntegerField(db_column='OF_ID', blank=True, null=True)  # Field name made lowercase.
    cds_af_id = models.IntegerField(db_column='CDS_AF_ID', blank=True, null=True)  # Field name made lowercase.
    cds_af_cod = models.CharField(db_column='CDS_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nome_af_cds = models.CharField(db_column='NOME_AF_CDS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cdsord_af_cod = models.CharField(db_column='CDSORD_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aa_off_id = models.IntegerField(db_column='AA_OFF_ID', blank=True, null=True)  # Field name made lowercase.
    stato_of_cod = models.CharField(db_column='STATO_OF_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_id = models.IntegerField(db_column='TIPO_COMP_AF_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_comp_af_cod = models.CharField(db_column='TIPO_COMP_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    des_tipo_comp_af = models.CharField(db_column='DES_TIPO_COMP_AF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.IntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_gen_des = models.CharField(db_column='AF_GEN_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anno_corso_af = models.IntegerField(db_column='ANNO_CORSO_AF', blank=True, null=True)  # Field name made lowercase.
    lista_anni_corso_af = models.CharField(db_column='LISTA_ANNI_CORSO_AF', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_regdid_id = models.IntegerField(db_column='AF_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod_af = models.CharField(db_column='TIPO_AF_COD_AF', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des_af = models.CharField(db_column='TIPO_AF_DES_AF', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb_id_af = models.ForeignKey(DidatticaAmbiti, models.DO_NOTHING, db_column='AMB_ID_AF', blank=True, null=True)  # Field name made lowercase.
    ambito_des_af = models.CharField(db_column='AMBITO_DES_AF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_af_intercla_cod_af = models.CharField(db_column='TIPO_AF_INTERCLA_COD_AF', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_intercla_des_af = models.CharField(db_column='TIPO_AF_INTERCLA_DES_AF', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb_intercla_id_af = models.IntegerField(db_column='AMB_INTERCLA_ID_AF', blank=True, null=True)  # Field name made lowercase.
    ambito_intercla_des_af = models.CharField(db_column='AMBITO_INTERCLA_DES_AF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    peso = models.DecimalField(db_column='PESO', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    peso_foglie_non_log = models.DecimalField(db_column='PESO_FOGLIE_NON_LOG', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    num_max_reit = models.IntegerField(db_column='NUM_MAX_REIT', blank=True, null=True)  # Field name made lowercase.
    non_erogabile_flg = models.IntegerField(db_column='NON_EROGABILE_FLG', blank=True, null=True)  # Field name made lowercase.
    livello_af_cod = models.CharField(db_column='LIVELLO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    livello_af_des = models.CharField(db_column='LIVELLO_AF_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_esa_cod = models.CharField(db_column='TIPO_ESA_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_esa_des = models.CharField(db_column='TIPO_ESA_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_val_cod = models.CharField(db_column='TIPO_VAL_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_val_des = models.CharField(db_column='TIPO_VAL_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    af_pdr_id = models.IntegerField(db_column='AF_PDR_ID', blank=True, null=True)  # Field name made lowercase.
    af_radice_id = models.IntegerField(db_column='AF_RADICE_ID', blank=True, null=True)  # Field name made lowercase.
    num_liv_albero = models.IntegerField(db_column='NUM_LIV_ALBERO', blank=True, null=True)  # Field name made lowercase.
    ciclo_id = models.IntegerField(db_column='CICLO_ID', blank=True, null=True)  # Field name made lowercase.
    ciclo_des = models.CharField(db_column='CICLO_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_ciclo_cod = models.CharField(db_column='TIPO_CICLO_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des_tipo_ciclo = models.CharField(db_column='DES_TIPO_CICLO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    org_did_sua_cod = models.IntegerField(db_column='ORG_DID_SUA_COD', blank=True, null=True)  # Field name made lowercase.
    sede_id = models.IntegerField(db_column='SEDE_ID', blank=True, null=True)  # Field name made lowercase.
    sede_des = models.CharField(db_column='SEDE_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_rag_cod = models.CharField(db_column='TIPO_RAG_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_rag_des = models.CharField(db_column='TIPO_RAG_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    af_capogruppo_id = models.IntegerField(db_column='AF_CAPOGRUPPO_ID', blank=True, null=True)  # Field name made lowercase.
    scelta_mod_flg = models.IntegerField(db_column='SCELTA_MOD_FLG', blank=True, null=True)  # Field name made lowercase.
    num_regud = models.DecimalField(db_column='NUM_REGUD', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_SCELTA_AF'
        ordering = ('ciclo_des',)


class DidatticaPianoSceltaFilAnd(models.Model):
    sce_fil_and_id = models.IntegerField(db_column='SCE_FIL_AND_ID', primary_key=True)  # Field name made lowercase.
    sce = models.ForeignKey('DidatticaPianoSceltaVincoli', models.DO_NOTHING, db_column='SCE_ID', blank=True, null=True)  # Field name made lowercase.
    sce_fil_or_id = models.IntegerField(db_column='SCE_FIL_OR_ID', blank=True, null=True)  # Field name made lowercase.
    sce_fil_or_des = models.CharField(db_column='SCE_FIL_OR_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo_filtro_cod = models.CharField(db_column='TIPO_FILTRO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_filtro_des = models.CharField(db_column='TIPO_FILTRO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    af_gen_id = models.IntegerField(db_column='AF_GEN_ID', blank=True, null=True)  # Field name made lowercase.
    af_gen_cod = models.CharField(db_column='AF_GEN_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af_gen_des = models.CharField(db_column='AF_GEN_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dip_sce_fil_and_id = models.IntegerField(db_column='DIP_SCE_FIL_AND_ID', blank=True, null=True)  # Field name made lowercase.
    dip_sce_fil_and_cod = models.CharField(db_column='DIP_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dip_sce_fil_and_des = models.CharField(db_column='DIP_SCE_FIL_AND_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    strac_sce_fil_and_id = models.IntegerField(db_column='STRAC_SCE_FIL_AND_ID', blank=True, null=True)  # Field name made lowercase.
    strac_sce_fil_and_cod = models.CharField(db_column='STRAC_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    strac_sce_fil_and_des = models.CharField(db_column='STRAC_SCE_FIL_AND_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cds_sce_fil_and_id = models.IntegerField(db_column='CDS_SCE_FIL_AND_ID', blank=True, null=True)  # Field name made lowercase.
    cds_sce_fil_and_cod = models.CharField(db_column='CDS_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cds_sce_fil_and_nome = models.CharField(db_column='CDS_SCE_FIL_AND_NOME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cfu = models.DecimalField(db_column='CFU', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tipo_af_sce_fil_and_cod = models.CharField(db_column='TIPO_AF_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_sce_fil_and_des = models.CharField(db_column='TIPO_AF_SCE_FIL_AND_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sett_cod = models.CharField(db_column='SETT_COD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_sce_fil_and_cod = models.CharField(db_column='TIPO_CORSO_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cla_miur_sce_fil_and_id = models.IntegerField(db_column='CLA_MIUR_SCE_FIL_AND_ID', blank=True, null=True)  # Field name made lowercase.
    cla_miur_sce_fil_and_cod = models.CharField(db_column='CLA_MIUR_SCE_FIL_AND_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cla_miur_sce_fil_and_des = models.CharField(db_column='CLA_MIUR_SCE_FIL_AND_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rif_cod = models.CharField(db_column='RIF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sett_post_rif_flg = models.IntegerField(db_column='SETT_POST_RIF_FLG', blank=True, null=True)  # Field name made lowercase.
    tipo_ins_cod = models.CharField(db_column='TIPO_INS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    peso_sce_fil_and = models.IntegerField(db_column='PESO_SCE_FIL_AND', blank=True, null=True)  # Field name made lowercase.
    not_flg = models.IntegerField(db_column='NOT_FLG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_SCELTA_FIL_AND'


class DidatticaPianoSceltaSchePiano(models.Model):
    sche_piano = models.OneToOneField('DidatticaPianoSche', models.DO_NOTHING, db_column='SCHE_PIANO_ID', primary_key=True)  # Field name made lowercase.
    sche_statutario_flg = models.BooleanField(db_column='SCHE_STATUTARIO_FLG', default=False)  # Field name made lowercase.
    sche_pds_regdid_id = models.IntegerField(db_column='SCHE_PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    sche_pds_cod = models.CharField(db_column='SCHE_PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sche_pds_des = models.CharField(db_column='SCHE_PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sche_ori_id = models.IntegerField(db_column='SCHE_ORI_ID', blank=True, null=True)  # Field name made lowercase.
    sche_cla_m_id = models.IntegerField(db_column='SCHE_CLA_M_ID', blank=True, null=True)  # Field name made lowercase.
    sche_apt_id = models.IntegerField(db_column='SCHE_APT_ID', blank=True, null=True)  # Field name made lowercase.
    sche_nota = models.CharField(db_column='SCHE_NOTA', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    data_ini_val = models.DateField(db_column='DATA_INI_VAL', blank=True, null=True)  # Field name made lowercase.
    data_fine_val = models.DateField(db_column='DATA_FINE_VAL', blank=True, null=True)  # Field name made lowercase.
    stato_piano_gen_cod = models.CharField(db_column='STATO_PIANO_GEN_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    contr_ac_piano_stu_cod = models.CharField(db_column='CONTR_AC_PIANO_STU_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    blocco_af_freq_piano_stu_flg = models.IntegerField(db_column='BLOCCO_AF_FREQ_PIANO_STU_FLG', blank=True, null=True)  # Field name made lowercase.
    sce = models.ForeignKey('DidatticaPianoSceltaVincoli', models.DO_NOTHING, db_column='SCE_ID')  # Field name made lowercase.
    ord_num = models.IntegerField(db_column='ORD_NUM', blank=True, null=True)  # Field name made lowercase.
    apt_slot_id = models.IntegerField(db_column='APT_SLOT_ID', blank=True, null=True)  # Field name made lowercase.
    apt_slot_cod = models.CharField(db_column='APT_SLOT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    apt_slot_des = models.CharField(db_column='APT_SLOT_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    apt_slot_anno_corso = models.IntegerField(db_column='APT_SLOT_ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    apt_slot_ord_num = models.IntegerField(db_column='APT_SLOT_ORD_NUM', blank=True, null=True)  # Field name made lowercase.
    sce_des = models.CharField(db_column='SCE_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_regdid_id = models.IntegerField(db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    anno_corso_ant = models.IntegerField(db_column='ANNO_CORSO_ANT', blank=True, null=True)  # Field name made lowercase.
    tipo_regsce_cod = models.CharField(db_column='TIPO_REGSCE_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_sce_cod = models.CharField(db_column='TIPO_SCE_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_sce_des = models.CharField(db_column='TIPO_SCE_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_regsce_des = models.CharField(db_column='TIPO_REGSCE_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tipo_um_regsce_cod = models.CharField(db_column='TIPO_UM_REGSCE_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    opz_flg = models.IntegerField(db_column='OPZ_FLG', blank=True, null=True)  # Field name made lowercase.
    min_unt = models.DecimalField(db_column='MIN_UNT', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    max_unt = models.DecimalField(db_column='MAX_UNT', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    livello = models.IntegerField(db_column='LIVELLO', blank=True, null=True)  # Field name made lowercase.
    vin_id = models.IntegerField(db_column='VIN_ID', blank=True, null=True)  # Field name made lowercase.
    vin_ord_num = models.IntegerField(db_column='VIN_ORD_NUM', blank=True, null=True)  # Field name made lowercase.
    vin_sce_des = models.CharField(db_column='VIN_SCE_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipi_af_tipi_sce_id = models.IntegerField(db_column='TIPI_AF_TIPI_SCE_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb = models.ForeignKey(DidatticaAmbiti, models.DO_NOTHING, db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sovran_flg = models.IntegerField(db_column='SOVRAN_FLG', blank=True, null=True)  # Field name made lowercase.
    sostegno_flg = models.IntegerField(db_column='SOSTEGNO_FLG', blank=True, null=True)  # Field name made lowercase.
    peso_sce = models.IntegerField(db_column='PESO_SCE', blank=True, null=True)  # Field name made lowercase.
    tesoretto_flg = models.IntegerField(db_column='TESORETTO_FLG', blank=True, null=True)  # Field name made lowercase.
    assegnazione_posti_flg = models.IntegerField(db_column='ASSEGNAZIONE_POSTI_FLG', blank=True, null=True)  # Field name made lowercase.
    delibera_flg = models.IntegerField(db_column='DELIBERA_FLG', blank=True, null=True)  # Field name made lowercase.
    azzera_cfu_flg = models.IntegerField(db_column='AZZERA_CFU_FLG', blank=True, null=True)  # Field name made lowercase.
    parametri_logistica_flg = models.IntegerField(db_column='PARAMETRI_LOGISTICA_FLG', blank=True, null=True)  # Field name made lowercase.
    tag_regsce_cod = models.CharField(db_column='TAG_REGSCE_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    peso_af_sce = models.DecimalField(db_column='PESO_AF_SCE', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    peso_min_singola_af = models.DecimalField(db_column='PESO_MIN_SINGOLA_AF', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    peso_max_singola_af = models.DecimalField(db_column='PESO_MAX_SINGOLA_AF', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_af_sce = models.DecimalField(db_column='NUM_AF_SCE', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    peso_af_sce_stat = models.DecimalField(db_column='PESO_AF_SCE_STAT', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    peso_af_sce_def_verifica = models.DecimalField(db_column='PESO_AF_SCE_DEF_VERIFICA', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk = models.DecimalField(db_column='NUM_BLK', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_stat = models.DecimalField(db_column='NUM_BLK_STAT', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_def_verifica = models.DecimalField(db_column='NUM_BLK_DEF_VERIFICA', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_contr_aa_off = models.DecimalField(db_column='NUM_BLK_CONTR_AA_OFF', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_statutario_flg_div = models.DecimalField(db_column='NUM_BLK_STATUTARIO_FLG_DIV', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_def_verifica_flg_div = models.DecimalField(db_column='NUM_BLK_DEF_VERIFICA_FLG_DIV', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_blk_contr_aa_off_flg_div = models.DecimalField(db_column='NUM_BLK_CONTR_AA_OFF_FLG_DIV', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    peso_blk = models.DecimalField(db_column='PESO_BLK', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    af_stessa_taf_flg = models.DecimalField(db_column='AF_STESSA_TAF_FLG', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    af_stessa_taf_intercla_flg = models.DecimalField(db_column='AF_STESSA_TAF_INTERCLA_FLG', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    af_stesso_ambito_flg = models.DecimalField(db_column='AF_STESSO_AMBITO_FLG', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    af_stesso_ambito_intercla_flg = models.DecimalField(db_column='AF_STESSO_AMBITO_INTERCLA_FLG', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    amb_id_af_regsce = models.DecimalField(db_column='AMB_ID_AF_REGSCE', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod_af_regsce = models.CharField(db_column='TIPO_AF_COD_AF_REGSCE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    amb_intercla_id_af_regsce = models.DecimalField(db_column='AMB_INTERCLA_ID_AF_REGSCE', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tipo_af_intercla_cod_af_regsce = models.CharField(db_column='TIPO_AF_INTERCLA_COD_AF_REGSCE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    num_af_taf_d = models.DecimalField(db_column='NUM_AF_TAF_D', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_af_taf_intercla_d = models.DecimalField(db_column='NUM_AF_TAF_INTERCLA_D', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_af_taf_e_f_s = models.DecimalField(db_column='NUM_AF_TAF_E_F_S', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_af_taf_intercla_e_f_s = models.DecimalField(db_column='NUM_AF_TAF_INTERCLA_E_F_S', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sett_cod_af_regsce = models.CharField(db_column='SETT_COD_AF_REGSCE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nota_pre = models.TextField(db_column='NOTA_PRE', blank=True, null=True)  # Field name made lowercase.
    nota_pre_vis_web_flg = models.IntegerField(db_column='NOTA_PRE_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    nota_post = models.TextField(db_column='NOTA_POST', blank=True, null=True)  # Field name made lowercase.
    nota_post_vis_web_flg = models.IntegerField(db_column='NOTA_POST_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_SCELTA_SCHE_PIANO'
        unique_together = (('sche_piano', 'sce'),)


class DidatticaPianoSceltaVincoli(models.Model):
    sce_id = models.IntegerField(db_column='SCE_ID', primary_key=True)  # Field name made lowercase.
    regpiani = models.ForeignKey(DidatticaPianoRegolamento, models.DO_NOTHING, db_column='REGPIANI_ID', blank=True, null=True)  # Field name made lowercase.
    ord_num = models.IntegerField(db_column='ORD_NUM', blank=True, null=True)  # Field name made lowercase.
    sce_des = models.CharField(db_column='SCE_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey(DidatticaPdsRegolamento, models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    anno_corso = models.IntegerField(db_column='ANNO_CORSO', blank=True, null=True)  # Field name made lowercase.
    anno_corso_ant = models.IntegerField(db_column='ANNO_CORSO_ANT', blank=True, null=True)  # Field name made lowercase.
    tipo_regsce_cod = models.CharField(db_column='TIPO_REGSCE_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_sce_cod = models.CharField(db_column='TIPO_SCE_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_um_regsce_cod = models.CharField(db_column='TIPO_UM_REGSCE_COD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    opz_flg = models.IntegerField(db_column='OPZ_FLG', blank=True, null=True)  # Field name made lowercase.
    min_unt = models.DecimalField(db_column='MIN_UNT', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    max_unt = models.DecimalField(db_column='MAX_UNT', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    livello = models.IntegerField(db_column='LIVELLO', blank=True, null=True)  # Field name made lowercase.
    vin = models.ForeignKey('self', models.DO_NOTHING, db_column='VIN_ID', blank=True, null=True)  # Field name made lowercase.
    vin_ord_num = models.IntegerField(db_column='VIN_ORD_NUM', blank=True, null=True)  # Field name made lowercase.
    vin_sce_des = models.CharField(db_column='VIN_SCE_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipi_af_tipi_sce_id = models.IntegerField(db_column='TIPI_AF_TIPI_SCE_ID', blank=True, null=True)  # Field name made lowercase.
    tipo_af_cod = models.CharField(db_column='TIPO_AF_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_af_des = models.CharField(db_column='TIPO_AF_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    amb_id = models.IntegerField(db_column='AMB_ID', blank=True, null=True)  # Field name made lowercase.
    ambito_des = models.CharField(db_column='AMBITO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sovran_flg = models.IntegerField(db_column='SOVRAN_FLG', blank=True, null=True)  # Field name made lowercase.
    sostegno_flg = models.IntegerField(db_column='SOSTEGNO_FLG', blank=True, null=True)  # Field name made lowercase.
    peso_sce = models.IntegerField(db_column='PESO_SCE', blank=True, null=True)  # Field name made lowercase.
    tesoretto_flg = models.IntegerField(db_column='TESORETTO_FLG', blank=True, null=True)  # Field name made lowercase.
    assegnazione_posti_flg = models.IntegerField(db_column='ASSEGNAZIONE_POSTI_FLG', blank=True, null=True)  # Field name made lowercase.
    delibera_flg = models.IntegerField(db_column='DELIBERA_FLG', blank=True, null=True)  # Field name made lowercase.
    azzera_cfu_flg = models.IntegerField(db_column='AZZERA_CFU_FLG', blank=True, null=True)  # Field name made lowercase.
    parametri_logistica_flg = models.IntegerField(db_column='PARAMETRI_LOGISTICA_FLG', blank=True, null=True)  # Field name made lowercase.
    tag_regsce_cod = models.CharField(db_column='TAG_REGSCE_COD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nota_pre = models.TextField(db_column='NOTA_PRE', blank=True, null=True)  # Field name made lowercase.
    nota_pre_vis_web_flg = models.IntegerField(db_column='NOTA_PRE_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    nota_post = models.TextField(db_column='NOTA_POST', blank=True, null=True)  # Field name made lowercase.
    nota_post_vis_web_flg = models.IntegerField(db_column='NOTA_POST_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_SCELTA_VINCOLI'


class DidatticaPianoSche(models.Model):
    sche_piano_id = models.IntegerField(db_column='SCHE_PIANO_ID', primary_key=True)  # Field name made lowercase.
    regpiani = models.ForeignKey(DidatticaPianoRegolamento, models.DO_NOTHING, db_column='REGPIANI_ID')  # Field name made lowercase.
    sche_piano_cod = models.CharField(db_column='SCHE_PIANO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sche_piano_des = models.CharField(db_column='SCHE_PIANO_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sche_piano_vis_web_flg = models.IntegerField(db_column='SCHE_PIANO_VIS_WEB_FLG', blank=True, null=True)  # Field name made lowercase.
    pds_regdid = models.ForeignKey(DidatticaPdsRegolamento, models.DO_NOTHING, db_column='PDS_REGDID_ID', blank=True, null=True)  # Field name made lowercase.
    pds_cod = models.CharField(db_column='PDS_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pds_des = models.CharField(db_column='PDS_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comune_flg = models.IntegerField(db_column='COMUNE_FLG', blank=True, null=True)  # Field name made lowercase.
    ori_id = models.IntegerField(db_column='ORI_ID', blank=True, null=True)  # Field name made lowercase.
    ori_cod = models.CharField(db_column='ORI_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ori_des = models.CharField(db_column='ORI_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cla_m_id = models.IntegerField(db_column='CLA_M_ID', blank=True, null=True)  # Field name made lowercase.
    cla_miur_cod = models.CharField(db_column='CLA_MIUR_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cla_miur_des = models.CharField(db_column='CLA_MIUR_DES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    apt_id = models.IntegerField(db_column='APT_ID', blank=True, null=True)  # Field name made lowercase.
    apt_cod = models.CharField(db_column='APT_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    apt_des = models.CharField(db_column='APT_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    data_ini_val = models.DateField(db_column='DATA_INI_VAL', blank=True, null=True)  # Field name made lowercase.
    data_fine_val = models.DateField(db_column='DATA_FINE_VAL', blank=True, null=True)  # Field name made lowercase.
    stato_piano_gen_cod = models.CharField(db_column='STATO_PIANO_GEN_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stato_piano_gen_des = models.CharField(db_column='STATO_PIANO_GEN_DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    contr_ac_piano_stu_cod = models.CharField(db_column='CONTR_AC_PIANO_STU_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    blocco_af_freq_piano_stu_flg = models.IntegerField(db_column='BLOCCO_AF_FREQ_PIANO_STU_FLG', blank=True, null=True)  # Field name made lowercase.
    nota_sche_piano = models.CharField(db_column='NOTA_SCHE_PIANO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    sche_piano_des_txt_id = models.IntegerField(db_column='SCHE_PIANO_DES_TXT_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIDATTICA_PIANO_SCHE'


class DidatticaArticoliRegolamentoStatus(PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    status_cod = models.CharField(db_column='STATUS_COD', max_length=100)  # Field name made lowercase.
    status_desc = models.TextField(db_column='STATUS_DESC', blank=True, null=True)  # Field name made lowercase.

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
    
    class Meta:
        managed = True
        db_table = 'DIDATTICA_ARTICOLI_REGOLAMENTO_STATUS'


class DidatticaCdsTipoCorso(PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_corso_cod = models.CharField(db_column='TIPO_CORSO_COD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo_corso_des = models.CharField(db_column='TIPO_CORSO_DES', max_length=80, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='NOTE', max_length=400, blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
    
    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_TIPO_CORSO'


class DidatticaArticoliRegolamentoStruttura(VisibileModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    aa = models.IntegerField(db_column='AA')  # Field name made lowercase.
    numero = models.PositiveIntegerField(db_column='NUMERO', blank=True, null=True)  # Field name made lowercase.
    titolo_it = models.CharField(db_column='TITOLO_IT', max_length=2000)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.
    id_didattica_cds_tipo_corso = models.ForeignKey(DidatticaCdsTipoCorso, models.PROTECT, db_column='ID_DIDATTICA_CDS_TIPO_CORSO')  # Field name made lowercase.
    id_didattica_articoli_regolamento_titolo = models.ForeignKey("DidatticaArticoliRegolamentoTitolo", models.PROTECT, db_column='ID_DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO')  # Field name made lowercase.

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_ARTICOLI_REGOLAMENTO_STRUTTURA'
        
        
class DidatticaCdsArticoliRegolamentoTestata(VisibileModAbstract, PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cds = models.ForeignKey('DidatticaCds', models.DO_NOTHING, db_column='CDS_ID')  # Field name made lowercase.
    aa = models.IntegerField(db_column='AA')  # Field name made lowercase.
    note = models.TextField(db_column='NOTE', blank=True)  # Field name made lowercase.
    id_didattica_articoli_regolamento_status = models.ForeignKey(DidatticaArticoliRegolamentoStatus, models.PROTECT, db_column='ID_DIDATTICA_ARTICOLI_REGOLAMENTO_STATUS')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
        
    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()
          
        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return user_office.office.organizational_structure.unique_code == self.cds.dip.dip_cod
        return True
        
    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()
        
        status_cod = self.id_didattica_articoli_regolamento_status\
                         .status_cod
        
        if status_cod == '0' and offices_names[0] in user_offices_names:
            return True
        elif status_cod == '1' and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ['2', '3'] and offices_names[2] in user_offices_names:
            return True
        
        return False

    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_ARTICOLI_REGOLAMENTO_TESTATA'


class DidatticaArticoliRegolamentoStrutturaTopic(VisibileModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_sito_web_cds_topic = models.ForeignKey(SitoWebCdsTopic, models.PROTECT, db_column='ID_SITO_WEB_CDS_TOPIC')  # Field name made lowercase.
    id_did_art_regolamento_struttura = models.ForeignKey(DidatticaArticoliRegolamentoStruttura, models.DO_NOTHING, db_column='ID_DID_ART_REGOLAMENTO_STRUTTURA')  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase. TODO

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
    
    class Meta:
        managed = True
        db_table = 'DIDATTICA_ARTICOLI_REGOLAMENTO_STRUTTURA_TOPIC'        
        
        
class DidatticaCdsArticoliRegolamento(VisibileModAbstract, PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_didattica_cds_articoli_regolamento_testata = models.ForeignKey(DidatticaCdsArticoliRegolamentoTestata, models.PROTECT, db_column='ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO_TESTATA', blank=True, null=True)  # Field name made lowercase.
    id_didattica_articoli_regolamento_struttura = models.ForeignKey(DidatticaArticoliRegolamentoStruttura, models.PROTECT, db_column='ID_DIDATTICA_ARTICOLI_REGOLAMENTO_STRUTTURA')  # Field name made lowercase.
    testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='NOTE', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.
       
    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
    
    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()
          
        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return user_office.office.organizational_structure.unique_code == self.id_didattica_cds_articoli_regolamento_testata.cds.dip.dip_cod
        return True
        
    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()
        
        status_cod = self.id_didattica_cds_articoli_regolamento_testata\
                         .id_didattica_articoli_regolamento_status\
                         .status_cod
        
        if status_cod == '0' and offices_names[0] in user_offices_names:
            return True
        elif status_cod == '1' and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ['2', '3'] and offices_names[2] in user_offices_names:
            return True
        
        return False
    
    def _check_lock_permission(self, user_offices_names, **kwargs):
        return self._check_edit_permission(user_offices_names, **kwargs)
       
    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_ARTICOLI_REGOLAMENTO'


class DidatticaArticoliRegolamentoTitolo(PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descr_titolo_it = models.CharField(db_column='DESCR_TITOLO_IT', max_length=1000)  # Field name made lowercase.
    descr_titolo_en = models.CharField(db_column='DESCR_TITOLO_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ordine = models.IntegerField(db_column='ORDINE')  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD', blank=True, null=True)  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)

    class Meta:
        managed = True
        db_table = 'DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO'
        

class DidatticaCdsSubArticoliRegolamento(VisibileModAbstract, PermissionsModAbstract):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ordine = models.PositiveIntegerField(db_column='ORDINE')  # Field name made lowercase.
    titolo_it = models.CharField(db_column='TITOLO_IT', max_length=1000)  # Field name made lowercase.
    titolo_en = models.CharField(db_column='TITOLO_EN', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    testo_it = models.TextField(db_column='TESTO_IT')  # Field name made lowercase.
    testo_en = models.TextField(db_column='TESTO_EN', blank=True, null=True)  # Field name made lowercase.
    id_didattica_cds_articoli_regolamento = models.ForeignKey(DidatticaCdsArticoliRegolamento, models.CASCADE, db_column='ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO', blank=True, null=True)  # Field name made lowercase.
    dt_mod = models.DateTimeField(db_column='DT_MOD')  # Field name made lowercase.
    id_user_mod = models.ForeignKey(get_user_model(), models.DO_NOTHING, db_column='ID_USER_MOD')  # Field name made lowercase.
    
    @classmethod
    def get_offices_names(cls, **kwargs):
        return (OFFICE_REGDIDS_DEPARTMENT,
                OFFICE_REGDIDS_REVISION,
                OFFICE_REGDIDS_APPROVAL)
    
    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()
          
        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return user_office.office.organizational_structure.unique_code == self.id_didattica_cds_articoli_regolamento.id_didattica_cds_articoli_regolamento_testata.cds.dip.dip_cod
        return True
        
    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()
        
        status_cod = self.id_didattica_cds_articoli_regolamento\
                         .id_didattica_cds_articoli_regolamento_testata\
                         .id_didattica_articoli_regolamento_status\
                         .status_cod
        
        if status_cod == '0' and offices_names[0] in user_offices_names:
            return True
        elif status_cod == '1' and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ['2', '3'] and offices_names[2] in user_offices_names:
            return True
        
        return False
    
    def _check_lock_permission(self, user_offices_names, **kwargs):
        return self._check_edit_permission(user_offices_names, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'DIDATTICA_CDS_SUB_ARTICOLI_REGOLAMENTO'