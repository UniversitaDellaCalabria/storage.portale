from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Case, When, Value, F
from django.db.models.functions import Concat

from cds.models import DidatticaCds, DidatticaCdsTipoCorso, DidatticaAttivitaFormativa
from .serializers import (
    CdsSerializer,
    DegreeTypeSerializer,
    DidatticaAttivitaFormativaSerializer,
    StudyActivitiesSerializer
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
    
    
class DidatticaAttivitaFormativaViewSet(ReadOnlyModelViewSet):
    serializer_class = DidatticaAttivitaFormativaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DidatticaAttivitaFormativaFilter 
    queryset = DidatticaAttivitaFormativa.objects.all()
    
    
class StudyActivitiesViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = StudyActivitiesSerializer
    filter_backends = [DjangoFilterBackend]
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