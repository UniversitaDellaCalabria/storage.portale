from django.contrib import admin
from django import forms

from .models import (
    RicercaAster2,
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)


class RicercaDocenteLineaApplicataModelForm(forms.ModelForm):
    class Meta:
        model = RicercaDocenteLineaApplicata
        fields = "__all__"
        exclude = ("user_ins", "user_mod")
        #  widgets = {'ordinamento': forms.HiddenInput()}


class RicercaDocenteLineaApplicataInline(admin.TabularInline):
    model = RicercaDocenteLineaApplicata
    #  sortable_field_name = "ordinamento"
    extra = 0
    autocomplete_fields = ("personale",)
    form = RicercaDocenteLineaApplicataModelForm
    classes = [
        "collapse",
    ]


class RicercaDocenteLineaBaseModelForm(forms.ModelForm):
    class Meta:
        model = RicercaDocenteLineaBase
        fields = "__all__"
        exclude = ("user_ins", "user_mod")
        #  widgets = {'ordinamento': forms.HiddenInput()}


class RicercaDocenteLineaBaseInline(admin.TabularInline):
    model = RicercaDocenteLineaBase
    #  sortable_field_name = "ordinamento"
    autocomplete_fields = ("personale",)
    extra = 0
    form = RicercaDocenteLineaBaseModelForm
    classes = [
        "collapse",
    ]


class RicercaAster2ModelForm(forms.ModelForm):
    class Meta:
        model = RicercaAster2
        fields = "__all__"
        exclude = ("user_ins", "user_mod")
        #  widgets = {'ordinamento': forms.HiddenInput()}


class RicercaAster2Inline(admin.TabularInline):
    model = RicercaAster2
    #  sortable_field_name = "ordinamento"
    extra = 0
    form = RicercaAster2ModelForm
    classes = [
        "collapse",
    ]


class RicercaLineaApplicataModelForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = "__all__"
        exclude = ("user_ins", "user_mod")


class RicercaLineaApplicataInline(admin.TabularInline):
    model = RicercaLineaApplicata
    extra = 0
    form = RicercaLineaApplicataModelForm
    classes = [
        "collapse",
    ]


class RicercaLineaBaseModelForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaBase
        fields = "__all__"
        exclude = ("user_ins", "user_mod")


class RicercaLineaBaseInline(admin.TabularInline):
    model = RicercaLineaBase
    extra = 0
    autocomplete_fields = ("ricerca_erc2",)
    form = RicercaLineaBaseModelForm
    classes = [
        "collapse",
    ]
