from generics.utils import decrypt
from generics.views import ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from research_lines.settings import OFFICE_RESEARCH_LINES
from teachers.api.v1.services import ServiceDocente

from .filters import (
    AllResearchLinesListFilter,
    ResearchLinesListFilter,
)
from .serializers import (
    AllResearchLinesSerializer,
    AppliedResearchLinesSerializer,
    BaseResearchLinesSerializer,
)


class ApiBaseResearchLinesList(ApiEndpointList):
    description = "Retrieves a list of base reasearch lines."
    serializer_class = BaseResearchLinesSerializer
    filter_backends = [ResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacher = decrypt(self.request.query_params.get("teacher"))
        department = request.query_params.get("department")
        year = request.query_params.get("year")

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        return ServiceDocente.getBaseResearchLines(
            search, teacher, department, year, only_active
        )


class ApiAppliedResearchLinesList(ApiEndpointList):
    description = "Retrieves a list of applied reasearch lines."
    serializer_class = AppliedResearchLinesSerializer
    filter_backends = [ResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        teacher = decrypt(self.request.query_params.get("teacher"))
        department = request.query_params.get("department")
        year = request.query_params.get("year")

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        return ServiceDocente.getAppliedResearchLines(
            search, teacher, department, year, only_active
        )


class ApiAllResearchLinesList(ApiEndpointList):
    description = "Retrieves a list of all research lines."
    serializer_class = AllResearchLinesSerializer
    filter_backends = [AllResearchLinesListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        year = request.query_params.get("year")
        department = request.query_params.get("department")
        ercs = request.query_params.get("ercs")
        asters = request.query_params.get("asters")
        exclude_base = request.query_params.get("exclude_base")
        exclude_applied = request.query_params.get("exclude_applied")

        only_active = True
        # get only active elements if public
        # get all elements if in CRUD backend
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        if request.user.is_authenticated:  # pragma: no cover
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_RESEARCH_LINES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False

        return ServiceDocente.getAllResearchLines(
            search,
            year,
            department,
            ercs,
            asters,
            exclude_base,
            exclude_applied,
            only_active,
        )
