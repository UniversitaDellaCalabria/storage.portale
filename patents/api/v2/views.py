from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Prefetch
from patents.models import BrevettoDatiBase, BrevettoInventori
from .serializers import PatentsSerializer
from .filters import PatentFilter
from patents.settings import OFFICE_PATENTS
from rest_framework.viewsets import ReadOnlyModelViewSet


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PATENTS_LIST_SUMMARY,
        description=descriptions.PATENTS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(PatentsSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.PATENTS_RETRIEVE_SUMMARY,
        description=descriptions.PATENTS_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(PatentsSerializer),
    ),
)
class PatentsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PatentsSerializer
    filterset_class = PatentFilter

    def get_queryset(self):
        request = self.request
        only_active = True

        if request.user.is_superuser:
            only_active = False
        if request.user.is_authenticated:
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_PATENTS,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        query_is_active = Q(is_active=True) if only_active else Q()

        return (
            BrevettoDatiBase.objects.filter(query_is_active)
            .prefetch_related(
                Prefetch(
                    "brevettoinventori",
                    queryset=BrevettoInventori.objects.only(
                        "matricola_inventore",
                        "cognomenome_origine",
                    ).distinct(),
                    to_attr="inventori",
                )
            )
            .only(
                "id",
                "id_univoco",
                "titolo",
                "nome_file_logo",
                "breve_descrizione",
                "trl_iniziale",
                "trl_aggiornato",
                "valorizzazione",
                "url_knowledge_share",
                "area_tecnologica",
                "area_tecnologica__descr_area_ita",
                "area_tecnologica__descr_area_eng",
                "is_active",
            )
            .distinct()
        )
