from django.forms.widgets import ClearableFileInput


class RicercaCRUDClearableWidget(ClearableFileInput):
    template_name = 'widgets/ricerca_crud.clearable_field.html'
