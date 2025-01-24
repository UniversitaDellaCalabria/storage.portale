from django.forms.widgets import DateTimeInput
from django_ckeditor_5.widgets import CKEditor5Widget


class RicercaCRUDDateTimeWidget(DateTimeInput):
    template_name = "widgets/ricerca_crud_datetime_field.html"

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
        self.format = '%Y-%m-%d %H:%M'


class RicercaCRUDCkEditorWidget(CKEditor5Widget):
    template_name = "widgets/ricerca_crud_ckeditor_widget.html"
