from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

from .serializers import CompaniesSerializer, TechAreaSerializer
from .filters import CompaniesFilter
from companies.models import (
    SpinoffStartupDatiBase,
    TipologiaAreaTecnologica,
)
from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet
from companies.settings import OFFICE_COMPANIES


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.COMPANIES_LIST_SUMMARY,
        description=descriptions.COMPANIES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(CompaniesSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.COMPANIES_RETRIEVE_SUMMARY,
        description=descriptions.COMPANIES_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(CompaniesSerializer),
    ),
)
class CompaniesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompaniesFilter
    serializer_class = CompaniesSerializer

    def get_queryset(self):
        request = self.request
        only_active = True

        if request.user.is_superuser:
            only_active = False
        if request.user.is_authenticated:
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_COMPANIES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        return (
            SpinoffStartupDatiBase.objects.filter(
                Q(is_active=True) if only_active else Q()
            )
            .values(
                "id",
                "piva",
                "nome_azienda",
                "nome_file_logo",
                "url_sito_web",
                "descrizione_ita",
                "descrizione_eng",
                "referente_unical",
                "matricola_referente_unical",
                "area_tecnologica",
                "area_tecnologica__descr_area_ita",
                "area_tecnologica__descr_area_eng",
                "is_startup",
                "is_spinoff",
                "is_active",
            )
            .distinct()
        )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TECH_AREA_LIST_SUMMARY,
        description=descriptions.TECH_AREA_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TechAreaSerializer(many=True)),
    )
)
class TechAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TechAreaSerializer
    queryset = TipologiaAreaTecnologica.objects.values(
        "id",
        "descr_area_ita",
        "descr_area_eng",
    ).distinct()
