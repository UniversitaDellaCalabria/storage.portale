from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

from rest_framework.pagination import PageNumberPagination

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import mixins, viewsets
from addressbook.utils import append_email_addresses

from .filters import (
    TeachersFilter,
    CoveragesFilter
)
from .serializers import (
    TeachersSerializer
)

from django.db.models import Prefetch, Q, OuterRef, Subquery
from addressbook.models import Personale
from structures.models import DidatticaDipartimento

class TeachersViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersSerializer
    filterset_class = TeachersFilter

    def get_queryset(self):
        dip_des_it_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_it")[:1] 
        
        dip_des_eng_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_eng")[:1]
        
        dip_id_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_id")[:1]
        
        dip_cod_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_cod")[:1] 

        query = (
            Personale.objects.filter(
                Q(fl_docente=1) | (Q(didatticacopertura__af__isnull=False) & ~Q(didatticacopertura__stato_coper_cod='R')))
            .annotate(
                dip_id=dip_id_subquery,
                dip_cod=dip_cod_subquery,
                dip_des_it=dip_des_it_subquery,
                dip_des_eng=dip_des_eng_subquery,
            )
            .values(
                "id_ab",
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "ds_ruolo_locale",
                "cd_ssd",
                "cd_uo_aff_org",
                "ds_ssd",
                "cv_full_it",
                "cv_short_it",
                "cv_full_eng",
                "cv_short_eng",
                "profilo",
                "ds_profilo",
                "ds_profilo_breve",
                "dip_id",
                "dip_cod",
                "dip_des_it",
                "dip_des_eng",
                "email",
            )
            .order_by("cognome", "nome", "middle_name")
            .distinct()
        )
        
        append_email_addresses(query, "id_ab")

        return query
    
    
class CoveragesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = TeachersSerializer
    filterset_class = CoveragesFilter

    def get_queryset(self):
        dip_des_it_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_it")[:1] 
        
        dip_des_eng_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_des_eng")[:1]
        
        dip_id_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_id")[:1]
        
        dip_cod_subquery = DidatticaDipartimento.objects.filter(
            dip_cod=OuterRef("cd_uo_aff_org")
        ).values("dip_cod")[:1] 

        query = (
            Personale.objects.filter(didatticacopertura__af__isnull=False)
            .exclude(didatticacopertura__stato_coper_cod='R')
            .annotate(
                dip_id=dip_id_subquery,
                dip_cod=dip_cod_subquery,
                dip_des_it=dip_des_it_subquery,
                dip_des_eng=dip_des_eng_subquery,
            )
            .values(
                "id_ab",
                "matricola",
                "nome",
                "middle_name",
                "cognome",
                "cd_ruolo",
                "ds_ruolo_locale",
                "cd_ssd",
                "cd_uo_aff_org",
                "ds_ssd",
                "cv_full_it",
                "cv_short_it",
                "cv_full_eng",
                "cv_short_eng",
                "profilo",
                "ds_profilo",
                "ds_profilo_breve",
            )
            .order_by("cognome", "nome", "middle_name")
            .distinct()
        )
        
        append_email_addresses(query, "id_ab")

        return query
    
  