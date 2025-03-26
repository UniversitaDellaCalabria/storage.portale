from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )
# from .docs import descriptions
# from api_docs import responses

from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets

# from .filters import CompaniesFilter
from .serializers import (
    LaboratoriesAreaSerializer,
    LaboratoriesScopesSerializer,
    InfrastructuresSerializer,
    Erc0ListSerializer,
    Erc1ListSerializer,
    Erc2ListSerializer,
    Aster1ListSerializer,
    Aster2ListSerializer
)

from laboratories.models import (
    LaboratorioAltriDipartimenti,
    LaboratorioAttivita,
    LaboratorioDatiBase,
    LaboratorioDatiErc1,
    LaboratorioInfrastruttura,
    LaboratorioPersonaleRicerca,
    LaboratorioPersonaleTecnico,
    LaboratorioServiziOfferti,
    LaboratorioTipologiaAttivita,
    LaboratorioUbicazione,
)
from research_lines.models import (
    RicercaAster1,
    RicercaAster2,
    RicercaErc0,
    RicercaErc1,
    RicercaErc2,
)
from django.db.models import Q, Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

class LaboratoriesAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesAreaSerializer
    queryset = LaboratorioDatiBase.objects.all().values("ambito").distinct().order_by("ambito")
    
class LaboratoriesScopesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = LaboratoriesScopesSerializer
    queryset = LaboratorioTipologiaAttivita.objects.all().values("id", "descrizione").distinct().order_by("id")
    
class InfrastructuresViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = InfrastructuresSerializer
    queryset = LaboratorioInfrastruttura.objects.all().values("id", "descrizione").distinct()
    
class ErcListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = Erc1ListSerializer
    queryset = RicercaErc0.objects.all().values("erc0_cod", "description", "description_en").distinct()
    
    def get_queryset(self):
        level = self.kwargs.get("level")
        
        if level == "1":
            for q in self.queryset:
                erc1 = (
                    RicercaErc1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "cod_erc1", "descrizione")
                    .distinct()
                    )

                q["erc1_list"] = [] if len(erc1) == 0 else erc1
                
        elif level == "2":
            for q in self.queryset:
                erc1 = (
                    RicercaErc1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "cod_erc1", "descrizione")
                    .distinct()
                    )

                q["erc1_list"] = [] if len(erc1) == 0 else erc1
                for erc1 in q["erc1_list"]:
                    erc2 = (
                        RicercaErc2.objects.filter(ricerca_erc1_id=erc1["id"])
                        .values("id", "cod_erc2", "descrizione")
                        .distinct()
                        )
                    erc1["erc2_list"] = [] if len(erc2) == 0 else erc2

        return self.queryset
        
    
    def get_serializer(self, *args, **kwargs):
        level = self.kwargs.get("level")
        if level == "1":
            return Erc1ListSerializer(*args, **kwargs)
        elif level == "2":
            return Erc2ListSerializer(*args, **kwargs)
        return Erc0ListSerializer(*args, **kwargs)
        
    
class AsterListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    queryset = RicercaErc0.objects.values("erc0_cod", "description", "description_en")
    
    def get_queryset(self):
        level = self.kwargs.get("level")
        
        if level == "1":
            for q in self.queryset:
                aster1 = (
                    RicercaAster1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "descrizione")
                    .distinct()
                    )

                q["aster1_list"] = [] if len(aster1) == 0 else aster1
                
        elif level == "2":
            for q in self.queryset:
                aster1 = (
                    RicercaAster1.objects.filter(ricerca_erc0_cod=q["erc0_cod"])
                    .values("id", "descrizione")
                    .distinct()
                    )
                q["aster1_list"] = [] if len(aster1) == 0 else aster1
                for aster1 in q["aster1_list"]:
                    aster2 = (
                        RicercaAster2.objects.filter(ricerca_aster1_id=aster1["id"])
                        .values("id", "descrizione")
                        .distinct()
                        )
                    aster1["aster2_list"] = [] if len(aster2) == 0 else aster2

        return self.queryset
        
    
    def get_serializer(self, *args, **kwargs):
        level = self.kwargs.get("level")
        return Aster1ListSerializer(*args, **kwargs) if level == "1" else Aster2ListSerializer(*args, **kwargs)
        