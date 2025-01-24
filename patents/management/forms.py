from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from generics.widgets import RicercaCRUDCKEditor5EmptyContentWidget
from patents.models import BrevettoDatiBase, BrevettoInventori


class BrevettoDatiBaseForm(forms.ModelForm):
    class Meta:
        model = BrevettoDatiBase
        labels = {
            "id_univoco": _("Patent identifier"),
            "titolo": _("Title"),
            "breve_descrizione": _("Short description"),
            "area_tecnologica": _("Tech area"),
            "url_knowledge_share": _("URL Knowledge Share"),
            "applicazioni": _("Applications"),
            "vantaggi": _("Advantages"),
            "trl_initial": _("Initial TRL"),
            "trl_aggiornato": _("Updated TRL"),
            "valorizzazione": _("Enhancement"),
            "proprieta": _("Property"),
            "status_legale": _("Legal status"),
            "data_priorita": _("Date"),
            "territorio": _("Territory"),
            "diritto_commerciale": _("Commercial right"),
            "disponibilita": _("Availability"),
            "area_ks": _("Area KS"),
            "nome_file_logo": _("Logo"),
            "is_active": _("Active"),
            "ordinamento": _("Ordering"),
            # 'url_immagine': _('Logo URL')
        }
        fields = [
            "is_active",
            "id_univoco",
            "titolo",
            "breve_descrizione",
            "area_tecnologica",
            "url_knowledge_share",
            "applicazioni",
            "vantaggi",
            "trl_iniziale",
            "trl_aggiornato",
            "valorizzazione",
            "proprieta",
            "status_legale",
            "data_priorita",
            "territorio",
            "diritto_commerciale",
            "disponibilita",
            "area_ks",
            "nome_file_logo",
            "ordinamento",
        ]
        # 'url_immagine']
        widgets = {
            "titolo": forms.Textarea(attrs={"rows": 2}),
            "proprieta": forms.Textarea(attrs={"rows": 2}),
            "breve_descrizione": RicercaCRUDCKEditor5EmptyContentWidget(),
            "applicazioni": RicercaCRUDCKEditor5EmptyContentWidget(),
            "vantaggi": RicercaCRUDCKEditor5EmptyContentWidget(),
            "data_priorita": BootstrapItaliaDateWidget,
        }

    # def __init__(self, *args, **kwargs):
    # super(BrevettoDatiBaseForm, self).__init__(*args, **kwargs)
    # _logo_field = self.instance.nome_file_logo
    # self.fields['nome_file_logo'].widget = RicercaCRUDClearableWidget(
    # {'upload_to': _logo_field.field.upload_to(
    # self.instance, _logo_field.name)}
    # )

    class Media:
        js = ("js/textarea-autosize.js",)


class BrevettoInventoriForm(forms.ModelForm):
    class Meta:
        model = BrevettoInventori
        fields = ["cognomenome_origine"]
        labels = {
            "cognomenome_origine": _("Name and Surname"),
        }
