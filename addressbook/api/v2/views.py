import datetime
from django_filters.rest_framework import DjangoFilterBackend
from addressbook.models import (
    Personale,
    PersonaleAttivoTuttiRuoli,
    PersonalePrioritaRuolo,
    PersonaleContatti,
)

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
from rest_framework.viewsets import ReadOnlyModelViewSet

# from .filters import PersonnelCfFilter, AddressbookFilter, AddressbookFilter
from .serializers import (
    AddressbookSerializer,
    PersonnelCfSerializer,
    AddressbookStructuresSerializer,
    RolesSerializer,
)
from structures.models import UnitaOrganizzativa
from rest_framework.response import Response
from rest_framework import status
from generics.utils import encrypt, decrypt
from django.db.models import Q, Prefetch, OuterRef, Subquery


class GetPersonApi(ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        matricola = data.get("id", "")
        if not matricola:
            return Response(
                "Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND
            )
        p = Personale.objects.filter(matricola=matricola).first()
        if not p:
            return Response("Il dato non esiste", status=status.HTTP_404_NOT_FOUND)
        return Response(encrypt(matricola))


class GetDecryptedPersonApi(ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        encrypted_matricola = data.get("id", "")
        if not encrypted_matricola:
            return Response(
                "Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND
            )
        try:
            m = decrypt(encrypted_matricola)
            return Response(m)
        except Exception:
            return Response(
                "Non è stato possibile decriptare il dato",
                status=status.HTTP_404_NOT_FOUND,
            )


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


class AddressbookViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AddressbookSerializer
    # filterset_class = AddressbookFilter
    queryset = (
        Personale.objects.filter(
            Q(flg_cessato=0, dt_rap_fin__gte=datetime.datetime.today())
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
            & ~Q(didatticacopertura__stato_coper_cod="R")
            | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
            & ~Q(didatticacopertura__stato_coper_cod="R"),
        )
        .prefetch_related(
            Prefetch(
                "personalecontatti",
                queryset=PersonaleContatti.objects.select_related("cd_tipo_cont"),
                to_attr="contatti",
            ),
            Prefetch(
                "personaleattivotuttiruoli",
                queryset=(
                    PersonaleAttivoTuttiRuoli.objects.filter(
                        cd_uo_aff_org__isnull=False
                    )
                    .select_related("cd_uo_aff_org")
                    .annotate(
                        priorita=Subquery(
                            PersonalePrioritaRuolo.objects.filter(
                                cd_ruolo=OuterRef("cd_ruolo")
                            ).values("priorita")[:1]
                        )
                    )
                    .distinct()
                ),
                to_attr="pers_attivo_tutti_ruoli",
            ),
        )
        .only(
            "nome",
            "middle_name",
            "cognome",
            "id_ab",
            "matricola",
            "fl_docente",
            "profilo",
            "ds_profilo",
            "ds_profilo_breve",
            "cd_ruolo",
            "ds_ruolo_locale",
            "dt_rap_ini",
        )
        .order_by("cognome", "nome")
    )


class AddressbookStructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AddressbookStructuresSerializer
    # filterset_class = AddressbookStructuresFilter
    queryset = (
        UnitaOrganizzativa.objects.filter(
            dt_fine_val__gte=datetime.datetime.today(),
        )
        .extra(
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
        )
        .values(
            "uo",
            "denominazione",
            "cd_tipo_nodo",
            "ds_tipo_nodo",
        )
        .distinct()
    )


class RolesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    serializer_class = RolesSerializer

    queryset = (
        Personale.objects.values("cd_ruolo", "ds_ruolo_locale")
        .order_by("ds_ruolo_locale")
        .distinct()
    )
