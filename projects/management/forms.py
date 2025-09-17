from django import forms
from django.utils.translation import gettext_lazy as _
# from django_ckeditor_5.widgets import CKEditor5Widget
from generics.widgets import RicercaCRUDCKEditor5EmptyContentWidget
from projects.models import ProgettoDatiBase, ProgettoResponsabileScientifico


class ProgettoDatiBaseForm(forms.ModelForm):
    class Meta:
        model = ProgettoDatiBase
        fields = [
            "is_active",
            "titolo",
            "anno_avvio",
            "ambito_territoriale",
            "tipologia_programma",
            "area_tecnologica",
            "descr_breve",
            "url_immagine",
            "abstract_ita",
            "abstract_eng",
            "url_sito_web",
            "call",
            "uo",
            "ordinamento",
        ]
        labels = {
            "titolo": _("Title"),
            "anno_avvio": _("Start year"),
            "ambito_territoriale": _("Territorial scope"),
            "tipologia_programma": _("Program type"),
            "area_tecnologica": _("Tech Area"),
            "descr_breve": _("Short description"),
            "url_immagine": _("Image URL"),
            "abstract_ita": _("Abstract (it)"),
            "abstract_eng": _("Abstract (en)"),
            "url_sito_web": _("URL"),
            "call": _("Call"),
            "uo": _("Organizational Unit"),
            "is_active": _("Active"),
            "ordinamento": _("Ordering"),
        }
        widgets = {
            "titolo": forms.Textarea(attrs={"rows": 2}),
            "descr_breve": RicercaCRUDCKEditor5EmptyContentWidget(),
            "abstract_ita": RicercaCRUDCKEditor5EmptyContentWidget(),
            "abstract_eng": RicercaCRUDCKEditor5EmptyContentWidget(),
            "uo": forms.HiddenInput(),
        }

    class Media:
        js = ("js/textarea-autosize.js",)


class ProgettoResponsabileScientificoForm(forms.ModelForm):
    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ["nome_origine"]
        labels = {"nome_origine": _("Name and Surname")}


class ProgettoRicercatoreForm(forms.ModelForm):
    class Meta:
        model = ProgettoResponsabileScientifico
        fields = ["nome_origine"]
        labels = {"nome_origine": _("Name and Surname")}


class ProgettoStrutturaForm(forms.Form):
    choosen_structure = forms.CharField(
        label=_("Structure"), widget=forms.HiddenInput(), required=True
    )
