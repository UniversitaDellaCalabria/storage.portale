from cds_brochure.models import (
    CdsBrochure,
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider,
)
from django import forms
from django.utils.translation import gettext_lazy as _
from generics.widgets import RicercaCRUDCkEditorWidget

from .validators import (
    CKEditorWidgetMaxLenghtValidator,
    CKEditorWidgetMinLenghtValidator,
)


# -- Dati corso: posti
class CdsBrochureDatiCorsoForm(forms.ModelForm):
    class Meta:
        model = CdsBrochure
        fields = [
            "num_posti",
        ]
        labels = {
            "num_posti": _("Seats Number"),
        }


# -- In pillole: corso in pillole, cosa si studia, iscrizione
class CdsBrochureInPilloleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CdsBrochureInPilloleForm, self).__init__(*args, **kwargs)

        labels = {
            "corso_in_pillole_it": _("Course in a nutshell (it)"),
            "corso_in_pillole_en": _("Course in a nutshell (en)"),
            "cosa_si_studia_it": _("What you will study (it)"),
            "cosa_si_studia_en": _("What you will study (en)"),
            "come_iscriversi_it": _("How to enroll (it)"),
            "come_iscriversi_en": _("How to enroll (en)"),
        }

        ckeditor_fields = [
            {"corso_in_pillole_it": {"min": 300, "max": 600, "enforce": False}},
            {"corso_in_pillole_en": {"min": 300, "max": 600, "enforce": False}},
            {"cosa_si_studia_it": {"min": 300, "max": 600, "enforce": False}},
            {"cosa_si_studia_en": {"min": 300, "max": 600, "enforce": False}},
            {"come_iscriversi_it": {"min": 300, "max": 600, "enforce": False}},
            {"come_iscriversi_en": {"min": 300, "max": 600, "enforce": False}},
        ]

        for field in ckeditor_fields:
            for name, min_max in field.items():
                self.fields[name] = forms.CharField(
                    label=labels[name],
                    required=False,
                    widget=RicercaCRUDCkEditorWidget(
                        attrs={"min": min_max["min"], "max": min_max["max"]}
                    ),
                    validators=[
                        CKEditorWidgetMinLenghtValidator(min_max["min"]),
                        CKEditorWidgetMaxLenghtValidator(min_max["max"]),
                    ]
                    if min_max["enforce"]
                    else [],
                )

    class Meta:
        model = CdsBrochure
        fields = [
            "corso_in_pillole_it",
            "corso_in_pillole_en",
            "cosa_si_studia_it",
            "cosa_si_studia_en",
            "come_iscriversi_it",
            "come_iscriversi_en",
        ]

    # class Media:
        # js = ("js/textarea-autosize.js",)


# -- Profilo corso: Descrizione, Ammissione, Obiettivi, Sbocchi
class CdsBrochureProfiloCorsoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CdsBrochureProfiloCorsoForm, self).__init__(*args, **kwargs)

        labels = {
            "descrizione_corso_it": _("Description (it)"),
            "descrizione_corso_en": _("Description (en)"),
            "accesso_corso_it": _("Admission (it)"),
            "accesso_corso_en": _("Admission (en)"),
            "obiettivi_corso_it": _("Goals (it)"),
            "obiettivi_corso_en": _("Goals (en)"),
            "sbocchi_professionali_it": _("Job opportunities (it)"),
            "sbocchi_professionali_en": _("Job opportunituies (en)"),
        }

        ckeditor_fields = [
            {"descrizione_corso_it": {"min": 0, "max": 700, "enforce": False}},
            {"descrizione_corso_en": {"min": 0, "max": 700, "enforce": False}},
            {"accesso_corso_it": {"min": 200, "max": 500, "enforce": False}},
            {"accesso_corso_en": {"min": 200, "max": 500, "enforce": False}},
            {"obiettivi_corso_it": {"min": 200, "max": 500, "enforce": False}},
            {"obiettivi_corso_en": {"min": 200, "max": 500, "enforce": False}},
            {"sbocchi_professionali_it": {"min": 300, "max": 500, "enforce": False}},
            {"sbocchi_professionali_en": {"min": 300, "max": 500, "enforce": False}},
        ]

        for field in ckeditor_fields:
            for name, min_max in field.items():
                self.fields[name] = forms.CharField(
                    label=labels[name],
                    required=False,
                    widget=RicercaCRUDCkEditorWidget(
                        attrs={"min": min_max["min"], "max": min_max["max"]}
                    ),
                    validators=[
                        CKEditorWidgetMinLenghtValidator(min_max["min"]),
                        CKEditorWidgetMaxLenghtValidator(min_max["max"]),
                    ]
                    if min_max["enforce"]
                    else [],
                )

    class Meta:
        model = CdsBrochure
        fields = [
            "descrizione_corso_it",
            "descrizione_corso_en",
            "accesso_corso_it",
            "accesso_corso_en",
            "obiettivi_corso_it",
            "obiettivi_corso_en",
            "sbocchi_professionali_it",
            "sbocchi_professionali_en",
        ]

    # class Media:
        # js = ("js/textarea-autosize.js",)


# -- Intro amm: Tasse, contributi, agevolazioni
class CdsBrochureIntroAmmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CdsBrochureIntroAmmForm, self).__init__(*args, **kwargs)

        labels = {
            "tasse_contributi_esoneri_it": _("Taxes (it)"),
            "tasse_contributi_esoneri_en": _("Taxes (en)"),
            "borse_studio_it": _("Scholarships (it)"),
            "borse_studio_en": _("Scholarships (en)"),
            "agevolazioni_it": _("Concessions (it)"),
            "agevolazioni_en": _("Concessions (en)"),
        }

        ckeditor_fields = [
            {"tasse_contributi_esoneri_it": {"min": 0, "max": 400, "enforce": False}},
            {"tasse_contributi_esoneri_en": {"min": 0, "max": 400, "enforce": False}},
            {"borse_studio_it": {"min": 200, "max": 400, "enforce": False}},
            {"borse_studio_en": {"min": 200, "max": 400, "enforce": False}},
            {"agevolazioni_it": {"min": 200, "max": 400, "enforce": False}},
            {"agevolazioni_en": {"min": 200, "max": 400, "enforce": False}},
        ]

        for field in ckeditor_fields:
            for name, min_max in field.items():
                self.fields[name] = forms.CharField(
                    label=labels[name],
                    required=False,
                    widget=RicercaCRUDCkEditorWidget(
                        attrs={"min": min_max["min"], "max": min_max["max"]}
                    ),
                    validators=[
                        CKEditorWidgetMinLenghtValidator(min_max["min"]),
                        CKEditorWidgetMaxLenghtValidator(min_max["max"]),
                    ]
                    if min_max["enforce"]
                    else [],
                )

    class Meta:
        model = CdsBrochure
        fields = [
            "tasse_contributi_esoneri_it",
            "tasse_contributi_esoneri_en",
            "borse_studio_it",
            "borse_studio_en",
            "agevolazioni_it",
            "agevolazioni_en",
        ]

    # class Media:
        # js = ("js/textarea-autosize.js",)


class CdsBrochureExStudentiForm(forms.ModelForm):
    class Meta:
        model = CdsBrochureExStudenti
        exclude = [
            "cds_brochure",
            "user_mod",
            "dt_mod",
        ]
        labels = {
            "ordine": _("Order"),
            "foto": _("Picture"),
            "profilo_it": _("Profile (it)"),
            "profilo_en": _("Profile (en)"),
            "link_it": _("Link (it)"),
            "link_en": _("Link (en)"),
        }


class SitoWebCdsForm(forms.ModelForm):
    ordine = forms.IntegerField(
        required=True,
        min_value=0,
        label=_("Order"),
    )

    class Meta:
        exclude = [
            "cds_brochure",
            "user_mod",
            "dt_mod",
        ]


class CdsBrochureSliderForm(SitoWebCdsForm):
    slider_it = forms.CharField(
        label=_("Scrollable text (it)"), required=False, max_length=130
    )
    slider_en = forms.CharField(
        label=_("Scrollable text (en)"), required=False, max_length=130
    )

    class Meta(SitoWebCdsForm.Meta):
        model = CdsBrochureSlider
        labels = {
            "slider_it": _("Scrollable text (it)"),
            "slider_en": _("Scrollable text (en)"),
            "ordine": _("Order"),
        }


class CdsBrochureLinkForm(SitoWebCdsForm):
    class Meta(SitoWebCdsForm.Meta):
        model = CdsBrochureLink
        labels = {
            "ordine": _("Order"),
            "descrizione_link_it": _("Link description (it)"),
            "descrizione_link_en": _("Link description (en)"),
            "link_it": _("Link (it)"),
            "link_en": _("Link (en)"),
        }
