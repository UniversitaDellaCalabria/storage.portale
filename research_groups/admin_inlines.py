from django import forms
from .models import RicercaDocenteGruppo
from django.contrib import admin


class RicercaDocenteGruppoModelForm(forms.ModelForm):
    class Meta:
        model = RicercaDocenteGruppo
        fields = "__all__"
        exclude = ("user_ins", "user_mod")
        #  widgets = {'ordinamento': forms.HiddenInput()}


class RicercaDocenteGruppoInline(admin.TabularInline):
    model = RicercaDocenteGruppo
    autocomplete_fields = ("personale",)
    #  sortable_field_name = "ordinamento"
    extra = 0
    form = RicercaDocenteGruppoModelForm
    classes = [
        "collapse",
    ]
