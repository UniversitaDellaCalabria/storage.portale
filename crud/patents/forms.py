from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (BrevettoDatiBase, BrevettoInventori)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates
from .. utils.widgets import RicercaCRUDClearableWidget


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class BrevettoDatiBaseForm(forms.ModelForm):

    class Meta:
        model = BrevettoDatiBase
        labels = {
            'id_univoco': _('Unique ID'),
            'titolo': _('Title'),
            'breve_descrizione': _('Short description'),
            'id_area_tecnologica': _('Tech area'),
            'url_knowledge_share': _('URL Knowledge Share'),
            'applicazioni': _('Applications'),
            'vantaggi': _('Advantages'),
            'trl_aggiornato': _('Updated TRL'),
            'proprieta': _('Property'),
            'id_status_legale': _('Legal status'),
            'data_priorita': _('Date'),
            'territorio': _('Territory'),
            'id_diritto_commerciale': _('Commercial right'),
            'id_disponibilita': _('Availability'),
            'area_ks': _('Area KS'),
            'nome_file_logo': _('Logo'),
            'url_immagine': _('Logo URL')
        }
        fields = ['id_univoco',
                  'titolo',
                  'breve_descrizione',
                  'id_area_tecnologica',
                  'url_knowledge_share',
                  'applicazioni',
                  'vantaggi',
                  'trl_aggiornato',
                  'proprieta',
                  'id_status_legale',
                  'data_priorita',
                  'territorio',
                  'id_diritto_commerciale',
                  'id_disponibilita',
                  'area_ks',
                  'nome_file_logo',
                  'url_immagine']
        widgets = {'breve_descrizione': CKEditorWidget(),
                   'applicazioni': CKEditorWidget(),
                   'vantaggi': CKEditorWidget(),
                   'data_priorita': BootstrapItaliaDateWidget,}

    def __init__(self, *args, **kwargs):
        super(BrevettoDatiBaseForm, self).__init__(*args, **kwargs)
        _logo_field = self.instance.nome_file_logo
        self.fields['nome_file_logo'].widget = RicercaCRUDClearableWidget(
            {'upload_to': _logo_field.field.upload_to(self.instance, _logo_field.name)}
        )

    class Media:
        js = ('js/textarea-autosize.js',)


class BrevettoInventoriForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    class Meta:
        model = BrevettoInventori
        fields = ['cognomenome_origine']
        labels = {
            "cognomenome_origine": _("Label"),
        }
