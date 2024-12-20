from django_filters import rest_framework as filters
from django.http import Http404

from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa


class CdsFilter(filters.FilterSet):
    nome_cds_it = filters.CharFilter(
        field_name="nome_cds_it",
        lookup_expr="icontains",
        label="Nome Cds",
        help_text="Filtra per nome del Cds.",
        # example="test"
    )

    class Meta:
        model = DidatticaCds
        fields = []


class DegreeTypeFilter(filters.FilterSet):
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = []


class DidatticaAttivitaFormativaFilter(filters.FilterSet):
    class Meta:
        model = DidatticaAttivitaFormativa
        fields = []