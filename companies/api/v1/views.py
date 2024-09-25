from companies.settings import OFFICE_COMPANIES
from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee

from .filters import ApiCompaniesListFilter
from .serializers import CompaniesSerializer, TechAreasSerializer
from .services import ServiceCompany


class ApiCompaniesList(ApiEndpointList):
    description = "La funzione restituisce la lista degli spin-off"
    serializer_class = CompaniesSerializer
    filter_backends = [ApiCompaniesListFilter]

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
    description = "La funzione restituisce un particolare spinoff/startup"
    serializer_class = CompaniesSerializer
    filter_backends = []

    def get_queryset(self):
        companyid = self.kwargs["companyid"]

        return ServiceCompany.getCompanyDetail(companyid)


class ApiTechAreasList(ApiEndpointList):
    description = "La funzione restituisce la lista delle aree tecnologiche"
    serializer_class = TechAreasSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceCompany.getTechAreas()
