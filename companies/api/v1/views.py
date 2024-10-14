from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.schemas.openapi_agid import AgidAutoSchema

from companies.settings import OFFICE_COMPANIES

from .filters import CompaniesListFilter
from .serializers import CompaniesSerializer, TechAreasSerializer
from .services import ServiceCompany


class ApiCompaniesList(ApiEndpointList):
    description = "Retrieves spinoffs/startups."
    serializer_class = CompaniesSerializer
    filter_backends = [CompaniesListFilter]

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
                office__name=OFFICE_COMPANIES,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False
        # end get active/all elements

        search = request.query_params.get("search")
        techarea = request.query_params.get("techarea")
        spinoff = request.query_params.get("spinoff")
        startup = request.query_params.get("startup")
        departments = request.query_params.get("departments")

        return ServiceCompany.getCompanies(
            search, techarea, spinoff, startup, departments, only_active
        )


class ApiCompanyDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a specific spinoff/startup."
    serializer_class = CompaniesSerializer
    schema = AgidAutoSchema(tags=["public"], operation_id_base="Company")

    def get_queryset(self):
        companyid = self.kwargs["companyid"]

        return ServiceCompany.getCompanyDetail(companyid)


class ApiTechAreasList(ApiEndpointList):
    description = "Retrieves a list of technology areas."
    serializer_class = TechAreasSerializer

    def get_queryset(self):
        return ServiceCompany.getTechAreas()
