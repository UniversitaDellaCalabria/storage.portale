from django_filters import rest_framework as filters
from django.db.models import Q
from structures.models import (
    UnitaOrganizzativa,
)
import datetime


class StructuresFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for name.",
    )
    father = filters.CharFilter(
        method="filter_father",
        label="Father",
        help_text="Search for father.",
    )
    type = filters.CharFilter(
        method="filter_type",
        label="Type",
        help_text="Search for type.",
    )
    depth = filters.CharFilter(
        method="filter_depth",
        label="Depth",
        help_text="Type 1 if you want to see the structure childs otherwise 0.",
    )

    def filter_depth(self, queryset, name, value):
        if value == "1":
            for q in queryset:
                q["childs"] = (
                    UnitaOrganizzativa.objects.filter(
                        uo_padre=q["uo"],
                        dt_fine_val__gte=datetime.datetime.today(),
                    )
                    .values("uo", "denominazione", "ds_tipo_nodo", "cd_tipo_nodo")
                    .distinct()
                    .order_by("denominazione")
                )
        return queryset

    def filter_type(self, queryset, name, value):
        query_type = Q()
        for k in type.split(","):
            q_type = Q(cd_tipo_nodo=k)
            query_type |= q_type
        return queryset.filter(query_type)

    def filter_father(self, queryset, name, value):
        query_father = (
            Q(uo_padre__isnull=True) if value is not None else Q(uo_padre__uo_id=value)
        )
        return queryset.filter(query_father)

    def filter_search(self, queryset, name, value):
        if value is not None:
            q_objects = Q()
            for k in value.split(" "):
                q_objects &= Q(denominazione__icontains=k)
            queryset = queryset.filter(q_objects)
        return queryset

    class Meta:
        model = UnitaOrganizzativa
        fields = []


class TypesFilter(filters.FilterSet):
    father = filters.CharFilter(
        field_name="uo_padre",
        lookup_expr="exact",
        label="Father",
        help_text="Search for father.",
    )

    class Meta:
        model = UnitaOrganizzativa
        fields = []
