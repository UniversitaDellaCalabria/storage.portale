from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

from .filters import ResearchGroupsFilter

from .serializers import (
    ResearchGroupsSerializer
)
from django.db.models import Prefetch
from research_groups.models import RicercaGruppo, RicercaDocenteGruppo


class ResearchGroupsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ResearchGroupsSerializer
    filterset_class = ResearchGroupsFilter

    def get_queryset(self):
        return (
            RicercaGruppo.objects.order_by("nome")
            .prefetch_related(
                Prefetch(
                    "ricercadocentegruppo_set",
                    queryset=RicercaDocenteGruppo.objects.select_related("personale").only(
                        "personale__matricola",
                        "personale__cognome",
                        "personale__nome",
                        "personale__middle_name",
                        "personale__sede",
                        "personale__ds_sede",
                    )
                )
            )
            .select_related("ricerca_erc1")
            .only(
                "id",
                "nome",
                "descrizione",
                "ricerca_erc1__cod_erc1",
                "ricerca_erc1__descrizione",
            )
            .distinct()
        )
