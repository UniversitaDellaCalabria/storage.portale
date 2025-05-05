from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

from .filters import BaseResearchLinesFilter, AppliedResearchLinesFilter

from .serializers import BaseResearchLinesSerializer, AppliedResearchLinessSerializer
from django.db.models import Prefetch, Q
from research_lines.models import (
    RicercaDocenteLineaApplicata,
    RicercaDocenteLineaBase,
    RicercaLineaApplicata,
    RicercaLineaBase,
)
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.BASE_RESEARCH_LINES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(
            BaseResearchLinesSerializer(many=True)
        ),
    ),
)
class BaseResearchLinesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = BaseResearchLinesSerializer
    filterset_class = BaseResearchLinesFilter

    def get_queryset(self):
        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        if self.request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        query_is_active = Q(visibile=True) if only_active else Q()

        return (
            RicercaLineaBase.objects.filter(query_is_active)
            .order_by("descrizione")
            .prefetch_related(
                Prefetch(
                    "ricercadocentelineabase_set",
                    queryset=RicercaDocenteLineaBase.objects.select_related(
                        "personale"
                    ).only(
                        "personale__matricola",
                        "personale__cognome",
                        "personale__nome",
                        "personale__middle_name",
                        "personale__sede",
                        "personale__ds_sede",
                    ),
                )
            )
            .select_related("ricerca_erc2")
            .only(
                "id",
                "descrizione",
                "descr_pubblicaz_prog_brevetto",
                "anno",
                "ricerca_erc2_id__cod_erc2",
                "ricerca_erc2_id__descrizione",
                "visibile",
            )
            .distinct()
        )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.APPLIED_RESEARCH_LINES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(
            AppliedResearchLinessSerializer(many=True)
        ),
    ),
)
class AppliedResearchLinesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AppliedResearchLinessSerializer
    filterset_class = AppliedResearchLinesFilter

    def get_queryset(self):
        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        if self.request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        query_is_active = Q(visibile=True) if only_active else Q()

        return (
            RicercaLineaApplicata.objects.filter(query_is_active)
            .order_by("descrizione")
            .prefetch_related(
                Prefetch(
                    "ricercadocentelineaapplicata_set",
                    queryset=RicercaDocenteLineaApplicata.objects.select_related(
                        "personale"
                    ).only(
                        "personale__matricola",
                        "personale__cognome",
                        "personale__nome",
                        "personale__middle_name",
                        "personale__sede",
                        "personale__ds_sede",
                    ),
                )
            )
            .select_related("ricerca_aster2")
            .only(
                "id",
                "descrizione",
                "descr_pubblicaz_prog_brevetto",
                "anno",
                "ricerca_aster2_id__ricerca_aster1_id",
                "ricerca_aster2_id__descrizione",
                "visibile",
            )
            .distinct()
        )
