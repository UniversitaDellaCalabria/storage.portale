from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    APIException,
    PermissionDenied,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)
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
    DidatticaCdsAltriDati,
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
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        ordinamento_subquery = (
            DidatticaCdsAltriDati.objects.filter(
                regdid__cds=OuterRef("cds"), ordinamento_didattico__isnull=False
            )
            .order_by("-regdid")
            .values("ordinamento_didattico")[:1]
        )
        return (
            DidatticaRegolamento.objects.select_related(
                "cds__dip", "didatticacdsaltridati"
            )
            .prefetch_related(Prefetch("cds__didatticacdslingua", to_attr="lingue"))
            .only(
                "regdid_id",
                "cds__cds_id",
                "cds__cds_cod",
                "aa_reg_did",
                "cds__nome_cds_it",
                "cds__area_cds",
                "cds__dip__dip_id",
                "cds__dip__dip_cod",
                "cds__dip__dip_des_it",
                "cds__tipo_corso_cod",
                "cds__tipo_corso_des",
                "cds__cla_miur_cod",
                "cds__cla_miur_des",
                "cds__intercla_miur_cod",
                "cds__intercla_miur_des",
                "modalita_erogazione",
                "frequenza_obbligatoria",
                "cds__durata_anni",
                "cds__valore_min",
                "stato_regdid_cod",
                "titolo_congiunto_cod",
                "cds__aa_ord_id",
                "cds__cdsord_id",
                "didatticacdsaltridati__manifesto_studi",
                "didatticacdsaltridati__regolamento_didattico",
            )
            .annotate(ordinamento_didattico=Subquery(ordinamento_subquery))
            .filter(stato_regdid_cod="A")
            .order_by("-regdid_id")
        )


@extend_schema(
    summary="List of all degree types",
    description="Retrieve a list of all available degree types with their codes and descriptions.",
    responses={
        200: OpenApiResponse(
            response=DegreeTypeSerializer(many=True),
            description="Success: List of degree types",
        ),
        403: OpenApiResponse(
            response=PermissionDenied,
            description="Forbidden",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value={"detail": "Forbidden", "code": 403},
                )
            ],
        ),
    },
)
class DegreeTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DegreeTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DegreeTypeFilter
    queryset = DidatticaCdsTipoCorso.objects.only(
        "tipo_corso_cod", "tipo_corso_des"
    ).order_by("tipo_corso_des")


@extend_schema(
    summary="List of all academic years",
    description="Retrieve a list of all available academic years in descending order.",
    responses={
        200: OpenApiResponse(
            response=AcademicYearsSerializer(many=True),
            description="Success: List of academic years",
        ),
        403: OpenApiResponse(
            response=PermissionDenied,
            description="Forbidden",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value={"detail": "Forbidden", "code": 403},
                )
            ],
        ),
    },
)
class AcademicYearsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AcademicYearsSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaRegolamento.objects.only("aa_reg_did").order_by("-aa_reg_did")


@extend_schema_view(
    list=extend_schema(
        summary="List of all study activities",
        description=(
            "Retrieve a paginated list of all study activities with brief information. "
            "They can be filtered by academic year, course year, course code, department, "
            "SSD, teaching, teacher, and course year."
        ),
        responses={
            200: OpenApiResponse(
                response=StudyActivitiesListSerializer(many=True),
                description="Success: List of study activities",
            ),
            403: OpenApiResponse(
                response=PermissionDenied,
                description="Forbidden: Access denied",
                examples=[
                    OpenApiExample(
                        "Forbidden", value={"detail": "Forbidden", "code": 403}
                    )
                ],
            ),
            500: OpenApiResponse(
                response=APIException,
                description="Server Error: Internal issue",
                examples=[
                    OpenApiExample(
                        "Server Error",
                        value={"detail": "Error: Internal Server Error", "code": 500},
                    )
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific study activity",
        description=(
            "Retrieve detailed information for a single study activity. "
            "The study activity is identified by its ID."
        ),
        responses={
            200: OpenApiResponse(
                response=StudyActivitiesDetailSerializer,
                description="Success: Detailed study activity information",
            ),
            403: OpenApiResponse(
                response=PermissionDenied,
                description="Forbidden: Access denied",
                examples=[
                    OpenApiExample(
                        "Forbidden", value={"detail": "Forbidden", "code": 403}
                    )
                ],
            ),
            404: OpenApiResponse(
                response=NotFound,
                description="Not Found: Study activity does not exist",
                examples=[
                    OpenApiExample(
                        "Not Found",
                        value={"detail": "Study activity not found", "code": 404},
                    )
                ],
            ),
            500: OpenApiResponse(
                response=APIException,
                description="Server Error: Internal issue",
                examples=[
                    OpenApiExample(
                        "Server Error",
                        value={"detail": "Error: Internal Server Error", "code": 500},
                    )
                ],
            ),
        },
    ),
)
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter
    queryset = DidatticaAttivitaFormativa.objects.all()

    def get_queryset(self):
        try:
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
                                            Value(" "),
                                            F("matricola_resp_did__middle_name"),
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
                                    then=Concat(
                                        Value(" ("), F("part_stu_des"), Value(")")
                                    ),
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

        except DidatticaAttivitaFormativa.DoesNotExist:
            raise NotFound(
                detail="The requested study activity does not exist.", code=404
            )
        except ValueError as e:
            raise ValidationError(detail=str(e), code=400)
        except PermissionError as e:
            raise PermissionDenied(detail=str(e), code=403)

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return StudyActivitiesDetailSerializer
            elif self.action == "list":
                return StudyActivitiesListSerializer
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )


@extend_schema(
    summary="List of all the CDS areas",
    description="Retrieve a list of all distinct Course of Study areas in Italian or in English.",
    responses={
        200: OpenApiResponse(
            response=CdsAreasSerializer(many=True),
            description="Success: List of CDS areas",
        ),
    },
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
    ),
    responses={
        200: OpenApiResponse(
            response=CdsExpiredSerializer(many=True),
            description="Success: List of expired courses",
        ),
        404: OpenApiResponse(
            response=NotFound,
            description="Not Found: No expired courses found",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "No expired courses found", "code": 404},
                )
            ],
        ),
        400: OpenApiResponse(
            response=ValidationError,
            description="Bad Request: Invalid request",
            examples=[
                OpenApiExample(
                    "Bad Request",
                    value={"detail": "Invalid request", "code": 400},
                )
            ],
        ),
        403: OpenApiResponse(
            response=PermissionDenied,
            description="Forbidden: Access denied",
            examples=[
                OpenApiExample(
                    "Forbidden",
                    value={"detail": "Forbidden", "code": 403},
                )
            ],
        ),
        500: OpenApiResponse(
            response=APIException,
            description="Server Error: Internal issue",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "Error: Internal Server Error", "code": 500},
                )
            ],
        ),
    },
)
class CdsExpiredViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CdsExpiredSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsExpiredFilter
    queryset = DidatticaRegolamento.objects.all()

    def get_queryset(self):
        try:
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
                    cds__isnull=False,
                )
                .exclude(stato_regdid_cod="R")
                .exclude(
                    aa_reg_did__lte=(settings.CURRENT_YEAR - F("cds__durata_anni"))
                )
                .exclude(cds__cds_cod__in=cds_morphed)
            )

            return regdids
        except DidatticaRegolamento.DoesNotExist:
            raise NotFound(detail="No expired courses found.", code=404)
        except ValueError as e:
            raise ValidationError(detail=str(e), code=400)
        except PermissionError as e:
            raise PermissionDenied(detail=str(e), code=403)
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )


@extend_schema(
    summary="List all CDS morphing histories",
    description=(
        "Retrieve a list of all Course of Study morphing histories. "
        "This shows how the ids of the curses have evolved over time, tracking their "
        "previous versions."
    ),
    responses={
        200: OpenApiResponse(
            response=CdsMorphSerializer(many=True),
            description="Success: List of morphing histories",
        ),
        404: OpenApiResponse(
            response=NotFound,
            description="Not Found: Course of Study not found",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "Course of Study not found", "code": 404},
                )
            ],
        ),
        500: OpenApiResponse(
            response=APIException,
            description="Server Error: Internal issue",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "Error: Internal Server Error", "code": 500},
                )
            ],
        ),
    },
)
class CdsMorphViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsMorphSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaCds.objects.all()

    def get_queryset(self, request, *args, **kwargs):
        if self.action == "list":
            try:
                collegamenti_prefetch = DidatticaCdsCollegamento.objects.select_related(
                    "cds_prec"
                )
                roots = (
                    DidatticaCdsCollegamento.objects.exclude(
                        cds__pk__in=DidatticaCdsCollegamento.objects.values_list(
                            "cds_prec", flat=True
                        )
                    )
                    .select_related("cds")
                    .prefetch_related(
                        Prefetch("cds_prec", queryset=collegamenti_prefetch)
                    )
                )

                previous_cds_cod_dict = {}
                for root in roots:
                    previous_cds_cod_dict[root.cds.cds_cod] = self._build_cds_history(
                        root.cds.cds_cod
                    )

                return Response(previous_cds_cod_dict)
            except DidatticaCds.DoesNotExist:
                raise NotFound(detail="No morphing histories found.", code=404)
            except Exception as e:
                raise APIException(
                    detail=f"An unexpected error occurred: {str(e)}", code=500
                )

        elif self.action == "retrieve":
            try:
                cds_cod = self.kwargs.get("pk")
                cds = (
                    DidatticaCds.objects.filter(cds_cod=cds_cod)
                    .order_by("-cds_id")
                    .first()
                )

                previous_cds_cod_list = []
                if cds:
                    current_cds = cds
                    while current_cds:
                        collegamento = DidatticaCdsCollegamento.objects.filter(
                            cds=current_cds
                        ).first()
                        if collegamento:
                            predecessor = collegamento.cds_prec
                            previous_cds_cod_list.append(predecessor.cds_cod)
                            current_cds = predecessor
                        else:
                            break

                return Response(previous_cds_cod_list)
            except DidatticaCds.DoesNotExist:
                raise NotFound(
                    detail="The requested morphing history does not exist.", code=404
                )
            except Exception as e:
                raise APIException(
                    detail=f"An unexpected error occurred: {str(e)}", code=500
                )

    def _build_cds_history(self, cds_cod, history=None):
        if history is None:
            history = []

        prec = (
            DidatticaCdsCollegamento.objects.filter(cds__cds_cod=cds_cod)
            .select_related("cds_prec")
            .first()
        )
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
    ),
    responses={
        200: OpenApiResponse(
            response=AcademicPathwaysListSerializer(many=True),
            description="Success: List of academic pathways",
        ),
        500: OpenApiResponse(
            response=APIException,
            description="Server Error: Internal issue",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "Error: Internal Server Error", "code": 500},
                )
            ],
        ),
    },
)
class AcademicPathsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    queryset = DidatticaPdsRegolamento.objects.all()
    lookup_field = "pds_regdid_id"

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return AcademicPathwaysDetailSerializer
            else:
                return AcademicPathwaysListSerializer
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )

    def get_queryset(self):
        try:
            if self.action == "list":
                attivita_formativa_qs = DidatticaAttivitaFormativa.objects.filter(
                    regdid=self.kwargs.get("regdid_id"),
                    pds_regdid=OuterRef("pds_regdid_id"),
                ).select_related("regdid__cds")
                return (
                    DidatticaPdsRegolamento.objects.filter(
                        Exists(attivita_formativa_qs)
                    )
                    .annotate(
                        duration=Subquery(
                            attivita_formativa_qs.values("regdid__cds__durata_anni")[:1]
                        )
                    )
                    .only("pds_regdid_id", "pds_cod", "regdid", "pds_des_it")
                    .order_by("pds_des_it")
                )
            elif self.action == "retrieve":
                return (DidatticaPdsRegolamento.objects).prefetch_related(
                    Prefetch(
                        "didatticaattivitaformativa_set",
                        queryset=DidatticaAttivitaFormativa.objects.filter(
                            af_id=F("af_radice_id")
                        ),
                    )
                )
        except DidatticaPdsRegolamento.DoesNotExist:
            raise NotFound(
                detail="The requested academic pathway does not exist.", code=404
            )
        except ValueError as e:
            raise ValidationError(detail=str(e), code=400)
        except PermissionError as e:
            raise PermissionDenied(detail=str(e), code=403)
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )
