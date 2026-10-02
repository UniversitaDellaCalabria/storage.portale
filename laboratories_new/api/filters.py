from django_filters import rest_framework as filters
from django.db.models import Q
from laboratories_new.models import LaboratorioDatiBase


class LaboratoriesFilters(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Cerca nel nome del laboratorio",
    )
    ambito = filters.CharFilter(
        field_name="ambito_s3_prevalente__id",
        lookup_expr="exact",
        label="Ambito",
    )
    dip = filters.CharFilter(method="filter_dip", label="Dipartimento")
    erc1 = filters.CharFilter(method="filter_erc1", label="Ricerca Erc1")
    infrastructure = filters.CharFilter(
        field_name="infrastruttura_riferimento__id",
        lookup_expr="exact",
        label="Infrastruttura",
    )
    teacher = filters.CharFilter(
        method="filter_teacher",
        label="Docente",
        help_text="Filtra per id_ab del personale coinvolto",
    )

    def filter_teacher(self, queryset, name, value):
        return queryset.filter(
            Q(laboratorioresponsabile__matricola_personale__id_ab=value)
            | Q(laboratorioaffiliati__matricola_personale__id_ab=value)
        ).distinct()

    def filter_erc1(self, queryset, name, value):
        return queryset.filter(
            laboratoriodatierc1__ricerca_erc1__cod_erc1__in=value.split(",")
        ).distinct()

    def filter_dip(self, queryset, name, value):
        return queryset.filter(
            laboratoriodipartimenti__didattica_dipartimento__dip_cod=value
        ).distinct()

    def filter_search(self, queryset, name, value):
        for k in value.split():
            queryset = queryset.filter(nome_laboratorio__icontains=k)
        return queryset

    class Meta:
        model = LaboratorioDatiBase
        fields = []
