from json import JSONEncoder

from django import forms
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import *

class PrettyJSONEncoder(JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=4, sort_keys=True, **kwargs)

class DidatticaArticoliRegolamentoStrutturaForm(forms.Form):
    structure = forms.JSONField(
        encoder=PrettyJSONEncoder,
        label=_('Structure JSON')
    )


class BaseArticoliModelForm(forms.ModelForm):
    class Meta:
        widgets = {
            'testo_it': CKEditor5Widget(),
            'testo_en': CKEditor5Widget()
        }
        labels = {
            'testo_it': _("Text (it)"),
            'testo_en': _("Text (en)")
        }

class DidatticaCdsArticoliRegolamentoForm(BaseArticoliModelForm):
    class Meta(BaseArticoliModelForm.Meta):
        model = DidatticaCdsArticoliRegolamento
        fields = ('testo_it', 'testo_en')
        

class DidatticaCdsSubArticoliRegolamentoForm(BaseArticoliModelForm):
    class Meta(BaseArticoliModelForm.Meta):
        model = DidatticaCdsSubArticoliRegolamento
        fields = ('ordine', 'titolo_it', 'titolo_en', 'testo_it', 'testo_en')
        labels = BaseArticoliModelForm.Meta.labels | {
            'ordine': _("Order"),
            'titolo_it': _("Titolo (it)"),
            'titolo_en': _("Titolo (en)")
        }
        help_texts = {
            'ordine': _("This field is also used to enumerate the article (ex: Art 1.x)")
        }
        
class DidatticaCdsArticoliRegolamentoNoteForm(forms.ModelForm):
    class Meta:
        model = DidatticaCdsArticoliRegolamento
        fields = ('note',)
        labels = {'note': _("Notes")}
        widgets = {'note': CKEditor5Widget()}