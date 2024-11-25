from json import JSONEncoder

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from generics.validators import validate_file_size, validate_xlsx_file_extension


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
    data = forms.JSONField(
        encoder=PrettyJSONEncoder,
        initial=list,
        label=_("Didactic regulation structure"),
        widget=forms.Textarea(
            attrs={
                "placeholder": 'Enter valid JSON data here. Example: {"key": "value"}',
                "rows": 6,
                "cols": 50,
            }
        ),
    )
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
    copy_previous = forms.BooleanField(
        initial=1,
        required=False,
        label=_("Copy articles from previous years"),
        help_text=_(
            "Check this box if you want to copy matching articles from the previous year for each didactic regulation"
        ),
    )
