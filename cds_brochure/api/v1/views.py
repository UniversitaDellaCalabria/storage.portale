from generics.views import ApiEndpointDetail, ApiEndpointList

from organizational_area.models import OrganizationalStructureOfficeEmployee

from .filters import CdsBrochuresListFilter
from .serializers import CdsBrochureLightSerializer, CdsBrochureSerializer
from .services import ServiceCdsBrochure
from ...settings import BROCHURES_VISIBLE


class ApiCdsBrochureList(ApiEndpointList):
    description = "Retrieves a list of course of study brochures."
    serializer_class = CdsBrochureLightSerializer
    filter_backends = [CdsBrochuresListFilter]

    def get_queryset(self):
        if not BROCHURES_VISIBLE and not self.request.user.is_superuser:
            my_offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__name=OFFICE_CDS_BROCHURE,
                office__is_active=True,
                office__organizational_structure__is_active=True,
            ).exists()
            if not my_offices:
                return CdsBrochure.objects.none()
        search = self.request.query_params.get("search")
        academic_year = self.request.query_params.get("academic_year")
        return ServiceCdsBrochure.getCdsBrochures(search, academic_year)


class ApiCdsBrochureDetail(ApiEndpointDetail):
    description = "Retrieves detailed information about the brochure of a specific course of study."
    serializer_class = CdsBrochureSerializer

    def get_queryset(self):
        cds_cod = self.kwargs["cds_cod"]
        return ServiceCdsBrochure.getCdsBrochure(cds_cod)
