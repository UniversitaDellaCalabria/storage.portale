from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (
    DidatticaCdsAltriDati, DidatticaCdsAltriDatiUfficio)

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
        widgets = {'orari': CKEditorWidget()}


class DidatticaCdsAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['num_posti', 'modalita_iscrizione',
                  'nome_origine_coordinatore',
                  'nome_origine_vice_coordinatore',
                  'manifesto_studi', 'regolamento_didattico' ]
        labels = {
            "nome_origine_coordinatore": _("Coordinator"),
            "nome_origine_vice_coordinatore": _("Deputy coordinator"),
            "num_posti": _("Number of seats"),
            "modalita_iscrizione": _("Registration procedure"),
            "manifesto_studi": _("Study manifesto"),
            "regolamento_didattico": _("Didactic regulation"),
        }
        widgets = {'modalita_iscrizione': CKEditorWidget()}
