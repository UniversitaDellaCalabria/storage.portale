from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from patents.settings import OFFICE_PATENTS

from .filters import ApiPatentsListFilter
from .serializers import PatentsSerializer
from .services import ServiceBrevetto


class ApiPatentsList(ApiEndpointList):
    description = "La funzione restituisce la lista dei brevetti"
    serializer_class = PatentsSerializer
    filter_backends = [ApiPatentsListFilter]

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
                office__name=OFFICE_PATENTS,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            )
            if my_offices.exists():
                only_active = False
        # end get active/all elements

        search = request.query_params.get("search")
        techarea = request.query_params.get("techarea")
        structure = request.query_params.get("structure")

        return ServiceBrevetto.getPatents(search, techarea, structure, only_active)


class ApiPatentDetail(ApiEndpointDetail):
    description = "La funzione restituisce uno specifico brevetto"
    serializer_class = PatentsSerializer
    filter_backends = []

    def get_queryset(self):
        patentid = self.kwargs["patentid"]

        return ServiceBrevetto.getPatentDetail(patentid)
