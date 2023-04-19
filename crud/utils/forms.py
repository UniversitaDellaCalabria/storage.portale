from django import forms
from django.utils.translation import gettext_lazy as _


class ChoosenPersonForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)
