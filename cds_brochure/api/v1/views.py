from cds.api.v1.services import ServiceDidatticaCds
from generics.views import ApiEndpointDetail, ApiEndpointList

from .filters import ApiCdsWebsitesListFilter
from .serializers import CdsWebsiteLightSerializer, CdsWebsiteSerializer


class ApiCdsWebsiteList(ApiEndpointList):
    description = "Restituisce l’elenco dei siti dei corsi di studio"
    serializer_class = CdsWebsiteLightSerializer
    filter_backends = [ApiCdsWebsitesListFilter]

    def get_queryset(self):
        search = self.request.query_params.get("search")
        return ServiceDidatticaCds.getCdsWebsites(search)


class ApiCdsWebsiteDetail(ApiEndpointDetail):
    description = "Restituisce il dettaglio di siti un corso di studio"
    serializer_class = CdsWebsiteSerializer
    filter_backends = []

    def get_queryset(self):
        cds_cod = self.kwargs["cdswebsitecod"]
        return ServiceDidatticaCds.getCdsWebsite(cds_cod)
