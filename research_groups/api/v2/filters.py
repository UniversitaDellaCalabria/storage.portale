from django.db.models import Q
from django_filters import rest_framework as filters
from generics.utils import decrypt
from research_groups.models import RicercaGruppo

class ResearchGroupsFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for research groups.",
    )
    cod = filters.CharFilter(
        method="filter_cod",
        label="ERC code(s)",
        help_text="ERC codes (comma-separated).",
    )

    teacher = filters.CharFilter(
        method="filter_teacher_department",
        label="Teacher matricola",
        help_text="Matricola del docente (encrypted).",
    )

    department = filters.CharFilter(
        method="filter_teacher_department",
        label="Department code",
        help_text="Codice del dipartimento (sede del docente).",
    )
    
    def filter_cod(self, queryset, name, value):
        if value:
            cod_list = [v.strip() for v in value.split(",") if v.strip()]
            if cod_list:
                return queryset.filter(ricerca_erc1__cod_erc1__in=cod_list)
        return queryset


    def filter_search(self, queryset, name, value):
        query_search = Q()
        if value:
            for k in value.split(" "):
                query_search &= (
                    Q(nome__icontains=k)
                    | Q(descrizione__icontains=k)
                    | Q(ricerca_erc1__descrizione__icontains=k)
                    | Q(ricercadocentegruppo__personale__cognome__istartswith=k)
                )
        return queryset.filter(query_search).distinct()

    def filter_teacher_department(self, queryset, name, value):
        teacher = self.data.get("teacher")
        department = self.data.get("department")

        if teacher:
            try:
                teacher = decrypt(teacher)
            except Exception:
                teacher = None

        query = Q()
        if teacher and department:
            query = Q(
                ricercadocentegruppo__personale__matricola=teacher,
                ricercadocentegruppo__personale__sede=department,
            )
        elif teacher:
            query = Q(ricercadocentegruppo__personale__matricola=teacher)
        elif department:
            query = Q(ricercadocentegruppo__personale__sede=department)

        return queryset.filter(query).distinct()

    class Meta:
        model = RicercaGruppo
        fields = []
