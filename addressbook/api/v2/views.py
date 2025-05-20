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

# from .filters import PersonnelCfFilter
from .serializers import PersonnelCfSerializer, RolesSerializer
from addressbook.models import Personale


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
