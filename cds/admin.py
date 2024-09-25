from django.contrib import admin

from .models import (
    DidatticaCds,
    DidatticaCdsLingua,
    DidatticaRegolamento,
    DidatticaTestiRegolamento,
)


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
