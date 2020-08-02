from django.contrib import admin
from django.contrib import messages
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . models import *


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaAster1)
class RicercaAster1Admin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaAster2)
class RicercaAster2Admin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaDocenteGruppo)
class RicercaDocenteGruppoAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaDocenteLineaApplicata)
class RicercaDocenteLineaApplicataAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaDocenteLineaBase)
class RicercaDocenteLineaBaseAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaErc1)
class RicercaErc1Admin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaErc2)
class RicercaErc2Admin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaGruppo)
class RicercaGruppoAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaLineaApplicata)
class RicercaLineaApplicataAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')


@admin.register(RicercaLineaBase)
class RicercaLineaBaseAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ins', 'user_mod')
