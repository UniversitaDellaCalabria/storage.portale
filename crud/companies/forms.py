from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (SpinoffStartupDatiBase,
                                SpinoffStartupDipartimento)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.widgets import RicercaCRUDClearableWidget


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class SpinoffStartupDatiBaseForm(forms.ModelForm):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=False)

    class Meta:
        model = SpinoffStartupDatiBase
        fields = ['piva', 'nome_azienda', 'descrizione_ita',
                  'descrizione_eng', 'url_sito_web',
                  'ceo', 'id_area_tecnologica',
                  'id_area_innovazione_s3_calabria', 'is_startup',
                  'is_spinoff', 'nome_file_logo']
        widgets = {'descrizione_ita': CKEditorWidget(),
                   'descrizione_eng': CKEditorWidget()}

    def __init__(self, *args, **kwargs):
        super(SpinoffStartupDatiBaseForm, self).__init__(*args, **kwargs)
        _logo_field = self.instance.nome_file_logo
        self.fields['nome_file_logo'].widget = RicercaCRUDClearableWidget(
            {'upload_to': _logo_field.field.upload_to(self.instance, _logo_field.name)}
        )

    class Media:
        js = ('js/textarea-autosize.js',)


class SpinoffStartupDatiBaseReferentForm(forms.ModelForm):

    class Meta:
        model = SpinoffStartupDatiBase
        fields = ['referente_unical']
        labels = {
            "referente_unical": _("Label"),
        }


class SpinoffStartupDatiBaseReferentWithoutIDForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    class Meta:
        model = SpinoffStartupDatiBase
        fields = []

    class Media:
        js = ('js/textarea-autosize.js',)


class SpinoffStartupDipartimentoForm(forms.ModelForm):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=False)

    class Meta:
        model = SpinoffStartupDipartimento
        fields = []

    class Media:
        js = ('js/textarea-autosize.js',)
