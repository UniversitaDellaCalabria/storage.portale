from django_filters import rest_framework as filters
from django.db.models import Q
from advanced_training.models import AltaFormazioneDatiBase


class HighFormationMastersFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for scientific director surname or course title in Italian.",
    )
    director = filters.CharFilter(
        field_name="matricola_direttore_scientifico",
        lookup_expr="exact",
        label="Director",
        help_text="Filter by scientific director id.",
    )
    coursetype = filters.CharFilter(
        method="filter_coursetype",
        label="Course Type",
        help_text="Filter by course type id.",
    )
    erogation = filters.CharFilter(
        field_name="alta_formazione_mod_erogazione.id",
        lookup_expr="exact",
        label="Erogation Mode",
        help_text="Filter by erogation mode id.",
    )
    department = filters.CharFilter(
        field_name="dipartimento_riferimento.dip_cod",
        lookup_expr="exact",
        label="Department",
        help_text="Filter by department cod.",
    )
    language = filters.CharFilter(
        field_name="lingua",
        lookup_expr="exact",
        label="Language",
        help_text="Filter by course language.",
    )
    year = filters.CharFilter(
        field_name="anno_rilevazione",
        lookup_expr="exact",
        label="Year",
        help_text="Filter by course year.",
    )

    def filter_coursetype(self, queryset, name, value):
        coursetypes = value.split(",")
        query_coursetype = Q(alta_formazione_tipo_corso__in=coursetypes)
        queryset = queryset.filter(query_coursetype)
        return queryset

    def filter_search(self, queryset, name, value):
        for k in value.split(" "):
            q_nome = Q(titolo_it__icontains=k) | Q(
                matricola_direttore_scientifico__cognome__istartswith=k
            )
            queryset = queryset.filter(q_nome)
        return queryset

    class Meta:
        model = AltaFormazioneDatiBase
        fields = []
