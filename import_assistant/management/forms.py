from json import JSONEncoder

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from generics.validators import validate_file_size, validate_xlsx_file_extension
from import_assistant.settings import (
    REGDID_IMPORT_DEFINE_NEW_STRUCTURE,
    REGDID_IMPORT_USE_CURR_STRUCTURE,
)


class CdsImportForm(forms.Form):
    cds_list_file = forms.FileField(
        label=_("Upload file") + " (.xlsx)",
        validators=[validate_file_size, validate_xlsx_file_extension],
        widget=forms.ClearableFileInput(attrs={"accept": ".xlsx"}),
    )
    year = forms.ChoiceField(
        label=_("Year"),
        choices=[
            (y, y)
            for y in range(settings.CURRENT_YEAR + 1, settings.CURRENT_YEAR - 1, -1)
        ],
    )


class PrettyJSONEncoder(JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=4, sort_keys=True, **kwargs)


class RegdidStructureImportForm(forms.Form):
    year = forms.ChoiceField(
        label=_("Year"),
        choices=[
            (y, y)
            for y in range(
                settings.CURRENT_YEAR + 1,
                settings.CURRENT_YEAR - 1,
                -1,
            )
        ],
    )

    structure_choice = forms.ChoiceField(
        choices=(
            (REGDID_IMPORT_USE_CURR_STRUCTURE, _("Use existing structure")),
            (REGDID_IMPORT_DEFINE_NEW_STRUCTURE, _("Define a new structure")),
        ),
        initial=REGDID_IMPORT_USE_CURR_STRUCTURE,
        required=True,
        label=_("Choose procedure:"),
        help_text=_("WARNING: Defining a new structure will reset every existing regulation."),
        widget=forms.RadioSelect(attrs={"id": "id_structure_choice"}),
    )

    data = forms.JSONField(
        encoder=PrettyJSONEncoder,
        initial=list,
        required=False,
        label=_("New didactic regulation structure"),
        widget=forms.Textarea(
            attrs={
                "placeholder": 'Enter valid JSON data here. Example: {"key": "value"}',
                "rows": 6,
                "cols": 50,
                "id": "id_data",
                "disabled": "disabled",
            }
        ),
    )
