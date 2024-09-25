from research_lines.admin_inlines import RicercaDocenteLineaApplicataInline, RicercaDocenteLineaBaseInline
from research_groups.admin_inlines import RicercaDocenteGruppoInline
from .models import Personale
from django.contrib import admin


@admin.register(Personale)
class PersonaleAdmin(admin.ModelAdmin):
    readonly_fields = ("user_ins", "user_mod")
    search_fields = ("nome", "cognome", "matricola", "email")
    list_display = ("nome", "cognome", "matricola", "email")
    inlines = [
        RicercaDocenteGruppoInline,
        RicercaDocenteLineaBaseInline,
        RicercaDocenteLineaApplicataInline,
    ]
