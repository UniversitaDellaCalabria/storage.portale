import datetime

from django.contrib.auth import get_user_model
from django.db import models
from generics.models import Permissions, VisibileAbstract

from .settings import (
    OFFICE_REGDIDS_APPROVAL,
    OFFICE_REGDIDS_DEPARTMENT,
    OFFICE_REGDIDS_REVISION,
)


class DidatticaArticoliRegolamentoStatus(Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    status_cod = models.CharField(db_column="STATUS_COD", max_length=100)
    status_desc = models.TextField(db_column="STATUS_DESC", blank=True, null=True)

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    class Meta:
        managed = True
        db_table = "DIDATTICA_ARTICOLI_REGOLAMENTO_STATUS"


class DidatticaArticoliRegolamentoStruttura(VisibileAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    aa = models.IntegerField(db_column="AA")
    numero = models.PositiveIntegerField(db_column="NUMERO")
    numero_prec = models.PositiveIntegerField(db_column="NUMERO_PREC", blank=True, null=True)
    titolo_it = models.CharField(db_column="TITOLO_IT", max_length=2000)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=2000, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )
    didattica_cds_tipo_corso = models.ForeignKey(
        "cds.DidatticaCdsTipoCorso",
        models.PROTECT,
        db_column="ID_DIDATTICA_CDS_TIPO_CORSO",
    )
    didattica_articoli_regolamento_titolo = models.ForeignKey(
        "DidatticaArticoliRegolamentoTitolo",
        models.PROTECT,
        db_column="ID_DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO",
    )

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    class Meta:
        managed = True
        db_table = "DIDATTICA_ARTICOLI_REGOLAMENTO_STRUTTURA"
        unique_together = ("aa", "numero", "didattica_cds_tipo_corso")


class DidatticaCdsArticoliRegolamentoTestata(VisibileAbstract, Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    cds = models.ForeignKey(
        "cds.DidatticaCds", models.DO_NOTHING, db_column="ID_DIDATTICA_CDS"
    )
    aa = models.IntegerField(db_column="AA")
    note = models.TextField(db_column="NOTE", blank=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    @classmethod
    def can_user_create_object(cls, user, **kwargs):
        regdid = kwargs.pop("regdid", None)
        if regdid is None or not regdid.aa_reg_did == datetime.datetime.now().year:
            return False

        importing = kwargs.pop("importing", False)
        if importing and (
            user.is_superuser
            or cls._get_all_user_offices(user)
            .filter(office__name__in=cls.get_offices_names()[1:3])
            .exists()
        ):
            return True

        dep_offices = cls._get_all_user_offices(user).filter(
            office__name=cls.get_offices_names()[0]
        )
        if dep_offices.exists():
            dep_codes = [
                dep_office.office.organizational_structure.unique_code
                for dep_office in dep_offices
            ]
            if regdid.cds.dip.dip_cod in dep_codes:
                return True
        return False

    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()

        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return (
                user_office.office.organizational_structure.unique_code
                == self.cds.dip.dip_cod
            )
        return True

    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()

        testata_status = (
            DidatticaCdsTestataStatus.objects.filter(
                didattica_cds_articoli_regolamento_testata=self.pk
            )
            .order_by("-data_status")
            .first()
        )
        if testata_status is None:
            return False

        status_cod = testata_status.didattica_articoli_regolamento_status.status_cod

        if status_cod == "0" and offices_names[0] in user_offices_names:
            return True
        elif status_cod == "1" and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ["2", "3"] and offices_names[2] in user_offices_names:
            return True

        return False

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_ARTICOLI_REGOLAMENTO_TESTATA"
        unique_together = ("cds", "aa")


class DidatticaCdsTestataStatus(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_articoli_regolamento_status = models.ForeignKey(
        DidatticaArticoliRegolamentoStatus,
        models.PROTECT,
        db_column="ID_DIDATTICA_ARTICOLI_REGOLAMENTO_STATUS",
    )
    didattica_cds_articoli_regolamento_testata = models.ForeignKey(
        DidatticaCdsArticoliRegolamentoTestata,
        models.PROTECT,
        db_column="ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO_TESTATA",
    )
    motivazione = models.TextField(db_column="MOTIVAZIONE", blank=True, null=True)
    data_status = models.DateTimeField(db_column="DATA_STATUS")
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(),
        models.DO_NOTHING,
        db_column="user_mod_id",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_TESTATA_STATUS"


class DidatticaCdsArticoliRegolamento(VisibileAbstract, Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    didattica_cds_articoli_regolamento_testata = models.ForeignKey(
        DidatticaCdsArticoliRegolamentoTestata,
        models.PROTECT,
        db_column="ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO_TESTATA",
    )
    didattica_articoli_regolamento_struttura = models.ForeignKey(
        DidatticaArticoliRegolamentoStruttura,
        models.PROTECT,
        db_column="ID_DIDATTICA_ARTICOLI_REGOLAMENTO_STRUTTURA",
    )
    testo_it = models.TextField(db_column="TESTO_IT")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    note = models.TextField(db_column="NOTE", blank=True, null=True)
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()

        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return (
                user_office.office.organizational_structure.unique_code
                == self.didattica_cds_articoli_regolamento_testata.cds.dip.dip_cod
            )
        return True

    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()

        testata_status = (
            DidatticaCdsTestataStatus.objects.filter(
                didattica_cds_articoli_regolamento_testata=self.didattica_cds_articoli_regolamento_testata.pk
            )
            .order_by("-data_status")
            .first()
        )
        if testata_status is None:
            return False

        status_cod = testata_status.didattica_articoli_regolamento_status.status_cod

        if status_cod == "0" and offices_names[0] in user_offices_names:
            return True
        elif status_cod == "1" and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ["2", "3"] and offices_names[2] in user_offices_names:
            return True

        return False

    def _check_lock_permission(self, user_offices_names, **kwargs):
        return self._check_edit_permission(user_offices_names, **kwargs)

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_ARTICOLI_REGOLAMENTO"
        unique_together = (
            "didattica_cds_articoli_regolamento_testata",
            "didattica_articoli_regolamento_struttura",
        )


class DidatticaArticoliRegolamentoTitolo(Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    descr_titolo_it = models.CharField(db_column="DESCR_TITOLO_IT", max_length=1000)
    descr_titolo_en = models.CharField(
        db_column="DESCR_TITOLO_EN", max_length=1000, blank=True, null=True
    )
    ordine = models.IntegerField(db_column="ORDINE")
    dt_mod = models.DateTimeField(db_column="DT_MOD", blank=True, null=True)
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    class Meta:
        managed = True
        db_table = "DIDATTICA_ARTICOLI_REGOLAMENTO_TITOLO"


class DidatticaCdsSubArticoliRegolamento(VisibileAbstract, Permissions):
    id = models.AutoField(db_column="ID", primary_key=True)
    ordine = models.PositiveIntegerField(db_column="ORDINE")
    titolo_it = models.CharField(db_column="TITOLO_IT", max_length=1000)
    titolo_en = models.CharField(
        db_column="TITOLO_EN", max_length=1000, blank=True, null=True
    )
    testo_it = models.TextField(db_column="TESTO_IT")
    testo_en = models.TextField(db_column="TESTO_EN", blank=True, null=True)
    didattica_cds_articoli_regolamento = models.ForeignKey(
        DidatticaCdsArticoliRegolamento,
        models.CASCADE,
        db_column="ID_DIDATTICA_CDS_ARTICOLI_REGOLAMENTO",
        blank=True,
        null=True,
    )
    dt_mod = models.DateTimeField(db_column="DT_MOD")
    user_mod = models.ForeignKey(
        get_user_model(), models.DO_NOTHING, db_column="user_mod_id"
    )

    @classmethod
    def get_offices_names(cls, **kwargs):
        return (
            OFFICE_REGDIDS_DEPARTMENT,
            OFFICE_REGDIDS_REVISION,
            OFFICE_REGDIDS_APPROVAL,
        )

    def _is_valid_office(self, office_name, all_user_offices, **kwargs):
        offices_names = self.get_offices_names()

        if office_name == offices_names[0]:
            user_office = all_user_offices.get(office__name=office_name)
            return (
                user_office.office.organizational_structure.unique_code
                == self.didattica_cds_articoli_regolamento.didattica_cds_articoli_regolamento_testata.cds.dip.dip_cod
            )
        return True

    def _check_edit_permission(self, user_offices_names, **kwargs):
        offices_names = self.get_offices_names()

        testata_status = (
            DidatticaCdsTestataStatus.objects.filter(
                didattica_cds_articoli_regolamento_testata=self.didattica_cds_articoli_regolamento.didattica_cds_articoli_regolamento_testata.pk
            )
            .order_by("-data_status")
            .first()
        )
        if testata_status is None:
            return False

        status_cod = testata_status.didattica_articoli_regolamento_status.status_cod

        if status_cod == "0" and offices_names[0] in user_offices_names:
            return True
        elif status_cod == "1" and offices_names[1] in user_offices_names:
            return True
        elif status_cod in ["2", "3"] and offices_names[2] in user_offices_names:
            return True

        return False

    def _check_lock_permission(self, user_offices_names, **kwargs):
        return self._check_edit_permission(user_offices_names, **kwargs)

    class Meta:
        managed = True
        db_table = "DIDATTICA_CDS_SUB_ARTICOLI_REGOLAMENTO"
