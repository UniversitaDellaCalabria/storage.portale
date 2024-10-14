from .services import ServiceCdsBrochure
from generics.views import ApiEndpointDetail, ApiEndpointList

from .filters import CdsBrochuresListFilter
from .serializers import CdsBrochureLightSerializer, CdsBrochureSerializer


class ApiCdsBrochureList(ApiEndpointList):
    description = "Retrieves a list of course of study brochures."
    serializer_class = CdsBrochureLightSerializer
    filter_backends = [CdsBrochuresListFilter]

    def get_queryset(self):
        search = self.request.query_params.get("search")
        return ServiceCdsBrochure.getCdsBrochures(search)


class ApiCdsBrochureDetail(ApiEndpointDetail):
    description = "Retrieves detailed information about the brochure of a specific course of study."
    serializer_class = CdsBrochureSerializer

    def get_queryset(self):
        cds_cod = self.kwargs["cds_cod"]
        return ServiceCdsBrochure.getCdsBrochure(cds_cod)
