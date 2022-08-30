from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ricerca_app.models import *


# common methods
def _clean_teacher_dates(obj, cleaned_data):
    dt_inizio = cleaned_data.get('dt_inizio')
    dt_fine = cleaned_data.get('dt_fine')

    if dt_inizio and dt_fine and dt_inizio > dt_fine:
        obj.add_error('dt_inizio',
                      _("Start date is greater than end date"))
        obj.add_error('dt_fine',
                      _("Start date is greater than end date"))
# end common methods

class RicercaGruppoForm(forms.ModelForm):
    class Meta:
        model = RicercaGruppo
        fields = ['nome', 'descrizione', 'ricerca_erc1']
        widgets = {'descrizione': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaGruppoDocenteForm(forms.ModelForm):
    choosen_teacher = forms.CharField(label=_('Teacher'),
                                      widget = forms.HiddenInput(),
                                      required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteGruppo
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget,}


class RicercaLineaApplicataForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_aster2']
        widgets = {'descr_pubblicaz_prog_brevetto': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaLineaBaseForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaBase
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto', 'anno', 'ricerca_erc2']
        widgets = {'descr_pubblicaz_prog_brevetto': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)


class RicercaDocenteLineaBaseForm(forms.ModelForm):
    choosen_teacher = forms.CharField(label=_('Teacher'),
                                      widget = forms.HiddenInput(),
                                      required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class RicercaDocenteLineaApplicataForm(forms.ModelForm):
    choosen_teacher = forms.CharField(label=_('Teacher'),
                                      widget = forms.HiddenInput(),
                                      required=True)

    def clean(self):
        cleaned_data = super().clean()
        _clean_teacher_dates(self, cleaned_data)

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


# class DidatticaCdsAltriDatiForm(forms.ModelForm):
#     class Meta:
#         model = DidatticaCdsAltriDati
#         fields = ['cds', 'matricola_coordinatore', 'nome_origine_coordinatore', 'matricola_vice_coordinatore', 'nome_origine_vice_coordinatore', 'num_posti', 'modalita_iscrizione']
#         widgets = {'modalita_iscrizione': forms.Textarea(attrs={'rows': 2})}
#
#     class Media:
#         js = ('js/textarea-autosize.js',)
#
#
#
# class DidatticaCdsAltriDatiUfficioForm(forms.ModelForm):
#     class Meta:
#         model = DidatticaCdsAltriDati
#         fields = ['cds', 'ordine', 'matricola_rifermento', 'nome_ufficio', 'nome_origine_riferimento', 'telefono', 'email', 'edificio', 'piano', 'orari', 'sportello_online']
#         widgets = {'orari': forms.Textarea(attrs={'rows': 2})}
#
#     class Media:
#         js = ('js/textarea-autosize.js',)
