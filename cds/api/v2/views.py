from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Case, When, Value, F
from django.db.models.functions import Concat

from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa, DidatticaRegolamento
from .serializers import (
    CdsSerializer,
    DegreeTypeSerializer,
    DidatticaAttivitaFormativaSerializer,
    StudyActivitiesListSerializer,
    StudyActivitiesDetailSerializer,
    AcademicYearsSerializer
)
from .filters import (
    CdsFilter,
    DegreeTypeFilter,
    DidatticaAttivitaFormativaFilter
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
    
    
class DidatticaAttivitaFormativaViewSet(ReadOnlyModelViewSet):
    serializer_class = DidatticaAttivitaFormativaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DidatticaAttivitaFormativaFilter 
    queryset = DidatticaAttivitaFormativa.objects.all()
    
    
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    filterset_class = DidatticaAttivitaFormativaFilter
    queryset = DidatticaAttivitaFormativa.objects.select_related("cds__dip", "matricola_resp_did").annotate(
                full_name=Concat(
                    F('matricola_resp_did__cognome'),
                    Value(' '),
                    F('matricola_resp_did__nome'),
                    Case(
                        When(matricola_resp_did__middle_name__isnull=False, then=Concat(Value(' '), F('matricola_resp_did__middle_name'))),
                        default=Value(''),
                        output_field=models.CharField()
                    ),
                    output_field=models.CharField()
                )
    )
    def get_serializer_class(self):
        if self.action == 'retrieve': 
            return StudyActivitiesDetailSerializer
        else:
            return StudyActivitiesListSerializer