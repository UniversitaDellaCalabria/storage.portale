from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import (RicercaDocenteGruppo, RicercaGruppo)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class RicercaGruppoForm(forms.ModelForm):
    class Meta:
        model = RicercaGruppo
        fields = ['nome', 'descrizione', 'ricerca_erc1']
        labels = {
            'nome': _('Name'),
            'description': _('Description'),
            'ricerca_erc1': _('ERC1')
        }
        widgets = {'descrizione': CKEditor5Widget()}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaGruppoDocenteForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteGruppo
        fields = ['dt_inizio', 'dt_fine']
        labels = {
            'dt_inizio': _('From'),
            'dt_fine': _('To')}

        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }
