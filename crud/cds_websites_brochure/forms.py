from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *
from django.conf import settings

from ricerca_app.models import *
from .validators import CKEditorWidgetMinLenghtValidator, CKEditorWidgetMaxLenghtValidator
from .widgets import CKEditorWidgetWordCount

UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')


class SitoWebCdsDatiBaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsDatiBaseForm, self).__init__(*args, **kwargs)
        
        self.fields['languages'] = forms.MultipleChoiceField(
            label=_("Languages"),
            choices = (('italiano', _('ITALIAN')), ('inglese', _('ENGLISH')), ('italiano, inglese', _('ITALIAN, ENGLISH')))
        )
        
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
            'accesso_corso_it': _('Admission (it)'),
            'accesso_corso_en': _('Admission (en)'),
            'obiettivi_corso_it': _('Goals (it)'),
            'obiettivi_corso_en': _('Goals (en)'),
            'sbocchi_professionali_it': _('Job opportunities (it)'),
            'sbocchi_professionali_en': _('Job opportunituies (en)')
        }
        
        ckeditor_fields = [
                   {'descrizione_corso_it': {'min': 0, 'max': 700, 'enforce': True}},
                   {'descrizione_corso_en': {'min': 0, 'max': 700, 'enforce': False}},
                   {'accesso_corso_it': {'min': 200, 'max': 500, 'enforce': True}},
                   {'accesso_corso_en': {'min': 200, 'max': 500, 'enforce': False}},
                   {'obiettivi_corso_it': {'min': 200, 'max': 500, 'enforce': True}},
                   {'obiettivi_corso_en': {'min': 200, 'max': 500, 'enforce': False}},
                   {'sbocchi_professionali_it': {'min': 300, 'max': 500, 'enforce': True}},
                   {'sbocchi_professionali_en': {'min': 300, 'max': 500, 'enforce': False}},
                   {'tasse_contributi_esoneri_it': {'min': 0, 'max': 400, 'enforce': True}},
                   {'tasse_contributi_esoneri_en': {'min': 0, 'max': 400, 'enforce': False}},
                   {'borse_studio_it': {'min': 200, 'max': 400, 'enforce': True}},
                   {'borse_studio_en': {'min': 200, 'max': 400, 'enforce': False}},
                   {'agevolazioni_it': {'min': 200, 'max': 400, 'enforce': True}},
                   {'agevolazioni_en': {'min': 200, 'max': 400, 'enforce': False}},
                   {'corso_in_pillole_it': {'min': 300, 'max': 600, 'enforce': True}},
                   {'corso_in_pillole_en': {'min': 300, 'max': 600, 'enforce': False}},
                   {'cosa_si_studia_it': {'min': 300, 'max': 600, 'enforce': True}},
                   {'cosa_si_studia_en': {'min': 300, 'max': 600, 'enforce': False}},
                   {'come_iscriversi_it': {'min': 300, 'max': 600, 'enforce': True}},
                   {'come_iscriversi_en': {'min': 300, 'max': 600, 'enforce': False}},
                ]
        
        for field in ckeditor_fields:
            for (name, min_max) in field.items():
                self.fields[name] = forms.CharField(
                    label=labels[name],
                    required=False,
                    widget=CKEditorWidgetWordCount(min_max['min'], min_max['max'], min_max['enforce']),
                    validators=[CKEditorWidgetMinLenghtValidator(min_max['min']), CKEditorWidgetMaxLenghtValidator(min_max['max'])] if min_max['enforce'] else []
                )

        self.order_fields([ 'aa',
                            'nome_corso_it',
                            'nome_corso_en',
                            'durata',
                            'num_posti',
                            'languages',
                            'classe_laurea_it',
                            'classe_laurea_en',
                            'classe_laurea_interclasse_it',
                            'classe_laurea_interclasse_en',
                            'link_video_cds_it',
                            'link_video_cds_en',
                            'descrizione_corso_it',
                            'descrizione_corso_en',
                            'tasse_contributi_esoneri_it',
                            'tasse_contributi_esoneri_en',
                            'borse_studio_it',
                            'borse_studio_en',
                            'agevolazioni_it',
                            'agevolazioni_en',
                            'corso_in_pillole_it',
                            'corso_in_pillole_en',
                            'cosa_si_studia_it',
                            'cosa_si_studia_en',
                            'come_iscriversi_it',
                            'come_iscriversi_en',
                            'accesso_corso_it',
                            'accesso_corso_en',
                            'obiettivi_corso_it',
                            'obiettivi_corso_en',
                            'sbocchi_professionali_it',
                            'sbocchi_professionali_en', 
                            'sito_web_en',
                            'sito_web_it',])

    aa = forms.IntegerField(
        required=True,
        min_value=1901,
        max_value=now().year,
        label=_("Academic year"),
    )

    class Meta:
        model = SitoWebCdsDatiBase
        exclude = ['dt_mod', 'id_user_mod', 'id_didattica_regolamento', 'cds_cod', 'cds', 'lingua_it', 'lingua_en']
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
        label=_("Order"),
    )
    class Meta:
        exclude = ['id_sito_web_cds_dati_base', 'id_user_mod', 'dt_mod',]

class SitoWebCdsSliderForm(SitoWebCdsForm):

    slider_it = forms.CharField(
            label=_("Scrollable text (it)"),
            required=False,
            max_length=130
        )
    slider_en = forms.CharField(
            label=_("Scrollable text (en)"),
            required=False,
            max_length=130
        )
       
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