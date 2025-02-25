from django.db.models import (
    OuterRef,
    Prefetch,
    Value,
)
from django.db.models.functions import Coalesce, Concat
from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     OpenApiParameter,
#     extend_schema,
#     extend_schema_view,
# )
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from cds.models import DidatticaCdsLingua, DidatticaRegolamentoAltriDati
from cds_brochure.models import (
    CdsBrochure,
)

from .filters import BrochuresFilter 
from .serializers import (
    BrochuresListSerializer,
    BrochuresDetailSerializer,
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
                            "cds__didatticaregolamentoaltridati_set",
                            queryset=DidatticaRegolamentoAltriDati.objects.filter(
                                regdid__cds__cds_cod=OuterRef('cds__cds_cod'),
                                regdid__aa_reg_did=OuterRef('aa'),
                                tipo_testo_regdid_cod = "URL_CDS_VIDEO"
                            )[:1],
                            to_attr="video_link"
                        ),
                        Prefetch(
                            "cds__didatticacdslingua_set",
                            queryset=DidatticaCdsLingua.objects
                            .filter(cdsord__cds_cod=OuterRef('cds__cds_cod'))
                            .only("iso6392_cod"),
                            to_attr="languages"
                        )
                    )
                    .values(
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
                        course_class = Concat(
                        Coalesce("cds__cla_miur_cod", Value("")),
                        Value(" "),
                        Coalesce("cds__cla_miur_des", Value("")),
                        ),
                        
                        course_interclass = Concat(
                            Coalesce("cds__intercla_miur_cod", Value("")),
                            Value(" "),
                            Coalesce("cds__intercla_miur_des", Value("")),
                        ),

                        
                    )
            )
        