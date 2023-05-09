from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ricerca_app.models import (SitoWebCdsDatiBase,
                                SitoWebCdsExStudenti,
                                SitoWebCdsLink,
                                SitoWebCdsSlider)

from .. utils.settings import CMS_STORAGE_ROOT_API
from .. utils.widgets import RicercaCRUDClearableWidget


CMS_STORAGE_ROOT_API = getattr(settings, 'CMS_STORAGE_ROOT_API', CMS_STORAGE_ROOT_API)


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


# class SpinoffStartupDatiBaseReferentForm(forms.ModelForm):
#     choosen_person = forms.CharField(label=_('Person'),
#                                      widget=forms.HiddenInput(),
#                                      required=False)
#
#     class Meta:
#         model = SpinoffStartupDatiBase
#         fields = ['referente_unical']
#         labels = {
#             "referente_unical": _("Label"),
#         }
#
#
# class SpinoffStartupDipartimentoForm(forms.ModelForm):
#     choosen_department = forms.CharField(label=_('Department'),
#                                          widget=forms.HiddenInput(),
#                                          required=False)
#
#     class Meta:
#         model = SpinoffStartupDipartimento
#         fields = []
#
#     class Media:
#         js = ('js/textarea-autosize.js',)
