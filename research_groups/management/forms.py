from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from generics.widgets import RicercaCRUDCKEditor5EmptyContentWidget
from research_groups.models import RicercaDocenteGruppo, RicercaGruppo


class RicercaGruppoForm(forms.ModelForm):
    class Meta:
        model = RicercaGruppo
        fields = ["nome", "descrizione", "ricerca_erc1"]
        labels = {
            "nome": _("Name"),
            "description": _("Description"),
            "ricerca_erc1": _("ERC1"),
        }
        widgets = {"descrizione": RicercaCRUDCKEditor5EmptyContentWidget()}

    class Media:
        js = ("js/textarea-autosize.js",)


class RicercaGruppoDocenteForm(forms.ModelForm):
    choosen_person = forms.CharField(
        label=_("Person"), widget=forms.HiddenInput(), required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        dt_inizio = cleaned_data.get("dt_inizio")
        dt_fine = cleaned_data.get("dt_fine")

        if dt_inizio and dt_fine and dt_inizio > dt_fine:
            self.add_error("dt_inizio", _("Start date is greater than end date"))
            self.add_error("dt_fine", _("Start date is greater than end date"))

    class Meta:
        model = RicercaDocenteGruppo
        fields = ["dt_inizio", "dt_fine"]
        labels = {"dt_inizio": _("From"), "dt_fine": _("To")}

        widgets = {
            "dt_inizio": BootstrapItaliaDateWidget,
            "dt_fine": BootstrapItaliaDateWidget,
        }
