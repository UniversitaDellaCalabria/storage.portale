from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *
from django.conf import settings

import requests

from ricerca_app.models import *


UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')


class SitoWebCdsDatiBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SitoWebCdsDatiBaseForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["sito_web_cds_status"] = bool(self.initial.get("sito_web_cds_status", None))
                
    sito_web_cds_status = forms.BooleanField(
        label=_("Status"),
        required=False,
    )
    aa = forms.IntegerField(
        required=True,
        min_value=1901,
        max_value=now().year,
        label=_("Academic year"),
    )

    class Meta:
        model = SitoWebCdsDatiBase
        exclude = ['dt_mod', 'id_user_mod', 'id_didattica_regolamento', 'cds_cod', 'cds']


        labels = {
            'aa': _('Academic year'),
            'cds': _('Cds name'),
            'cds_cod': _('Cds code'),
            'nome_corso_it': _('Course name (it)'),
            'nome_corso_en': _('Course name (en)'),
            'classe_laurea_it': _('Course class (it)'),
            'classe_laurea_en': _('Course class (en)'),
            'classe_laurea_interclasse_it': _('Course interclass (it)'),
            'classe_laurea_interclasse_en': _('Course interclass (en)'),
            'lingua_it': _('Language (it)'),
            'lingua_en': _('Language (en)'),
            'durata': _('Duration'),
            'num_posti': _('Seats Number'),
            'link_video_cds_it': _('Link video (it)'),
            'link_video_cds_en': _('Link video (en)'),
            'descrizione_corso_it': _('Description (it)'),
            'descrizione_corso_en': _('Description (en)'),
            'tasse_contributi_esoneri_it': _('Taxes (it)'),
            'tasse_contributi_esoneri_en': _('Taxes (en)'),
            'borse_studio_it': _('Scholarships (it)'),
            'borse_studio_en': _('Scholarships (en)'),
            'agevolazioni_it': _('Concessions (it)'),
            'agevolazioni_en': _('Concessions (en)'),
            'corso_in_pillole_it': _('Short description (it)'),
            'corso_in_pillole_en': _('Short description (en)'),
            'cosa_si_studia_it': _('Study plan (it)'),
            'cosa_si_studia_en': _('Study plan (en)'),
            'come_iscriversi_it': _('Enrollement mode (it)'),
            'come_iscriversi_en': _('Enrollement mode (en)'),
            'sito_web_it': _('Website (it)'),
            'sito_web_en': _('Website (en)'),
            'sito_web_cds_status': _('Status'),
            'accesso_corso_it': _('Admission (it)'),
            'accesso_corso_en': _('Admission (en)'),
            'obiettivi_corso_it': _('Goals (it)'),
            'obiettivi_corso_en': _('Goals (en)'),
            'sbocchi_professionali_it': _('Job opportunities (it)'),
            'sbocchi_professionali_en': _('Job opportunituies (en)')
        }
        
        widgets = {'descrizione_corso_it': CKEditorWidget(),
                   'descrizione_corso_en': CKEditorWidget(),
                   'accesso_corso_it': CKEditorWidget(),
                   'accesso_corso_en': CKEditorWidget(),
                   'obiettivi_corso_it': CKEditorWidget(),
                   'obiettivi_corso_en': CKEditorWidget(),
                   'sbocchi_professionali_it': CKEditorWidget(),
                   'sbocchi_professionali_en': CKEditorWidget(),
                   'tasse_contributi_esoneri_it': CKEditorWidget(),
                   'tasse_contributi_esoneri_en': CKEditorWidget(),
                   'borse_studio_it': CKEditorWidget(),
                   'borse_studio_en': CKEditorWidget(),
                   'agevolazioni_it': CKEditorWidget(),
                   'agevolazioni_en': CKEditorWidget(),
                   'corso_in_pillole_it': CKEditorWidget(),
                   'corso_in_pillole_en': CKEditorWidget(),
                   'cosa_si_studia_it': CKEditorWidget(),
                   'cosa_si_studia_en': CKEditorWidget(),
                   'come_iscriversi_it': CKEditorWidget(),
                   'come_iscriversi_en': CKEditorWidget(),
                   }

    class Media:
        js = ('js/textarea-autosize.js',)

class SitoWebCdsExStudentiForm(forms.ModelForm):
    
    class Meta:
        model = SitoWebCdsExStudenti
        exclude = ['id_sito_web_cds_dati_base', 'id_user_mod', 'dt_mod',]
        labels = {
            'ordine': _("Order"),
            'foto': _("Picture"),
            'profilo_it': _("Profile (it)"),
            'profilo_en': _("Profile (en)"),
            'link_it': _("Link (it)"),
            'link_en': _("Link (en)"),
        }


class SitoWebCdsForm(forms.ModelForm):
    ordine = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=100,
        label=_("Order"),
    )
    class Meta:
        exclude = ['id_sito_web_cds_dati_base', 'id_user_mod', 'dt_mod',]

class SitoWebCdsSliderForm(SitoWebCdsForm):
       
    class Meta(SitoWebCdsForm.Meta):
        model = SitoWebCdsSlider
        labels = {
            'slider_it': _("Scrollable text (it)"),
            'slider_en': _("Scrollable text (en)"),
            'ordine': _("Order"),
        }
        
class SitoWebCdsLinkForm(SitoWebCdsForm):
    class Meta(SitoWebCdsForm.Meta):
        model = SitoWebCdsLink
        labels = {
            'ordine': _("Order"),
            'descrizione_link_it': _("Link description (it)"),
            'descrizione_link_en': _("Link description (en)"),
            'link_it': _("Link (it)"),
            'link_en': _("Link (en)"),
        }

class SitoWebCdsTopicArticoliRegForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsTopicArticoliRegForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["visibile"] = bool(self.initial.get("visibile", None))
            
    visibile = forms.BooleanField(
        label=_("Visible"),
        required=False,
    )
    ordine = forms.IntegerField(
        required=True,
        max_value=100,
        min_value=1,
        label=_("Order"),
    )
    
    class Meta:
        model = SitoWebCdsTopicArticoliReg
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic', 'id_sito_web_cds_oggetti_portale', 'id_sito_web_cds_articoli_regolamento']
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
            "testo_it": _("Text (it)"),
            "testo_en": _("Text (en)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "id_sito_web_cds_articoli_regolamento": _("Regulament Article"),
            "id_sito_web_cds_oggetti_portale": _("Portal object"),
        }
   
class SitoWebCdsArticoliRegolamentoItemForm(SitoWebCdsTopicArticoliRegForm):
    def __init__(self, *args, **kwargs):
        cds_id = kwargs.pop("cds_id", None)
        
        super(SitoWebCdsArticoliRegolamentoItemForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            choices = SitoWebCdsArticoliRegolamento.objects.filter(cds_id=cds_id).values_list("id", "aa_regdid_id", "titolo_articolo_it").order_by("aa_regdid_id", "titolo_articolo_it")
            choices = map(lambda reg: (reg[0], f"{reg[1]} - {reg[2]}"), choices)
            choices = tuple(choices)
        else:
            choices=((self.instance.id_sito_web_cds_articoli_regolamento.id, f"{self.instance.id_sito_web_cds_articoli_regolamento.aa_regdid_id} - {self.instance.id_sito_web_cds_articoli_regolamento.titolo_articolo_it}"),)
        
        self.fields["id_sito_web_cds_articoli_regolamento"] = forms.ChoiceField(
            choices=choices,
            label=_("Regulament article"),
        )

class SitoWebCdsOggettiItemForm(SitoWebCdsTopicArticoliRegForm):
    def __init__(self, *args, **kwargs):
        cds_id = kwargs.pop("cds_id", None)
        
        super(SitoWebCdsOggettiItemForm, self).__init__(*args, **kwargs)
        
        choices = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_id).values_list("id", "aa_regdid_id", "titolo_it", "testo_it").order_by("aa_regdid_id", "titolo_it", "testo_it")
        choices = map(lambda reg: (reg[0], f"{reg[1]} - {reg[2] if reg[2] else ''} - {reg[3] if reg[3] else ''}"), choices)
        choices = tuple(choices)
        
        self.fields["id_sito_web_cds_oggetti_portale"] = forms.ChoiceField(
            choices=choices,
            label=_("Portal object"),
        )
        
     
class SitoWebCdsOggettiPortaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsOggettiPortaleForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["visibile"] = bool(self.initial.get("visibile", None))
            
    def clean(self):
        super(SitoWebCdsOggettiPortaleForm, self).clean()
        titolo_it = self.cleaned_data.get("titolo_it")
        testo_it = self.cleaned_data.get("testo_it")
        if not titolo_it and not testo_it:
            raise forms.ValidationError(_("At least one must be provided between:") +
                                        f" {self.fields['titolo_it'].label} or {self.fields['testo_it'].label}")
        return self.cleaned_data
    
    id_classe_oggetto_portale = forms.ChoiceField(
        required=True,
        choices=(("WebPath", _("WebPath")),("Publication", _("Publication"))),
        label=_("Object class"),
    )
    aa_regdid_id = forms.IntegerField(
        required=True,
        min_value=1901,
        max_value= now().year,
        label=_("Academic year"),
    )
    id_oggetto_portale = forms.IntegerField(
        required=True,
        min_value=0,
        label=_("Object id"),
    )
    visibile = forms.BooleanField(
        label=_("Visible"),
        required=False,
    )
    class Meta:
        model = SitoWebCdsOggettiPortale
        exclude = ['dt_mod', 'id_user_mod','id_sito_web_cds_topic', 'cds', 'ordine',]
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
            "testo_it": _("Text (it)"),
            "testo_en": _("Text (en)"),
            "id_oggetto_portale": _("Object Id"),
            "aa_regdid_id": _("Didactic regulation academic year"),
            "id_classe_oggetto_portale": _("Object class"),
            "visibile": _("Visible"),
        }
    class Media:
        js = ('js/textarea-autosize.js',)
        
        
class SitoWebCdsTopicArticoliRegAltriDatiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsTopicArticoliRegAltriDatiForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["visibile"] = bool(self.initial.get("visibile", None))
            
    
    visibile = forms.BooleanField(
        label=_("Visible"),
        required=False,
    )
    ordine = forms.IntegerField(
        required=True,
        max_value=100,
        min_value=1,
        label=_("Order"),
    )
    id_sito_web_cds_tipo_dato = forms.ChoiceField(
        required=True,
        choices=tuple(SitoWebCdsTipoDato.objects.all().values_list("id", "descr_breve")),
        label=_("Type"),
    )
    link = forms.URLField(
        label=_("Link"),
        required=False,
    )
    
    class Meta:
        model = SitoWebCdsTopicArticoliRegAltriDati
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic_articoli_reg', 'id_sito_web_cds_tipo_dato']
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "testo_it": _("Text (it)"),
            "testo_en": _("Text (en)"),
            "id_sito_web_cds_tipo_dato": _("Type"),
            "link": _("Link"),
        }