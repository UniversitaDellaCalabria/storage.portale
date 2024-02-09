from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import SpinoffStartupDatiBase

from .. utils.settings import CMS_STORAGE_ROOT_API
# from .. utils.widgets import RicercaCRUDClearableWidget


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class SpinoffStartupDatiBaseForm(forms.ModelForm):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=False)

    def clean(self):
        cleaned_data = super().clean()
        is_spinoff = cleaned_data.get('is_spinoff', False)
        is_startup = cleaned_data.get('is_startup', False)

        if not is_spinoff and not is_startup:
            msg = _("At least one choice between spinoff and startup must be made")
            self.add_error('is_spinoff', msg)
            self.add_error('is_startup', msg)

    class Meta:
        model = SpinoffStartupDatiBase
        fields = ['is_active', 'piva', 'nome_azienda', 'descrizione_ita',
                  'descrizione_eng', 'url_sito_web',
                  'ceo', 'id_area_tecnologica',
                  'id_area_innovazione_s3_calabria', 'is_startup',
                  'is_spinoff', 'nome_file_logo',
                  'ordinamento']
        labels = {
            'piva': _('VAT number'),
            'nome_azienda': _('Name'),
            'descrizione_ita': _('Description (it)'),
            'descrizione_eng': _('Description (en)'),
            'url_sito_web': _('URL'),
            'id_area_tecnologica': _('Tech Area'),
            'id_area_innovazione_s3_calabria': _('Calabria S3 Innovation'),
            'is_startup': _('Startup'),
            'is_spinoff': _('Spinoff'),
            'nome_file_logo': _('Logo'),
            'ceo': _('CEO'),
            'is_active': _('Active'),
            'ordinamento': _('Ordering')
        }
        widgets = {'descrizione_ita': CKEditor5Widget(),
                   'descrizione_eng': CKEditor5Widget()}

    class Media:
        js = ('js/textarea-autosize.js',)


class SpinoffStartupDatiBaseReferentForm(forms.ModelForm):
    class Meta:
        model = SpinoffStartupDatiBase
        fields = ['referente_unical']
        labels = {
            "referente_unical": _("Name and Surname"),
        }


class SpinoffStartupDipartimentoForm(forms.Form):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=True)
