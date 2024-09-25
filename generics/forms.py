from django import forms
from django.utils.translation import gettext_lazy as _


class ChoosenPersonForm(forms.Form):
    choosen_person = forms.CharField(label=_('Person'),
                                     widget=forms.HiddenInput(),
                                     required=False)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        super(ChoosenPersonForm, self).__init__(*args, **kwargs)
        if required:
            self.fields['choosen_person'].required = True
