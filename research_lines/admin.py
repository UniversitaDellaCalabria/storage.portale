from django.contrib import admin

from .admin_inlines import (
    RicercaAster2Inline,
    RicercaDocenteLineaApplicataInline,
    RicercaDocenteLineaBaseInline,
    RicercaLineaApplicataInline,
    RicercaLineaBaseInline,
)
from .models import *


@admin.register(RicercaAster1)
class RicercaAster1Admin(admin.ModelAdmin):
    list_display = ("descrizione",)
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaAster2Inline,
    ]


@admin.register(RicercaAster2)
class RicercaAster2Admin(admin.ModelAdmin):
    list_display = (
        "ricerca_aster1",
        "descrizione",
    )
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaLineaApplicataInline,
    ]


#  @admin.register(RicercaDocenteLineaApplicata)
#  class RicercaDocenteLineaApplicataAdmin(admin.ModelAdmin):
#  readonly_fields = ('user_ins', 'user_mod')


#  @admin.register(RicercaDocenteLineaBase)
#  class RicercaDocenteLineaBaseAdmin(admin.ModelAdmin):
#  readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaErc1)
class RicercaErc1Admin(admin.ModelAdmin):
    list_display = (
        "cod_erc1",
        "descrizione",
    )
    readonly_fields = ("user_ins", "user_mod")


@admin.register(RicercaErc2)
class RicercaErc2Admin(admin.ModelAdmin):
    search_fields = ("cod_erc2",)
    list_filter = ("ricerca_erc1",)
    list_display = (
        "cod_erc2",
        "ricerca_erc1",
        "descrizione",
    )
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaLineaBaseInline,
    ]


@admin.register(RicercaLineaApplicata)
class RicercaLineaApplicataAdmin(admin.ModelAdmin):
    list_display = (
        "descrizione",
        "ricerca_aster2",
        "anno",
        "descr_pubblicaz_prog_brevetto",
    )
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaDocenteLineaApplicataInline,
    ]


@admin.register(RicercaLineaBase)
class RicercaLineaBaseAdmin(admin.ModelAdmin):
    list_display = (
        "descrizione",
        "ricerca_erc2",
        "anno",
        "descr_pubblicaz_prog_brevetto",
    )
    autocomplete_fields = ("ricerca_erc2",)
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaDocenteLineaBaseInline,
    ]
