from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (RicercaDocenteLineaBase,
                                RicercaLineaApplicata,
                                RicercaLineaBase)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class RicercaLineaApplicataForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_aster2']
        widgets = {'descr_pubblicaz_prog_brevetto': CKEditorWidget()}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaLineaBaseForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaBase
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_erc2']
        widgets = {'descr_pubblicaz_prog_brevetto': CKEditorWidget()}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaDocenteLineaBaseForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Teacher'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class RicercaDocenteLineaApplicataForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }