from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, viewsets

from .filters import PhdFilter, PhdActivitiesFilter
from .serializers import (
    PhdSerializer,
    PhdActivitiesSerializer,
    PhdActivitiesTypesSerializer,
    PhdActivitiesTypologiesSerializer,
    PhdSsdSerializer,
    RefPhdSerializer,
    RefStructuresSerializer,
)

from django.db.models import Prefetch

from phd.models import (
    DidatticaDottoratoAttivitaFormativa,
    DidatticaDottoratoAttivitaFormativaAltriDocenti,
    DidatticaDottoratoAttivitaFormativaDocente,
    DidatticaDottoratoAttivitaFormativaTipologia,
    DidatticaDottoratoCds,
)
from phd.settings import PHD_CYCLES


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(
            PhdSerializer(many=True), include_bad_request=False
        ),
    )
)
class PhdViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhdSerializer
    filterset_class = PhdFilter
    queryset = (
        DidatticaDottoratoCds.objects.select_related("dip_cod")
        .prefetch_related("idesse3_ddr", "idesse3_ddpds")
        .order_by(
            "idesse3_ddr__aa_regdid_id",
            "dip_cod__dip_cod",
            "cds_cod",
            "idesse3_ddpds__pds_cod",
        )
        .only(
            "dip_cod__dip_id",
            "dip_cod__dip_cod",
            "dip_cod__dip_des_it",
            "dip_cod__dip_des_eng",
            "cds_cod",
            "cdsord_des",
            "tipo_corso_cod",
            "tipo_corso_des",
            "durata_anni",
            "valore_min",
            "idesse3_ddr__aa_regdid_id",
            "idesse3_ddr__regdid_cod",
            "idesse3_ddr__frequenza_obbligatoria",
            "idesse3_ddr__num_ciclo",
            "idesse3_ddr__regdid_id_esse3",
            "idesse3_ddpds__pds_cod",
            "idesse3_ddpds__pds_des",
        )
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_CYCLES_LIST_SUMMARY,
    )
)
class PhdCyclesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        result = {str(cycle[0]): cycle[1] for cycle in PHD_CYCLES}
        return Response(result)


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_ACTIVITIES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(PhdActivitiesSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.PHD_ACTIVITIES_RETRIEVE_SUMMARY,
        responses=responses.COMMON_RETRIEVE_RESPONSES(PhdActivitiesSerializer),
    ),
)
class PhdActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhdActivitiesSerializer
    filterset_class = PhdActivitiesFilter

    def get_queryset(self):
        return (
            DidatticaDottoratoAttivitaFormativa.objects.prefetch_related(
                Prefetch(
                    "didatticadottoratoattivitaformativadocente_set",
                    queryset=DidatticaDottoratoAttivitaFormativaDocente.objects.only(
                        "matricola", "cognome_nome_origine"
                    ),
                    to_attr="docente",
                ),
                Prefetch(
                    "didatticadottoratoattivitaformativaaltridocenti_set",
                    queryset=DidatticaDottoratoAttivitaFormativaAltriDocenti.objects.only(
                        "matricola", "cognome_nome_origine"
                    ),
                    to_attr="altri_docenti",
                ),
            )
            .select_related("tipologia")
            .only(
                "id",
                "nome_af",
                "ssd",
                "numero_ore",
                "cfu",
                "tipo_af",
                "rif_dottorato",
                "ciclo",
                "struttura_proponente",
                "struttura_proponente_origine",
                "contenuti_af",
                "prerequisiti",
                "num_min_studenti",
                "num_max_studenti",
                "verifica_finale",
                "modalita_verifica",
                "avvio",
                "fine",
                "orario_aule",
                "note",
                "visualizza_orario",
                "tipologia__nome_it",
                "tipologia__nome_en",
            )
        )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_ACTIVITIES_TYPES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(
            PhdActivitiesTypesSerializer(many=True)
        ),
    )
)
class PhdActivitiesTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhdActivitiesTypesSerializer
    queryset = (
        DidatticaDottoratoAttivitaFormativa.objects.filter(tipo_af__isnull=False)
        .order_by("tipo_af")
        .values("tipo_af")
        .distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_ACTIVITIES_TYPOLOGIES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(
            PhdActivitiesTypologiesSerializer(many=True)
        ),
    )
)
class PhdActivitiesTypologiesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhdActivitiesTypologiesSerializer
    queryset = DidatticaDottoratoAttivitaFormativaTipologia.objects.all()


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.PHD_SSD_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(PhdSsdSerializer(many=True)),
    )
)
class PhdSsdViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhdSsdSerializer
    queryset = (
        DidatticaDottoratoAttivitaFormativa.objects.filter(ssd__isnull=False)
        .order_by("ssd")
        .values("ssd")
        .distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.REF_PHD_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(RefPhdSerializer(many=True)),
    )
)
class RefPhdViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = RefPhdSerializer
    queryset = (
        DidatticaDottoratoAttivitaFormativa.objects.filter(rif_dottorato__isnull=False)
        .exclude(rif_dottorato__exact="")
        .order_by("rif_dottorato")
        .values("rif_dottorato")
        .distinct()
    )


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.REF_STRUCTURES_LIST_SUMMARY,
        responses=responses.COMMON_LIST_RESPONSES(RefStructuresSerializer(many=True)),
    )
)
class RefStructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = RefStructuresSerializer
    queryset = (
        DidatticaDottoratoAttivitaFormativa.objects.filter(
            struttura_proponente_origine__isnull=False
        )
        .exclude(struttura_proponente_origine__exact="")
        .order_by("struttura_proponente_origine")
        .values("struttura_proponente_origine")
        .distinct()
    )
