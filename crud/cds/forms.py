from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import (
    DidatticaCds, DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio, DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti)

from .. utils.forms import ChoosenPersonForm
from .. utils.settings import CMS_STORAGE_ROOT_API


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DidatticaCdsAltriDatiCoordinatorForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)


class DidatticaCdsAltriDatiUfficioForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDatiUfficio
        fields = ['ordine', 'nome_ufficio',
                  'telefono', 'email', 'edificio', 'piano', 'orari',
                  'sportello_online', 'nome_origine_riferimento', ]
        labels = {
            "nome_origine_riferimento": _("Responsible"),
        }
        widgets = {'orari': CKEditor5Widget()}


class DidatticaCdsAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['num_posti', 'modalita_iscrizione',
                  'nome_origine_coordinatore',
                  'nome_origine_vice_coordinatore']
                  # 'manifesto_studi', 'regolamento_didattico']
        labels = {
            "nome_origine_coordinatore": _("Coordinator"),
            "nome_origine_vice_coordinatore": _("Deputy coordinator"),
            "num_posti": _("Number of seats"),
            "modalita_iscrizione": _("Registration procedure"),
            "visibile": _("Visibile"),
            # "manifesto_studi": _("Study manifesto"),
            # "regolamento_didattico": _("Didactic regulation"),
        }
        widgets = {'modalita_iscrizione': CKEditor5Widget()}


class DidatticaCdsOrdinamentoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['ordinamento_didattico']
        labels = {
            "ordinamento_didattico": _("Teaching system"),
        }


class DidatticaCdsManifestoRegolamentoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['manifesto_studi', 'regolamento_didattico']
        labels = {
            "manifesto_studi": _("Study manifesto"),
            "regolamento_didattico": _("Didactic regulation"),
        }


class DidatticaCdsGruppoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsGruppi
        fields = ['visibile', 'descr_breve_it', 'descr_breve_en', 'descr_lunga_it',
                  'descr_lunga_en', 'ordine']
        # labels = {
            # "manifesto_studi": _("Study manifesto"),
            # "regolamento_didattico": _("Didactic regulation"),
        # }
        widgets = {'descr_breve_it': forms.Textarea(attrs={'rows': 2}),
                   'descr_breve_en': forms.Textarea(attrs={'rows': 2}),
                   'descr_lunga_it': forms.Textarea(attrs={'rows': 2}),
                   'descr_lunga_en': forms.Textarea(attrs={'rows': 2})}



    class Media:
        js = ('js/textarea-autosize.js',)


class DidatticaCdsGruppoComponenteForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsGruppiComponenti
        fields = ['visibile', 'nome', 'cognome', 'funzione_it',
                  'funzione_en', 'ordine']


class ChoosenPersonForm(ChoosenPersonForm, forms.ModelForm):

    class Meta:
        model = DidatticaCdsGruppiComponenti
        fields = ['visibile', 'funzione_it', 'funzione_en', 'ordine']
