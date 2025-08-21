from addressbook.api.v1.services import ServicePersonale
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport

from structures.api.v1.filters import StructuresListFilter, StructureTypesListFilter

from .schemas import StructureDetailSchema
from .serializers import (
    DepartmentSerializer,
    StructureDetailSerializer,
    StructureFunctionsSerializer,
    StructuresSerializer,
    StructureTypesSerializer,
)
from .services import ServiceDipartimento


class ApiDepartmentsList(ApiEndpointList):
    description = "Retrieves a list of departments."
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return ServiceDipartimento.getDepartmentsList(self.language)


class ApiDepartmentDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a department."
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        departmentcod = self.kwargs["departmentcod"]
        return ServiceDipartimento.getDepartment(departmentcod)


class ApiStructuresList(ApiEndpointList):
    description = "Retrieves a list of orgranizational structures."
    serializer_class = StructuresSerializer
    filter_backends = [StructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        father = request.query_params.get("father")
        depth = request.query_params.get("depth")
        type = request.query_params.get("type")
        return ServicePersonale.getStructuresList(search, father, type, depth)


class ApiStructureTypesList(ApiEndpointListSupport):
    description = "Retrieves a list of typologies of organizational structures."
    serializer_class = StructureTypesSerializer
    filter_backends = [StructureTypesListFilter]

    def get_queryset(self):
        father = self.request.query_params.get("father")
        return ServicePersonale.getStructureTypes(father)


class ApiStructureDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a specific organizational structure."
    serializer_class = StructureDetailSerializer
    #schema = StructureDetailSchema(tags=['public'])

    def get_queryset(self):
        structureid = self.kwargs["structureid"]
        return ServicePersonale.getStructure(structureid)


class ApiStructureFunctionsList(ApiEndpointList):
    description = "Retrieves a list of functions of organizational structures."
    serializer_class = StructureFunctionsSerializer

    def get_queryset(self):
        return ServicePersonale.getStructureFunctions()
