import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

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
from django.db.models import OuterRef, Subquery


from structures.models import (
    DidatticaDipartimentoUrl,
    DidatticaDipartimento,
    UnitaOrganizzativa,
    UnitaOrganizzativaContatti,
    UnitaOrganizzativaFunzioni,
    UnitaOrganizzativaTipoFunzioni,
)


class StructuresViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = StructuresSerializer
    filterset_class = StructuresFilter

    def get_serializer_class(self):
        if self.action == "list":
            return StructuresSerializer
        else:
            return StructureSerializer

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
            email_subquery = Subquery(
                UnitaOrganizzativaContatti.objects.filter(
                    ab=OuterRef("id_ab"), cd_tipo_cont="EMAIL"
                ).values("contatto")[:1]
            )
            pec_subquery = Subquery(
                UnitaOrganizzativaContatti.objects.filter(
                    ab=OuterRef("id_ab"), cd_tipo_cont="PEC"
                ).values("contatto")[:1]
            )
            tfr_subquery = Subquery(
                UnitaOrganizzativaContatti.objects.filter(
                    ab=OuterRef("id_ab"), cd_tipo_cont="TFR"
                ).values("contatto")[:1]
            )

            funzioniPersonale = UnitaOrganizzativaFunzioni.objects.filter(
                cd_csa=OuterRef("cd_csa"),
                cod_fis__flg_cessato=False,
                termine__gt=datetime.datetime.now(),
            ).only(
                "ds_funzione",
                "funzione",
                "cod_fis__nome",
                "cod_fis__cognome",
                "cod_fis__middle_name",
                "cod_fis__matricola",
            )

            return (
                UnitaOrganizzativa.objects.filter(
                    dt_fine_val__gte=datetime.datetime.today()
                )
                .annotate(
                    urls=urls_subquery,
                    email=email_subquery,
                    pec=pec_subquery,
                    tfr=tfr_subquery,
                    id=funzioniPersonale.values("cod_fis__matricola"),
                    cognome=funzioniPersonale.values("cod_fis__cognome"),
                    nome=funzioniPersonale.values("cod_fis__nome"),
                    middle_name=funzioniPersonale.values("cod_fis__middle_name"),
                    function=funzioniPersonale.values("ds_funzione"),
                    functionCod=funzioniPersonale.values("funzione"),
                )
                .values(
                    "uo",
                    "denominazione",
                    "uo_padre",
                    "denominazione_padre",
                    "ds_tipo_nodo",
                    "cd_tipo_nodo",
                    "ds_mission",
                    "cd_csa",
                    "urls",
                    "email",
                    "pec",
                    "tfr",
                    "id",
                    "cognome",
                    "nome",
                    "middle_name",
                    "function",
                    "functionCod",
                )
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


class DepartmentsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = DepartmentsSerializer
    lookup_field = "dip_cod"

    def get_queryset(self):
        language = self.request.LANGUAGE_CODE
        ordering_field = "dip_des_it" if language == "it" else "dip_des_eng"
        urls_subquery = Subquery(
            DidatticaDipartimentoUrl.objects.filter(dip_cod=OuterRef("dip_cod")).values(
                "dip_url"
            )[:1]
        )
        return (
            DidatticaDipartimento.objects.annotate(urls=urls_subquery)
            .order_by(ordering_field)
            .values(
                "dip_id",
                "dip_cod",
                "dip_des_it",
                "dip_des_eng",
                "dip_nome_breve",
                "urls",
            )
        )
