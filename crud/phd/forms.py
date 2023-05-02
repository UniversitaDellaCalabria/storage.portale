import requests

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

from ricerca_app.models import (DidatticaDottoratoAttivitaFormativa,
                                DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                DidatticaDottoratoAttivitaFormativaDocente)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.utils import _clean_teacher_dates


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DidatticaDottoratoAttivitaFormativaAltriDocentiForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                      widget = forms.HiddenInput(),
                                      required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaAltriDocenti
        fields = ['cognome_nome_origine']
        labels = {
            "cognome_nome_origine": f'{_("Label")} {_("Teacher")}',
        }


class DidatticaDottoratoAttivitaFormativaDocenteForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                      widget = forms.HiddenInput(),
                                      required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaDocente
        fields = ['cognome_nome_origine']
        labels = {
            "cognome_nome_origine": f'{_("Label")} {_("Teacher")}',
        }


class DidatticaDottoratoAttivitaFormativaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        url = f'{CMS_STORAGE_ROOT_API}{reverse("ricerca:phd-ssd-list")}?page_size=1000'
        api = requests.get(url)
        ssd = api.json()['results']
        lista_ssd = []
        lista_tipo_af = [('Dipartimentale','Dipartimentale'),
                         ('Attività di Ateneo', 'Attività di Ateneo')]
        lista_rif_dott = []
        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(rif_dottorato__isnull=False)\
                                                   .values('rif_dottorato')\
                                                   .distinct()

        for q in query:
            lista_rif_dott.append((q['rif_dottorato'], q['rif_dottorato']))
        for s in ssd:
            lista_ssd.append((s['SSD'], s['SSD']))

        self.fields['ssd'] = forms.ChoiceField(choices=lista_ssd)
        self.fields['tipo_af'] = forms.ChoiceField(choices=lista_tipo_af)
        self.fields['rif_dottorato'] = forms.ChoiceField(choices=lista_rif_dott)


    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = '__all__'
        exclude = ['dt_mod', 'user_mod_id', 'struttura_proponente_origine']

        labels = {
            'nome_af': _('Nome Attività Formativa'),
            'ssd': _('SSD'),
            'cfu': _('CFU'),
            'contenuti_af': _('Contenuti Alta Formazione'),
            'rif_dottorato': _('Dottorato di Riferimento'),
            'id_struttura_proponente': _('Struttura Centrale'),
            'modalita_verifica': _('Modalità di Verifica'),
            'avvio': _('Data Prevista di Inizio'),
            'fine': _('Data Prevista di Fine'),
            'orario_aule': _('Orario e Aule'),

        }

        widgets = {'nome_af': forms.Textarea(attrs={'rows': 1}),
                   'rif_dottorato': forms.Textarea(attrs={'rows': 1}),
                   'avvio': BootstrapItaliaDateWidget,
                   'fine': BootstrapItaliaDateWidget,
                   'contenuti_af': CKEditorWidget(),
                   'prerequisiti': CKEditorWidget(),
                   'modalita_verifica': CKEditorWidget(),
                   'orario_aule': CKEditorWidget(),
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)