from django.forms.widgets import DateTimeInput
from django_ckeditor_5.widgets import CKEditor5Widget


class RicercaCRUDDateTimeWidget(DateTimeInput):
    template_name = "widgets/ricerca_crud_datetime_field.html"

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
        self.format = '%Y-%m-%d %H:%M'


class RicercaCRUDCKEditor5EmptyContentWidget(CKEditor5Widget):
    def __init__(self, *args, **kwargs):
        # Personalizza la configurazione iniziale di CKEditor (se necessario)
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        # Personalizza il valore qui (ad esempio, rimuovi contenuti vuoti)
        if value.strip() == '<p>&nbsp;</p>':
            return ''
        return value


class RicercaCRUDCkEditorWidget(RicercaCRUDCKEditor5EmptyContentWidget):
    template_name = "widgets/ricerca_crud_ckeditor_widget.html"
