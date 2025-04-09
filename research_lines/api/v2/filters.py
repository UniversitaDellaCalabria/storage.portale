from django.db.models import Q
from django_filters import rest_framework as filters
from generics.utils import decrypt
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)

class BaseResearchLinesFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search for research groups.",
    )
    
    year = filters.CharFilter(
        field_name="anno",
        lookup_expr="exact",
        label="Year",
        help_text="Year of the research group.",
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

    def filter_search(self, queryset, name, value):
        query_search = Q()
        if value:
            for k in value.split(" "):
                q_descrizione = Q(descrizione__icontains=k)
                query_search &= q_descrizione
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
                ricercadocentelineabase__personale__matricola=teacher,
                ricercadocentelineabase__personale__sede=department,
            )
        elif teacher:
            query = Q(ricercadocentelineabase__personale__matricola=teacher)
        elif department:
            query = Q(ricercadocentelineabase__personale__sede=department)

        return queryset.filter(query).distinct()

    class Meta:
        model = RicercaLineaBase
        fields = []
