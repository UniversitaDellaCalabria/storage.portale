from cds.api.v1.services import ServiceDidatticaCds
from generics.views import ApiEndpointDetail, ApiEndpointList

from .filters import ApiHighFormationMastersListFilter
from .serializers import (
    HighFormationCourseTypesSerializer,
    HighFormationMastersSerializer,
)


class ApiHighFormationMastersDetail(ApiEndpointDetail):
    description = "La funzione restituisce il dettaglio di un master"
    serializer_class = HighFormationMastersSerializer
    filter_backends = [ApiHighFormationMastersListFilter]

    def get_queryset(self):
        master_id = self.kwargs["id"]
        return ServiceDidatticaCds.getHighFormationMaster(master_id)


class ApiHighFormationCourseTypesList(ApiEndpointList):
    description = (
        "La funzione restituisce la lista dei tipi di corso dell'alta formazione"
    )
    serializer_class = HighFormationCourseTypesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDidatticaCds.getHighFormationCourseTypes()


class ApiHighFormationMastersList(ApiEndpointList):
    description = "La funzione restituisce i master alta formazione"
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
