from addressbook.models import Personale
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
# ~ from rest_framework.pagination import PageNumberPagination
from generics.api.pagination import PageNumberPagination
from generics.views import ClearResponseViewSet

from rest_framework import mixins, viewsets
from .filters import LaboratoriesFilters
from laboratories.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from .serializers import (
    LaboratoriesSerializer,
    LaboratorySerializer,
    LaboratoriesAreaSerializer,
    LaboratoriesScopesSerializer,
    InfrastructuresSerializer,
    Erc0ListSerializer,
    Erc1ListSerializer,
    Erc2ListSerializer,
    Aster1ListSerializer,
    Aster2ListSerializer,
)

# from laboratories.models import (
#     LaboratorioAltriDipartimenti,
#     LaboratorioAttivita,
#     LaboratorioDatiBase,
#     LaboratorioDatiErc1,
#     LaboratorioInfrastruttura,
#     LaboratorioPersonaleRicerca,
#     LaboratorioPersonaleTecnico,
#     LaboratorioServiziOfferti,
#     LaboratorioTipologiaAttivita,
#     LaboratorioUbicazione,
# )
from laboratories.models import (
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioAttivita,
    LaboratorioAffiliati,
    LaboratorioDipartimenti,
    LaboratorioResponsabile,
    LaboratorioServizi,
    LaboratorioUbicazione,
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from django.db.models import Q, Prefetch

from rest_framework.viewsets import ReadOnlyModelViewSet


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.LABORATORIES_LIST_SUMMARY,
        description=descriptions.LABORATORIES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(LaboratoriesSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.LABORATORIES_RETRIEVE_SUMMARY,
        description=descriptions.LABORATORIES_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(LaboratoriesSerializer),
    ),
)
class LaboratoriesViewSet(ReadOnlyModelViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesSerializer
    filterset_class = LaboratoriesFilters

    def get_serializer_class(self):
        return LaboratoriesSerializer if self.action == "list" else LaboratorySerializer

    def get_queryset(self):
        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        elif self.request.user.is_authenticated:  # pragma: no cover
            user_profile = None
            if self.request.user.taxpayer_id is not None:
                user_profile = Personale.objects.filter(
                    cod_fis=self.request.user.taxpayer_id
                ).first()

            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )

            is_scientific_director = (
                user_profile is not None
                and LaboratorioResponsabile.objects.filter(
                    matricola_personale=user_profile
                ).exists()
            )
            is_operator = offices.filter(office__name=OFFICE_LABORATORIES).exists()
            is_validator = offices.filter(
                office__name=OFFICE_LABORATORY_VALIDATORS
            ).exists()
            if is_operator or is_validator or is_scientific_director:
                only_active = False

        query_is_active = Q(visibile=True) if only_active else Q()

        if self.action == "list":
            return (
                LaboratorioDatiBase.objects.filter(
                    query_is_active,
                )
                .select_related("ambito_s3_prevalente", "infrastruttura_riferimento")
                .prefetch_related(
                    Prefetch(
                        "laboratorioubicazione_set",
                        queryset=LaboratorioUbicazione.objects.only(
                            "laboratorio_dati_base", "superficie_mq"
                        ),
                        to_attr="ubicazione",
                    ),
                    Prefetch(
                        "laboratorioaffiliati_set",
                        queryset=LaboratorioAffiliati.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        ).exclude(
                            laboratorio_ruolo__descr_ruolo_it__icontains="tecnic"
                        ),
                        to_attr="personale_ricerca",
                    ),
                    Prefetch(
                        "laboratorioaffiliati_set",
                        queryset=LaboratorioAffiliati.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        )
                        .filter(laboratorio_ruolo__descr_ruolo_it__icontains="tecnic")
                        .only(
                            "laboratorio_dati_base",
                            "matricola_personale__matricola",
                            "matricola_personale__nome",
                            "matricola_personale__cognome",
                            "matricola_personale__middle_name",
                            "matricola_personale__id_ab",
                            "laboratorio_ruolo__descr_ruolo_it",
                            "laboratorio_ruolo__descr_ruolo_en",
                        ),
                        to_attr="personale_tecnico",
                    ),
                    Prefetch(
                        "laboratorioresponsabile_set",
                        queryset=LaboratorioResponsabile.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        ).only(
                            "laboratorio_dati_base",
                            "matricola_personale__id_ab",
                            "matricola_personale__matricola",
                            "matricola_personale__nome",
                            "matricola_personale__cognome",
                            "matricola_personale__middle_name",
                            "laboratorio_ruolo__descr_ruolo_it",
                            "laboratorio_ruolo__descr_ruolo_en",
                            "data_inizio",
                            "data_fine",
                        ),
                        to_attr="responsabili",
                    ),
                    Prefetch(
                        "laboratorioattivita_set",
                        queryset=(
                            LaboratorioAttivita.objects.select_related(
                                "tipologia_attivita"
                            )
                            .only(
                                "laboratorio_dati_base",
                                "tipologia_attivita__id",
                                "tipologia_attivita__descrizione_it",
                                "tipologia_attivita__descrizione_en",
                                "descr_finalita_it",
                                "descr_finalita_en",
                            )
                            .distinct()
                        ),
                        to_attr="attivita",
                    ),
                    Prefetch(
                        "laboratoriodipartimenti_set",
                        queryset=(
                            LaboratorioDipartimenti.objects.select_related(
                                "didattica_dipartimento"
                            )
                            .filter(principale=True)
                            .only(
                                "laboratorio_dati_base",
                                "didattica_dipartimento__dip_id",
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            )
                            .distinct()
                        ),
                        to_attr="dipartimento_principale",
                    ),
                    Prefetch(
                        "laboratoriodipartimenti_set",
                        queryset=(
                            LaboratorioDipartimenti.objects.select_related(
                                "didattica_dipartimento"
                            )
                            .exclude(principale=True)
                            .only(
                                "laboratorio_dati_base",
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            )
                            .distinct()
                        ),
                        to_attr="other_dep",
                    ),
                )
                .only(
                    "id",
                    "nome_laboratorio",
                    "acronimo",
                    "tipologia",
                    "ambito_s3_prevalente__id",
                    "ambito_s3_prevalente__codice",
                    "ambito_s3_prevalente__denominazione_it",
                    "ambito_s3_prevalente__denominazione_en",
                    "infrastruttura_riferimento__id",
                    "infrastruttura_riferimento__descrizione_it",
                    "infrastruttura_riferimento__descrizione_en",
                    "nome_file_logo",
                    "visibile",
                )
                .distinct()
            )
        if self.action == "retrieve":
            query = (
                LaboratorioDatiBase.objects.filter(
                    query_is_active, id=self.kwargs["pk"]
                )
                .select_related("ambito_s3_prevalente", "infrastruttura_riferimento")
                .prefetch_related(
                    Prefetch(
                        "laboratoriodatierc1_set",
                        queryset=LaboratorioDatiErc1.objects.select_related(
                            "ricerca_erc1__ricerca_erc0_cod"
                        )
                        .only(
                            "laboratorio_dati_base",
                            "ricerca_erc1__id",
                            "ricerca_erc1__cod_erc1",
                            "ricerca_erc1__descrizione",
                            "ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                            "ricerca_erc1__ricerca_erc0_cod__description",
                            "ricerca_erc1__ricerca_erc0_cod__description_en",
                        )
                        .distinct(),
                        to_attr="erc0",
                    ),
                    Prefetch(
                        "laboratorioaffiliati_set",
                        queryset=LaboratorioAffiliati.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        )
                        .exclude(laboratorio_ruolo__descr_ruolo_it__icontains="tecnic")
                        .only(
                            "laboratorio_dati_base",
                            "nome_cognome",
                            "ente_provenienza",
                            "matricola_personale__id_ab",
                            "matricola_personale__matricola",
                            "matricola_personale__nome",
                            "matricola_personale__cognome",
                            "matricola_personale__cod_fis",
                            "matricola_personale__middle_name",
                            "laboratorio_ruolo__descr_ruolo_it",
                            "laboratorio_ruolo__descr_ruolo_en",
                        ),
                        to_attr="personale_ricerca",
                    ),
                    Prefetch(
                        "laboratorioaffiliati_set",
                        queryset=LaboratorioAffiliati.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        )
                        .filter(laboratorio_ruolo__descr_ruolo_it__icontains="tecnic")
                        .only(
                            "laboratorio_dati_base",
                            "nome_cognome",
                            "matricola_personale__id_ab",
                            "matricola_personale__matricola",
                            "matricola_personale__nome",
                            "matricola_personale__cognome",
                            "matricola_personale__middle_name",
                            "laboratorio_ruolo__descr_ruolo_it",
                            "laboratorio_ruolo__descr_ruolo_en",
                        ),
                        to_attr="personale_tecnico",
                    ),
                    Prefetch(
                        "laboratorioresponsabile_set",
                        queryset=LaboratorioResponsabile.objects.select_related(
                            "matricola_personale", "laboratorio_ruolo"
                        ).only(
                            "laboratorio_dati_base",
                            "matricola_personale__id_ab",
                            "matricola_personale__matricola",
                            "matricola_personale__nome",
                            "matricola_personale__cognome",
                            "matricola_personale__middle_name",
                            "matricola_personale__cod_fis",
                            "laboratorio_ruolo__descr_ruolo_it",
                            "laboratorio_ruolo__descr_ruolo_en",
                            "data_inizio",
                            "data_fine",
                        ),
                        to_attr="responsabili",
                    ),
                    Prefetch(
                        "laboratorioattivita_set",
                        queryset=(
                            LaboratorioAttivita.objects.select_related(
                                "tipologia_attivita"
                            )
                            .only(
                                "laboratorio_dati_base",
                                "tipologia_attivita__id",
                                "tipologia_attivita__descrizione_it",
                                "tipologia_attivita__descrizione_en",
                                "descr_finalita_it",
                                "descr_finalita_en",
                            )
                            .distinct()
                        ),
                        to_attr="attivita",
                    ),
                    Prefetch(
                        "laboratoriodipartimenti_set",
                        queryset=(
                            LaboratorioDipartimenti.objects.select_related(
                                "didattica_dipartimento"
                            )
                            .filter(principale=True)
                            .only(
                                "laboratorio_dati_base",
                                "didattica_dipartimento__dip_id",
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            )
                            .distinct()
                        ),
                        to_attr="dipartimento_principale",
                    ),
                    Prefetch(
                        "laboratoriodipartimenti_set",
                        queryset=(
                            LaboratorioDipartimenti.objects.select_related(
                                "didattica_dipartimento"
                            )
                            .exclude(principale=True)
                            .only(
                                "laboratorio_dati_base",
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            )
                            .distinct()
                        ),
                        to_attr="other_dep",
                    ),
                    Prefetch(
                        "laboratorioservizi_set",
                        queryset=LaboratorioServizi.objects.select_related(
                            "laboratorio_anagrafica_servizi"
                        ).only(
                            "laboratorio_dati_base",
                            "descrizione_it",
                            "descrizione_en",
                            "laboratorio_anagrafica_servizi__nome_servizio_it",
                            "laboratorio_anagrafica_servizi__nome_servizio_en",
                            "laboratorio_anagrafica_servizi__descrizione_servizio_it",
                            "laboratorio_anagrafica_servizi__descrizione_servizio_en",
                        ),
                        to_attr="servizi_offerti",
                    ),
                    Prefetch(
                        "laboratorioubicazione_set",
                        queryset=LaboratorioUbicazione.objects.only(
                            "laboratorio_dati_base",
                            "edificio",
                            "piano",
                            "superficie_mq",
                            "note",
                        ),
                        to_attr="ubicazione",
                    ),
                )
                .only(
                    "id",
                    "descrizione",
                    "nome_laboratorio",
                    "acronimo",
                    "tipologia",
                    "nome_file_logo",
                    "ambito_s3_prevalente__id",
                    "ambito_s3_prevalente__codice",
                    "ambito_s3_prevalente__denominazione_it",
                    "ambito_s3_prevalente__denominazione_en",
                    "infrastruttura_riferimento__id",
                    "infrastruttura_riferimento__descrizione_it",
                    "infrastruttura_riferimento__descrizione_en",
                    "altre_strutture_riferimento",
                    "descr_altre_strutture_riferimento_it",
                    "descr_altre_strutture_riferimento_en",
                    "visibile",
                )
            )

            return query


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.LABORATORIES_AREA_LIST_SUMMARY,
        description=descriptions.LABORATORIES_AREA_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            LaboratoriesAreaSerializer(many=True)
        ),
    )
)
class LaboratoriesAreaViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesAreaSerializer
    queryset = (
        LaboratorioDatiBase.objects.all().values("ambito").distinct().order_by("ambito")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.LABORATORIES_SCOPES_LIST_SUMMARY,
        description=descriptions.LABORATORIES_SCOPES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(
            LaboratoriesScopesSerializer(many=True)
        ),
    ),
)
class LaboratoriesScopesViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesScopesSerializer
    queryset = (
        LaboratorioTipologiaAttivita.objects.all()
        .values("id", "descrizione")
        .distinct()
        .order_by("id")
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.INFRASTRUCTURES_LIST_SUMMARY,
        description=descriptions.INFRASTRUCTURES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(InfrastructuresSerializer(many=True)),
    )
)
class InfrastructuresViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = InfrastructuresSerializer
    queryset = (
        LaboratorioInfrastruttura.objects.all().values("id", "descrizione").distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ERC_LIST_SUMMARY,
        description=descriptions.ERC_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(Erc1ListSerializer(many=True)),
    )
)
class ErcListViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = Erc1ListSerializer
    queryset = (
        RicercaErc0.objects.all()
        .values("erc0_cod", "description", "description_en")
        .distinct()
    )

    def get_queryset(self):
        level = self.kwargs.get("level")

        if level == "1":
            for q in self.queryset:
                erc1 = (
                    RicercaErc1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "cod_erc1", "descrizione")
                    .distinct()
                )

                q["erc1_list"] = [] if len(erc1) == 0 else erc1

        elif level == "2":
            for q in self.queryset:
                erc1 = (
                    RicercaErc1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "cod_erc1", "descrizione")
                    .distinct()
                )

                q["erc1_list"] = [] if len(erc1) == 0 else erc1
                for erc1 in q["erc1_list"]:
                    erc2 = (
                        RicercaErc2.objects.filter(ricerca_erc1_id=erc1["id"])
                        .values("id", "cod_erc2", "descrizione")
                        .distinct()
                    )
                    erc1["erc2_list"] = [] if len(erc2) == 0 else erc2

        return self.queryset

    def get_serializer(self, *args, **kwargs):
        level = self.kwargs.get("level")
        if level == "1":
            return Erc1ListSerializer(*args, **kwargs)
        elif level == "2":
            return Erc2ListSerializer(*args, **kwargs)
        return Erc0ListSerializer(*args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.INFRASTRUCTURES_LIST_SUMMARY,
        description=descriptions.INFRASTRUCTURES_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(),
    )
)
class AsterListViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    queryset = RicercaErc0.objects.values("erc0_cod", "description", "description_en")

    def get_queryset(self):
        level = self.kwargs.get("level")

        if level == "1":
            for q in self.queryset:
                aster1 = (
                    RicercaAster1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "descrizione")
                    .distinct()
                )

                q["aster1_list"] = [] if len(aster1) == 0 else aster1

        elif level == "2":
            for q in self.queryset:
                aster1 = (
                    RicercaAster1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "descrizione")
                    .distinct()
                )
                q["aster1_list"] = [] if len(aster1) == 0 else aster1
                for aster1 in q["aster1_list"]:
                    aster2 = (
                        RicercaAster2.objects.filter(ricerca_aster1_id=aster1["id"])
                        .values("id", "descrizione")
                        .distinct()
                    )
                    aster1["aster2_list"] = [] if len(aster2) == 0 else aster2

        return self.queryset

    def get_serializer(self, *args, **kwargs):
        level = self.kwargs.get("level")
        return (
            Aster1ListSerializer(*args, **kwargs)
            if level == "1"
            else Aster2ListSerializer(*args, **kwargs)
        )
