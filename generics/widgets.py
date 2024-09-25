from django.forms.widgets import DateTimeInput
from django_ckeditor_5.widgets import CKEditor5Widget


class RicercaCRUDDateTimeWidget(DateTimeInput):
    template_name = "widgets/ricerca_crud_datetime_field.html"

    class Media:
        css = {
            "all": ("css/font-awesome.min.css", "css/bootstrap-datetimepicker.min.css")
        }
        js = (
            "js/datetimepicker/moment.min.js",
            "js/datetimepicker/bootstrap-datetimepicker.js",
        )


class RicercaCRUDCkEditorWidget(CKEditor5Widget):
    template_name = "widgets/ricerca_crud_ckeditor_widget.html"
