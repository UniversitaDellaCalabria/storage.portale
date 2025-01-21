from django_filters import rest_framework as filters
from django.db.models import Q

from cds.models import (
    DidatticaCds, 
    DidatticaCdsTipoCorso, 
    DidatticaAttivitaFormativa, 
    DidatticaCopertura,
    DidatticaRegolamento
)


class CdsFilter(filters.FilterSet):
    nome_cds_it = filters.CharFilter(
        field_name="cds__nome_cds_it",
        lookup_expr="icontains",
        label="Nome Cds",
        help_text="Filtra per nome del Cds.",
    )
    academic_year = filters.CharFilter(
        field_name="aa_reg_did",
        lookup_expr="exact",
        label="Academic Year",
        help_text="Filter by academic year",
    )

    class Meta:
        model = DidatticaRegolamento
        fields = []
        

class CdsExpiredFilter(filters.FilterSet):
    yearfrom = filters.NumberFilter(
        field_name='aa_reg_did', 
        lookup_expr='gte', 
        label='Year From')
    
    coursetypes = filters.CharFilter(
        field_name='cds__tipo_corso_cod', 
        lookup_expr='in', 
        label='Course Types')

    class Meta:
        model = DidatticaRegolamento
        fields = []

 


class DegreeTypeFilter(filters.FilterSet):
    class Meta:
        model = DidatticaCdsTipoCorso
        fields = []
        


class StudyActivitiesFilter(filters.FilterSet):
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
        label="Teaching Name",
        help_text="Filter by teaching name..",
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
    
    coperture = filters.CharFilter(
        method="filter_by_teacher_code",
        label="Teacher Code",
        help_text="Filter activities based on teacher coverage using the teacher code."
    )
    def filter_by_teacher_code(self, queryset, name, value):
        coperture = DidatticaCopertura.objects.filter(matricola_resp_did=value).exclude(stato_coper_cod="R").values("af_id")
        return queryset.filter(Q(af_id__in=coperture) | Q(af_master_id__in=coperture))
    


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

