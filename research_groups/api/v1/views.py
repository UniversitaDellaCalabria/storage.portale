from generics.views import ApiEndpointList
from teachers.api.v1.services import ServiceDocente

from .filters import ResearchGroupsListFilter
from .serializers import AllResearchGroupsSerializer


class ApiResearchGroupsList(ApiEndpointList):
    description = (
        "Retrieves a list of research groups ordered by name."
    )
    serializer_class = AllResearchGroupsSerializer
    filter_backends = [ResearchGroupsListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        department = request.query_params.get("department")
        cod = request.query_params.get("coderc1")
        teacher = request.query_params.get("teacher")
        return ServiceDocente.getAllResearchGroups(
            search=search, teacher=teacher, department=department, cod=cod
        )
