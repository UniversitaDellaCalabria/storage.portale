from generics.views import ApiEndpointDetail, ApiEndpointList

from organizational_area.models import OrganizationalStructureOfficeEmployee

from .filters import CdsBrochuresListFilter
from .serializers import CdsBrochureLightSerializer, CdsBrochureSerializer
from .services import ServiceCdsBrochure

from ...models import CdsBrochure
from ...settings import BROCHURES_VISIBLE, OFFICE_CDS_BROCHURE


def _access_granted(user):
    if BROCHURES_VISIBLE:
        return True
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    belongs_to_office = OrganizationalStructureOfficeEmployee.objects.filter(
        employee=user,
        office__name=OFFICE_CDS_BROCHURE,
        office__is_active=True,
        office__organizational_structure__is_active=True,
    ).exists()
    return belongs_to_office


class ApiCdsBrochureList(ApiEndpointList):
    description = "Retrieves a list of course of study brochures."
    serializer_class = CdsBrochureLightSerializer
    filter_backends = [CdsBrochuresListFilter]

    def get_queryset(self):
        request = self.request
        if not _access_granted(request.user):
            return CdsBrochure.objects.none()
        search = request.query_params.get("search")
        academic_year = request.query_params.get("academic_year")
        return ServiceCdsBrochure.getCdsBrochures(search, academic_year)


class ApiCdsBrochureDetail(ApiEndpointDetail):
    description = "Retrieves detailed information about the brochure of a specific course of study."
    serializer_class = CdsBrochureSerializer

    def get_queryset(self):
        if not _access_granted(self.request.user):
            return CdsBrochure.objects.none()
        cds_cod = self.kwargs["cds_cod"]
        return ServiceCdsBrochure.getCdsBrochure(cds_cod)
