from django.contrib.auth import get_user_model
from django.db import models
from generics.models import InsModAbstract


class RicercaDocenteGruppo(InsModAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    dt_inizio = models.DateField(db_column="DT_INIZIO", blank=True, null=True)
    dt_fine = models.DateField(db_column="DT_FINE", blank=True, null=True)
    personale = models.ForeignKey(
        "addressbook.Personale",
        models.CASCADE,
        db_column="ID_PERSONALE",
        blank=True,
        null=True,
    )
    ricerca_gruppo = models.ForeignKey(
        "RicercaGruppo", models.CASCADE, db_column="ID_RICERCA_GRUPPO"
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rdg",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rdg",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_DOCENTE_GRUPPO"

    def __str__(self):  # pragma: no cover
        return "{} [{}]".format(self.personale, self.ricerca_gruppo.nome)


class RicercaGruppo(InsModAbstract):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome = models.CharField(db_column="NOME", max_length=200)
    descrizione = models.TextField(db_column="DESCRIZIONE")
    ricerca_erc1 = models.ForeignKey(
        "research_lines.RicercaErc1",
        models.SET_NULL,
        db_column="ID_RICERCA_ERC1",
        blank=True,
        null=True,
    )
    user_ins = models.ForeignKey(
        get_user_model(),
        related_name="user_ins_rg",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user_mod = models.ForeignKey(
        get_user_model(),
        related_name="user_mod_rg",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "RICERCA_GRUPPO"

    def __str__(self):  # pragma: no cover
        return "{}".format(self.nome)
