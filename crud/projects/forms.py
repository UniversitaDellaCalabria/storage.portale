from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (ProgettoDatiBase, ProgettoResponsabileScientifico)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class ProgettoDatiBaseForm(forms.ModelForm):
    class Meta:
        model = ProgettoDatiBase
        fields = ['titolo', 'anno_avvio', 'id_ambito_territoriale',
                  'id_tipologia_programma', 'id_area_tecnologica',
                  'descr_breve', 'url_immagine', 'abstract_ita',
                  'abstract_eng', 'url_sito_web', 'call', 'uo']
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'descr_breve': CKEditorWidget(),
                   'abstract_ita': CKEditorWidget(),
                   'abstract_eng': CKEditorWidget(),
                   'anno_avvio': BootstrapItaliaDateWidget,
                   'uo': forms.HiddenInput()}

    class Media:
        js = ('js/textarea-autosize.js',)


class ProgettoResponsabileScientificoForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ['nome_origine']
        labels = {
            "nome_origine": _("Label")
        }


class ProgettoRicercatoreForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ['nome_origine']
        labels = {
            "nome_origine": _("Label")
        }


class ProgettoStrutturaForm(forms.Form):
    choosen_structure = forms.CharField(label=_('Structure'),
                                        widget=forms.HiddenInput(),
                                        required=True)
