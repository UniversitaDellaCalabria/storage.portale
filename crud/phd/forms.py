import datetime
import requests

from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import (DidatticaSsd,
                                DidatticaDottoratoAttivitaFormativa,
                                DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                DidatticaDottoratoAttivitaFormativaDocente,
                                UnitaOrganizzativa)

from .. utils.settings import (ALLOWED_STRUCTURE_TYPES,
                               CMS_STORAGE_ROOT_API,
                               STRUCTURES_FATHER)
from .. utils.utils import _clean_teacher_dates

from . settings import PHD_CYCLES


ALLOWED_STRUCTURE_TYPES = getattr(
    settings, 'ALLOWED_STRUCTURE_TYPES', ALLOWED_STRUCTURE_TYPES)
CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)
STRUCTURES_FATHER = getattr(
    settings, 'STRUCTURES_FATHER', STRUCTURES_FATHER)
PHD_CYCLES = getattr(settings, 'PHD_CYCLES', PHD_CYCLES)

class DidatticaDottoratoAttivitaFormativaAltriDocentiForm(forms.ModelForm):
    class Meta:
        model = DidatticaDottoratoAttivitaFormativaAltriDocenti
        fields = ['cognome_nome_origine']
        labels = {
            "cognome_nome_origine": _("Name and Surname"),
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

        ssd_list = DidatticaSsd.objects.all()
        structures = UnitaOrganizzativa.objects.filter(uo_padre=STRUCTURES_FATHER,
                                                       cd_tipo_nodo__in=ALLOWED_STRUCTURE_TYPES,
                                                       dt_fine_val__gte=datetime.datetime.today())

        lista_tipo_af = [
                         ('', '-'),
                         ('Dipartimentale', 'Dipartimentale'),
                         ('Attività di Ateneo', 'Attività di Ateneo')]

        lista_rif_dott = [('Tutti i corsi di dottorato',
                           'Tutti i corsi di dottorato'),]

        query = DidatticaDottoratoAttivitaFormativa.objects\
                                                   .filter(rif_dottorato__isnull=False)\
                                                   .values('rif_dottorato')\
                                                   .distinct()

        for q in query:
            lista_rif_dott.append((q['rif_dottorato'], q['rif_dottorato']))

        self.fields['id_struttura_proponente'] = forms.ModelChoiceField(
            label=_('Central Structure'),
            queryset=structures,
            required=False)
        self.fields['id_didattica_ssd'] = forms.ModelChoiceField(
            queryset=ssd_list,
            label=_('SSD'))
        self.fields['tipo_af'] = forms.ChoiceField(
            label=_('Type'),
            choices=lista_tipo_af)
        self.fields['rif_dottorato'] = forms.ChoiceField(
            label=_('Reference'),
            choices=lista_rif_dott,
            required=True)
        self.fields['ciclo'] = forms.ChoiceField(
            label=_('Cycle'),
            choices=PHD_CYCLES,
            required=True
        )

    def clean(self):
        cleaned_data = super().clean()
        tipo_af = cleaned_data.get('tipo_af')
        rif_dottorato = cleaned_data.get('rif_dottorato', False)

        if tipo_af == 'Dipartimentale' and not rif_dottorato:
            msg = _('Reference PhD required if activity type is Departmental')
            self.add_error('tipo_af', msg)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = '__all__'
        exclude = ['dt_mod', 'user_mod_id', 'ssd', 'struttura_proponente_origine']

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
            'tipologia': _('Tipologia attività')
        }

        widgets = {'nome_af': forms.Textarea(attrs={'rows': 1}),
                   # 'rif_dottorato': forms.Textarea(attrs={'rows': 1}),
                   'contenuti_af': CKEditor5Widget(),
                   'prerequisiti': CKEditor5Widget(),
                   'modalita_verifica': CKEditor5Widget(),
                   'orario_aule': CKEditor5Widget(),
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)
