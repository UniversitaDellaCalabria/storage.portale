from rest_framework.viewsets import ReadOnlyModelViewSet
from cds.models import DidatticaCds
from .serializers import CdsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CdsFilter
from generics.pagination import UnicalStorageApiPaginationList



class CdsViewSet(ReadOnlyModelViewSet):
    serializer_class = CdsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CdsFilter
    # pagination_class = UnicalStorageApiPaginationList
    queryset = DidatticaCds.objects.all()
