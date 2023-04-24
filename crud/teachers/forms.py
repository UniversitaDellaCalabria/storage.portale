from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (DocenteMaterialeDidattico,
                                DocentePtaAltriDati,
                                DocentePtaBacheca)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.widgets import RicercaCRUDDateTimeWidget


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DocentePtaAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DocentePtaAltriDati
        fields = ['breve_bio', 'breve_bio_en', 'orario_ricevimento',
                  'orario_ricevimento_en', 'orcid', 'path_foto',
                  'path_cv_ita', 'path_cv_en', ]
        widgets = {'breve_bio_en': CKEditorWidget(),
                   # 'breve_bio': forms.Textarea(attrs={'rows': 2}),
                   'breve_bio': CKEditorWidget(),
                   'orario_ricevimento': CKEditorWidget(),
                   'orario_ricevimento_en': CKEditorWidget()
                   }

    class Media:
        js = ('js/textarea-autosize.js',)


class DocentePtaBachecaForm(forms.ModelForm):
    class Meta:
        model = DocentePtaBacheca
        fields = ['tipo_testo', 'tipo_testo_en','titolo', 'titolo_en',
                  'testo', 'testo_en', 'url_testo', 'url_testo_en',
                  #'dt_pubblicazione',
                  'dt_inizio_validita', 'dt_fine_validita',
                  'ordine', 'attivo']
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
                  'ordine', 'attivo',]
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'titolo_en': forms.Textarea(attrs={'rows': 2}),
                   'testo': CKEditorWidget(),
                   'testo_en': CKEditorWidget(),
                   # 'dt_pubblicazione': BootstrapItaliaDateWidget,
                   'dt_inizio_validita': BootstrapItaliaDateWidget,
                   'dt_fine_validita': BootstrapItaliaDateWidget}

    class Media:
        js = ('js/textarea-autosize.js',)
