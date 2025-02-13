from django.db.models import Exists, OuterRef, Q
from django_filters import rest_framework as filters
from generics.utils import decrypt

from cds.models import (
    DidatticaAttivitaFormativa,
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
    cds_name = filters.CharFilter(
        method="filter_cds_name",
        label="Study course name",
        help_text="Name of the study course.",
    )
    academic_year = filters.NumberFilter(
        field_name="aa_off_id",
        lookup_expr="iexact",
        label="Academic Year",
        help_text="Academic year.",
    )
    course_year = filters.NumberFilter(
        field_name="anno_corso",
        lookup_expr="iexact",
        label="Course Year",
        help_text="Year of erogation of the course.",
    )
    cds_cod = filters.CharFilter(
        field_name="cds__cds_cod",
        lookup_expr="exact",
        label="Cds code",
        help_text="Code of the course of study.",
    )
    department_cod = filters.CharFilter(
        field_name="cds__dip__dip_cod",
        lookup_expr="exact",
        label="Department code",
        help_text="Code of the departmental structure.",
    )
    teacher_last_name = filters.CharFilter(
        field_name="matricola_resp_did__cognome",
        lookup_expr="icontains",
        label="Teacher last name",
        help_text="Teacher's last name.",
    )
    ssd = filters.CharFilter(
        field_name="sett_cod",
        lookup_expr="icontains",
        label="SSD",
        help_text="(Scientific Disciplinary Sector) SSD/SDS code.",
    )
    cycle = filters.CharFilter(
        method="filter_cycle",
        label="Cycle",
        help_text="Activity cycle.",
    )
    teacher_matricola = filters.CharFilter(
        method="filter_teacher_matricola",
        label="Teacher matricola",
        help_text="Encrypted teacher matricola.",
    )

    def filter_teacher_matricola(self, queryset, name, value):
        decrypted_matricola = decrypt(value)
        return queryset.filter(
            Exists(
                DidatticaCopertura.objects.filter(
                    Q(af_id=OuterRef("af_id")) | Q(af_id=OuterRef("af_master_id")),
                    matricola_resp_did=decrypted_matricola,
                ).exclude(stato_coper_cod="R")
            )
        )

    def filter_cycle(self, queryset, name, value):
        return queryset.filter(
            Q(tipo_ciclo_cod__icontains=value)
            | Q(des_tipo_ciclo__icontains=value)
            | Q(ciclo_des__icontains=value)
        )

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(des__icontains=value) | Q(af_gen_des_eng__icontains=value)
        )

    def filter_cds_name(self, queryset, name, value):
        return queryset.filter(
            Q(cds__nome_cds_it__icontains=value) | Q(cds__nome_cds_eng__icontains=value)
        )

    class Meta:
        model = DidatticaAttivitaFormativa
        fields = []
