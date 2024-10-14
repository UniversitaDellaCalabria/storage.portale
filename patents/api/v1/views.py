from generics.views import ApiEndpointDetail, ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.schemas.openapi_agid import AgidAutoSchema

from patents.settings import OFFICE_PATENTS

from .filters import PatentsListFilter
from .serializers import PatentsSerializer
from .services import ServiceBrevetto


class ApiPatentsList(ApiEndpointList):
    description = "Retrieves a list of patents."
    serializer_class = PatentsSerializer
    filter_backends = [PatentsListFilter]

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
    description = "Retrieves detailed information of a specifc patent."
    serializer_class = PatentsSerializer
    schema = AgidAutoSchema(tags=["public"], operation_id_base="Patent")

    def get_queryset(self):
        patentid = self.kwargs["patentid"]

        return ServiceBrevetto.getPatentDetail(patentid)
