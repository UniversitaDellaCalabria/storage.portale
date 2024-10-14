from cds.api.v1.serializers import ProgramTypesSerializer
from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.filters import OrderingFilter
from structures.api.v1.serializers import TerritorialScopesSerializer

from projects.settings import OFFICE_PROJECTS

from .filters import ProjectsListFilter
from .serializers import ProjectInfrastructuresSerializer, ProjectSerializer
from .services import ServiceProgetto


class ApiProjectsList(ApiEndpointList):
    description = "Retrieves a list of projects."
    serializer_class = ProjectSerializer
    filter_backends = [ProjectsListFilter, OrderingFilter]

    def get_queryset(self):
        request = self.request
        only_active = True

        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_PROJECTS,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False
        # end get active/all elements

        search = request.query_params.get("search")
        techarea = request.query_params.get("techarea")
        infrastructure = request.query_params.get("infrastructure")
        programtype = request.query_params.get("programtype")
        territorialscope = request.query_params.get("territorialscope")
        notprogramtype = request.query_params.get("-programtype")
        year = request.query_params.get("year")

        return ServiceProgetto.getProjects(
            search,
            techarea,
            infrastructure,
            programtype,
            territorialscope,
            notprogramtype,
            year,
            only_active,
        )


class ApiProjectDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a specific project."
    serializer_class = ProjectSerializer

    def get_queryset(self):
        projectid = self.kwargs["projectid"]
        return ServiceProgetto.getProjectDetail(projectid)


class ApiProjectsTerritorialScopesList(ApiEndpointList):
    description = "Retrieves a list of territorial scopes of projects."
    serializer_class = TerritorialScopesSerializer

    def get_queryset(self):
        return ServiceProgetto.getTerritorialScopes()


class ApiProjectsProgramTypesList(ApiEndpointList):
    description = "Retrieves a list of program types of projects."
    serializer_class = ProgramTypesSerializer

    def get_queryset(self):
        return ServiceProgetto.getProgramTypes()


class ApiProjectsInfrastructuresList(ApiEndpointList):
    description = "Retrieves a list of infrastructures of projects."
    serializer_class = ProjectInfrastructuresSerializer

    def get_queryset(self):
        return ServiceProgetto.getProjectInfrastructures()
