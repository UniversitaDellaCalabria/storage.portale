from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


class OggettiPortaleWidget(TextInput):
    template_name = "widgets/cds_websites_oggetti_portale_widget.html"

    def __init__(self, cds_id, attrs=None):
        self.cds_id = cds_id
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        initial_value = value if value is not None else ""
        context["widget"]["cds_id"] = self.cds_id
        context["widget"]["initial_value"] = initial_value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(renderer.render(self.template_name, context))  # nosec B703, B308


class ExternalOggettiPortaleWidget(TextInput):
    template_name = "widgets/cds_websites_external_oggetti_portale_widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        initial_value = value if value is not None else ""
        context["widget"]["initial_value"] = initial_value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(renderer.render(self.template_name, context))  # nosec B703, B308
