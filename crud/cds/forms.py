from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.validators import validate_pdf_file_extension, validate_file_size
from ricerca_app.models import (
    DidatticaCds, DidatticaCdsAltriDati,
    DidatticaCdsAltriDatiUfficio, DidatticaCdsGruppi,
    DidatticaCdsGruppiComponenti, DidatticaRegolamentoAltriDati)

from .. utils.forms import ChoosenPersonForm
from .. utils.settings import CMS_STORAGE_ROOT_API


CMS_STORAGE_ROOT_API = getattr(
    settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


class DidatticaCdsAltriDatiCoordinatorForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=True)


class DidatticaCdsAltriDatiUfficioForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDatiUfficio
        fields = ['ordine', 'nome_ufficio',
                  'telefono', 'email', 'edificio', 'piano', 'orari',
                  'sportello_online', 'nome_origine_riferimento']
        labels = {
            "nome_origine_riferimento": _("Responsible"),
        }
        widgets = {'orari': CKEditor5Widget()}


class DidatticaCdsAltriDatiForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = [# 'num_posti', 'modalita_iscrizione',
                  'nome_origine_coordinatore',
                  'nome_origine_vice_coordinatore',
                  #'num_posti'
                  ]
                  # 'manifesto_studi', 'regolamento_didattico']
        labels = {
            "nome_origine_coordinatore": _("Coordinator"),
            "nome_origine_vice_coordinatore": _("Deputy coordinator"),
            # "num_posti": _("Number of seats"),
            # "modalita_iscrizione": _("Registration procedure"),
            "visibile": _("Visibile"),
            # "manifesto_studi": _("Study manifesto"),
            # "regolamento_didattico": _("Didactic regulation"),
        }
        # widgets = {'modalita_iscrizione': CKEditor5Widget()}


class DidatticaCdsOrdinamentoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['ordinamento_didattico']
        labels = {
            "ordinamento_didattico": _("Teaching system"),
        }


class DidatticaCdsManifestoRegolamentoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsAltriDati
        fields = ['manifesto_studi', 'regolamento_didattico']
        labels = {
            "manifesto_studi": _("Study manifesto"),
            "regolamento_didattico": _("Didactic regulation"),
        }


class DidatticaCdsGruppoForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsGruppi
        fields = ['visibile', 'descr_breve_it', 'descr_breve_en', 'descr_lunga_it',
                  'descr_lunga_en', 'ordine']
        # labels = {
            # "manifesto_studi": _("Study manifesto"),
            # "regolamento_didattico": _("Didactic regulation"),
        # }
        widgets = {'descr_breve_it': forms.Textarea(attrs={'rows': 2}),
                   'descr_breve_en': forms.Textarea(attrs={'rows': 2}),
                   'descr_lunga_it': forms.Textarea(attrs={'rows': 2}),
                   'descr_lunga_en': forms.Textarea(attrs={'rows': 2})}



    class Media:
        js = ('js/textarea-autosize.js',)


class DidatticaCdsGruppoComponenteForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsGruppiComponenti
        fields = ['visibile', 'nome', 'cognome', 'funzione_it',
                  'funzione_en', 'ordine']


class ChoosenPersonForm(ChoosenPersonForm, forms.ModelForm):

    class Meta:
        model = DidatticaCdsGruppiComponenti
        fields = ['visibile', 'funzione_it', 'funzione_en', 'ordine']


class DidatticaRegolamentoAltriDatiForm(forms.ModelForm):
    def __init__(self, clob_type, clob_label, tipo_testo_regdid_cod, form_name, *args, **kwargs):
        
        clob_label_it = _(clob_label) + " (it)"
        clob_label_en = _(clob_label) + " (en)"
                
        super(DidatticaRegolamentoAltriDatiForm, self).__init__(*args, **kwargs)
        
        if clob_type == "PDF": # pdf file
            self.fields['clob_txt_ita'] = forms.FileField(validators=[validate_pdf_file_extension, validate_file_size])
            self.fields['clob_txt_eng'] = forms.FileField(validators=[validate_pdf_file_extension, validate_file_size])
            self.fields['clob_txt_eng'].widget = forms.widgets.ClearableFileInput()
        elif clob_type == "URL": # url to some resource
            self.fields['clob_txt_ita'] = forms.URLField()
            self.fields['clob_txt_eng'] = forms.URLField()
        elif clob_type == "HTML": # markdown text
            self.fields['clob_txt_ita'] = forms.CharField(widget=CKEditor5Widget())
            self.fields['clob_txt_eng'] = forms.CharField(widget=CKEditor5Widget())
        else: # default is handled as plain text
            self.fields['clob_txt_ita'] = forms.CharField(widget=forms.widgets.Textarea())
            self.fields['clob_txt_eng'] = forms.CharField(widget=forms.widgets.Textarea())
        # common
        self.fields['clob_txt_ita'].required = False
        self.fields['clob_txt_eng'].required = False
        self.fields['clob_txt_ita'].label = clob_label_it
        self.fields['clob_txt_eng'].label = clob_label_en
        self.fields['form_name'] = forms.CharField(
            initial=form_name,
            widget=forms.widgets.HiddenInput()
        )
        # tipo_testo_regdid_cod
        self.fields['tipo_testo_regdid_cod'] = forms.CharField(
            initial=tipo_testo_regdid_cod,
            widget=forms.widgets.HiddenInput()
        )
        
    class Meta:
        model = DidatticaRegolamentoAltriDati
        fields = ["clob_txt_ita", "clob_txt_eng"]