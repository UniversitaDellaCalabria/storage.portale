from django.conf import settings
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db import models
from rest_framework import viewsets, mixins
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
    CdsMorphSerializer,
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

@extend_schema(
        summary="List of all degree types",
        description="Retrieve a list of all available degree types with their codes and descriptions."
    )
class DegreeTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DegreeTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DegreeTypeFilter
    queryset = DidatticaCdsTipoCorso.objects.only("tipo_corso_cod", "tipo_corso_des").order_by("tipo_corso_des")


@extend_schema(
        summary="List of all academic years",
        description="Retrieve a list of all available academic years in descending order."
    )
class AcademicYearsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AcademicYearsSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaRegolamento.objects.only("aa_reg_did").order_by("-aa_reg_did")
            
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    queryset = DidatticaAttivitaFormativa.objects.all()

    @extend_schema(
        summary="List of all study activities",
        description=(
            "Retrieve a paginated list of all study activities with brief information. "
            "They can be filtered by academic year, course year, course code, department, "
            "SSD, teaching, teacher, and course year."
        ),
    )
    def list(self):
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
        
    @extend_schema(
        summary="Retrieve a specific study activity",
        description=(
            "Retrieve detailed information for a single study activity."
            "The study activity is identified by its ID."
        ),
    )
    def retrieve(self, request, *args, **kwargs):
            return DidatticaAttivitaFormativa.objects.select_related("matricola_resp_did").all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudyActivitiesDetailSerializer
        else:
            return StudyActivitiesListSerializer

@extend_schema(
    summary="List of all the CDS areas",
    description="Retrieve a list of all distinct Course of Study areas in Italian or in English."
)
class CdsAreasViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CdsAreasSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = (
        DidatticaCds.objects.values("area_cds", "area_cds_en")
        .filter(area_cds__isnull=False, area_cds_en__isnull=False)
        .distinct()
    )

@extend_schema(
    summary="List of expired courses",
    description=(
        "Retrieve a list of expired courses that are no longer active. "
        "This excludes courses that have been morphed into new ones."
    )
)
class CdsExpiredViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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

@extend_schema(
        summary="List all CDS morphing histories",
        description=(
            "Retrieve a list of all Course of Study morphing histories. "
            "This shows how the ids of the curses have evolved over time, tracking their "
            "previous versions."
        )
    )
class CdsMorphViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsMorphSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaCds.objects.all() 

    def list(self, request, *args, **kwargs):
        collegamenti_prefetch = DidatticaCdsCollegamento.objects.select_related('cds_prec')
        roots = DidatticaCdsCollegamento.objects.exclude(
            cds__pk__in=DidatticaCdsCollegamento.objects.values_list('cds_prec', flat=True)
        ).select_related('cds').prefetch_related(Prefetch('cds_prec', queryset=collegamenti_prefetch))
        
        previous_cds_cod_dict = {}
        for root in roots:
            previous_cds_cod_dict[root.cds.cds_cod] = self._build_cds_history(root.cds.cds_cod)

        return Response(previous_cds_cod_dict)
        
    def retrieve(self, request, *args, **kwargs):
        cds_cod = self.kwargs.get('pk')
        cds = DidatticaCds.objects.filter(cds_cod=cds_cod).order_by("-cds_id").first()
        
        previous_cds_cod_list = []
        if cds:  
            current_cds = cds
            while current_cds:
                collegamento = DidatticaCdsCollegamento.objects.filter(cds=current_cds).first()
                if collegamento:
                    predecessor = collegamento.cds_prec
                    previous_cds_cod_list.append(predecessor.cds_cod)
                    current_cds = predecessor
                else:
                    break

        return Response(previous_cds_cod_list)


    def _build_cds_history(self, cds_cod, history=None):
        if history is None:
            history = []

        prec = DidatticaCdsCollegamento.objects.filter(cds__cds_cod=cds_cod).select_related('cds_prec').first()
        if prec and prec.cds_prec:
            history.append(prec.cds_prec.cds_cod)
            self._build_cds_history(prec.cds_prec.cds_cod, history)
        return history


@extend_schema(
    summary="Academic Pathways Management",
    description=(
        "API endpoints for managing academic pathways. Provides functionality to list all "
        "academic pathways and retrieve detailed information about specific pathways, "
        "including their associated study activities."
    )
)
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
