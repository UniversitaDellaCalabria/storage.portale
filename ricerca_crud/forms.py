from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings


from ricerca_crud.settings import CMS_STORAGE_ROOT_API

import json
import requests

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

import ricerca_app.api_views
from ricerca_app.models import (BrevettoDatiBase, BrevettoInventori,
                                DidatticaCdsAltriDati, DidatticaCdsAltriDatiUfficio,
                                DocenteMaterialeDidattico, DocentePtaAltriDati,
                                DocentePtaBacheca, ProgettoDatiBase,
                                ProgettoResponsabileScientifico, RicercaDocenteGruppo,
                                RicercaDocenteLineaBase, RicercaGruppo,
                                RicercaLineaApplicata, RicercaLineaBase,
                                SpinoffStartupDatiBase,
                                SpinoffStartupDipartimento,
                                DidatticaDottoratoAttivitaFormativa,
                                DidatticaDottoratoAttivitaFormativaAltriDocenti,
                                DidatticaDottoratoAttivitaFormativaDocente)

CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)

# common methods
def _clean_teacher_dates(obj, cleaned_data):
    dt_inizio = cleaned_data.get('dt_inizio')
    dt_fine = cleaned_data.get('dt_fine')

    if dt_inizio and dt_fine and dt_inizio > dt_fine:
        obj.add_error('dt_inizio',
                      _("Start date is greater than end date"))
        obj.add_error('dt_fine',
                      _("Start date is greater than end date"))
# end common methods


class RicercaGruppoForm(forms.ModelForm):
    class Meta:
        model = RicercaGruppo
        fields = ['nome', 'descrizione', 'ricerca_erc1']
        widgets = {'descrizione': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaGruppoDocenteForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteGruppo
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class RicercaLineaApplicataForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_aster2']
        widgets = {'descr_pubblicaz_prog_brevetto': forms.Textarea(attrs={
                                                                   'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaLineaBaseForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaBase
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_erc2']
        widgets = {'descr_pubblicaz_prog_brevetto': forms.Textarea(attrs={
                                                                   'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaDocenteLineaBaseForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Teacher'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class RicercaDocenteLineaApplicataForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class DidatticaCdsAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['nome_origine_coordinatore', 'nome_origine_vice_coordinatore',
                  'num_posti', 'modalita_iscrizione']
        labels = {
            "nome_origine_coordinatore": _("Coordinator name (plain text)"),
            "nome_origine_vice_coordinatore": _("Deputy coordinator name (plain text)"),
            "num_posti": _("Number of seats"),
            "modalita_iscrizione": _("Registration procedure"),
        }
        help_texts = {
            "nome_origine_coordinatore": _("Change this field only if necessary or if the person you are looking for is not in the database"),
            "nome_origine_vice_coordinatore": _("Change this field only if necessary or if the person you are looking for is not in the database"),
        }
        widgets = {'modalita_iscrizione': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class DidatticaCdsAltriDatiCoordinatorForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)


class DidatticaCdsAltriDatiUfficioForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDatiUfficio
        fields = ['ordine', 'nome_ufficio', 'nome_origine_riferimento',
                  'telefono', 'email', 'edificio', 'piano', 'orari',
                  'sportello_online']
        labels = {
            "nome_origine_riferimento": _("Responsible name (plain text)"),
        }
        help_texts = {
            "nome_origine_riferimento": _("Change this field only if necessary or if the person you are looking for is not in the database"),
        }
        widgets = {'orari': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class BrevettoDatiBaseForm(forms.ModelForm):

    class Meta:
        model = BrevettoDatiBase
        fields = ['id_univoco', 'titolo', 'url_immagine',
                  'breve_descrizione', 'id_area_tecnologica',
                  'url_knowledge_share', 'applicazioni', 'vantaggi',
                  'trl_aggiornato', 'proprieta', 'id_status_legale',
                  'data_priorita', 'territorio', 'id_diritto_commerciale',
                  'id_disponibilita', 'area_ks', 'nome_file_logo']
        widgets = {'breve_descrizione': forms.Textarea(attrs={'rows': 2}),
                   'applicazioni': forms.Textarea(attrs={'rows': 2}),
                   'vantaggi': forms.Textarea(attrs={'rows': 2}),
                   'data_priorita': BootstrapItaliaDateWidget}

    class Media:
        js = ('js/textarea-autosize.js',)


class BrevettoInventoriForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = BrevettoInventori
        fields = ['cognomenome_origine']
        labels = {
            "cognomenome_origine": _("Inventor name (plain text)"),
        }
        help_texts = {
            "cognomenome_origine": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }


class BrevettoInventoriWithoutFieldsForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = BrevettoInventori
        fields = []


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
        widgets = {'descrizione_ita': forms.Textarea(attrs={'rows': 2}),
                   'descrizione_eng': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class SpinoffStartupDatiBaseReferentForm(forms.ModelForm):

    class Meta:
        model = SpinoffStartupDatiBase
        fields = ['referente_unical']
        labels = {
            "referente_unical": _("Unical referent name (plain text)"),
        }
        help_texts = {
            "referente_unical": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }

    class Media:
        js = ('js/textarea-autosize.js',)


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
                                         required=True)

    class Meta:
        model = SpinoffStartupDipartimento
        fields = []

    class Media:
        js = ('js/textarea-autosize.js',)


class ProgettoDatiBaseForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=True)

    class Meta:
        model = ProgettoDatiBase
        fields = ['titolo', 'anno_avvio', 'id_ambito_territoriale',
                  'id_tipologia_programma', 'id_area_tecnologica',
                  'descr_breve', 'url_immagine', 'abstract_ita',
                  'abstract_eng', 'url_sito_web', 'call', 'uo']
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'descr_breve': forms.Textarea(attrs={'rows': 2}),
                   'abstract_ita': forms.Textarea(attrs={'rows': 2}),
                   'abstract_eng': forms.Textarea(attrs={'rows': 2}),
                   'anno_avvio': BootstrapItaliaDateWidget, 'uo': forms.HiddenInput()}

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
            "nome_origine": _("Director name (plain text)"),
        }
        help_texts = {
            "nome_origine": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }


class ProgettoResponsabileScientificoWithoutFieldsForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = ProgettoResponsabileScientifico
        fields = []


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
            "nome_origine": _("Director name (plain text)"),
        }
        help_texts = {
            "nome_origine": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }


class ProgettoRicercatoreWithoutFieldsForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = ProgettoResponsabileScientifico
        fields = []


class ProgettoDatiBaseFormWithoutFields(forms.ModelForm):
    choosen_structure = forms.CharField(label=_('Structure'),
                                        widget=forms.HiddenInput(),
                                        required=True)

    class Meta:
        model = ProgettoDatiBase
        fields = []

    class Media:
        js = ('js/textarea-autosize.js',)


class DocentePtaAltriDatiForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=True)

    class Meta:
        model = DocentePtaAltriDati
        fields = ['breve_bio', 'breve_bio_en', 'orario_ricevimento',
                  'orario_ricevimento_en', 'orcid', 'path_foto',
                  'path_cv_ita', 'path_cv_en', ]
        widgets = {'breve_bio_en': forms.Textarea(attrs={'rows': 2}),
                   'breve_bio': forms.Textarea(attrs={'rows': 2}),
                   'orario_ricevimento': forms.Textarea(attrs={'rows': 2}),
                   'orario_ricevimento_en': forms.Textarea(attrs={'rows': 2})
                   }

    class Media:
        js = ('js/textarea-autosize.js',)


class DocentePtaBachecaForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=True)

    class Meta:
        model = DocentePtaBacheca
        fields = ['titolo', 'titolo_en', 'tipo_testo', 'tipo_testo_en',
                  'testo', 'testo_en', 'url_testo', 'url_testo_en',
                  'ordine', 'attivo', 'dt_pubblicazione',
                  'dt_inizio_validita', 'dt_fine_validita']
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'titolo_en': forms.Textarea(attrs={'rows': 2}),
                   'testo': forms.Textarea(attrs={'rows': 2}),
                   'testo_en': forms.Textarea(attrs={'rows': 2}),
                   'dt_pubblicazione': BootstrapItaliaDateWidget,
                   'dt_inizio_validita': BootstrapItaliaDateWidget,
                   'dt_fine_validita': BootstrapItaliaDateWidget}

        help_texts = {
            "attivo": _(
                "Set 0 if is not active. 1 otherwise."),
        }

    class Media:
        js = ('js/textarea-autosize.js',)


class DocenteMaterialeDidatticoForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=True)

    class Meta:
        model = DocenteMaterialeDidattico
        fields = ['titolo', 'titolo_en', 'testo', 'testo_en',
                  'url_testo', 'url_testo_en', 'ordine', 'attivo',
                  'dt_pubblicazione', 'dt_inizio_validita', 'dt_fine_validita']
        widgets = {'titolo': forms.Textarea(attrs={'rows': 2}),
                   'titolo_en': forms.Textarea(attrs={'rows': 2}),
                   'testo': forms.Textarea(attrs={'rows': 2}),
                   'testo_en': forms.Textarea(attrs={'rows': 2}),
                   'dt_pubblicazione': BootstrapItaliaDateWidget,
                   'dt_inizio_validita': BootstrapItaliaDateWidget,
                   'dt_fine_validita': BootstrapItaliaDateWidget}

        help_texts = {
            "attivo": _(
                "Set 0 if is not active. 1 otherwise."),
        }

    class Media:
        js = ('js/textarea-autosize.js',)




class DidatticaDottoratoAttivitaFormativaForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=True)

    def __init__(self, *args, **kwargs):
        url = f'{CMS_STORAGE_ROOT_API}{reverse("ricerca:phd-ssd-list")}?page_size=1000'
        api = requests.get(url)
        ssd = api.json()['results']
        lista_ssd = []
        lista_tipo_af = [('Dipartimentale','Dipartimentale'),('Attività di Ateneo', 'Attività di Ateneo')]
        lista_rif_dott = []
        query = DidatticaDottoratoAttivitaFormativa.objects.values('rif_dottorato').distinct()

        for q in query:
            lista_rif_dott.append((q['rif_dottorato'], q['rif_dottorato']))
        for s in ssd:
            lista_ssd.append((s['SSD'], s['SSD']))
        super().__init__(*args, **kwargs)

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


        widgets = {'nome_af': forms.Textarea(attrs={'rows': 3}), 'rif_dottorato': forms.Textarea(attrs={'rows': 1}), \
                   'avvio': BootstrapItaliaDateWidget, 'fine': BootstrapItaliaDateWidget, \
                   'contenuti_af': forms.Textarea(attrs={'rows': 4}), 'prerequisiti': forms.Textarea(attrs={'rows': 2}), \
                   'modalita_verifica': forms.Textarea(attrs={'rows': 3}), 'orario_aule': forms.Textarea(attrs={'rows': 4})}


        help_texts = {
            "nome_af": _(
                "*Campo necessario"),

            "ssd": _(
                "*Campo necessario"),

            "numero_ore": _(
                "*Campo necessario"),

            "cfu": _(
                "*Campo necessario"),

            "tipo_af": _(
                "*Campo necessario"),

            "rif_dottorato": _(
                "*Campo necessario"),

            "id_struttura_proponente": _(
                "*Campo necessario"),

            "contenuti_af": _(
                "*Campo necessario"),

            "modalita_verifica": _(
                "*Campo necessario"),

        }

    class Media:
        js = ('js/textarea-autosize.js',)



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
            "cognome_nome_origine": _("Teacher name (plain text)"),
        }
        help_texts = {
            "cognome_nome_origine": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }


class DidatticaDottoratoAttivitaFormativaDocenteWithoutFieldsForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                      widget = forms.HiddenInput(),
                                      required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaDocente
        fields = []



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
            "cognome_nome_origine": _("Teacher name (plain text)"),
        }
        help_texts = {
            "cognome_nome_origine": _(
                "Change this field only if necessary or if the person you are looking for is not in the database"),
        }


class DidatticaDottoratoAttivitaFormativaAltriDocentiWithoutFieldsForm(forms.ModelForm):
    choosen_person = forms.CharField(label=_('Person'),
                                      widget = forms.HiddenInput(),
                                      required=False)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = DidatticaDottoratoAttivitaFormativaAltriDocenti
        fields = []
