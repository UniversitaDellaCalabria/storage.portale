from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget
from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget
from research_lines.models import (
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)


class RicercaLineaApplicataForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaApplicata
        fields = [
            "descrizione",
            "descr_pubblicaz_prog_brevetto",
            "anno",
            "ricerca_aster2",
            "visibile",
        ]
        labels = {
            "descrizione": _("Denomination"),
            "descr_pubblicaz_prog_brevetto": _("Patent project description"),
            "anno": _("Year"),
            "ricerca_aster2": _("ASTER2"),
        }
        widgets = {"descr_pubblicaz_prog_brevetto": CKEditor5Widget()}

    class Media:
        js = ("js/textarea-autosize.js",)


class RicercaLineaBaseForm(forms.ModelForm):
    class Meta:
        model = RicercaLineaBase
        fields = [
            "descrizione",
            "descr_pubblicaz_prog_brevetto",
            "anno",
            "ricerca_erc2",
            "visibile",
        ]
        labels = {
            "descrizione": _("Denomination"),
            "descr_pubblicaz_prog_brevetto": _("Patent project description"),
            "anno": _("Year"),
            "ricerca_erc2": _("ERC2"),
        }
        widgets = {"descr_pubblicaz_prog_brevetto": CKEditor5Widget()}

    class Media:
        js = ("js/textarea-autosize.js",)


class RicercaDocenteLineaBaseForm(forms.ModelForm):
    choosen_person = forms.CharField(
        label=_("Teacher"), widget=forms.HiddenInput(), required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        dt_inizio = cleaned_data.get("dt_inizio")
        dt_fine = cleaned_data.get("dt_fine")

        if dt_inizio and dt_fine and dt_inizio > dt_fine:
            self.add_error("dt_inizio", _("Start date is greater than end date"))
            self.add_error("dt_fine", _("Start date is greater than end date"))

    class Meta:
        model = RicercaDocenteLineaBase
        fields = ["dt_inizio", "dt_fine"]
        labels = {
            "dt_inizio": _("From"),
            "dt_fine": _("To"),
        }
        widgets = {
            "dt_inizio": BootstrapItaliaDateWidget,
            "dt_fine": BootstrapItaliaDateWidget,
        }


class RicercaDocenteLineaApplicataForm(forms.ModelForm):
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
        model = RicercaDocenteLineaBase
        fields = ["dt_inizio", "dt_fine"]
        labels = {
            "dt_inizio": _("From"),
            "dt_fine": _("To"),
        }
        widgets = {
            "dt_inizio": BootstrapItaliaDateWidget,
            "dt_fine": BootstrapItaliaDateWidget,
        }
