from generics.views import ApiEndpointDetail, ApiEndpointList
from rest_framework.schemas.openapi_agid import AgidAutoSchema

from .filters import HighFormationMastersListFilter
from .serializers import (
    ErogationModesSerializer,
    HighFormationCourseTypesSerializer,
    HighFormationMastersSerializer,
)
from .services import ServiceAltaFormazione


class ApiHighFormationMastersList(ApiEndpointList):
    description = "Retrieves the list of high-formation masters."
    serializer_class = HighFormationMastersSerializer
    filter_backends = [HighFormationMastersListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        director = request.query_params.get("director")
        coursetype = request.query_params.get("coursetype")
        erogation = request.query_params.get("erogation")
        department = request.query_params.get("department")
        language = request.query_params.get("language")
        year = request.query_params.get("year")

        return ServiceAltaFormazione.getHighFormationMasters(
            search, director, coursetype, erogation, department, language, year
        )


class ApiHighFormationMastersDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a high-formation master."
    serializer_class = HighFormationMastersSerializer
    schema = AgidAutoSchema(tags=["public"], operation_id_base="HighFormationMaster")

    def get_queryset(self):
        master_id = self.kwargs["id"]
        return ServiceAltaFormazione.getHighFormationMaster(master_id)


class ApiHighFormationCourseTypesList(ApiEndpointList):
    description = "Retrieves the list of high-formation course types."
    serializer_class = HighFormationCourseTypesSerializer

    def get_queryset(self):
        return ServiceAltaFormazione.getHighFormationCourseTypes()


class ApiErogationModesList(ApiEndpointList):
    description = "Retrieves the list of erogation modes."
    serializer_class = ErogationModesSerializer

    def get_queryset(self):
        return ServiceAltaFormazione.getErogationModes()
