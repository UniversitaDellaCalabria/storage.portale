# from django.forms.widgets import ClearableFileInput, DateTimeInput
from django.forms.widgets import DateTimeInput


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
