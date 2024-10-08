from cds.api.v1.services import ServiceDidatticaCds
from generics.views import ApiEndpointDetail, ApiEndpointList

from .filters import ApiHighFormationMastersListFilter
from .serializers import (
    HighFormationCourseTypesSerializer,
    HighFormationMastersSerializer,
)


class ApiHighFormationMastersList(ApiEndpointList):
    description = "Returns the list of high-formation masters."
    serializer_class = HighFormationMastersSerializer
    filter_backends = [ApiHighFormationMastersListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        director = request.query_params.get("director")
        coursetype = request.query_params.get("coursetype")
        erogation = request.query_params.get("erogation")
        department = request.query_params.get("department")
        language = request.query_params.get("language")
        year = request.query_params.get("year")

        return ServiceDidatticaCds.getHighFormationMasters(
            search, director, coursetype, erogation, department, language, year
        )


class ApiHighFormationMastersDetail(ApiEndpointDetail):
    description = "Returns the details of a high-formation master."
    serializer_class = HighFormationMastersSerializer

    def get_queryset(self):
        master_id = self.kwargs["id"]
        return ServiceDidatticaCds.getHighFormationMaster(master_id)


class ApiHighFormationCourseTypesList(ApiEndpointList):
    description = "Returns the list of high-formation course types."
    serializer_class = HighFormationCourseTypesSerializer

    def get_queryset(self):
        return ServiceDidatticaCds.getHighFormationCourseTypes()
