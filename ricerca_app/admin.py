from django.contrib import admin
from django.contrib import messages
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . admin_inlines import *
from . models import *


@admin.register(Personale)
class PersonaleAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')
    search_fields = ('nome', 'cognome', 'matricola', 'email')
    list_display = ('nome', 'cognome', 'matricola', 'email')
    inlines = [
        RicercaDocenteGruppoInline,
        RicercaDocenteLineaBaseInline,
        RicercaDocenteLineaApplicataInline,
    ]


@admin.register(RicercaGruppo)
class RicercaGruppoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione')
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaDocenteGruppoInline, ]


@admin.register(RicercaDocenteGruppo)
class RicercaDocenteGruppoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'dt_inizio', 'dt_fine', 'ricerca_gruppo')
    autocomplete_fields = ('docente',)
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaAster1)
class RicercaAster1Admin(admin.ModelAdmin):
    list_display = ('descrizione',)
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaAster2Inline, ]


@admin.register(RicercaAster2)
class RicercaAster2Admin(admin.ModelAdmin):
    list_display = ('ricerca_aster1', 'descrizione',)
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaLineaApplicataInline, ]


#  @admin.register(RicercaDocenteLineaApplicata)
#  class RicercaDocenteLineaApplicataAdmin(admin.ModelAdmin):
    #  readonly_fields = ('user_ins', 'user_mod')


#  @admin.register(RicercaDocenteLineaBase)
#  class RicercaDocenteLineaBaseAdmin(admin.ModelAdmin):
    #  readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaErc1)
class RicercaErc1Admin(admin.ModelAdmin):
    list_display = ('cod_erc1', 'descrizione',)
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaErc2)
class RicercaErc2Admin(admin.ModelAdmin):
    search_fields = ('cod_erc2', )
    list_filter = ('ricerca_erc1', )
    list_display = ('cod_erc2', 'ricerca_erc1', 'descrizione',)
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaLineaBaseInline, ]


@admin.register(RicercaLineaApplicata)
class RicercaLineaApplicataAdmin(admin.ModelAdmin):
    list_display = ('descrizione', 'ricerca_aster2', 'anno',
                    'descr_pubblicaz_prog_brevetto')
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaDocenteLineaApplicataInline,
               ]


@admin.register(RicercaLineaBase)
class RicercaLineaBaseAdmin(admin.ModelAdmin):
    list_display = ('descrizione', 'ricerca_erc2', 'anno',
                    'descr_pubblicaz_prog_brevetto')
    autocomplete_fields = ('ricerca_erc2', )
    readonly_fields = ('user_ins', 'user_mod')
    inlines = [RicercaDocenteLineaBaseInline, ]


@admin.register(DidatticaDipartimento)
class DipartimentoAdmin(admin.ModelAdmin):
    readonly_fields = ('dip_des_it', 'dip_des_eng')
    list_display = ('dip_cod', 'dip_des_it')


@admin.register(ComuniAll)
class ComuniAllAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(DidatticaCds)
class DidatticaCdsAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(DidatticaCdsLingua)
class DidatticaCdsLinguaAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(DidatticaRegolamento)
class DidatticaRegolamentoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(DidatticaTestiRegolamento)
class DidatticaTestiRegolamentoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(TerritorioIt)
class TerritorioItAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()
