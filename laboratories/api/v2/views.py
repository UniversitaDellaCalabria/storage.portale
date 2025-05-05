from addressbook.models import Personale
from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from addressbook.utils import append_email_addresses, get_personale_matricola

# from .filters import CompaniesFilter
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

from laboratories.models import (
    LaboratorioAltriDipartimenti,
    LaboratorioAttivita,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioInfrastruttura,
    LaboratorioPersonaleRicerca,
    LaboratorioPersonaleTecnico,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from django.db.models import Q, Prefetch, Case, When, Value

from rest_framework.viewsets import ReadOnlyModelViewSet
class LaboratoriesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesSerializer
    
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
                and LaboratorioDatiBase.objects.filter(
                    matricola_responsabile_scientifico=user_profile
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
                .prefetch_related(
                    Prefetch(
                        "laboratoriopersonalericerca_set",
                        queryset=LaboratorioPersonaleRicerca.objects.only(
                            "matricola_personale_ricerca__matricola",
                            "matricola_personale_ricerca__nome",
                            "matricola_personale_ricerca__cognome",
                            "matricola_personale_ricerca__middle_name",
                        ),
                        to_attr="personale_ricerca",
                    ),
                    Prefetch(
                        "laboratoriopersonaletecnico_set",
                        queryset=LaboratorioPersonaleTecnico.objects.only(
                            "matricola_personale_tecnico__matricola",
                            "matricola_personale_tecnico__nome",
                            "matricola_personale_tecnico__cognome",
                            "matricola_personale_tecnico__middle_name",
                            "ruolo",
                        ),
                        to_attr="personale_tecnico",
                    ),
                    Prefetch(
                        "laboratorioattivita_set",
                        queryset=(
                            LaboratorioAttivita.objects.only(
                                "tipologia_attivita__id", "tipologia_attivita__descrizione"
                            ).distinct()
                        ),
                        to_attr="attivita",
                    ),
                    Prefetch(
                        "laboratorioaltridipartimenti_set",
                        queryset=(
                            LaboratorioAltriDipartimenti.objects.only(
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            ).distinct()
                        ),
                        to_attr="other_dep",
                    ),
                )
                .only(
                    "id",
                    "nome_laboratorio",
                    "ambito",
                    "dipartimento_riferimento_nome",
                    "dipartimento_riferimento__dip_id",
                    "dipartimento_riferimento__dip_cod",
                    "sede_dimensione",
                    "responsabile_scientifico",
                    "matricola_responsabile_scientifico",
                    "laboratorio_interdipartimentale",
                    "finalita_servizi_it",
                    "finalita_servizi_en",
                    "finalita_ricerca_it",
                    "finalita_ricerca_en",
                    "finalita_didattica_en",
                    "finalita_didattica_it",
                    "infrastruttura_riferimento__id",
                    "infrastruttura_riferimento__descrizione",
                    "acronimo",
                    "nome_file_logo",
                    "visibile",
                )
                .distinct()
            )
        if self.action == "retrieve":
            query = LaboratorioDatiBase.objects.filter(query_is_active, id=self.kwargs["pk"]).prefetch_related(
                Prefetch(
                    "laboratoriodatierc1_set",
                    queryset=LaboratorioDatiErc1.objects.select_related(
                        "ricerca_erc1__ricerca_erc0_cod"
                    ).only(
                        "ricerca_erc1__id",
                        "ricerca_erc1__cod_erc1",
                        "ricerca_erc1__descrizione",
                        "ricerca_erc1__ricerca_erc0_cod__erc0_cod",
                        "ricerca_erc1__ricerca_erc0_cod__description",
                        "ricerca_erc1__ricerca_erc0_cod__description_en",
                    ).distinct(),
                    to_attr="erc0",
                ),
                Prefetch(
                        "laboratoriopersonalericerca_set",
                        queryset=LaboratorioPersonaleRicerca.objects.only(
                            "matricola_personale_ricerca__matricola",
                            "matricola_personale_ricerca__nome",
                            "matricola_personale_ricerca__cognome",
                            "matricola_personale_ricerca__middle_name",
                        ),
                        to_attr="personale_ricerca",
                    ),
                    Prefetch(
                        "laboratoriopersonaletecnico_set",
                        queryset=LaboratorioPersonaleTecnico.objects.only(
                            "matricola_personale_tecnico__matricola",
                            "matricola_personale_tecnico__nome",
                            "matricola_personale_tecnico__cognome",
                            "matricola_personale_tecnico__middle_name",
                            "ruolo",
                        ),
                        to_attr="personale_tecnico",
                    ),
                    Prefetch(
                        "laboratorioattivita_set",
                        queryset=(
                            LaboratorioAttivita.objects.only(
                                "tipologia_attivita__id", "tipologia_attivita__descrizione"
                            ).distinct()
                        ),
                        to_attr="attivita",
                    ),
                    Prefetch(
                        "laboratorioaltridipartimenti_set",
                        queryset=(
                            LaboratorioAltriDipartimenti.objects.only(
                                "didattica_dipartimento__dip_cod",
                                "didattica_dipartimento__dip_des_it",
                                "didattica_dipartimento__dip_des_eng",
                            ).distinct()
                        ),
                        to_attr="other_dep",
                    ),
                    Prefetch(
                        "laboratorioserviziofferti_set",
                        queryset= LaboratorioServiziOfferti.objects.only("nome_servizio", "descrizione_servizio"),
                        to_attr="servizi_offerti",
                    ),
                    Prefetch(
                        "laboratorioubicazione_set",
                        queryset=LaboratorioUbicazione.objects.only("edificio", "piano", "note"),
                        to_attr="ubicazione",
                    ),
                    ).only(
                "id",
                "referente_compilazione",
                "matricola_referente_compilazione",
                "nome_laboratorio",
                "acronimo",
                "nome_file_logo",
                "dipartimento_riferimento__dip_id",
                "dipartimento_riferimento__dip_cod",
                "dipartimento_riferimento__dip_des_it",
                "dipartimento_riferimento__dip_des_eng",
                "infrastruttura_riferimento__id",
                "infrastruttura_riferimento__descrizione",
                "ambito",
                "finalita_servizi_it",
                "finalita_servizi_en",
                "finalita_ricerca_it",
                "finalita_ricerca_en",
                "finalita_didattica_en",
                "finalita_didattica_it",
                "responsabile_scientifico",
                "matricola_responsabile_scientifico",
                "matricola_responsabile_scientifico__id_ab",
                "laboratorio_interdipartimentale",
                "sito_web",
                "strumentazione_descrizione",
                "visibile",
            )
            # append_email_addresses(query, "matricola_responsabile_scientifico__id_ab")
            # append_email_addresses(query.first().personale_ricerca, "matricola_personale_ricerca__id_ab")
            # append_email_addresses(query.first().personale_tecnico, "matricola_personale_tecnico__id_ab")
            
            return query

class LaboratoriesAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesAreaSerializer
    queryset = (
        LaboratorioDatiBase.objects.all().values("ambito").distinct().order_by("ambito")
    )


class LaboratoriesScopesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesScopesSerializer
    queryset = (
        LaboratorioTipologiaAttivita.objects.all()
        .values("id", "descrizione")
        .distinct()
        .order_by("id")
    )


class InfrastructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = InfrastructuresSerializer
    queryset = (
        LaboratorioInfrastruttura.objects.all().values("id", "descrizione").distinct()
    )


class ErcListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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


class AsterListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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
