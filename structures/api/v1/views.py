from addressbook.api.v1.services import ServicePersonale
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport
from structures.api.v1.filters import ApiStructuresListFilter

from .serializers import (
    DepartmentSerializer,
    StructureDetailSerializer,
    StructureFunctionsSerializer,
    StructuresSerializer,
    StructureTypesSerializer,
)
from .services import ServiceDipartimento


class ApiDepartmentsList(ApiEndpointList):
    description = "La funzione restituisce la lista dei dipartimenti"
    serializer_class = DepartmentSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDipartimento.getDepartmentsList(self.language)


class ApiDepartmentDetail(ApiEndpointDetail):
    description = "La funzione restituisce uno specifico dipartimento"
    serializer_class = DepartmentSerializer
    filter_backends = []

    def get_queryset(self):
        departmentcod = self.kwargs["departmentcod"]
        return ServiceDipartimento.getDepartment(departmentcod)


class ApiStructuresList(ApiEndpointList):
    description = "La funzione restituisce le strutture organizzative"
    serializer_class = StructuresSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        father = request.query_params.get("father")
        depth = request.query_params.get("depth")
        type = request.query_params.get("type")
        return ServicePersonale.getStructuresList(search, father, type, depth)


class ApiStructureTypesList(ApiEndpointListSupport):
    description = "La funzione restituisce le tipologie di strutture organizzative"
    serializer_class = StructureTypesSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        father = self.request.query_params.get("father")
        return ServicePersonale.getStructureTypes(father)


class ApiStructureDetail(ApiEndpointDetail):
    description = "La funzione restituisce una specifica struttura"
    serializer_class = StructureDetailSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        structureid = self.kwargs["structureid"]
        return ServicePersonale.getStructure(structureid)


class ApiStructureFunctionsList(ApiEndpointList):
    description = (
        "La funzione restituisce la lista delle funzioni della unità organizzativa"
    )
    serializer_class = StructureFunctionsSerializer
    filter_backends = []

    def get_queryset(self):
        return ServicePersonale.getStructureFunctions()
