from django.db.models import (
    Prefetch,
    Value,
    Case,
    When,
)
from django.db.models.functions import Coalesce, Concat
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from .docs import descriptions
from api_docs import responses
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from cds_brochure.models import (
    CdsBrochure,
    CdsBrochureExStudenti,
    CdsBrochureLink,
    CdsBrochureSlider,
)

from .filters import BrochuresFilter 
from .serializers import (
    BrochuresListSerializer,
    BrochuresDetailSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary=descriptions.BROCHURE_LIST_SUMMARY,
        description=descriptions.BROCHURE_LIST_DESCRIPTION,
        responses=responses.COMMON_LIST_RESPONSES(BrochuresListSerializer(many=True)),
    ),
    retrieve=extend_schema(
        summary=descriptions.BROCHURE_RETRIEVE_SUMMARY,
        description=descriptions.BROCHURE_RETRIEVE_DESCRIPTION,
        responses=responses.COMMON_RETRIEVE_RESPONSES(BrochuresDetailSerializer),
        parameters=[
            OpenApiParameter(
                name="cds__cds_cod",
                type=str,
                pattern=r"^\d+$",
                required=True,
                description="A value identifying the cod of a Course of Study.",
                location=OpenApiParameter.PATH,
            )
        ],
    ),
)
class BrochuresViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrochuresFilter
    lookup_field = 'cds__cds_cod' 
    queryset = CdsBrochure.objects.select_related("cds").all()
    
    def get_serializer_class(self):
        return BrochuresListSerializer if self.action == 'list' else BrochuresDetailSerializer
    

    
    def get_queryset(self):
        if self.action == 'list':
            return (self.queryset.only(
                    "id",
                    "aa",
                    "cds__cds_cod",
                    "cds__nome_cds_it",
                    "cds__nome_cds_eng",
                )
            )
        
        if self.action == 'retrieve':
            return (self.queryset.filter(cds__cds_cod=self.kwargs.get('cds__cds_cod') )
                    .prefetch_related(
                        Prefetch(
                            "cdsbrochureexstudenti_set",
                            queryset=CdsBrochureExStudenti.objects.only(
                                "id",
                                "nome",
                                "ordine",
                                "profilo_it",
                                "profilo_en",
                                "link_it",
                                "link_en",
                                "foto",)
                            .order_by("ordine"),
                            to_attr="exStudenti"
                        ),
                        Prefetch(
                            "cdsbrochurelink_set",
                            queryset=CdsBrochureLink.objects.only(
                                "id",
                                "ordine",
                                "descrizione_link_it",
                                "descrizione_link_en",
                                "link_it",
                                "link_en",).order_by("ordine"),
                            to_attr="links"
                        ),
                        Prefetch(
                            "cdsbrochureslider_set",
                            queryset=CdsBrochureSlider.objects.only(
                               "id",
                                "ordine",
                                "slider_it",
                                "slider_en",).order_by("ordine"),
                            to_attr="sliders"
                        ),
                    )
                    .only(
                        "id",
                        "cds__cds_cod",
                        "aa",
                        "cds__nome_cds_it",
                        "cds__nome_cds_eng",
                        "cds__cla_miur_cod",
                        "cds__cla_miur_des",
                        "cds__intercla_miur_cod",
                        "cds__intercla_miur_des",
                        "cds__durata_anni",
                        "num_posti",
                        "descrizione_corso_it",
                        "descrizione_corso_en",
                        "accesso_corso_it",
                        "accesso_corso_en",
                        "obiettivi_corso_it",
                        "obiettivi_corso_en",
                        "sbocchi_professionali_it",
                        "sbocchi_professionali_en",
                        "tasse_contributi_esoneri_it",
                        "tasse_contributi_esoneri_en",
                        "borse_studio_it",
                        "borse_studio_en",
                        "agevolazioni_it",
                        "agevolazioni_en",
                        "corso_in_pillole_it",
                        "corso_in_pillole_en",
                        "cosa_si_studia_it",
                        "cosa_si_studia_en",
                        "come_iscriversi_it",
                        "come_iscriversi_en",
                    )
                    .annotate(
                        course_class = Case(
                            When(
                                cds__cla_miur_cod__isnull=False,
                                cds__cla_miur_des__isnull=False,
                                then=Concat(
                                    Coalesce("cds__cla_miur_cod", Value("")),
                                    Value(" "),
                                    Coalesce("cds__cla_miur_des", Value("")),
                                )
                            ),
                            default=Value(None),
                        ),
                        
                        course_interclass = Case(
                            When(
                                cds__intercla_miur_cod__isnull=False,
                                cds__intercla_miur_des__isnull=False,
                                then=Concat(
                                    Coalesce("cds__intercla_miur_cod", Value("")),
                                    Value(" "),
                                    Coalesce("cds__intercla_miur_des", Value("")),
                                )
                            ),
                            default=Value(None),
                        ),

                        
                    )
            )
        