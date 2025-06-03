from django.db.models import Q
from django_filters import rest_framework as filters
from companies.models import SpinoffStartupDatiBase


class CompaniesFilter(filters.FilterSet):
    techarea = filters.CharFilter(
        field_name="area_tecnologica",
        lookup_expr="exact",
        label="Technological Area",
        help_text="Search by technological area",
    )
    spinoff = filters.BooleanFilter(
        field_name="is_spinoff",
        label="Spin-Off",
        help_text="Filter by whether the company is a spin-off (True/False)",
    )
    startup = filters.BooleanFilter(
        field_name="is_startup",
        label="Startup",
        help_text="Filter by whether the company is a Startup (True/False)",
    )
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search by company name or description",
    )
    departments = filters.CharFilter(
        method="filter_departments",
        label="Departments",
        help_text="Filter by departments",
    )

    def filter_search(self, queryset, name, value):
        if value:
            query_search = Q()
            for k in value.split(" "):
                q_nome = Q(descrizione_ita__icontains=k) | Q(nome_azienda__icontains=k)
                query_search &= q_nome
            return queryset.filter(query_search)

    def filter_departments(self, queryset, name, value):
        if value:
            dep_codes = value.split(",")
            queryset = queryset.filter(
                spinoffstartupdipartimento__didattica_dipartimento__dip_cod__in=dep_codes
            ).distinct()
        return queryset

    class Meta:
        model = SpinoffStartupDatiBase
        fields = []
