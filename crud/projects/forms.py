
from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (
    ProgettoDatiBase, ProgettoResponsabileScientifico)

from .. utils.settings import CMS_STORAGE_ROOT_API


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class ProgettoDatiBaseForm(forms.ModelForm):
    class Meta:
        model = ProgettoDatiBase
        fields = ['titolo', 'anno_avvio', 'id_ambito_territoriale',
                  'id_tipologia_programma', 'id_area_tecnologica',
                  'descr_breve', 'url_immagine', 'abstract_ita',
                  'abstract_eng', 'url_sito_web', 'call', 'uo']
        labels = {
            'titolo': _('Title'),
            'anno_avvio': _('Start year'),
            'id_ambito_territoriale': _('Territorial scope'),
            'id_tipologia_programma': _('Program type'),
            'id_area_tecnologica': _('Tech Area'),
            'descr_breve': _('Short description'),
            'url_immagine': _('Image URL'),
            'abstract_ita': _('Abstract (it)'),
            'abstract_eng': _('Abstract (en)'),
            'url_sito_web': _('URL'),
            'call': _('Call'),
            'uo': _('Organizational Unit'),
        }
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'descr_breve': CKEditorWidget(),
                   'abstract_ita': CKEditorWidget(),
                   'abstract_eng': CKEditorWidget(),
                   'uo': forms.HiddenInput()}

    class Media:
        js = ('js/textarea-autosize.js',)


class ProgettoResponsabileScientificoForm(forms.ModelForm):
    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ['nome_origine']
        labels = {
            "nome_origine": _("Name and Surname")
        }


class ProgettoRicercatoreForm(forms.ModelForm):
    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ['nome_origine']
        labels = {
            "nome_origine": _("Name and Surname")
        }


class ProgettoStrutturaForm(forms.Form):
    choosen_structure = forms.CharField(label=_('Structure'),
                                        widget=forms.HiddenInput(),
                                        required=True)
