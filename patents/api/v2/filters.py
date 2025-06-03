from django.db.models import Q
from django_filters import rest_framework as filters
from patents.models import BrevettoDatiBase


class PatentFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Title",
        help_text="Search by title",
    )
    techarea = filters.CharFilter(
        field_name="filter_techarea",
        lookup_expr="exact",
        label="Teaching Area",
        help_text="Search by Teaching Area",
    )
    structure = filters.CharFilter(
        method="filter_structure",
        label="Structure",
        help_text="Search by structure",
    )

    def filter_search(self, queryset, search, value):
        for k in search.split(" "):
            return queryset.filter(Q(titolo__icontains=k))

    def filter_structure(self, queryset, structure, value):
        return queryset.filter(
            Q(brevettoinventori__matricola_inventore__cd_uo_aff_org=structure)
        )

    class Meta:
        model = BrevettoDatiBase
        fields = []
