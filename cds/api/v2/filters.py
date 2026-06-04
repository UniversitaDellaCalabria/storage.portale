from django.db.models import Exists, OuterRef, Q
from django_filters import rest_framework as filters
from generics.utils import decrypt

from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaAttivitaFormativaErogata,
    DidatticaAttivitaFormativaPds,
    DidatticaCdsLingua,
    DidatticaCdsTipoCorso,
    DidatticaCopertura,
    DidatticaRegolamento,
)


class CdsFilter(filters.FilterSet):
    name = filters.CharFilter(
        method="filter_name",
        label="Study course name",
        help_text="Name of the study course.",
    )
    academic_year = filters.NumberFilter(
        field_name="aa_reg_did",
        lookup_expr="exact",
        label="Academic year",
        help_text="Academic year",
    )
    department_cod = filters.CharFilter(
        field_name="cds__dip__dip_cod",
        lookup_expr="exact",
        label="Department code",
        help_text="Code of the departmental structure.",
    )
    department_id = filters.CharFilter(
        field_name="cds__dip__dip_id",
        lookup_expr="exact",
        label="Department unique ID",
        help_text="Unique ID of the departmental structure.",
    )
    department_name = filters.CharFilter(
        field_name="cds__dip__dip_des_it",
        lookup_expr="icontains",
        label="Department name",
        help_text="Name of the departmental structure.",
    )
    cds_cod = filters.CharFilter(
        field_name="cds__cds_cod",
        lookup_expr="exact",
        label="Cds code",
        help_text="Code of the course of study.",
    )
    course_type = filters.MultipleChoiceFilter(
        field_name="cds__tipo_corso_cod",
        choices=DidatticaCdsTipoCorso.objects.values_list(
            "tipo_corso_cod", "tipo_corso_des"
        ),
        label="Course type",
        help_text="Type of course of study.",
    )
    course_class_cod = filters.CharFilter(
        field_name="cds__cla_miur_cod",
        lookup_expr="icontains",
        label="Course class code",
        help_text="Code of the course of study class.",
    )
    course_class_name = filters.CharFilter(
        field_name="cds__cla_miur_des",
        lookup_expr="icontains",
        label="Course class name",
        help_text="Name of the course of study class.",
    )
    joint_degree = filters.MultipleChoiceFilter(
        field_name="titolo_congiunto_cod",
        choices=(("N", "No"), ("S", "Yes"), ("D", "Double")),
        label="Course type",
        help_text="Type of course of study.",
    )
    area = filters.CharFilter(
        method="filter_area",
        lookup_expr="exact",
        label="Area",
        help_text="Area of the course of study.",
    )
    language = filters.CharFilter(
        method="filter_language",
        label="Language",
        help_text="Language of the course of study.",
    )

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(cds__nome_cds_it__icontains=value) | Q(cds__nome_cds_eng__icontains=value)
        )

    def filter_area(self, queryset, name, value):
        return queryset.filter(
            Q(cds__area_cds__icontains=value) | Q(cds__area_cds_en__icontains=value)
        )

    def filter_language(self, queryset, name, value):
        return queryset.filter(
            Exists(
                DidatticaCdsLingua.objects.filter(
                    Q(lingua_des_it__icontains=value)
                    | Q(lingua_des_eng__icontains=value)
                    | Q(iso6392_cod__icontains=value),
                    cdsord=OuterRef("cds__cdsord_id"),
                )
            )
        )

    def filter_queryset(self, queryset):
        """
        Filter queryset based on the didactic regulation status
        if academic_year is not provided in the query params
        """
        queryset = super().filter_queryset(queryset)
        if not self.request.query_params.get("academic_year"):
            queryset = queryset.filter(stato_regdid_cod="A")
        return queryset

    class Meta:
        model = DidatticaRegolamento
        fields = []


class CdsExpiredFilter(filters.FilterSet):
    year_from = filters.NumberFilter(
        field_name="aa_reg_did",
        lookup_expr="gte",
        label="Year from",
        help_text="Academic year search lower bound (included)",
    )
    course_type = filters.MultipleChoiceFilter(
        field_name="cds__tipo_corso_cod",
        choices=DidatticaCdsTipoCorso.objects.values_list(
            "tipo_corso_cod", "tipo_corso_des"
        ),
        label="Course type",
        help_text="Type of course of study.",
    )

    class Meta:
        model = DidatticaRegolamento
        fields = []

class StudyActivitiesFilter(filters.FilterSet):
    name = filters.CharFilter(
        method="filter_name",
        label="Teaching name",
        help_text="Name of the study activity.",
    )
    academic_year = filters.NumberFilter(
        method="filter_academic_year",
        label="Academic Year",
        help_text="Academic year.",
    )
    course_year = filters.NumberFilter(
        method="filter_course_year",
        label="Course Year",
        help_text="Year of erogation of the course.",
    )
    cds_name = filters.CharFilter(
        method="filter_cds_name",
        label="Study course name",
        help_text="Name of the study course.",
    )
    cds_cod = filters.CharFilter(
        method="filter_cds_cod",
        label="Study course name",
        help_text="Name of the study course.",
    )
    department_cod = filters.CharFilter(
        method="department_cod",
        label="Department code",
        help_text="Code of the departmental structure.",
    )
    teacher_matricola = filters.CharFilter(
        method="filter_teacher_matricola",
        label="Teacher matricola",
        help_text="Encrypted teacher matricola.",
    )
    ssd = filters.CharFilter(
        method="filter_ssd",
        label="SSD",
        help_text="(Scientific Disciplinary Sector) SSD/SDS code.",
    )
    
    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(mod_off_id__ana_mod_desc_ita__icontains=value) |
            Q(mod_off_id__ana_mod_desc_ita__icontains=value) |
            Q(mod_off_id__af_off__ana_af_desc_ita__icontains=value) |
            Q(mod_off_id__af_off__ana_af_desc_ita__icontains=value)
        )
        
    def filter_academic_year(self, queryset, name, value):
        return queryset.filter(pds__aa_off_id=value).distinct()

    def filter_course_year(self, queryset, name, value):
        return queryset.filter(pds__anno_corso=value).distinct()

    def filter_cds_name(self, queryset, name, value):
        return queryset.filter(
            Q(mod_off_id__af_off__id_cds__nome_cds_it__icontains=value) |
            Q(mod_off_id__af_off__id_cds__nome_cds_eng__icontains=value)
        )

    def filter_cds_cod(self, queryset, name, value):
        return queryset.filter(
            mod_off_id__af_off__id_cds__cds_cod=value
        )

    def filter_department_cod(self, queryset, name, value):
        return queryset.filter(
            mod_off_id__af_off__id_cds__dip__dip_cod__iexact=value
        )

    def filter_teacher_last_name(self, queryset, name, value):
        return queryset.filter(
            mod_off_id__doc_resp_mod_id_ab__cognome__iexact=value
        )
        
    def filter_ssd(self, queryset, name, value):
        return queryset.filter(
            sett_cod__iexact=value
        )

    def filter_teacher_matricola(self, queryset, name, value):
        decrypted_matricola = decrypt(value)
        return queryset.filter(
            Exists(
                DidatticaCopertura.objects.filter(
                    Q(erog_id=OuterRef("erog_id")),
                    doc_matricola=decrypted_matricola,
                ).exclude(stato_coper_cod="R")
            )
        )

    class Meta:
        model = DidatticaAttivitaFormativaErogata
        fields = []
