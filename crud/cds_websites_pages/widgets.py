from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput
from django.urls import reverse

class OggettiPortaleWidget(TextInput):
    template_name = 'widgets/cds_websites_pages_oggetti_portale_widget.html'
    
    def __init__(self, sito_web_cds_dati_base_id, attrs=None):
        self.sito_web_cds_dati_base_id = sito_web_cds_dati_base_id
        super().__init__(attrs)
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        initial_value = value if value is not None else ''
        context["widget"]["sito_web_cds_dati_base_id"] = self.sito_web_cds_dati_base_id 
        context["widget"]["initial_value"] = initial_value
        return context
        
    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(renderer.render(self.template_name, context))
    

class ExternalOggettiPortaleWidget(TextInput):
    template_name = 'widgets/cds_websites_pages_external_oggetti_portale_widget.html'
            
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        initial_value = value if value is not None else ''
        context["widget"]["initial_value"] = initial_value
        return context
        
    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(renderer.render(self.template_name, context))