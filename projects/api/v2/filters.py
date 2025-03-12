from django_filters import rest_framework as filters
from django.db.models import Q
from projects.models import ProgettoDatiBase
class ProjectsFilter(filters.FilterSet):
    search = filters.CharFilter(
    method="filter_search", 
    label="Search", 
    help_text="Search for projects by title, technological area, infrastructure, year, or territorial scope."
    )
    techarea = filters.CharFilter(
        field_name="area_tecnologica", 
        lookup_expr="exact", 
        label="Technological Area", 
        help_text="Filter by exact match for the technological area."
    )
    infrastructure = filters.NumberFilter(
        field_name="uo", 
        lookup_expr="exact", 
        label="Infrastructure", 
        help_text="Filter by id of the infrastructure."
    )
    programtype = filters.CharFilter(
        method="filter_programtype", 
        label="Program Type", 
        help_text="Filter by the program type."
    )
    notprogramtype = filters.CharFilter(
        method="filter_notprogramtype", 
        label="Not Program Type", 
        help_text="Exclude projects of the specified program types."
    )
    territorialscope = filters.CharFilter(
        field_name="ambito_territoriale", 
        lookup_expr="exact", 
        label="Territorial Scope", 
        help_text="Filter by territorial scope."
    )
    year = filters.NumberFilter(
        field_name="anno_avvio", 
        lookup_expr="exact", 
        label="Year", 
        help_text="Filter by the year the project started."
    )


    def filter_search(self, queryset, name, value):
        search_terms = value.split(" ")
        query = Q()
        for term in search_terms:
            query |= (
                Q(titolo__icontains=term)
                | Q(area_tecnologica__descr_area_ita__icontains=term)
                | Q(uo__denominazione__icontains=term)
                | Q(anno_avvio__icontains=term)
                | Q(ambito_territoriale__ambito_territoriale__icontains=term)
            )
        return queryset.filter(query)

    def filter_programtype(self, queryset, name, value):
        programtypes = value.split(",")
        return queryset.filter(tipologia_programma__in=programtypes)

    def filter_notprogramtype(self, queryset, name, value):
        notprogramtypes = value.split(",")
        return queryset.exclude(tipologia_programma__in=notprogramtypes)
    
    class Meta:
        model = ProgettoDatiBase
        fields = []