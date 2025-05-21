import datetime
from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

# from .filters import PersonnelCfFilter, AddressbookFilter
from .serializers import PersonnelCfSerializer, AddressbookStructuresSerializer, RolesSerializer
from addressbook.models import (
    Personale
)
from structures.models import UnitaOrganizzativa
        
        

class AddressbookStructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AddressbookStructuresSerializer
    # filterset_class = AddressbookStructuresFilter
    queryset = UnitaOrganizzativa.objects.filter(
            dt_fine_val__gte=datetime.datetime.today(),
        ).extra(
            select={
                "matricola": "PERSONALE.MATRICOLA",
                "cd_uo_aff_org": "PERSONALE.CD_UO_AFF_ORG",
            },
            tables=["PERSONALE"],
            where=[
                "UNITA_ORGANIZZATIVA.UO=PERSONALE.CD_UO_AFF_ORG",
                "PERSONALE.FLG_CESSATO=0",
                "PERSONALE.CD_UO_AFF_ORG is not NULL",
            ],
        ).values(
            "uo",
            "denominazione",
            "cd_tipo_nodo",
            "ds_tipo_nodo",
        ).distinct()

class PersonnelCfViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PersonnelCfSerializer
    # filterset_class = PersonnelCfFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = (
        Personale.objects.filter(
            flg_cessato=0, dt_rap_fin__gte=datetime.datetime.today()
        )
        .only(
            "nome",
            "middle_name",
            "cognome",
            "cod_fis",
            "cd_ruolo",
            "ds_ruolo_locale",
            "cd_uo_aff_org",
            "ds_aff_org",
            "matricola",
        )
        .order_by("cognome")
    )


class RolesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    serializer_class = RolesSerializer

    queryset = (
        Personale.objects.values("cd_ruolo", "ds_ruolo_locale")
        .order_by("ds_ruolo_locale")
        .distinct()
    )
