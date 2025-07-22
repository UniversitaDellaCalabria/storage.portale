import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from .filters import StructuresFilter, TypesFilter

from .serializers import (
    StructuresSerializer,
    StructureSerializer,
    TypesSerializer,
    FunctionSerializer,
    DepartmentsSerializer,
)
from django.db.models import OuterRef, Subquery, Prefetch


from structures.models import (
    DidatticaDipartimentoUrl,
    DidatticaDipartimento,
    UnitaOrganizzativa,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaTipoFunzioni,
)


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.STRUCTURES_LIST_SUMMARY,
        description=descriptions.STRUCTURES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(StructuresSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.STRUCTURES_RETRIEVE_SUMMARY,
        description=descriptions.STRUCTURES_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(StructuresSerializer),
    ),
)
class StructuresViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = StructuresSerializer
    filterset_class = StructuresFilter

    def get_serializer_class(self):
        return StructuresSerializer if self.action == "list" else StructureSerializer

    def get_queryset(self):
        urls_subquery = Subquery(
            DidatticaDipartimentoUrl.objects.filter(dip_cod=OuterRef("uo")).values(
                "dip_url"
            )[:1]
        )
        if self.action == "list":
            return (
                UnitaOrganizzativa.objects.annotate(urls=urls_subquery)
                .values(
                    "uo",
                    "denominazione",
                    "ds_tipo_nodo",
                    "cd_tipo_nodo",
                    "dt_fine_val",
                    "uo_padre",
                    "urls",
                )
                .filter(dt_fine_val__gte=datetime.datetime.today())
                .distinct()
                .order_by("denominazione")
            )
        else:
            return (
                UnitaOrganizzativa.objects.filter(
                    dt_fine_val__gte=datetime.datetime.today()
                )
                .annotate(
                    urls=urls_subquery,
                )
                .prefetch_related(
                    Prefetch(
                        "unitaorganizzativafunzioni",
                        queryset=(
                            UnitaOrganizzativaFunzioni.objects.filter(
                                cod_fis__flg_cessato=False,
                                termine__gt=datetime.datetime.now(),
                            ).select_related("cod_fis")
                        ),
                        to_attr="funzioni",
                    ),
                )
                .select_related("unitaorganizzativacontatti")
                .only(
                    "uo",
                    "denominazione",
                    "uo_padre",
                    "denominazione_padre",
                    "ds_tipo_nodo",
                    "cd_tipo_nodo",
                    "ds_mission",
                    "cd_csa",
                    "unitaorganizzativacontatti__cd_tipo_cont",
                    "unitaorganizzativacontatti__contatto",
                )
            )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TYPES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(TypesSerializer(many=True)),
    ),
)
class TypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TypesSerializer
    filterset_class = TypesFilter
    queryset = (
        UnitaOrganizzativa.objects.values("ds_tipo_nodo", "cd_tipo_nodo")
        .distinct()
        .order_by("ds_tipo_nodo")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.FUNCTIONS_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(FunctionSerializer(many=True)),
    ),
)
class FunctionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = FunctionSerializer
    queryset = (
        UnitaOrganizzativaTipoFunzioni.objects.values(
            "cd_tipo_nod", "funzione", "descr_funzione"
        )
        .distinct()
        .order_by("cd_tipo_nod")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.DEPARTMENTS_LIST_SUMMARY,
        description=descriptions.DEPARTMENTS_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(DepartmentsSerializer(many=True)),
    ),
)
class DepartmentsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = DepartmentsSerializer
    lookup_field = "dip_cod"

    def get_queryset(self):
        language = self.request.LANGUAGE_CODE
        ordering_field = "dip_des_it" if language == "it" else "dip_des_eng"
        urls_subquery = Subquery(
            DidatticaDipartimentoUrl.objects.filter(dip_cod=OuterRef("dip_cod")).values("dip_url")[:1]
        )
        return (
            DidatticaDipartimento.objects.annotate(urls=urls_subquery)
            .order_by(ordering_field)
        )
