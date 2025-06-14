from django_filters import rest_framework as filters
from django.db.models import Q
from laboratories.models import LaboratorioDatiBase
from generics.utils import decrypt

class LaboratoriesFilters(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for finalità ricerca, finalità didattica o finalità servizi",
    )
    ambito = filters.CharFilter(
        field_name="ambito",
        lookup_expr="exact",
        label="Ambito",
        help_text="Search for ambito",
    )
    dip = filters.CharFilter(
        method="filter_dip",
        label="Dipartimento",
        help_text="Search for dipartimento",
    )
    erc1 = filters.CharFilter(
        method="filter_erc1",
        label="Ricerca Erc1",
        help_text="Search for ricerca erc1",
    )
    infrastructure = filters.CharFilter(
        field_name="infrastruttura_riferimento__id",
        lookup_expr="exact",
        label="Infrastruttura",
        help_text="Search for id dell'infrastruttura",
    )

    teacher = filters.CharFilter(
        method="filter_teacher",
        label="Docente",
        help_text="Filtra per matricola del personale coinvolto",
    )
    scope = filters.CharFilter(
        method="filter_scope",
        label="Tipologia attività",
        help_text="Filtra per id tipologia attività",
    )

    def filter_teacher(self, queryset, name, value):
        valueDecript = decrypt(value)
        return queryset.filter(
            Q(matricola_responsabile_scientifico__matricola=valueDecript)
            | Q(laboratoriopersonaletecnico__matricola_personale_tecnico__matricola=valueDecript)
            | Q(laboratoriopersonalericerca__matricola_personale_ricerca__matricola=valueDecript)
        ).distinct()

    def filter_scope(self, queryset, name, value):
        return queryset.filter(
            laboratorioattivita__tipologia_attivita__id=value
        ).distinct()

    
    def filter_erc1(self, queryset, name, value):
        erc1_allowed = value.split(",")
        query_erc1 = Q(
            laboratoriodatierc1__ricerca_erc1__cod_erc1__in=erc1_allowed
        )
        return queryset.filter(query_erc1)
    
    def filter_dip(self, queryset, name, value):
        query_dip = Q(dipartimento_riferimento__dip_cod__exact=value)
        query_dip |= Q(laboratorioaltridipartimenti__didattica_dipartimento__dip_cod=value)
                
        return queryset.filter(query_dip)

    def filter_search(self, queryset, name, value):
        language = self.request.query_params.get("language", "it")
        query_search = Q()
        if value:
            for k in value.split(" "):
                q_search = Q(nome_laboratorio__icontains=k)
                if language == "it":
                    q_search |= (
                        Q(finalita_ricerca_it__icontains=k)
                        | Q(finalita_didattica_it__icontains=k)
                        | Q(finalita_servizi_it__icontains=k)
                    )
                else:
                    q_search |= (
                        Q(finalita_ricerca_en__icontains=k)
                        | Q(finalita_didattica_en__icontains=k)
                        | Q(finalita_servizi_en__icontains=k)
                    )
                query_search &= q_search
                
        return queryset.filter(query_search)


    class Meta:
        model = LaboratorioDatiBase
        fields = []
