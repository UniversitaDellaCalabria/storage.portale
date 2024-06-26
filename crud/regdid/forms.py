from json import JSONEncoder
from re import sub

from django import forms
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.widgets import CKEditor5Widget

from ricerca_app.models import *
from ricerca_app.validators import validate_pdf_file_extension, validate_file_size

def _normalize_text(text):
    normalized_text = text
    normalized_text = sub(r"(\&[a-z0-9#]{2,8}\;)", " ", normalized_text)
    normalized_text = sub(r"(\r|\n)", "", normalized_text)
    normalized_text = normalized_text.strip()
    normalized_text = strip_tags(normalized_text)
    return normalized_text

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
            'testo_it': CKEditor5Widget(config_name="regdid"),
            'testo_en': CKEditor5Widget(config_name="regdid")
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
            'titolo_it': _("Title (it)"),
            'titolo_en': _("Title (en)")
        }
        
class DidatticaCdsArticoliRegolamentoNoteForm(forms.ModelForm):
    def clean_note(self):
        data = self.cleaned_data["note"]
        if data:
            data_n = _normalize_text(data)
            if not data_n or data_n.isspace():
                data = None
        return data
    
    class Meta:
        model = DidatticaCdsArticoliRegolamento
        fields = ('note',)
        labels = {'note': _("Notes")}
        widgets = {'note': CKEditor5Widget(config_name="regdid")}
        help_texts = {'note': _("This field is shared between the main article and its sub articles")}
        
class DidatticaCdsArticoliRegolamentoTestataNoteForm(DidatticaCdsArticoliRegolamentoNoteForm):
    def clean_note(self):
        data = self.cleaned_data["note"]
        if data:
            data_n = _normalize_text(data)
            if not data_n or data_n.isspace():
                data = ''
        return data
        
    class Meta(DidatticaCdsArticoliRegolamentoNoteForm.Meta):
        model = DidatticaCdsArticoliRegolamentoTestata
        help_texts = {}
        
        
class DidatticaCdsTestataStatusForm(forms.Form):
    motivazione = forms.CharField(
        label = _("Reason"),
        required = True,
        widget=forms.widgets.Textarea()
    )
    
class RegolamentoPdfImportForm(forms.Form):
    pdf = forms.FileField(
        label=_("PDF Regulation"),
        validators=[validate_pdf_file_extension, validate_file_size],
        required=True,
    )
    
    first_page = forms.ChoiceField(
        label=_("Number of the page which contains 'TITOLO I' - Count from 1 from the title page (included)"),
        choices=(((num, num) for num in range(1,200)))
    )
    
    last_page = forms.ChoiceField(
        label=_("Number of the page which contains the last article untill the end - Count from 1 from the title page (included)"),
        choices=(((num, num) for num in range(1,200)))
    )