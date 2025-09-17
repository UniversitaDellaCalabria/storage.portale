from django_filters.rest_framework import DjangoFilterBackend
from projects.settings import OFFICE_PROJECTS
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

from .serializers import (
    ProjectsSerializer,
    TerritorialScopesSerializer,
    ProgramTypesSerializer,
    InfrastructuresSerializer,
)
from .filters import ProjectsFilter
from projects.models import (
    ProgettoAmbitoTerritoriale,
    ProgettoDatiBase,
    ProgettoResponsabileScientifico,
    ProgettoRicercatore,
    ProgettoTipologiaProgramma,
)
from django.db.models import Q, Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PROJECTS_LIST_SUMMARY,
        description=descriptions.PROJECTS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(ProjectsSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.PROJECTS_RETRIEVE_SUMMARY,
        description=descriptions.PROJECTS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(ProjectsSerializer),
    ),
)
class ProjectsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectsFilter
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        request = self.request
        only_active = True
        if request.user.is_superuser:
            only_active = False
        if request.user.is_authenticated:
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_PROJECTS,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        query = (
            ProgettoDatiBase.objects.filter(Q(is_active=True) if only_active else Q())
            .select_related(
                "tipologia_programma", "ambito_territoriale", "uo", "area_tecnologica"
            )
            .prefetch_related(
                Prefetch(
                    "progettoresponsabilescientifico_set",
                    queryset=ProgettoResponsabileScientifico.objects.only(
                        "matricola", "nome_origine"
                    ),
                    to_attr="responsabili",
                ),
                Prefetch(
                    "progettoricercatore_set",
                    queryset=ProgettoRicercatore.objects.only(
                        "matricola", "nome_origine"
                    ),
                    to_attr="ricercatori",
                ),
            )
            .only(
                "id",
                "ambito_territoriale__id",
                "ambito_territoriale__ambito_territoriale",
                "tipologia_programma__id",
                "tipologia_programma__nome_programma",
                "titolo",
                "anno_avvio",
                "uo",
                "uo__denominazione",
                "descr_breve",
                "url_immagine",
                "abstract_ita",
                "abstract_eng",
                "area_tecnologica",
                "area_tecnologica__descr_area_ita",
                "area_tecnologica__descr_area_eng",
                "url_sito_web",
                "is_active",
            )
            .distinct()
            .order_by(
                "ordinamento",
                "-anno_avvio",
                "ambito_territoriale__ambito_territoriale",
            )
        )
        return query


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TERRITORIAL_SCOPES_LIST_SUMMARY,
        description=descriptions.TERRITORIAL_SCOPES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            TerritorialScopesSerializer(many=True)
        ),
    )
)
class TerritorialScopesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TerritorialScopesSerializer
    queryset = ProgettoAmbitoTerritoriale.objects.values(
        "id", "ambito_territoriale"
    ).distinct()


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PROGRAM_TYPES_LIST_SUMMARY,
        description=descriptions.PROGRAM_TYPES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(ProgramTypesSerializer(many=True)),
    )
)
class ProgramTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ProgramTypesSerializer
    queryset = (
        ProgettoTipologiaProgramma.objects.values("id", "nome_programma")
        .order_by("nome_programma")
        .distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.INFRASTRUCTURES_LIST_SUMMARY,
        description=descriptions.INFRASTRUCTURES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(InfrastructuresSerializer(many=True)),
    )
)
class InfrastructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = InfrastructuresSerializer
    queryset = (
        ProgettoDatiBase.objects.values("uo", "uo__denominazione")
        .exclude(uo__isnull=True)
        .distinct()
        .order_by("uo__denominazione")
    )
