from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *
from django.conf import settings

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import *

from . widgets import OggettiPortaleWidget, ExternalOggettiPortaleWidget

UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')

class SitoWebCdsTopicArticoliRegForm(forms.ModelForm):
    
    def __init__(self, *args, user=None, **kwargs):
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
        
        self.instance_provided = 'instance' in kwargs and kwargs['instance'] is not None
        if self.instance_provided:
            if not user or (not user.is_superuser and self.instance.id_user_mod_id in getattr(settings, "ETL_USER_IDS", [])):
                for field in self.fields.values():
                    field.widget.attrs['disabled'] = 'disabled'
    
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
        widgets = {
            'testo_it': CKEditor5Widget(config_name="regdid"),
            'testo_en': CKEditor5Widget(config_name="regdid")
        }
   
class SitoWebCdsArticoliRegolamentoItemForm(SitoWebCdsTopicArticoliRegForm):
    def __init__(self, *args, user=None, **kwargs):
        super(SitoWebCdsArticoliRegolamentoItemForm, self).__init__(*args, user=user, **kwargs)
        if not user or not user.is_superuser:
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'disabled'

class SitoWebCdsOggettiItemForm(SitoWebCdsTopicArticoliRegForm):
    def __init__(self, *args, user=None, **kwargs):
        cds_id = kwargs.pop("cds_id", None)
        
        super(SitoWebCdsOggettiItemForm, self).__init__(*args, user=user, **kwargs)
        
        choices = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_id).order_by("aa_regdid_id", "titolo_it")
        swcd_base = SitoWebCdsDatiBase.objects.get(cds_id=cds_id)
        
        self.fields["id_sito_web_cds_oggetti_portale"].queryset = choices
        self.fields["id_sito_web_cds_oggetti_portale"].label = _("Portal object")
        self.fields["id_sito_web_cds_oggetti_portale"].required = True
        self.fields["testo_it"].help_text = _("Used only for webpaths, when provided, the object will be shown as a collapsible element containing this text alongside the webpath")
        self.fields["testo_en"].help_text = _("Used only for webpaths, when provided, the object will be shown as a collapsible element containing this text alongside the webpath")
        self.fields["id_sito_web_cds_oggetti_portale"].widget = OggettiPortaleWidget(swcd_base.id)
        self.fields["id_sito_web_cds_oggetti_portale"].label= _("Portal object")
        
        self.order_fields(['visibile', 'id_sito_web_cds_oggetti_portale', 'ordine', 'titolo_it', 'titolo_en', 'testo_it','testo_en'])
        
    class Meta(SitoWebCdsTopicArticoliRegForm.Meta):
        exclude = [field for field in SitoWebCdsTopicArticoliRegForm.Meta.exclude if not field == 'id_sito_web_cds_oggetti_portale']

        
     
class SitoWebCdsOggettiPortaleForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(SitoWebCdsOggettiPortaleForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["visibile"] = bool(self.initial.get("visibile", None))
        self.fields["titolo_it"].help_text = _("Used to identify the object inside the dropdown menu when adding it to a topic")
        self.fields["titolo_en"].help_text = _("Used to identify the object inside the dropdown menu when adding it to a topic")
        self.fields["id_classe_oggetto_portale"] = forms.ChoiceField(
            required=True,
            choices=(("WebPath", _("WebPath")),("Publication", _("Publication"))),
            label=_("Object class"),
            help_text=_("Publication / WebPath (Active page)")
        )
        self.fields["id_oggetto_portale"].widget=ExternalOggettiPortaleWidget()
        self.fields["id_oggetto_portale"].label=_("Object")
        
        self.fields["visibile"] = forms.BooleanField(
            label=_("Visible"),
            required=False,
        )    
        
        self.order_fields(['visibile', 'id_classe_oggetto_portale', 'id_oggetto_portale', 'titolo_it', 'titolo_en'])
        
        self.instance_provided = 'instance' in kwargs and kwargs['instance'] is not None
        if self.instance_provided:
            if not user or (not user.is_superuser and self.instance.id_user_mod_id in getattr(settings, "ETL_USER_IDS", [])):
                for field in self.fields.values():
                    field.widget.attrs['disabled'] = 'disabled'
                    

    class Meta:
        model = SitoWebCdsOggettiPortale
        exclude = ['dt_mod', 'id_user_mod','id_sito_web_cds_topic', 'cds', 'ordine', 'aa_regdid_id', 'testo_it', 'testo_en']
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
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
        self.fields["link"] = forms.URLField(
            label=_("Link"),
            required=False,
        )
        self.fields["titolo_it"].help_text = _("Shown above the element if provided")
        self.fields["titolo_en"].help_text = _("Shown above the element if provided")
        self.fields["testo_it"].help_text = _("If provided it is used as the link text")
        self.fields["testo_en"].help_text = _("If provided it is used as the link text")
        self.fields["id_sito_web_cds_tipo_dato"].help_text=_("Used to determine the icon to show on the left of the element")

        self.order_fields(['visibile', 'ordine', "titolo_it", 'titolo_en', 'testo_it','testo_en', 'link', 'id_sito_web_cds_tipo_dato',])

    
    class Meta:
        model = SitoWebCdsTopicArticoliRegAltriDati
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic_articoli_reg']
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

class SitoWebCdsSubArticoliRegolamentoForm(forms.ModelForm):
    
    def __init__(self, *args, user=None, **kwargs):
        super(SitoWebCdsSubArticoliRegolamentoForm, self).__init__(*args, **kwargs)
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
        
        self.instance_provided = 'instance' in kwargs and kwargs['instance'] is not None
        if self.instance_provided:
            if not user or not user.is_superuser:
                for field in self.fields.values():
                    field.widget.attrs['disabled'] = 'disabled'
        
    class Meta:
        model = SitoWebCdsSubArticoliRegolamento
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic_articoli_reg']
        labels = {
            "titolo_it": _("Title (it)"),
            "titolo_en": _("Title (en)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "testo_it": _("Text (it)"),
            "testo_en": _("Text (en)"),
        }
            