# from django.forms.widgets import ClearableFileInput, DateTimeInput
from django import forms, get_version
from django.conf import settings
from django.forms.renderers import get_default_renderer
from django.forms.widgets import DateTimeInput
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_ckeditor_5.widgets import CKEditor5Widget

# class RicercaCRUDClearableWidget(ClearableFileInput):
    # template_name = 'widgets/ricerca_crud.clearable_field.html'


class RicercaCRUDDateTimeWidget(DateTimeInput):
    template_name = "widgets/ricerca_crud_datetime_field.html"

    class Media:
        css = {
            "all": ("css/font-awesome.min.css",
                    "css/bootstrap-datetimepicker.min.css")
        }
        js = (
            "js/datetimepicker/moment.min.js",
            "js/datetimepicker/bootstrap-datetimepicker.js",
        )


class RicercaCRUDCkEditorWidget(CKEditor5Widget):
    template_name = 'widgets/ricerca_crud_ckeditor_widget.html'
