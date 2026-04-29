import os
from django.forms.widgets import ClearableFileInput
from django.urls import reverse


class UrlValueWrapper:
    """
    Un wrapper che espone un attributo .url modificabile 
    e si comporta come una stringa per il nome del file.
    """
    def __init__(self, original_file, custom_url):
        self.file = original_file
        self.url = custom_url # Qui non abbiamo il blocco della property

    def __str__(self):
        return str(self.file)

    def __getattr__(self, name):
        # Passa qualsiasi altra chiamata (es. .size, .path) al file originale
        return getattr(self.file, name)

        
class CustomFileWidget(ClearableFileInput):
        
    def render(self, name, value, attrs=None, renderer=None):
        # Qui hai accesso a 'name'
        self.current_field_name = name 
        return super().render(name, value, attrs, renderer)
        
    def format_value(self, value):
        """
        'value' qui è l'oggetto FieldFile. 
        Se esiste, possiamo manipolare come appare nel link.
        """
        if value and hasattr(value, 'url'):
            response = None
            
            if self.current_field_name == 'path_doc_delibera':
                response = reverse(
                    "advanced-training:management:advanced-training-download-delibera",
                    kwargs={"pk": value.instance.pk},
                )
                
            if self.current_field_name == 'path_piano_finanziario':
                response = reverse(
                    "advanced-training:management:advanced-training-download-piano-finanziario",
                    kwargs={"pk": value.instance.pk},
                )
                
            if self.current_field_name == 'path_cv':
                response = reverse(
                    "advanced-training:management:advanced-training-download-cv-incarico",
                    kwargs={
                        "pk": value.instance.alta_formazione_dati_base.pk,
                        "pk_incarico": value.instance.pk
                    },
                )

            if response:
                return UrlValueWrapper("Download", response)
                
        return str(value)
