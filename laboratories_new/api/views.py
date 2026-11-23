import logging
from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from organizational_area.models import OrganizationalStructureOfficeEmployee

from generics.api.pagination import PageNumberPagination
from generics.views import ClearResponseViewSet

from .filters import LaboratoriesFilters, snapshot_matches
from laboratories_new.settings import OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS
from .serializers import (
    Aster1ListSerializer,
    Aster2ListSerializer,
    Erc0ListSerializer,
    Erc1ListSerializer,
    Erc2ListSerializer,
    InfrastructuresSerializer,
    LaboratoriesAreaSerializer,
    LaboratoriesScopesSerializer,
    LaboratoriesSerializer,
    LaboratorySerializer,
)
from laboratories_new.models import (
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioAffiliati,
    LaboratorioDipartimenti,
    LaboratorioInfrastruttura,
    LaboratorioResponsabile,
    LaboratorioServizi,
    LaboratorioUbicazione,
    AmbitiS3,
    TraiettorieS3,
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from django.db.models import Q, Prefetch

from laboratories_new.snapshot_adapter import snapshot_to_obj
from laboratories_new.snapshot_service import current_snapshots, published_lab_ids
from laboratories_new.management.utils import (
    _scientific_directors,
    defer_personale_dates,
    laboratory_statuses,
)

logger = logging.getLogger(__name__)


class LaboratoryAccessMixin:
    """Permessi di visibilita' sui laboratori, calcolati una volta per richiesta."""

    def _access(self):
        if hasattr(self, "_access_cache"):
            return self._access_cache

        user = self.request.user
        is_staff_role = False  # superuser, operatore, validatore
        director_lab_ids = frozenset()

        if user.is_superuser:
            is_staff_role = True
        elif user.is_authenticated:
            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=user,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            is_staff_role = offices.filter(
                office__name__in=[OFFICE_LABORATORIES, OFFICE_LABORATORY_VALIDATORS]
            ).exists()

            # Il responsabile scientifico (incarico in corso) vede i laboratori
            # nascosti di cui e' responsabile, non tutti
            taxpayer_id = getattr(user, "taxpayer_id", None)
            if not is_staff_role and taxpayer_id:
                director_lab_ids = frozenset(
                    _scientific_directors(taxpayer_id).values_list(
                        "laboratorio_dati_base_id", flat=True
                    )
                )

        self._access_cache = {
            "staff": is_staff_role,
            "director_lab_ids": director_lab_ids,
        }
        return self._access_cache

    def _can_see_all_hidden(self):
        return self._access()["staff"]

    def _is_manager(self):
        """Ha un ruolo nella gestione dei laboratori (staff o responsabile)."""
        access = self._access()
        return access["staff"] or bool(access["director_lab_ids"])

    def _can_see_hidden(self, lab_id):
        access = self._access()
        return access["staff"] or lab_id in access["director_lab_ids"]


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
class LaboratoriesViewSet(
    LaboratoryAccessMixin, ReadOnlyModelViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesSerializer
    filterset_class = LaboratoriesFilters
    # Sessione: la lista della gestione chiama questa API dal browser (axios,
    # senza token); senza SessionAuthentication l'utente risulterebbe anonimo e
    # non vedrebbe ne' i laboratori senza snapshot ne' lo stato di approvazione.
    # Il ViewSet e' in sola lettura, quindi il controllo CSRF non entra in gioco.
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_serializer_class(self):
        return LaboratoriesSerializer if self.action == "list" else LaboratorySerializer

    def _visibility_query(self):
        # Un laboratorio e' visibile se ha uno snapshot in corso, anche mentre e'
        # da approvare (nelle tabelle in quel momento ha visibile=False).
        # I dati si leggono dallo snapshot; i filtri di ricerca restano sulle
        # tabelle.
        if self._can_see_all_hidden():
            return Q()
        public = Q(id__in=published_lab_ids())
        director_lab_ids = self._access()["director_lab_ids"]
        if director_lab_ids:
            return public | Q(id__in=director_lab_ids)
        return public

    def _snapshot_objs(self, lab_ids):
        """Oggetti da serializzare, letti dallo snapshot in corso.
        Fallback sulle tabelle per i laboratori senza snapshot (creati dopo lo
        snapshot iniziale e non ancora approvati), visibili solo a chi li gestisce."""
        snaps = current_snapshots(lab_ids)
        missing = [i for i in lab_ids if i not in snaps]
        live = {}
        if missing:
            live = {
                lab.id: lab for lab in self.get_queryset().filter(id__in=missing)
            }
        objs = []
        for lab_id in lab_ids:
            if lab_id in snaps:
                objs.append(snapshot_to_obj(snaps[lab_id], published=True))
            elif lab_id in live:
                objs.append(live[lab_id])
        return objs

    def _filtered_lab_ids(self):
        """
        Id dei laboratori da elencare, filtrati e ordinati per nome.

        Per i laboratori approvati le tabelle coincidono con lo snapshot, e per
        quelli senza snapshot (visibili solo a chi li gestisce) si mostrano le
        tabelle: in entrambi i casi filtri e ordinamento restano sul DB.
        Per quelli con modifiche in attesa (snapshot in corso + visibile=False)
        le tabelle hanno dati non approvati: filtri e nome per l'ordinamento si
        prendono dallo snapshot, cosi' non si trovano cercando dati non pubblici.
        """
        base_qs = self.get_queryset()
        filtered = self.filter_queryset(base_qs)

        pending_ids = set(
            LaboratorioDatiBase.objects.filter(
                self._visibility_query(),
                visibile=False,
                id__in=published_lab_ids(),
            ).values_list("id", flat=True)
        )

        names = dict(
            filtered.exclude(id__in=pending_ids).values_list("id", "nome_laboratorio")
        )

        if pending_ids:
            # filter_queryset ha gia' validato i parametri (errore 400 se invalidi)
            filterset = self.filterset_class(
                self.request.query_params, queryset=base_qs, request=self.request
            )
            filterset.is_valid()
            params = filterset.form.cleaned_data
            for lab_id, data in current_snapshots(pending_ids).items():
                if snapshot_matches(data, params):
                    names[lab_id] = data.get("nome_laboratorio")

        return [
            lab_id
            for lab_id, _name in sorted(
                names.items(), key=lambda kv: ((kv[1] or "").casefold(), kv[0])
            )
        ]

    def list(self, request, *args, **kwargs):
        ids = self._filtered_lab_ids()
        page = self.paginate_queryset(ids)
        lab_ids = list(page if page is not None else ids)

        objs = self._snapshot_objs(lab_ids)
        serializer = self.get_serializer(objs, many=True)

        # stato di approvazione (approvato / da approvare) per tutti i laboratori
        # della pagina, solo per chi ha un ruolo nella gestione. Si calcola sulle
        # tabelle, dove ci sono le modifiche non ancora approvate (lo snapshot e'
        # la versione visibile). Per gli altri vale il default del serializer.
        if self._is_manager() and objs:
            approved = dict(
                LaboratorioDatiBase.objects.filter(
                    id__in=[obj.id for obj in objs]
                ).values_list("id", "visibile")
            )
            statuses = laboratory_statuses(approved)
            for obj in objs:
                if obj.id in statuses:
                    obj.lab_status = statuses[obj.id]

        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        if str(pk).isdigit():
            data = current_snapshots([int(pk)]).get(int(pk))
            if data is not None:
                # snapshot in corso = versione visibile a tutti
                obj = snapshot_to_obj(data, published=True)
                return Response(self.get_serializer(obj).data)
        # senza snapshot: mai approvato, visibile solo a chi vede i nascosti
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        query_is_active = self._visibility_query()

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
                            "laboratorio_dati_base",
                            # "superficie_mq"
                        ),
                        to_attr="ubicazione",
                    ),
                    Prefetch(
                        "laboratorioaffiliati_set",
                        queryset=defer_personale_dates(
                            LaboratorioAffiliati.objects.select_related(
                                "matricola_personale", "laboratorio_ruolo"
                            ).exclude(
                                laboratorio_ruolo__descr_ruolo_it__icontains="tecnic"
                            )
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
                            "traiettoria_s3"
                        ).only(
                            "laboratorio_dati_base",
                            "traiettoria_s3__id",
                            "traiettoria_s3__denominazione_it",
                            "traiettoria_s3__denominazione_en",
                        ),
                        to_attr="servizi_offerti",
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
                .order_by("nome_laboratorio", "id")
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
                            # "superficie_mq",
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
        AmbitiS3.objects.filter(laboratoriodatibase__isnull=False)
        .only("id", "denominazione_it", "denominazione_en")
        .distinct()
        .order_by("denominazione_it", "id")
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
        TraiettorieS3.objects.filter(attiva=True)
        .only("id", "denominazione_it", "denominazione_en")
        .order_by("codice", "id")
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
    queryset = LaboratorioInfrastruttura.objects.only(
        "id", "descrizione_it", "descrizione_en"
    ).order_by("id")


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

    def get_serializer_class(self):
        return {
            "1": Erc1ListSerializer,
            "2": Erc2ListSerializer,
        }.get(self.kwargs.get("level"), Erc0ListSerializer)

    def get_queryset(self):
        level = self.kwargs.get("level")

        erc0_list = list(
            RicercaErc0.objects.values(
                "erc0_cod", "description", "description_en"
            ).order_by("erc0_cod")
        )
        if level not in ("1", "2"):
            return erc0_list

        erc1_by_erc0 = defaultdict(list)
        erc1_by_id = {}
        for e in RicercaErc1.objects.values(
            "id", "cod_erc1", "descrizione", "ricerca_erc0_cod"
        ).order_by("cod_erc1"):
            e["erc2_list"] = []
            erc1_by_erc0[e["ricerca_erc0_cod"]].append(e)
            erc1_by_id[e["id"]] = e

        if level == "2":
            for x in RicercaErc2.objects.values(
                "id", "cod_erc2", "descrizione", "ricerca_erc1_id"
            ).order_by("cod_erc2"):
                parent = erc1_by_id.get(x["ricerca_erc1_id"])
                if parent:
                    parent["erc2_list"].append(x)

        for q in erc0_list:
            q["erc1_list"] = erc1_by_erc0.get(q["erc0_cod"], [])
        return erc0_list


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ASTER_LIST_SUMMARY,
        description=descriptions.ASTER_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(Aster1ListSerializer(many=True)),
    )
)
class AsterListViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet
):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        return (
            Aster1ListSerializer
            if self.kwargs.get("level") == "1"
            else Aster2ListSerializer
        )

    def get_queryset(self):
        level = self.kwargs.get("level")

        erc0_list = list(
            RicercaErc0.objects.values(
                "erc0_cod", "description", "description_en"
            ).order_by("erc0_cod")
        )

        aster1_by_erc0 = defaultdict(list)
        aster1_by_id = {}
        for a in RicercaAster1.objects.values(
            "id", "descrizione", "ricerca_erc0_cod"
        ).order_by("id"):
            a["aster2_list"] = []
            aster1_by_erc0[a["ricerca_erc0_cod"]].append(a)
            aster1_by_id[a["id"]] = a

        if level == "2":
            for x in RicercaAster2.objects.values(
                "id", "descrizione", "ricerca_aster1_id"
            ).order_by("id"):
                parent = aster1_by_id.get(x["ricerca_aster1_id"])
                if parent:
                    parent["aster2_list"].append(x)

        for q in erc0_list:
            q["aster1_list"] = aster1_by_erc0.get(q["erc0_cod"], [])
        return erc0_list
