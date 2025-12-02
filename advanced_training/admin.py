from django.contrib import admin

from .models import AltaFormazioneFinestraTemporale

@admin.register(AltaFormazioneFinestraTemporale)
class AltaFormazioneFinestraTemporaleAdmin(admin.ModelAdmin):
    list_display = ("titolo", "data_inizio", "data_fine", "anno_accademico", "note")