from django_filters import rest_framework as filters
from phd.models import (
    DidatticaDottoratoCds,
    DidatticaDottoratoAttivitaFormativa,
)
from django.db.models import Q

class PhdFilter(filters.FilterSet):
    cycle = filters.CharFilter(
        field_name="idesse3_ddr__num_ciclo",
        lookup_expr="exact",
        label="Cycle",
        help_text="Search for cycle of an educational activity.",
    )
    cdscod = filters.CharFilter(
        field_name="cds_cod",
        lookup_expr="exact",
        label="Cds code",
        help_text="Search for course of study code.",
    )
    departmentid = filters.NumberFilter(
        field_name="dip_cod__dip_id",
        lookup_expr="exact",
        label="Department ID",
        help_text="Search for department ID.",
    )
    pdscod = filters.CharFilter(
        field_name="idesse3_ddpds__pds_cod",
        lookup_expr="exact",
        label="Study plan code",
        help_text="Search for study plan code.",
    )
    regdid = filters.NumberFilter(
        field_name="idesse3_ddr__regdid_id_esse3",
        lookup_expr="exact",
        label="Didactic regulation",
        help_text="Search for didactic regulation ID.",
    )
    year = filters.NumberFilter(
        field_name="idesse3_ddr__aa_regdid_id",
        lookup_expr="exact",
        label="Year",
        help_text="Search for a specific year of erogation.",
    )
    yearFrom = filters.NumberFilter(
        field_name="idesse3_ddr__aa_regdid_id",
        lookup_expr="gte",
        label="Year From",
        help_text="Search for first year of erogation.",
    )
    yearTo = filters.NumberFilter(
        field_name="idesse3_ddr__aa_regdid_id",
        lookup_expr="lte",
        label="Year To",
        help_text="Search for last year of erogation.",
    )

    class Meta:
        model = DidatticaDottoratoCds
        fields = []


class PhdActivitiesFilter(filters.FilterSet):
    cycle = filters.CharFilter(
        field_name="ciclo",
        lookup_expr="exact",
        label="Cycle",
        help_text="Search for cycle of an educational activity.",
    )
    phd = filters.CharFilter(
        field_name="rif_dottorato",
        lookup_expr="icontains",
        label="PhD",
        help_text="Search for PhD reference.",
    )

    search = filters.CharFilter(
        field_name="nome_af",
        lookup_expr="icontains",
        label="Search",
        help_text="Search for educational activity name.",
    )
    structure = filters.CharFilter(
        field_name="struttura_proponente_origine",
        lookup_expr="icontains",
        label="Structure",
        help_text="Search for structure name.",
    )

    ssd = filters.CharFilter(
        field_name="ssd",
        lookup_expr="icontains",
        label="SSD",
        help_text="Search for SSD.",
    )

    typology = filters.NumberFilter(
        field_name="tipologia",
        lookup_expr="exact",
        label="Typology",
        help_text="Filter by typology ID.",
    )
    
    teacher = filters.CharFilter(
        method="filter_by_teacher_name",
        label="Teacher",
        help_text="Filter by teacher name."
        )

    def filter_by_teacher_name(self, queryset, name, value):
        return queryset.filter(
            Q(didatticadottoratoattivitaformativadocente__cognome_nome_origine__icontains=value)
            | Q(didatticadottoratoattivitaformativaaltridocenti__cognome_nome_origine__icontains=value)
        ).distinct()

    class Meta:
        model = DidatticaDottoratoAttivitaFormativa
        fields = []
