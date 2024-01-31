from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import *
from django.conf import settings

from ricerca_app.models import *
from .validators import *

UNICMS_AUTH_TOKEN = getattr(settings, 'UNICMS_AUTH_TOKEN', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', '')


class SitoWebCdsDatiBaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SitoWebCdsDatiBaseForm, self).__init__(*args, **kwargs)
        
        self.fields['languages'] = forms.MultipleChoiceField(
            label=_("Languages"),
            choices = (('italiano', _('ITALIAN')), ('inglese', _('ENGLISH')), ('italiano, inglese', _('ITALIAN, ENGLISH')))
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
                            'sito_web_it',
                            'sito_web_en',
                            'accesso_corso_it',
                            'accesso_corso_en',
                            'obiettivi_corso_it',
                            'obiettivi_corso_en',
                            'sbocchi_professionali_it',
                            'sbocchi_professionali_en',]) 

    aa = forms.IntegerField(
        required=True,
        min_value=1901,
        max_value=now().year,
        label=_("Academic year"),
    )

    class Meta:
        model = SitoWebCdsDatiBase
        exclude = ['dt_mod', 'id_user_mod', 'id_didattica_regolamento', 'cds_cod', 'cds', 'lingua_it', 'lingua_en']

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