from django.contrib import admin

from .models import ComuniAll, DidatticaDipartimento, TerritorioIt


@admin.register(DidatticaDipartimento)
class DipartimentoAdmin(admin.ModelAdmin):
    readonly_fields = ("dip_des_it", "dip_des_eng")
    list_display = ("dip_cod", "dip_des_it")


@admin.register(ComuniAll)
class ComuniAllAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()


@admin.register(TerritorioIt)
class TerritorioItAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ()
