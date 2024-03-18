
from decimal import Decimal
from datetime import date as dt

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import *


# from .. utils.widgets import RicercaCRUDClearableWidget


class LaboratorioDatiBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        operator_departments_codes = kwargs.pop('allowed_department_codes', [])

        super().__init__(*args, **kwargs)

        if operator_departments_codes:
            department_choices = DidatticaDipartimento.objects.filter(dip_cod__in=operator_departments_codes)\
                                                .values_list('dip_id', 'dip_des_it')
        else:
            department_choices = DidatticaDipartimento.objects.all()\
                                                .values_list('dip_id', 'dip_des_it')

        self.fields["choosen_department_id"] = forms.MultipleChoiceField(label=_('Related Department'),
                                            choices=tuple(department_choices),
                                            required=True
                                            )
       
        # self.fields['laboratorio_interdipartimentale'] = forms.ChoiceField(
        #     label=_('Interdepartmental Laboratory'),
        #     choices=(('SI', 'SI'),('NO', 'NO')),
        # )

        self.order_fields(field_order=
                          ( 'nome_laboratorio',
                            'acronimo',
                            'logo_laboratorio',
                            'nome_file_logo',
                            'choosen_department_id',
                            'id_infrastruttura_riferimento',
                            'altre_strutture_riferimento',
                            'descr_altre_strutture_riferimento_it',
                            'descr_altre_strutture_riferimento_en',
                            'sito_web',
                            #'ambito',
                            #'sede_dimensione', 'sede_note_descrittive',
                            #'strumentazione_descrizione', 'strumentazione_valore',
                            #'laboratorio_interdipartimentale',
                            ))

    class Meta:
        model = LaboratorioDatiBase
        fields = ['nome_laboratorio', 'acronimo', 'logo_laboratorio',# 'laboratorio_interdipartimentale',
                  'altre_strutture_riferimento', 'descr_altre_strutture_riferimento_it',
                  'descr_altre_strutture_riferimento_en',# 'ambito',
                  #'sede_dimensione', 'sede_note_descrittive',
                  #'strumentazione_descrizione', 'strumentazione_valore',
                  'id_infrastruttura_riferimento',
                  'sito_web', 'nome_file_logo']
        labels = {
            'nome_laboratorio': _('Name'),
            'acronimo': _('Acronym'),
            'logo_laboratorio': _('Link Laboratory Logo'),
            #'laboratorio_interdipartimentale': _('Interdepartmental Laboratory'),
            'altre_strutture_riferimento': _('Other Structures'),
            'descr_altre_strutture_riferimento_it': _('Other Structures Description (it)'),
            'descr_altre_strutture_riferimento_en': _('Other Structures Description (en)'),
            #'ambito': _('Scope'),
            #'sede_dimensione': _('Office Dimension'),
            #'sede_note_descrittive': _('Office Description Notes'),
            #'strumentazione_descrizione': _('Instrumentation Description'),
            #'strumentazione_valore': _('Instrumentation Value'),
            'id_infrastruttura_riferimento': _("Reference Infrastrucure"),
            'sito_web': _('Website'),
            'nome_file_logo': _('Logo')
        }
        widgets = {'descr_altre_strutture_riferimento_it': CKEditor5Widget(),
                   'descr_altre_strutture_riferimento_en': CKEditor5Widget(),
                   #'strumentazione_descrizione': CKEditor5Widget(),
                   #'sede_note_descrittive': CKEditor5Widget(),
                  }
        

class LaboratorioDatiBaseInterdipartimentaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LaboratorioDatiBaseInterdipartimentaleForm, self).__init__(*args, **kwargs)
        
        self.fields['laboratorio_interdipartimentale'] = forms.ChoiceField(
            label=_('Interdepartmental Laboratory'),
            choices=(('SI', _('YES')),('NO', 'NO')),
            help_text=_("Extra departments selection is available only after selecting 'YES' and then saving"),
        )
    class Meta:
        model = LaboratorioDatiBase
        fields = ['laboratorio_interdipartimentale']
        labels = {
            'laboratorio_interdipartimentale': _('Interdepartmental Laboratory'),
        }
class LaboratorioDatiBaseInfoSedeStruttureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LaboratorioDatiBaseInfoSedeStruttureForm, self).__init__(*args, **kwargs)
        self.fields['sede_dimensione'].help_text = _("Total square meters")
        self.fields['sede_note_descrittive'].help_text = _("Any addition to the provided data")
        self.fields['strumentazione_descrizione'].help_text = _("Public-use text (detail list below)")
    class Meta:
        model = LaboratorioDatiBase
        fields = ['sede_note_descrittive', 'sede_dimensione', 'strumentazione_descrizione']
        labels = {
            'sede_dimensione': _('Office - Overall Dimensions'),
            'sede_note_descrittive': _('Office - Description Notes'),
            'strumentazione_descrizione': _('Equipment - Description'),
        }
        widgets = {
            'sede_note_descrittive': CKEditor5Widget(),
            'strumentazione_descrizione': CKEditor5Widget(),
        }
        

class LaboratorioDatiBaseStrumentazioneValoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LaboratorioDatiBaseStrumentazioneValoreForm, self).__init__(*args, **kwargs)
        self.fields['strumentazione_valore'].validators = [MinValueValidator(Decimal(0))]
        self.fields['strumentazione_valore'].required = True
    class Meta:
        model = LaboratorioDatiBase
        fields = ['strumentazione_valore']
        labels = {
            'strumentazione_valore': _('Equipment - Overall Value')
        }
        
class LaboratorioDatiBaseAmbitoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LaboratorioDatiBaseAmbitoForm, self).__init__(*args, **kwargs)
        scope_choices = LaboratorioDatiBase.objects.all().values_list("ambito", flat=True).distinct().order_by("ambito")
        scope_choices = tuple(map(lambda ambito: (ambito, ambito), scope_choices))
        self.fields['ambito'] = forms.ChoiceField(
            label=_('Areas'),
            choices = scope_choices
            )
    class Meta:
        model = LaboratorioDatiBase
        fields = ['ambito']
        labels = {
            'ambito': _('Scope')
        }


class LaboratorioDatiBaseScientificDirectorForm(forms.Form):
    responsabile_scientifico = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )

class LaboratorioDatiBaseSafetyManagerForm(forms.Form):
    preposto_sicurezza = forms.CharField(
        label=_("Name and Surname"),
        max_length=200,
    )

class LaboratorioDatiBaseScientificDirectorChoosenPersonForm(forms.Form):
    choosen_scientific_director = forms.CharField(label=_('Scientific Director'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        super(LaboratorioDatiBaseScientificDirectorChoosenPersonForm, self).__init__(*args, **kwargs)
        if required:
            self.fields['choosen_scientific_director'].required = True

class LaboratorioDatiBaseSafetyManagerChoosenPersonForm(forms.Form):
    choosen_safety_manager = forms.CharField(label=_('Safety Manager'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        super(LaboratorioDatiBaseSafetyManagerChoosenPersonForm, self).__init__(*args, **kwargs)
        if required:
            self.fields['choosen_safety_manager'].required = True

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

        self.fields["costo_unitario"] = forms.FloatField(
            label=_('Unit Cost'),
            min_value=0
        )
        self.fields["quantita"] = forms.IntegerField(
            label=_('Quantity'),
            min_value=1
        )

    class Meta:
        model = LaboratorioAttrezzature
        fields = ['tipologia', 'descrizione', 'costo_unitario', 'quantita']
        labels = {
            'tipologia': _('Type'),
            'descrizione': _('Description')
        }

class LaboratorioAttrezzatureFondiForm(forms.Form):
    choices = tuple(LaboratorioFondo.objects.all().order_by('-nome_fondo').values_list('id', 'nome_fondo'))

    id_laboratorio_fondo = forms.MultipleChoiceField(
            label=_('Funds'),
            choices=choices,
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )

class LaboratorioAttrezzatureRischiForm(forms.Form):
    choices = tuple(TipologiaRischio.objects.all().order_by('descr_tipologia').values_list('id', 'descr_tipologia'))

    id_tipologia_rischio = forms.MultipleChoiceField(
            label=_('Risk Types'),
            choices=choices,
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )


class LaboratorioDatiErc1Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        erc0 = RicercaErc0.objects.all().values_list("erc0_cod", "description")
        erc0_choices = ((e0[0], e0[1]) for e0 in erc0)
        
        erc1 = RicercaErc1.objects.all()
        
        erc1_ls = erc1.filter(ricerca_erc0_cod='LS').values_list("id", "descrizione")
        erc1_ls_choices = ((e1[0], e1[1]) for e1 in erc1_ls)
        
        erc1_pe = erc1.filter(ricerca_erc0_cod='PE').values_list("id", "descrizione")
        erc1_pe_choices = ((e1[0], e1[1]) for e1 in erc1_pe)
        
        erc1_sh = erc1.filter(ricerca_erc0_cod='SH').values_list("id", "descrizione")
        erc1_sh_choices = ((e1[0], e1[1]) for e1 in erc1_sh)
        
        self.fields['erc0_selector'] = forms.ChoiceField(
            label=_('ERC Classification'),
            choices = erc0_choices
        )
        
        self.fields['id_ricerche_erc1_ls'] = forms.MultipleChoiceField(
            label=_('ERC Classification - Life Science'),
            choices=erc1_ls_choices,
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
        
        self.fields['id_ricerche_erc1_pe'] = forms.MultipleChoiceField(
            label=_('ERC Classification - Physical Sciences and Engineering'),
            choices=erc1_pe_choices,
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
        
        self.fields['id_ricerche_erc1_sh'] = forms.MultipleChoiceField(
            label=_('ERC Classification - Social Sciences and Humanities'),
            choices=erc1_sh_choices,
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

class LaboratorioPersonaleForm(forms.Form):
    laboratory_staff = forms.CharField(
        label=_("Name and Surname"),
        max_length=200)

class LaboratorioPersonaleTecnicoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ruolo'] = forms.CharField(
            required=True,
            label=_("Role"))

        self.fields['percentuale_impegno'] = forms.FloatField(
            required=True,
            label=_("Commitment %"),
            min_value=0,
            max_value=100
        )

class LaboratorioAttivitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        activity_types_already_specified=kwargs.pop("activity_types_already_specified", ())
        super().__init__(*args, **kwargs)
        activity_types = LaboratorioTipologiaAttivita.objects.exclude(id__in=activity_types_already_specified).values_list("id", "descrizione")

        self.fields['tipologia_attivita'] = forms.ChoiceField(
            label=_('Activity Type'),
            choices=activity_types,
            required=True)

        self.order_fields(field_order=('tipologia_attivita', 'descr_finalita_it', 'descr_finalita_en'))
    class Meta:
        model = LaboratorioDatiBase.tipologia_attivita.through
        fields = ['descr_finalita_it',
                  'descr_finalita_en']
        labels = {
            'descr_finalita_it': _('Purpouse (it)'),
            'descr_finalita_en': _('Purpouse (en)'),
        }

        widgets = {'descr_finalita_it': CKEditor5Widget(),
                   'descr_finalita_en': CKEditor5Widget()}

class LaboratorioServiziErogatiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anno'] = forms.IntegerField(
            max_value=dt.today().year,
            min_value=1901,
            required=True,
            label=_('Year')
        )
        self.fields['importo_euro'] = forms.FloatField(min_value=0, required=True, label=_('Monetary Amount (Euros)'))
        self.fields['durata_mesi'] = forms.IntegerField(min_value=0, required=True, label=_('Duration (Months)'))

    class Meta:
        model = LaboratorioServiziErogati
        exclude = ('id_laboratorio_dati', 'matricola_responsabile', 'responsabile_origine',)
        labels = {
            'descrizione': _('Description'),
            'committenti': _('Client'),
            'durata_mesi': _('Duration (Months)'),
            'importo_euro': _('Monetary Amount (Euros)'),
            'strumentazione': _('Equipment'),
        }

class LaboratorioServiziErogatiResponsabileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['laboratory_manager'] = forms.CharField(
            required=True,
            label=_("Name and Surname"))

class LaboratorioServiziOffertiForm(forms.ModelForm):
    class Meta:
        model = LaboratorioServiziOfferti
        fields = ['nome_servizio', 'descrizione_servizio']
        label = {
            "nome_servizio" : _("Name"),
            "descrizione_servizio": _("Description"),
        }


#ModelForm
class LaboratorioTipologiaRischioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        available_risk_types = TipologiaRischio.objects.all().order_by("descr_tipologia").values("id", "descr_tipologia")

        choices = []
        for risk_type in available_risk_types:
            choices.append((risk_type["id"], risk_type["descr_tipologia"]))


        self.fields['tipologie_rischio'] = forms.MultipleChoiceField(
            label=_('Risk Types'),
            choices=tuple(choices),
            widget=forms.CheckboxSelectMultiple(),
            required=False)

    class Meta:
        model = LaboratorioDatiBase.tipologia_rischio.through
        exclude = ["id_tipologia_rischio", "id_laboratorio_dati", "tipologia_rischio_origine"]


