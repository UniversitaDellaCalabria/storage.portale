from django.db.models import Q
from django_filters import rest_framework as filters
from cds_brochure.models import CdsBrochure

class BrochuresFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_search', label='Search by the name of the course of study.')

    def filter_by_search(self, queryset, name, value):
        query_search = Q()
        for k in value.split(" "):
            q_nome_corso_it = Q(cds__nome_cds_it__icontains=k)
            query_search &= q_nome_corso_it
        return queryset.filter(query_search)

    class Meta:
        model = CdsBrochure
        fields = ['search']
