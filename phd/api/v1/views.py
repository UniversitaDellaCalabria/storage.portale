from generics.views import ApiEndpointDetail, ApiEndpointList
from phd.settings import PHD_CYCLES
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ApiPhdListFilter
from .serializers import (
    PhdActivitiesSerializer,
    PhdActivityTypeSerializer,
    PhdActivityTypologySerializer,
    PhdSerializer,
    PhdSsdListSerializer,
    RefPhdSerializer,
    RefStructuresSerializer,
)
from .services import ServiceDottorato


class ApiPhdList(ApiEndpointList):
    description = "La funzione restituisce una lista di dottorati"
    serializer_class = PhdSerializer
    filter_backends = [ApiPhdListFilter]

    def get_queryset(self):
        return ServiceDottorato.getPhd(self.request.query_params)


class ApiPhdCycles(APIView):
    def get(self, request):
        result = {}
        for cycle in PHD_CYCLES:
            result[cycle[0]] = cycle[1]
        return Response(result)


class ApiPhdActivitiesList(ApiEndpointList):
    description = "La funzione restituisce la lista delle attività dei dottorati"
    serializer_class = PhdActivitiesSerializer
    filter_backends = []

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        structure = request.query_params.get("structure")
        phd = request.query_params.get("phd")
        cycle = request.query_params.get("cycle")
        ssd = request.query_params.get("ssd")
        teacher = request.query_params.get("teacher")
        typology = request.query_params.get("typology")

        return ServiceDottorato.getPhdActivities(
            search, structure, phd, ssd, teacher, cycle, typology
        )


class ApiPhdActivityDetail(ApiEndpointDetail):
    description = (
        "La funzione restituisce il dettaglio di una attività riferita ad un dottorato"
    )
    serializer_class = PhdActivitiesSerializer
    filter_backends = []

    def get_queryset(self):
        activity_id = self.kwargs["id"]
        return ServiceDottorato.getPhdActivity(activity_id)


class ApiRefPhdList(ApiEndpointList):
    description = "La funzione restituisce la lista dei dottorati di riferimento"
    serializer_class = RefPhdSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getRefPhd()


class ApiRefStructuresList(ApiEndpointList):
    description = "La funzione restituisce la lista delle strutture di riferimento"
    serializer_class = RefStructuresSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getRefStructures()


class ApiPhdSsdList(ApiEndpointList):
    description = "La funzione restituisce la lista degli ssd dei dottorati"
    serializer_class = PhdSsdListSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdSsdList()


class ApiPhdActivityTypeList(ApiEndpointList):
    description = "La funzione restituisce la lista dei tipi di attività di dottorato"
    serializer_class = PhdActivityTypeSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypeList()


class ApiPhdActivityTypologies(ApiEndpointList):
    description = (
        "La funzione restituisce la lista delle tipologie di attività di dottorato"
    )
    serializer_class = PhdActivityTypologySerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypologies()
