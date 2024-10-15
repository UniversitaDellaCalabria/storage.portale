from generics.views import ApiEndpointDetail, ApiEndpointList
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from rest_framework.views import APIView

from phd.settings import PHD_CYCLES

from .filters import PhdActivitiesListFilter, PhdListFilter
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
    description = "Retrieves a list of PhDs."
    serializer_class = PhdSerializer
    filter_backends = [PhdListFilter]

    def get_queryset(self):
        return ServiceDottorato.getPhd(self.request.query_params)


class ApiPhdCycles(APIView):
    description = "Retrieves a list of PhD cycles."
    schema = AgidAutoSchema(tags=["public"])

    def get(self, request):
        result = {}
        for cycle in PHD_CYCLES:
            result[cycle[0]] = cycle[1]
        return Response(result)


class ApiPhdActivitiesList(ApiEndpointList):
    description = "Retrieves a list of activities of PhD programs."
    serializer_class = PhdActivitiesSerializer
    filter_backends = [PhdActivitiesListFilter]

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
    description = "Retrieves detailed information about an activity of a PhD program."
    serializer_class = PhdActivitiesSerializer
    schema = AgidAutoSchema(tags=["public"], operation_id_base="PhdActivity")

    def get_queryset(self):
        activity_id = self.kwargs["id"]
        return ServiceDottorato.getPhdActivity(activity_id)


class ApiRefPhdList(ApiEndpointList):
    description = "Retrieves a list of names of PhD programs."
    serializer_class = RefPhdSerializer

    def get_queryset(self):
        return ServiceDottorato.getRefPhd()


class ApiRefStructuresList(ApiEndpointList):
    description = "Retrieves a list of proposing structures of PhDs programs."
    serializer_class = RefStructuresSerializer

    def get_queryset(self):
        return ServiceDottorato.getRefStructures()


class ApiPhdSsdList(ApiEndpointList):
    description = (
        "Retrieves a list of SSDs (Scientific Disciplinary Sectors) of PhD programs."
    )
    serializer_class = PhdSsdListSerializer

    def get_queryset(self):
        return ServiceDottorato.getPhdSsdList()


class ApiPhdActivityTypeList(ApiEndpointList):
    description = "Retrieves a list of types of activities of PhD programs."
    serializer_class = PhdActivityTypeSerializer

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypeList()


class ApiPhdActivityTypologies(ApiEndpointList):
    description = "Retrieves a list of typologies of activities of PhD programs."
    serializer_class = PhdActivityTypologySerializer

    def get_queryset(self):
        return ServiceDottorato.getPhdActivityTypologies()
