from django.contrib import admin

from .models import (
    DidatticaCds,
    DidatticaCdsCollegamento,
    DidatticaCdsLingua,
    DidatticaRegolamento,
)


@admin.register(DidatticaCds)
class DidatticaCdsAdmin(admin.ModelAdmin):
    list_display = ("cds_id", "cds_cod", "nome_cds_it", "dip")
    search_fields = ("nome_cds_it", "cds_cod")
    list_display_links = ("cds_id",)
    list_filter = ("tipo_corso_cod",)


@admin.register(DidatticaCdsLingua)
class DidatticaCdsLinguaAdmin(admin.ModelAdmin):
    @admin.display(description="CDS")
    def cds(self, obj):
        return f"{obj.cdsord.cds_cod} - {obj.cdsord.nome_cds_it}"

    @admin.display(description="ISO COD")
    def iso_cod(self, obj):
        return obj.iso6392_cod.upper()

    list_display = ("cds", "iso_cod")
    list_display_links = ("cds",)
    list_filter = ("iso6392_cod",)
    search_fields = (
        "cdsord__nome_cds_it",
        "cdsord__cds_cod",
    )
    search_help_text = "Search by Cds Name or Cds Cod"


@admin.register(DidatticaRegolamento)
class DidatticaRegolamentoAdmin(admin.ModelAdmin):
    list_display = ("regdid_id", "aa_reg_did", "cds")
    list_display_links = ("regdid_id",)
    list_filter = ("cds__tipo_corso_cod",)
    search_fields = (
        "cds__nome_cds_it",
        "cds__cds_cod",
    )
    search_help_text = "Search by Cds Name or Cds Cod"

@admin.register(DidatticaCdsCollegamento)
class DidattiCdsCollegamentoAdmin(admin.ModelAdmin):
    @admin.display(description="New CDS COD", ordering="cds__cds_cod")
    def cds_cod(self, obj):
        return obj.cds.cds_cod

    @admin.display(description="Previous CDS COD", ordering="cds_prec__cds_cod")
    def cds_prec_cod(self, obj):
        return obj.cds_prec.cds_cod

    @admin.display(description="New CDS Name", ordering="cds__nome_cds_it")
    def cds_nome_cds_it(self, obj):
        return obj.cds.nome_cds_it

    @admin.display(description="Previous CDS Name", ordering="cds_prec__nome_cds_it")
    def cds_prec_nome_cds_it(self, obj):
        return obj.cds_prec.nome_cds_it

    list_display = (
        "cds_cod",
        "cds_nome_cds_it",
        "cds_prec_cod",
        "cds_prec_nome_cds_it",
    )
    list_display_links = (
        "cds_cod",
        "cds_prec_cod",
    )
    search_fields = (
        "cds__nome_cds_it",
        "cds_prec__nome_cds_it",
        "cds__cds_cod",
        "cds_prec__cds_cod",
    )
    search_help_text = "Search by Cds Name or Cds Cod"
    raw_id_fields = ("cds", "cds_prec")
    list_select_related = ("cds", "cds_prec")
