from django.conf import settings
from django.db import models
from django.db.models import Case, Exists, F, OuterRef, Q, Subquery, Value, When
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from cds.models import (
    DidatticaAttivitaFormativa,
    DidatticaCds,
    DidatticaCdsCollegamento,
    DidatticaCdsTipoCorso,
    DidatticaCopertura,
    DidatticaPdsRegolamento,
    DidatticaRegolamento,
)

from .filters import (
    CdsExpiredFilter,
    CdsFilter,
    DegreeTypeFilter,
    StudyActivitiesFilter,
)
from .serializers import (
    AcademicPathwaysListSerializer,
    AcademicYearsSerializer,
    CdsAreasSerializer,
    CdsExpiredSerializer,
    CdsSerializer,
    DegreeTypeSerializer,
    StudyActivitiesDetailSerializer,
    StudyActivitiesListSerializer,
)


class CdsViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsFilter
    queryset = DidatticaCds.objects.all()


class DegreeTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = DegreeTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DegreeTypeFilter
    queryset = DidatticaCdsTipoCorso.objects.all()


class AcademicYearsViewSet(ReadOnlyModelViewSet):
    serializer_class = AcademicYearsSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        return (
            DidatticaRegolamento.objects.values("aa_reg_did")
            .distinct()
            .order_by("-aa_reg_did")
        )


class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    queryset = (
        DidatticaAttivitaFormativa.objects.select_related(
            "cds__dip", "matricola_resp_did"
        )
        .annotate(
            full_name=Case(
                When(
                    matricola_resp_did__cognome__isnull=True,
                    matricola_resp_did__nome__isnull=True,
                    matricola_resp_did__middle_name__isnull=True,
                    then=Value(""),
                ),
                default=Concat(
                    F("matricola_resp_did__cognome"),
                    Value(" "),
                    F("matricola_resp_did__nome"),
                    Case(
                        When(
                            matricola_resp_did__middle_name__isnull=False,
                            then=Concat(
                                Value(" "), F("matricola_resp_did__middle_name")
                            ),
                        ),
                        default=Value(""),
                        output_field=models.CharField(),
                    ),
                    output_field=models.CharField(),
                ),
            ),
            group_description=Concat(
                F("des"),
                Case(
                    When(
                        part_stu_des__isnull=False,
                        then=Concat(Value(" ("), F("part_stu_des"), Value(")")),
                    )
                ),
                output_field=models.CharField(),
            ),
            father=F("des"),
            af_gen_cod_fallback=Subquery(
                DidatticaCopertura.objects.filter(af_id=OuterRef("af_id")).values(
                    "af_gen_cod"
                )[:1]
            ),
            anno_corso_fallback=Subquery(
                DidatticaCopertura.objects.filter(af_id=OuterRef("af_id")).values(
                    "anno_corso"
                )[:1]
            ),
            ciclo_des_fallback=Subquery(
                DidatticaCopertura.objects.filter(af_id=OuterRef("af_id")).values(
                    "ciclo_des"
                )[:1]
            ),
        )
        .annotate(
            af_gen_cod_final=Case(
                When(af_gen_cod__isnull=True, then=F("af_gen_cod_fallback")),
                default=F("af_gen_cod"),
                output_field=models.CharField(),
            ),
            anno_corso_final=Case(
                When(anno_corso__isnull=True, then=F("anno_corso_fallback")),
                default=F("anno_corso"),
                output_field=models.IntegerField(),
            ),
            ciclo_des_final=Case(
                When(ciclo_des__isnull=True, then=F("ciclo_des_fallback")),
                default=F("ciclo_des"),
                output_field=models.CharField(),
            ),
        )
        .filter(
            Q(
                af_id__in=Subquery(
                    DidatticaCopertura.objects.filter(
                        ~Q(stato_coper_cod="R") | Q(stato_coper_cod__isnull=True)
                    ).values("af_id")
                )
            )
            | Q(
                af_master_id__in=Subquery(
                    DidatticaCopertura.objects.filter(
                        ~Q(stato_coper_cod="R") | Q(stato_coper_cod__isnull=True)
                    ).values("af_id")
                )
            )
        )
        .distinct()
        .order_by("des")
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudyActivitiesDetailSerializer
        else:
            return StudyActivitiesListSerializer


class CdsAreasViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsAreasSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = (
        DidatticaCds.objects.values("area_cds", "area_cds_en")
        .filter(area_cds__isnull=False, area_cds_en__isnull=False)
        .distinct()
    )

    def get(self, request, *args, **kwargs):
        lang = request.LANGUAGE_CODE
        self.language = request.query_params.get("lang", lang).lower()

        cache_key = "cdsareas"
        kwargs["cache_key"] = cache_key

        return super().get(request, *args, **kwargs)


class CdsExpiredViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsExpiredSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsExpiredFilter

    def get_queryset(self):
        cds_morphed = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec__cds_cod", flat=True
        )

        regdids = (
            DidatticaRegolamento.objects.select_related("cds")
            .filter(
                ~Exists(
                    DidatticaRegolamento.objects.filter(
                        cds=OuterRef("cds"),
                        aa_reg_did__gt=OuterRef("aa_reg_did"),
                    ).exclude(stato_regdid_cod="R")
                ),
                aa_reg_did__lt=settings.CURRENT_YEAR,
            )
            .exclude(stato_regdid_cod="R")
            .exclude(aa_reg_did__lte=(settings.CURRENT_YEAR - F("cds__durata_anni")))
            .exclude(cds__cds_cod__in=cds_morphed)
            .values("aa_reg_did", "cds__cds_cod", "cds__durata_anni")
        )

        return regdids


class AcademicPathsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = AcademicPathwaysListSerializer

    def get_queryset(self):
        attivita_formativa_qs = DidatticaAttivitaFormativa.objects.filter(
            regdid=self.kwargs.get("regdid_id"), pds_regdid=OuterRef("pds_regdid_id")
        ).select_related("regdid__cds")
        return (
            DidatticaPdsRegolamento.objects.filter(Exists(attivita_formativa_qs))
            .annotate(
                duration=Subquery(
                    attivita_formativa_qs.values("regdid__cds__durata_anni")[:1]
                )
            )
            .only("pds_regdid_id", "pds_cod", "regdid", "pds_des_it")
            .order_by("pds_des_it")
        )
