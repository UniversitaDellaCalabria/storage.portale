from django.conf import settings
from django.db import models
from django.db.models import (
    Case,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce, Concat
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
    AcademicPathwaysDetailSerializer,
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
    queryset = DidatticaCdsTipoCorso.objects.only("tipo_corso_cod", "tipo_corso_des").order_by("tipo_corso_des")


class AcademicYearsViewSet(ReadOnlyModelViewSet):
    serializer_class = AcademicYearsSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaRegolamento.objects.only("aa_reg_did").order_by("-aa_reg_did")
            
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    queryset = DidatticaAttivitaFormativa.objects.all()

    def get_queryset(self):
        if self.action == "list":
            coperture_qs = DidatticaCopertura.objects.filter(
                af_id=OuterRef("af_id")
            ).values("af_gen_cod", "anno_corso", "ciclo_des")[:1]

            return (
                DidatticaAttivitaFormativa.objects.select_related(
                    "cds__dip", "matricola_resp_did"
                )
                .only(
                    "af_id",
                    "af_gen_cod",
                    "af_gen_des_eng",
                    "cds_id",
                    "cds__cds_cod",
                    "des",
                    "lista_lin_did_af",
                    "af_radice_id",
                    "regdid_id",
                    "cds__dip__dip_des_it",
                    "cds__dip__dip_des_eng",
                    "cds__dip__dip_cod",
                    "anno_corso",
                    "aa_off_id",
                    "ciclo_des",
                    "sett_cod",
                    "sett_des",
                    "part_stu_cod",
                    "part_stu_des",
                    "fat_part_stu_cod",
                    "fat_part_stu_des",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                    "matricola_resp_did__matricola",
                    "matricola_resp_did__cognome",
                    "matricola_resp_did__nome",
                    "matricola_resp_did__middle_name",
                    "pds_des",
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
                    fatherName=F("des"),
                    af_gen_cod_final=Coalesce(
                        F("af_gen_cod"),
                        Subquery(coperture_qs.values("af_gen_cod")),
                        output_field=models.CharField(),
                    ),
                    anno_corso_final=Coalesce(
                        F("anno_corso"),
                        Subquery(coperture_qs.values("anno_corso")),
                        output_field=models.IntegerField(),
                    ),
                    ciclo_des_final=Coalesce(
                        F("ciclo_des"),
                        Subquery(coperture_qs.values("ciclo_des")),
                        output_field=models.CharField(),
                    ),
                )
                .filter(
                    Q(
                        af_id__in=Subquery(
                            DidatticaCopertura.objects.filter(
                                ~Q(stato_coper_cod="R")
                                | Q(stato_coper_cod__isnull=True)
                            ).values("af_id")
                        )
                    )
                    | Q(
                        af_master_id__in=Subquery(
                            DidatticaCopertura.objects.filter(
                                ~Q(stato_coper_cod="R")
                                | Q(stato_coper_cod__isnull=True)
                            ).values("af_id")
                        )
                    )
                )
                .order_by("des")
            )
        elif self.action == "retrieve":
            return DidatticaAttivitaFormativa.objects.select_related(
                "matricola_resp_did"
            ).all()

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


class CdsExpiredViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsExpiredSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsExpiredFilter

    def get_queryset(self):
        cds_morphed = DidatticaCdsCollegamento.objects.values_list(
            "cds_prec__cds_cod", flat=True
        )

        regdids = (
            DidatticaRegolamento.objects.filter(
                ~Exists(
                    DidatticaRegolamento.objects.filter(
                        cds=OuterRef("cds"),
                        aa_reg_did__gt=OuterRef("aa_reg_did"),
                    ).exclude(stato_regdid_cod="R")
                ),
                aa_reg_did__lt=settings.CURRENT_YEAR,
                cds__isnull=False
            )
            .exclude(stato_regdid_cod="R")
            .exclude(aa_reg_did__lte=(settings.CURRENT_YEAR - F("cds__durata_anni")))
            .exclude(cds__cds_cod__in=cds_morphed)
        )

        return regdids


class AcademicPathsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    queryset = DidatticaPdsRegolamento.objects.all()
    lookup_field = "pds_regdid_id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AcademicPathwaysDetailSerializer
        else:
            return AcademicPathwaysListSerializer

    def get_queryset(self):
        if self.action == "list":
            attivita_formativa_qs = DidatticaAttivitaFormativa.objects.filter(
                regdid=self.kwargs.get("regdid_id"),
                pds_regdid=OuterRef("pds_regdid_id"),
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
        elif self.action == "retrieve":
            return (
                DidatticaPdsRegolamento.objects
            ).prefetch_related(
                Prefetch(
                    "didatticaattivitaformativa_set",
                    queryset=DidatticaAttivitaFormativa.objects.filter(
                        af_id=F("af_radice_id")
                    ),
                )
            )
