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

from .. utils.settings import (ALLOWED_STRUCTURE_TYPES,
                               CMS_STORAGE_ROOT_API,
                               STRUCTURES_FATHER)
from .. utils.utils import _clean_teacher_dates


ALLOWED_STRUCTURE_TYPES = getattr(
    settings, 'ALLOWED_STRUCTURE_TYPES', ALLOWED_STRUCTURE_TYPES)
CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)
STRUCTURES_FATHER = getattr(
    settings, 'STRUCTURES_FATHER', STRUCTURES_FATHER)


class DidatticaDottoratoAttivitaFormativaAltriDocentiForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaAltriDocenti
        fields = ['cognome_nome_origine']
        labels = {
            "cognome_nome_origine": f'{_("Label")}',
        }


class DidatticaDottoratoAttivitaFormativaDocenteForm(forms.ModelForm):
    class Meta:
        model = DidatticaDottoratoAttivitaFormativaDocente
        fields = ['cognome_nome_origine']
        labels = {
            "cognome_nome_origine": _("Name and Surname"),
        }


class DidatticaDottoratoAttivitaFormativaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        allowed_structures_types = ''
        if ALLOWED_STRUCTURE_TYPES:
            allowed_structures_types = ','.join(ALLOWED_STRUCTURE_TYPES)

        ssd_url = f'{CMS_STORAGE_ROOT_API}{reverse("ricerca:phd-ssd-list")}?page_size=1000'
        ssd_api = requests.get(ssd_url)
        ssd = ssd_api.json()['results']
        lista_ssd = [('', _('Not classifiable'))]

        structures_url = f'{CMS_STORAGE_ROOT_API}{reverse("ricerca:structureslist")}?page_size=1000&father={STRUCTURES_FATHER}&type={allowed_structures_types}'
        structures_api = requests.get(structures_url)
        structures = structures_api.json()['results']
        lista_structures = [('', '-'),]

        lista_tipo_af = [
                         ('', '-'),
                         ('Dipartimentale', 'Dipartimentale'),
                         ('Attività di Ateneo', 'Attività di Ateneo')]

        lista_rif_dott = [('', '-'),]

        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(rif_dottorato__isnull=False)\
                                                   .values('rif_dottorato')\
                                                   .distinct()

        for q in query:
            lista_rif_dott.append((q['rif_dottorato'], q['rif_dottorato']))
        for s in ssd:
            if s['SSD'] != 'Non classificabile':
                lista_ssd.append((s['SSD'], s['SSD']))
        for s in structures:
            lista_structures.append((s['StructureCod'], s['StructureName']))

        self.fields['id_struttura_proponente'] = forms.ChoiceField(
            label=_('Central Structure'),
            choices=lista_structures)
        self.fields['ssd'] = forms.ChoiceField(
            label=_('SSD'),
            choices=lista_ssd)
        self.fields['tipo_af'] = forms.ChoiceField(
            label=_('Type'),
            choices=lista_tipo_af)
        self.fields['rif_dottorato'] = forms.ChoiceField(
            label=_('Reference'),
            choices=lista_rif_dott,
            required=False)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = '__all__'
        exclude = ['dt_mod', 'user_mod_id', 'struttura_proponente_origine']

        labels = {
            'nome_af': _('Denomination'),
            # 'ssd': _('SSD'),
            'cfu': _('CFU'),
            'contenuti_af': _('Contents'),
            # 'rif_dottorato': _('Reference'),
            # 'id_struttura_proponente': _('Central Structure'),
            'modalita_verifica': _('Verification Mode'),
            'avvio': _('Expected Start Date'),
            'fine': _('Expected End Date'),
            'orario_aule': _('Timetable and Classrooms'),
            'num_max_studenti': _('Maximum students number'),
            'num_min_studenti': _('Minimum students number'),
        }

        widgets = {'nome_af': forms.Textarea(attrs={'rows': 1}),
                   # 'rif_dottorato': forms.Textarea(attrs={'rows': 1}),
                   'avvio': BootstrapItaliaDateWidget,
                   'fine': BootstrapItaliaDateWidget,
                   'contenuti_af': CKEditorWidget(),
                   'prerequisiti': CKEditorWidget(),
                   'modalita_verifica': CKEditorWidget(),
                   'orario_aule': CKEditorWidget(),
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)
