from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *
from django.conf import settings

from ricerca_app.models import *

UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')

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
        min_value=0,
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
    
    id_classe_oggetto_portale = forms.ChoiceField(
        required=True,
        choices=(("WebPath", _("WebPath")),("Publication", _("Publication"))),
        label=_("Object class"),
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
        exclude = ['dt_mod', 'id_user_mod','id_sito_web_cds_topic', 'cds', 'ordine', 'aa_regdid_id']
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
        min_value=0,
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