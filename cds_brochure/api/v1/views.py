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
        return ServiceCdsBrochure.getCdsBrochures(language=self.language,
                                                  query_params=self.request.query_params)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        return super().get(*args, **kwargs)


class ApiCdsBrochureDetail(ApiEndpointDetail):
    description = "Retrieves detailed information about the brochure of a specific course of study."
    permission_classes = [BrochureVisibilityPermission]
    serializer_class = CdsBrochureSerializer

    def get_queryset(self):
        cds_cod = self.kwargs["cds_cod"]
        return ServiceCdsBrochure.getCdsBrochure(cds_cod)
