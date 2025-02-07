from generics.views import ApiEndpointDetail, ApiEndpointList

from .filters import CdsBrochuresListFilter
from .permissions import BrochureVisibilityPermission
from .serializers import CdsBrochureLightSerializer, CdsBrochureSerializer
from .services import ServiceCdsBrochure

from ...models import CdsBrochure
from ...settings import BROCHURES_VISIBLE, OFFICE_CDS_BROCHURE


class ApiCdsBrochureList(ApiEndpointList):
    description = "Retrieves a list of course of study brochures."
    permission_classes = [BrochureVisibilityPermission]
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
    permission_classes = [BrochureVisibilityPermission]
    serializer_class = CdsBrochureSerializer

    def get_queryset(self):
        cds_cod = self.kwargs["cds_cod"]
        return ServiceCdsBrochure.getCdsBrochure(cds_cod)
