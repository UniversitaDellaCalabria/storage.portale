from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (DocenteMaterialeDidattico,
                                DocentePtaAltriDati,
                                DocentePtaBacheca)

from .. utils.settings import CMS_STORAGE_ROOT_API
# from .. utils.widgets import RicercaCRUDClearableWidget
from .. utils.widgets import RicercaCRUDDateTimeWidget


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DocentePtaAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DocentePtaAltriDati
        fields = ['breve_bio', 'breve_bio_en', 'orario_ricevimento',
                  'orario_ricevimento_en', 'orcid', 'path_foto',
                  'path_cv_ita', 'path_cv_en', ]
        labels = {
            'breve_bio': _('Short Bio (it)'),
            'breve_bio_en': _('Short Bio (en)'),
            'orario_ricevimento': _('Reception hours (it)'),
            'orario_ricevimento_en': _('Reception hours (en)'),
            'path_cv_ita': _('Curriculum (it)'),
            'path_cv_en': _('Curriculum (en)'),
            'path_foto': _('Photo'),
        }
        help_texts = {
            'path_foto': _('Please upload a square format photo'),
        }
        widgets = {'breve_bio_en': CKEditorWidget(),
                   # 'breve_bio': forms.Textarea(attrs={'rows': 2}),
                   'breve_bio': CKEditorWidget(),
                   'orario_ricevimento': CKEditorWidget(),
                   'orario_ricevimento_en': CKEditorWidget()
                   }

        # def __init__(self, *args, **kwargs):
            # super(BrevettoDatiBaseForm, self).__init__(*args, **kwargs)
            # path_cv_ita = self.instance.path_cv_ita
            # self.fields['path_cv_ita'].widget = RicercaCRUDClearableWidget(
                # {'upload_to': path_cv_ita.field.upload_to(
                    # self.instance, path_cv_ita.name)}
            # )
            # path_cv_en = self.instance.path_cv_en
            # self.fields['path_cv_en'].widget = RicercaCRUDClearableWidget(
                # {'upload_to': path_cv_en.field.upload_to(
                    # self.instance, path_cv_en.name)}
            # )
            # path_cv_ita = self.instance.path_cv_ita
            # self.fields['path_cv_ita'].widget = RicercaCRUDClearableWidget(
                # {'upload_to': path_cv_ita.field.upload_to(
                    # self.instance, path_cv_ita.name)}
            # )

    class Media:
        js = ('js/textarea-autosize.js',)


class DocentePtaBachecaForm(forms.ModelForm):
    class Meta:
        model = DocentePtaBacheca
        fields = ['tipo_testo', 'tipo_testo_en', 'titolo', 'titolo_en',
                  'testo', 'testo_en', 'url_testo', 'url_testo_en',
                  # 'dt_pubblicazione',
                  'dt_inizio_validita', 'dt_fine_validita',
                  'ordine', 'attivo']
        labels = {
            'tipo_testo': _('Type (it)'),
            'tipo_testo_en': _('Type (en)'),
            'titolo': _('Title (it)'),
            'titolo_en': _('Title (en)'),
            'testo': _('Text (it)'),
            'testo_en': _('Text (en)'),
            'url_testo': _('URL (it)'),
            'url_testo_en': _('URL (en)'),
            'dt_inizio_validita': _('Valid from'),
            'dt_fine_validita': _('Valid until'),
        }
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'titolo_en': forms.Textarea(attrs={'rows': 2}),
                   'testo': CKEditorWidget(),
                   'testo_en': CKEditorWidget(),
                   # 'dt_pubblicazione': BootstrapItaliaDateWidget,
                   # 'dt_inizio_validita': BootstrapItaliaDateWidget,
                   'dt_inizio_validita': RicercaCRUDDateTimeWidget(),
                   # 'dt_fine_validita': BootstrapItaliaDateWidget}
                   'dt_fine_validita': RicercaCRUDDateTimeWidget}

    class Media:
        js = ('js/textarea-autosize.js',)


class DocenteMaterialeDidatticoForm(forms.ModelForm):
    class Meta:
        model = DocenteMaterialeDidattico
        fields = ['titolo', 'titolo_en', 'testo', 'testo_en',
                  'url_testo', 'url_testo_en',
                  # 'dt_pubblicazione',
                  'dt_inizio_validita', 'dt_fine_validita',
                  'ordine', 'attivo', ]
        labels = {
            'titolo': _('Title (it)'),
            'titolo_en': _('Title (en)'),
            'testo': _('Text (it)'),
            'testo_en': _('Text (en)'),
            'url_testo': _('URL (it)'),
            'url_testo_en': _('URL (en)'),
            'dt_inizio_validita': _('Valid from'),
            'dt_fine_validita': _('Valid until'),
        }
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'titolo_en': forms.Textarea(attrs={'rows': 2}),
                   'testo': CKEditorWidget(),
                   'testo_en': CKEditorWidget(),
                   # 'dt_pubblicazione': BootstrapItaliaDateWidget,
                   'dt_inizio_validita': BootstrapItaliaDateWidget,
                   'dt_fine_validita': BootstrapItaliaDateWidget}

    class Media:
        js = ('js/textarea-autosize.js',)
