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
            
        self.fields["visibile"] = forms.BooleanField(
            label=_("Visible"),
            required=False,
        )
        self.fields["ordine"] = forms.IntegerField(
            required=True,
            min_value=0,
            label=_("Order"),
        )
    
    class Meta:
        model = SitoWebCdsTopicArticoliReg
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic', 'id_sito_web_cds_oggetti_portale', 'id_didattica_cds_articoli_regolamento']
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
            "testo_it": _("Text (it)"),
            "testo_en": _("Text (en)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "id_didattica_cds_articoli_regolamento": _("Regulation Article"),
            "id_sito_web_cds_oggetti_portale": _("Portal object"),
        }
   
class SitoWebCdsArticoliRegolamentoItemForm(SitoWebCdsTopicArticoliRegForm):
    def __init__(self, *args, **kwargs):
        cds_id = kwargs.pop("cds_id", None)
        super(SitoWebCdsArticoliRegolamentoItemForm, self).__init__(*args, **kwargs)
    class Meta(SitoWebCdsTopicArticoliRegForm.Meta):
        exclude = ["titolo_it", "titolo_en", "testo_it", "testo_en"] + SitoWebCdsTopicArticoliRegForm.Meta.exclude

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
        
        self.order_fields(['visibile', 'id_sito_web_cds_oggetti_portale', 'ordine', 'titolo_it', 'titolo_en', 'testo_it','testo_en'])

        
     
class SitoWebCdsOggettiPortaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsOggettiPortaleForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["visibile"] = bool(self.initial.get("visibile", None))
        self.fields["titolo_it"].help_text = _("Used to identify the object inside the dropdown menu when adding it to a topic")
        self.fields["titolo_en"].help_text = _("Used to identify the object inside the dropdown menu when adding it to a topic")
        self.fields["testo_it"].help_text = _("Used only for webpaths, when provided, the object will be shown as a collapsible element containing this text alongside the webpath")
        self.fields["testo_en"].help_text = _("Used only for webpaths, when provided, the object will be shown as a collapsible element containing this text alongside the webpath")
        self.fields["id_classe_oggetto_portale"] = forms.ChoiceField(
            required=True,
            choices=(("WebPath", _("WebPath")),("Publication", _("Publication"))),
            label=_("Object class"),
            help_text=_("Publication / WebPath (Active page)")
        )
        self.fields["id_oggetto_portale"] = forms.IntegerField(
            required=True,
            min_value=0,
            label=_("Object id"),
            help_text=_("Use Publication/WebPath ID from the editorial board")
        )
        self.fields["visibile"] = forms.BooleanField(
            label=_("Visible"),
            required=False,
        )    
        
        self.order_fields(['visibile', 'id_oggetto_portale', 'id_classe_oggetto_portale', 'titolo_it', 'titolo_en', 'testo_it','testo_en'])


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
            
        self.fields["visibile"] = forms.BooleanField(
            label=_("Visible"),
            required=False,
        )
        self.fields["ordine"]  = forms.IntegerField(
            required=True,
            min_value=0,
            label=_("Order"),
        )
        self.fields["id_sito_web_cds_tipo_dato"] = forms.ChoiceField(
            required=True,
            choices=tuple(SitoWebCdsTipoDato.objects.all().values_list("id", "descr_breve")),
            label=_("Type"),
            help_text=_("Used to determine the icon to show on the left of the element")
        )
        self.fields["link"] = forms.URLField(
            label=_("Link"),
            required=False,
        )
        self.fields["titolo_it"].help_text = _("Shown above the element if provided")
        self.fields["titolo_en"].help_text = _("Shown above the element if provided")
        self.fields["testo_it"].help_text = _("If provided it is used as the link text")
        self.fields["testo_en"].help_text = _("If provided it is used as the link text")

        self.order_fields(['visibile', 'ordine', "titolo_it", 'titolo_en', 'testo_it','testo_en', 'link', 'id_sito_web_cds_tipo_dato',])

    
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