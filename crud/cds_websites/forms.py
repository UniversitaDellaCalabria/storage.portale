from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

import requests

from ricerca_app.models import *


UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')


class SitoWebCdsDatiBaseForm(forms.ModelForm):
    # choosen_department = forms.CharField(label=_('Department'),
    #                                      widget=forms.HiddenInput(),
    #                                      required=False)

    class Meta:
        model = SitoWebCdsDatiBase
        fields = '__all__'
        exclude = ['dt_mod', 'id_user_mod']


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
                   'corse_in_pillole_it': CKEditorWidget(),
                   'corse_in_pillole_en': CKEditorWidget(),
                   'cosa_si_studia_it': CKEditorWidget(),
                   'cosa_si_studia_en': CKEditorWidget(),
                   'come_iscriversi_it': CKEditorWidget(),
                   'come_iscriversi_en': CKEditorWidget(),
                   }

    # def __init__(self, *args, **kwargs):
    #     super(SitoWebCdsDatiBaseForm, self).__init__(*args, **kwargs)
    #     _logo_field = self.instance.nome_file_logo
    #     self.fields['nome_file_logo'].widget = RicercaCRUDClearableWidget(
    #         {'upload_to': _logo_field.field.upload_to(self.instance, _logo_field.name)}
    #     )

    class Media:
        js = ('js/textarea-autosize.js',)


class SitoWebCdsTopicArticoliItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsTopicArticoliItemForm, self).__init__(*args, **kwargs)
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
            "titolo_it": _("Title (IT)"),
            "titolo_en": _("Title (EN)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "id_sito_web_cds_articoli_regolamento": _("Regulament Article"),
        }
   
class SitoWebCdsArticoliRegolamentoForm(SitoWebCdsTopicArticoliItemForm):
    def __init__(self, *args, **kwargs):
        cds_id = kwargs.pop("cds_id", None)
        
        super(SitoWebCdsArticoliRegolamentoForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            already_chosen = SitoWebCdsTopicArticoliReg.objects.filter(id_sito_web_cds_articoli_regolamento__cds_id=cds_id).values_list("id_sito_web_cds_articoli_regolamento", flat=True)
            choices=tuple(SitoWebCdsArticoliRegolamento.objects.filter(cds_id=cds_id).exclude(id__in=already_chosen).values_list("id", "titolo_articolo_it"))
        else:
            choices=((self.instance.id_sito_web_cds_articoli_regolamento.id, self.instance.id_sito_web_cds_articoli_regolamento.titolo_articolo_it),)
        
        self.fields["id_sito_web_cds_articoli_regolamento"] = forms.ChoiceField(
            choices=choices,
            label=_("Articolo Regolamento"),
        )
        
     
class SitoWebCdsOggettiPortaleForm(forms.ModelForm):
       
    
    id_classe_oggetto_portale = forms.ChoiceField(
        required=True,
        choices=(("WebPath", _("WebPath")),("Publication", _("Publication"))),
        label=_("Object Class"),
    )
    aa_regdid_id = forms.IntegerField(
        required=True,
        min_value=1901,
        max_value=timezone.now().year,
        label=_("Didactic Regulation Year"),
    )
    id_oggetto_portale = forms.IntegerField(
        required=True,
        min_value=0,
    )
    class Meta:
        model = SitoWebCdsOggettiPortale
        exclude = ['dt_mod', 'id_user_mod','id_sito_web_cds_topic', 'cds', 'ordine', 'visibile']
        
        
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
    )
    
    class Meta:
        model = SitoWebCdsTopicArticoliRegAltriDati
        exclude = ['dt_mod', 'id_user_mod', 'id_sito_web_cds_topic_articoli_reg', 'id_sito_web_cds_tipo_dato']
        labels = {
            "titolo_it": _("Title (IT)"),
            "titolo_en": _("Title (EN)"),
            "ordine": _("Order"),
            "visibile": _("Visible"),
            "testo_it": _("Text (IT)"),
            "testo_en": _("Text (EN)"),
            "id_sito_web_cds_tipo_dato": _("Type"),
            "link": _("Link"),
        }