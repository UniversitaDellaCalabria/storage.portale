from django.contrib import admin

from .admin_inlines import RicercaDocenteGruppoInline
from .models import RicercaDocenteGruppo, RicercaGruppo


@admin.register(RicercaGruppo)
class RicercaGruppoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descrizione")
    readonly_fields = ("user_ins", "user_mod")
    inlines = [
        RicercaDocenteGruppoInline,
    ]


@admin.register(RicercaDocenteGruppo)
class RicercaDocenteGruppoAdmin(admin.ModelAdmin):
    list_display = ("personale", "dt_inizio", "dt_fine", "ricerca_gruppo")
    autocomplete_fields = ("personale",)
    readonly_fields = ("user_ins", "user_mod")
