from django.db.models import (
    Prefetch,
    Value,
    Case,
    When,
    Q,
    CharField,
    F,
)
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
from cds_websites.settings import OFFICE_CDS_WEBSITES

from .serializers import (
    TopicListSerialzer,
    ArticlesTopicSerializer,
)
from cds_websites.models import (
    SitoWebCdsTopic,
    SitoWebCdsTopicArticoliRegAltriDati,
    SitoWebCdsSubArticoliRegolamento,
    SitoWebCdsTopicArticoliReg,
)

from django.db.models import OuterRef, Subquery


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.TOPIC_LIST_SUMMARY,
        description=descriptions.TOPIC_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(TopicListSerialzer(many=True)),
    ),
)
class TopicListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TopicListSerialzer
    queryset = SitoWebCdsTopic.objects.only(
        "id", "descr_topic_it", "descr_topic_en", "visibile"
    ).distinct()


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.ARTICLESTOPIC_LIST_SUMMARY,
        description=descriptions.ARTICLESTOPIC_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(ArticlesTopicSerializer(many=True)),
    ),
)
class ArticlesTopicListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ClearResponseViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = ArticlesTopicSerializer

    def get_queryset(self):
        cds_cod = self.kwargs.get("cds_cod")
        topic_id = self.kwargs.get("topic_id")

        topic_id_list = topic_id.split(",")

        only_active = True
        if self.request.user.is_superuser:
            only_active = False  # pragma: no cover
        elif self.request.user.is_authenticated:  # pragma: no cover
            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=self.request.user,
                office__is_active=True,
                office__name=OFFICE_CDS_WEBSITES,
                office__organizational_structure__is_active=True,
            )

            if offices.exists():
                only_active = False

        query_visibile = Q(visibile=True) if only_active else Q()
        query_topic_id = Q(sito_web_cds_topic__id__in=topic_id_list)
        query_cds_cod = Q(
            didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds__cds_cod=str(
                cds_cod
            )
        ) | Q(sito_web_cds_oggetti_portale__cds__cds_cod=str(cds_cod))

        articoli_reg_altri_dati_qs = (
            SitoWebCdsTopicArticoliRegAltriDati.objects.filter(query_visibile)
            .select_related("sito_web_cds_tipo_dato")
            .defer("dt_mod", "user_mod", "sito_web_cds_tipo_dato__descr_lunga")
            .annotate(
                type_id=F("sito_web_cds_tipo_dato__id"),
                type=F("sito_web_cds_tipo_dato__descr_breve"),
            )
        )

        sub_articoli_qs = SitoWebCdsSubArticoliRegolamento.objects.filter(
            query_visibile
        ).defer("dt_mod", "user_mod")

        return (
            SitoWebCdsTopicArticoliReg.objects.prefetch_related(
                Prefetch(
                    "sitowebcdstopicarticoliregaltridati_set",
                    queryset=articoli_reg_altri_dati_qs,
                ),
                Prefetch(
                    "sitowebcdssubarticoliregolamento_set", queryset=sub_articoli_qs
                ),
            )
            .select_related(
                "sito_web_cds_oggetti_portale__cds",
                "didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds",
                "sito_web_cds_topic",
            )
            .filter(query_topic_id, query_cds_cod, query_visibile)
            .only(
                "id",
                "titolo_it",
                "titolo_en",
                "testo_it",
                "testo_en",
                "visibile",
                "ordine",
                "sito_web_cds_topic__id",
                "sito_web_cds_topic__descr_topic_it",
                "sito_web_cds_topic__descr_topic_en",
                "sito_web_cds_oggetti_portale__id",
                "sito_web_cds_oggetti_portale__id_classe_oggetto_portale",
                "sito_web_cds_oggetti_portale__id_oggetto_portale",
                "sito_web_cds_oggetti_portale__aa_regdid_id",
                "sito_web_cds_oggetti_portale__testo_it",
                "sito_web_cds_oggetti_portale__testo_en",
                "sito_web_cds_oggetti_portale__cds__cds_cod",
                "didattica_cds_articoli_regolamento__id",
                "didattica_cds_articoli_regolamento__didattica_cds_articoli_regolamento_testata__cds__cds_cod",
            )
            .annotate(
                tipo=Case(
                    When(
                        didattica_cds_articoli_regolamento__isnull=False,
                        then=Value("Article"),
                    ),
                    default=Value("Object"),
                    output_field=CharField(),
                )
            )
            .order_by("sito_web_cds_topic__id", "ordine")
        )


