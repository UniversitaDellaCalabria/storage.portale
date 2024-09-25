from django.contrib.auth import get_user_model
from django.db import models
from generics.models import InsModAbstract, VisibileModAbstract


class RicercaAster1(InsModAbstract):
    descrizione = models.TextField(db_column="DESCRIZIONE")
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_ra1",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_ra1",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    ricerca_erc0_cod = models.ForeignKey(
        "RicercaErc0",
        models.PROTECT,
        db_column="RICERCA_ERC0_COD",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_ASTER1"

    def __str__(self):  # pragma: no cover
        return "{}".format(self.descrizione)


class RicercaAster2(InsModAbstract):
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=200)
    ricerca_aster1 = models.ForeignKey(
        RicercaAster1, models.DO_NOTHING, db_column="RICERCA_ASTER1_ID"
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_ra2",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_ra2",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_ASTER2"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.ricerca_aster1, self.descrizione)


class RicercaDocenteLineaApplicata(InsModAbstract):
    dt_inizio = models.DateField(db_column="DT_INIZIO", blank=True, null=True)

    dt_fine = models.DateField(db_column="DT_FINE", blank=True, null=True)
    personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="PERSONALE_ID",
        blank=True,
        null=True,
    )
    ricerca_linea_applicata = models.ForeignKey(
        "RicercaLineaApplicata",
        models.CASCADE,
        db_column="RICERCA_LINEA_APPLICATA_ID",
        blank=True,
        null=True,
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rdla",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rdla",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_DOCENTE_LINEA_APPLICATA"


class RicercaDocenteLineaBase(InsModAbstract):
    dt_inizio = models.DateField(db_column="DT_INIZIO", blank=True, null=True)

    dt_fine = models.DateField(db_column="DT_FINE", blank=True, null=True)
    personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="PERSONALE_ID",
        blank=True,
        null=True,
    )
    ricerca_linea_base = models.ForeignKey(
        "RicercaLineaBase",
        models.CASCADE,
        db_column="RICERCA_LINEA_BASE_ID",
        blank=True,
        null=True,
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rdlb",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rdlb",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_DOCENTE_LINEA_BASE"


class RicercaErc0(models.Model):
    # Field name made lowercase.
    erc0_cod = models.CharField(db_column="ERC0_COD", primary_key=True, max_length=2)
    # Field name made lowercase.
    description = models.CharField(db_column="DESCRIPTION", max_length=100)
    description_en = models.CharField(
        db_column="DESCRIPTION_EN", max_length=100, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "RICERCA_ERC0"


class RicercaErc1(InsModAbstract):
    cod_erc1 = models.CharField(db_column="COD_ERC1", unique=True, max_length=40)

    descrizione = models.TextField(db_column="DESCRIZIONE")
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_re1",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_re1",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    ricerca_erc0_cod = models.ForeignKey(
        RicercaErc0, models.PROTECT, db_column="RICERCA_ERC0_COD", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "RICERCA_ERC1"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cod_erc1, self.descrizione)


class RicercaErc2(InsModAbstract):
    cod_erc2 = models.CharField(db_column="COD_ERC2", unique=True, max_length=60)

    descrizione = models.TextField(db_column="DESCRIZIONE")
    ricerca_erc1 = models.ForeignKey(
        RicercaErc1, models.PROTECT, db_column="RICERCA_ERC1_ID", blank=True, null=True
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_re2",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_re2",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_ERC2"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.cod_erc2, self.descrizione)


class RicercaLineaApplicata(InsModAbstract, VisibileModAbstract):
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(
        db_column="DESCR_PUBBLICAZ_PROG_BREVETTO", blank=True, null=True
    )

    anno = models.IntegerField(db_column="ANNO", blank=True, null=True)
    ricerca_aster2 = models.ForeignKey(
        RicercaAster2, models.DO_NOTHING, db_column="RICERCA_ASTER2_ID"
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rla",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rla",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_LINEA_APPLICATA"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.ricerca_aster2, self.descrizione)


class RicercaLineaBase(InsModAbstract, VisibileModAbstract):
    descrizione = models.CharField(db_column="DESCRIZIONE", max_length=400)
    descr_pubblicaz_prog_brevetto = models.TextField(
        db_column="DESCR_PUBBLICAZ_PROG_BREVETTO", blank=True, null=True
    )

    anno = models.IntegerField(db_column="ANNO", blank=True, null=True)
    ricerca_erc2 = models.ForeignKey(
        RicercaErc2, models.DO_NOTHING, db_column="RICERCA_ERC2_ID"
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rlb",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rlb",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_LINEA_BASE"

    def __str__(self):  # pragma: no cover
        return "{} {}".format(self.ricerca_erc2, self.descrizione)
