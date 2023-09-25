import requests

from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse


from ricerca_app.models import LaboratorioDatiBase, LaboratorioDatiErc1, RicercaErc1, LaboratorioAttrezzature, LaboratorioTipologiaRischio, LaboratorioUbicazione

from .. utils.settings import CMS_STORAGE_ROOT_API
# from .. utils.widgets import RicercaCRUDClearableWidget


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class LaboratorioDatiBaseForm(forms.ModelForm):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        laboratory_areas_url = f'{CMS_STORAGE_ROOT_API}{reverse("ricerca:laboratoriesareas")}'
        laboratory_areas_api = requests.get(laboratory_areas_url)
        laboratory_areas = laboratory_areas_api.json()['results']
        lista_areee = []

        lista_scelte_laboratorio_interdipartimentale = [('SI', 'SI'),
                                                        ('NO', 'NO')]

        for l in laboratory_areas:
            lista_areee.append((l['Area'], l['Area']))

        self.fields['ambito'] = forms.ChoiceField(
            label=_('Areas'),
            choices=lista_areee
        )
        self.fields['laboratorio_interdipartimentale'] = forms.ChoiceField(
            label=_('Interdepartimental Laboratory'),
            choices=lista_scelte_laboratorio_interdipartimentale
        )


    class Meta:
        model = LaboratorioDatiBase
        fields = ['nome_laboratorio', 'acronimo', 'logo_laboratorio', 'laboratorio_interdipartimentale',
                  'altre_strutture_riferimento', 'descr_altre_strutture_riferimento_it',
                  'descr_altre_strutture_riferimento_en', 'ambito',
                  'finalita_ricerca_en', 'finalita_ricerca_it',
                  'finalita_servizi_en', 'finalita_servizi_it',
                  'finalita_didattica_en', 'finalita_didattica_it',
                  'sede_dimensione', 'sede_note_descrittive',
                  'strumentazione_descrizione', 'strumentazione_valore',
                  'id_infrastruttura_riferimento',
                  'sito_web', 'nome_file_logo']
        labels = {
            'nome_laboratorio': _('Name'),
            'acronimo': _('Acronym'),
            'logo_laboratorio': _('Link Laboratory Logo'),
            'laboratorio_interdipartimentale': _('Interdepartmetal Laboratory'),
            'altre_strutture_riferimento': _('Other Structures'),
            'descr_altre_strutture_riferimento_it': _('Other Structures Description (it)'),
            'descr_altre_strutture_riferimento_en': _('Other Structures Description (en)'),
            'ambito': _('Scope'),
            'finalita_ricerca_it': _('Research Purposes (it)'),
            'finalita_ricerca_en': _('Research Purposes (en)'),
            'finalita_servizi_it': _('Service Purposes (it)'),
            'finalita_servizi_en': _('Service Purposes (en)'),
            'finalita_didattica_it': _('Educational Purposes (it)'),
            'finalita_didattica_en': _('Educational Purposes (en)'),
            'sede_dimensione': _('Office Dimension'),
            'sede_note_descrittive': _('Office Description Notes'),
            'strumentazione_descrizione': _('Instrumentation Description'),
            'strumentazione_valore': _('Instrumentation Value'),
            'id_infrastruttura_riferimento': _("Reference Infrastrucure"),
            'sito_web': _('Website'),
            'nome_file_logo': _('Logo')
        }
        widgets = {'descr_altre_strutture_riferimento_it': CKEditorWidget(),
                   'descr_altre_strutture_riferimento_en': CKEditorWidget(),
                   'finalita_ricerca_it': CKEditorWidget(),
                   'finalita_ricerca_en': CKEditorWidget(),
                   'finalita_servizi_it': CKEditorWidget(),
                   'finalita_servizi_en': CKEditorWidget(),
                   'finalita_didattica_it': CKEditorWidget(),
                   'finalita_didattica_en': CKEditorWidget(),
                   'strumentazione_descrizione': CKEditorWidget(),
                   'sede_note_descrittive': CKEditorWidget(),
                  }

    class Media:
        js = ('js/textarea-autosize.js: CKEditorWidget(),',)


class LaboratorioDatiBaseUnicalReferentForm(forms.ModelForm):
    class Meta:
        model = LaboratorioDatiBase
        fields = ['referente_compilazione', 'email_compilazione']
        labels = {
            "referente_compilazione": _("Name and Surname"),
            "email_compilazione": _("Email")
        }
        
class LaboratorioDatiBaseScientificDirectorForm(forms.ModelForm):
    class Meta:
        model = LaboratorioDatiBase
        fields = ['responsabile_scientifico']
        labels = {
            "responsabile_scientifico": _("Name and Surname")
        }

class LaboratorioDatiBaseScientificDirectorChoosenPersonForm(forms.Form):
    choosen_scientific_director = forms.CharField(label=_('Scientific Director'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        super(LaboratorioDatiBaseScientificDirectorChoosenPersonForm, self).__init__(*args, **kwargs)
        if required:
            self.fields['choosen_scientific_director'].required = True

class LaboratorioDatiBaseUnicalReferentChoosenPersonForm(forms.Form):
    choosen_unical_referent = forms.CharField(label=_('Unical Referent'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        super(LaboratorioDatiBaseUnicalReferentChoosenPersonForm, self).__init__(*args, **kwargs)
        if required:
            self.fields['choosen_unical_referent'].required = True


# class LaboratorioDatiBaseReferentForm(forms.ModelForm):
#     class Meta:
#         model = LaboratorioDatiBase
#         fields = ['referente_compilazione']
#         labels = {
#             "referente_compilazione": _("Name and Surname")
#         }


class LaboratorioDatiBaseDipartimentoForm(forms.Form):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=True)


class LaboratorioAltriDipartimentiForm(forms.Form):
    choosen_department = forms.CharField(label=_('Department'),
                                         widget=forms.HiddenInput(),
                                         required=True)

class LaboratorioAttrezzatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LaboratorioAttrezzature
        fields = ['tipologia', 'descrizione', 'fondi', 'costo_unitario', 'quantita', 'tipo_rischi']
        labels = {
            'tipologia': _('Type'),
            'descrizione': _('Description'),
            'fondi': _('Funds'),
            'costo_unitario': _('Unit Cost'),
            'quantita': _('Quantity'),
            'tipo_rischi': _('Type of Risks')
        }

class LaboratorioTipologiaRischioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipologia_rischio'] = forms.CharField(
            label=_('Tipologia Rischio'),
            required=True
        )

    class Meta:
        model = LaboratorioTipologiaRischio
        fields = ['tipologia_rischio']
        labels = {
            'tipologia_rischio': _('Type of Risks'),
        }

class LaboratorioDatiErc1Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        lista_erc1 = []
        ricerca_erc1 = RicercaErc1.objects.all()
        for erc1 in ricerca_erc1:
            kv = (erc1.id, erc1.descrizione)
            lista_erc1.append(kv)
        
        tuple_erc1 = tuple(lista_erc1)
        
        self.fields['id_ricerche_erc1'] = forms.MultipleChoiceField(
            label=_('Ricerche ERC1'),
            choices=tuple_erc1,
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )

class LaboratorioUbicazioneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['sede_principale'] = forms.ChoiceField(
            label=_('Main Location'),
            choices=(('SI', 'SI'), ('NO', 'NO')),
            required=True
        )
        
    
    class Meta:
        model = LaboratorioUbicazione
        fields = ['edificio', 'piano', 'sede_principale', 'note']
        labels = {
            'edificio': _('Building'),
            'piano': _('Floor'),
            'sede_principale': _('Main Location'),
            'note': _('Notes'),
        }
