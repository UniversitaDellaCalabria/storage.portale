from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget

from ricerca_app.models import *


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
    class Meta:
        model = RicercaDocenteGruppo
        fields = ['dt_inizio', 'dt_fine']
        widgets = {'dt_inizio': BootstrapItaliaDateWidget,
                   'dt_fine': BootstrapItaliaDateWidget, }


class RicercaLineaApplicataForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = ['descrizione', 'descr_pubblicaz_prog_brevetto',
                  'anno', 'ricerca_aster2']

    class Media:
        js = ('js/textarea-autosize.js',)
