from django_filters import rest_framework as filters
from django.db.models import Q

from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa


class CdsFilter(filters.FilterSet):
    nome_cds_it = filters.CharFilter(
        field_name="nome_cds_it",
        lookup_expr="icontains",
        label="Nome Cds",
        help_text="Filtra per nome del Cds.",
        # example="test"
    )

    class Meta:
        model = DidatticaCds
        fields = []


class DegreeTypeFilter(filters.FilterSet):
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = []
        


class DidatticaAttivitaFormativaFilter(filters.FilterSet):
    academic_year = filters.NumberFilter(
        field_name="aa_off_id",
        lookup_expr="iexact",
        label="Academic Year",
        help_text="Filter by academic year.",
    )
    course_year = filters.NumberFilter(
        field_name="anno_corso",
        lookup_expr="iexact",
        label="Course Year",
        help_text="Filter by course year.",
    )
    department = filters.CharFilter(
        field_name="cds_id__dip_id__dip_cod",
        lookup_expr="icontains",
        label="Department Code",
        help_text="Filter by department code.",
    )
    cds = filters.CharFilter(
        method="filter_cds",
        label="Cds name",
        help_text="Filter by Cds name.",
    )
    teacher = filters.CharFilter(
        field_name="matricola_resp_did__cognome",
        lookup_expr="istartswith",
        label="Teacher",
        help_text="Filter by teacher's last name.",
    )
    teaching = filters.CharFilter(
        field_name="des",
        lookup_expr="icontains",
        label="IT Teaching Name",
        help_text="Filter by teaching name in Italian.",
    )
    ssd = filters.CharFilter(
        method="filter_ssd",
        label="Sett Cod",
        help_text="Filter by SSD codes.",
    )
    period = filters.CharFilter(
        field_name="ciclo_des",
        lookup_expr="icontains",
        label="Ciclo Des",
        help_text="Filter by cycle des.",
    )
    cds_cod = filters.CharFilter(
        field_name="cds_id__cds_cod",
        lookup_expr="iexact",
        label="Cds Code",
        help_text="Filter by Cds code.",
    )
    teacher_code = filters.CharFilter(
        field_name="matricola_resp_did",
        lookup_expr="exact",
        label="Teacher Code",
        help_text="Filter by teacher code.",
    )
    '''
    father = filters.CharFilter(
        field_name="af_radice_id",
        lookup_expr="iexact",
        label="Father ID",
        help_text="Filter by father activity ID.",
    )
    '''

    def filter_cds(self, queryset, name, value):
        return queryset.filter(
            Q(cds_id__nome_cds_it__icontains=value) |
            Q(cds_id__nome_cds_eng__icontains=value)
        )
    def filter_teaching(self, queryset, name, value):
        return queryset.filter(
            Q(des__icontains=value) |
            Q(af_gen_des_eng__icontains=value)
        )
    def filter_ssd(self, queryset, name, value):
        ssd_filters = Q()
        for k in value.split(" "):
            ssd_filters |= Q(sett_cod__icontains=k)
        return queryset.filter(ssd_filters)

        

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = []

