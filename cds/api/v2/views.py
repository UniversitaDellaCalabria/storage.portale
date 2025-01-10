from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Case, When, Value, F, Subquery, OuterRef
from django.db.models.functions import Concat

from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa, DidatticaRegolamento, DidatticaCopertura
from .serializers import (
    CdsSerializer,
    DegreeTypeSerializer,
    StudyActivitiesListSerializer,
    StudyActivitiesDetailSerializer,
    AcademicYearsSerializer
)
from .filters import (
    CdsFilter,
    DegreeTypeFilter,
    StudyActivitiesFilter
)

class CdsViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsFilter
    queryset = DidatticaCds.objects.all()


class DegreeTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = DegreeTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DegreeTypeFilter
    queryset = DidatticaCdsTipoCorso.objects.all()
    
class AcademicYearsViewSet(ReadOnlyModelViewSet):
    serializer_class = AcademicYearsSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = DidatticaRegolamento.objects.all()
    
    def get_queryset(self):
        return DidatticaRegolamento.objects.values('aa_reg_did').distinct().order_by('-aa_reg_did')
    
    
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudyActivitiesFilter 
    queryset = DidatticaAttivitaFormativa.objects.select_related("cds__dip", "matricola_resp_did").annotate(
                full_name=Concat(
                    Case(
                        When(matricola_resp_did__cognome__isnull=True, then=Value('')),
                    ),
                    F('matricola_resp_did__cognome'),
                    Value(' '),
                    F('matricola_resp_did__nome'),
                    Case(
                        When(matricola_resp_did__middle_name__isnull=False, then=Concat(Value(' '), F('matricola_resp_did__middle_name'))),
                        default=Value(''),
                        output_field=models.CharField()
                    ),
                    output_field=models.CharField()
                ),
                
                group_description=Concat(
                    F('des'),
                    Case(
                        When(part_stu_des__isnull=False, then=Concat(Value(" ("), F('part_stu_des'), Value(")")))
                    ),
                    output_field=models.CharField()
                ),
                
                father=F('des'),
                
                af_gen_cod_fallback=Subquery(
                    DidatticaCopertura.objects.filter(
                        af_id=OuterRef('af_id')
                    ).values('af_gen_cod')[:1]
                ),
                
                anno_corso_fallback=Subquery(
                    DidatticaCopertura.objects.filter(
                        af_id=OuterRef('af_id')
                    ).values('anno_corso')[:1]
                ),
                
                ciclo_des_fallback=Subquery(
                    DidatticaCopertura.objects.filter(
                        af_id=OuterRef('af_id')
                    ).values('ciclo_des')[:1]
                ),
                
    ).annotate(
        # Gestiamo i valori null usando Case/When
        af_gen_cod_final=Case(
            When(af_gen_cod__isnull=True, then=F('af_gen_cod_fallback')),
            default=F('af_gen_cod'),
            output_field=models.CharField()
        ),
        anno_corso_final=Case(
            When(anno_corso__isnull=True, then=F('anno_corso_fallback')),
            default=F('anno_corso'),
            output_field=models.IntegerField()
        ),
        ciclo_des_final=Case(
            When(ciclo_des__isnull=True, then=F('ciclo_des_fallback')),
            default=F('ciclo_des'),
            output_field=models.CharField()
        )
    ).distinct().order_by("des")
    
    
    def get_serializer_class(self):
        if self.action == 'retrieve': 
            return StudyActivitiesDetailSerializer
        else:
            return StudyActivitiesListSerializer
                    
            
    