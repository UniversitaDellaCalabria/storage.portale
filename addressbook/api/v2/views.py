import datetime
from django_filters.rest_framework import DjangoFilterBackend
from addressbook.models import (
    Personale,
    PersonaleAttivoTuttiRuoli,
    PersonalePrioritaRuolo,
    PersonaleContatti,
)
from addressbook.utils import get_personale_matricola

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import PersonnelCfFilter, AddressbookFilter, AddressbookStructuresFilter
from .serializers import (
    AddressbookSerializer,
    PersonnelCfSerializer,
    AddressbookStructuresSerializer,
    RolesSerializer,
    AddressbookDetailSerializer,
    AddressbookFullSerializer,
    AddressbookFullDetailSerializer,
)
from structures.models import UnitaOrganizzativa, UnitaOrganizzativaFunzioni
from rest_framework.response import Response
from rest_framework import status
from generics.utils import encrypt, decrypt
from django.db.models import (
    Q,
    Prefetch,
    OuterRef,
    Subquery,
    Value,
    Exists,
    Case,
    When,
    BooleanField,
)
from rest_framework.viewsets import ViewSet


class GetPersonApi(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "Retrieves the encrypted matricola of a person."

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


class GetDecryptedPersonApi(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "Retrieves the decypted matricola of a person."

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

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PERSONNEL_CF_LIST_SUMMARY,
        description=descriptions.PERSONNEL_CF_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(PersonnelCfSerializer(many=True)),
    ),
)
class PersonnelCfViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PersonnelCfSerializer
    filterset_class = PersonnelCfFilter
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

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ADDRESSBOOK_LIST_SUMMARY,
        description=descriptions.ADDRESSBOOK_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(AddressbookSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.ADDRESSBOOK_DETAIL_SUMMARY,
        description=descriptions.ADDRESSBOOK_DETAIL_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(AddressbookSerializer),
    ),
)
class AddressbookViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressbookFilter
    lookup_field = "matricola"

    def get_queryset(self):
        if self.action == "list":
            return (
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
                        queryset=PersonaleContatti.objects.select_related(
                            "cd_tipo_cont"
                        ),
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
                                    )
                                    .order_by("priorita")
                                    .values("priorita")[:1]
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
        else:
            personale_id = get_personale_matricola(self.kwargs.get("matricola"))
            query_teacher = Personale.objects.filter(
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1),
                didatticacopertura__af__isnull=False,
                matricola=personale_id,
            )
            return (
                Personale.objects.filter(
                    Q(flg_cessato=0)
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                    & ~Q(didatticacopertura__stato_coper_cod="R")
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                    & ~Q(didatticacopertura__stato_coper_cod="R"),
                    matricola=personale_id,
                )
                .prefetch_related(
                    Prefetch(
                        "personalecontatti",
                        queryset=PersonaleContatti.objects.select_related(
                            "cd_tipo_cont"
                        ),
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
                                    )
                                    .order_by("priorita")
                                    .values("priorita")[:1]
                                )
                            )
                            .distinct()
                        ),
                        to_attr="pers_attivo_tutti_ruoli",
                    ),
                    Prefetch(
                        "unitaorganizzativafunzioni_set",
                        queryset=(
                            UnitaOrganizzativaFunzioni.objects.filter(
                                termine__gt=datetime.datetime.now(),
                                decorrenza__lt=datetime.datetime.now(),
                            ).select_related("cd_csa")
                        ),
                        to_attr="functions",
                    ),
                )
                .only(
                    "id_ab",
                    "matricola",
                    "cod_fis",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "ds_ssd",
                    "cd_uo_aff_org",
                    "ds_aff_org",
                    "telrif",
                    "email",
                    "fl_docente",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve",
                    "cd_genere",
                )
                .annotate(
                    has_copertura=Exists(query_teacher),
                    cop_teacher=Case(
                        When(Q(fl_docente=True), then=Value(False)),
                        When(
                            Q(fl_docente=False) & Q(has_copertura=True),
                            then=Value(True),
                        ),
                        default=Value(False),
                        output_field=BooleanField(),
                    ),
                )
            )

    def get_object(self):
        return self.get_queryset().first()

    def get_serializer_class(self):
        if self.action == "list":
            return AddressbookSerializer
        return AddressbookDetailSerializer

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ADDRESSBOOK_FULL_LIST_SUMMARY,
        description=descriptions.ADDRESSBOOK_FULL_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(AddressbookFullSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.ADDRESSBOOK_FULL_DETAIL_SUMMARY,
        description=descriptions.ADDRESSBOOK_FULL_DETAIL_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(AddressbookFullSerializer),
    ),
)
class AddressbookFullViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = AddressbookFilter
    lookup_field = "matricola"

    def get_queryset(self):
        if self.action == "list":
            return AddressbookViewSet.get_queryset(self)
        else:
            personale_id = self.kwargs.get("matricola")
            query_teacher = Personale.objects.filter(
                Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1),
                didatticacopertura__af__isnull=False,
                matricola=personale_id,
            )
            return (
                Personale.objects.filter(
                    Q(matricola=personale_id) | Q(cod_fis=personale_id),
                    Q(flg_cessato=0)
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year)
                    & ~Q(didatticacopertura__stato_coper_cod="R")
                    | Q(didatticacopertura__aa_off_id=datetime.datetime.now().year - 1)
                    & ~Q(didatticacopertura__stato_coper_cod="R"),
                )
                .prefetch_related(
                    Prefetch(
                        "personalecontatti",
                        queryset=PersonaleContatti.objects.select_related(
                            "cd_tipo_cont"
                        ),
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
                                    )
                                    .order_by("priorita")
                                    .values("priorita")[:1]
                                )
                            )
                            .distinct()
                        ),
                        to_attr="pers_attivo_tutti_ruoli",
                    ),
                    Prefetch(
                        "unitaorganizzativafunzioni_set",
                        queryset=(
                            UnitaOrganizzativaFunzioni.objects.filter(
                                termine__gt=datetime.datetime.now(),
                                decorrenza__lt=datetime.datetime.now(),
                            ).select_related("cd_csa")
                        ),
                        to_attr="functions",
                    ),
                )
                .only(
                    "id_ab",
                    "matricola",
                    "cod_fis",
                    "nome",
                    "middle_name",
                    "cognome",
                    "cd_ruolo",
                    "ds_ruolo_locale",
                    "cd_ssd",
                    "ds_ssd",
                    "cd_uo_aff_org",
                    "ds_aff_org",
                    "telrif",
                    "email",
                    "fl_docente",
                    "cv_full_it",
                    "cv_short_it",
                    "cv_full_eng",
                    "cv_short_eng",
                    "profilo",
                    "ds_profilo",
                    "ds_profilo_breve",
                    "cd_genere",
                )
                .annotate(
                    has_copertura=Exists(query_teacher),
                    cop_teacher=Case(
                        When(Q(fl_docente=True), then=Value(False)),
                        When(
                            Q(fl_docente=False) & Q(has_copertura=True),
                            then=Value(True),
                        ),
                        default=Value(False),
                        output_field=BooleanField(),
                    ),
                )
            )

    def get_object(self):
        return self.get_queryset().first()

    def get_serializer_class(self):
        if self.action == "list":
            return AddressbookFullSerializer
        return AddressbookFullDetailSerializer

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ADDRESSBOOK_STRUCTURES_LIST_SUMMARY,
        description=descriptions.ADDRESSBOOK_STRUCTURES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(AddressbookStructuresSerializer(many=True)),
    ),
)
class AddressbookStructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = AddressbookStructuresSerializer
    filterset_class = AddressbookStructuresFilter
    queryset = (
        UnitaOrganizzativa.objects.filter(
            dt_fine_val__gte=datetime.datetime.today(),
        )
        .only(
            "uo",
            "denominazione",
            "cd_tipo_nodo",
            "ds_tipo_nodo",
        )
        .distinct()
    )

@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ROLES_LIST_SUMMARY,
        description=descriptions.ROLES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(RolesSerializer(many=True)),
    ),
)
class RolesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = RolesSerializer
    queryset = (
        Personale.objects.values("cd_ruolo", "ds_ruolo_locale")
        .distinct()
        .order_by("ds_ruolo_locale")
    )
