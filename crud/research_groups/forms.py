from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (RicercaDocenteGruppo, RicercaGruppo)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class RicercaGruppoForm(forms.ModelForm):
    class Meta:
        model = RicercaGruppo
        fields = ['nome', 'descrizione', 'ricerca_erc1']
        widgets = {'descrizione': CKEditorWidget()}

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
        labels = {'dt_inizio': _('Date start'),
                  'dt_fine': _('Date end') }

        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }
