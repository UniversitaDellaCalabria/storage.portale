from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (DidatticaCdsAltriDati, DidatticaCdsAltriDatiUfficio)

from .. utils.settings import CMS_STORAGE_ROOT_API


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DidatticaCdsAltriDatiCoordinatorForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)


class DidatticaCdsAltriDatiUfficioForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDatiUfficio
        fields = ['ordine', 'nome_ufficio', 'nome_origine_riferimento',
                  'telefono', 'email', 'edificio', 'piano', 'orari',
                  'sportello_online']
        labels = {
            "nome_origine_riferimento": f'{_("Label")}',
        }
        help_texts = {
            "nome_origine_riferimento": _("If it is an extension, select it directly from the list below. Otherwise, manually enter or edit the data"),
        }
        widgets = {'orari': CKEditorWidget()}

    class Media:
        js = ('js/textarea-autosize.js',)


class DidatticaCdsAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['nome_origine_coordinatore', 'nome_origine_vice_coordinatore',
                  'num_posti', 'modalita_iscrizione']
        labels = {
            "nome_origine_coordinatore": f'{_("Label")} {_("Coordinator")}',
            "nome_origine_vice_coordinatore": f'{_("Label")} {_("Deputy coordinator")}',
            "num_posti": _("Number of seats"),
            "modalita_iscrizione": _("Registration procedure"),
        }
        help_texts = {
            "nome_origine_coordinatore": _("If it is an extension, select it directly from the list below. Otherwise, manually enter or edit the data"),
            "nome_origine_vice_coordinatore": _("If it is an extension, select it directly from the list below. Otherwise, manually enter or edit the data"),
        }
        widgets = {'modalita_iscrizione': CKEditorWidget()}

    class Media:
        js = ('js/textarea-autosize.js',)
